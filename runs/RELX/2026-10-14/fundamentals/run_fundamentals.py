"""Fundamentals agent, RELX PLC (RELX / REL.L), run 2026-10-14.

All ratios go through desk/fundamentals.py (growth, margin, roic, cash_conversion, leverage, interest_cover).
Every money input is GBP m (RELX reports in pounds) and carries its document + page. Nothing is estimated.
Inputs were read from the primary SEC filings (downloaded from EDGAR, CIK 929869) or from the Data agent's
financials.csv, which quotes the same filings.

Bases (labelled on every row):
  "group"             RELX as reported (includes print and print-related revenue)
  "ex print"          group less the print & print-related segment (RELX reports print separately from 2025;
                      FY23 and FY24 restated in AR25 note 1 p.145 and note 2 p.146)
  "old segments"      business areas as first reported (print still inside Risk, STM and Legal)

Run from the repo root:  PYTHONPATH=. python runs/RELX/2026-10-14/fundamentals/run_fundamentals.py
"""
import csv
from pathlib import Path

import yaml

from desk.fundamentals import cash_conversion, growth, interest_cover, leverage, margin, roic

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]

# ---- source labels ---------------------------------------------------------------------------------------------
AR25 = "RELX Annual Report 2025 (20-F ex 15.2, 0001104659-26-017277)"
AR24 = "RELX Annual Report 2024 (20-F ex 15.2, 0001558370-25-001178)"
AR22 = "RELX Annual Report 2022 (20-F ex 15.2, 0001558370-23-001846)"
AR21 = "RELX Annual Report 2021 (20-F ex 15.2, 0001193125-22-045453)"
R25 = "RELX FY2025 results (6-K ex 99.1, 0000929869-26-000008)"
R24 = "RELX FY2024 results (6-K ex 99.1, 0000929869-25-000010)"
R23 = "RELX FY2023 results (6-K ex 99.1, 0000929869-24-000016)"
R22 = "RELX FY2022 results (6-K ex 99.1, 0000929869-23-000048)"
R21 = "RELX FY2021 results (6-K ex 99.1, 0001564590-22-004516)"
H126 = "RELX H1 2026 interim results (6-K ex 99.1, 0000929869-26-000054)"
FIVE = f"{AR25} p.186 five year summary"

YEARS = [2021, 2022, 2023, 2024, 2025]
rows, seg_rows, checks = [], [], []


def add(item, year, value, formula, inputs, basis, source, unit="ratio"):
    rows.append({"item": item, "year": year, "value": None if value is None else round(value, 5),
                 "unit": unit, "formula": formula, "inputs": inputs, "basis": basis, "source": source})


# ---- inputs (GBP m) --------------------------------------------------------------------------------------------
revenue = {2020: 7110, 2021: 7244, 2022: 8553, 2023: 9161, 2024: 9434, 2025: 9590}
rev_src = {2020: f"{AR22} p.162 income statement", **{y: FIVE for y in YEARS}}
cost_of_sales = {2021: 2562, 2022: 3045, 2023: 3216, 2024: 3300, 2025: 3233}
cos_src = {2021: f"{AR22} p.162 income statement", 2022: f"{AR22} p.162 income statement",
           **{y: f"{AR25} p.138 income statement" for y in (2023, 2024, 2025)}}
