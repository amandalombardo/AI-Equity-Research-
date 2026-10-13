"""Data agent script (KO, run 2026-10-13): peers.csv and the run-date cross-check of KO's listed equity stakes.

Filing figures: SEC XBRL companyfacts API (10-K FY25 and latest 10-Q). Prices, share-split events and consensus
EPS: Yahoo Finance (non-filing sources, flagged). USD m unless stated.
Run from the repo root:  PYTHONPATH=. python runs/KO/2026-10-13/data/build_peers.py
"""
import datetime as dt
import json
from pathlib import Path

import pandas as pd
import requests

DATA = Path(__file__).resolve().parent
SEC = {"User-Agent": "AI Equity Research Desk student project contact@example.com"}
YH = {"User-Agent": "Mozilla/5.0"}
RUN_DATE = dt.date(2026, 10, 13)
PEERS = {"PEP": "0000077476", "KDP": "0001418135", "MNST": "0000865752"}

# candidate us-gaap tags per item (first one with data wins)
TAGS = {
    "revenue": ["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax"],
    "operating_income": ["OperatingIncomeLoss"],
    "da": ["DepreciationDepletionAndAmortization", "DepreciationAndAmortization"],
    "net_income": ["NetIncomeLoss", "ProfitLoss"],
    "ocf": ["NetCashProvidedByUsedInOperatingActivities"],
    "capex": ["PaymentsToAcquirePropertyPlantAndEquipment", "PaymentsToAcquireProductiveAssets"],
}
BAL = {
    "debt_current": ["ShortTermBorrowings", "DebtCurrent"],          # PEP / KDP: include current maturities of LTD
    "debt_noncurrent": ["LongTermDebtAndCapitalLeaseObligations", "LongTermDebtNoncurrent"],
    "cash": ["CashAndCashEquivalentsAtCarryingValue"],
    "st_investments": ["ShortTermInvestments"],
    "nci": ["MinorityInterest"],
}


def facts(cik):
    r = requests.get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json", headers=SEC, timeout=120)
    r.raise_for_status()
    return r.json()


def series(f, tag):
    g = f["facts"]["us-gaap"].get(tag)
    if not g:
        return []
    return [x for x in list(g["units"].values())[0] if x.get("form") in ("10-K", "10-Q")]


def flow(f, cands, start_year_end, min_days, max_days, latest=True):
    """A duration fact (start->end) for the first tag with data; latest end if `latest`."""
    for tag in cands:
        xs = [x for x in series(f, tag) if x.get("start")
              and min_days <= (pd.Timestamp(x["end"]) - pd.Timestamp(x["start"])).days <= max_days
              and x["start"][:4] in start_year_end]
        if xs:
            xs.sort(key=lambda x: (x["end"], x["filed"]))
            return tag, xs
    return None, []


def ltm(f, cands):
    """LTM = FY25 + latest 2026 year-to-date - same period of 2025 (all from 10-K / 10-Q XBRL)."""
    tag, fy = flow(f, cands, ("2024", "2025"), 350, 380)
    fy = [x for x in fy if x["end"][:4] == "2025"]
    if not fy:
        return None, None, None
    fy25 = fy[-1]
    _, ytd = flow(f, [tag], ("2025", "2026"), 80, 300)
    # 2026 year-to-date periods: start just after the FY25 year end, end in 2026
    ytd26 = [x for x in ytd if x["end"][:4] == "2026"
             and 0 < (pd.Timestamp(x["start"]) - pd.Timestamp(fy25["end"])).days <= 7]
    if not ytd26:
        return fy25["val"] / 1e6, fy25["end"], tag
    cur = max(ytd26, key=lambda x: (x["end"], (pd.Timestamp(x["end"]) - pd.Timestamp(x["start"])).days))
    n = (pd.Timestamp(cur["end"]) - pd.Timestamp(cur["start"])).days
    _, prev = flow(f, [tag], ("2024", "2025"), n - 10, n + 10)
    prev = [x for x in prev if x["start"] == fy25["start"]]
    if not prev:
        return None, None, tag
    return (fy25["val"] + cur["val"] - prev[-1]["val"]) / 1e6, cur["end"], tag


def bal(f, cands, end):
    for tag in cands:
        xs = [x for x in series(f, tag) if not x.get("start") and x["end"] == end]
        if xs:
            return xs[-1]["val"] / 1e6, tag
    return 0.0, None


