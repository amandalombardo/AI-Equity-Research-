"""Fundamentals agent, KO run 2026-10-13. Builds ratios.csv and segments.csv.

Run from the repo root:  PYTHONPATH=. python runs/KO/2026-10-13/fundamentals/build_ratios.py
All money is USD m. All arithmetic goes through desk/fundamentals.py (growth, margin, roic,
cash_conversion, leverage, interest_cover); this script only adds/subtracts balance-sheet lines
to build the inputs (invested capital, net debt, EBITDA, FCF), each line labelled.
"""
import csv
from pathlib import Path

from desk import fundamentals as f

RUN = Path("runs/KO/2026-10-13")
OUT = RUN / "fundamentals"
YEARS = [2021, 2022, 2023, 2024, 2025]

# ---- Data agent figures (financials.csv, every row carries its own source) ----
D = {}
SRC = {}
with open(RUN / "data" / "financials.csv") as fh:
    for r in csv.DictReader(fh):
        D[(r["item"], int(r["fiscal_year"]))] = float(r["value_musd"])
        SRC[(r["item"], int(r["fiscal_year"]))] = r["source"]


def g(item, y):
    return D.get((item, y))


# ---- Figures read from the filings by this agent (not in financials.csv) ----
Q4 = {2021: "0000021344-22-000004", 2022: "0000021344-23-000005", 2023: "0000021344-24-000004",
      2024: "0000021344-25-000005", 2025: "0001628280-26-006642"}
# Organic revenue growth (non-GAAP), as published in each year's Q4 results 8-K headline
# ("Organic Revenues (Non-GAAP) Grew X% ... for the Full Year"). Whole percent, company rounding.
ORGANIC = {2021: 0.16, 2022: 0.16, 2023: 0.12, 2024: 0.12, 2025: 0.05}
# Published comparable operating margin (non-GAAP), Q4 8-K "Comparable Operating Margin" line, used as a check.
PUB_COMP_MARGIN = {2021: 0.2874, 2022: 0.2868, 2023: 0.2913, 2024: 0.3003, 2025: 0.3124}
# Comparable (non-GAAP) effective tax rate, full year, Q4 8-K reconciliation of income taxes.
# FY21 and FY22 from the Q4 2022 8-K, FY23 Q4 2023 8-K, FY24 Q4 2024 8-K, FY25 Q4 2025 8-K.
COMP_TAX = {2021: 0.186, 2022: 0.190, 2023: 0.190, 2024: 0.186, 2025: 0.206}
# Comparable (non-GAAP) interest expense, full year, same reconciliation tables.
# FY21/FY22 Q4 2022 8-K, FY23 Q4 2023 8-K, FY24/FY25 Q4 2025 8-K.
COMP_INT = {2021: 776, 2022: 906, 2023: 1552, 2024: 1681, 2025: 1679}
FY20_NET_REVENUES = 33014   # Q4 2021 8-K (0000021344-22-000004), condensed income statement, FY2020 column
IRS_DEPOSIT_CASH = 6041     # Q4 2024 8-K FCF reconciliation "Plus: IRS Tax Litigation Deposit 6,041"
IRS_DEPOSIT_CAPITAL = 6000  # FY25 10-K tax note: "$6.0 billion" (same figure as ko-roic-evidence.md)
FAIRLIFE_PAYMENT = 6069     # Q4 2025 8-K FCF reconciliation "Plus: fairlife Contingent Consideration Payment 6,069"
DCF_TAX = 0.237             # briefs/KO.yaml dcf comment / inputs.yaml tax_rate (IRS case lost)

rows = []


def add(item, year, value, unit, formula, inputs, source):
    rows.append({"item": item, "year": year,
                 "value": "MISSING" if value is None else round(value, 6),
                 "unit": unit, "formula": formula, "inputs_used": inputs, "source": source})


FIN = "runs/KO/2026-10-13/data/financials.csv (10-K XBRL; see row sources)"