adj_op = {2021: 2210, 2022: 2683, 2023: 3030, 2024: 3199, 2025: 3342}          # adjusted (non-GAAP)
rep_op = {2021: 1884, 2022: 2323, 2023: 2682, 2024: 2861, 2025: 3027}          # IFRS operating profit
adj_ebitda = {2021: 2697, 2022: 3174, 2023: 3544, 2024: 3724, 2025: 3846}
adj_interest = {2021: 133, 2022: 194, 2023: 314, 2024: 296, 2025: 283}         # adjusted net interest expense
rep_interest = {2021: 142, 2022: 201, 2023: 315, 2024: 298, 2025: 286}         # reported net finance costs
adj_cash_flow = {2021: 2230, 2022: 2709, 2023: 2962, 2024: 3101, 2025: 3301}
rep_net_profit = {2021: 1471, 2022: 1634, 2023: 1781, 2024: 1934, 2025: 2065}  # attributable to shareholders
adj_net_profit = {2021: 1689, 2022: 1961, 2023: 2156, 2024: 2241, 2025: 2358}
net_debt = {2021: 6017, 2022: 6604, 2023: 6446, 2024: 6563, 2025: 7201}       # RELX definition, incl. leases
leases = {2021: 208, 2022: 182, 2023: 141, 2024: 103, 2025: 97}                # lease liabilities in net debt
lease_src = "data/financials.csv lease_liabilities (20-F XBRL ifrs-full:LeaseLiabilities); FY25 = FY25 results p.13"
# Adjusted effective tax rate (RELX), applied to adjusted operating profit in RELX's own ROIC
adj_etr = {2021: 0.185, 2022: 0.213, 2023: 0.204, 2024: 0.225, 2025: 0.225}
etr_src = {2021: f"{R21} p.13 ROIC table", 2022: f"{R22} p.13 ROIC table", 2023: f"{R23} p.12 ROIC table",
           2024: f"{AR25} p.204 ROIC table", 2025: f"{AR25} p.204 ROIC table"}
# Average invested capital as RELX defines it (adds back all acquired-intangible amortisation and goodwill impairment,
# retranslated at average FX), published as an average only
avg_ic = {2021: 15108, 2022: 16920, 2023: 17184, 2024: 16743, 2025: 16799}
ic_src = {2021: f"{R22} p.13", 2022: f"{R22} p.13", 2023: f"{R23} p.12", 2024: f"{R24} p.12", 2025: f"{R25} p.14"}
# Net capital employed at 31 Dec (book: net goodwill and intangibles + PP&E + investments + pensions + working capital)
nce = {2020: 9536, 2021: 9810, 2022: 11089, 2023: 10389, 2024: 10571, 2025: 10322}
nce_src = {2020: f"{AR21} p.63", 2021: f"{AR21} p.63 / {AR22} p.85", 2022: f"{AR22} p.85",
           2023: f"{AR24} p.206 APM table", 2024: f"{AR25} p.204 APM table", 2025: f"{AR25} p.204 APM table"}
fcf = {2021: 1672, 2022: 1970, 2023: 1988, 2024: 2126, 2025: 2313}             # free cash flow before dividends
fcf_src = {2021: f"{R21} p.12", 2022: f"{R22} p.11", 2023: f"{R23} p.11", 2024: f"{R24} p.11", 2025: f"{R25} p.11"}

# Published growth (RELX non-GAAP): underlying (organic: excludes FX, M&A, print from 2025, exhibition cycling)
# and constant currency (excludes FX only, so it includes print run-off, disposals and cycling)
underlying = {2021: 0.07, 2022: 0.09, 2023: 0.08, 2024: 0.07, 2025: 0.07}
const_ccy = {2021: 0.08, 2022: 0.11, 2023: 0.07, 2024: 0.06, 2025: 0.04}
fx_effect = {2021: -0.06, 2022: 0.07, 2023: 0.0, 2024: -0.03, 2025: -0.02}
growth_src = {2021: f"{R21} p.1 and revenue paragraph", 2022: f"{R22} revenue paragraph",
              2023: f"{R23} revenue paragraph ('broadly neutral' currency)", 2024: f"{R24} revenue paragraph",
              2025: f"{R25} p.4 and p.9"}

# Print & print-related segment (reported separately from 2025; FY23-24 restated)
print_rev = {2023: 586, 2024: 517, 2025: 399}
print_op = {2023: 253, 2024: 217, 2025: 185}
print_src = f"{AR25} p.145 note 1 (FY23 restatement) and p.146 note 2 segment table"

# H1 (six months to 30 June)
h1 = {"H1 2025": dict(rev=4741, adj_op=1652, rep_op=1490, print_rev=189, print_op=84, ebitda=1908, capex=255, prepub=46),
      "H1 2026": dict(rev=4871, adj_op=1727, rep_op=1585, print_rev=157, print_op=78, ebitda=1992, capex=292, prepub=54)}
