"""Run the full valuation (base case + bear case) from the PM brief and the agents' sourced inputs.

Usage: python -m desk.valuation_run briefs/DGE.yaml runs/DGE/<date>/inputs.yaml runs/DGE/<date>/valuation

inputs.yaml holds every value that is null in the brief, each with a source, e.g.
    tax_rate: {value: 0.23, source: "FY26 20-F p.142, tax rate before exceptional items"}
The run stops if any required input is still missing, so nothing is silently estimated.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

from desk import dcf
from desk.excel_export import write_dcf_workbook
from desk.rating import rating

REQUIRED = ["base_sales", "base_margin", "tax_rate", "da_pct_sales", "capex_pct_sales", "nwc_pct_sales",
            "risk_free", "beta", "pre_tax_cost_of_debt", "debt_weight", "net_debt", "shares_outstanding_m",
            "fx_usd_per_gbp", "share_price_gbp_pence", "stub_years"]
OPTIONAL_BRIDGE = ["lease_liabilities", "minority_interests", "pension_deficit", "associates", "disposal_proceeds",
                   "restructuring_cash"]
# needed only when the brief values the company at its balance sheet date and rolls forward
ROLL_FORWARD = ["dividends_ex_before_valuation_musd"]


def load_inputs(path: str, extra_required: list | None = None) -> tuple[dict, dict]:
    raw = yaml.safe_load(Path(path).read_text()) or {}
    values = {k: (v["value"] if isinstance(v, dict) else v) for k, v in raw.items()}
    sources = {k: (v.get("source") if isinstance(v, dict) else None) for k, v in raw.items()}
    missing = [k for k in REQUIRED + OPTIONAL_BRIDGE + (extra_required or []) if values.get(k) is None]
    unsourced = [k for k in values if not sources.get(k)]
    if missing or unsourced:
        raise SystemExit(f"Cannot value. Missing inputs: {missing}. Inputs without a source: {unsourced}")
    return values, sources


def apply_brief_rules(brief: dict, v: dict, sources: dict) -> None:
    """Apply PM rules from the brief that replace an agent input.

    Cost of debt: if the brief sets a credit spread, the pre-tax cost of debt is the marginal
    cost of new borrowing = risk-free rate + credit spread (not the historic interest cost).
    """
    spread = brief["dcf"]["wacc"].get("credit_spread")
    if spread is not None:
        sources["pre_tax_cost_of_debt_historic"] = sources.get("pre_tax_cost_of_debt")
        v["pre_tax_cost_of_debt_historic"] = v["pre_tax_cost_of_debt"]
        v["pre_tax_cost_of_debt"] = v["risk_free"] + spread
        sources["pre_tax_cost_of_debt"] = f"risk-free {v['risk_free']:.2%} + credit spread {spread:.2%} (PM rule, briefs)"


def rolls_forward(brief: dict) -> bool:
    """True if the brief values at the balance sheet date and rolls equity forward to the valuation date."""
    return brief["dcf"].get("valuation_basis", "stub") == "balance_sheet_date"


def build(brief: dict, v: dict, growth=None, flow_through=None, wacc_shift=0.0) -> dict:
    d = brief["dcf"]
    roll = rolls_forward(brief)
    w = dcf.wacc(dcf.WaccInputs(risk_free=v["risk_free"], equity_risk_premium=d["wacc"]["equity_risk_premium"],
                                beta=v["beta"], pre_tax_cost_of_debt=v["pre_tax_cost_of_debt"],
                                tax_rate=v["tax_rate"], debt_weight=v["debt_weight"]))
    inp = dcf.DcfInputs(base_sales=v["base_sales"], base_margin=v["base_margin"],
                        growth=growth or d["organic_growth"], cumulative_savings=d["savings"]["cumulative_musd"],
                        flow_through=d["savings"]["flow_through"] if flow_through is None else flow_through,
                        tax_rate=v["tax_rate"], da_pct_sales=v["da_pct_sales"], capex_pct_sales=v["capex_pct_sales"],
                        nwc_pct_sales=v["nwc_pct_sales"], wacc=w["wacc"] + wacc_shift,
                        terminal_growth=d["terminal_growth"], years=d["forecast_years"],
                        # balance-sheet basis: value at the 30 June balance sheet date, with all of FY27 ahead
                        stub_years=0.0 if roll else v["stub_years"], mid_year=d["mid_year_convention"],
                        terminal_capex_pct_sales=d.get("terminal_capex_pct_sales"))
    if d.get("terminal_ronic") is not None:
        if d.get("terminal_capex_pct_sales") is not None:
            raise SystemExit("Brief sets both terminal_capex_pct_sales and terminal_ronic: choose one")
        inp.terminal_capex_pct_sales = dcf.capex_pct_for_ronic(inp, d["terminal_ronic"])
    val = dcf.value(inp)
    bridge = dcf.Bridge(net_debt=v["net_debt"], **{k: v[k] for k in OPTIONAL_BRIDGE})
    roll_args = ({"cost_of_equity": w["cost_of_equity"], "years": v["stub_years"],
                  "dividends": v["dividends_ex_before_valuation_musd"]} if roll else None)
    eq = dcf.equity_bridge(val["enterprise_value"], bridge, v["shares_outstanding_m"], v["fx_usd_per_gbp"], roll_args)
    r = rating(eq["per_share_gbp_pence"], v["share_price_gbp_pence"], **brief["rating"])
    return {"wacc": {**w, "wacc_used": inp.wacc}, "inputs": inp, "dcf": val, "bridge": bridge.__dict__, "roll": roll_args,
            "equity": eq, "rating": r}


def main(brief_path: str, inputs_path: str, out_dir: str) -> None:
    brief = yaml.safe_load(Path(brief_path).read_text())
    v, sources = load_inputs(inputs_path, ROLL_FORWARD if rolls_forward(brief) else None)
    apply_brief_rules(brief, v, sources)
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    base = build(brief, v)
    bear_cfg = brief["scenarios"]["bear"]
    bear = build(brief, v, growth=bear_cfg["organic_growth"], flow_through=bear_cfg["flow_through"],
                 wacc_shift=bear_cfg["wacc_shift"])
    w0, g0 = base["inputs"].wacc, base["inputs"].terminal_growth
    # not rounded, so the middle cell of the grid equals the base case exactly
    waccs = [w0 + s for s in (-0.01, -0.005, 0, 0.005, 0.01)]
    growths = [0.015, 0.020, 0.025, 0.030]
    grid_ev = dcf.sensitivity(base["inputs"], waccs, growths, brief["dcf"].get("terminal_ronic"))
    b = dcf.Bridge(**base["bridge"])
    grid_px = [[None if ev is None else dcf.equity_bridge(ev, b, v["shares_outstanding_m"], v["fx_usd_per_gbp"], base["roll"])["per_share_gbp_pence"]
                for ev in row] for row in grid_ev]

    def summary(s):
        return {"wacc": s["wacc"], "enterprise_value_musd": s["dcf"]["enterprise_value"],
                "tv_share_of_ev": s["dcf"]["tv_share_of_ev"],
                "terminal_year": s["dcf"]["terminal_year"], "implied_exit_ev_ebitda": s["dcf"]["implied_exit_ev_ebitda"],
                "equity": s["equity"], "rating": s["rating"],
                "forecast": [{k: r[k] for k in ("year", "sales", "ebit", "ebit_margin", "ufcf", "pv")} for r in s["dcf"]["rows"]]}

    result = {"base": summary(base), "bear": summary(bear), "bridge_musd": base["bridge"],
              "sensitivity_value_per_share_pence": {"wacc": waccs, "terminal_growth": growths, "grid": grid_px},
              "inputs": v, "sources": sources}
    (out / "valuation.json").write_text(json.dumps(result, indent=2, default=float))
    write_dcf_workbook(out / "dcf.xlsx", brief, v, sources, base)
    print(json.dumps({"base_value_pence": base["equity"]["per_share_gbp_pence"], "base_rating": base["rating"]["rating"],
                      "bear_value_pence": bear["equity"]["per_share_gbp_pence"]}, indent=2))


if __name__ == "__main__":
    main(*sys.argv[1:4])
