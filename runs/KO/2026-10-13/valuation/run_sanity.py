"""Valuation agent sanity checks, rating flip points and labelled scenarios for KO (run 2026-10-13).

Never edits briefs/KO.yaml or inputs.yaml: every variant is written as a scratch copy in valuation/scratch/ and
re-run through the desk engine (desk.valuation_run.build). Per-share values in US dollars.
Run from the repo root: PYTHONPATH=. python runs/KO/2026-10-13/valuation/run_sanity.py
"""
import copy
import json
from pathlib import Path

import yaml

from desk import dcf
from desk.valuation_run import apply_brief_rules, build, extra_required, load_inputs

HERE = Path(__file__).parent
RUN = HERE.parent
ROOT = RUN.parents[2]
SCRATCH = HERE / "scratch"
SCRATCH.mkdir(exist_ok=True)
BRIEF_PATH, INPUTS_PATH = ROOT / "briefs" / "KO.yaml", RUN / "inputs.yaml"
brief0 = yaml.safe_load(BRIEF_PATH.read_text())
raw0 = yaml.safe_load(INPUTS_PATH.read_text())
price = raw0["share_price_usd"]["value"]
buy, sell = brief0["rating"]["buy_if_upside_at_least"], brief0["rating"]["sell_if_downside_at_least"]
hold_floor, buy_floor = price * (1 - sell), price * (1 + buy)  # value per share at which SELL->HOLD and HOLD->BUY


def run_copy(name, brief, raw, wacc_shift=0.0):
    """Write scratch copies, load them exactly as the engine does, and value."""
    bp, ip = SCRATCH / f"{name}_brief.yaml", SCRATCH / f"{name}_inputs.yaml"
    bp.write_text(yaml.safe_dump(brief, sort_keys=False))
    ip.write_text(yaml.safe_dump(raw, sort_keys=False, width=200))
    b = yaml.safe_load(bp.read_text())
    v, s = load_inputs(str(ip), extra_required(b))
    apply_brief_rules(b, v, s)
    return build(b, v, wacc_shift=wacc_shift)


def summary(r):
    return {"value_per_share_usd": r["equity"]["per_share_usd"], "upside": r["rating"]["upside"], "rating": r["rating"]["rating"],
            "wacc": r["wacc"]["wacc_used"], "cost_of_equity": r["wacc"]["cost_of_equity"],
            "enterprise_value_musd": r["dcf"]["enterprise_value"], "tv_share_of_ev": r["dcf"]["tv_share_of_ev"],
            "implied_exit_ev_ebitda": r["dcf"]["implied_exit_ev_ebitda"]}


def set_input(raw, key, val, note):
    raw = copy.deepcopy(raw)
    raw[key] = {"value": val, "source": f"SCRATCH SCENARIO ONLY, not the base: {note}"}
    return raw


def solve(fn, lo, hi, target, tol=1e-7):
    """Bisection: the parameter at which value per share = target (value assumed monotonic in the parameter)."""
    flo, fhi = fn(lo) - target, fn(hi) - target
    if flo * fhi > 0:
        return None
    for _ in range(80):
        mid = (lo + hi) / 2
        fm = fn(mid) - target
        if abs(hi - lo) < tol:
            break
        if fm * flo > 0:
            lo, flo = mid, fm
        else:
            hi = mid
    return (lo + hi) / 2


base = run_copy("base_check", brief0, raw0)
base_ps = base["equity"]["per_share_usd"]

# ---- flip points (each variable alone, everything else at base) ----
def by_beta(b):
    return run_copy("flip_beta", brief0, set_input(raw0, "beta", b, f"beta {b}"))["equity"]["per_share_usd"]


def by_wacc_shift(s):  # shift added to the engine's WACC (same mechanism as the brief's bear wacc_shift)
    return run_copy("flip_wacc", brief0, raw0, wacc_shift=s)["equity"]["per_share_usd"]


def by_tg(g):
    b = copy.deepcopy(brief0)
    b["dcf"]["terminal_growth"] = g
    return run_copy("flip_tg", b, raw0)["equity"]["per_share_usd"]


def by_margin(m):
    return run_copy("flip_margin", brief0, set_input(raw0, "base_margin", m, f"margin {m}"))["equity"]["per_share_usd"]