H1SRC = f"{H126} p.3 (revenue, adj. OP), p.9 (print revenue and adj. OP), p.10 (EBITDA, capex, pre-publication), p.24 (reported OP)"

# ---- 1. Growth -------------------------------------------------------------------------------------------------
for y in YEARS:
    # Reported growth = revenue in pounds / prior-year revenue - 1 (includes currency, M&A, print run-off)
    add("reported_revenue_growth", y, growth(revenue[y], revenue[y - 1]),
        "revenue / prior-year revenue - 1 (GBP)", f"{revenue[y]} / {revenue[y-1]}", "group",
        f"{rev_src[y]}; {rev_src[y-1]}")
    add("underlying_revenue_growth_published", y, underlying[y],
        "as published by RELX (organic, non-GAAP): constant currency, ex acquisitions <12m, disposals, "
        "exhibition cycling; ex print from 2025", "published", "group", f"{FIVE}; {growth_src[y]}")
    add("constant_currency_revenue_growth_published", y, const_ccy[y],
        "as published by RELX: revenue growth at constant FX (includes M&A, print, cycling)", "published", "group",
        growth_src[y])
    add("currency_effect_on_revenue_growth_published", y, fx_effect[y], "as published by RELX (points of growth)",
        "published", "group", growth_src[y])
add("reported_revenue_growth", "H1 2026", growth(h1["H1 2026"]["rev"], h1["H1 2025"]["rev"]),
    "H1 revenue / prior H1 revenue - 1 (GBP)", "4871 / 4741", "group", f"{H126} p.3")
add("underlying_revenue_growth_published", "H1 2026", 0.07, "as published by RELX (organic, ex print)", "published",
    "group", f"{H126} p.3 and p.9")
add("constant_currency_revenue_growth_published", "H1 2026", 0.05, "as published by RELX", "published", "group",
    f"{H126} p.3")

# FY25 growth bridge (AR25 p.199 'Components of reported revenue growth', GBP m): contribution of each component =
# growth(prior revenue + component, prior revenue), i.e. component / FY24 revenue
bridge = {"underlying": 586, "exhibition_cycling": -48, "acquisitions": 14, "disposals": -91,
          "print_and_print_related": -109, "currency": -196}
for k, v in bridge.items():
    add(f"fy25_growth_contribution_{k}", 2025, growth(revenue[2024] + v, revenue[2024]),
        "component (GBP m) / FY24 revenue", f"{v} / {revenue[2024]}", "group",
        f"{AR25} p.199 APM 'Components of reported revenue growth'")
# Print revenue change (run-off speed)
add("print_revenue_growth", 2024, growth(print_rev[2024], print_rev[2023]), "print revenue / prior - 1",
    "517 / 586", "print segment", print_src)
add("print_revenue_growth", 2025, growth(print_rev[2025], print_rev[2024]), "print revenue / prior - 1",
    "399 / 517", "print segment", print_src)
add("print_revenue_growth", "H1 2026", growth(157, 189), "H1 print revenue / prior H1 - 1", "157 / 189",
    "print segment", f"{H126} p.9")

# ---- 2. Margins ------------------------------------------------------------------------------------------------
for y in YEARS:
    gp = revenue[y] - cost_of_sales[y]  # gross profit = revenue - cost of sales (IFRS income statement line)
    add("gross_margin", y, margin(gp, revenue[y]), "(revenue - cost of sales) / revenue",
        f"({revenue[y]} - {cost_of_sales[y]}) / {revenue[y]}", "group", f"{cos_src[y]}; {rev_src[y]}")
    # Adjusted operating margin (RELX's 'before exceptionals' measure): excludes acquired-intangible amortisation and
    # acquisition/disposal items; JV profit grossed up for JV tax and interest
    add("adjusted_operating_margin", y, margin(adj_op[y], revenue[y]), "adjusted operating profit / revenue (non-GAAP)",
        f"{adj_op[y]} / {revenue[y]}", "group", FIVE)
    add("reported_operating_margin", y, margin(rep_op[y], revenue[y]), "IFRS operating profit / revenue",
        f"{rep_op[y]} / {revenue[y]}", "group", FIVE)
    # The gap between the two = acquired-intangible amortisation + acquisition items + JV tax gross-up, as % of revenue
    add("adjusted_minus_reported_operating_profit_pct_revenue", y, margin(adj_op[y] - rep_op[y], revenue[y]),
        "(adjusted OP - reported OP) / revenue", f"({adj_op[y]} - {rep_op[y]}) / {revenue[y]}", "group", FIVE)
