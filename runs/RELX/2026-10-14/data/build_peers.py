"""Data agent script (RELX, run 2026-10-14): peers.csv for the comps agent.

SEC peers (TRI, VRSK, SPGI, MCO): filing figures read from each filing's own XBRL instance (desk.data_sources.parse_instance),
not the SEC companyfacts summary (which lagged: VRSK and SPGI stopped at Q1 2026 there). LTM to 30 Jun 2026 =
FY25 (10-K / 40-F) + H1 2026 year-to-date - H1 2025 year-to-date (both from the Q2 10-Q / Thomson Reuters H1 6-K).
Price and NTM EPS consensus from Yahoo (non-filing, flagged). European peers (WKL.AS, EXPN.L, LSEG.L) and the optional
INF.L: no SEC filings and company sites are blocked here, so every figure is Yahoo Finance -> flag: non-filing source.
Amounts in millions of each company's reporting currency (column `ccy`); multiples are currency-free.
Run from the repo root:  SEC_CONTACT_EMAIL=... PYTHONPATH=. python runs/RELX/2026-10-14/data/build_peers.py
"""
import datetime as dt
from pathlib import Path

import pandas as pd
import requests

from desk.data_sources import _sec_get, fred_series, parse_instance

DATA = Path(__file__).resolve().parent
YH = {"User-Agent": "Mozilla/5.0"}
RUN_DATE = dt.date(2026, 10, 14)
PRICE_DATE = "2026-10-13"   # 13 Oct 2026 close, same date as the RELX price
A = "https://www.sec.gov/Archives/edgar/data"

