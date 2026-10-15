"""Bear agent: one-change-at-a-time value impacts for KO (run 2026-10-13). Values per share in US DOLLARS.

Re-run 15 Oct 2026 (evidence audit, docs/audit-2026-10-15/KO.md): the brief now has ERP 4.2% and
scenarios.bear.bear_agent_margin 0.319; inputs.yaml has priced_at_valuation_date_musd (listed stakes not grown in the
roll-forward). Scenarios that move the LISTED stakes now move priced_at_valuation_date_musd by the same amount, so the
run-date market value is not grown again. Added: the stacked bear case at the PM's 31.9% margin and the audit stress lines
(ERP 5.0% Kroll, 5.5% Fernandez). Results from 13 Oct are kept in bear_runs_2026-10-13_superseded.json.
Final re-run 15 Oct 2026 (PM bear responses, "Accept all"): FY26 growth +5.0% in base and bear (briefs/KO.yaml). The FY26
5.0% stress lines became the base; they are replaced by reference runs at the old 6.0%.

Never edits briefs/KO.yaml or inputs.yaml. Each scenario writes a scratch copy of both files to bear/scratch/<name>/
and runs the desk engine on it exactly as the Valuation agent did:
    python -m desk.valuation_run <brief> <inputs> <out_dir>
The value per share is read back from <out_dir>/valuation.json ("base" block = the scenario with one change).
Run from the repo root: PYTHONPATH=. python runs/KO/2026-10-13/bear/run_bear.py
"""
import copy
import json
import os
import subprocess
import sys
from pathlib import Path

import yaml

from desk import fundamentals
from desk.valuation_run import apply_brief_rules, build, extra_required, load_inputs

HERE = Path(__file__).parent
RUN = HERE.parent
ROOT = RUN.parents[2]
SCRATCH = HERE / "scratch"
BRIEF0 = yaml.safe_load((ROOT / "briefs" / "KO.yaml").read_text())
RAW0 = yaml.safe_load((RUN / "inputs.yaml").read_text())


def v(key):
    return RAW0[key]["value"]


def set_input(raw, key, val, note):
    raw = copy.deepcopy(raw)
    raw[key] = {"value": val, "source": f"BEAR SCRATCH SCENARIO ONLY, not the base: {note}"}
    return raw


def run(name, brief=None, raw=None):
    """Write scratch copies and run the engine CLI (desk.valuation_run) on them."""
    d = SCRATCH / name
    d.mkdir(parents=True, exist_ok=True)
    bp, ip = d / "brief.yaml", d / "inputs.yaml"
    bp.write_text(yaml.safe_dump(brief or BRIEF0, sort_keys=False))
    ip.write_text(yaml.safe_dump(raw or RAW0, sort_keys=False, width=200))
    env = {**os.environ, "PYTHONPATH": str(ROOT)}
    subprocess.run([sys.executable, "-m", "desk.valuation_run", str(bp), str(ip), str(d)], check=True, cwd=ROOT,
                   env=env, capture_output=True)
    full = json.loads((d / "valuation.json").read_text())
    out = full["base"]
    return {"bear_block_value_per_share_usd": full["bear"]["equity"]["per_share_usd"],
            "bear_block_rating": full["bear"]["rating"]["rating"], "bear_block_wacc": full["bear"]["wacc"]["wacc_used"],
            "value_per_share_usd": out["equity"]["per_share_usd"], "rating": out["rating"]["rating"],
            "upside": out["rating"]["upside"], "wacc": out["wacc"]["wacc_used"],
            "enterprise_value_musd": out["enterprise_value_musd"], "tv_share_of_ev": out["tv_share_of_ev"],
            "implied_exit_ev_ebitda": out["implied_exit_ev_ebitda"]}


res = {}
res["base_check"] = run("base_check")
base_ps = res["base_check"]["value_per_share_usd"]

# ---------- Challenge 1: margin (Fundamentals / Data) ----------
# (a) the brief's literal bear: FY24 comparable operating margin 30.0% (Q4 2024 8-K 0000021344-25-000005), which INCLUDES CCBA
res["c1_margin_30pct_fy24_incl_ccba"] = run("c1_margin_300", raw=set_input(RAW0, "base_margin", 0.300,
                                            "FY24 comparable operating margin 30.0%, Q4 2024 8-K 0000021344-25-000005"))