# FY21 adjusted OP includes a GBP 35m one-off corporate real-estate charge (FY21 results p.2): margin without it
add("adjusted_operating_margin_ex_one_off", 2021, margin(adj_op[2021] + 35, revenue[2021]),
    "(adjusted OP + one-off real-estate charge) / revenue", "(2210 + 35) / 7244", "group", f"{R21} p.2; {FIVE}")
for y in (2023, 2024, 2025):
    # Margin without print = (group adjusted OP - print adjusted OP) / (group revenue - print revenue)
    add("adjusted_operating_margin_ex_print", y, margin(adj_op[y] - print_op[y], revenue[y] - print_rev[y]),
        "(adjusted OP - print adjusted OP) / (revenue - print revenue)",
        f"({adj_op[y]} - {print_op[y]}) / ({revenue[y]} - {print_rev[y]})",
        "ex print (FY23-24 restated)", f"{print_src}; {FIVE}")
    add("print_adjusted_operating_margin", y, margin(print_op[y], print_rev[y]), "print adjusted OP / print revenue",
        f"{print_op[y]} / {print_rev[y]}", "print segment", print_src)
for p, d in h1.items():
    add("adjusted_operating_margin", p, margin(d["adj_op"], d["rev"]), "adjusted operating profit / revenue",
        f"{d['adj_op']} / {d['rev']}", "group", H1SRC)
    add("reported_operating_margin", p, margin(d["rep_op"], d["rev"]), "IFRS operating profit / revenue",
        f"{d['rep_op']} / {d['rev']}", "group", H1SRC)
    add("adjusted_operating_margin_ex_print", p, margin(d["adj_op"] - d["print_op"], d["rev"] - d["print_rev"]),
        "(adjusted OP - print adjusted OP) / (revenue - print revenue)",
        f"({d['adj_op']} - {d['print_op']}) / ({d['rev']} - {d['print_rev']})", "ex print", H1SRC)
    add("print_adjusted_operating_margin", p, margin(d["print_op"], d["print_rev"]),
        "print adjusted OP / print revenue", f"{d['print_op']} / {d['print_rev']}", "print segment", H1SRC)

# ---- 3. Returns ------------------------------------------------------------------------------------------------
for y in YEARS:
    # RELX-reported ROIC = adjusted OP x (1 - adjusted ETR) / average invested capital. Only the average is
    # published, so it is passed as both opening and closing (roic() then uses it unchanged).
    add("roic_relx_definition", y, roic(adj_op[y], adj_etr[y], avg_ic[y], avg_ic[y]),
        "adjusted OP x (1 - adjusted ETR) / average invested capital (incl. all acquired goodwill and intangibles "
        "at cost)", f"{adj_op[y]} x (1 - {adj_etr[y]}) / {avg_ic[y]}", "group",
        f"{FIVE}; {etr_src[y]}; {ic_src[y]}")
    # Book ROIC = same NOPAT / average of opening and closing NET CAPITAL EMPLOYED (book values, after amortisation)
    add("roic_book_net_capital_employed", y, roic(adj_op[y], adj_etr[y], nce[y - 1], nce[y]),
        "adjusted OP x (1 - adjusted ETR) / average(opening, closing net capital employed)",
        f"{adj_op[y]} x (1 - {adj_etr[y]}) / avg({nce[y-1]}, {nce[y]})", "group",
        f"{FIVE}; {etr_src[y]}; NCE {nce_src[y-1]} and {nce_src[y]}")
# Sensitivity: FY25 RELX ROIC at the brief's 22.8% tax rate (the terminal RONIC is 15.4% at 22.5%)
add("roic_relx_definition_at_brief_tax_rate", 2025, roic(adj_op[2025], 0.228, avg_ic[2025], avg_ic[2025]),
    "adjusted OP x (1 - 22.8%) / average invested capital", f"3342 x (1 - 0.228) / 16799", "group",
    f"{FIVE}; {R25} p.14; brief dcf.tax_rate")

