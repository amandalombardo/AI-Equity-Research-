"""Data agent (ULVR, run 2026-10-14): apply PM decision 10 (14 Oct 2026, docs/phase5/ulvr-run-flags.md items A, C, D and B).

Updates ONLY capex_pct_sales, nwc_pct_sales and associates in ../inputs.yaml; every other key (incl. the Risk agent's beta,
the Fundamentals agent's minority_share_of_operating_profit and buybacks_after_balance_sheet_meur) is kept as it is.
Figures come from financials.csv (20-F XBRL and filing text, each row sourced) and market_data.json (13 Oct 2026 closes).
Run from the repo root:  python runs/ULVR/2026-10-14/data/apply_pm_decision10.py
"""
import json
from pathlib import Path

import pandas as pd
import yaml

DATA = Path(__file__).resolve().parent
INPUTS = DATA.parent / "inputs.yaml"
F20 = ("Unilever FY25 Form 20-F (SEC accession 0000217410-26-000007, filed 12 Mar 2026, "
       "https://www.sec.gov/Archives/edgar/data/217410/000021741026000007/ul-20251231.htm)")
TMICC424 = "TMICC resale prospectus, Form 424(b)(4) (accession 0001104659-26-042683, 13 Apr 2026)"
PM = "PM decision 14 Oct 2026 (decision 10, docs/phase5/ulvr-run-flags.md item {}; briefs/ULVR.yaml comments)"

fin = pd.read_csv(DATA / "financials.csv")
mkt = json.loads((DATA / "market_data.json").read_text())
brief = yaml.safe_load(Path("briefs/ULVR.yaml").read_text())
inp = yaml.safe_load(INPUTS.read_text())


def v(item, fy=2025):
    return float(fin[(fin["item"] == item) & (fin["fiscal_year"] == fy)]["value_meur"].iloc[0])


sales = v("net_sales")
S = lambda x, n=0: f"{x:,.{n}f}"

# 1. Capex incl. software and other intangibles (item A): PP&E + intangibles purchases, % of turnover
capex_ppe, capex_int = v("capex"), v("capex_intangibles")
capex_pct = (capex_ppe + capex_int) / sales

# 2. Working capital without BOTH Magnum transition balances (item D)
inv, rec, pay = v("inventories"), v("trade_and_other_receivables"), v("trade_and_other_payables")
due_from, due_to = v("receivable_due_from_tmicc_in_trade_receivables"), v("payable_due_to_tmicc_in_trade_payables")
nwc = (inv + (rec - due_from) - (pay - due_to)) / sales     # operating working capital / sales

# 3. Associates and other investments (items E, B, C, D)
micc = mkt["MICC.AS"]
tmicc = 121_604_413 * micc["close"] / 1e6                    # listed stake at the 13 Oct close
rf, beta = inp["risk_free"]["value"], inp["beta"]["value"]
erp, g = brief["dcf"]["wacc"]["equity_risk_premium"], brief["dcf"]["terminal_growth"]
ke = rf + beta * erp                                         # cost of equity (CAPM): risk-free + beta x equity risk premium
jv_div = 229.0                                               # 20-F note 11: JV 'Dividends received/reductions' (229) + associates (nil)
jv = jv_div * (1 + g) / (ke - g)                             # Gordon growth: next year's dividend / (cost of equity - growth)
assoc_book = v("associates_book_value")
fv_inv = v("other_equity_investments_fvoci_ex_tmicc") + v("other_financial_assets_fvtpl_noncurrent")
magnum_net = due_from - due_to                               # net transition balance owed TO Unilever
associates = tmicc + jv + assoc_book + fv_inv + magnum_net