for y in YEARS:
    sales = g("net_sales", y)
    prev = g("net_sales", y - 1) if y > 2021 else FY20_NET_REVENUES
    # Reported revenue growth (USD, GAAP net operating revenues)
    add("revenue_growth_reported", y, f.growth(sales, prev), "ratio", "net_sales_t / net_sales_t-1 - 1",
        f"{sales:.0f} / {prev:.0f}", FIN + ("" if y > 2021 else "; FY20 33,014 from Q4 2021 8-K 0000021344-22-000004"))
    # Organic revenue growth (non-GAAP, ex currency and acquisitions/divestitures), AS PUBLISHED
    add("revenue_growth_organic_published", y, ORGANIC[y], "ratio", "as published (not calculated)",
        "company figure, whole %", f"Q4 {y} results 8-K ex.99.1, accession {Q4[y]}, headline")

    # Gross margin (reported, GAAP)
    gp = g("gross_profit", y)
    add("gross_margin_reported", y, f.margin(gp, sales), "ratio", "gross_profit / net_sales",
        f"{gp:.0f} / {sales:.0f}", FIN)

    # Operating margin, reported (GAAP): includes fairlife remeasurement, impairments, restructuring
    op = g("operating_profit_reported", y)
    add("operating_margin_reported", y, f.margin(op, sales), "ratio", "operating_profit_reported / net_sales",
        f"{op:.0f} / {sales:.0f}", FIN)
    # Operating margin, comparable (non-GAAP, before items impacting comparability = "before exceptionals")
    cop, crev = g("comparable_operating_income", y), g("comparable_net_revenues", y)
    cm = f.margin(cop, crev)
    add("operating_margin_comparable", y, cm, "ratio", "comparable_operating_income / comparable_net_revenues",
        f"{cop:.0f} / {crev:.0f}", f"Q4 {y} results 8-K, accession {Q4[y]}, GAAP to non-GAAP reconciliation")
    # Check: difference vs the company's published comparable margin (percentage points as a ratio)
    add("operating_margin_comparable_minus_published", y, cm - PUB_COMP_MARGIN[y], "ratio",
        "calculated comparable margin - published comparable margin", f"{cm:.6f} - {PUB_COMP_MARGIN[y]}",
        f"Q4 {y} 8-K {Q4[y]} 'Comparable Operating Margin (Non-GAAP)'")

    # Free cash flow (KO definition) = operating cash flow - purchases of PP&E
    ocf, capex, np_ = g("operating_cash_flow", y), g("capex", y), g("net_profit_to_owners", y)
    fcf = ocf - capex
    add("free_cash_flow_reported", y, fcf, "USD m", "operating_cash_flow - capex", f"{ocf:.0f} - {capex:.0f}", FIN)
    # Cash conversion = FCF / net profit attributable to shareowners
    add("cash_conversion_reported", y, f.cash_conversion(fcf, np_), "ratio", "FCF / net_profit_to_owners",
        f"{fcf:.0f} / {np_:.0f}", FIN)
    one_off = {2024: IRS_DEPOSIT_CASH, 2025: FAIRLIFE_PAYMENT}.get(y, 0)
    fcf_x = fcf + one_off
    add("free_cash_flow_ex_one_offs", y, fcf_x, "USD m",
        "FCF + IRS deposit (FY24) + fairlife payment (FY25)", f"{fcf:.0f} + {one_off}",
        "Q4 2024 8-K 0000021344-25-000005 (IRS 6,041); Q4 2025 8-K 0001628280-26-006642 (fairlife 6,069)")
    add("cash_conversion_ex_one_offs", y, f.cash_conversion(fcf_x, np_), "ratio",
        "(FCF + one-off cash payment) / net_profit_to_owners", f"{fcf_x:.0f} / {np_:.0f}",
        "as above + " + FIN)

    # Net debt = short-term borrowings + current and non-current long-term debt
    #            - cash - short-term investments - marketable securities (leases excluded, as Data agent)
    debt = g("short_term_borrowings", y) + g("long_term_debt_current", y) + g("long_term_debt_noncurrent", y)
    liquid = g("cash", y) + g("short_term_investments", y) + g("marketable_securities", y)
    nd = debt - liquid
    add("net_debt", y, nd, "USD m", "ST borrowings + LTD current + LTD non-current - cash - ST investments - marketable securities",
        f"{g('short_term_borrowings', y):.0f}+{g('long_term_debt_current', y):.0f}+{g('long_term_debt_noncurrent', y):.0f}"
        f"-{g('cash', y):.0f}-{g('short_term_investments', y):.0f}-{g('marketable_securities', y):.0f}", FIN)
    da = g("depreciation_amortisation", y)
    # EBITDA = operating income + depreciation and amortisation (reported and comparable bases)
    ebitda_r, ebitda_c = op + da, cop + da
    add("ebitda_reported", y, ebitda_r, "USD m", "operating_profit_reported + D&A", f"{op:.0f} + {da:.0f}", FIN)
    add("ebitda_comparable", y, ebitda_c, "USD m", "comparable_operating_income + D&A", f"{cop:.0f} + {da:.0f}",
        f"Q4 8-K {Q4[y]} + " + FIN)
    # Leverage = net debt / EBITDA
    add("net_debt_to_ebitda_reported", y, f.leverage(nd, ebitda_r), "x", "net_debt / ebitda_reported",
        f"{nd:.0f} / {ebitda_r:.0f}", "derived above")
    add("net_debt_to_ebitda_comparable", y, f.leverage(nd, ebitda_c), "x", "net_debt / ebitda_comparable",
        f"{nd:.0f} / {ebitda_c:.0f}", "derived above")

    # Interest cover = operating income / interest
    ie, ii = g("interest_expense", y), g("interest_income", y)
    nie = ie - ii
    add("net_interest_expense", y, nie, "USD m", "interest_expense - interest_income", f"{ie:.0f} - {ii:.0f}", FIN)
    add("interest_cover_reported_net", y, f.interest_cover(op, nie), "x", "operating_profit_reported / net_interest_expense",
        f"{op:.0f} / {nie:.0f}", FIN)
    add("interest_cover_reported_gross", y, f.interest_cover(op, ie), "x", "operating_profit_reported / interest_expense",
        f"{op:.0f} / {ie:.0f}", FIN)
    add("interest_cover_comparable_gross", y, f.interest_cover(cop, COMP_INT[y]), "x",
        "comparable_operating_income / comparable_interest_expense", f"{cop:.0f} / {COMP_INT[y]}",
        f"Q4 8-K reconciliations ({Q4[y]} and following year)")

