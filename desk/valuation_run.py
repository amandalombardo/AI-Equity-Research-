"""Run the full valuation (base case + bear case) from the PM brief and the agents' sourced inputs.

Usage: python -m desk.valuation_run briefs/<TICKER>.yaml runs/<TICKER>/<date>/inputs.yaml runs/<TICKER>/<date>/valuation

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
from desk.units import fx_key, money_key, per_share_key, price_currency, reporting_currency, share_price_key

REQUIRED = ["base_sales", "base_margin", "tax_rate", "da_pct_sales", "capex_pct_sales", "nwc_pct_sales",
            "risk_free", "beta", "pre_tax_cost_of_debt", "debt_weight", "net_debt", "shares_outstanding_m",
            "stub_years"]
OPTIONAL_BRIDGE = ["lease_liabilities", "minority_interests", "pension_deficit", "associates", "disposal_proceeds",
                   "restructuring_cash"]
# needed only when the brief values the company at its balance sheet date and rolls forward
# (in millions of the reporting currency: dividends_ex_before_valuation_musd or _meur)
DIVIDENDS = "dividends_ex_before_valuation"
# needed only when the brief's bridge lists buybacks_after_balance_sheet_m<ccy> (e.g. Unilever's 2026 buyback): cash
# spent on buybacks between the balance sheet date and the run date, when the share count is after the buyback
BUYBACKS = "buybacks_after_balance_sheet"
# needed only when the brief's bridge lists priced_at_valuation_date_m<ccy>: the part of associates and disposal proceeds
# already valued at the run date (e.g. listed stakes at today's price), which the roll-forward must not grow again
PRICED_NOW = "priced_at_valuation_date"
ROLL_FORWARD = [money_key(DIVIDENDS, "USD")]
# needed only when the brief values minorities proportionately (bridge.minorities_method: proportionate)
PROPORTIONATE = ["minority_share_of_operating_profit"]
# needed only when the brief lists contingent liabilities in its bridge (e.g. Coca-Cola's IRS case, assumed lost)
CONTINGENT = ["contingent_liabilities"]


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


def proportionate_minorities(brief: dict) -> bool:
    """True if the brief values minority interests as their share of operating profit x EV, not at book."""
    method = brief["dcf"]["bridge"].get("minorities_method", "book")
    if method not in ("book", "proportionate"):
        raise SystemExit(f"Unknown minorities_method {method!r}: use book or proportionate")
    return method == "proportionate"


def has_contingent_liabilities(brief: dict) -> bool:
    """True if the brief's bridge has a contingent_liabilities_musd (or _meur) line, so the agent must supply a sourced value."""
    bridge = brief["dcf"]["bridge"]
    return "contingent_liabilities_musd" in bridge or money_key("contingent_liabilities", reporting_currency(brief["company"])) in bridge


def buybacks_key(brief: dict) -> str | None:
    """The buyback input name if the brief's bridge lists buybacks (rolled-forward valuations only), else None."""
    key = money_key(BUYBACKS, reporting_currency(brief["company"]))
    return key if rolls_forward(brief) and key in brief["dcf"]["bridge"] else None


def priced_now_key(brief: dict) -> str | None:
    """The input name for bridge items already priced at the valuation date, if the brief's bridge lists it."""
    key = money_key(PRICED_NOW, reporting_currency(brief["company"]))
    return key if rolls_forward(brief) and key in brief["dcf"]["bridge"] else None


def price_inputs(company: dict) -> list:
    """The share price and, for a London price, the FX rate (reporting currency per GBP) from the brief's company."""
    if price_currency(company) == "GBp":
        return [fx_key(reporting_currency(company)), "share_price_gbp_pence"]
    per_share_key(price_currency(company), reporting_currency(company))  # refuses a USD price for a EUR reporter
    return ["share_price_usd"]


def dividends_key(brief: dict) -> str:
    return money_key(DIVIDENDS, reporting_currency(brief["company"]))


def extra_required(brief: dict) -> list:
    return (price_inputs(brief["company"])
            + ([dividends_key(brief)] if rolls_forward(brief) else []) + (PROPORTIONATE if proportionate_minorities(brief) else [])
            + (CONTINGENT if has_contingent_liabilities(brief) else [])
            + ([buybacks_key(brief)] if buybacks_key(brief) else [])
            + ([priced_now_key(brief)] if priced_now_key(brief) else []))


def fx_rate(brief: dict, v: dict) -> float | None:
    """Reporting currency per GBP (USD or EUR per GBP) for a London price; None for a US-dollar price."""
    co = brief["company"]
    return v[fx_key(reporting_currency(co))] if price_currency(co) == "GBp" else None


def savings_m(d: dict, rep: str) -> list:
    """Announced savings per forecast year, in millions of the reporting currency (cumulative_musd or _meur)."""
    return d["savings"].get(money_key("cumulative", rep), d["savings"].get("cumulative_musd"))