old = {k: inp[k]["value"] for k in ("capex_pct_sales", "nwc_pct_sales", "associates")}
inp["capex_pct_sales"] = {"value": round(capex_pct, 5), "source":
    f"{PM.format('A')}: FY25 (purchase of PP&E {S(capex_ppe)} + purchase of intangible assets {S(capex_int)}) / turnover {S(sales)} = "
    f"{capex_pct:.3%}. {F20} p.132 cash flow statement; XBRL ifrs-full:PurchaseOfPropertyPlantAndEquipmentClassifiedAsInvestingActivities, "
    f"PurchaseOfIntangibleAssetsClassifiedAsInvestingActivities, Revenue. Consistent with D&A 2.6% (1,310), which includes amortisation of those intangibles. "
    f"Brief capex_pct_sales 0.0315. Was 0.028 (PP&E only)."}
inp["nwc_pct_sales"] = {"value": round(nwc, 5), "source":
    f"{PM.format('D')}: FY25 (inventories {S(inv)} + (trade and other current receivables {S(rec)} - EUR {S(due_from)}m due from TMICC) "
    f"- (trade payables and other current liabilities {S(pay)} - EUR {S(due_to)}m due to TMICC)) / turnover {S(sales)} = {nwc:.2%}. "
    f"{F20} p.131 balance sheet; note 13 p.159 ('include EUR 2.1 billion due from TMICC': TSA receivables and working capital subsidies "
    f"recoverable on TSA exit); note 14 p.160 ('include EUR 1.6 billion due to TMICC'); XBRL ifrs-full:Inventories, TradeAndOtherCurrentReceivables, "
    f"TradeAndOtherCurrentPayables. Both temporary Magnum transition balances removed; the net EUR {S(magnum_net)}m is in associates. "
    f"Amounts as disclosed, rounded to EUR 0.1bn. Was -0.07821."}
inp["associates"] = {"value": round(associates, 1), "source":
    f"{PM.format('B, C, D; E agreed 13 Oct')}: sum of (1) TMICC 19.85%: 121,604,413 shares ({TMICC424}) x EUR {micc['close']:.3f} "
    f"(Yahoo MICC.AS close {micc['date']}) = {S(tmicc,1)}; (2) joint ventures by Gordon growth: FY25 dividends received from JVs and "
    f"associates EUR 229m ({F20} p.158 note 11: JVs 'Dividends received/reductions (229)', associates nil; the p.132 cash-flow line is 243 "
    f"because it also includes dividends from other non-current investments, which are valued in (4)) x (1 + {g:.1%}) / (cost of equity "
    f"{ke:.4%} - {g:.1%}) = {S(jv,1)}, cost of equity = risk-free {rf:.2%} (inputs.yaml) + beta {beta} (inputs.yaml, Risk agent) x ERP "
    f"{erp:.1%} (brief); (3) associates at book {S(assoc_book)} ({F20} p.158 note 11); (4) other fair-value financial investments "
    f"{S(fv_inv)} = equity investments FVOCI excl. TMICC 561 (2,216 - 1,655) + non-current FVTPL 'Other' 341 ({F20} p.174 note 17A); "
    f"amortised-cost assets 368 (incl. judicial deposits 175) excluded; (5) net Magnum transition balance owed to Unilever "
    f"{S(due_from)} - {S(due_to)} = {S(magnum_net)} ({F20} notes 13-14, p.159-160). Was 2,044.2 (TMICC + JVs/associates at book 109). "
    f"If the run's cost of equity changes, the JV value must be recomputed."}
INPUTS.write_text(yaml.safe_dump(inp, sort_keys=False, width=160, allow_unicode=True))

print(f"capex_pct_sales {old['capex_pct_sales']} -> {inp['capex_pct_sales']['value']}")
print(f"nwc_pct_sales   {old['nwc_pct_sales']} -> {inp['nwc_pct_sales']['value']}")
print(f"associates      {old['associates']} -> {inp['associates']['value']}")
print(f"  TMICC {tmicc:.1f} | ke {ke:.5f} | JV {jv:.1f} | assoc book {assoc_book} | FV inv {fv_inv} | Magnum net {magnum_net}")
print("keys kept:", [k for k in inp if k not in ("capex_pct_sales", "nwc_pct_sales", "associates")])
