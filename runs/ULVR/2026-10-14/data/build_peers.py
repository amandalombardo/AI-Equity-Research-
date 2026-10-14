"""Data agent script (ULVR, run 2026-10-14): peers.csv for the comps agent.

US peers (PG, CL, KMB): filing figures from the SEC XBRL companyfacts API (latest 10-K + latest 10-Q year-to-date,
LTM = last fiscal year + current YTD - prior-year YTD). Price and consensus EPS from Yahoo (non-filing, flagged).
European peers (RKT.L, BEI.DE, OR.PA, HEN3.DE) and the optional HINDUNILVR.NS: no SEC filings, so every figure is
Yahoo Finance quoteSummary (financialData / defaultKeyStatistics / earningsTrend) -> flag: non-filing source.
Amounts in millions of each company's own currency (column `ccy`); multiples are currency-free.
Run from the repo root:  python runs/ULVR/2026-10-14/data/build_peers.py
"""
import datetime as dt
import os
from pathlib import Path

import pandas as pd
import requests

DATA = Path(__file__).resolve().parent
SEC = {"User-Agent": f"AI Equity Research Desk {os.environ.get('SEC_CONTACT_EMAIL', 'contact@example.com')}"}
YH = {"User-Agent": "Mozilla/5.0"}
RUN_DATE = dt.date(2026, 10, 14)
PRICE_DATE = "2026-10-13"   # last completed close before the run date (London/European markets were still open)

US = {"PG": ("Procter & Gamble", "0000080424", 6), "CL": ("Colgate-Palmolive", "0000021665", 12),
      "KMB": ("Kimberly-Clark", "0000055785", 12)}
EU = {"RKT.L": ("Reckitt Benckiser", 12), "BEI.DE": ("Beiersdorf", 12), "OR.PA": ("L'Oreal", 12),
      "HEN3.DE": ("Henkel", 12)}
OPTIONAL = {"HINDUNILVR.NS": ("Hindustan Unilever", 3)}

TAGS = {
    "revenue": ["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax", "SalesRevenueNet"],
    "operating_income": ["OperatingIncomeLoss"],
    "da": ["DepreciationDepletionAndAmortization", "DepreciationAndAmortization", "DepreciationAmortizationAndAccretionNet"],
    "net_income": ["NetIncomeLoss"],
    "ocf": ["NetCashProvidedByUsedInOperatingActivities"],
    "capex": ["PaymentsToAcquirePropertyPlantAndEquipment", "PaymentsToAcquireProductiveAssets"],
}
BAL = {
    "debt_current": ["DebtCurrent", "ShortTermBorrowingsAndCurrentPortionOfLongTermDebt", "LongTermDebtCurrentAndShortTermBorrowings",
                     "ShortTermBankLoansAndNotesPayable"],  # CL: bank loans/notes only (no current LTD tagged at 30 Jun 2026)
    "debt_noncurrent": ["LongTermDebtNoncurrent", "LongTermDebtAndCapitalLeaseObligations"],
    "cash": ["CashAndCashEquivalentsAtCarryingValue", "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents"],  # PG: 2nd tag
    "st_investments": ["ShortTermInvestments", "AvailableForSaleSecuritiesDebtSecuritiesCurrent"],
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
    return [x for x in g["units"].get("USD", []) if x.get("form") in ("10-K", "10-Q")]


def days(x):
    return (pd.Timestamp(x["end"]) - pd.Timestamp(x["start"])).days


def ltm(f, cands):
    """LTM = latest fiscal year + latest year-to-date after it - same period a year earlier (10-K / 10-Q XBRL)."""
    for tag in cands:
        xs = [x for x in series(f, tag) if x.get("start")]
        fys = [x for x in xs if 350 <= days(x) <= 380 and x["form"] == "10-K"]
        if not fys:
            continue
        fy = max(fys, key=lambda x: (x["end"], x["filed"]))
        if fy["end"] < "2025-06-01":   # stale tag (company switched tags)
            continue
        ytd = [x for x in xs if 0 < (pd.Timestamp(x["start"]) - pd.Timestamp(fy["end"])).days <= 7 and days(x) < 350]
        if not ytd:
            return fy["val"] / 1e6, fy["end"], tag, "FY"
        cur = max(ytd, key=lambda x: (x["end"], days(x)))
        prev = [x for x in xs if x["start"] == fy["start"] and abs(days(x) - days(cur)) <= 10]
        if not prev:
            return None, None, tag, "prior YTD missing"
        return (fy["val"] + cur["val"] - prev[-1]["val"]) / 1e6, cur["end"], tag, "LTM"
    return None, None, None, "no tag"


def bal(f, cands, end):
    for tag in cands:
        xs = [x for x in series(f, tag) if not x.get("start") and x["end"] == end]
        if xs:
            return xs[-1]["val"] / 1e6, tag
    return 0.0, None


def yahoo_close(t, day):
    p1 = int(dt.datetime.fromisoformat("2026-10-01").timestamp())
    p2 = int(dt.datetime.fromisoformat(day).timestamp()) + 86400
    r = requests.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{t}",
                     params={"period1": p1, "period2": p2, "interval": "1d"}, headers=YH, timeout=60)
    r.raise_for_status()
    res = r.json()["chart"]["result"][0]
    pts = [(str(dt.datetime.fromtimestamp(ts, dt.timezone.utc).date()), c) for ts, c in
           zip(res["timestamp"], res["indicators"]["quote"][0]["close"]) if c]
    pts = [p for p in pts if p[0] <= day]
    return pts[-1], res["meta"].get("currency")


