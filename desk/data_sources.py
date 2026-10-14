"""Download raw data for the Data agent. Every value keeps a record of where it came from.

Sources (all free):
- SEC EDGAR: the XBRL data filed with each annual report (20-F for Diageo, 10-K for US companies). We read each
  filing's own XBRL file rather than the SEC "company facts" summary, because (found on the
  first real run, Oct 2026) the summary lagged the FY26 20-F by months and leaves out
  Diageo's own tags such as net sales and operating profit before exceptional items.
- Yahoo Finance chart data for share prices (DGE.L in pence, KO in US dollars) and the benchmark index
  (FTSE 100 ^FTSE or S&P 500 ^GSPC, set in the brief)
- FRED for the 10-year government bond yield in the reporting currency (US Treasury DGS10, or German Bund IRLTLT01DEM156N for euro reporters) and, for London prices only, the FX rate (DEXUSUK, with DEXUSEU for euro reporters)

Network hosts needed: data.sec.gov, www.sec.gov, query1.finance.yahoo.com,
query2.finance.yahoo.com, fc.yahoo.com, fred.stlouisfed.org.

If a download fails, functions raise. The Data agent must report the failure and never
replace missing data with estimates.

Which XBRL labels are read is set by the brief: company.accounting = "diageo_ifrs" (default), "ifrs" (standard IFRS labels, e.g. Unilever) or "us_gaap".
Amounts are read in the reporting currency (company.reporting_currency) and the output column says which.

Usage: python -m desk.data_sources briefs/<TICKER>.yaml runs/<TICKER>/<date>/data
"""
from __future__ import annotations

import io
import json
import os
import sys
import time
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path

import pandas as pd
import requests
import yaml

from desk.units import fx_key, money_key, price_currency, reporting_currency

# SEC asks automated requests to identify themselves with a contact.
# Set SEC_CONTACT_EMAIL in the environment; SEC refuses requests without a real contact (HTTP 403).
SEC_HEADERS = {"User-Agent": f"AI Equity Research Desk (student project) {os.environ.get('SEC_CONTACT_EMAIL', 'contact@example.com')}"}
# Yahoo refuses requests without a browser-like User-Agent.
YAHOO_HEADERS = {"User-Agent": "Mozilla/5.0 (equity research desk)"}