# (b) like-for-like: FY24 comparable operating margin EX-CCBA. Operating margin = (comparable OI - CCBA EBIT) /
#     (comparable revenue - CCBA revenue). CCBA figures are calendar 2024 (Coca-Cola HBC deal factsheet, inputs.yaml),
#     i.e. the SAME year as FY24, so this is the cleanest like-for-like comparison.
ccba_rev, ccba_ebit = 3632.3, 266.2          # USD m, EUR 3,357m / EUR 246m x 1.082 (inputs.yaml base_sales / base_margin)
fy24_comp_oi, fy24_comp_rev = 14085.0, 46897.0  # Q4 2024 8-K reconciliation (data/financials.csv)
fy24_margin_ex_ccba = fundamentals.margin(fy24_comp_oi - ccba_ebit, fy24_comp_rev - ccba_rev)
res["fy24_margin_ex_ccba"] = fy24_margin_ex_ccba
# (c) the PM's bear margin exactly as decided on 13 Oct 2026 (brief scenarios.bear.bear_agent_margin = 0.319), one change
BEAR_M = BRIEF0["scenarios"]["bear"]["bear_agent_margin"]
res["c1_margin_pm_bear_319"] = run("c1_margin_319", raw=set_input(RAW0, "base_margin", BEAR_M,
                                   "PM bear margin 31.9% (briefs/KO.yaml scenarios.bear.bear_agent_margin, decision 13 Oct 2026)"))
res["c1_margin_fy24_ex_ccba"] = run("c1_margin_fy24_ex_ccba", raw=set_input(RAW0, "base_margin", fy24_margin_ex_ccba,
                                    "FY24 comparable margin ex-CCBA (14,085-266.2)/(46,897-3,632.3)"))

# ---------- Challenge 2: currency drag (Valuation / PM growth path) ----------
b = copy.deepcopy(BRIEF0)
# FY26 as the base (read from the brief: +5.0% since the PM decision of 15 Oct 2026), then 1% a year = the full 2020-25
# average currency drag of 3.2 pts (ko-growth-evidence.md)
b["dcf"]["organic_growth"] = [BRIEF0["dcf"]["organic_growth"][0], 0.010, 0.010, 0.010, 0.010]
res["c2_growth_1pct_fy27_30"] = run("c2_growth_1pct", brief=b)
b = copy.deepcopy(BRIEF0)
b["dcf"]["organic_growth"] = [0.045, 0.030, 0.030, 0.030, 0.030]  # FY26 if the currency tailwind (+1%) and the 0.5pt beat vs original 4-5% fade
res["c2_fy26_4p5pct"] = run("c2_fy26_4p5", brief=b)

# ---------- Challenge 3: IRS case and FY26 cash flow (Data / PM) ----------
# decomposition of the PM's "lose" case vs a win: liability only, tax-rate uplift only, both (= win scenario)
res["c3_irs_win_full"] = run("c3_irs_win", raw=set_input(set_input(set_input(RAW0, "contingent_liabilities", 0.0, "IRS win"),
                            "associates", v("associates") + 6000.0, "IRS win: $6.0bn deposit refunded (FY25 10-K)"),
                            "tax_rate", 0.199, "IRS win: 19.9% underlying (Q2 2026 8-K)"))
res["c3_irs_tax_only_19p9"] = run("c3_irs_tax_only", raw=set_input(RAW0, "tax_rate", 0.199, "19.9% only, liability kept"))
res["c3_irs_liability_only_0"] = run("c3_irs_liab_only", raw=set_input(RAW0, "contingent_liabilities", 0.0, "liability 0, tax kept"))
# bear: interest keeps accruing on the unpaid 2010-25 amount until paid (FY25 10-K Note 12; Q2 2026 10-Q Note 9 gives
# +$900m for H1 2026). The PM excluded the $900m (mistakes log row 17); test adding it anyway.
res["c3_irs_plus_h1_accrual"] = run("c3_irs_plus900", raw=set_input(RAW0, "contingent_liabilities", 14900.0,
                                    "14,000 + 900 H1 2026 accrual (Q2 2026 10-Q Note 9)"))