# ---- 4. Cash conversion ----------------------------------------------------------------------------------------
for y in YEARS:
    # Desk definition: free cash flow / net profit attributable to shareholders. RELX's FCF before dividends =
    # adjusted cash flow (after capex and lease principal) - net interest - cash tax - acquisition/disposal items.
    add("cash_conversion_fcf_to_reported_net_profit", y, cash_conversion(fcf[y], rep_net_profit[y]),
        "free cash flow before dividends / reported net profit attributable", f"{fcf[y]} / {rep_net_profit[y]}",
        "group", f"{fcf_src[y]}; {FIVE}")
    add("cash_conversion_fcf_to_adjusted_net_profit", y, cash_conversion(fcf[y], adj_net_profit[y]),
        "free cash flow before dividends / adjusted net profit attributable", f"{fcf[y]} / {adj_net_profit[y]}",
        "group", f"{fcf_src[y]}; {FIVE}")
    # RELX's own KPI: adjusted cash flow (pre interest and tax) / adjusted operating profit
    add("adjusted_cash_flow_conversion_relx", y, cash_conversion(adj_cash_flow[y], adj_op[y]),
        "adjusted cash flow / adjusted operating profit (RELX KPI; target 90%+)", f"{adj_cash_flow[y]} / {adj_op[y]}",
        "group", FIVE)

# ---- 5. Leverage and interest cover ----------------------------------------------------------------------------
for y in YEARS:
    add("net_debt_to_ebitda_incl_leases", y, leverage(net_debt[y], adj_ebitda[y]),
        "net debt (RELX definition, incl. leases) / adjusted EBITDA (GBP)", f"{net_debt[y]} / {adj_ebitda[y]}",
        "group", FIVE)
    add("net_debt_to_ebitda_ex_leases", y, leverage(net_debt[y] - leases[y], adj_ebitda[y]),
        "(net debt - lease liabilities) / adjusted EBITDA (brief's net debt basis)",
        f"({net_debt[y]} - {leases[y]}) / {adj_ebitda[y]}", "group", f"{FIVE}; {lease_src}")
    # Interest cover = operating profit / net interest expense (times)
    add("interest_cover_adjusted", y, interest_cover(adj_op[y], adj_interest[y]),
        "adjusted OP / adjusted net interest expense", f"{adj_op[y]} / {adj_interest[y]}", "group", FIVE, unit="x")
    add("interest_cover_reported", y, interest_cover(rep_op[y], rep_interest[y]),
        "IFRS OP / reported net finance costs", f"{rep_op[y]} / {rep_interest[y]}", "group", FIVE, unit="x")
# 30 Jun 2026: LTM EBITDA = FY25 - H1 2025 + H1 2026
ltm_ebitda = adj_ebitda[2025] - h1["H1 2025"]["ebitda"] + h1["H1 2026"]["ebitda"]
add("net_debt_to_ebitda_incl_leases", "Jun 2026 LTM", leverage(8733, ltm_ebitda),
    "net debt 30 Jun 2026 / LTM adjusted EBITDA (FY25 - H1 25 + H1 26)", f"8733 / (3846 - 1908 + 1992)", "group",
    f"{H126} p.10-11; {FIVE}")
add("net_debt_to_ebitda_ex_leases", "Jun 2026 LTM", leverage(8733 - 119, ltm_ebitda),
    "(net debt - leases) 30 Jun 2026 / LTM adjusted EBITDA", f"(8733 - 119) / {ltm_ebitda}", "group",
    f"{H126} p.10-11; {FIVE}")
for y, v in {2021: 2.4, 2022: 2.1, 2023: 2.0, 2024: 1.8, 2025: 2.0}.items():
    add("net_debt_to_ebitda_relx_published", y, v, "as published by RELX (in USD, incl. unfunded pensions, ex JV EBITDA)",
        "published", "group", f"{AR25} p.67-68 (via risk/notes.md); FY25 {R25} p.2", unit="x")

