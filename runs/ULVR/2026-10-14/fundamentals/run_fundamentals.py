"""Fundamentals agent, Unilever (ULVR), run 2026-10-14.

All ratios go through desk/fundamentals.py (growth, margin, roic, cash_conversion, leverage, interest_cover).
Every input is EUR m (Unilever reports in euros) and carries its filing + page. Nothing is estimated.

Bases (label on every row):
  FY21-FY22  "Group incl. Ice Cream, as first reported"
  FY23-FY25  "continuing operations, re-presented WITHOUT Ice Cream (FY25 20-F)" unless a row says otherwise.
  Some FY23 items (ROIC, FCF, net debt, UEBITDA) exist only incl. Ice Cream: labelled as such.

Run from the repo root:  PYTHONPATH=. python runs/ULVR/2026-10-14/fundamentals/run_fundamentals.py
"""
import csv
from pathlib import Path

from desk.fundamentals import cash_conversion, growth, interest_cover, leverage, margin, roic

HERE = Path(__file__).resolve().parent

# ---- source labels ---------------------------------------------------------------------------------------------
F25 = "Unilever FY25 Form 20-F (accession 0000217410-26-000007)"
F24 = "Unilever FY24 Form 20-F (accession 0000217410-25-000015) XBRL"
F23 = "Unilever FY23 Form 20-F (accession 0000217410-24-000017) XBRL"
F22 = "Unilever FY22 Form 20-F (accession 0000217410-23-000016) XBRL"
F21 = "Unilever FY21 Form 20-F (accession 0000217410-22-000009) XBRL"
K25 = "Unilever FY25 results 6-K (0001654954-26-001155)"
K24 = "Unilever FY24 results 6-K (0001654954-25-001439)"
K23 = "Unilever FY23 results 6-K (0001654954-24-001469)"
K22 = "Unilever FY22 results 6-K (0001654954-23-001506)"
K21 = "Unilever FY21 results 6-K (0001654954-22-001398)"
H126 = "Unilever H1 2026 results 6-K (0000217410-26-000057)"
F425 = "Form 425 investor presentation (0000217410-26-000027) slide 25"

INC = "Group incl. Ice Cream, as first reported"
EXC = "continuing ops, re-presented without Ice Cream"

rows = []


def add(item, year, value, formula, inputs, basis, source, unit="ratio"):
    rows.append({"item": item, "year": year, "value": None if value is None else round(value, 5),
                 "unit": unit, "formula": formula, "inputs": inputs, "basis": basis, "source": source})


# ---- 1. Sales growth -------------------------------------------------------------------------------------------
# Reported growth = turnover change in euros (includes currency and acquisitions/disposals).
turnover = {  # (year, basis): (value EUR m, source)
    (2020, INC): (50724, f"{F21} ifrs-full:Revenue"),
    (2021, INC): (52444, f"{F23} ifrs-full:Revenue"),
    (2022, INC): (60073, f"{F24} ifrs-full:Revenue"),
    (2023, INC): (59604, f"{F24} ifrs-full:Revenue"),
    (2024, INC): (60761, f"{F24} ifrs-full:Revenue"),
    (2023, EXC): (51680, f"{F25} p.137 note 2 segment table"),
    (2024, EXC): (52479, f"{F25} p.137 note 2 segment table"),
    (2025, EXC): (50503, f"{F25} p.137 note 2 segment table"),
}
for yr, cur_b, prev_b in [(2021, INC, INC), (2022, INC, INC), (2023, INC, INC), (2024, EXC, EXC),
                          (2024, INC, INC), (2025, EXC, EXC)]:
    c, cs = turnover[(yr, cur_b)]
    p, ps = turnover[(yr - 1, prev_b)]
    add("reported_sales_growth", yr, growth(c, p), "turnover / prior-year turnover - 1 (same basis both years)",
        f"{c} / {p}", cur_b, f"{cs}; {ps}")

# Organic growth = Unilever's underlying sales growth (USG) as PUBLISHED (excludes currency, M&A and price
# growth above 26% in hyperinflationary economies). Not recomputed: taken from each year's results 6-K headline.
usg = {2021: (0.045, K21, INC), 2022: (0.090, K22, INC), 2023: (0.070, K23, INC),
       2024: (0.042, K24, INC), 2025: (0.035, f"{K25}; {F25} p.12", EXC)}