# Tags to try for each line item, in order of preference. "deo:" tags are Diageo's own
# (extension) tags. The Data agent must still check the chosen tag against the 20-F text.
# Trap: ifrs-full:Revenue is Diageo's "sales" INCLUDING excise duties (c.$28bn); the analysis
# uses NET sales (after excise, c.$20bn), which only exists as Diageo's own deo:NetSales tag.
TAGS = {
    "net_sales": ["deo:NetSales"],
    "sales_incl_excise": ["ifrs-full:Revenue"],
    "excise_duties": ["deo:ExciseDuties"],
    "gross_profit": ["ifrs-full:GrossProfit"],
    "marketing": ["deo:MarketingExpensesBeforeExceptionals", "deo:MarketingExpenses"],
    "operating_profit_bei": ["deo:OperatingProfitLossBeforeExceptionalItems"],
    "exceptional_operating_items": ["deo:ExceptionalOperatingItemsIncludedInOperatingProfitLoss"],
    "operating_profit_reported": ["ifrs-full:ProfitLossFromOperatingActivities"],
    "depreciation_amortisation": ["deo:DepreciationAndIntangibleAssetAmortisationExpense"],
    "depreciation_amortisation_impairment": ["ifrs-full:DepreciationAmortisationAndImpairmentLossReversalOfImpairmentLossRecognisedInProfitOrLoss"],
    "adjusted_ebitda": ["deo:AdjustedEBITDA"],
    "share_of_associates_profit": ["ifrs-full:ShareOfProfitLossOfAssociatesAndJointVenturesAccountedForUsingEquityMethod"],
    "net_finance_charges": ["ifrs-full:FinanceIncomeCost"],
    "net_interest": ["ifrs-full:InterestRevenueExpense"],
    "profit_before_tax": ["ifrs-full:ProfitLossBeforeTax"],
    "income_tax": ["ifrs-full:IncomeTaxExpenseContinuingOperations"],
    "net_profit_to_owners": ["ifrs-full:ProfitLossAttributableToOrdinaryEquityHoldersOfParentEntity",
                             "ifrs-full:ProfitLossAttributableToOwnersOfParent"],
    "operating_cash_flow": ["ifrs-full:CashFlowsFromUsedInOperatingActivities"],
    "capex": ["deo:PurchaseOfPropertyPlantAndEquipmentAndComputerSoftware",
              "ifrs-full:PurchaseOfPropertyPlantAndEquipmentClassifiedAsInvestingActivities"],
    "proceeds_from_ppe_disposals": ["deo:ProceedsFromDisposalOfPropertyPlantAndEquipmentAndComputerSoftware"],
    "dividends_paid_to_shareholders": ["ifrs-full:DividendsPaidToEquityHoldersOfParentClassifiedAsFinancingActivities"],
    "inventories": ["ifrs-full:Inventories"],
    "maturing_inventories": ["deo:MaturingInventories"],
    "trade_and_other_receivables": ["ifrs-full:TradeAndOtherCurrentReceivables"],
    "trade_and_other_payables": ["ifrs-full:TradeAndOtherCurrentPayables"],
    "cash": ["ifrs-full:CashAndCashEquivalents"],
    "net_borrowings": ["ifrs-full:Borrowings"],  # Diageo uses this tag for NET borrowings incl. leases (note 17)
    "gross_borrowings": ["deo:GrossBorrowings"],
    "lease_liabilities": ["ifrs-full:LeaseLiabilities"],
    "adjusted_net_borrowings": ["deo:AdjustedNetBorrowings"],
    "non_controlling_interests": ["ifrs-full:NoncontrollingInterests"],
    "investments_in_associates": ["ifrs-full:InvestmentAccountedForUsingEquityMethod",
                                  "ifrs-full:InvestmentsInAssociatesAccountedForUsingEquityMethod"],
    "post_employment_net_liability": ["ifrs-full:LiabilityAssetOfDefinedBenefitPlans"],
    "post_employment_deficit_plans": ["ifrs-full:NoncurrentRecognisedLiabilitiesDefinedBenefitPlan"],
    "equity_total": ["ifrs-full:Equity"],
    "equity_to_owners": ["ifrs-full:EquityAttributableToOwnersOfParent"],
    "assets_held_for_sale": ["deo:AssetsIncludedInDisposalGroupsClassifiedAsAssetsHeldForSale",
                             "ifrs-full:NoncurrentAssetsOrDisposalGroupsClassifiedAsHeldForSale"],
    "liabilities_held_for_sale": ["ifrs-full:LiabilitiesIncludedInDisposalGroupsClassifiedAsHeldForSale"],
}
# US companies filing a 10-K under US GAAP (written for Coca-Cola, FY25 10-K; checked against its XBRL file).
# Traps: KO's "net operating revenues" are us-gaap:Revenues. Operating income here is REPORTED; the forecast
# base uses the comparable (non-GAAP) margin from the earnings release, which has no XBRL tag.
US_GAAP_TAGS = {
    "net_sales": ["us-gaap:Revenues", "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
    "cost_of_sales": ["us-gaap:CostOfGoodsAndServicesSold"],
    "gross_profit": ["us-gaap:GrossProfit"],
    "sga": ["us-gaap:SellingGeneralAndAdministrativeExpense"],
    "operating_profit_reported": ["us-gaap:OperatingIncomeLoss"],
    "depreciation_amortisation": ["us-gaap:DepreciationDepletionAndAmortization", "us-gaap:DepreciationAndAmortization"],
    "intangible_impairment": ["us-gaap:ImpairmentOfIntangibleAssetsExcludingGoodwill"],
    "share_of_associates_profit": ["us-gaap:IncomeLossFromEquityMethodInvestments"],
    "interest_expense": ["us-gaap:InterestExpenseNonoperating", "us-gaap:InterestExpense"],
    "interest_income": ["us-gaap:InvestmentIncomeInterest"],
    "profit_before_tax": ["us-gaap:IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest"],
    "income_tax": ["us-gaap:IncomeTaxExpenseBenefit"],
    "net_profit_to_owners": ["us-gaap:NetIncomeLoss"],
    "operating_cash_flow": ["us-gaap:NetCashProvidedByUsedInOperatingActivities"],
    "capex": ["us-gaap:PaymentsToAcquirePropertyPlantAndEquipment"],
    "proceeds_from_ppe_disposals": ["us-gaap:ProceedsFromSaleOfPropertyPlantAndEquipment"],
    "dividends_paid_to_shareholders": ["us-gaap:PaymentsOfDividends", "us-gaap:PaymentsOfDividendsCommonStock"],
    "share_buybacks": ["us-gaap:PaymentsForRepurchaseOfCommonStock"],
    "inventories": ["us-gaap:InventoryNet"],
    "trade_and_other_receivables": ["us-gaap:AccountsReceivableNetCurrent"],
    "trade_and_other_payables": ["us-gaap:AccountsPayableAndAccruedLiabilitiesCurrent"],
    "cash": ["us-gaap:CashAndCashEquivalentsAtCarryingValue"],
    "short_term_investments": ["us-gaap:OtherShortTermInvestments", "us-gaap:ShortTermInvestments"],
    "marketable_securities": ["us-gaap:MarketableSecurities", "us-gaap:MarketableSecuritiesCurrent"],
    "short_term_borrowings": ["us-gaap:NotesAndLoansPayable", "us-gaap:ShortTermBorrowings"],
    "long_term_debt_current": ["us-gaap:LongTermDebtAndCapitalLeaseObligationsCurrent", "us-gaap:LongTermDebtCurrent"],
    "long_term_debt_noncurrent": ["us-gaap:LongTermDebtAndCapitalLeaseObligations", "us-gaap:LongTermDebtNoncurrent"],
    "operating_lease_liabilities": ["us-gaap:OperatingLeaseLiability"],
    "non_controlling_interests": ["us-gaap:MinorityInterest"],
    "investments_in_associates": ["us-gaap:EquityMethodInvestments"],
    "equity_to_owners": ["us-gaap:StockholdersEquity"],
    "equity_total": ["us-gaap:StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest"],
    "assets_held_for_sale": ["us-gaap:AssetsOfDisposalGroupIncludingDiscontinuedOperation"],
    "liabilities_held_for_sale": ["us-gaap:LiabilitiesOfDisposalGroupIncludingDiscontinuedOperation"],
    # Coca-Cola's own tag: potential IRS tax and interest liability if it loses the tax case (10-K note 12)
    "irs_potential_liability": ["ko:IncrementalTaxAndInterestLiability"],
}
US_GAAP_SHARE_TAGS = {
    "shares_issued_m": ("us-gaap:CommonStockSharesIssued", ""),
    "treasury_shares_m": ("us-gaap:TreasuryStockCommonShares", ""),
    "weighted_average_shares_m": ("us-gaap:WeightedAverageNumberOfSharesOutstandingBasic", ""),
    "weighted_average_diluted_shares_m": ("us-gaap:WeightedAverageNumberOfDilutedSharesOutstanding", ""),
}
SHARE_TAGS = {
    "shares_issued_m": ("ifrs-full:NumberOfSharesIssuedAndFullyPaid", ""),
    "treasury_shares_m": ("ifrs-full:NumberOfSharesOutstanding",
                          "ifrs-full:ComponentsOfEquityAxis=ifrs-full:TreasurySharesMember"),
    "employee_trust_shares_m": ("ifrs-full:NumberOfSharesOutstanding",
                                "ifrs-full:TypesOfSharebasedPaymentArrangementsAxis=deo:EmployeeShareTrustsMember"),
    "weighted_average_shares_m": ("ifrs-full:WeightedAverageShares", ""),
}
# Companies filing a 20-F with standard IFRS labels only (written for Unilever, FY25 20-F; checked against its XBRL file).
# Traps: Unilever's "turnover" is ifrs-full:Revenue (no excise, unlike Diageo). Operating profit here is REPORTED, after
# restructuring; the forecast base uses underlying operating profit (non-GAAP, results 6-K), which has no XBRL tag.
IFRS_TAGS = {
    "net_sales": ["ifrs-full:Revenue"],
    "operating_profit_reported": ["ifrs-full:ProfitLossFromOperatingActivities"],
    "restructuring": ["ifrs-full:ExpenseOfRestructuringActivities"],
    "depreciation_amortisation": ["ifrs-full:DepreciationAndAmortisationExpense"],
    "share_of_associates_profit": ["ifrs-full:ShareOfProfitLossOfAssociatesAndJointVenturesAccountedForUsingEquityMethod"],
    "net_finance_charges": ["ifrs-full:FinanceIncomeCost"],
    "profit_before_tax": ["ifrs-full:ProfitLossBeforeTax"],
    "income_tax": ["ifrs-full:IncomeTaxExpenseContinuingOperations"],
    "net_profit_to_owners": ["ifrs-full:ProfitLossAttributableToOwnersOfParent"],
    "operating_cash_flow": ["ifrs-full:CashFlowsFromUsedInOperatingActivities"],
    "capex": ["ifrs-full:PurchaseOfPropertyPlantAndEquipmentClassifiedAsInvestingActivities"],
    "capex_intangibles": ["ifrs-full:PurchaseOfIntangibleAssetsClassifiedAsInvestingActivities"],
    "dividends_paid_to_shareholders": ["ifrs-full:DividendsPaidToEquityHoldersOfParentClassifiedAsFinancingActivities"],
    "inventories": ["ifrs-full:Inventories"],
    "trade_and_other_receivables": ["ifrs-full:TradeAndOtherCurrentReceivables"],
    "trade_and_other_payables": ["ifrs-full:TradeAndOtherCurrentPayables"],
    "cash": ["ifrs-full:CashAndCashEquivalents"],
    "other_current_financial_assets": ["ifrs-full:OtherCurrentFinancialAssets"],
    "gross_borrowings": ["ifrs-full:Borrowings"],
    "lease_liabilities": ["ifrs-full:LeaseLiabilities"],
    "non_controlling_interests": ["ifrs-full:NoncontrollingInterests"],
    "investments_in_associates": ["ifrs-full:InvestmentAccountedForUsingEquityMethod"],
    "post_employment_net_liability": ["ifrs-full:LiabilityAssetOfDefinedBenefitPlans"],  # negative = surplus
    "equity_total": ["ifrs-full:Equity"],
    "equity_to_owners": ["ifrs-full:EquityAttributableToOwnersOfParent"],
    "assets_held_for_sale": ["ifrs-full:NoncurrentAssetsOrDisposalGroupsClassifiedAsHeldForSale"],
    "liabilities_held_for_sale": ["ifrs-full:LiabilitiesIncludedInDisposalGroupsClassifiedAsHeldForSale"],
}
IFRS_SHARE_TAGS = {
    "weighted_average_shares_m": ("ifrs-full:WeightedAverageShares", ""),
}
TAG_MAPS = {"diageo_ifrs": (TAGS, SHARE_TAGS), "ifrs": (IFRS_TAGS, IFRS_SHARE_TAGS),
            "us_gaap": (US_GAAP_TAGS, US_GAAP_SHARE_TAGS)}


def tag_map(company: dict) -> tuple[dict, dict]:
    """The line-item and share labels to read, chosen by the brief's company.accounting."""
    key = company.get("accounting", "diageo_ifrs")
    if key not in TAG_MAPS:
        raise SystemExit(f"Unknown company.accounting {key!r}: use one of {sorted(TAG_MAPS)}")
    return TAG_MAPS[key]


def _sec_get(url: str) -> requests.Response:
    r = requests.get(url, headers=SEC_HEADERS, timeout=120)
    r.raise_for_status()
    time.sleep(0.2)  # SEC fair-access limit is 10 requests per second
    return r


def annual_reports(cik: str, count: int = 5, form_type: str = "20-F") -> list[dict]:
    """The latest `count` annual reports (20-F or 10-K, newest first) with their XBRL instance file URL."""
    sub = _sec_get(f"https://data.sec.gov/submissions/CIK{cik.zfill(10)}.json").json()["filings"]["recent"]
    out = []
    for form, acc, doc, period, filed in zip(sub["form"], sub["accessionNumber"], sub["primaryDocument"],
                                             sub["reportDate"], sub["filingDate"]):
        if form != form_type:
            continue
        folder = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc.replace('-', '')}"
        out.append({"form": form, "accession": acc, "period_end": period, "filed": filed, "document": f"{folder}/{doc}",
                    "instance": f"{folder}/{doc.rsplit('.', 1)[0]}_htm.xml"})
        if len(out) == count:
            break
    return out


