"""Data agent script (KO, run 2026-10-13): builds financials.csv, tie_out.csv and ../inputs.yaml.

Reads financials_raw.csv and market_inputs.json (written by `python -m desk.data_sources`), plus
figures typed in from SEC filings. Every typed-in number is quoted next to its source.
Run from the repo root:  python runs/KO/2026-10-13/data/build_inputs.py
"""
import json
from datetime import date
from pathlib import Path

import pandas as pd
import yaml

from desk import fundamentals

RUN = Path(__file__).resolve().parents[1]
DATA = RUN / "data"
brief = yaml.safe_load(Path("briefs/KO.yaml").read_text())
raw = pd.read_csv(DATA / "financials_raw.csv")
mkt = json.loads((DATA / "market_inputs.json").read_text())

EDGAR = "https://www.sec.gov/Archives/edgar/data/21344"
K25 = f"KO FY25 10-K (accession 0001628280-26-010047, filed 2026-02-20, {EDGAR}/000162828026010047/ko-20251231.htm)"
Q425 = f"KO Q4 2025 results 8-K ex.99.1 (accession 0001628280-26-006642, {EDGAR}/000162828026006642/a2025q4earningsreleaseex-9.htm)"
Q226 = f"KO Q2 2026 results 8-K ex.99.1 (accession 0001628280-26-049922, {EDGAR}/000162828026049922/a2026q2earningsreleaseex-9.htm)"
QQ226 = f"KO Q2 2026 10-Q (accession 0001628280-26-050503, {EDGAR}/000162828026050503/ko-20260703.htm)"
QQ126 = f"KO Q1 2026 10-Q (accession 0001628280-26-028802, {EDGAR}/000162828026028802/ko-20260403.htm)"
Q4 = {2021: "0000021344-22-000004", 2022: "0000021344-23-000005", 2023: "0000021344-24-000004",
      2024: "0000021344-25-000005", 2025: "0001628280-26-006642"}
RUN_DATE = date(2026, 10, 13)
BALANCE_DATE = date(2025, 12, 31)


def v(item, fy):
    """One XBRL value (USD m, or millions of shares) from financials_raw.csv."""
    return float(raw[(raw["item"] == item) & (raw["fiscal_year"] == fy)]["value_musd"].iloc[0])


def q4src(fy):
    return f"KO Q4 {fy} results 8-K ex.99.1 (accession {Q4[fy]}), reconciliation of GAAP to non-GAAP, full year"