# FY26 FCF reconciliation: model unlevered FCF vs KO's FY26 FCF guidance (Q2 2026 8-K 0001628280-26-049922: ~$12.4bn)
bb = yaml.safe_load((SCRATCH / "base_check" / "brief.yaml").read_text())
vv, ss = load_inputs(str(SCRATCH / "base_check" / "inputs.yaml"), extra_required(bb))
apply_brief_rules(bb, vv, ss)
fy26 = build(bb, vv)["dcf"]["rows"][0]
guided_fcf, guided_capex = 12400.0, 2200.0
fy25_interest_paid, fy25_interest_income = 1724.0, 786.0   # FY25 10-K: interest paid (cash flow note); XBRL InvestmentIncomeInterest
fy25_div_from_equity_investees = 993.0                     # FY25 10-K Note 6: dividends received from equity method investees
fy25_sbc = 279.0                                           # FY25 10-K cash flow statement: stock-based compensation expense
recon = {
    "model_fy26_ufcf": fy26["ufcf"],
    "model_fy26_components": {k: fy26[k] for k in ("sales", "ebit", "tax", "nopat", "da", "capex", "delta_nwc", "ufcf")},
    # IRS: guidance tax rate 19.9% excludes the case; the model charges 23.7% -> extra tax = EBIT x 3.8 points
    "add_irs_tax_uplift_not_in_guidance": fy26["ebit"] * (0.237 - 0.199),
    # KO's FCF includes dividends from Monster/bottlers; the DCF values those stakes in the bridge instead
    "add_dividends_from_equity_investees_fy25": fy25_div_from_equity_investees,
    # non-cash expense inside comparable operating income, added back in KO's cash from operations
    "add_stock_based_comp_fy25": fy25_sbc,
    # KO's FCF is levered: after net interest paid (after tax at 19.9%); the DCF is unlevered
    "less_net_interest_after_tax_fy25": -(fy25_interest_paid - fy25_interest_income) * (1 - 0.199),
    # guided capex vs model capex (4.405% of ex-CCBA sales)
    "less_capex_guidance_vs_model": -(guided_capex - fy26["capex"]),
}
explained = recon["model_fy26_ufcf"] + sum(val for k, val in recon.items() if k.startswith(("add_", "less_")))
recon["explained_total"] = explained
recon["ko_guided_fcf"] = guided_fcf
recon["residual_unexplained"] = guided_fcf - explained  # CCBA part-year cash flow, other non-cash items, cash one-offs
recon["gap_guidance_minus_model"] = guided_fcf - recon["model_fy26_ufcf"]  # what the reconciling items must explain
res["c3_fy26_fcf_reconciliation_musd"] = recon

# leverage if the IRS liability is paid in cash (desk.fundamentals.leverage = net debt / EBITDA)
res["c3_leverage"] = {
    "now_net_debt_to_comparable_ebitda": fundamentals.leverage(v("net_debt"), 16063.0),
    "after_paying_14bn": fundamentals.leverage(v("net_debt") + 14000.0, 16063.0),
}

# ---------- Challenge 4: equity stakes at market (Data / Valuation bridge) ----------
listed_run = 39539.5        # data/associates_rollforward_check.csv
listed_dec25 = 34286.0      # FY25 10-K fair value of listed equity-method stakes
listed_book = 13999.0       # FY25 10-K book value of the same stakes
monster_run = 17774.9       # data/associates_rollforward_check.csv
res["monster_share_of_listed"] = monster_run / listed_run


def listed_cut(cut, note):
    """Lower the LISTED stakes by `cut` (USD m): both inside associates and in the not-grown run-date part
    (priced_at_valuation_date_musd), because the listed stakes are priced at the run date (mistakes log row 24)."""
    r = set_input(RAW0, "associates", v("associates") - cut, note)
    return set_input(r, "priced_at_valuation_date_musd", v("priced_at_valuation_date_musd") - cut, note)


res["c4_stakes_at_31dec25_fair_value"] = run("c4_stakes_dec25", raw=listed_cut(listed_run - listed_dec25,
                                             "listed at 31 Dec 2025 fair value 34,286"))
