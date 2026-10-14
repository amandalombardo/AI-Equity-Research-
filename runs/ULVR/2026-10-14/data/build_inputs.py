"""Data agent script (ULVR, run 2026-10-14): financials.csv, tie_out.csv, market_data.json and ../inputs.yaml.

Inputs: financials_raw.csv and market_inputs.json written by `python -m desk.data_sources briefs/ULVR.yaml <this folder>`,
plus figures read from the primary filings (cited row by row below). All money amounts EUR m unless the name says otherwise.
Run from the repo root:  python runs/ULVR/2026-10-14/data/build_inputs.py
"""
import datetime as dt
import json
from pathlib import Path

import pandas as pd
import requests
import yaml

from desk.data_sources import fred_series

DATA = Path(__file__).resolve().parent
RUN = DATA.parent
RUN_DATE = dt.date(2026, 10, 14)
BS_DATE = dt.date(2025, 12, 31)
PRICE_DATE = "2026-10-13"   # last COMPLETED close: on 14 Oct the London/Amsterdam/Mumbai sessions were still open
YH = {"User-Agent": "Mozilla/5.0"}

# ---------------------------------------------------------------- document citations
F20 = ("Unilever FY25 Form 20-F (SEC accession 0000217410-26-000007, filed 12 Mar 2026, "
       "https://www.sec.gov/Archives/edgar/data/217410/000021741026000007/ul-20251231.htm)")
R25 = ("Unilever FY25 results 6-K (accession 0001654954-26-001155, 12 Feb 2026, "
       "https://www.sec.gov/Archives/edgar/data/217410/000165495426001155/a6773s.htm)")
H126 = ("Unilever H1 2026 results 6-K (accession 0000217410-26-000057, 28 Jul 2026, "
        "https://www.sec.gov/Archives/edgar/data/217410/000021741026000057/ul-20260630.htm)")
P425 = ("Unilever Foods/McCormick investor presentation, Form 425 (accession 0000217410-26-000027, 31 Mar 2026, "
        "https://www.sec.gov/Archives/edgar/data/217410/000021741026000027/apollo-425formxinvestorp.htm)")
C425 = "Unilever investor call transcript 31 Mar 2026, Form 425 (accession 0000217410-26-000032)"
MKCQ = ("McCormick 10-Q for the quarter to 31 Aug 2026 (accession 0000063754-26-000329, filed 1 Oct 2026, "
        "https://www.sec.gov/Archives/edgar/data/63754/000006375426000329/mkc-20260831.htm)")
TVR_AUG = "Unilever 6-K Total Voting Rights 1 Sep 2026 (accession 0001654954-26-008017): position at 31 Aug 2026"
TVR_JUL = "Unilever 6-K Total Voting Rights 3 Aug 2026 (accession 0001654954-26-007194): position at 31 Jul 2026"
TMICC424 = ("TMICC resale prospectus, Form 424(b)(4) (accession 0001104659-26-042683, 13 Apr 2026; CIK 0002071668): "
            "up to 121,604,413 ordinary shares offered by Unilever (19.86% of outstanding)")
SIX = {2021: "FY21 results 6-K (accession 0001654954-22-001398)", 2022: "FY22 results 6-K (accession 0001654954-23-001506)",
       2023: "FY23 results 6-K (accession 0001654954-24-001469)", 2024: "FY24 results 6-K (accession 0001654954-25-001439)",
       2025: R25}