def parse_instance(xml_bytes: bytes) -> pd.DataFrame:
    """All facts in an XBRL instance: tag (prefix:name), start, end, dimensions, unit, value."""
    root = ET.fromstring(xml_bytes)
    xi = "{http://www.xbrl.org/2003/instance}"
    prefixes = {}
    for _, (prefix, uri) in ET.iterparse(io.BytesIO(xml_bytes), events=["start-ns"]):
        prefixes[uri] = prefix
    contexts = {}
    for c in root.iter(f"{xi}context"):
        p = c.find(f"{xi}period")
        start, end, inst = (p.find(f"{xi}{k}") for k in ("startDate", "endDate", "instant"))
        seg = c.find(f"{xi}entity/{xi}segment")
        dims = ";".join(f"{m.get('dimension')}={(m.text or '').strip()}" for m in seg) if seg is not None else ""
        contexts[c.get("id")] = (start.text if start is not None else None, (end if end is not None else inst).text, dims)
    rows = []
    for el in root:
        ctx = el.get("contextRef")
        if ctx is None or el.text is None:
            continue
        uri, name = el.tag[1:].split("}")
        start, end, dims = contexts[ctx]
        rows.append({"tag": f"{prefixes.get(uri, uri)}:{name}", "start": start, "end": end, "dims": dims,
                     "unit": el.get("unitRef", ""), "value": el.text.strip()})
    return pd.DataFrame(rows)