res["c4_monster_minus_30pct"] = run("c4_monster_m30", raw=listed_cut(0.30 * monster_run, "Monster stake -30%"))
# tax leakage: realising market value above book would trigger tax on the gain; 21% = US federal statutory rate
# (FY25 10-K tax rate reconciliation). Book is used as a proxy for tax basis (not disclosed): FLAG.
tax_leak = 0.21 * (listed_run - listed_book)
res["c4_tax_leakage_musd"] = tax_leak
res["c4_stakes_after_tax_on_gain"] = run("c4_stakes_tax", raw=listed_cut(tax_leak,
                                         "listed stakes net of 21% tax on gain over book"))

# ---------- Challenge 5: beta stability (Risk) ----------
# Damodaran betas.xls (data/damodaran_betas_us_jan2026.xls), 'Industry Averages', Beverage (Soft), unlevered beta corrected
# for cash: 2022 1.116, 2023 1.201, 2024 0.700, 2025 0.510, 2026 0.575, average 2022-26 0.8205. Relevered x1.0584 (Hamada).
relever = 1.0584193437257772  # risk/beta_evidence.json
for label, ub in (("avg_2022_26", 0.8204851316412943), ("y2024", 0.70)):
    res[f"c5_beta_{label}"] = run(f"c5_beta_{label}", raw=set_input(RAW0, "beta", ub * relever,
                                  f"Damodaran soft-beverage unlevered {ub} x {relever:.4f}"))

# ---------- Is the desk too harsh? (single changes the other way, then all together) ----------
res["harsh_tg_3pct"] = run("harsh_tg3", brief={**copy.deepcopy(BRIEF0), "dcf": {**BRIEF0["dcf"], "terminal_growth": 0.03}})
res["harsh_beta_5y_weekly_0p35"] = run("harsh_beta035", raw=set_input(RAW0, "beta", 0.3457, "KO 5y weekly regression (risk.json)"))
res["harsh_ronic_31p4"] = run("harsh_ronic314", brief={**copy.deepcopy(BRIEF0), "dcf": {**BRIEF0["dcf"], "terminal_ronic": 0.314}})
res["harsh_da_fy25_2p19"] = run("da_fy25", raw=set_input(RAW0, "da_pct_sales", 0.0219, "FY25 D&A 1,050 / 47,941"))
gen_raw = set_input(set_input(set_input(set_input(RAW0, "contingent_liabilities", 0.0, "IRS win"), "associates",
          v("associates") + 6000.0, "deposit refunded"), "tax_rate", 0.199, "19.9%"), "beta", 0.3457, "5y weekly regression")
gen_brief = copy.deepcopy(BRIEF0)
gen_brief["dcf"]["terminal_growth"] = 0.03
gen_brief["dcf"]["terminal_ronic"] = 0.314
res["harsh_all_generous_together"] = run("harsh_all", brief=gen_brief, raw=gen_raw)
# Re-run 15 Oct 2026: with ERP 4.2% the four-together case crosses the HOLD line, so test which of the four it needs.
# Leave-one-out: all generous changes except one (each reverts to the base input).
irs_win_raw = set_input(set_input(set_input(RAW0, "contingent_liabilities", 0.0, "IRS win"), "associates",
              v("associates") + 6000.0, "deposit refunded"), "tax_rate", 0.199, "19.9%")
res["generous_without_beta"] = run("gen_wo_beta", brief=gen_brief, raw=irs_win_raw)
res["generous_without_irs_win"] = run("gen_wo_irs", brief=gen_brief, raw=set_input(RAW0, "beta", 0.3457, "5y weekly regression"))
gb = copy.deepcopy(gen_brief); gb["dcf"]["terminal_growth"] = BRIEF0["dcf"]["terminal_growth"]
res["generous_without_tg3"] = run("gen_wo_tg3", brief=gb, raw=gen_raw)
gb = copy.deepcopy(gen_brief); gb["dcf"]["terminal_ronic"] = BRIEF0["dcf"]["terminal_ronic"]
res["generous_without_ronic"] = run("gen_wo_ronic", brief=gb, raw=gen_raw)