def yahoo_close(t, start, end):
    p1 = int(dt.datetime.fromisoformat(start).timestamp()); p2 = int(dt.datetime.fromisoformat(end).timestamp())
    r = requests.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{t}",
                     params={"period1": p1, "period2": p2, "interval": "1d", "events": "split"}, headers=YH, timeout=60)
    r.raise_for_status()
    res = r.json()["chart"]["result"][0]
    pts = [(str(dt.date.fromtimestamp(ts)), c) for ts, c in zip(res["timestamp"], res["indicators"]["quote"][0]["close"]) if c]
    splits = {str(dt.date.fromtimestamp(int(k))): v["numerator"] / v["denominator"]
              for k, v in res.get("events", {}).get("splits", {}).items()}
    return pts[-1], res["meta"].get("currency"), splits


def yahoo_eps_consensus(t):
    s = requests.Session(); s.headers.update(YH)
    s.get("https://fc.yahoo.com", timeout=30)
    crumb = s.get("https://query1.finance.yahoo.com/v1/test/getcrumb", timeout=30).text
    r = s.get(f"https://query2.finance.yahoo.com/v10/finance/quoteSummary/{t}",
              params={"modules": "earningsTrend", "crumb": crumb}, timeout=60)
    r.raise_for_status()
    tr = {x["period"]: x for x in r.json()["quoteSummary"]["result"][0]["earningsTrend"]["trend"]}
    return {p: (tr[p]["endDate"], tr[p]["earningsEstimate"]["avg"].get("raw"), tr[p]["revenueEstimate"]["avg"].get("raw"))
            for p in ("0y", "+1y")}


rows = []
for t, cik in PEERS.items():
    f = facts(cik)
    cover = [x for x in f["facts"]["dei"]["EntityCommonStockSharesOutstanding"]["units"]["shares"]][-1]
    (pdate, price), ccy, splits = yahoo_close(t, "2026-01-01", "2026-10-14")
    # Trap: a split after the 10-Q cover date means the cover share count must be scaled to today's price basis
    split_adj = 1.0
    for d, ratio in splits.items():
        if d > cover["end"]:
            split_adj *= ratio
    shares_m = cover["val"] / 1e6 * split_adj
    vals, tags = {}, {}
    for k, c in TAGS.items():
        vals[k], vals[k + "_end"], tags[k] = ltm(f, c)
    if t == "KDP":  # KDP tags depreciation and intangible amortisation separately
        dep, _, _ = ltm(f, ["Depreciation"]); amo, _, _ = ltm(f, ["AmortizationOfIntangibleAssets"])
        vals["da"] = dep + amo; tags["da"] = "Depreciation + AmortizationOfIntangibleAssets"
    bal_end = vals["revenue_end"]
    b = {k: bal(f, c, bal_end) for k, c in BAL.items()}
    debt = b["debt_current"][0] + b["debt_noncurrent"][0]
    cash = b["cash"][0] + b["st_investments"][0]
    mcap = shares_m * price
    ev = mcap + debt - cash + b["nci"][0]  # enterprise value = equity + debt - cash + minorities (leases excluded, as KO)
    ebitda = vals["operating_income"] + vals["da"]  # EBITDA = reported operating income + D&A (GAAP, unadjusted)
    fcf = vals["ocf"] - vals["capex"]
    cons = yahoo_eps_consensus(t)
    w26 = (dt.date(2026, 12, 31) - RUN_DATE).days / 365  # NTM = time-weighted FY26 and FY27 consensus
    eps_ntm = w26 * cons["0y"][1] + (1 - w26) * cons["+1y"][1]
    rows.append({
        "name": {"PEP": "PepsiCo", "KDP": "Keurig Dr Pepper", "MNST": "Monster Beverage"}[t], "ticker": t,
        "fy_end_month": 12, "latest_fy_end": "2025-12-31" if t != "PEP" else "2025-12-27", "ltm_end": bal_end,
        "price_usd": round(price, 2), "price_date": pdate, "shares_m": round(shares_m, 1),
        "market_cap_musd": round(mcap), "net_debt_musd": round(debt - cash), "nci_musd": b["nci"][0],
        "ev_musd": round(ev), "revenue_ltm_musd": round(vals["revenue"]), "ebitda_ltm_musd": round(ebitda),
        "ebitda_ntm_musd": None, "net_income_ltm_musd": round(vals["net_income"]),
        "pe_ltm": round(mcap / vals["net_income"], 2), "eps_ntm_consensus_usd": round(eps_ntm, 3),
        "pe_ntm": round(price / eps_ntm, 2), "fcf_ltm_musd": round(fcf), "fcf_yield_ltm": round(fcf / mcap, 4),
        "ev_ebitda_ltm": round(ev / ebitda, 2),
        "source": (f"SEC EDGAR XBRL companyfacts CIK {cik} (10-K FY25 + latest 10-Q YTD; tags: "
                   + ", ".join(f"{k}={v}" for k, v in tags.items()) + f"; shares dei:EntityCommonStockSharesOutstanding "
                   f"{cover['val']:,} at {cover['end']} accn {cover['accn']}"
                   + (f" x split {split_adj:g} (Yahoo split event)" if split_adj != 1 else "")
                   + f"); price Yahoo {t} close; NTM EPS Yahoo consensus FY26 {cons['0y'][1]} / FY27 {cons['+1y'][1]}"),
        "flag": "non-filing source: price, NTM EPS consensus; ebitda_ntm MISSING (no free EBITDA consensus); EBITDA is GAAP unadjusted",
    })
    if t == "KDP":
        rows[-1]["flag"] += ("; KDP LTM mixes pre/post JDE Peet's acquisition (Q2 2026 revenue 7,309 vs 3,976 in Q1; debt and NCI "
                             "3.9-4.2bn jump in 2026) so LTM multiples are distorted; GAAP net income depressed by deal costs")
    if t == "MNST":
        rows[-1]["flag"] += "; 2-for-1 split 11 Aug 2026 applied to 10-Q cover share count; no debt"
    if t == "PEP":
        rows[-1]["flag"] += "; PEP fiscal year ends last Saturday of Dec (52/53 weeks); LTM to 5 Sep 2026 (Q3 10-Q)"