# ---- 6. Investment intensity (to test the brief's capex and D&A) -----------------------------------------------
# Capex incl. pre-publication spend as % of revenue (the brief's 7.10% basis)
for y, c, pp, src in [(2024, 484, 92, f"{R25} p.11"), (2025, 525, 102, f"{R25} p.11")]:
    add("capex_incl_prepublication_pct_revenue", y, margin(c + pp, revenue[y]),
        "(capex + pre-publication spend) / revenue", f"({c} + {pp}) / {revenue[y]}", "group", f"{src}; {FIVE}")
for p, d in h1.items():
    add("capex_incl_prepublication_pct_revenue", p, margin(d["capex"] + d["prepub"], d["rev"]),
        "(capex + pre-publication spend) / revenue", f"({d['capex']} + {d['prepub']}) / {d['rev']}", "group", H1SRC)
# D&A on the brief's basis (internally developed + PP&E + pre-publication; excl. leases and acquired intangibles)
add("da_brief_basis_pct_revenue", 2025, margin(352 + 26 + 89, revenue[2025]),
    "(internally developed amortisation + PP&E depreciation + pre-publication amortisation) / revenue",
    "(352 + 26 + 89) / 9590", "group", f"{R25} p.27 note 2; {FIVE}")
add("da_brief_basis_pct_revenue", "H1 2026", margin(193 + 12 + 42, 4871),
    "(internally developed + PP&E + pre-publication) / revenue", "(193 + 12 + 42) / 4871", "group", f"{H126} p.25")

# ---- 7. Segments (RELX's operating segments) and geography -----------------------------------------------------
SEG_SRC = {
    "FY2023 restated": f"{AR25} p.145 note 1 restatement table",
    "FY2024 restated": f"{AR25} p.146 note 2; growth not restated (old-basis rates in {R24} p.4)",
    "FY2025": f"{AR25} p.146 note 2; growth rates {R25} p.4",
    "H1 2025": f"{H126} p.4 (print p.9)",
    "H1 2026": f"{H126} p.4 (print p.9)",
}
seg = {  # (revenue, adjusted OP, underlying revenue growth, constant-currency revenue growth)
    "FY2023 restated": {"Risk": (3224, 1170, None, None), "Scientific, Technical & Medical": (2581, 940, None, None),
                        "Legal": (1655, 360, None, None), "Exhibitions": (1115, 319, None, None),
                        "Print & print-related": (586, 253, None, None)},
    "FY2024 restated": {"Risk": (3336, 1233, None, None), "Scientific, Technical & Medical": (2624, 981, None, None),
                        "Legal": (1718, 381, None, None), "Exhibitions": (1239, 398, None, None),
                        "Print & print-related": (517, 217, None, None)},
    "FY2025": {"Risk": (3485, 1305, 0.08, 0.07), "Scientific, Technical & Medical": (2714, 1035, 0.05, 0.05),
               "Legal": (1806, 415, 0.09, 0.08), "Exhibitions": (1186, 410, 0.08, -0.02),
               "Print & print-related": (399, 185, None, None)},
    "H1 2025": {"Risk": (1748, 660, None, None), "Scientific, Technical & Medical": (1323, 491, None, None),
                "Legal": (900, 188, None, None), "Exhibitions": (581, 234, None, None),
                "Print & print-related": (189, 84, None, None)},
    "H1 2026": {"Risk": (1810, 697, 0.08, 0.07), "Scientific, Technical & Medical": (1370, 519, 0.06, 0.06),
                "Legal": (959, 208, 0.10, 0.09), "Exhibitions": (575, 226, 0.06, 0.01),
                "Print & print-related": (157, 78, None, None)},
}
prior = {"FY2024 restated": "FY2023 restated", "FY2025": "FY2024 restated", "H1 2026": "H1 2025"}
for per, segs in seg.items():
    for name, (r, op, ug, cc) in segs.items():
        pr = seg[prior[per]][name][0] if per in prior else None
        seg_rows.append({"kind": "operating segment", "name": name, "period": per, "revenue_mgbp": r,
                         "adjusted_operating_profit_mgbp": op,
                         "adjusted_operating_margin": round(margin(op, r), 5),
                         "reported_revenue_change_gbp": None if pr is None else round(growth(r, pr), 5),
                         "underlying_revenue_growth_published": ug, "constant_currency_growth_published": cc,
                         "source": SEG_SRC[per]})