# ---- financials.csv: XBRL line items (reported, US GAAP) plus figures quoted from filing text
fin = raw[["item", "fiscal_year", "value_musd"]].copy()
fin["source"] = raw["source"] + " | XBRL tag " + raw["tag"]
fin["value_musd"] = fin["value_musd"].round(1)
text_items = [
    # comparable (non-GAAP) revenue and operating income: Q4 results 8-K reconciliations
    ("comparable_net_revenues", 2021, 38658, q4src(2021)), ("comparable_operating_income", 2021, 11109, q4src(2021)),
    ("comparable_net_revenues", 2022, 43046, q4src(2022)), ("comparable_operating_income", 2022, 12345, q4src(2022)),
    ("comparable_net_revenues", 2023, 45784, q4src(2023)), ("comparable_operating_income", 2023, 13336, q4src(2023)),
    ("comparable_net_revenues", 2024, 46897, q4src(2024)), ("comparable_operating_income", 2024, 14085, q4src(2024)),
    ("comparable_net_revenues", 2025, 48062, q4src(2025)), ("comparable_operating_income", 2025, 15013, q4src(2025)),
    ("comparable_eps_usd", 2025, 3.00, Q425 + ": 'Comparable EPS (Non-GAAP) Grew 4% to $3.00'"),
    ("free_cash_flow_reported", 2025, 5300, Q425 + ": 'Free Cash Flow (Non-GAAP) was $5.3 Billion' (after the $6.1bn fairlife payment)"),
    # working capital pieces not in the desk tag map
    ("prepaid_expenses_and_other_current_assets", 2025, 2433, K25 + " balance sheet | XBRL us-gaap:PrepaidExpenseAndOtherAssetsCurrent"),
    ("prepaid_expenses_and_other_current_assets", 2024, 2998, K25 + " balance sheet | XBRL us-gaap:PrepaidExpenseAndOtherAssetsCurrent"),
    ("fairlife_contingent_consideration_in_payables", 2024, 6126, K25 + " Note 8 'Accounts payable and accrued expenses': contingent consideration liability (fairlife) 6,126 at 31 Dec 2024"),
    ("fairlife_contingent_consideration_in_payables", 2025, 0, K25 + " Note 8: contingent consideration liability nil at 31 Dec 2025 (paid 2025)"),
    # segment: Bottling Investments (contains CCBA, but also other consolidated bottlers, e.g. India)
    ("bottling_investments_revenue_total", 2025, 5735, K25 + " Note 'Operating segments' table: Bottling Investments total net operating revenues"),
    ("bottling_investments_comparable_operating_income", 2025, 426, Q425 + " segment reconciliation: Bottling Investments comparable operating income"),
    ("bottling_investments_operating_income_reported", 2025, 426, K25 + " segment table: Bottling Investments operating income (7.4% margin, MD&A)"),
    # CCBA (bottling operations in Africa) held for sale at 31 Dec 2025
    ("ccba_assets_held_for_sale", 2025, 5342, K25 + " Note 2 held-for-sale table (after 1,265 allowance)"),
    ("ccba_liabilities_held_for_sale", 2025, 2570, K25 + " Note 2 held-for-sale table"),
    ("ccba_debt_in_liabilities_held_for_sale", 2025, 187 + 398 + 850, K25 + " Note 2: loans and notes 187 + current LTD 398 + LTD 850"),
    ("ccba_cash_in_assets_held_for_sale", 2025, 178, K25 + " Note 2: cash, cash equivalents and short-term investments 178"),
    ("ccba_impairment_charge", 2025, 1274, K25 + " Note 2 | XBRL us-gaap:DisposalGroupNotDiscontinuedOperationLossGainOnWriteDown [BottlingOperationsInAfricaMember]"),
    # listed equity-method stakes
    ("listed_equity_investees_fair_value", 2025, 34286, K25 + " Note 6 equity method investments: fair value of publicly traded investees (p.85)"),
    ("listed_equity_investees_carrying_value", 2025, 13999, K25 + " Note 6 (p.85)"),
    # pension (Note 14)
    ("pension_plans_net_asset", 2025, 295, K25 + " Note 14 'Net asset (liability) recognized', pension plans"),
    ("other_postretirement_net_liability", 2025, -112, K25 + " Note 14 'Net asset (liability) recognized', other postretirement plans"),
    ("pension_and_opeb_gross_accrued_liability", 2025, 863, K25 + " MD&A contractual obligations: 'total accrued liability for pension and other postretirement benefit plans ... $863 million'"),
    # debt detail
    ("long_term_debt_total_incl_current", 2025, 43941, K25 + " Note 11 long-term debt table (no finance-lease line disclosed)"),
    ("long_term_debt_fair_value", 2025, 39385, K25 + " Note 11 footnote 4"),
    ("long_term_debt_weighted_avg_rate", 2025, 0.033, K25 + " Note 11: weighted-average effective rate 3.3%"),
]
fin = pd.concat([fin, pd.DataFrame(text_items, columns=fin.columns)], ignore_index=True)
fin.sort_values(["item", "fiscal_year"]).to_csv(DATA / "financials.csv", index=False)