for yr, (v, s, b) in usg.items():
    add("organic_sales_growth_usg", yr, v, "as published by Unilever (USG, non-GAAP)", "published", b,
        f"{s} headline 'Underlying sales growth (USG)'")

# ---- 2. Gross margin -------------------------------------------------------------------------------------------
# Gross margin = gross profit / turnover (gross profit = turnover - cost of sales incl. distribution costs).
gp = {(2021, INC): (22185, f"{F23} ifrs-full:GrossProfit"), (2022, INC): (24167, f"{F24} ifrs-full:GrossProfit"),
      (2023, INC): (25175, f"{F24} ifrs-full:GrossProfit"), (2024, INC): (27370, f"{F24} ifrs-full:GrossProfit"),
      (2023, EXC): (22500, f"{F25} p.139 note 3"), (2024, EXC): (24503, f"{F25} p.139 note 3"),
      (2025, EXC): (23709, f"{F25} p.139 note 3")}
for key in [(2021, INC), (2022, INC), (2023, EXC), (2024, EXC), (2025, EXC), (2023, INC), (2024, INC)]:
    g, gs = gp[key]
    t, ts = turnover[key]
    add("gross_margin", key[0], margin(g, t), "gross profit / turnover", f"{g} / {t}", key[1], f"{gs}; {ts}")

# ---- 3. Operating margins --------------------------------------------------------------------------------------
# Underlying operating margin (non-GAAP) = operating profit before non-underlying items (restructuring,
# disposals, impairments, acquisition costs) / turnover. Reported margin = IFRS operating profit / turnover.
uop = {(2021, INC): (9636, f"{K22} ROIC reconciliation"), (2022, INC): (9683, f"{K22} ROIC reconciliation"),
       (2023, INC): (9931, f"{K23} ROIC reconciliation"), (2024, INC): (11179, f"{K24} ROIC reconciliation"),
       (2023, EXC): (9079, f"{F25} p.137 note 2"), (2024, EXC): (10198, f"{F25} p.137 note 2"),
       (2025, EXC): (10084, f"{F25} p.137 note 2")}
op = {(2021, INC): (8702, f"{F23} ifrs-full:ProfitLossFromOperatingActivities"),
      (2022, INC): (10755, f"{F24} ifrs-full:ProfitLossFromOperatingActivities"),
      (2023, INC): (9758, f"{K23} ROIC reconciliation"), (2024, INC): (9400, f"{K24} ROIC reconciliation"),
      (2023, EXC): (8998, f"{F25} p.137 note 2"), (2024, EXC): (8829, f"{F25} p.137 note 2"),
      (2025, EXC): (9037, f"{F25} p.137 note 2")}
for key in [(2021, INC), (2022, INC), (2023, EXC), (2024, EXC), (2025, EXC), (2023, INC), (2024, INC)]:
    t, ts = turnover[key]
    u, us = uop[key]
    o, os_ = op[key]
    add("operating_margin_underlying", key[0], margin(u, t), "underlying operating profit / turnover (non-GAAP)",
        f"{u} / {t}", key[1], f"{us}; {ts}")
    add("operating_margin_reported", key[0], margin(o, t), "IFRS operating profit / turnover",
        f"{o} / {t}", key[1], f"{os_}; {ts}")

# Restructuring as % of turnover (the gap the PM's 17.7% base margin deducts); FY21-22 Group, FY23-25 ex Ice Cream.
restr = {2021: (632, f"{F23} ifrs-full:ExpenseOfRestructuringActivities"),
         2022: (777, f"{F24} ifrs-full:ExpenseOfRestructuringActivities"),
         2023: (425, f"{F25} ifrs-full:ExpenseOfRestructuringActivities"),
         2024: (710, f"{F25} ifrs-full:ExpenseOfRestructuringActivities"),
         2025: (599, f"{F25} ifrs-full:ExpenseOfRestructuringActivities")}
for yr, (r, rs) in restr.items():
    b = INC if yr <= 2022 else EXC
    t, ts = turnover[(yr, b)]
    add("restructuring_pct_turnover", yr, margin(r, t), "restructuring costs / turnover", f"{r} / {t}", b,
        f"{rs}; {ts}")

