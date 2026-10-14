"""Data agent script (RELX, run 2026-10-14): financials.csv, tie_out.csv, market_data.json and (with --write-inputs) ../inputs.yaml.

Inputs: financials_raw.csv, market_inputs.json and prices.csv written by
`python -m desk.data_sources briefs/RELX.yaml runs/RELX/2026-10-14/data`, plus figures read from the primary filings
(SEC EDGAR, RELX PLC CIK 929869), each cited below with document and page. All money amounts GBP m unless the name says
otherwise; the share price is in pence (GBp). RELX reports in pounds, so no exchange rate is needed.
Run from the repo root:  PYTHONPATH=. python runs/RELX/2026-10-14/data/build_inputs.py [--write-inputs]
"""
import datetime as dt
import json
import sys
from pathlib import Path

import pandas as pd
import yaml

DATA = Path(__file__).resolve().parent
RUN = DATA.parent
REPO = RUN.parents[2]
BRIEF = yaml.safe_load((REPO / "briefs" / "RELX.yaml").read_text())
BS_DATE = dt.date(2025, 12, 31)      # balance sheet date (valuation_basis: balance_sheet_date)
PRICE_DATE = dt.date(2026, 10, 13)   # 13 Oct 2026 CLOSE (not an intraday 14 Oct price: Unilever-run bug)

# ---------------------------------------------------------------- document citations (SEC EDGAR, CIK 929869)
E = "https://www.sec.gov/Archives/edgar/data/929869"
AR25 = f"RELX Annual Report 2025 (20-F ex 15.2, accession 0001104659-26-017277, filed 19 Feb 2026, {E}/000110465926017277/relx-20251231xex15d2.htm)"
F20 = f"RELX FY25 Form 20-F (accession 0001104659-26-017277, {E}/000110465926017277/relx-20251231x20f.htm)"
FY25R = f"RELX FY2025 results 6-K ex 99.1 (accession 0000929869-26-000008, 12 Feb 2026, {E}/000092986926000008/relx-20260201xex99d1.htm)"
H126 = f"RELX H1 2026 interim results 6-K ex 99.1 (accession 0000929869-26-000054, 23 Jul 2026, {E}/000092986926000054/relx-20260723xex99d1.htm)"
BB23JUL = f"RELX buyback announcement 23 Jul 2026, 6-K ex 99.1 (accession 0000929869-26-000056, {E}/000092986926000056/relx-20260723xex99d1.htm)"
BB7SEP = f"RELX buyback announcement 7 Sep 2026, 6-K ex 99.1 (accession 0000929869-26-000068, {E}/000092986926000068/relx-20260803xex99d1.htm)"
TX = f"RELX 'Transactions in own shares' weekly notices, 6-K of 1 Oct 2026 ex 99.3, 99.4, 99.6 (accession 0000929869-26-000071, {E}/000092986926000071/)"
TX6 = f"RELX 'Transactions in own shares' 28 Sep 2026, 6-K ex 99.6 (accession 0000929869-26-000071, {E}/000092986926000071/relx-ex99d6.htm)"
DIVINT = f"RELX 6-K 27 Aug 2026, interim dividend euro equivalent (accession 0000929869-26-000064)"
XBRL25 = f"{F20} XBRL instance relx-20251231x20f_htm.xml"