w0 = base["wacc"]["wacc_used"]
flips = {}
for label, fn, lo, hi, fmt in [
        ("beta", by_beta, -0.5, 0.6091, "beta"),
        ("wacc", by_wacc_shift, -0.04, 0.0, "wacc_shift"),
        ("terminal_growth", by_tg, 0.020, w0 - 0.0005, "g"),
        ("base_margin", by_margin, 0.33191, 0.80, "margin")]:
    f = {}
    for name, tgt in (("sell_to_hold_at_usd", hold_floor), ("hold_to_buy_at_usd", buy_floor)):
        x = solve(fn, lo, hi, tgt)
        f[name] = {"target_value_usd": tgt, "parameter": x, "value_check_usd": fn(x) if x is not None else None,
                   "status": "found" if x is not None else f"not reached in search range [{lo}, {hi}]"}
        if label == "wacc" and x is not None:
            f[name]["wacc_level"] = w0 + x
    flips[label] = f

# ---- scenario 1: beta from Damodaran 2022-26 average unlevered beta, relevered at the same Hamada factor ----
ev_beta = json.loads((RUN / "risk" / "beta_evidence.json").read_text())
factor = ev_beta["hamada_relever_factor"]
avg_unlevered = 0.820485  # Damodaran US Beverage (Soft) average unlevered beta 2022-26, as given by the lead agent
beta_avg = avg_unlevered * factor  # Hamada relevering: unlevered beta x (1 + (1 - t) x D/E)
sc_beta = run_copy("scenario_beta_avg", brief0, set_input(raw0, "beta", beta_avg,
                   f"Damodaran 2022-26 average unlevered beta {avg_unlevered} x Hamada factor {factor:.4f}"))

# ---- scenario 2: KO WINS the IRS case ----
raw_win = set_input(raw0, "contingent_liabilities", 0.0, "IRS case won: no liability")
raw_win = set_input(raw_win, "associates", raw0["associates"]["value"] + 6000.0,
                    "base associates + USD 6,000m 2007-09 deposit refunded (cash-equivalent)")
raw_win = set_input(raw_win, "tax_rate", 0.199, "IRS case won: FY26 underlying rate 19.9% without the 3.8-point uplift")
sc_win = run_copy("scenario_irs_win", brief0, raw_win)

d = base["dcf"]
comps = json.loads((HERE / "comps.json").read_text())
peer_ev_ebitda = [p["ev_ebitda_ltm"] for p in comps["peers"]]
primary = comps["comps_range_usd_primary"]
out = {
    "currency": "USD per share; USD m",
    "base_value_usd_recheck": base_ps,
    "checks": {
        "tv_share_of_ev": {"value": d["tv_share_of_ev"], "threshold": 0.75, "flag": d["tv_share_of_ev"] > 0.75},
        "implied_exit_ev_ebitda": {"value": d["implied_exit_ev_ebitda"], "peer_low": min(peer_ev_ebitda),
                                   "peer_high": max(peer_ev_ebitda), "peer_median": sorted(peer_ev_ebitda)[1],
                                   "ko_own_ev_ebitda_ltm": comps["ko_own_multiples"]["ev_ebitda_ltm_comparable_incl_ccba"],
                                   "within_peer_range": min(peer_ev_ebitda) <= d["implied_exit_ev_ebitda"] <= max(peer_ev_ebitda)},
        "wacc": {"value": w0, "range": [0.06, 0.09], "flag": not 0.06 <= w0 <= 0.09},
        "dcf_vs_comps": {"dcf_usd": base_ps, "comps_median_usd": primary["implied_value"],
                         "comps_low_usd": primary["low"], "comps_high_usd": primary["high"],
                         "gap": base_ps / primary["implied_value"] - 1}},  # gap = DCF / comps - 1
    "rating_thresholds_usd": {"hold_if_at_least": hold_floor, "buy_if_at_least": buy_floor},
    "flip_points": flips,
    "scenarios_not_base": {
        "beta_damodaran_2022_26_average": {"unlevered": avg_unlevered, "relever_factor": factor, "beta": beta_avg, **summary(sc_beta)},
        "irs_case_won": {"contingent_liabilities_musd": 0.0, "associates_musd": raw_win["associates"]["value"],
                         "tax_rate": 0.199, "note": "beta left at 0.6091 (relevered at 23.7%); USD 385m interest receivable not added",
                         **summary(sc_win)}},
}
(HERE / "sanity_checks.json").write_text(json.dumps(out, indent=2, default=float))
print(json.dumps(out, indent=1, default=float))