# ---- 4. ROIC ---------------------------------------------------------------------------------------------------
# ROIC = underlying operating profit x (1 - underlying effective tax rate) / average invested capital
# (invested capital = goodwill + intangibles + PP&E + net assets held for sale + inventories + trade receivables
#  - trade payables, Unilever's definition).
roic_in = [  # year, UOP, underlying ETR, IC open, IC close, basis, source
    (2021, 9636, 0.226, 40795, 45763, INC, f"{K21} ROIC reconciliation (ETR 22.6%)"),
    (2022, 9683, 0.241, 45763, 46247, INC, f"{K22} ROIC reconciliation (ETR 24.1%)"),
    (2023, 9931, 0.256, 46247, 44726, INC, f"{K23} ROIC reconciliation (ETR 25.6%)"),
    (2024, 11179, 0.258, 44726, 47187, INC, f"{K24} ROIC reconciliation (ETR 25.8%)"),
    # FY24 re-presented: only the average (39,559) is disclosed, so it is passed as both open and close.
    (2024, 10198, 0.259, 39559, 39559, EXC, f"{F25} p.45 ROIC table, average IC only (ETR 25.9%)"),
    (2025, 10084, 0.257, 40706, 38298, EXC, f"{F25} p.45 ROIC table (2024 close adjusted for Ice Cream, ETR 25.7%)"),
]
for yr, u, tx, o_, c_, b, s in roic_in:
    add("roic_underlying", yr, roic(u, tx, o_, c_), "UOP x (1 - underlying ETR) / average(IC open, IC close)",
        f"{u}, {tx}, {o_}, {c_}", b, s)
for yr, v, b, s in [(2021, 0.172, INC, K21), (2022, 0.160, INC, K22), (2023, 0.162, INC, K23),
                    (2024, 0.181, INC, K24), (2024, 0.191, EXC, f"{F25} p.45"), (2025, 0.190, EXC, f"{F25} p.45; {K25}")]:
    add("roic_underlying_published", yr, v, "as published by Unilever", "published", b, s)
# ROIC after restructuring (basis of the agreed terminal RONIC 17.8%): restructuring is a recurring cost, so it is
# deducted from UOP before tax; tax at the brief's 26.0%; FY25 average invested capital 39,502.
uop_after_restr = 10084 - 599
add("roic_after_restructuring", 2025, roic(uop_after_restr, 0.26, 39502, 39502),
    "(UOP - restructuring) x (1 - 26.0% brief tax) / average IC", "10084 - 599 = 9485, 0.26, 39502, 39502", EXC,
    f"{F25} p.45 ROIC table; restructuring {F25} XBRL ExpenseOfRestructuringActivities; tax briefs/ULVR.yaml dcf.tax_rate")
add("roic_after_restructuring_actual_etr", 2025, roic(uop_after_restr, 0.257, 39502, 39502),
    "(UOP - restructuring) x (1 - 25.7% FY25 underlying ETR) / average IC", "9485, 0.257, 39502, 39502", EXC,
    f"{F25} p.43 (ETR) and p.45 (IC)")

# ---- 5. Cash conversion ----------------------------------------------------------------------------------------
# Cash conversion (desk definition) = free cash flow / net profit attributable to shareholders.
# Unilever FCF = cash from operations - tax paid - net capex - net interest paid.
cc_in = [
    (2021, 6393, 6049, INC, f"FCF {K22} FCF reconciliation; net profit {F23} ifrs-full:ProfitLossAttributableToOwnersOfParent"),
    (2022, 5198, 7642, INC, f"FCF {K22}; net profit {F24} XBRL (includes c.EUR 2.3bn gain on the Tea sale, {K23})"),
    (2023, 7091, 6487, INC, f"FCF {K23}; net profit {F25} p.128 total attributable (incl. Ice Cream)"),
    (2024, 6304, 5430, EXC, f"FCF {F25} p.44 (re-presented); net profit continuing attributable {F25} p.128"),
    (2025, 5921, 5682, EXC, f"FCF {F25} p.44; net profit continuing attributable {F25} p.128"),
]
for yr, fcf, np_, b, s in cc_in:
    add("cash_conversion", yr, cash_conversion(fcf, np_), "free cash flow / net profit attributable to shareholders",
        f"{fcf} / {np_}", b, s)