# ---- tie-out vs the brief's published FY25 figures
pub = brief["checks"]["published_fy25"]
tol = brief["checks"]["data_tie_out_tolerance"]
fcf = v("operating_cash_flow", 2025) - v("capex", 2025)  # free cash flow = operating cash flow - capex (KO definition)
ours = {"net_sales_musd": v("net_sales", 2025),
        "operating_profit_reported_musd": v("operating_profit_reported", 2025),
        "comparable_operating_margin": round(fundamentals.margin(15013, 48062), 4),  # comparable OI / comparable revenue
        "free_cash_flow_musd": fcf,
        "eps_comparable_usd": 3.00}
tie = pd.DataFrame([{"item": k, "brief": pub[k], "data_agent": ours[k],
                     "diff_pct": round(ours[k] / pub[k] - 1, 5)} for k in pub])
tie["flag"] = tie["diff_pct"].abs() > tol
tie.to_csv(DATA / "tie_out.csv", index=False)

# ---- inputs.yaml
years = range(2021, 2026)
sales5 = sum(v("net_sales", y) for y in years)
da_pct = sum(v("depreciation_amortisation", y) for y in years) / sales5   # D&A intensity, 5-year pooled average
capex_pct = sum(v("capex", y) for y in years) / sales5                     # capex intensity, 5-year pooled average

# net working capital (operating) = inventories + trade receivables + prepaid - payables & accrued
nwc25 = v("inventories", 2025) + v("trade_and_other_receivables", 2025) + 2433 - v("trade_and_other_payables", 2025)
nwc24_ex_fairlife = (v("inventories", 2024) + v("trade_and_other_receivables", 2024) + 2998
                     - (v("trade_and_other_payables", 2024) - 6126))
nwc_pct = nwc25 / v("net_sales", 2025)

debt25 = v("short_term_borrowings", 2025) + v("long_term_debt_current", 2025) + v("long_term_debt_noncurrent", 2025)
debt24 = v("short_term_borrowings", 2024) + v("long_term_debt_current", 2024) + v("long_term_debt_noncurrent", 2024)
cash_like = v("cash", 2025) + v("short_term_investments", 2025) + v("marketable_securities", 2025)
net_debt = debt25 - cash_like                                    # net debt = gross borrowings - cash & liquid investments
kd_hist = v("interest_expense", 2025) / ((debt25 + debt24) / 2)  # historic cost of debt = interest / average gross debt

shares = v("shares_issued_m", 2025) - v("treasury_shares_m", 2025)  # shares outstanding = issued - treasury
px = mkt["share_price_usd"]
mcap = shares * px["value"]
debt_weight = net_debt / (net_debt + mcap)                        # market-value weight of (net) debt in capital

days = (RUN_DATE - BALANCE_DATE).days
stub = days / 365                                                 # fraction of a year from balance sheet to run date

dps_ex = 3 * 0.53                                                 # three $0.53 quarterly dividends ex in 2026 (see source)
divs = dps_ex * shares

associates = 34286 + (20235 - 13999)  # listed stakes at fair value + unlisted equity-method investments at book