_S = None


def quote_summary(t):
    global _S
    if _S is None:
        _S = requests.Session(); _S.headers.update(YH)
        _S.get("https://fc.yahoo.com", timeout=30)
        _S.crumb = _S.get("https://query1.finance.yahoo.com/v1/test/getcrumb", timeout=30).text
    r = _S.get(f"https://query2.finance.yahoo.com/v10/finance/quoteSummary/{t}",
               params={"modules": "financialData,defaultKeyStatistics,summaryDetail,earningsTrend,price",
                       "crumb": _S.crumb}, timeout=60)
    r.raise_for_status()
    return r.json()["quoteSummary"]["result"][0]


def raw(d, k):
    v = d.get(k)
    return v.get("raw") if isinstance(v, dict) else v


def eps_ntm(q, fy_end_month):
    """NTM EPS = time-weighted current and next fiscal-year consensus (Yahoo earningsTrend '0y' and '+1y')."""
    tr = {x["period"]: x for x in q["earningsTrend"]["trend"]}
    e0, e1 = raw(tr["0y"]["earningsEstimate"], "avg"), raw(tr["+1y"]["earningsEstimate"], "avg")
    end0 = dt.date.fromisoformat(tr["0y"]["endDate"])
    if e0 is None or e1 is None:
        return None, None, None, None
    w0 = max(0.0, min(1.0, (end0 - RUN_DATE).days / 365))
    return w0 * e0 + (1 - w0) * e1, e0, e1, tr["0y"]["endDate"]