# ---------------------------------------------------------------- facts read from the filings (EUR m)
F = {
    # FY25 results 6-K, non-GAAP reconciliations
    "uop25": 10084, "op25": 9037, "nonund25": 1047, "fcf25": 5921, "net_debt25": 23076, "uetr25": 0.257,
    "total_fin_liab25": 28278, "cash_bs25": 3941, "other_cur_fin_assets25": 1121, "nc_fin_deriv25": 140,
    "avg_invested_capital25": 39502,
    # 20-F
    "leases25": 1326, "bonds25": 26038, "bank25": 233, "leases24": 1486, "bonds24": 28648, "bank24": 521,
    "int_bank25": 52, "int_bonds25": 967, "int_leases25": 79,
    "jv_book25": 94, "assoc_book25": 15, "jv_share_profit25": 245, "jv_dividends25": 229,
    "tmicc_fv25": 1655, "pension_net_surplus25": 3518, "pension_funded_deficit25": 100, "pension_unfunded25": 844,
    "trade_receivables25": 4852, "prepayments25": 1369, "other_receivables25": 1125,
    "trade_payables25": 10994, "accruals25": 4649, "social_sec25": 565, "deferred_consid25": 26, "other_pay25": 705,
    "tmicc_payable25": 1600, "nci_hul25": 1569,
    # perimeter (Form 425 presentation)
    "perim_sales": 10700, "perim_uop": 2600,
    # H1 2026 6-K
    "net_debt_h126": 25961, "tmicc_fv_h126": 1852, "div_h126_equity": 2034, "buyback_h126": 1507, "uetr_h126": 0.260,
    "foods_bg_sales_h126": 6300, "foods_bg_uom_h126": 0.233,
}
UOP_HIST = {  # underlying operating profit and turnover as first reported (FY21-22 incl. Ice Cream) and re-presented (FY23-25 ex IC)
    2021: (9636, 52444, SIX[2021] + ", UOP reconciliation (Group incl. Ice Cream)"),
    2022: (9683, 60073, SIX[2022] + ", UOP reconciliation (Group incl. Ice Cream)"),
    2023: (9079, 51680, F20 + " p.137-138, note 2 segment table, 2023 re-presented without Ice Cream"),
    2024: (10198, 52479, R25 + ", UOP reconciliation, 2024 re-presented without Ice Cream"),
    2025: (10084, 50503, R25 + ", UOP reconciliation (continuing operations)"),
}


def yahoo_close(ticker: str, day: str) -> tuple[str, float, str]:
    """Unadjusted daily close on or before `day` (Yahoo chart data)."""
    p1 = int(dt.datetime.fromisoformat(day).timestamp()) - 12 * 86400
    p2 = int(dt.datetime.fromisoformat(day).timestamp()) + 86400
    r = requests.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}",
                     params={"period1": p1, "period2": p2, "interval": "1d"}, headers=YH, timeout=60)
    r.raise_for_status()
    res = r.json()["chart"]["result"][0]
    pts = [(str(dt.datetime.fromtimestamp(t, dt.timezone.utc).date()), c)
           for t, c in zip(res["timestamp"], res["indicators"]["quote"][0]["close"]) if c is not None]
    pts = [p for p in pts if p[0] <= day]
    return pts[-1][0], float(pts[-1][1]), res["meta"].get("currency")


def yahoo_shares(ticker: str) -> float:
    s = requests.Session(); s.headers.update(YH)
    s.get("https://fc.yahoo.com", timeout=30)
    crumb = s.get("https://query1.finance.yahoo.com/v1/test/getcrumb", timeout=30).text
    r = s.get(f"https://query2.finance.yahoo.com/v10/finance/quoteSummary/{ticker}",
              params={"modules": "defaultKeyStatistics", "crumb": crumb}, timeout=60)
    return r.json()["quoteSummary"]["result"][0]["defaultKeyStatistics"]["sharesOutstanding"]["raw"]


# ---------------------------------------------------------------- market data
mi = json.loads((DATA / "market_inputs.json").read_text())
usd_eur = fred_series("DEXUSEU"); usd_gbp = fred_series("DEXUSUK"); inr_usd = fred_series("DEXINUS")
fx = pd.concat([usd_eur, usd_gbp, inr_usd], axis=1, join="inner").dropna()
fx_date = str(fx.index[-1].date())
USD_PER_EUR, USD_PER_GBP, INR_PER_USD = (float(x) for x in fx.iloc[-1])
EUR_PER_GBP = USD_PER_GBP / USD_PER_EUR      # cross rate: (USD per GBP) / (USD per EUR)
INR_PER_EUR = INR_PER_USD * USD_PER_EUR      # cross rate: (INR per USD) x (USD per EUR)
assert abs(EUR_PER_GBP - mi["fx_eur_per_gbp"]["value"]) < 1e-9, "FX differs from desk.data_sources output"

mkt = {}
for t in ["ULVR.L", "MKC", "MICC.AS", "HINDUNILVR.NS", "EURUSD=X", "EURGBP=X"]:
    d, c, ccy = yahoo_close(t, PRICE_DATE)
    mkt[t] = {"date": d, "close": c, "currency": ccy}