# FY25 sensitivity: CCBA debt (1,435) and cash (178) sit in held-for-sale, outside the net debt above
nd25 = [r["value"] for r in rows if r["item"] == "net_debt" and r["year"] == 2025][0]
ccba_net = g("ccba_debt_in_liabilities_held_for_sale", 2025) - g("ccba_cash_in_assets_held_for_sale", 2025)
nd25c = nd25 + ccba_net
e25c = [r["value"] for r in rows if r["item"] == "ebitda_comparable" and r["year"] == 2025][0]
add("net_debt_incl_ccba_held_for_sale", 2025, nd25c, "USD m", "net_debt + CCBA debt - CCBA cash (held for sale)",
    f"{nd25:.0f} + 1435 - 178", FIN + " (FY25 10-K Note 2)")
add("net_debt_incl_ccba_to_ebitda_comparable", 2025, f.leverage(nd25c, e25c), "x", "net_debt_incl_ccba / ebitda_comparable",
    f"{nd25c:.0f} / {e25c:.0f}", "derived above")


# ---- ROIC (definition of docs/phase5/ko-roic-evidence.md) ----
def invested_capital(y):
    # Invested capital = total equity (incl. minorities) + all borrowings + operating leases
    #                    - cash - ST investments - marketable securities - equity-method stakes
    return (g("equity_total", y) + g("short_term_borrowings", y) + g("long_term_debt_current", y)
            + g("long_term_debt_noncurrent", y) + g("operating_lease_liabilities", y)
            - g("cash", y) - g("short_term_investments", y) - g("marketable_securities", y)
            - g("investments_in_associates", y))


for y in YEARS:
    ic = invested_capital(y)
    add("invested_capital", y, ic, "USD m",
        "equity_total + ST borrowings + LTD current + LTD non-current + operating leases - cash - ST inv - marketable sec - equity-method investments",
        "financials.csv lines for that year", FIN)