rows = []
for t, (name, cik, fym) in US.items():
    f = facts(cik)
    cover = f["facts"]["dei"]["EntityCommonStockSharesOutstanding"]["units"]["shares"][-1]
    (pdate, price), ccy = yahoo_close(t, PRICE_DATE)
    shares_m = cover["val"] / 1e6
    vals, tags, kinds = {}, {}, {}
    for k, c in TAGS.items():
        vals[k], vals[k + "_end"], tags[k], kinds[k] = ltm(f, c)
    bal_end = vals["revenue_end"]
    b = {k: bal(f, c, bal_end) for k, c in BAL.items()}
    debt = b["debt_current"][0] + b["debt_noncurrent"][0]
    cash = b["cash"][0] + b["st_investments"][0]
    mcap = shares_m * price
    ev = mcap + debt - cash + b["nci"][0]          # enterprise value = equity + debt - cash + minorities (leases excluded)
    ebitda = vals["operating_income"] + vals["da"]  # EBITDA = reported operating income + D&A (GAAP, unadjusted)
    fcf = vals["ocf"] - vals["capex"]               # free cash flow = operating cash flow - capex
    q = quote_summary(t)
    ntm, e0, e1, end0 = eps_ntm(q, fym)
    rows.append({
        "name": name, "ticker": t, "ccy": "USD", "fy_end_month": fym, "ltm_end": bal_end,
        "price": round(price, 2), "price_date": pdate, "shares_m": round(shares_m, 1), "market_cap_m": round(mcap),
        "net_debt_m": round(debt - cash), "nci_m": round(b["nci"][0]), "ev_m": round(ev),
        "revenue_ltm_m": round(vals["revenue"]), "ebitda_ltm_m": round(ebitda), "ebitda_ntm_m": None,
        "net_income_ltm_m": round(vals["net_income"]), "pe_ltm": round(mcap / vals["net_income"], 2),
        "eps_ntm_consensus": round(ntm, 3) if ntm else None, "pe_ntm": round(price / ntm, 2) if ntm else None,
        "fcf_ltm_m": round(fcf), "fcf_yield_ltm": round(fcf / mcap, 4), "ev_ebitda_ltm": round(ev / ebitda, 2),
        "source": (f"SEC EDGAR XBRL companyfacts CIK {cik} (latest 10-K + 10-Q YTD; tags: "
                   + ", ".join(f"{k}={v} ({kinds[k]})" for k, v in tags.items())
                   + f"; debt={b['debt_current'][1]}+{b['debt_noncurrent'][1]}, cash={b['cash'][1]}+{b['st_investments'][1]}"
                   + f"; shares dei:EntityCommonStockSharesOutstanding {cover['val']:,} at {cover['end']} accn {cover['accn']})"
                   + f"; price Yahoo {t} close {pdate}; NTM EPS Yahoo consensus FY to {end0}: {e0} / next FY: {e1}"),
        "flag": "flag: non-filing source (price, NTM EPS consensus); ebitda_ntm MISSING (no free EBITDA consensus); "
                "EBITDA is GAAP unadjusted",
    })
    if t == "PG":
        rows[-1]["flag"] += "; PG fiscal year ends 30 June: LTM = FY26 (to 30 Jun 2026), Q1 FY27 10-Q not yet filed"
    if t == "KMB":
        rows[-1]["flag"] += ("; DISTORTED: pending acquisition of Kenvue (merger agreement 2 Nov 2025, KMB Q2 2026 10-Q note 4; "
                             "Kenvue note exchange offers under way, 8-Ks 0001104659-26-111354 and 0001104659-26-115239) and "
                             "pending IFP joint venture with Suzano (held for sale): the price reflects the merger, LTM figures do not")
    if t == "CL":
        rows[-1]["flag"] += ("; current debt = ShortTermBankLoansAndNotesPayable only (no current long-term debt tagged at 30 Jun 2026)"
                             "; GAAP EBITDA and net income LTM (to 30 Jun 2026) depressed by the Q4 2025 skin health (Filorga) impairment, USD 919m pre-tax / 794m after tax "
                             "(CL FY25 10-K, accession 0000021665-26-000006): EV/EBITDA LTM and P/E LTM overstated, prefer P/E NTM")