d, c, ccy = yahoo_close("MICC.AS", "2026-06-30")
mkt["MICC.AS@2026-06-30"] = {"date": d, "close": c, "currency": ccy}
mkt["HINDUNILVR.NS_shares"] = yahoo_shares("HINDUNILVR.NS")
mkt["fred"] = {"date": fx_date, "USD_per_EUR": USD_PER_EUR, "USD_per_GBP": USD_PER_GBP, "INR_per_USD": INR_PER_USD,
               "EUR_per_GBP": EUR_PER_GBP, "INR_per_EUR": INR_PER_EUR}
mkt["desk_data_sources_price_14oct_intraday"] = mi["share_price_gbp_pence"]
(DATA / "market_data.json").write_text(json.dumps(mkt, indent=2))
assert mkt["ULVR.L"]["currency"] == "GBp" and mkt["MKC"]["currency"] == "USD" and mkt["MICC.AS"]["currency"] == "EUR"

# ---------------------------------------------------------------- financials.csv
raw = pd.read_csv(DATA / "financials_raw.csv")
basis = {y: ("Group incl. Ice Cream (as first reported)" if y <= 2022 else "") for y in range(2021, 2026)}
rows = []
for r in raw.itertuples():
    is_bs = r.item in {"inventories", "trade_and_other_receivables", "trade_and_other_payables", "cash",
                       "other_current_financial_assets", "gross_borrowings", "lease_liabilities", "non_controlling_interests",
                       "post_employment_net_liability", "equity_total", "equity_to_owners", "liabilities_held_for_sale"}
    if is_bs:
        b = "balance sheet as reported (incl. Ice Cream)" if r.fiscal_year <= 2024 else "balance sheet after the Ice Cream demerger"
    else:
        b = basis[r.fiscal_year] or "continuing operations, re-presented without Ice Cream"
    rows.append({"item": r.item, "fiscal_year": r.fiscal_year, "value_meur": r.value_meur,
                 "source": f"{r.source} | XBRL tag {r.tag} | basis: {b}"})
for y, (uop, sales, src) in UOP_HIST.items():
    rows.append({"item": "underlying_operating_profit", "fiscal_year": y, "value_meur": uop, "source": src})
    rows.append({"item": "turnover_same_basis_as_uop", "fiscal_year": y, "value_meur": sales, "source": src})
