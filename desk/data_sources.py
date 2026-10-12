"""Download raw data for the Data agent. Every value keeps a record of where it came from.

Sources (all free):
- SEC EDGAR: the XBRL data filed with each of Diageo's 20-F annual reports. We read each
  filing's own XBRL file rather than the SEC "company facts" summary, because (found on the
  first real run, Oct 2026) the summary lagged the FY26 20-F by months and leaves out
  Diageo's own tags such as net sales and operating profit before exceptional items.
- Yahoo Finance chart data for share prices (DGE.L in pence) and the FTSE 100 (^FTSE)
- FRED for the US 10-year Treasury yield (DGS10) and GBP/USD (DEXUSUK)

Network hosts needed: data.sec.gov, www.sec.gov, query1.finance.yahoo.com,
query2.finance.yahoo.com, fc.yahoo.com, fred.stlouisfed.org.

If a download fails, functions raise. The Data agent must report the failure and never
replace missing data with estimates.

Usage: python -m desk.data_sources briefs/DGE.yaml runs/DGE/<date>/data
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
SHARE_TAGS = {
    "shares_issued_m": ("ifrs-full:NumberOfSharesIssuedAndFullyPaid", ""),
    "treasury_shares_m": ("ifrs-full:NumberOfSharesOutstanding",
                          "ifrs-full:ComponentsOfEquityAxis=ifrs-full:TreasurySharesMember"),
    "employee_trust_shares_m": ("ifrs-full:NumberOfSharesOutstanding",
                                "ifrs-full:TypesOfSharebasedPaymentArrangementsAxis=deo:EmployeeShareTrustsMember"),
    "weighted_average_shares_m": ("ifrs-full:WeightedAverageShares", ""),
}


def _sec_get(url: str) -> requests.Response:
    r = requests.get(url, headers=SEC_HEADERS, timeout=120)
    r.raise_for_status()
    time.sleep(0.2)  # SEC fair-access limit is 10 requests per second
    return r


def annual_reports(cik: str, count: int = 5) -> list[dict]:
    """The latest `count` 20-F filings (newest first) with their XBRL instance file URL."""
    sub = _sec_get(f"https://data.sec.gov/submissions/CIK{cik.zfill(10)}.json").json()["filings"]["recent"]
    out = []
    for form, acc, doc, period, filed in zip(sub["form"], sub["accessionNumber"], sub["primaryDocument"],
                                             sub["reportDate"], sub["filingDate"]):
        if form != "20-F":
            continue
        folder = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc.replace('-', '')}"
        out.append({"accession": acc, "period_end": period, "filed": filed, "document": f"{folder}/{doc}",
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


def financials(cik: str, years: int = 5) -> pd.DataFrame:
    """Line items for the last `years` fiscal years. Each year is taken from the newest 20-F that
    reports it, so restated comparatives win over the originally filed figure."""
    reports = annual_reports(cik, years)
    rows, seen = [], set()
    for rep in reports:  # newest first
        facts = parse_instance(_sec_get(rep["instance"]).content)
        # this filing's fiscal year and its comparatives (not later dates such as bond maturities)
        ends = sorted({e for e in facts["end"].dropna() if e[5:] == rep["period_end"][5:] and e <= rep["period_end"]},
                      reverse=True)
        for end in ends[:3]:
            fy = int(end[:4])
            for item, tags in TAGS.items():
                if (item, fy) in seen:
                    continue
                for tag in tags:
                    v = _pick(facts, tag, end)
                    if v is not None:
                        rows.append({"item": item, "fiscal_year": fy, "value_musd": v / 1e6, "tag": tag,
                                     "source": f"SEC EDGAR 20-F accession {rep['accession']} filed {rep['filed']} ({rep['document']})"})
                        seen.add((item, fy))
                        break
            for item, (tag, dims) in SHARE_TAGS.items():
                if (item, fy) in seen:
                    continue
                v = _pick(facts, tag, end, dims, unit="shares")
                if v is not None:
                    rows.append({"item": item, "fiscal_year": fy, "value_musd": v / 1e6, "tag": f"{tag} [{dims}]".replace(" []", ""),
                                 "source": f"SEC EDGAR 20-F accession {rep['accession']} filed {rep['filed']} ({rep['document']})"})
                    seen.add((item, fy))
    out = pd.DataFrame(rows).sort_values(["item", "fiscal_year"]).reset_index(drop=True)
    fys = sorted(out["fiscal_year"].unique())[-years:]
    out = out[out["fiscal_year"].isin(fys)]
    out.attrs["missing"] = [f"{i} FY{fy % 100}" for i in list(TAGS) + list(SHARE_TAGS) for fy in fys
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


def main(brief_path: str, out_dir: str) -> None:
    brief = yaml.safe_load(Path(brief_path).read_text())
    co = brief["company"]
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    fin = financials(co["sec_cik"])
    fin.to_csv(out / "financials_raw.csv", index=False)

    px = pd.concat([prices(co["ticker_lse"]), prices(co["benchmark_index"])], axis=1, sort=True)
    px.to_csv(out / "prices.csv")

    rf, fx = fred_series("DGS10"), fred_series("DEXUSUK")
    close = last_close(co["ticker_lse"])
    if close["currency"] != "GBp":
        raise RuntimeError(f"{co['ticker_lse']} is quoted in {close['currency']}, expected GBp (pence)")
    market = {
        "risk_free": {"value": float(rf.iloc[-1]) / 100, "date": str(rf.index[-1].date()),
                      "source": "FRED DGS10 (US 10-year Treasury, constant maturity)"},
        "fx_usd_per_gbp": {"value": float(fx.iloc[-1]), "date": str(fx.index[-1].date()),
                           "source": "FRED DEXUSUK (USD per GBP, noon buying rate New York)"},
        "share_price_gbp_pence": {"value": close["value"], "date": close["date"],
                                  "source": f"Yahoo Finance {co['ticker_lse']} close (pence, GBp)"},
        "downloaded_on": str(date.today()),
    }
    (out / "market_inputs.json").write_text(json.dumps(market, indent=2))
    print(json.dumps({"rows": len(fin), "missing_items": fin.attrs["missing"], **market}, indent=2))


if __name__ == "__main__":
    main(*sys.argv[1:3])