for yr, v, b, s in [(2022, 0.97, INC, K23), (2023, 1.11, INC, K23), (2024, 1.06, INC, K24),
                    (2024, 1.04, EXC, f"{F25} p.44"), (2025, 1.00, EXC, f"{F25} p.44")]:
    add("cash_conversion_unilever_definition", yr, v,
        "as published: FCF excl. tax on disposals / net profit excl. disposals, JVs, associates", "published", b, s)

# ---- 6. Net debt / EBITDA --------------------------------------------------------------------------------------
# Leverage = net debt (Unilever definition, leases inside) / underlying EBITDA (UOP + depreciation & amortisation).
lev_in = [
    (2021, 25510, 11382, INC, f"{K21} net debt reconciliation; UEBITDA {K22}"),
    (2022, 23676, 11408, INC, f"{K22} net debt and UEBITDA reconciliations"),
    (2023, 23657, 11509, INC, f"{K23} net debt; UEBITDA {K24}"),
    (2024, 24519, 12803, INC, f"{K24} net debt and UEBITDA (as first reported, 1.9x)"),
    (2024, 24519, 11434, "net debt at 31 Dec 2024 (incl. Ice Cream) / UEBITDA re-presented without Ice Cream",
     f"net debt {K25}; UEBITDA {F25} p.44"),
    (2025, 23076, 11394, EXC, f"{F25} p.44 (UEBITDA); net debt {K25} / {F25} p.164 note 15C"),
]
for yr, nd, eb, b, s in lev_in:
    add("net_debt_to_underlying_ebitda", yr, leverage(nd, eb), "net debt / underlying EBITDA", f"{nd} / {eb}", b, s,
        unit="x")

# ---- 7. Interest cover -----------------------------------------------------------------------------------------
# Interest cover = operating profit / net finance costs (net finance costs include the pension interest credit).
ic_in = [
    (2021, 9636, 8702, 354, INC, f"{K21} (net finance costs 354)"),
    (2022, 9683, 10755, 493, INC, f"{K22} (net finance costs 493)"),
    (2023, 9079, 8998, 409, EXC, f"{F25} XBRL ifrs-full:FinanceIncomeCost and p.137"),
    (2024, 10198, 8829, 520, EXC, f"{F25} p.44 UEBITDA reconciliation and p.137"),
    (2025, 10084, 9037, 503, EXC, f"{F25} p.44 UEBITDA reconciliation and p.137"),
]
for yr, u, o, nf, b, s in ic_in:
    add("interest_cover_underlying", yr, interest_cover(u, nf), "underlying operating profit / net finance costs",
        f"{u} / {nf}", b, s, unit="x")
    add("interest_cover_reported", yr, interest_cover(o, nf), "IFRS operating profit / net finance costs",
        f"{o} / {nf}", b, s, unit="x")

# ---- 8. Minorities' share of operating profit of the business that REMAINS after the Foods sale ----------------
# Proportionate minorities (brief bridge.minorities_method): outside shareholders own this share of the DCF value.
# Step A: minorities' share of the Group's UNDERLYING net profit (continuing ops), FY24 (cleaner HUL year).
#   underlying NCI profit = reported NCI profit (609) - NCI share of non-underlying items after tax (+22)
#   underlying Group profit = underlying profit to shareholders (6,816) + underlying NCI profit
# Step B: assume minorities' share of operating profit = their share of net profit (A1), and that all minority
#   profit stays with Unilever (A2: HUL incl. India Foods stays; the perimeter excludes India).
# Step C: re-base onto the remaining company: x Group UOP / (Group UOP - Foods perimeter UOP), FY25.
nci_rep_24, nci_nonund_24, sh_und_24 = 609, 22, 6816
nci_und_24 = nci_rep_24 - nci_nonund_24                         # minorities' underlying profit, FY24
grp_und_24 = sh_und_24 + nci_und_24                             # Group underlying net profit (before minorities)
share_grp_24 = margin(nci_und_24, grp_und_24)                   # minorities' share of Group profit
uop_25, perim_uop_25 = 10084, 2600
remain_uop_25 = uop_25 - perim_uop_25                           # remaining company UOP (ex Foods perimeter)
rebase = margin(uop_25, remain_uop_25)                          # Group UOP / remaining UOP
nci_uop_equiv = share_grp_24 * uop_25                           # minorities' operating-profit equivalent
minority_share = margin(nci_uop_equiv, remain_uop_25)           # = share_grp_24 x rebase