# ---------------------------------------------------------------- facts read from the filings (GBP m), re-checked on this run
F = {
    # FY25 results release
    "net_debt25": 7201, "leases_in_net_debt25": 97, "bank_bond25": 7170, "hedge_deriv25": 60, "nonhedge_swaps25": 5,
    "cash25": 131, "eff_rate_bank_bond25": 0.039,
    "cur_payables_results25": 4260, "nc_other_payables_results25": 9,
    # Annual Report 2025
    "inventories_prepub25": 311, "receivables25": 2468, "payables25": 4268, "nc_other_payables_ar25": 1,
    "deferred_income25": 2390, "nci25": 24, "net_pension_assets25": 197, "net_pension_obligations25": 154,
    "jv_book25": 164, "vc_other_inv25": 131, "jv_adj_op25": 57, "finance_costs25": 298, "finance_costs24": 304,
    "gross_debt24": 6544, "gross_debt25": 7267, "ebt_shares25_m": 4.891047,
    # H1 2026
    "div_final_cash": 851, "div_interim_cost": 366, "buyback_h1": 1750, "net_debt_h126": 8733, "leases_h126": 119,
    # buyback announcements and weekly notices
    "buyback_1_21jul": 100, "buyback_23jul_4sep": 150, "buyback_7_25sep_vwap": 56.2, "shares_7_25sep": 2225133,
    "shares_ex_treasury_25sep": 1743754727,
}
ADJ = {  # AR25 p.186 five-year summary, adjusted (non-GAAP) figures, GBP m
    "adjusted_ebitda": [2697, 3174, 3544, 3724, 3846],
    "adjusted_operating_profit": [2210, 2683, 3030, 3199, 3342],
    "adjusted_net_interest_expense": [133, 194, 314, 296, 283],
    "adjusted_profit_before_tax": [2077, 2489, 2716, 2903, 3059],
    "adjusted_tax_charge": [384, 530, 553, 652, 688],
    "adjusted_net_profit_to_shareholders": [1689, 1961, 2156, 2241, 2358],
    "adjusted_cash_flow": [2230, 2709, 2962, 3101, 3301],
}
TEXT_ROWS = [  # (item, fiscal_year, GBP m, source) for items RELX does not tag with a standard IFRS label
    *[("capitalised_development_spend", y, v, f"{AR25} p.140, consolidated cash flow statement, 'Expenditure on internally developed intangible assets' (XBRL: no ifrs-full label)")
      for y, v in ((2023, 447), (2024, 464), (2025, 504))],
    *[("capex_total_relx_definition", y, v, f"{XBRL25} relx:CapitalExpendituresAdditions (PP&E + internally developed intangibles); FY25 also {FY25R} p.11")
      for y, v in ((2023, 477), (2024, 484), (2025, 525))],
    *[("pre_publication_costs_capitalised", y, v, f"{XBRL25} relx:PrePublicationCostsCapitalized; {FY25R} p.11 'excludes pre-publication costs of GBP 102m (2024: GBP 92m)'")
      for y, v in ((2024, 92), (2025, 102))],
    *[("pre_publication_amortisation", y, v, f"{XBRL25} relx:PrePublicationAmortisation")
      for y, v in ((2023, 76), (2024, 77), (2025, 89))],
    ("amortisation_internally_developed_intangibles", 2025, 352, f"{XBRL25} relx:AmortisationOfInternallyDevelopedIntangibleAssets"),
    ("net_debt_relx_definition", 2024, 6563, f"{FY25R} p.13 (includes leases 103)"),
    ("net_debt_relx_definition", 2025, 7201, f"{FY25R} p.13: bank and bond borrowings 7,170 + leases 97 + hedging derivative net liabilities 60 + non-hedge swap liabilities 5 - cash 131"),
    ("lease_liabilities_in_net_debt", 2025, 97, f"{FY25R} p.13"),
    ("net_debt_ex_leases", 2025, 7104, f"computed: 7,201 - 97 ({FY25R} p.13)"),
    ("finance_costs", 2024, 304, f"{AR25} p.156, note 7"),
    ("finance_costs", 2025, 298, f"{AR25} p.156, note 7"),
    ("deferred_income_in_payables", 2025, 2390, f"{AR25} p.176, note 20"),
    ("venture_capital_and_other_investments", 2025, 131, f"{AR25} p.167, note 15; p.141 balance sheet 'Other investments'"),
    ("jv_share_of_adjusted_operating_profit", 2025, 57, f"{AR25} p.206, APM leverage ratio table"),
    ("employee_benefit_trust_shares_m", 2025, 4.891047, f"{AR25} p.179, share capital note: 4,891,047 shares held by the EBT (inside treasury in the accounts, but NOT in the parent's treasury count in voting-rights notices)"),
    *[(k, 2021 + i, v, f"{AR25} p.186, five year summary (adjusted figures, non-GAAP)") for k, vs in ADJ.items() for i, v in enumerate(vs)],
]
NOT_NEEDED = {  # desk IFRS labels RELX does not tag; why the valuation does not need them
    "restructuring": "RELX has no separately reported restructuring line or programme; the forecast base is adjusted operating profit and the brief sets restructuring_cash_mgbp 0",
    "capex_intangibles": "the IFRS label is not used; RELX's capitalised development spend is read from the AR25 p.140 cash flow text (row capitalised_development_spend). The valuation uses the brief's capex_pct_sales (H1 2026)",
    "other_current_financial_assets": "not part of RELX's net debt definition (FY25R p.13); not needed",
    "assets_held_for_sale / liabilities_held_for_sale": "none at 31 Dec 2025 (AR25 p.141 balance sheet has no such line; only FY23 had 44/14); confirms disposal_proceeds 0",
}