for y in YEARS:
    cop = g("comparable_operating_income", y)
    if y == 2021:
        for k in ("roic_comparable_dcf_tax", "roic_comparable_company_tax", "roic_comparable_dcf_tax_ex_irs_deposit"):
            add(k, y, None, "ratio", "needs FY20 invested capital", "FY20 balance sheet not in data folder", "MISSING")
        continue
    o, c = invested_capital(y - 1), invested_capital(y)
    # ROIC = comparable operating income x (1 - tax) / average invested capital
    add("roic_comparable_dcf_tax", y, f.roic(cop, DCF_TAX, o, c), "ratio",
        "comparable_OI x (1 - 23.7%) / avg(IC open, IC close)", f"{cop:.0f}, {DCF_TAX}, {o:.0f}, {c:.0f}",
        "ko-roic-evidence.md option B; Q4 8-K " + Q4[y])
    add("roic_comparable_company_tax", y, f.roic(cop, COMP_TAX[y], o, c), "ratio",
        "comparable_OI x (1 - comparable tax rate) / avg IC", f"{cop:.0f}, {COMP_TAX[y]}, {o:.0f}, {c:.0f}",
        "ko-roic-evidence.md option A; Q4 8-K " + Q4[y])
    oo = o - (IRS_DEPOSIT_CAPITAL if y - 1 >= 2024 else 0)
    cc = c - (IRS_DEPOSIT_CAPITAL if y >= 2024 else 0)
    add("roic_comparable_dcf_tax_ex_irs_deposit", y, f.roic(cop, DCF_TAX, oo, cc), "ratio",
        "as roic_comparable_dcf_tax, IC less $6.0bn IRS deposit from FY24", f"{cop:.0f}, {DCF_TAX}, {oo:.0f}, {cc:.0f}",
        "ko-roic-evidence.md option C; FY25 10-K tax note")

with open(OUT / "ratios.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)

# ---- Segment table: Coca-Cola's own operating segments (FY25 10-K Note 20 / Q4 2025 8-K) ----
# revenue, reported OI: FY25 10-K p.117 (Note 20). comparable revenue and OI: Q4 2025 8-K pp.26 and 28.
# reported and organic % change: Q4 2025 8-K p.26 (organic as published); reported % also 10-K p.45.
SEG = [  # name, rev25, rev24, comp_rev25, comp_rev24, oi25, oi24, comp_oi25, comp_oi24, reported %, organic %
    ("EMEA (Europe, Middle East & Africa)", 11513, 10958, 11548, 10912, 4298, 4255, 4335, 4210, 0.05, 0.06),
    ("Latin America", 6334, 6471, 6379, 6425, 3742, 3792, 3831, 3872, -0.02, 0.10),
    ("North America", 19586, 18869, 19599, 18855, 5070, 4556, 5910, 5372, 0.04, 0.04),
    ("Asia Pacific", 5638, 5594, 5666, 5536, 2042, 2156, 2111, 2098, 0.01, 0.05),
    ("Bottling Investments", 5735, 6223, 5735, 6223, 426, 496, 426, 497, -0.08, 0.01),
    ("Corporate", 144, 110, 144, 110, -1816, -5263, -1600, -1964, 0.30, 0.30),
    ("Eliminations", -1009, -1164, -1009, -1164, None, None, None, None, None, None),
    ("Consolidated", 47941, 47061, 48062, 46897, 13762, 9992, 15013, 14085, 0.02, 0.05),
]
with open(OUT / "segments.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["segment", "revenue_fy25_musd", "revenue_fy24_musd", "revenue_growth_reported_calc",
                "revenue_growth_reported_published", "revenue_growth_organic_published",
                "comparable_revenue_fy25_musd", "operating_income_reported_fy25_musd", "operating_income_reported_fy24_musd",
                "comparable_operating_income_fy25_musd", "comparable_operating_income_fy24_musd",
                "comparable_operating_margin_fy25", "comparable_operating_margin_fy24", "source"])
    for (n, r25, r24, cr25, cr24, o25, o24, co25, co24, rep, org) in SEG:
        w.writerow([n, r25, r24, round(f.growth(r25, r24), 6), rep if rep is not None else "n/a",
                    org if org is not None else "n/a", cr25, o25 if o25 is not None else "n/a",
                    o24 if o24 is not None else "n/a", co25 if co25 is not None else "n/a",
                    co24 if co24 is not None else "n/a",
                    round(f.margin(co25, cr25), 6) if co25 is not None and n not in ("Corporate",) else "n/a",
                    round(f.margin(co24, cr24), 6) if co24 is not None and n not in ("Corporate",) else "n/a",
                    "FY25 10-K 0001628280-26-010047 Note 20 p.116-117 (revenue, reported OI); Q4 2025 8-K "
                    "0001628280-26-006642 ex.99.1 p.14 (segment summary), p.26 (comparable revenue, reported and "
                    "organic % change), p.28 (comparable OI)"])
print(f"wrote {len(rows)} ratio rows and {len(SEG)} segment rows")