# FY24 underlying growth on the OLD segment basis (print inside Risk/STM/Legal), as first reported
for name, ug in {"Risk": 0.08, "Scientific, Technical & Medical": 0.04, "Legal": 0.07, "Exhibitions": 0.11}.items():
    seg_rows.append({"kind": "operating segment (old basis, as first reported)", "name": name, "period": "FY2024",
                     "revenue_mgbp": None, "adjusted_operating_profit_mgbp": None, "adjusted_operating_margin": None,
                     "reported_revenue_change_gbp": None, "underlying_revenue_growth_published": ug,
                     "constant_currency_growth_published": None,
                     "source": f"{R24} p.4 business area analysis (not comparable with FY25 basis)"})
# Geography: RELX discloses revenue by geographical market in three regions only (AR25 note 2 p.146-147)
geo = {"North America": {2023: 5386, 2024: 5495, 2025: 5595, "H1 2025": 2837, "H1 2026": 2878},
       "Europe (incl. UK)": {2023: 1908, 2024: 2025, 2025: 2000, "H1 2025": 956, "H1 2026": 1018},
       "Rest of world": {2023: 1867, 2024: 1914, 2025: 1995, "H1 2025": 948, "H1 2026": 975}}
geo_tot = {2023: 9161, 2024: 9434, 2025: 9590, "H1 2025": 4741, "H1 2026": 4871}
for name, v in geo.items():
    for per, r in v.items():
        pr = {2024: 2023, 2025: 2024, "H1 2026": "H1 2025"}.get(per)
        src = f"{AR25} p.146 (2023) and p.147 (2024-25) note 2 'Revenue by geographical market'" \
            if isinstance(per, int) else f"{H126} p.24 note 2"
        seg_rows.append({"kind": "geographical market (not an operating segment)", "name": name, "period": per,
                         "revenue_mgbp": r, "adjusted_operating_profit_mgbp": None, "adjusted_operating_margin": None,
                         "reported_revenue_change_gbp": None if pr is None else round(growth(r, v[pr]), 5),
                         "underlying_revenue_growth_published": "not published",
                         "constant_currency_growth_published": "not published",
                         "source": src + f"; share of group = {round(margin(r, geo_tot[per]), 5)}"})
for name in ["Asia Pacific", "Latin America & Caribbean", "Africa"]:
    seg_rows.append({"kind": "template region", "name": name, "period": "FY2025", "revenue_mgbp": "not published",
                     "adjusted_operating_profit_mgbp": None, "adjusted_operating_margin": None,
                     "reported_revenue_change_gbp": None, "underlying_revenue_growth_published": "not published",
                     "constant_currency_growth_published": "not published",
                     "source": f"{AR25} p.146-147: RELX splits only North America / Europe / Rest of world"})

# ---- 7b. Changes in margin (percentage points, as decimals) ---------------------------------------------------
R0 = {(r["item"], r["year"]): r["value"] for r in rows}


def pts(item, year, a, b, formula, src):
    # change in a ratio = later value - earlier value (decimal; 0.01 = 1 percentage point)
    add(item, year, a - b, formula, f"{a} - {b}", "group", src, unit="ratio points")


pts("adjusted_margin_change_fy21_fy25_reported_basis", "FY21-FY25", R0[("adjusted_operating_margin", 2025)],
    R0[("adjusted_operating_margin", 2021)], "FY25 adjusted margin - FY21 adjusted margin", "ratios.csv rows above")
pts("adjusted_margin_change_fy21_fy25_ex_one_off", "FY21-FY25", R0[("adjusted_operating_margin", 2025)],
    R0[("adjusted_operating_margin_ex_one_off", 2021)], "FY25 adjusted margin - FY21 margin ex GBP 35m charge",
    "ratios.csv rows above")
pts("gross_margin_change", 2025, R0[("gross_margin", 2025)], R0[("gross_margin", 2024)],
    "FY25 gross margin - FY24 gross margin", "ratios.csv rows above")