inputs = {
    "base_sales": {"value": None, "status": "MISSING - STOP",
                   "source": "MISSING. Brief requires FY25 net operating revenues EXCLUDING CCBA (bottling operations in Africa). "
                             "No KO filing discloses CCBA's revenue: checked FY25 10-K (Note 2 held-for-sale table gives only assets/"
                             "liabilities; segment note gives Bottling Investments 5,735 total, which also contains India and other "
                             "consolidated bottlers; XBRL has no revenue fact for ko:BottlingOperationsInAfricaMember), Q3 2025 10-Q "
                             "(0001628280-25-046054), Q3 2025 release (0001628280-25-045577), Q4 2025 release, Q1 and Q2 2026 10-Qs, "
                             "Q2 2026 release. KO filed no 8-K for the CCBA deal. Buyer (Coca-Cola HBC) announcements are not on EDGAR "
                             "and the CCHBC/LSE sites are blocked from this environment. Reported FY25 revenue incl. CCBA = 47,941 "
                             "(not a substitute). See notes.md."},
    "base_margin": {"value": round(fundamentals.margin(15013, 48062), 5),
                    "source": f"{Q425} reconciliation: comparable operating income 15,013 / comparable net operating revenues 48,062 "
                              "(FY25, INCLUDES CCBA). FLAG: CCBA operating income is not disclosed, so no ex-CCBA margin can be "
                              "computed; ex-CCBA margin would be HIGHER (Bottling Investments segment comparable margin 7.4% = 426/5,735)."},
    "tax_rate": {"value": 0.237,
                 "source": f"PM decision (IRS case assumed lost): 19.9% underlying effective tax rate, FY26 guidance ({Q226}, outlook table) "
                           f"+ 3.8 points if the Tax Court methodology keeps applying ({QQ226} Note 9 Commitments and Contingencies "
                           "(brief says note 12): 'would increase the Company's effective tax rate by approximately 3.8%')"},
    "da_pct_sales": {"value": round(da_pct, 5),
                     "source": "FY21-FY25 depreciation & amortisation / net operating revenues, pooled over 5 years "
                               "(XBRL us-gaap:DepreciationDepletionAndAmortization and us-gaap:Revenues, 10-Ks FY22-FY25; financials_raw.csv)"},
    "capex_pct_sales": {"value": round(capex_pct, 5),
                        "source": "FY21-FY25 purchases of property, plant and equipment / net operating revenues, pooled over 5 years "
                                  "(XBRL us-gaap:PaymentsToAcquirePropertyPlantAndEquipment; financials_raw.csv). FY26 guidance capex c.$2.2bn (Q4 2025 8-K)."},
    "nwc_pct_sales": {"value": round(nwc_pct, 5),
                      "source": f"FY25 (inventories 4,425 + trade receivables 3,038 + prepaid & other current 2,433 - accounts payable & accrued "
                                f"14,813 = {nwc25:,.0f}) / net operating revenues 47,941; {K25} balance sheet. Negative = suppliers fund KO. "
                                f"FY24 cross-check ex-fairlife liability 6,126: {nwc24_ex_fairlife:,.0f} = {nwc24_ex_fairlife / v('net_sales', 2024):.2%} of sales."},
    "risk_free": {"value": mkt["risk_free"]["value"], "source": f"{mkt['risk_free']['source']}, {mkt['risk_free']['date']}"},
    "pre_tax_cost_of_debt": {"value": round(kd_hist, 5),
                             "source": f"Historic, reference only: FY25 interest expense 1,654 / average gross debt "
                                       f"(({debt24:,.0f} at 31 Dec 2024 + {debt25:,.0f} at 31 Dec 2025)/2); {K25}. Engine uses risk-free + "
                                       "credit_spread 0.69% (brief)."},
    "debt_weight": {"value": round(debt_weight, 5),
                    "source": f"net debt {net_debt:,.0f} / (net debt + market cap {mcap:,.0f} = {shares:,.0f}m shares x ${px['value']:.2f} "
                              f"Yahoo KO close {px['date']})"},
    "net_debt": {"value": round(net_debt, 1),
                 "source": f"{K25} balance sheet at 31 Dec 2025: loans and notes payable 1,551 + current maturities of LTD 1,822 + LTD 42,119 "
                           "- cash 10,270 - short-term investments 3,602 - marketable securities 1,934. No finance-lease liability is "
                           "disclosed separately (none inside or outside). EXCLUDES CCBA debt 1,435 and cash 178 (in held-for-sale)."},
    "lease_liabilities": {"value": 1722.0,
                          "source": f"{K25} Note 10: total operating lease liabilities 1,722 (current 321 in payables, noncurrent 1,401 in other "
                                    "noncurrent liabilities); NOT in net debt, so deducted separately."},
    "minority_interests": {"value": v("non_controlling_interests", 2025),
                           "source": f"{K25} balance sheet: equity attributable to noncontrolling interests 2,106 (book; includes the 40% "
                                     "India bottling NCI sold July 2025 and the outside shareholders of CCBA - see FLAG)"},
    "pension_deficit": {"value": 0.0,
                        "source": f"{K25} Note 14: pension plans net ASSET 295, other postretirement net liability 112 = net surplus 183; "
                                  "brief rule 0 if in surplus. Gross accrued liability of deficit plans 863 (MD&A) - see notes."},
    "associates": {"value": float(associates),
                   "source": f"{K25} Note 6: listed equity-method stakes at FAIR VALUE 34,286 at 31 Dec 2025 (Monster 15,659, CCEP 7,163, "
                             "Coca-Cola FEMSA 5,543, Coca-Cola HBC 4,051, CCBJH 822, CCI 770, Andina 278) + unlisted equity-method "
                             "investments at book (total 20,235 - listed book 13,999 = 6,236). FLAG: 31 Dec 2025 values, not run date "
                             "(10-K gives no share counts); run-date roll-forward cross-check in notes.md."},
    "disposal_proceeds": {"value": 0.0,
                          "source": "FLAG: CCBA sale proceeds are NOT disclosed in any KO filing (10-K Note 2, Q2 2026 10-Q Note 2); "
                                    "sale not closed at 3 Jul 2026 (Q2 2026 10-Q). 0 entered, but this UNDERSTATES value if base_sales "
                                    "excludes CCBA. Held-for-sale net assets at 31 Dec 2025 = 5,342 - 2,570 = 2,772 (carrying value at "
                                    "fair value less costs to sell, 100% basis incl. outside shareholders)."},
    "restructuring_cash": {"value": 0.0,
                           "source": f"{K25} Note 19: productivity and reinvestment program (2012-2017) 'substantially completed' at 31 Dec 2025 "
                                     "(FY25 charge 97); no new programme announced in the Q1/Q2 2026 10-Qs."},
    "contingent_liabilities": {"value": 14900.0,
                               "source": f"PM decision (assume KO loses the IRS case): 14,000 potential tax and interest 2010-2025 at "
                                         f"31 Dec 2025 ({K25}, XBRL ko:IncrementalTaxAndInterestLiability) + 900 for H1 2026 "
                                         f"({QQ226} Note 9). $6.0bn deposit already paid (2007-09) not refunded in base case."},
    "shares_outstanding_m": {"value": shares,
                             "source": f"{K25} XBRL: 7,040m issued (us-gaap:CommonStockSharesIssued) - 2,738m treasury "
                                       "(us-gaap:TreasuryStockCommonShares) at 31 Dec 2025. Check: Q2 2026 10-Q cover 4,302,549,243 at 27 Jul 2026."},
    "share_price_usd": {"value": px["value"], "source": f"{px['source']}, {px['date']}"},
    "stub_years": {"value": round(stub, 5), "source": f"{days} days from 31 Dec 2025 balance sheet to run date {RUN_DATE} / 365"},
    "dividends_ex_before_valuation_musd": {
        "value": round(divs, 1),
        "source": f"3 quarterly dividends of $0.53 = $1.59/share went ex between 1 Jan and 13 Oct 2026 x {shares:,.0f}m shares. "
                  f"Q1: declared Feb 2026 ({K25} 'increased our regular quarterly dividend to $0.53'), booked Q1 ({QQ126} equity "
                  f"statement, $2,280m); Q2: record 15 Jun 2026 ({QQ126}); Q3: record 15 Sep 2026, payable 1 Oct 2026 ({QQ226}). "
                  "Ex-dates 13 Mar, 15 Jun, 15 Sep 2026 (Yahoo KO dividend events, non-filing cross-check). Q4 dividend not yet ex."},
}
(RUN / "inputs.yaml").write_text(yaml.safe_dump(inputs, sort_keys=False, allow_unicode=True, width=1000))
print(tie.to_string())
print(json.dumps({k: d["value"] for k, d in inputs.items()}, indent=1))
print({"nwc24_ex_fairlife": nwc24_ex_fairlife, "nwc25": nwc25, "debt25": debt25, "debt24": debt24, "mcap": mcap})