# ---------- Stacked bear case (PM decisions 13 Oct 2026 + brief bear scenario) ----------
# Brief scenarios.bear (1% growth FY27-30, WACC +1 point) PLUS the PM's bear margin 31.9%. The engine's bear block already
# applies the growth path and WACC shift; the margin goes in through base_margin. PM decisions: no tax on stake gains,
# beta 0.6091 kept, so neither is stacked. We read the "bear" block of valuation.json.
res["stacked_bear_pm_319"] = run("stacked_bear_319", raw=set_input(RAW0, "base_margin", BEAR_M,
                                 "stacked bear: PM bear margin 31.9% (briefs/KO.yaml scenarios.bear.bear_agent_margin)"))
# Reference only (PM decision 15 Oct 2026 adopted FY26 +5.0% in base and bear): the stacked bear at the OLD FY26 +6.0%,
# to show the step from the morning re-run. Not a scenario the desk uses.
b = copy.deepcopy(BRIEF0)
b["scenarios"]["bear"]["organic_growth"] = [0.060] + list(BRIEF0["scenarios"]["bear"]["organic_growth"][1:])
res["ref_stacked_bear_319_fy26_6p0_pre_decision"] = run("ref_stacked_bear_319_fy26_6p0", brief=b, raw=set_input(RAW0, "base_margin", BEAR_M,
                                       "reference: stacked bear 31.9% at the pre-decision FY26 6.0%"))

# ---------- Audit stress lines (evidence audit 15 Oct 2026), one change each ----------
for label, erp in (("kroll_5p0", 0.050), ("fernandez_5p5", 0.055)):
    b = copy.deepcopy(BRIEF0)
    b["dcf"]["wacc"]["equity_risk_premium"] = erp   # Kroll US 5.0% / Fernandez 2025 survey US 5.5% (erp-evidence.md 2b, 2c)
    res[f"audit_erp_{label}"] = run(f"audit_erp_{label}", brief=b)
# Audit finding 3 (FY26 +5.0%) was ACCEPTED by the PM on 15 Oct 2026 and is now the base. Reference only: the base at the
# OLD FY26 +6.0%, i.e. the step from the morning re-run (USD 50.76) to the final base.
b = copy.deepcopy(BRIEF0)
b["dcf"]["organic_growth"] = [0.060] + list(BRIEF0["dcf"]["organic_growth"][1:])
res["ref_fy26_6p0_pre_decision"] = run("ref_fy26_6p0_pre_decision", brief=b)

# market-implied yields at $90.12 (plain ratios, for the memo)
mcap = v("shares_outstanding_m") * v("share_price_usd")
res["market"] = {"market_cap_musd": mcap, "fcf_yield_on_fy26_guidance": guided_fcf / mcap,
                 "earnings_yield_comparable_fy25": 3.00 / v("share_price_usd"), "us10y": v("risk_free"),
                 "fcf_yield_minus_us10y": guided_fcf / mcap - v("risk_free")}  # yield gap vs the risk-free rate

# derived figures quoted in challenges.md
val0 = json.loads((RUN / "valuation" / "valuation.json").read_text())
res["derived"] = {
    "brief_bear_minus_base_usd": val0["bear"]["equity"]["per_share_usd"] - base_ps,
    "engine_bear_valuation_json_usd": val0["bear"]["equity"]["per_share_usd"],
    "stacked_bear_minus_base_usd": res["stacked_bear_pm_319"]["bear_block_value_per_share_usd"] - base_ps,
    "beta_2024_relevered": 0.70 * relever,
    "investee_dividend_yield_on_listed_market_value": fy25_div_from_equity_investees / listed_run,  # dividend yield
}
for k, r in res.items():
    if isinstance(r, dict) and "value_per_share_usd" in r:
        r["impact_vs_base_usd"] = r["value_per_share_usd"] - base_ps
(HERE / "bear_runs.json").write_text(json.dumps(res, indent=2, default=float))
for k, r in res.items():
    if isinstance(r, dict) and "value_per_share_usd" in r:
        print(f"{k:40s} USD {r['value_per_share_usd']:7.2f}  impact {r['impact_vs_base_usd']:+7.2f}  {r['rating']}  WACC {r['wacc']:.4f}"
              f"  | bear block USD {r['bear_block_value_per_share_usd']:.2f} {r['bear_block_rating']}")
    else:
        print(k, json.dumps(r, default=float)[:600])
