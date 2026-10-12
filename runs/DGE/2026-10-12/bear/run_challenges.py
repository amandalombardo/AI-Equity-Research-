"""Bear agent: re-run the engine with ONE change at a time (desk.valuation_run.build), and record the impact."""
import copy
import json
from pathlib import Path

import yaml

from desk import valuation_run

RUN = Path(__file__).resolve().parents[1]
brief = yaml.safe_load(Path("briefs/DGE.yaml").read_text())
v, _src = valuation_run.load_inputs(str(RUN / "inputs.yaml"))
valuation_run.apply_brief_rules(brief, v, _src)  # cost of debt = risk-free + credit spread (PM rule)
base = valuation_run.build(brief, v)["equity"]["per_share_gbp_pence"]


def run(name, inputs=None, brief_changes=None, **kw):
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
    return {"challenge": name, "value_pence": px, "impact_pence": px - base, "wacc": r["wacc"]["wacc_used"],
            "rating": r["rating"]["rating"], "upside": r["rating"]["upside"]}


res = [
    run("0 Reference: historic cost of debt 3.81% (the first run's input, rejected by the PM)", {"pre_tax_cost_of_debt": v["pre_tax_cost_of_debt_historic"]}),
    run("2 Risk: beta 1.0 instead of 0.48", {"beta": 1.0}),
    run("3 Valuation: savings flow-through 25% (management says savings fund reinvestment)", brief_changes={"dcf.savings.flow_through": 0.25}),
    run("3b Valuation: savings flow-through 0% (savings fully reinvested)", brief_changes={"dcf.savings.flow_through": 0.0}),
    run("3c Valuation: supply-chain savings phased 25% FY27, 50% FY28, 75% FY29, 100% FY30", brief_changes={"dcf.savings.cumulative_musd": [377.5, 925.0, 962.5, 1000.0, 1000.0]}),
    run("4 Valuation: terminal growth 1.5% (IWSR: spirits volumes falling)", brief_changes={"dcf.terminal_growth": 0.015}),
    run("5 Fundamentals: no organic growth FY27-31 (3-year track record averages -0.3%)", brief_changes={"dcf.organic_growth": [0.0] * 5}),
    run("6 Data: net debt rolled forward for the 30c FY26 final dividend (2,222m x $0.30)", {"net_debt": v["net_debt"] + 0.30 * v["shares_outstanding_m"]}),
    run("1b Valuation: credit spread 2.0% instead of 1.0% (BBB-type spread if leverage stays above target)", {"pre_tax_cost_of_debt": v["risk_free"] + 0.02}),
]
out = {"base_value_pence": base, "share_price_pence": v["share_price_gbp_pence"], "challenges": res}
(Path(__file__).parent / "challenges.json").write_text(json.dumps(out, indent=2))
for r in res:
    print(f"{r['challenge'][:75]:75s} {r['value_pence']:8.0f} {r['impact_pence']:+8.0f} wacc {r['wacc']:.4f} {r['rating']} {r['upside']:+.3f}")