pts("bear_margin_minus_fy23_ex_print_margin", 2023, yaml.safe_load(open(REPO / "briefs" / "RELX.yaml"))["scenarios"]["bear"]["bear_agent_margin"], R0[("adjusted_operating_margin_ex_print", 2023)],
    "brief bear margin (scenarios.bear.bear_agent_margin) - FY23 adjusted margin ex print", "briefs/RELX.yaml; ratios.csv")

# ---- 8. Brief assumptions vs the record ------------------------------------------------------------------------
full_brief = yaml.safe_load(open(REPO / "briefs" / "RELX.yaml"))
brief = full_brief["dcf"]
bear_margin = full_brief["scenarios"]["bear"]["bear_agent_margin"]
R = {(r["item"], r["year"]): r["value"] for r in rows}


def chk(assumption, brief_value, record, record_value, verdict):
    checks.append({"assumption": assumption, "brief_value": brief_value, "record": record,
                   "record_value": None if record_value is None else round(record_value, 5), "verdict": verdict})


chk("FY26 growth (GBP)", brief["organic_growth"][0], "H1 2026 reported revenue growth",
    R[("reported_revenue_growth", "H1 2026")], "consistent (the brief's own rule)")
avg_rep = sum(R[("reported_revenue_growth", y)] for y in YEARS) / 5  # simple average of FY21-25 reported growth
chk("FY27-30 growth", brief["organic_growth"][1], "FY21-25 average reported GBP growth", avg_rep,
    "brief is below the 5-yr average, which is lifted by FY22 (+7pt FX, exhibitions recovery)")
chk("FY27-30 growth", brief["organic_growth"][1], "FY25 print drag on group growth",
    R[("fy25_growth_contribution_print_and_print_related", 2025)],
    "print drag shrinks as print shrinks; constant-ccy growth should drift up towards underlying (7%): 5% is cautious")
chk("Base margin (ex print, held flat)", brief["base_margin"], "H1 2026 adjusted margin ex print",
    R[("adjusted_operating_margin_ex_print", "H1 2026")], "matches the brief's computation")
chk("Base margin (ex print, held flat)", brief["base_margin"], "FY25 adjusted margin ex print",
    R[("adjusted_operating_margin_ex_print", 2025)], "FY23-FY25 ex-print margin rose each year; flat is cautious")
chk("Bear margin 33.1% labelled 'FY23 level'", bear_margin, "FY23 adjusted margin ex print",
    R[("adjusted_operating_margin_ex_print", 2023)],
    "FLAG: 33.1% is the FY23 GROUP margin incl. print; on the brief's ex-print basis FY23 was lower")
chk("Tax rate", brief["tax_rate"], "FY25 adjusted ETR", adj_etr[2025], "consistent (H1 2026 22.8% vs FY24-25 22.5%)")
chk("Capex incl. pre-publication", brief["capex_pct_sales"], "FY25 (capex + pre-publication) / revenue",
    R[("capex_incl_prepublication_pct_revenue", 2025)], "brief above FY25; H1 2026 is the highest period on record")
chk("D&A (brief basis)", brief["da_pct_sales"], "FY25 D&A on brief basis / revenue",
    R[("da_brief_basis_pct_revenue", 2025)], "consistent; capex exceeds D&A by about 2% of revenue")
chk("Terminal RONIC", brief["terminal_ronic"], "FY25 RELX ROIC recomputed", R[("roic_relx_definition", 2025)],
    "consistent with RELX's own measure; book ROIC is much higher (see roic_book_net_capital_employed)")
chk("Terminal RONIC", brief["terminal_ronic"], "FY25 book ROIC on net capital employed",
    R[("roic_book_net_capital_employed", 2025)], "brief takes the cautious measure")

# ---- write ------------------------------------------------------------------------------------------------------
for fname, data in [("ratios.csv", rows), ("segments.csv", seg_rows), ("brief_checks.csv", checks)]:
    with open(HERE / fname, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(data[0].keys()))
        w.writeheader()
        w.writerows(data)
    print(fname, len(data), "rows")