manual = [
    ("non_underlying_items_in_operating_profit", 2025, F["nonund25"], R25 + ", UOP reconciliation"),
    ("free_cash_flow", 2025, F["fcf25"], R25 + ", FCF reconciliation (CFO 10,772 - tax 2,720 - net capex 1,465 - net interest 666)"),
    ("net_debt_unilever_definition", 2025, F["net_debt25"], R25 + ", net debt reconciliation: total financial liabilities 28,278 - cash 3,941 - other current financial assets 1,121 - non-current derivatives 140 (lease liabilities 1,326 INSIDE)"),
    ("net_debt_unilever_definition", 2024, 24519, R25 + ", net debt reconciliation (2024 not re-presented, incl. Ice Cream)"),
    ("total_financial_liabilities", 2025, F["total_fin_liab25"], F20 + " p.164, note 15C"),
    ("bonds_and_other_loans", 2025, F["bonds25"], F20 + " p.164, note 15C"),
    ("bank_loans_and_overdrafts", 2025, F["bank25"], F20 + " p.164, note 15C"),
    ("lease_liabilities_note15c", 2025, F["leases25"], F20 + " p.164, note 15C (part of financial liabilities, so inside net debt)"),
    ("interest_bank_loans", 2025, F["int_bank25"], F20 + " p.148, note 5"),
    ("interest_bonds_and_other_loans", 2025, F["int_bonds25"], F20 + " p.148, note 5"),
    ("interest_lease_liabilities", 2025, F["int_leases25"], F20 + " p.148, note 5"),
    ("joint_ventures_book_value", 2025, F["jv_book25"], F20 + " p.158, note 11 (Pepsi Lipton partnerships, Unilever FIMA/Gallo Portugal, Binzagr)"),
    ("associates_book_value", 2025, F["assoc_book25"], F20 + " p.158, note 11"),
    ("jv_dividends_received", 2025, F["jv_dividends25"], F20 + " p.158, note 11 movements"),
    ("tmicc_stake_fair_value", 2025, F["tmicc_fv25"], F20 + " p.174, note 17A footnote (e): non-current FVOCI equity investment, NOT in net debt"),
    ("pension_net_surplus", 2025, F["pension_net_surplus25"], F20 + " p.43 and note 4B (p.141-146)"),
    ("pension_funded_schemes_in_deficit", 2025, F["pension_funded_deficit25"], F20 + " p.131 balance sheet"),
    ("pension_unfunded_schemes", 2025, F["pension_unfunded25"], F20 + " p.131 balance sheet"),
    ("trade_receivables", 2025, F["trade_receivables25"], F20 + " p.159, note 13"),
    ("prepayments_and_accrued_income", 2025, F["prepayments25"], F20 + " p.159, note 13"),
    ("other_receivables", 2025, F["other_receivables25"], F20 + " p.159, note 13"),
    ("trade_payables", 2025, F["trade_payables25"], F20 + " p.160, note 14"),
    ("accruals_current", 2025, F["accruals25"], F20 + " p.160, note 14"),
    ("social_security_and_sundry_taxes", 2025, F["social_sec25"], F20 + " p.160, note 14"),
    ("other_current_payables", 2025, F["other_pay25"], F20 + " p.160, note 14"),
    ("payable_due_to_tmicc_in_trade_payables", 2025, F["tmicc_payable25"], F20 + " p.160, note 14: 'trade payables and other current liabilities include EUR 1.6 billion due to TMICC' (inventory subsidy + TSA balances)"),
    ("nci_hindustan_unilever_book", 2025, F["nci_hul25"], F20 + " p.162-163, note 15B"),
    ("average_invested_capital", 2025, F["avg_invested_capital25"], R25 + ", ROIC reconciliation"),
    ("foods_perimeter_sales", 2025, F["perim_sales"], P425 + ", slide 25 'Unilever Foods transaction perimeter' (preliminary carve-out, IFRS)"),
    ("foods_perimeter_uop", 2025, F["perim_uop"], P425 + ", slide 25"),
    ("net_debt_unilever_definition_30jun2026", 2026, F["net_debt_h126"], H126 + ", net debt reconciliation at 30 Jun 2026 (fiscal_year 2026 = H1 2026)"),
    ("share_buyback_cash_h1_2026", 2026, F["buyback_h126"], H126 + ", cash flow statement 'Repurchase of shares' (EUR 1.5bn programme, completed June 2026)"),
]
for item, fy, v, src in manual:
    rows.append({"item": item, "fiscal_year": fy, "value_meur": v, "source": src})
fin = pd.DataFrame(rows).sort_values(["item", "fiscal_year"])
fin.to_csv(DATA / "financials.csv", index=False)


def val(item, fy=2025):
    return float(fin[(fin["item"] == item) & (fin["fiscal_year"] == fy)]["value_meur"].iloc[0])


# ---------------------------------------------------------------- tie-out vs brief checks.published_fy25
brief = yaml.safe_load(Path("briefs/ULVR.yaml").read_text())
pub, tol = brief["checks"]["published_fy25"], brief["checks"]["data_tie_out_tolerance"]
ours = {"net_sales_meur": val("net_sales"), "underlying_operating_profit_meur": val("underlying_operating_profit"),
        "underlying_operating_margin": val("underlying_operating_profit") / val("net_sales"),
        "free_cash_flow_meur": val("free_cash_flow"), "net_debt_meur": val("net_debt_unilever_definition")}
tie = pd.DataFrame([{"item": k, "brief": pub[k], "data_agent": round(v, 5), "diff_pct": round(v / pub[k] - 1, 5),
                     "flag": abs(v / pub[k] - 1) > tol} for k, v in ours.items()])
tie.to_csv(DATA / "tie_out.csv", index=False)