SRC_MIN = (f"NCI continuing 609 and Group net profit 6,039: {F25} p.128 income statement; NCI share of "
           f"non-underlying items +22: {F25} p.42; underlying profit to shareholders 6,816: {F25} p.43; "
           f"UOP 10,084: {F25} p.137; Foods perimeter UOP 2,600: {F425} (perimeter excludes India Foods)")
add("nci_share_group_underlying_profit", 2024, share_grp_24,
    "(NCI 609 - NCI non-underlying 22) / (shareholders' underlying 6,816 + NCI underlying 587)",
    f"{nci_und_24} / {grp_und_24}", EXC, SRC_MIN)
add("remaining_company_uop_meur", 2025, remain_uop_25, "Group UOP - Foods perimeter UOP", f"{uop_25} - {perim_uop_25}",
    "FY25 continuing less Foods sale perimeter", SRC_MIN, unit="EUR m")
add("minority_share_of_operating_profit", 2025, minority_share,
    "FY24 NCI share of Group underlying profit x Group UOP FY25 / (Group UOP FY25 - perimeter UOP)",
    f"{share_grp_24:.5f} x {uop_25} / {remain_uop_25}", "remaining company (ex Foods perimeter)", SRC_MIN)

# Cross-checks (same method, other periods).
nci_und_25 = 531 - (-34)                                        # FY25: NCI share of non-underlying items was -34
share_grp_25 = margin(nci_und_25, 6761 + nci_und_25)
add("minority_share_check_fy25", 2025, margin(share_grp_25 * uop_25, remain_uop_25),
    "FY25 NCI share of underlying profit x UOP / remaining UOP", f"{nci_und_25} / {6761 + nci_und_25}; {uop_25}/{remain_uop_25}",
    "cross-check", f"{F25} p.42, p.43, p.128; {F425}")
nci_und_h1 = 267 - 2                                            # H1 2026: NCI share of non-underlying items +2
share_grp_h1 = margin(nci_und_h1, 3508 + nci_und_h1)
add("minority_share_check_h1_2026", 2026, margin(share_grp_h1 * uop_25, remain_uop_25),
    "H1 2026 NCI share of underlying profit x FY25 UOP / remaining UOP",
    f"{nci_und_h1} / {3508 + nci_und_h1}; {uop_25}/{remain_uop_25}", "cross-check (H1 2026 incl. Foods)",
    f"{H126} underlying EPS reconciliation and non-underlying items note; {F425}")
# HUL consistency: HUL minorities' share of HUL profit should equal the 38.1% outside holding (61.90% Unilever).
add("hul_nci_share_of_hul_profit", 2024, margin(446, 1167), "HUL NCI share of profit / HUL profit after tax",
    "446 / 1167", "HUL as consolidated", f"{F25} p.162 note 15B; Unilever stake 61.90% p.194")
add("hul_nci_share_of_hul_profit", 2025, margin(539, 940), "HUL NCI share of profit / HUL profit after tax",
    "539 / 940", "HUL as consolidated (distorted: HUL ice cream demerger)", f"{F25} p.162 note 15B")
add("hul_nci_share_of_group_underlying_profit", 2024, margin(446, grp_und_24),
    "HUL NCI profit / Group underlying net profit", f"446 / {grp_und_24}", EXC, f"{F25} p.162, p.43, p.42")

# ---- Reference items quoted in commentary / flags (not ratios) --------------------------------------------------
add("demerger_gain_in_net_profit_meur", 2025, 3373, "reported, non-cash gain on the Ice Cream demerger (discontinued ops)",
    "published", "total Group (discontinued operations)", f"{F25} p.128 income statement", unit="EUR m")
add("non_underlying_items_in_operating_profit_meur", 2022, 10755 - 9683, "IFRS operating profit - UOP (net gain; Tea sale)",
    "10755 - 9683", INC, f"{K22} ROIC reconciliation; Tea gain EUR 2.3bn per {K23}", unit="EUR m")
add("non_underlying_items_in_operating_profit_meur", 2024, 10198 - 8829, "UOP - IFRS operating profit (net charge)",
    "10198 - 8829", EXC, f"{F25} p.137 note 2 (disposal losses, productivity programme)", unit="EUR m")