# optional peers (not computed from filings here)
rows.append({"name": "Coca-Cola Europacific Partners", "ticker": "CCEP", "fy_end_month": 12,
             "source": "Not built: CCEP files 6-K/20-F style reports without XBRL companyfacts; company site blocked from this environment",
             "flag": "MISSING (optional peer, bottler - show separately)"})
rows.append({"name": "Diageo", "ticker": "DEO", "fy_end_month": 6,
             "source": "See runs/DGE/2026-10-12/data/peers.csv and financials.csv (Diageo 20-F FY26); not recomputed here",
             "flag": "optional out-of-sector cross-check; June year end, not calendarised"})
pd.DataFrame(rows).to_csv(DATA / "peers.csv", index=False)
print(pd.DataFrame(rows).drop(columns=["source"]).to_string())

# ---- run-date cross-check of KO's listed equity stakes (NOT the inputs.yaml value: 10-K gives no share counts)
# value_t = fair value at 31 Dec 2025 x (price_t / price_0) x (USD per local currency_t / _0), holdings assumed unchanged
# (Q2 2026 10-Q: disposals of equity method investments only $1m in H1 2026). Yahoo closes are split-adjusted.
stakes = [("Monster", 15659, "MNST", None), ("CCEP", 7163, "CCEP", None), ("Coca-Cola FEMSA", 5543, "KOF", None),
          ("Coca-Cola HBC", 4051, "CCH.L", ("GBPUSD=X", "usd_per")), ("CCBJH", 822, "2579.T", ("JPY=X", "per_usd")),
          ("Coca-Cola Icecek", 770, "CCOLA.IS", ("TRY=X", "per_usd")), ("Andina", 278, "ANDINA-B.SN", ("CLP=X", "per_usd"))]
out = []
for name, fv0, t, fx in stakes:
    (d0, p0), c0, _ = yahoo_close(t, "2025-12-20", "2026-01-01")
    (d1, p1), _, _ = yahoo_close(t, "2026-10-01", "2026-10-14")
    fxr = 1.0
    if fx:
        (_, f0), _, _ = yahoo_close(fx[0], "2025-12-20", "2026-01-01")
        (_, f1), _, _ = yahoo_close(fx[0], "2026-10-01", "2026-10-14")
        fxr = f1 / f0 if fx[1] == "usd_per" else f0 / f1
    out.append({"stake": name, "ticker": t, "currency": c0, "fair_value_31dec25_musd": fv0, "price_31dec25": round(p0, 3),
                "price_date_0": d0, "price_run": round(p1, 3), "price_date_run": d1, "fx_factor": round(fxr, 4),
                "value_run_date_musd": round(fv0 * p1 / p0 * fxr, 1)})
x = pd.DataFrame(out)
x.to_csv(DATA / "associates_rollforward_check.csv", index=False)
print(x.to_string(), "\nTOTAL", x["value_run_date_musd"].sum())