for t, (name, fym) in {**EU, **OPTIONAL}.items():
    q = quote_summary(t)
    fd, ks, sd, pr = q["financialData"], q["defaultKeyStatistics"], q["summaryDetail"], q["price"]
    (pdate, price), ccy = yahoo_close(t, PRICE_DATE)
    fin_ccy = raw(fd, "financialCurrency")
    shares_m = raw(ks, "sharesOutstanding") / 1e6
    px = price / 100 if ccy == "GBp" else price      # London quotes in pence: convert to pounds
    mcap = shares_m * px
    extra = ""
    if t == "HEN3.DE":
        # Trap: HEN3 is Henkel's PREFERRED share line only; market cap = ordinary (HEN.DE) + preferred shares at their own prices
        q2 = quote_summary("HEN.DE")
        (pd2, p2), _ = yahoo_close("HEN.DE", PRICE_DATE)
        s2 = raw(q2["defaultKeyStatistics"], "sharesOutstanding") / 1e6
        mcap += s2 * p2
        extra = f"; market cap = preferred {shares_m:.1f}m x {price:.2f} + ordinary {s2:.1f}m x HEN.DE {p2:.2f} ({pd2})"
        shares_m += s2
    debt, cash = raw(fd, "totalDebt") / 1e6, raw(fd, "totalCash") / 1e6
    ev = mcap + debt - cash                          # minorities not available from this source (small for these peers)
    ebitda, ni = raw(fd, "ebitda") / 1e6, raw(ks, "netIncomeToCommon") / 1e6
    fcf = raw(fd, "freeCashflow") / 1e6 if raw(fd, "freeCashflow") is not None else None  # Yahoo 'levered' FCF
    ntm, e0, e1, end0 = eps_ntm(q, fym)
    flag = ("fcf MISSING (Yahoo gives no FCF); " if fcf is None else "") + "flag: non-filing source (all figures Yahoo Finance; EBITDA, debt, cash, FCF are Yahoo LTM figures, not checked to the annual report)"
    if fin_ccy and fin_ccy != (ccy.upper() if ccy != "GBp" else "GBP"):
        flag += f"; financials in {fin_ccy}, price in {ccy}: P/E and FCF yield use Yahoo's own ratios"
    rows.append({
        "name": name, "ticker": t, "ccy": fin_ccy, "fy_end_month": fym,
        "ltm_end": str(dt.datetime.fromtimestamp(raw(ks, "mostRecentQuarter"), dt.timezone.utc).date()) if raw(ks, "mostRecentQuarter") else None,
        "price": round(price, 2), "price_date": pdate, "shares_m": round(shares_m, 1), "market_cap_m": round(mcap),
        "net_debt_m": round(debt - cash), "nci_m": None, "ev_m": round(ev),
        "revenue_ltm_m": round(raw(fd, "totalRevenue") / 1e6), "ebitda_ltm_m": round(ebitda), "ebitda_ntm_m": None,
        "net_income_ltm_m": round(ni), "pe_ltm": round(mcap / ni, 2),
        "eps_ntm_consensus": round(ntm, 3) if ntm else None, "pe_ntm": round(px / ntm, 2) if ntm else None,  # pref price / EPS for Henkel
        "fcf_ltm_m": round(fcf) if fcf is not None else None,
        "fcf_yield_ltm": round(fcf / mcap, 4) if fcf is not None else None, "ev_ebitda_ltm": round(ev / ebitda, 2),
        "source": (f"Yahoo Finance quoteSummary {t} (financialData: ebitda, totalDebt, totalCash, freeCashflow, totalRevenue; "
                   f"defaultKeyStatistics: sharesOutstanding, netIncomeToCommon; earningsTrend FY to {end0}: {e0} / next FY: {e1}); "
                   f"price Yahoo {t} close {pdate} ({ccy}){extra}. Annual report not reachable from this environment (company sites blocked)"),
        "flag": flag + ({"RKT.L": "; Yahoo LTM net income may include disposal gains or impairments (not checked): treat P/E LTM with care",
                         "HEN3.DE": "; Henkel has two share lines (ordinary HEN.DE + preferred HEN3.DE): market cap uses both; P/E NTM uses the preferred price"}.get(t, "")) + ("; OPTIONAL: Unilever's 61.9%-owned subsidiary, show separately, not in the median" if t in OPTIONAL else ""),
    })

out = pd.DataFrame(rows)
out.to_csv(DATA / "peers.csv", index=False)
print(out.drop(columns=["source"]).to_string())