def financials() -> pd.DataFrame:
    raw = pd.read_csv(DATA / "financials_raw.csv")
    raw["source"] = raw["source"] + " XBRL " + raw["tag"]
    rows = raw[["item", "fiscal_year", "value_mgbp", "source"]]
    text = pd.DataFrame(TEXT_ROWS, columns=["item", "fiscal_year", "value_mgbp", "source"])
    out = pd.concat([rows, text]).sort_values(["item", "fiscal_year"]).reset_index(drop=True)
    return out[out["fiscal_year"].between(2021, 2025)]


def tie_out(fin: pd.DataFrame) -> pd.DataFrame:
    tol = BRIEF["checks"]["data_tie_out_tolerance"]
    pub = BRIEF["checks"]["published_fy25"]
    get = lambda i: float(fin[(fin["item"] == i) & (fin["fiscal_year"] == 2025)]["value_mgbp"].iloc[0])
    mine = {"net_sales_mgbp": get("net_sales"), "adjusted_operating_profit_mgbp": get("adjusted_operating_profit"),
            # adjusted operating margin = adjusted operating profit / revenue
            "adjusted_operating_margin": round(get("adjusted_operating_profit") / get("net_sales"), 5),
            # RELX net debt = gross borrowings incl. leases (XBRL ifrs-full:Borrowings) + derivative liabilities - cash
            "net_debt_mgbp": get("gross_borrowings") + F["hedge_deriv25"] + F["nonhedge_swaps25"] - get("cash")}
    rows = []
    for k, v in mine.items():
        diff = v / pub[k] - 1
        rows.append({"item": k, "brief": pub[k], "data_agent": v, "diff_pct": round(diff, 5), "flag": abs(diff) > tol})
    return pd.DataFrame(rows)