with open(HERE / "ratios.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)

# ---- Segments (FY25 20-F; USG where Unilever publishes it) ------------------------------------------------------
seg = []


def sadd(kind, name, year, turnover_meur, usg_pct, reported_change, uop_meur, uom, source):
    seg.append({"kind": kind, "segment": name, "year": year, "turnover_meur": turnover_meur,
                "organic_growth_usg": usg_pct, "reported_turnover_change": None if reported_change is None
                else round(reported_change, 5), "underlying_operating_profit_meur": uop_meur,
                "underlying_operating_margin": None if uom is None else round(uom, 5), "source": source})


bg = {  # name: (T25, UOP25, T24, UOP24, USG25, page, USG24 first reported)
    "Beauty & Wellbeing": (12848, 2471, 13157, 2552, 0.043, "p.19", 0.065),
    "Personal Care": (13161, 2973, 13618, 3014, 0.047, "p.22", 0.052),
    "Home Care": (11565, 1718, 12352, 1785, 0.026, "p.25", 0.029),
    "Foods": (12929, 2922, 13352, 2847, 0.025, "p.28", 0.026),
}
for name, (t25, u25, t24, u24, g25, pg, g24) in bg.items():
    # Segment growth = turnover change in euros; margin = segment UOP / segment turnover.
    sadd("business_group (operating segment)", name, 2025, t25, g25, growth(t25, t24), u25, margin(u25, t25),
         f"{F25} p.137 note 2 (turnover, UOP); USG {F25} {pg} and p.12")
    sadd("business_group (operating segment)", name, 2024, t24, g24, None, u24, margin(u24, t24),
         f"{F25} p.137 note 2 (re-presented without Ice Cream); USG {K24} (as first reported)")
sadd("business_group (operating segment)", "Total", 2025, 50503, 0.035, growth(50503, 52479), 10084,
     margin(10084, 50503), f"{F25} p.137, p.12")
sadd("sale perimeter", "Foods sale perimeter (Foods ex India Foods, Lifestyle Nutrition, Lipton RTD)", 2025, 10700,
     0.027, None, 2600, margin(2600, 10700), F425)
sadd("remaining company", "Unilever ex Foods perimeter", 2025, 50503 - 10700, None, None, remain_uop_25,
     margin(remain_uop_25, 50503 - 10700), f"{F25} p.137 less {F425}")

geo = [  # name, T25, T24, USG25, source of USG
    ("Asia Pacific Africa", 22427, 23448, 0.046, f"{K25} 'Full Year Review: Geographical Areas' (20-F p.12 says 'mid-single-digit' for Asia Pacific)"),
    ("The Americas", 18622, 19605, 0.033, f"{K25} 'Full Year Review: Geographical Areas'"),
    ("  of which North America", 11220, 11140, 0.053, f"{F25} p.12"),
    ("  of which Latin America", 7402, 8465, 0.005, f"{F25} p.12"),
    ("Europe", 9454, 9426, 0.015, f"{F25} p.12"),
    ("Emerging markets", 30008, 32033, 0.035, f"{F25} p.12"),
    ("Developed markets", 20495, 20446, 0.036, f"{F25} p.12"),
]
for name, t25, t24, g25, gs in geo:
    sadd("geography (additional information, not a segment)", name, 2025, t25, g25, growth(t25, t24), None, None,
         f"turnover {F25} p.138 note 2 'Additional information by geographies'; USG {gs}")
for name, t25, t24, g25, gs in [("United States", 10497, 10393, None, "USG not published"),
                                ("India", 6217, 6492, 0.040, f"{F25} p.12"),
                                ("United Kingdom", 2226, 2202, None, "USG not published")]:
    sadd("country", name, 2025, t25, g25, growth(t25, t24), None, None, f"turnover {F25} p.138 note 2; USG {gs}")
sadd("geography", "Africa (separately)", 2025, None, None, None, None, None,
     f"MISSING: Africa is inside 'Asia Pacific Africa'; no turnover or USG figure ({F25} p.12 says only 'low single-digit growth')")

with open(HERE / "segments.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(seg[0].keys()))
    w.writeheader()
    w.writerows(seg)

print(f"minority_share_of_operating_profit = {minority_share:.5f}  (group share FY24 {share_grp_24:.5f}, "
      f"rebase {rebase:.5f}, NCI UOP-equivalent {nci_uop_equiv:.1f}, remaining UOP {remain_uop_25})")
print(f"rows: ratios {len(rows)}, segments {len(seg)}")