def _pick(facts: pd.DataFrame, tag: str, end: str, dims: str = "", unit: str = "usd") -> float | None:
    """One value for a tag at a fiscal year end: a full-year amount (flows) or a balance at that date.

    Only facts in `unit` count. Trap: Diageo reported in GBP up to FY23 and in USD from FY24, so
    the FY22 and FY23 20-Fs hold sterling figures. USD figures for those years come from the
    restated comparatives in the FY24 and FY25 20-Fs.
    """
    f = facts[(facts["tag"] == tag) & (facts["end"] == end) & (facts["dims"] == dims)
              & (facts["unit"].str.lower() == unit)]
    if f.empty:
        return None
    if f["start"].notna().any():
        days = (pd.to_datetime(f["end"]) - pd.to_datetime(f["start"])).dt.days
        f = f[f["start"].isna() | (days > 350)]
    vals = pd.to_numeric(f["value"], errors="coerce").dropna().unique()
    if len(vals) == 0:
        return None
    if len(vals) > 1:
        raise ValueError(f"{tag} has conflicting values {vals} at {end}")
    return float(vals[0])


def financials(cik: str, years: int = 5, form_type: str = "20-F", tags: dict | None = None,
               share_tags: dict | None = None, currency: str = "USD") -> pd.DataFrame:
    """Line items for the last `years` fiscal years, in millions of `currency` (the reporting currency; column
    value_m<currency>, e.g. value_musd). Each year is taken from the newest annual report that reports it, so
    restated comparatives win over the originally filed figure."""
    col = money_key("value", currency)
    tags = TAGS if tags is None else tags
    share_tags = SHARE_TAGS if share_tags is None else share_tags
    reports = annual_reports(cik, years, form_type)
    rows, seen = [], set()
    for rep in reports:  # newest first
        facts = parse_instance(_sec_get(rep["instance"]).content)
        # this filing's fiscal year and its comparatives (not later dates such as bond maturities)
        ends = sorted({e for e in facts["end"].dropna() if e[5:] == rep["period_end"][5:] and e <= rep["period_end"]},
                      reverse=True)
        for end in ends[:3]:
            fy = int(end[:4])
            for item, candidates in tags.items():
                if (item, fy) in seen:
                    continue
                for tag in candidates:
                    v = _pick(facts, tag, end, unit=currency.lower())
                    if v is not None:
                        rows.append({"item": item, "fiscal_year": fy, col: v / 1e6, "tag": tag,
                                     "source": f"SEC EDGAR {rep['form']} accession {rep['accession']} filed {rep['filed']} ({rep['document']})"})
                        seen.add((item, fy))
                        break
            for item, (tag, dims) in share_tags.items():
                if (item, fy) in seen:
                    continue
                v = _pick(facts, tag, end, dims, unit="shares")
                if v is not None:
                    rows.append({"item": item, "fiscal_year": fy, col: v / 1e6, "tag": f"{tag} [{dims}]".replace(" []", ""),
                                 "source": f"SEC EDGAR {rep['form']} accession {rep['accession']} filed {rep['filed']} ({rep['document']})"})
                    seen.add((item, fy))
    out = pd.DataFrame(rows).sort_values(["item", "fiscal_year"]).reset_index(drop=True)
    fys = sorted(out["fiscal_year"].unique())[-years:]
    out = out[out["fiscal_year"].isin(fys)]
    out.attrs["missing"] = [f"{i} FY{fy % 100}" for i in list(tags) + list(share_tags) for fy in fys
                            if (i, fy) not in seen]
    return out