# ---------------------------------------------------------------- inputs.yaml
sales25 = val("net_sales")
base_sales = sales25 - F["perim_sales"]                      # ex-perimeter turnover (decision 1)
base_uop = F["uop25"] - F["perim_uop"]                       # ex-perimeter underlying operating profit
restr = [val("restructuring", y) / val("net_sales", y) for y in (2023, 2024, 2025)]
restr_avg = sum(restr) / 3                                   # recurring restructuring, % of turnover, FY23-25
inv, rec, pay = val("inventories"), val("trade_and_other_receivables"), val("trade_and_other_payables")
nwc_all = (inv + rec - pay) / sales25                        # operating working capital / sales, XBRL definition
nwc_ex_tmicc = (inv + rec - (pay - F["tmicc_payable25"])) / sales25   # without the one-off TMICC demerger balance
nwc_trade = (inv + F["trade_receivables25"] - F["trade_payables25"]) / sales25  # strict trade-only items

avg_debt = ((F["bank24"] + F["bonds24"] + F["leases24"]) + (F["bank25"] + F["bonds25"] + F["leases25"])) / 2
interest = F["int_bank25"] + F["int_bonds25"] + F["int_leases25"]
kd_hist = interest / avg_debt                                # historic pre-tax cost of debt = interest / average gross debt

shares_m = 2154.327621                                       # voting shares at 31 Aug 2026 (excl. 30.7m treasury)
px_p = mkt["ULVR.L"]["close"]
mcap_eur = shares_m * px_p / 100 * EUR_PER_GBP               # market cap: shares x price (pence -> GBP) x EUR per GBP
debt_w = F["net_debt25"] / (F["net_debt25"] + mcap_eur)       # market-value debt weight D / (D + E)
debt_w_h1 = F["net_debt_h126"] / (F["net_debt_h126"] + mcap_eur)

micc_px = mkt["MICC.AS"]["close"]
tmicc_mv = 121_604_413 * micc_px / 1e6                       # listed stake at market
associates = tmicc_mv + F["jv_book25"] + F["assoc_book25"]

mkc_existing = 14_522_864 + 254_541_615                     # McCormick voting + non-voting shares, 10-Q cover (31 Aug 2026)
mkc_new = mkc_existing * 65 / 35                             # Unilever + its shareholders get 65%; existing holders 35%
mkc_px = mkt["MKC"]["close"]
consid_usd = 15_700 + mkc_new / 1e6 * mkc_px                 # cash + shares at market, USD m
disposal_eur = consid_usd / USD_PER_EUR                      # convert at EUR/USD (USD per EUR)
disposal_eur_yh = consid_usd / mkt["EURUSD=X"]["close"]

stub = (RUN_DATE - BS_DATE).days / 365                        # fraction of FY26 elapsed at the run date
div_q2 = 0.4664 * 2_154_327_344 / 1e6                         # Q2 2026: EUR 0.4664 x voting shares at 31 Jul 2026
divs = F["div_h126_equity"] + div_q2                          # Q4 2025 + Q1 2026 (H1 2026 equity statement) + Q2 2026

hul_sh = mkt["HINDUNILVR.NS_shares"]
hul_mv_eur = hul_sh * mkt["HINDUNILVR.NS"]["close"] / INR_PER_EUR / 1e6
hul_minority = hul_mv_eur * (1 - 0.619)

