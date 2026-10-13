"""Bear agent (Phase 3 re-run; refreshed 2026-10-13 for proportionate minorities): re-run the engine with ONE change at a time (desk.valuation_run.build), record the impact.

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
# extra_required(brief) = roll-forward input + minority_share_of_operating_profit (brief: minorities_method proportionate)
v, _src = valuation_run.load_inputs(str(RUN / "inputs.yaml"), valuation_run.extra_required(brief))
valuation_run.apply_brief_rules(brief, v, _src)  # cost of debt = risk-free + credit spread (PM rule)
base_run = valuation_run.build(brief, v)
base = base_run["equity"]["per_share_gbp_pence"]
base_wacc = base_run["wacc"]["wacc_used"]
# the base must reproduce the Valuation agent's published value (valuation.json), else STOP
_published = json.loads((RUN / "valuation/valuation.json").read_text())["base"]["equity"]["per_share_gbp_pence"]
if abs(base - _published) > 0.05:
    raise SystemExit(f"Base {base:.2f}p does not match valuation.json {_published:.2f}p: STOP")
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


# Minorities at market for USL (listed), book for the rest (USD m). Market value of the outside stake
# = outside shareholders' % x shares x share price (INR) / INR per USD.
USL_OUTSIDE_PCT = 1 - 0.5721      # 42.79%: Diageo owns 57.21% of United Spirits (inputs.yaml disposal_proceeds source)
USL_SHARES_M = 727.35             # USL shares outstanding, m (Yahoo Finance UNITDSPR.NS, 12 Oct 2026)
USL_PRICE_INR = 1362.5            # USL share price, INR (Yahoo Finance UNITDSPR.NS close, 12 Oct 2026)
INR_PER_USD = 95.285              # Yahoo Finance INR=X, 12 Oct 2026
OTHER_MINORITIES_BOOK = 1328.0    # other non-controlling interests at book, USD m (20-F FY26 p.189; INCLUDES EABL's 35%)
USL_MINORITY_MARKET = USL_OUTSIDE_PCT * USL_SHARES_M * USL_PRICE_INR / INR_PER_USD  # market value of minority stake, USD m
MIXED_MINORITIES = USL_MINORITY_MARKET + OTHER_MINORITIES_BOOK                       # USD m


def solve(fn, lo, hi, tol=1e-6):
    """Bisection: the input at which value per share crosses the SELL line (fn(x) = value - SELL line)."""
    flo = fn(lo)
    for _ in range(200):
        mid = (lo + hi) / 2
        fm = fn(mid)
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
        if hi - lo < tol:
            break
    return (lo + hi) / 2


def _value(brief_changes=None, inputs=None):
    return run("x", "solver", inputs, brief_changes)["value_pence"]


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
    run("8", "Valuation/PM: minorities = USL outside stake at market (USD %.0fm) + others at book (USD 1,328m) = USD %.0fm"
        % (USL_MINORITY_MARKET, MIXED_MINORITIES),
        {"minority_interests": MIXED_MINORITIES}, brief_changes={"dcf.bridge.minorities_method": "book"}),
    run("8'", "Check: old book method (USD 2,083m, incl. EABL's 35%)", brief_changes={"dcf.bridge.minorities_method": "book"}),
    run("B", "Engine bear scenario (no growth, 25% flow-through, WACC +1pt): combined, NOT a single change",
        growth=bear["organic_growth"], flow_through=bear["flow_through"], wacc_shift=bear["wacc_shift"]),
]
# SELL-flip thresholds re-solved here with the engine (cross-check of valuation/sanity_checks.json)
flips = {
    "flow_through": solve(lambda x: _value({"dcf.savings.flow_through": x}) - SELL_BELOW, 0.0, 0.46),
    "beta": solve(lambda x: _value(inputs={"beta": x}) - SELL_BELOW, 0.96, 1.2),
    "terminal_ronic": solve(lambda x: _value({"dcf.terminal_ronic": x}) - SELL_BELOW, 0.09, 0.134),
    "mixed_minorities_musd": solve(lambda x: _value({"dcf.bridge.minorities_method": "book"}, {"minority_interests": x})
                                   - SELL_BELOW, 0.0, 10000.0, tol=0.01),
}
out = {"base_value_pence": base, "base_wacc": base_wacc, "share_price_pence": v["share_price_gbp_pence"],
       "sell_threshold_pence": SELL_BELOW, "headroom_to_sell_pence": base - SELL_BELOW,
       "base_minorities_deducted_musd": base_run["equity"]["minorities_deducted"],
       "usl_minority_market_musd": USL_MINORITY_MARKET, "mixed_minorities_musd": MIXED_MINORITIES,
       # EV / operating profit multiples on the minorities' slice (USD m). Minorities' operating profit ex-EABL
       # = share 2.566% x group operating profit ex-EABL 5,432.8 (inputs.yaml minority_share_of_operating_profit source)
       "minorities_operating_profit_ex_eabl_musd": v["minority_share_of_operating_profit"] * 5432.8,
       "dcf_multiple_on_minorities_x": base_run["equity"]["minorities_deducted"] / (v["minority_share_of_operating_profit"] * 5432.8),
       "usl_market_stake_over_all_minorities_op_profit_x": USL_MINORITY_MARKET / (v["minority_share_of_operating_profit"] * 5432.8),
       "sell_if": {"flow_through_below": flips["flow_through"], "beta_above": flips["beta"],
                   "terminal_ronic_below": flips["terminal_ronic"],
                   "minorities_book_basis_above_musd": flips["mixed_minorities_musd"]},
       "retired": {"6 (old)": "Deducting the 30c FY26 final dividend: retired. It goes ex on 15 Oct 2026, after the 12 Oct "
                   "valuation date, so the 1,673p price is cum-dividend (data/notes.md, Phase 3 additions)."},
       "challenges": res}
(Path(__file__).parent / "challenges.json").write_text(json.dumps(out, indent=2))
print(f"base {base:.1f}p  wacc {base_wacc:.4f}  SELL below {SELL_BELOW:.1f}p  headroom {base - SELL_BELOW:.1f}p")
print(f"minorities base {base_run['equity']['minorities_deducted']:.1f}  USL mkt {USL_MINORITY_MARKET:.1f}  mixed {MIXED_MINORITIES:.1f} (USD m)")
print("SELL flips:", {k: round(x, 5) for k, x in flips.items()})
for r in res:
    tc = r["terminal_capex_pct_sales"]
    print(f"{r['id']:4s} {r['challenge'][:70]:70s} {r['value_pence']:8.1f} {r['impact_pence']:+7.1f} "
          f"wacc {r['wacc']:.4f} tcapex {tc if tc is None else round(tc, 4)} {r['rating']} {r['upside']:+.3f}")