# name, ticker, CIK, FY-end month, annual instance, H1 2026 instance, H1 document
SEC_PEERS = {
    "TRI": ("Thomson Reuters", "1075124", 12, f"{A}/1075124/000119312526094222/tri-20251231_htm.xml",
            f"{A}/1075124/000119312526338256/tri-20260630_htm.xml", "40-F 0001193125-26-094222; H1 6-K 0001193125-26-338256"),
    "VRSK": ("Verisk Analytics", "1442145", 12, f"{A}/1442145/000143774926004452/vrsk20251231_10k_htm.xml",
             f"{A}/1442145/000143774926024749/vrsk20260630_10q_htm.xml", "10-K 0001437749-26-004452; Q2 10-Q 0001437749-26-024749"),
    "SPGI": ("S&P Global", "64040", 12, f"{A}/64040/000006404026000013/spgi-20251231_htm.xml",
             f"{A}/64040/000006404026000045/spgi-20260630_htm.xml", "10-K 0000064040-26-000013; Q2 10-Q 0000064040-26-000045"),
    "MCO": ("Moody's", "1059556", 12, f"{A}/1059556/000162828026009136/mco-20251231_htm.xml",
            f"{A}/1059556/000162828026049398/mco-20260630_htm.xml", "10-K 0001628280-26-009136; Q2 10-Q 0001628280-26-049398"),
}
# flows: each option is a list of tags that are SUMMED; the first option with all tags present wins
FLOWS = {
    "revenue": [["us-gaap:Revenues"], ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"], ["ifrs-full:Revenue"]],
    "operating_income": [["us-gaap:OperatingIncomeLoss"], ["ifrs-full:ProfitLossFromOperatingActivities"]],
    "da": [["us-gaap:DepreciationDepletionAndAmortization"], ["us-gaap:DepreciationAndAmortization"],
           ["us-gaap:Depreciation", "us-gaap:AmortizationOfIntangibleAssets"],
           ["ifrs-full:DepreciationExpense", "tri:AmortizationOfComputerSoftware", "tri:AmortizationOfOtherIdentifiableIntangibleAssets"]],
    "net_income": [["us-gaap:NetIncomeLoss"], ["ifrs-full:ProfitLossAttributableToOwnersOfParent"]],
    "ocf": [["us-gaap:NetCashProvidedByUsedInOperatingActivities"], ["ifrs-full:CashFlowsFromUsedInOperatingActivities"]],
    "capex": [["us-gaap:PaymentsToAcquirePropertyPlantAndEquipment"], ["us-gaap:PaymentsToAcquireProductiveAssets"],
              ["ifrs-full:PurchaseOfPropertyPlantAndEquipmentClassifiedAsInvestingActivities"]],
}
BALANCES = {
    "debt": [["us-gaap:LongTermDebt"], ["us-gaap:DebtCurrent", "us-gaap:LongTermDebtAndCapitalLeaseObligations"],
             ["us-gaap:LongTermDebtCurrent", "us-gaap:LongTermDebtNoncurrent"], ["ifrs-full:ShorttermBorrowings", "ifrs-full:LongtermBorrowings"]],
    "short_term_borrowings": [["us-gaap:CommercialPaper"], ["us-gaap:ShortTermBorrowings"]],
    "cash": [["us-gaap:CashAndCashEquivalentsAtCarryingValue"], ["ifrs-full:CashAndCashEquivalents"]],
    "nci": [["us-gaap:MinorityInterest", "us-gaap:RedeemableNoncontrollingInterestEquityCarryingAmount"], ["us-gaap:MinorityInterest"],
            ["ifrs-full:NoncontrollingInterests"]],
}
NOTES = {
    "TRI": "TRI reports under IFRS in USD; D&A = depreciation + amortisation of computer software + other identifiable intangibles; "
           "capex tag (PP&E line) is TRI's 'capital expenditures' incl. capitalised software (FY25 634); shares from Yahoo (40-F cover count is stale); "
           "PENDING: sale of 51% of Global Print to a KKR joint venture (TRI Q2 2026 results 6-K ex 99.1, accession 0001193125-26-333835): "
           "LTM figures still include print",
    "SPGI": "EV includes redeemable non-controlling interest (S&P Dow Jones Indices minority, CME Group) at carrying amount",
    "VRSK": "debt = current debt + long-term debt incl. finance leases",
    "MCO": "",
}
EU = {"WKL.AS": ("Wolters Kluwer", 12), "EXPN.L": ("Experian", 3), "LSEG.L": ("London Stock Exchange Group", 12)}
OPTIONAL = {"INF.L": ("Informa", 12)}


def facts(url):
    f = parse_instance(_sec_get(url).content)
    f = f[f["dims"] == ""].copy()
    f["num"] = pd.to_numeric(f["value"], errors="coerce")
    return f


def flow(f, options, start, end):
    """Sum of the first option whose tags all have a value for exactly this period (start..end)."""
    for opt in options:
        vals = []
        for tag in opt:
            x = f[(f["tag"] == tag) & (f["start"] == start) & (f["end"] == end)]["num"].dropna()
            if x.empty:
                break
            vals.append(float(x.iloc[0]))
        else:
            return sum(vals) / 1e6, "+".join(opt)
    return None, None


def balance(f, options, end):
    for opt in options:
        vals = []
        for tag in opt:
            x = f[(f["tag"] == tag) & (f["start"].isna()) & (f["end"] == end)]["num"].dropna()
            if x.empty:
                break
            vals.append(float(x.iloc[0]))
        else:
            return sum(vals) / 1e6, "+".join(opt)
    return 0.0, None


def yahoo_close(t, day=PRICE_DATE):
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


def eps_ntm(q):
    """NTM EPS = time-weighted current and next fiscal-year consensus (Yahoo earningsTrend '0y' and '+1y')."""
    tr = {x["period"]: x for x in q.get("earningsTrend", {}).get("trend", [])}
    if "0y" not in tr or "+1y" not in tr:
        return None, None, None, None
    e0, e1 = raw(tr["0y"]["earningsEstimate"], "avg"), raw(tr["+1y"]["earningsEstimate"], "avg")
    if e0 is None or e1 is None:
        return None, None, None, None
    end0 = dt.date.fromisoformat(tr["0y"]["endDate"])
    w0 = max(0.0, min(1.0, (end0 - RUN_DATE).days / 365))   # share of the next 12 months still in the current fiscal year
    return w0 * e0 + (1 - w0) * e1, e0, e1, tr["0y"]["endDate"]


def fx_usd_per_gbp():
    s = fred_series("DEXUSUK")
    s = s[s.index <= PRICE_DATE]
    return float(s.iloc[-1]), str(s.index[-1].date())


rows = []
for t, (name, cik, fym, ann_url, h1_url, docs) in SEC_PEERS.items():
    fa, fh = facts(ann_url), facts(h1_url)
    v, used = {}, {}
    for k, opts in FLOWS.items():
        fy, tag = flow(fa, opts, "2025-01-01", "2025-12-31")
        y26, _ = flow(fh, opts, "2026-01-01", "2026-06-30")
        y25, _ = flow(fh, opts, "2025-01-01", "2025-06-30")
        # LTM = last fiscal year + this year-to-date - same period last year
        v[k] = fy + y26 - y25 if None not in (fy, y26, y25) else None
        used[k] = tag if v[k] is not None else f"MISSING (FY {fy}, H1-26 {y26}, H1-25 {y25})"
    b = {k: balance(fh, o, "2026-06-30") for k, o in BALANCES.items()}
    (pdate, price), ccy = yahoo_close(t)
    q = quote_summary(t)
    cover = fh[fh["tag"] == "dei:EntityCommonStockSharesOutstanding"]["num"].dropna()
    if not cover.empty:
        shares_m, sh_src = float(cover.iloc[0]) / 1e6, "dei:EntityCommonStockSharesOutstanding (Q2 10-Q cover)"
    else:
        shares_m, sh_src = raw(q["defaultKeyStatistics"], "sharesOutstanding") / 1e6, "Yahoo sharesOutstanding (non-filing)"
    mcap = shares_m * price
    debt = b["debt"][0] + b["short_term_borrowings"][0]
    ev = mcap + debt - b["cash"][0] + b["nci"][0]       # enterprise value = equity + debt - cash + minorities
    ebitda = v["operating_income"] + v["da"] if None not in (v["operating_income"], v["da"]) else None  # EBITDA = operating income + D&A
    fcf = v["ocf"] - v["capex"] if None not in (v["ocf"], v["capex"]) else None                         # FCF = operating cash flow - capex
    ntm, e0, e1, end0 = eps_ntm(q)
    rows.append({
        "name": name, "ticker": t, "ccy": "USD", "fy_end_month": fym, "ltm_end": "2026-06-30",
        "price": round(price, 2), "price_date": pdate, "shares_m": round(shares_m, 1), "market_cap_m": round(mcap),
        "net_debt_m": round(debt - b["cash"][0]), "nci_m": round(b["nci"][0]), "ev_m": round(ev),
        "revenue_ltm_m": round(v["revenue"]) if v["revenue"] else None,
        "ebitda_ltm_m": round(ebitda) if ebitda else None, "ebitda_ntm_m": None,
        "net_income_ltm_m": round(v["net_income"]), "pe_ltm": round(mcap / v["net_income"], 2),
        "eps_ntm_consensus": round(ntm, 3) if ntm else None, "pe_ntm": round(price / ntm, 2) if ntm else None,
        "fcf_ltm_m": round(fcf) if fcf is not None else None, "fcf_yield_ltm": round(fcf / mcap, 4) if fcf is not None else None,
        "ev_ebitda_ltm": round(ev / ebitda, 2) if ebitda else None,
        "source": (f"SEC EDGAR XBRL instances CIK {cik}: {docs} (LTM = FY25 + H1 2026 - H1 2025; tags: "
                   + ", ".join(f"{k}={used[k]}" for k in FLOWS)
                   + "; " + ", ".join(f"{k}={b[k][1]}" for k in BALANCES) + f" at 2026-06-30; shares {sh_src})"
                   + f"; price Yahoo {t} close {pdate} ({ccy}); NTM EPS Yahoo consensus FY to {end0}: {e0} / next FY: {e1}"),
        "flag": ("flag: non-filing source (price, NTM EPS consensus" + (", shares" if "Yahoo" in sh_src else "") + "); "
                 "ebitda_ntm MISSING (no free EBITDA consensus); EBITDA is reported operating income + D&A, unadjusted"
                 + (f"; {NOTES[t]}" if NOTES[t] else "")),
    })

usd_gbp, fx_date = fx_usd_per_gbp()
for t, (name, fym) in {**EU, **OPTIONAL}.items():
    q = quote_summary(t)
    fd, ks = q["financialData"], q["defaultKeyStatistics"]
    (pdate, price), ccy = yahoo_close(t)
    fin_ccy = raw(fd, "financialCurrency")
    shares_m = raw(ks, "sharesOutstanding") / 1e6
    px_main = price / 100 if ccy == "GBp" else price          # London quotes in pence: convert to pounds
    px_ccy = "GBP" if ccy == "GBp" else ccy
    fx, extra = 1.0, ""
    if fin_ccy == "USD" and px_ccy == "GBP":                   # Experian reports in USD but is priced in pence
        fx, extra = usd_gbp, f"; market cap converted to USD at FRED DEXUSUK {usd_gbp} ({fx_date})"
    px_fin = px_main * fx                                      # price in the reporting currency
    mcap = shares_m * px_fin
    debt, cash = (raw(fd, "totalDebt") or 0) / 1e6, (raw(fd, "totalCash") or 0) / 1e6
    ev = mcap + debt - cash                                    # minorities not available from this source
    ebitda, ni = raw(fd, "ebitda"), raw(ks, "netIncomeToCommon")
    ebitda, ni = (ebitda / 1e6 if ebitda else None), (ni / 1e6 if ni else None)
    fcf = raw(fd, "freeCashflow")
    fcf = fcf / 1e6 if fcf is not None else None              # Yahoo 'levered' free cash flow
    ntm, e0, e1, end0 = eps_ntm(q)
    fwd_pe = raw(q["summaryDetail"], "forwardPE")
    pe_ntm = round(px_fin / ntm, 2) if ntm else None
    flag = "flag: non-filing source (all figures Yahoo Finance; EBITDA, debt, cash, FCF are Yahoo LTM figures, not checked to the annual report)"
    if pe_ntm and fwd_pe and abs(pe_ntm / fwd_pe - 1) > 0.25:
        flag += f"; CHECK: P/E NTM {pe_ntm} differs from Yahoo forwardPE {round(fwd_pe, 2)} by >25% (EPS currency or units?)"
    if fcf is None:
        flag += "; fcf MISSING"
    if t == "EXPN.L":
        flag += "; Experian fiscal year ends 31 March: LTM per Yahoo is to its latest reported quarter/half"
    if t in ("LSEG.L", "INF.L"):
        flag += "; P/E LTM uses REPORTED net income (after acquired-intangible amortisation / impairments) while NTM EPS consensus is ADJUSTED: prefer P/E NTM"
    if t in OPTIONAL:
        flag += "; OPTIONAL (exhibitions and academic publishing): show separately, not in the median"
    rows.append({
        "name": name, "ticker": t, "ccy": fin_ccy, "fy_end_month": fym,
        "ltm_end": str(dt.datetime.fromtimestamp(raw(ks, "mostRecentQuarter"), dt.timezone.utc).date()) if raw(ks, "mostRecentQuarter") else None,
        "price": round(price, 2), "price_date": pdate, "shares_m": round(shares_m, 1), "market_cap_m": round(mcap),
        "net_debt_m": round(debt - cash), "nci_m": None, "ev_m": round(ev),
        "revenue_ltm_m": round(raw(fd, "totalRevenue") / 1e6) if raw(fd, "totalRevenue") else None,
        "ebitda_ltm_m": round(ebitda) if ebitda else None, "ebitda_ntm_m": None,
        "net_income_ltm_m": round(ni) if ni else None, "pe_ltm": round(mcap / ni, 2) if ni else None,
        "eps_ntm_consensus": round(ntm, 3) if ntm else None, "pe_ntm": pe_ntm,
        "fcf_ltm_m": round(fcf) if fcf is not None else None, "fcf_yield_ltm": round(fcf / mcap, 4) if fcf is not None else None,
        "ev_ebitda_ltm": round(ev / ebitda, 2) if ebitda else None,
        "source": (f"Yahoo Finance quoteSummary {t} (financialData: ebitda, totalDebt, totalCash, freeCashflow, totalRevenue, "
                   f"financialCurrency {fin_ccy}; defaultKeyStatistics: sharesOutstanding, netIncomeToCommon; earningsTrend FY to {end0}: "
                   f"{e0} / next FY: {e1}); price Yahoo {t} close {pdate} ({ccy}){extra}. Annual report not reachable from this environment "
                   "(company sites blocked; no SEC filings)"),
        "flag": flag,
    })

out = pd.DataFrame(rows)
out.to_csv(DATA / "peers.csv", index=False)
print(out.drop(columns=["source"]).to_string())
for _, r in out.iterrows():
    print(r["ticker"], "|", r["source"][:400], "|", r["flag"])
