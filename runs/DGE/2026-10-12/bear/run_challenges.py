"""Bear agent (Phase 3 re-run): re-run the engine with ONE change at a time (desk.valuation_run.build), record the impact.

Run from the repo root:  PYTHONPATH=. python runs/DGE/2026-10-12/bear/run_challenges.py
The brief values at the 30 June balance sheet date and rolls equity forward, so inputs are loaded with ROLL_FORWARD.
Nothing in briefs/DGE.yaml, inputs.yaml or desk/ is changed: each change is applied to an in-memory copy.
"""
import copy
import json
from pathlib import Path

import yaml

from desk import valuation_run

RUN = Path(__file__).resolve().parents[1]
REPO = RUN.parents[2]
brief = yaml.safe_load((REPO / "briefs/DGE.yaml").read_text())
v, _src = valuation_run.load_inputs(str(RUN / "inputs.yaml"), valuation_run.ROLL_FORWARD)
valuation_run.apply_brief_rules(brief, v, _src)  # cost of debt = risk-free + credit spread (PM rule)
base_run = valuation_run.build(brief, v)
base = base_run["equity"]["per_share_gbp_pence"]
base_wacc = base_run["wacc"]["wacc_used"]
SELL_BELOW = v["share_price_gbp_pence"] * (1 - brief["rating"]["sell_if_downside_at_least"])  # SELL threshold, pence


def run(cid, name, inputs=None, brief_changes=None, **kw):
    """One change vs the base case: override sourced inputs and/or brief assumptions on a copy."""
    vv = {**v, **(inputs or {})}
    b = copy.deepcopy(brief)
    for path, val in (brief_changes or {}).items():
        node = b
        keys = path.split(".")
        for k in keys[:-1]:
            node = node[k]
        node[keys[-1]] = val
    r = valuation_run.build(b, vv, **kw)
    px = r["equity"]["per_share_gbp_pence"]
    return {"id": cid, "challenge": name, "value_pence": px, "impact_pence": px - base,  # value impact vs base, pence/share
            "wacc": r["wacc"]["wacc_used"], "terminal_capex_pct_sales": r["inputs"].terminal_capex_pct_sales,
            "rating": r["rating"]["rating"], "upside": r["rating"]["upside"], "flips_to_sell": px < SELL_BELOW}


bear = brief["scenarios"]["bear"]
res = [
    run("1", "Risk: beta 0.72 (Diageo's own 5y weekly regression) instead of bottom-up 0.96 [case FOR the stock]", {"beta": 0.72}),
    run("1b", "Risk: beta 1.00 (volatility 2.5x the index; Risk agent FLAG 1)", {"beta": 1.00}),
    run("2a", "Valuation/PM: savings flow-through 40%", brief_changes={"dcf.savings.flow_through": 0.40}),
    run("2b", "Valuation/PM: savings flow-through 33% (Diageo's 2017 'two thirds reinvested' rule)", brief_changes={"dcf.savings.flow_through": 0.33}),
    run("2c", "Valuation/PM: savings flow-through 25% (FY22-24 track record; brief bear)", brief_changes={"dcf.savings.flow_through": 0.25}),
    run("2d", "Valuation/PM: supply-chain savings phased 25/50/75/100% FY27-30 (slower than brief)", brief_changes={"dcf.savings.cumulative_musd": [377.5, 925.0, 962.5, 1000.0, 1000.0]}),
    run("3a", "Valuation/PM: terminal RONIC 10.8% (capex c.7.1% of sales held forever)", brief_changes={"dcf.terminal_ronic": 0.108}),
    run("3a'", "Check: terminal capex = 5y average 7.106% exactly (terminal_ronic off)", brief_changes={"dcf.terminal_ronic": None}),
    run("3b", "Valuation/PM: terminal RONIC = WACC (growth creates no value)", brief_changes={"dcf.terminal_ronic": base_wacc}),
    run("4", "Data/Valuation: terminal growth 1.5% (IWSR: spirits volumes falling)", brief_changes={"dcf.terminal_growth": 0.015}),
    run("5", "Fundamentals: no organic growth FY27-31 (3-year record -0.3% CAGR vs 4.0% target)", brief_changes={"dcf.organic_growth": [0.0] * 5}),
    run("6", "Valuation/PM: credit spread 2.0% (leverage 3.1x above the A-band range)", {"pre_tax_cost_of_debt": v["risk_free"] + 0.02}),
    run("7", "Data: restructuring cash after tax relief at 24.3% (850 -> 643) [case FOR the stock]", {"restructuring_cash": v["restructuring_cash"] * (1 - v["tax_rate"])}),
    run("B", "Engine bear scenario (no growth, 25% flow-through, WACC +1pt): combined, NOT a single change",
        growth=bear["organic_growth"], flow_through=bear["flow_through"], wacc_shift=bear["wacc_shift"]),
]
out = {"base_value_pence": base, "base_wacc": base_wacc, "share_price_pence": v["share_price_gbp_pence"],
       "sell_threshold_pence": SELL_BELOW,
       "retired": {"6 (old)": "Deducting the 30c FY26 final dividend: retired. It goes ex on 15 Oct 2026, after the 12 Oct "
                   "valuation date, so the 1,673p price is cum-dividend (data/notes.md, Phase 3 additions)."},
       "challenges": res}
(Path(__file__).parent / "challenges.json").write_text(json.dumps(out, indent=2))
print(f"base {base:.1f}p  wacc {base_wacc:.4f}  SELL below {SELL_BELOW:.1f}p")
for r in res:
    tc = r["terminal_capex_pct_sales"]
    print(f"{r['id']:4s} {r['challenge'][:70]:70s} {r['value_pence']:8.1f} {r['impact_pence']:+7.1f} "
          f"wacc {r['wacc']:.4f} tcapex {tc if tc is None else round(tc, 4)} {r['rating']} {r['upside']:+.3f}")