def prices(ticker: str, years: int = 5) -> pd.Series:
    """Daily closes adjusted for dividends and splits (for returns), from Yahoo Finance chart data."""
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{requests.utils.quote(ticker)}"
    r = requests.get(url, params={"range": f"{years}y", "interval": "1d"}, headers=YAHOO_HEADERS, timeout=60)
    r.raise_for_status()
    res = r.json()["chart"]["result"][0]
    adj = res["indicators"]["adjclose"][0]["adjclose"]
    idx = pd.to_datetime(res["timestamp"], unit="s").normalize()
    s = pd.Series(adj, index=idx, name=ticker, dtype=float).dropna()
    if s.empty:
        raise RuntimeError(f"no price data for {ticker}")
    s.attrs["currency"] = res["meta"].get("currency")
    return s[~s.index.duplicated(keep="last")]


def last_close(ticker: str) -> dict:
    """The latest actual (unadjusted) close and its currency. Use this, not an adjusted series, as the share price."""
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{requests.utils.quote(ticker)}"
    r = requests.get(url, params={"range": "5d", "interval": "1d"}, headers=YAHOO_HEADERS, timeout=60)
    r.raise_for_status()
    res = r.json()["chart"]["result"][0]
    closes = [(t, c) for t, c in zip(res["timestamp"], res["indicators"]["quote"][0]["close"]) if c is not None]
    t, c = closes[-1]
    return {"value": float(c), "date": str(pd.to_datetime(t, unit="s").date()), "currency": res["meta"].get("currency")}