S = lambda x, n=0: f"{x:,.{n}f}"
inputs = {
    "base_sales": {"value": round(base_sales, 1), "source":
        f"EUR m, ex the Foods sale perimeter (decision 1): FY25 turnover {S(sales25)} ({R25}, UOP reconciliation; = 20-F XBRL ifrs-full:Revenue) "
        f"less perimeter FY25 sales {S(F['perim_sales'])} ({P425}, slide 25, 'EUR 10.7bn', preliminary carve-out). Perimeter rounded to EUR 0.1bn."},
    "base_margin": {"value": brief["dcf"]["base_margin"], "source":
        f"PM decision 3 (briefs/ULVR.yaml dcf.base_margin): ex-perimeter underlying margin {base_uop/base_sales:.2%} "
        f"(UOP {S(F['uop25'])} - perimeter UOP {S(F['perim_uop'])} = {S(base_uop)}; {R25}; {P425} slide 25) less FY23-25 average "
        f"restructuring {restr_avg:.2%} of turnover (425/51,680, 710/52,479, 599/50,503; 20-F XBRL ifrs-full:ExpenseOfRestructuringActivities, "
        f"FY25 20-F p.137-138 note 2) = {base_uop/base_sales - restr_avg:.2%}, rounded by the PM to 17.7%. H1 2026 6-K guides FY26 restructuring 'around 1.0% of turnover'."},
    "tax_rate": {"value": brief["dcf"]["tax_rate"], "source":
        f"PM decision 9 (briefs/ULVR.yaml dcf.tax_rate): H1 2026 underlying ETR 26.0% and FY26 guide 'around 26%' ({H126}, finance costs and tax); "
        f"FY25 underlying ETR 25.7% ({F20} p.43; {R25}) helped by one-off tax settlements."},
    "da_pct_sales": {"value": brief["dcf"]["da_pct_sales"], "source":
        f"PM decision (sign-off G): FY25 depreciation and amortisation 1,310 / turnover 50,503 = {1310/50503:.3%} "
        f"({F20}; XBRL ifrs-full:DepreciationAndAmortisationExpense, p.137 note 2 segment table)."},
    "capex_pct_sales": {"value": brief["dcf"]["capex_pct_sales"], "source":
        f"PM decision (sign-off G): FY25 purchase of PP&E 1,417 / turnover 50,503 = {1417/50503:.3%} ({F20} p.132 cash flow statement; "
        f"XBRL ifrs-full:PurchaseOfPropertyPlantAndEquipmentClassifiedAsInvestingActivities). EXCLUDES purchase of intangibles 174 (incl. would be {(1417+174)/50503:.2%}): FLAG in notes.md."},
    "nwc_pct_sales": {"value": round(nwc_ex_tmicc, 5), "source":
        f"FY25 (inventories {S(inv)} + trade and other current receivables {S(rec)} - (trade payables and other current liabilities {S(pay)} "
        f"- EUR 1,600m due to TMICC)) / turnover {S(sales25)} = {nwc_ex_tmicc:.2%}. {F20} p.131 balance sheet, notes 13-14 p.159-160; XBRL "
        f"ifrs-full:Inventories, TradeAndOtherCurrentReceivables, TradeAndOtherCurrentPayables. TRAP: payables include a one-off EUR 1.6bn due to TMICC "
        f"(inventory subsidy + transitional services, note 14), removed here. Brief formula with all XBRL items = {nwc_all:.2%}; strict trade-only "
        f"(4,043 + trade receivables 4,852 - trade payables 10,994) = {nwc_trade:.2%}. Balance sheet still includes the Foods perimeter. FLAG for PM."},
    "risk_free": {"value": mi["risk_free"]["value"], "source":
        f"{mi['risk_free']['source']}, latest month {mi['risk_free']['date']} (Aug 2026 average 3.18%); PM decision 7: euro cash flows -> Bund, not the gilt."},
    "pre_tax_cost_of_debt": {"value": round(kd_hist, 5), "source":
        f"Historic, reference only: FY25 interest on bank loans 52 + bonds and other loans 967 + leases 79 = {S(interest)} ({F20} p.148 note 5) / "
        f"average gross debt {S(avg_debt)} (bank loans + bonds + leases, 31 Dec 2024 30,655 and 31 Dec 2025 27,597; {F20} p.164 note 15C). "
        f"The engine uses risk-free + credit_spread 0.70% (brief) = {mi['risk_free']['value'] + 0.007:.2%}. H1 2026 6-K: net finance costs 2.5% of average net debt."},
    "debt_weight": {"value": round(debt_w, 5), "source":
        f"Market values: net debt {S(F['net_debt25'])} (31 Dec 2025) / (net debt + market cap EUR {S(mcap_eur)} = {shares_m:,.3f}m shares x "
        f"{px_p:.1f}p (Yahoo ULVR.L close {mkt['ULVR.L']['date']}) x {EUR_PER_GBP:.5f} EUR per GBP (FRED DEXUSUK/DEXUSEU {fx_date})). "
        f"With 30 Jun 2026 net debt 25,961: {debt_w_h1:.2%}."},
    "net_debt": {"value": float(F["net_debt25"]), "source":
        f"Unilever's definition at 31 Dec 2025 ({R25}, net debt reconciliation; {F20} p.164 note 15C): total financial liabilities 28,278 "
        f"(bank 233 + bonds 26,038 + LEASES 1,326 + derivatives 452 + other 229) - cash 3,941 - other current financial assets 1,121 "
        f"- non-current financial asset derivatives 140 = 23,076. Lease liabilities ARE INSIDE. TMICC stake is non-current FVOCI, NOT inside. "
        f"Does NOT reflect the EUR 1,507m share buyback of H1 2026 (see notes.md FLAG)."},
    "lease_liabilities": {"value": 0.0, "source":
        f"0 because the EUR 1,326m of lease liabilities is already inside net debt ({F20} p.164 note 15C; p.171 note 16B 'Less: lease liabilities (1,326)')."},
    "minority_interests": {"value": float(val("non_controlling_interests")), "source":
        f"Book value at 31 Dec 2025, of which Hindustan Unilever 1,569 ({F20} p.131 balance sheet, p.162-163 note 15B; XBRL ifrs-full:NoncontrollingInterests). "
        f"Reference only: brief minorities_method = proportionate (Fundamentals agent supplies minority_share_of_operating_profit)."},
    "pension_deficit": {"value": 0.0, "source":
        f"Brief rule (0 if in surplus): net SURPLUS EUR 3,518m at 31 Dec 2025 ({F20} p.43 and note 4B; XBRL ifrs-full:LiabilityAssetOfDefinedBenefitPlans "
        f"= -3,518); gross deficit plans 944 (funded in deficit 100 + unfunded 844, p.131) are inside that net figure. 30 Jun 2026: surplus 3.7bn ({H126})."},
    "associates": {"value": round(associates, 1), "source":
        f"TMICC 19.85% at market: 121,604,413 shares ({TMICC424}) x EUR {micc_px:.3f} (Yahoo MICC.AS close {mkt['MICC.AS']['date']}) = {S(tmicc_mv,1)}; "
        f"+ joint ventures 94 + associates 15 at book ({F20} p.158 note 11). No sell-down found: Unilever 6-Ks to 25 Sep 2026 and TMICC 6-Ks/424B3 "
        f"to 30 Sep 2026 (EDGAR CIK 0002071668) show no sale; H1 2026 6-K still carries the stake at 1,852. FLAG: JVs earn 245 a year (book 94)."},
    "disposal_proceeds": {"value": round(disposal_eur, 1), "source":
        f"Foods consideration at run-date market value (decision 1): cash USD 15,700m + new McCormick shares {mkc_new:,.0f} "
        f"(= existing {mkc_existing:,} [voting 14,522,864 + non-voting 254,541,615, {MKCQ} cover] x 65/35; 55.1% to Unilever shareholders + 9.9% "
        f"to Unilever, 10-Q note 2) x USD {mkc_px:.2f} (Yahoo MKC close {mkt['MKC']['date']}) = USD {S(mkc_new/1e6*mkc_px,1)}m; total USD "
        f"{S(consid_usd,1)}m / {USD_PER_EUR:.4f} USD per EUR (FRED DEXUSEU {fx_date}) = EUR {S(disposal_eur,1)}m. Yahoo EURUSD=X "
        f"{mkt['EURUSD=X']['close']:.4f} ({mkt['EURUSD=X']['date']}) would give {S(disposal_eur_yh,1)}. Tax on the cash: MISSING, NOT deducted "
        f"(PM decision 5; CFO: 'premature to start making estimates', {C425}). Received at closing (expected mid-2027): timing FLAG in notes.md."},
    "restructuring_cash": {"value": float(brief["dcf"]["bridge"]["restructuring_cash_meur"]), "source":
        f"Brief (decision 3): 'c.EUR 500m one-off restructuring to offset stranded costs ... to be incurred over 2027-2029' ({P425}, slide 19)."},
    "shares_outstanding_m": {"value": shares_m, "source":
        f"{TVR_AUG}: issued 2,185,205,247 - treasury 30,703,780 - group-held 173,846 = 2,154,327,621 shares with voting rights. "
        f"No later Total Voting Rights 6-K on EDGAR at the run date (latest Unilever filing 25 Sep 2026). Ordinary shares; 1 UL ADR = 1 share."},
    "fx_eur_per_gbp": {"value": EUR_PER_GBP, "source":
        f"{mi['fx_eur_per_gbp']['source']}, {fx_date} (USD per GBP {USD_PER_GBP} / USD per EUR {USD_PER_EUR}); Yahoo EURGBP=X "
        f"{mkt['EURGBP=X']['date']}: {1/mkt['EURGBP=X']['close']:.5f}."},
    "share_price_gbp_pence": {"value": px_p, "source":
        f"Yahoo Finance ULVR.L close {mkt['ULVR.L']['date']} (pence, GBp), last completed close before the run date. desk.data_sources wrote "
        f"{mi['share_price_gbp_pence']['value']}p dated {mi['share_price_gbp_pence']['date']}, which was an INTRADAY price (London open): not used."},
    "stub_years": {"value": round(stub, 5), "source":
        f"{(RUN_DATE - BS_DATE).days} days from the 31 Dec 2025 balance sheet to the run date {RUN_DATE} / 365."},
    "dividends_ex_before_valuation_meur": {"value": round(divs, 1), "source":
        f"Dividends that went ex between 31 Dec 2025 and {RUN_DATE}: Q4 2025 EUR 0.4664 (ex 26 Feb 2026; {R25} note 9) and Q1 2026 EUR 0.4664 "
        f"(ex 14 May 2026; {H126}: 'in line with the Q1 2026 dividend') = 2,034 booked in the H1 2026 equity statement ({H126}); + Q2 2026 EUR 0.4664 "
        f"(ex 6 Aug 2026, {H126} note 10) x 2,154,327,344 voting shares ({TVR_JUL}) = {S(div_q2,1)}. Q3 2026 goes ex 12 Nov 2026 (after the run date). "
        f"EXCLUDES the EUR 1,507m H1 2026 buyback (FLAG in notes.md)."},
    # ---- extra items for other agents (not read by the engine)
    "buyback_after_balance_sheet_meur": {"value": float(F["buyback_h126"]), "source":
        f"{H126} cash flow 'Repurchase of shares (1,507)'; 30,703,780 shares now in treasury ({TVR_AUG}). Cash left after 31 Dec 2025 while "
        f"shares_outstanding_m is post-buyback: FLAG for the valuation agent (not read by the engine)."},
    "tmicc_payable_meur": {"value": float(F["tmicc_payable25"]), "source": f"{F20} p.160 note 14: EUR 1.6bn due to TMICC inside trade payables. Possible debt-like item: FLAG."},
    "hul_market_value_meur": {"value": round(hul_mv_eur, 1), "source":
        f"Bear line: Hindustan Unilever {hul_sh/1e6:,.1f}m shares (Yahoo HINDUNILVR.NS sharesOutstanding: flag non-filing source) x INR "
        f"{mkt['HINDUNILVR.NS']['close']:.1f} (Yahoo close {mkt['HINDUNILVR.NS']['date']}) / {INR_PER_EUR:.3f} INR per EUR (FRED DEXINUS x DEXUSEU {fx_date}). "
        f"Outside holders 38.1% (Unilever 61.90%, {F20} p.194 related undertakings) = EUR {S(hul_minority,1)}m."},
    "foods_perimeter_interim_cash_flows_meur": {"value": None, "source":
        f"MISSING: no cash-flow disclosure for the perimeter between 1 Jan 2026 and closing (not in {H126}, {P425}, or McCormick filings; "
        f"no S-4 yet). Indicators only: perimeter FY25 UOP 2,600 ({P425}); H1 2026 Foods business group (wider than the perimeter) turnover "
        f"EUR 6.3bn, UOM 23.3% ({H126}, business group review)."},
}
(RUN / "inputs.yaml").write_text(yaml.safe_dump(inputs, sort_keys=False, width=160, allow_unicode=True))

print(tie.to_string())
for k, v in inputs.items():
    print(f"{k:42s} {v['value']}")
print("mcap_eur", round(mcap_eur), "nwc all/ex/trade", round(nwc_all, 4), round(nwc_ex_tmicc, 4), round(nwc_trade, 4),
      "restr avg", round(restr_avg, 4), "MKC new shares", round(mkc_new), "TMICC 30 Jun close", mkt["MICC.AS@2026-06-30"],
      "TMICC implied 30 Jun", round(F["tmicc_fv_h126"] * 1e6 / 121_604_413, 3), "HUL minority", round(hul_minority))
