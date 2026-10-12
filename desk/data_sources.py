"""Download raw data for the Data agent. Every value keeps a record of where it came from.

Sources (all free):
- SEC EDGAR XBRL "company facts" for Diageo's 20-F filings (IFRS tags)
- Yahoo Finance via yfinance for share prices (DGE.L in pence) and the FTSE 100 (^FTSE)
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
from pathlib import Path

import pandas as pd
import requests
import yaml

# SEC asks automated requests to identify themselves with a contact.
# Set SEC_CONTACT_EMAIL in the environment; SEC may refuse requests without a real contact.
SEC_HEADERS = {"User-Agent": f"AI Equity Research Desk (student project) {os.environ.get('SEC_CONTACT_EMAIL', 'contact@example.com')}"}

# IFRS tags to try for each line item, in order of preference. The Data agent must check the
# chosen tag against the 20-F text, because companies sometimes use their own extension tags.
IFRS_TAGS = {
    "revenue": ["Revenue", "RevenueFromContractsWithCustomers"],
    "operating_profit": ["ProfitLossFromOperatingActivities"],
    "net_profit_to_owners": ["ProfitLossAttributableToOwnersOfParent"],
    "depreciation_amortisation": ["DepreciationAndAmortisationExpense", "DepreciationAmortisationAndImpairmentLossReversalOfImpairmentLossRecognisedInProfitOrLoss"],
    "capex": ["PurchaseOfPropertyPlantAndEquipmentClassifiedAsInvestingActivities"],
    "operating_cash_flow": ["CashFlowsFromUsedInOperatingActivities"],
    "inventories": ["Inventories"],
    "income_tax": ["IncomeTaxExpenseContinuingOperations"],
    "profit_before_tax": ["ProfitLossBeforeTax"],
    "finance_costs": ["FinanceCosts"],
    "non_controlling_interests": ["NoncontrollingInterests"],
    "investments_in_associates": ["InvestmentsInAssociatesAccountedForUsingEquityMethod"],
    "lease_liabilities": ["LeaseLiabilities"],
    "equity": ["Equity"],
}


def sec_company_facts(cik: str) -> dict:
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik.zfill(10)}.json"
    r = requests.get(url, headers=SEC_HEADERS, timeout=60)
    r.raise_for_status()
    return r.json()


def annual_series(facts: dict, tags: list[str], unit: str = "USD") -> pd.DataFrame:
    """Annual values (from 20-F filings) for the first tag that exists, with source details.

    Keeps the most recently filed value for each fiscal period end, so restated figures win.
    """
    ifrs = facts.get("facts", {}).get("ifrs-full", {})
    for tag in tags:
        if tag not in ifrs or unit not in ifrs[tag].get("units", {}):
            continue
        rows = [x for x in ifrs[tag]["units"][unit] if x.get("form", "").startswith("20-F")]
        if not rows:
            continue
        df = pd.DataFrame(rows)
        # annual duration items have a start date about a year before the end; instants have none
        if "start" in df:
            days = (pd.to_datetime(df["end"]) - pd.to_datetime(df["start"])).dt.days
            df = df[(days > 350) | df["start"].isna()]
        df = df.sort_values("filed").groupby("end").tail(1).sort_values("end")
        df["tag"] = tag
        df["source"] = "SEC EDGAR " + df["form"] + " accession " + df["accn"] + " filed " + df["filed"]
        return df[["end", "val", "tag", "source"]]
    raise KeyError(f"none of the tags {tags} found in 20-F data")


def financials(cik: str) -> pd.DataFrame:
    facts = sec_company_facts(cik)
    frames, missing = [], []
    for item, tags in IFRS_TAGS.items():
        try:
            df = annual_series(facts, tags)
            df.insert(0, "item", item)
            frames.append(df)
        except KeyError:
            missing.append(item)
    out = pd.concat(frames, ignore_index=True)
    out["val_musd"] = out["val"] / 1e6
    out.attrs["missing"] = missing
    return out


def prices(ticker: str, years: int = 5) -> pd.Series:
    import yfinance as yf
    df = yf.download(ticker, period=f"{years}y", interval="1d", auto_adjust=True, progress=False)
    if df.empty:
        raise RuntimeError(f"no price data for {ticker}")
    close = df["Close"]
    return (close.iloc[:, 0] if isinstance(close, pd.DataFrame) else close).rename(ticker)


def fred_series(series_id: str) -> pd.Series:
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    df = pd.read_csv(io.StringIO(r.text))
    df.columns = ["date", series_id]
    df[series_id] = pd.to_numeric(df[series_id], errors="coerce")
    return df.dropna().set_index(pd.to_datetime(df.dropna()["date"]))[series_id]


def main(brief_path: str, out_dir: str) -> None:
    brief = yaml.safe_load(Path(brief_path).read_text())
    co = brief["company"]
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    fin = financials(co["sec_cik"])
    fin.to_csv(out / "financials_raw.csv", index=False)

    px = pd.concat([prices(co["ticker_lse"]), prices(co["benchmark_index"])], axis=1)
    px.to_csv(out / "prices.csv")

    rf, fx = fred_series("DGS10"), fred_series("DEXUSUK")
    market = {
        "risk_free": {"value": float(rf.iloc[-1]) / 100, "date": str(rf.index[-1].date()),
                      "source": "FRED DGS10 (US 10-year Treasury, constant maturity)"},
        "fx_usd_per_gbp": {"value": float(fx.iloc[-1]), "date": str(fx.index[-1].date()),
                           "source": "FRED DEXUSUK (USD per GBP)"},
        "share_price_gbp_pence": {"value": float(px[co["ticker_lse"]].dropna().iloc[-1]),
                                  "date": str(px[co["ticker_lse"]].dropna().index[-1].date()),
                                  "source": f"Yahoo Finance {co['ticker_lse']} close (pence)"},
    }
    (out / "market_inputs.json").write_text(json.dumps(market, indent=2))
    print(json.dumps({"rows": len(fin), "missing_items": fin.attrs["missing"], **market}, indent=2))


if __name__ == "__main__":
    main(*sys.argv[1:3])