def fred_series(series_id: str) -> pd.Series:
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    df = pd.read_csv(io.StringIO(r.text))
    df.columns = ["date", series_id]
    df[series_id] = pd.to_numeric(df[series_id], errors="coerce")
    df = df.dropna()
    return df.set_index(pd.to_datetime(df["date"]))[series_id]


# risk-free rate by reporting currency: 10-year government bond yields on FRED
RISK_FREE = {"USD": ("DGS10", "US 10-year Treasury, constant maturity, daily"),
             "EUR": ("IRLTLT01DEM156N", "German 10-year Bund yield, OECD monthly average")}


def price_ticker(company: dict) -> str:
    """The listing whose price the valuation compares with: company.price_ticker, else the London ticker."""
    return company.get("price_ticker") or company["ticker_lse"]


def main(brief_path: str, out_dir: str) -> None:
    brief = yaml.safe_load(Path(brief_path).read_text())
    co = brief["company"]
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    tags, share_tags = tag_map(co)
    rep = reporting_currency(co)
    fin = financials(co["sec_cik"], form_type=co.get("annual_form", "20-F"), tags=tags, share_tags=share_tags,
                     currency=rep)
    fin.to_csv(out / "financials_raw.csv", index=False)

    ticker, ccy = price_ticker(co), price_currency(co)
    px = pd.concat([prices(ticker), prices(co["benchmark_index"])], axis=1, sort=True)
    px.to_csv(out / "prices.csv")

    # the risk-free rate is in the currency of the cash flows (the reporting currency), not of the share price
    rf_id, rf_name = RISK_FREE[rep]
    rf = fred_series(rf_id)
    close = last_close(ticker)
    if close["currency"] != ccy:
        raise RuntimeError(f"{ticker} is quoted in {close['currency']}, expected {ccy} (brief company.price_currency)")
    market = {
        "risk_free": {"value": float(rf.iloc[-1]) / 100, "date": str(rf.index[-1].date()), "source": f"FRED {rf_id} ({rf_name})"},
        "downloaded_on": str(date.today()),
    }
    if ccy == "GBp":
        usd_gbp = fred_series("DEXUSUK")
        if rep == "USD":
            fx, fx_src = usd_gbp, "FRED DEXUSUK (USD per GBP, noon buying rate New York)"
        else:
            # EUR per GBP = (USD per GBP) / (USD per EUR), both noon buying rates on the same day
            both = pd.concat([usd_gbp, fred_series("DEXUSEU")], axis=1, join="inner").dropna()
            fx, fx_src = both.iloc[:, 0] / both.iloc[:, 1], "FRED DEXUSUK / DEXUSEU (EUR per GBP, noon buying rates New York)"
        market[fx_key(rep)] = {"value": float(fx.iloc[-1]), "date": str(fx.index[-1].date()), "source": fx_src}
        market["share_price_gbp_pence"] = {"value": close["value"], "date": close["date"],
                                           "source": f"Yahoo Finance {ticker} close (pence, GBp)"}
    else:
        market["share_price_usd"] = {"value": close["value"], "date": close["date"],
                                     "source": f"Yahoo Finance {ticker} close (US dollars)"}
    (out / "market_inputs.json").write_text(json.dumps(market, indent=2))
    print(json.dumps({"rows": len(fin), "missing_items": fin.attrs["missing"], **market}, indent=2))


if __name__ == "__main__":
    main(*sys.argv[1:3])