def build(brief: dict, v: dict, growth=None, flow_through=None, wacc_shift=0.0) -> dict:
    d = brief["dcf"]
    rep = reporting_currency(brief["company"])
    roll = rolls_forward(brief)
    w = dcf.wacc(dcf.WaccInputs(risk_free=v["risk_free"], equity_risk_premium=d["wacc"]["equity_risk_premium"],
                                beta=v["beta"], pre_tax_cost_of_debt=v["pre_tax_cost_of_debt"],
                                tax_rate=v["tax_rate"], debt_weight=v["debt_weight"]))
    inp = dcf.DcfInputs(base_sales=v["base_sales"], base_margin=v["base_margin"],
                        growth=growth or d["organic_growth"], cumulative_savings=savings_m(d, rep),
                        flow_through=d["savings"]["flow_through"] if flow_through is None else flow_through,
                        tax_rate=v["tax_rate"], da_pct_sales=v["da_pct_sales"], capex_pct_sales=v["capex_pct_sales"],
                        nwc_pct_sales=v["nwc_pct_sales"], wacc=w["wacc"] + wacc_shift,
                        terminal_growth=d["terminal_growth"], years=d["forecast_years"],
                        # balance-sheet basis: value at the 30 June balance sheet date, with all of FY27 ahead
                        stub_years=0.0 if roll else v["stub_years"], mid_year=d["mid_year_convention"],
                        terminal_capex_pct_sales=d.get("terminal_capex_pct_sales"))
    if d.get("terminal_ronic") == "pending":
        raise SystemExit("The PM has not yet set terminal_ronic in the brief (it says 'pending'): cannot value")
    if d.get("terminal_ronic") is not None:
        if d.get("terminal_capex_pct_sales") is not None:
            raise SystemExit("Brief sets both terminal_capex_pct_sales and terminal_ronic: choose one")
        inp.terminal_capex_pct_sales = dcf.capex_pct_for_ronic(inp, d["terminal_ronic"])
    val = dcf.value(inp)
    bridge = dcf.Bridge(net_debt=v["net_debt"], **{k: v[k] for k in OPTIONAL_BRIDGE},
                        contingent_liabilities=v["contingent_liabilities"] if has_contingent_liabilities(brief) else 0.0,
                        minority_share_of_ev=v["minority_share_of_operating_profit"] if proportionate_minorities(brief) else None)
    roll_args = ({"cost_of_equity": w["cost_of_equity"], "years": v["stub_years"],
                  "dividends": v[dividends_key(brief)],
                  "buybacks": v[buybacks_key(brief)] if buybacks_key(brief) else 0.0,
                  "priced_at_valuation_date": v[priced_now_key(brief)] if priced_now_key(brief) else 0.0}
                 if roll else None)
    eq = dcf.equity_bridge(val["enterprise_value"], bridge, v["shares_outstanding_m"], fx_rate(brief, v), roll_args, rep)
    ccy = price_currency(brief["company"])
    # fair value and share price in the same units: pence for a London price, US dollars for a US price
    r = rating(eq[per_share_key(ccy, rep)], v[share_price_key(ccy)], **brief["rating"])
    return {"wacc": {**w, "wacc_used": inp.wacc}, "inputs": inp, "dcf": val, "bridge": bridge.__dict__, "roll": roll_args,
            "equity": eq, "rating": r}


def main(brief_path: str, inputs_path: str, out_dir: str) -> None:
    brief = yaml.safe_load(Path(brief_path).read_text())
    v, sources = load_inputs(inputs_path, extra_required(brief))
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
    # terminal growth around the brief's own rate (2.0% for Diageo and KO gives 1.5%, 2.0%, 2.5%, 3.0% as before)
    growths = [g0 + s for s in (-0.005, 0, 0.005, 0.01)]
    grid_ev = dcf.sensitivity(base["inputs"], waccs, growths, brief["dcf"].get("terminal_ronic"))
    b = dcf.Bridge(**base["bridge"])
    ccy, rep = price_currency(brief["company"]), reporting_currency(brief["company"])
    key = per_share_key(ccy, rep)
    grid_px = [[None if ev is None else dcf.equity_bridge(ev, b, v["shares_outstanding_m"], fx_rate(brief, v), base["roll"], rep)[key]
                for ev in row] for row in grid_ev]

    def summary(s):
        return {"wacc": s["wacc"], money_key("enterprise_value", rep): s["dcf"]["enterprise_value"],
                "tv_share_of_ev": s["dcf"]["tv_share_of_ev"],
                "terminal_year": s["dcf"]["terminal_year"], "implied_exit_ev_ebitda": s["dcf"]["implied_exit_ev_ebitda"],
                "equity": s["equity"], "rating": s["rating"],
                "forecast": [{k: r[k] for k in ("year", "sales", "ebit", "ebit_margin", "ufcf", "pv")} for r in s["dcf"]["rows"]]}

    grid_name = {"GBp": "sensitivity_value_per_share_pence", "USD": "sensitivity_value_per_share_usd"}[ccy]
    result = {"price_currency": ccy, "reporting_currency": rep, "base": summary(base), "bear": summary(bear),
              money_key("bridge", rep): base["bridge"],
              grid_name: {"wacc": waccs, "terminal_growth": growths, "grid": grid_px},
              "inputs": v, "sources": sources}
    (out / "valuation.json").write_text(json.dumps(result, indent=2, default=float))
    write_dcf_workbook(out / "dcf.xlsx", brief, v, sources, base)
    unit = {"GBp": "pence", "USD": "usd"}[ccy]
    print(json.dumps({f"base_value_{unit}": base["equity"][key], "base_rating": base["rating"]["rating"],
                      f"bear_value_{unit}": bear["equity"][key]}, indent=2))


if __name__ == "__main__":
    main(*sys.argv[1:4])