def build_inputs(market: dict) -> dict:
    d = BRIEF["dcf"]
    px = market["share_price_gbp_pence"]
    assert px["date"] == str(PRICE_DATE), f"share price is dated {px['date']}, not the 13 Oct 2026 close"
    shares_m = F["shares_ex_treasury_25sep"] / 1e6
    mcap = px["value"] / 100 * shares_m                       # market capitalisation = price (GBP) x shares
    net_debt = F["net_debt25"] - F["leases_in_net_debt25"]    # PM bridge: net debt without leases
    nwc = F["inventories_prepub25"] + F["receivables25"] - F["payables25"]   # operating working capital
    avg_debt = (F["gross_debt24"] + F["gross_debt25"]) / 2
    divs = F["div_final_cash"] + F["div_interim_cost"]
    buybacks = F["buyback_h1"] + F["buyback_1_21jul"] + F["buyback_23jul_4sep"] + F["buyback_7_25sep_vwap"]
    stub_days = (PRICE_DATE - BS_DATE).days
    brief_note = "PM decision 14 Oct 2026, briefs/RELX.yaml"
    return {
        "base_sales": {"value": float(BRIEF["base_year"]["net_sales_mgbp"]), "source":
            f"GBP m, FY25 revenue 9,590 ({FY25R} p.26; {AR25} p.186; XBRL ifrs-full:RevenueFromContractsWithCustomers). The DCF base "
            "is FY25 revenue INCLUDING print (399); the margin decision (35.0%) is on H1 2026 adjusted margin EX print, applied to this base "
            "(PM decision, brief dcf.base_margin comment)."},
        "base_margin": {"value": d["base_margin"], "source":
            f"{brief_note} dcf.base_margin: H1 2026 adjusted operating margin without print (1,727 - 78) / (4,871 - 157) = 35.0% ({H126} p.1-9). "
            "Data agent check: FY25 adjusted margin 3,342 / 9,590 = 34.85% incl. print (AR25 p.186)."},
        "tax_rate": {"value": d["tax_rate"], "source":
            f"{brief_note} dcf.tax_rate: H1 2026 effective tax rate 22.8%, 'best estimate of the annual tax rate expected for the full financial year' ({H126} p.28, note 7)."},
        "da_pct_sales": {"value": d["da_pct_sales"], "source":
            f"{brief_note} dcf.da_pct_sales: H1 2026 (internally developed 193 + PP&E 12 + pre-publication 42) / revenue 4,871 = 5.07% "
            f"({H126} p.10 and p.25); lease depreciation (18) excluded because leases are not in net debt."},
        "capex_pct_sales": {"value": d["capex_pct_sales"], "source":
            f"{brief_note} dcf.capex_pct_sales: H1 2026 (capex 292 incl. capitalised development 280 + pre-publication spend 54) / 4,871 = 7.10% "
            f"({H126} p.10, quote re-checked: 'Capital expenditure was GBP 292m ... excludes pre-publication costs of GBP 54m')."},
        "nwc_pct_sales": {"value": round(nwc / BRIEF["base_year"]["net_sales_mgbp"], 5), "source":
            f"FY25 (inventories and pre-publication costs {F['inventories_prepub25']} + trade and other receivables {F['receivables25']} "
            f"- trade and other payables {F['payables25']}) / revenue 9,590 = {nwc} / 9,590 = {nwc / 9590:.4%}. {AR25} p.141 balance sheet, "
            f"notes 18-20 (p.176; payables include deferred income {F['deferred_income25']}); XBRL relx:InventoriesAndPrepublicationCosts, "
            f"ifrs-full:TradeAndOtherCurrentReceivables, TradeAndOtherCurrentPayables. FLAG: the results release balance sheet shows current payables "
            f"{F['cur_payables_results25']} with {F['nc_other_payables_results25']} non-current ({FY25R} p.22) against {F['payables25']} + "
            f"{F['nc_other_payables_ar25']} in the audited Annual Report: GBP 8m reclassified between current and non-current. "
            f"The audited 4,268 is used; with 4,260 the ratio would be {(nwc + 8) / 9590:.4%}."},
        "risk_free": {"value": 0.0545, "source":
            f"{brief_note} dcf.wacc.risk_free comment: UK 10-year gilt at the 13 Oct 2026 close, 5.45% (Investing.com historical data 5.4542%; "
            "Trading Economics 5.44%). FLAG: aggregator figures; the Bank of England and DMO sites are blocked, and Trading Economics did not "
            "resolve from the Data agent's environment, so the Data agent could not re-check 5.45% itself. Reference only: FRED IRLTLT01GBM156N "
            f"(OECD monthly average) Aug 2026 = {market['risk_free']['value']:.4%} (stale); FRED DGS10 (US 10-year) 13 Oct 2026 = 5.21%."},
        "pre_tax_cost_of_debt": {"value": F["eff_rate_bank_bond25"], "source":
            f"Historic, reference only: RELX-stated effective interest rate on gross bank and bond borrowings 3.9% in 2025 ({FY25R} p.13; "
            f"'average interest rate on gross debt was 3.9%', p.2). Cross-check: finance costs {F['finance_costs25']} ({AR25} p.156, note 7) / "
            f"average gross debt incl. leases {avg_debt:,.1f} (31 Dec 2024 {F['gross_debt24']:,}, 31 Dec 2025 {F['gross_debt25']:,}; FY25R p.13) = "
            f"{F['finance_costs25'] / avg_debt:.2%} (finance costs include derivative and pension items). The engine uses risk-free 5.45% + "
            f"credit_spread 0.70% (brief; FRED BAMLC0A3CA 0.70 on 13 Oct 2026) = 6.15%."},
        "debt_weight": {"value": round(net_debt / (net_debt + mcap), 5), "source":
            f"Market values: net debt ex leases {net_debt:,} (31 Dec 2025, FY25R p.13) / (net debt + market cap GBP {mcap:,.1f}m = "
            f"{shares_m:,.6f}m shares (ex treasury, 25 Sep 2026, {TX6}) x {px['value']:.0f}p (Yahoo REL.L close {px['date']})). "
            f"Cross-check with 30 Jun 2026 net debt ex leases {F['net_debt_h126'] - F['leases_h126']:,} ({H126} p.11): "
            f"{(F['net_debt_h126'] - F['leases_h126']) / (F['net_debt_h126'] - F['leases_h126'] + mcap):.2%}."},
        "net_debt": {"value": float(net_debt), "source":
            f"RELX net debt 7,201 at 31 Dec 2025 LESS the 97 of lease liabilities inside it = {net_debt:,} ({FY25R} p.13: 'Gross debt of GBP 7,267m "
            "... bank and bond borrowings of GBP 7,170m ... and lease liabilities of GBP 97m ... In aggregate, these give the net debt figure of "
            "GBP 7,201m'). Includes hedging derivative net liabilities 60 and non-hedge swap liabilities 5, net of cash 131. PM bridge decision: "
            "leases excluded because lease depreciation is not added back in D&A. Does NOT include the 2026 buybacks (deducted separately)."},
        "lease_liabilities": {"value": 0.0, "source":
            f"PM bridge (briefs/RELX.yaml lease_liabilities_mgbp 0): the GBP 97m of leases ({FY25R} p.13) is taken OUT of net debt and NOT added "
            "here, because lease costs already reduce the forecast cash flow (lease depreciation is left out of D&A)."},
        "minority_interests": {"value": float(F["nci25"]), "source":
            f"Book value of non-controlling interests at 31 Dec 2025 ({FY25R} p.22; {AR25} p.141; XBRL ifrs-full:NoncontrollingInterests 24). Brief minorities_method: book."},
        "pension_deficit": {"value": 0.0, "source":
            f"Brief rule (0 when in surplus): net SURPLUS of 43 at 31 Dec 2025 = net pension assets {F['net_pension_assets25']} - net pension obligations "
            f"{F['net_pension_obligations25']} ({AR25} p.141; XBRL ifrs-full:LiabilityAssetOfDefinedBenefitPlans = -43; FY25R p.29-30)."},
        "associates": {"value": float(F["vc_other_inv25"]), "source":
            f"Venture capital and other investments at book = fair value, 131 at 31 Dec 2025 ({AR25} p.167, note 15; p.141 'Other investments'). "
            f"Joint ventures and associates (book {F['jv_book25']}) are NOT added: their profit is inside adjusted operating profit (JV share of adjusted "
            f"operating profit {F['jv_adj_op25']}, {AR25} p.206; reconciliation reclassifies JV tax +14 and finance income -1 into adjusted OP, {FY25R} p.26)."},
        "disposal_proceeds": {"value": 0.0, "source":
            f"Brief: no pending disposal. No assets held for sale at 31 Dec 2025 ({AR25} p.141 balance sheet; no XBRL held-for-sale facts for FY25)."},
        "restructuring_cash": {"value": 0.0, "source": "Brief: no announced one-off restructuring programme (none in FY25R or H126)."},
        "shares_outstanding_m": {"value": shares_m, "source":
            f"{TX6}: 'RELX PLC holds 85,329,583 ordinary shares in treasury, and has 1,743,754,727 ordinary shares in issue (excluding treasury "
            "shares)' after buybacks to 25 Sep 2026. Ordinary shares; 1 ADR = 1 share (not used). Includes shares held by the Employee Benefit "
            f"Trust (4.89m at 31 Dec 2025, {AR25} p.179): FLAG in notes.md. Purchases from 28 Sep to 13 Oct 2026 not yet filed."},
        "share_price_gbp_pence": {"value": px["value"], "source":
            f"Yahoo Finance REL.L close {px['date']} (pence, GBp), the 13 Oct 2026 CLOSE (desk.data_sources last_close, unadjusted). Not an intraday 14 Oct price."},
        "stub_years": {"value": round(stub_days / 365, 5), "source":
            f"{stub_days} days from the 31 Dec 2025 balance sheet to the 13 Oct 2026 price date / 365."},
        "dividends_ex_before_valuation_mgbp": {"value": float(divs), "source":
            f"Dividends that went ex between 31 Dec 2025 and 13 Oct 2026: 2025 final 48.0p (ex 7 May 2026, {FY25R} p.27), cash GBP 851m "
            f"({H126} p.20 cash flow and p.25 note 4: 'amounted to GBP 851m'); 2026 interim 20.9p (ex 6 Aug 2026, paid 10 Sep 2026), "
            f"'expected total cost of funding this dividend is GBP 366m' ({H126} p.25 note 4; payment confirmed {DIVINT}). = {divs:,}. "
            "Excludes distributions to minorities (9 in H1). FLAG: 366 is RELX's expected cost; the actual cash is not yet published."},
        "buybacks_after_balance_sheet_mgbp": {"value": round(buybacks, 1), "source":
            f"Cash spent on buybacks 1 Jan to 25 Sep 2026 (the date of the share count): H1 1,750 ({H126} p.20 cash flow; p.12 'Total consideration "
            f"... was GBP 1,750m') + 100 (1-21 Jul, {BB23JUL}: 'completion of a GBP 100 million ... programme on 21 July 2026') + 150 (23 Jul-4 Sep, "
            f"{BB7SEP}: 'completion of a GBP 150 million ... programme on 4 September 2026') + 56.2 (7-25 Sep, {F['shares_7_25sep']:,} shares x daily "
            f"VWAP summed over 15 trading days, {TX}; excludes 0.5% stamp duty and commission, c. GBP 0.3m) = {buybacks:,.1f}. "
            "Employee Benefit Trust purchases (60 in H1) are not buybacks and are excluded."},
    }


def main(write_inputs: bool) -> None:
    fin = financials()
    fin.to_csv(DATA / "financials.csv", index=False)
    tie = tie_out(fin)
    tie.to_csv(DATA / "tie_out.csv", index=False)
    market = json.loads((DATA / "market_inputs.json").read_text())
    inputs = build_inputs(market)
    (DATA / "market_data.json").write_text(json.dumps({"price_date": str(PRICE_DATE), "market_inputs": market,
                                                       "not_needed_items": NOT_NEEDED}, indent=2))
    print(tie.to_string(index=False))
    print(json.dumps({k: v["value"] for k, v in inputs.items()}, indent=2))
    if write_inputs:
        (RUN / "inputs.yaml").write_text(yaml.safe_dump(inputs, sort_keys=False, width=160, allow_unicode=True))
        print("wrote", RUN / "inputs.yaml")


if __name__ == "__main__":
    main("--write-inputs" in sys.argv)
