"""Valuation agent sanity checks, sizings and rating flip points for ULVR (run 2026-10-14).

Never edits briefs/ULVR.yaml or inputs.yaml. Every variant is an in-memory copy of the engine's inputs, valued with
desk.valuation_run.build (the same code as the base case). Money in EUR m; value per share in pence (GBp) unless labelled.
Run from the repo root (after run_comps.py): PYTHONPATH=. python runs/ULVR/2026-10-14/valuation/run_sanity.py
"""
import copy
import json
from datetime import date
from pathlib import Path

import yaml

from desk import dcf
from desk.valuation_run import apply_brief_rules, build, extra_required, load_inputs

HERE = Path(__file__).resolve().parent
RUN = HERE.parent
ROOT = RUN.parents[2]
brief0 = yaml.safe_load((ROOT / "briefs" / "ULVR.yaml").read_text())
v0, src = load_inputs(str(RUN / "inputs.yaml"), extra_required(brief0))
apply_brief_rules(brief0, v0, src)
mkt = json.loads((RUN / "data" / "market_data.json").read_text())
comps_out = json.loads((HERE / "comps.json").read_text())

price = v0["share_price_gbp_pence"]
shares, fx = v0["shares_outstanding_m"], v0["fx_eur_per_gbp"]
buy, sell = brief0["rating"]["buy_if_upside_at_least"], brief0["rating"]["sell_if_downside_at_least"]
hold_floor, buy_floor = price * (1 - sell), price * (1 + buy)   # value per share (pence) where SELL->HOLD and HOLD->BUY
ERP, G0 = brief0["dcf"]["wacc"]["equity_risk_premium"], brief0["dcf"]["terminal_growth"]


def pence(eur_m):
    """EUR m at today's date -> pence per share: EUR m / shares / (EUR per GBP) x 100 (desk.dcf.equity_bridge, no bridge)."""
    return dcf.equity_bridge(eur_m, dcf.Bridge(net_debt=0.0), shares, fx, None, "EUR")["per_share_gbp_pence"]


def grow(x, rate, years):
    """x carried forward at `rate` for `years` (compound growth; desk.dcf.roll_forward with nothing paid out)."""
    return dcf.roll_forward(x, rate, years)


def pv(x, rate, years):
    """Present value of x received in `years` at a discount `rate`: x / (1 + rate)^years."""
    return x / grow(1.0, rate, years)


# ---------- joint ventures: the PM's Gordon growth value depends on the cost of equity (data/apply_pm_decision10.py) ----
JV_DIV = 229.0   # FY25 dividends received from JVs, 20-F note 11 p.158


def jv_value(ke, g):
    """Gordon growth: next year's dividend / (cost of equity - growth) = 229 x (1 + g) / (Ke - g)."""
    return JV_DIV * (1 + g) / (ke - g)


KE0 = dcf.cost_of_equity(v0["risk_free"], v0["beta"], ERP)
JV0 = jv_value(KE0, G0)
ASSOC_EX_JV = v0["associates"] - JV0          # TMICC + associates at book + other investments + Magnum net balance
TMICC = 121_604_413 * mkt["MICC.AS"]["close"] / 1e6   # listed stake: shares (TMICC 424(b)(4)) x MICC.AS close, EUR m


def run(v=None, brief=None, wacc_shift=0.0, growth=None):
    return build(brief or brief0, v or v0, growth=growth, wacc_shift=wacc_shift)


def with_beta(beta, g=G0):
    """Inputs with a new beta AND the JV value recomputed at the new cost of equity (consistent)."""
    v = copy.deepcopy(v0)
    v["beta"] = beta
    v["associates"] = ASSOC_EX_JV + jv_value(dcf.cost_of_equity(v["risk_free"], beta, ERP), g)
    return v


def ps(r):
    return r["equity"]["per_share_gbp_pence"]


def summary(r):
    return {"value_per_share_pence": ps(r), "value_per_share_eur": r["equity"]["per_share_eur"],
            "upside": r["rating"]["upside"], "rating": r["rating"]["rating"], "wacc": r["wacc"]["wacc_used"],
            "cost_of_equity": r["wacc"]["cost_of_equity"], "enterprise_value_meur": r["dcf"]["enterprise_value"],
            "tv_share_of_ev": r["dcf"]["tv_share_of_ev"], "implied_exit_ev_ebitda": r["dcf"]["implied_exit_ev_ebitda"]}


base = run()
B = ps(base)
d = base["dcf"]
t_roll = v0["stub_years"]

# ================= sanity checks =================
peer_mults = [p["ev_ebitda_ltm"] for p in comps_out["peers"]]
core_mults = [p["ev_ebitda_ltm"] for p in comps_out["peers"] if p["ticker"] not in ("KMB", "CL")]
primary = comps_out["comps_range_pence_primary"]
checks = {
    "tv_share_of_ev": {"value": d["tv_share_of_ev"], "threshold": 0.75, "flag": d["tv_share_of_ev"] > 0.75},
    "implied_exit_ev_ebitda": {"value": d["implied_exit_ev_ebitda"], "peer_low": min(peer_mults), "peer_high": max(peer_mults),
                               "peer_median_all_7": comps_out["legs"]["ev_ebitda_ltm_all_7"]["median_multiple"],
                               "peer_median_ex_KMB_CL": comps_out["legs"]["ev_ebitda_ltm_ex_KMB_and_CL"]["median_multiple"],
                               "ulvr_market_implied_remaining_business": comps_out["ulvr_own_multiples"]["market_implied_ev_ebitda_ltm_pm_basis"],
                               "within_peer_range": min(peer_mults) <= d["implied_exit_ev_ebitda"] <= max(peer_mults),
                               "within_range_ex_KMB_CL": min(core_mults) <= d["implied_exit_ev_ebitda"] <= max(core_mults)},
    "wacc": {"value": base["wacc"]["wacc"], "range": [0.06, 0.09], "flag": not 0.06 <= base["wacc"]["wacc"] <= 0.09},
    "dcf_vs_comps": {"dcf_pence": B, "comps_median_pence": primary["implied_value"], "comps_low_pence": primary["low"],
                     "comps_high_pence": primary["high"],
                     "gap": B / primary["implied_value"] - 1,                       # gap = DCF / comps - 1
                     "comps_ex_KMB_pence": comps_out["legs"]["ev_ebitda_ltm_ex_KMB"]["value_per_share_pence"]["implied_value"],
                     "comps_underlying_ebitda_pence": comps_out["legs"]["ev_ebitda_ltm_all_7_x_underlying_ebitda"]["value_per_share_pence"]["implied_value"]}}

# ================= (a) Foods consideration: received at closing vs today's value =================
closing = date(2027, 6, 30)            # "expected mid-2027" (brief; data notes FLAG 7)
run_date = date(2026, 10, 14)
t_close = (closing - run_date).days / 365   # years from the run date to closing
usd_per_eur = mkt["fred"]["USD_per_EUR"]
cash_eur = 15_700 / usd_per_eur        # USD 15.7bn cash consideration in EUR m (FRED rate, as inputs.yaml)
shares_eur = v0["disposal_proceeds"] - cash_eur
kd = v0["pre_tax_cost_of_debt"]        # Bund + single-A spread: a fair rate for a contractual cash claim on McCormick
wacc0 = base["wacc"]["wacc"]
timing = {"years_run_date_to_closing": t_close, "closing_assumed": str(closing),
          "consideration_today_meur": v0["disposal_proceeds"], "cash_part_meur": cash_eur, "mccormick_shares_part_meur": shares_eur}
for label, x, rate in [("all_at_cost_of_equity", v0["disposal_proceeds"], KE0),
                       ("all_at_wacc", v0["disposal_proceeds"], wacc0),
                       ("cash_only_at_cost_of_debt", cash_eur, kd)]:
    p = pv(x, rate, t_close)
    timing[label] = {"rate": rate, "present_value_meur": p, "reduction_meur": x - p, "reduction_pence": pence(x - p)}
timing["note"] = ("Today's market value of the McCormick shares already is the present value of receiving them at closing, "
                  "less any McCormick dividends paid before closing (not in the data folder: MISSING). So the cash-only line "
                  "is the most defensible size; the cost-of-equity line is an upper bound.")
timing["per_1pt_of_discount_rate_pence"] = pence(v0["disposal_proceeds"] - pv(v0["disposal_proceeds"], 0.01, t_close))
timing["foods_interim_cash_flows"] = ("MISSING (inputs.yaml foods_perimeter_interim_cash_flows_meur: null). Data agent "
                                      "indicator only: about EUR 2.9bn (about 113p) before capex and working capital, if "
                                      "the economics to closing belong to Unilever. Offsets the timing reduction above.")

# ================= roll-forward of run-date market values (FLAG 1 of the first run: RESOLVED, commit 3414aec) ==========
# The engine now grows only the balance-sheet-date part of equity at Ke; the Foods consideration and the TMICC stake
# (priced at 13 Oct 2026) are added back ungrown. Check that the input equals those two items and that the engine's
# equity equals the hand-built roll-forward.
PRICED = v0["priced_at_valuation_date_meur"]
run_date_items = v0["disposal_proceeds"] + TMICC
eq_check = dcf.roll_forward(base["equity"]["equity_value_balance_sheet_date"], KE0, t_roll,
                            v0["dividends_ex_before_valuation_meur"], v0["buybacks_after_balance_sheet_meur"], run_date_items)
roll_flag = {"status": "RESOLVED in desk/ (commit 3414aec, mistakes log row 24)",
             "priced_at_valuation_date_meur_input": PRICED, "foods_plus_tmicc_recomputed_meur": run_date_items,
             "input_matches": abs(PRICED - run_date_items) < 0.1,
             "engine_equity_meur": base["equity"]["equity_value"], "hand_built_equity_meur": eq_check,
             "previous_engine_value_pence": 4101.434719926086, "change_pence": B - 4101.434719926086}
assert roll_flag["input_matches"] and abs(eq_check - base["equity"]["equity_value"]) < 1.0

# ================= (b) tax on the Foods cash: each EUR 1bn =================
v_tax = copy.deepcopy(v0)
v_tax["restructuring_cash"] = v0["restructuring_cash"] + 1000.0   # scratch only: EUR 1bn more debt-like cash out
tax = {"per_eur_1bn_pence_today": pence(1000.0),
       "per_eur_1bn_pence_through_engine_bridge": B - ps(run(v_tax)),
       "per_eur_1bn_pence_paid_at_closing_pv_at_cost_of_debt": pence(pv(1000.0, kd, t_close)),
       "bear_25pct_of_cash_meur": 0.25 * cash_eur, "bear_25pct_of_cash_pence_today": pence(0.25 * cash_eur),
       "note": "39p is the right size for a tax known today. The engine line is higher because a bridge line entered "
               "as a 31 Dec 2025 amount is grown at Ke for 0.786 years; a tax figure known today should be added to "
               "priced_at_valuation_date as well, which gives the 39p."}

# ================= (c) beta sensitivity (JV value recomputed at each cost of equity) =================
betas = {"bottom_up_base": v0["beta"], "own_5y_weekly": 0.54, "own_5y_monthly": 0.91}
beta_sens = {}
for k, b in betas.items():
    vb = with_beta(b)
    r = run(vb)
    v_nojv = copy.deepcopy(v0)
    v_nojv["beta"] = b
    beta_sens[k] = {"beta": b, "jv_value_meur": jv_value(dcf.cost_of_equity(v0["risk_free"], b, ERP), G0),
                    "associates_meur": vb["associates"], **summary(r),
                    "value_if_jv_not_recomputed_pence": ps(run(v_nojv))}

# ================= (d) where the value per share comes from =================
# The engine: equity today = (equity at 31 Dec - items priced today) x (1 + Ke)^t + items priced today - dividends
# - buybacks. Each balance-sheet-date item is grown at Ke; the Foods consideration and TMICC (priced today) are not.
f = grow(1.0, KE0, t_roll)
mi = base["equity"]["minorities_deducted"]
parts_meur = {
    "dcf_remaining_business_ev": d["enterprise_value"] * f,
    "less_minorities_proportionate": -mi * f,
    "less_net_debt_31dec2025": -v0["net_debt"] * f,
    "less_restructuring_cash": -v0["restructuring_cash"] * f,
    "foods_consideration": v0["disposal_proceeds"],
    "tmicc_stake": PRICED - v0["disposal_proceeds"],   # the input's TMICC figure (1,935.2, rounded), not grown
    "joint_ventures_gordon": JV0 * f,
    "other_associates_investments_magnum_balance": (ASSOC_EX_JV - (PRICED - v0["disposal_proceeds"])) * f,
    "less_dividends_ex_since_31dec": -v0["dividends_ex_before_valuation_meur"],
    "less_buybacks_since_31dec": -v0["buybacks_after_balance_sheet_meur"]}
parts_p = {k: pence(x) for k, x in parts_meur.items()}
assert abs(sum(parts_p.values()) - B) < 1e-6
dcf_net = parts_p["dcf_remaining_business_ev"] + parts_p["less_minorities_proportionate"]
non_op = parts_p["foods_consideration"] + parts_p["tmicc_stake"] + parts_p["joint_ventures_gordon"] + parts_p["other_associates_investments_magnum_balance"]
claims = parts_p["less_net_debt_31dec2025"] + parts_p["less_restructuring_cash"] + parts_p["less_dividends_ex_since_31dec"] + parts_p["less_buybacks_since_31dec"]
decomp = {"pence": parts_p, "subtotals_pence": {
    "dcf_remaining_business_after_minorities": dcf_net, "foods_consideration": parts_p["foods_consideration"],
    "other_non_operating_assets": non_op - parts_p["foods_consideration"], "all_non_operating_assets": non_op,
    "net_debt_restructuring_dividends_buybacks": claims, "total_value_per_share": B},
    "share_of_value_per_share": {"dcf_remaining_business_after_minorities": dcf_net / B,
                                 "foods_consideration": parts_p["foods_consideration"] / B,
                                 "other_non_operating_assets": (non_op - parts_p["foods_consideration"]) / B,
                                 "net_debt_and_cash_paid_out": claims / B},
    "growth_factor_at_ke_for_31dec_items": f}

# ================= (e) SELL/HOLD/BUY flip points (one variable at a time) =================
def solve(fn, lo, hi, target, tol=1e-9):
    """Bisection: the parameter at which value per share = target (value assumed monotonic in the parameter)."""
    flo, fhi = fn(lo) - target, fn(hi) - target
    if flo * fhi > 0:
        return None
    for _ in range(200):
        mid = (lo + hi) / 2
        fm = fn(mid) - target
        if abs(hi - lo) < tol:
            break
        if fm * flo > 0:
            lo, flo = mid, fm
        else:
            hi = mid
    return (lo + hi) / 2


def by_beta(b):
    return ps(run(with_beta(b)))


def by_wacc_shift(s):
    return ps(run(wacc_shift=s))


def by_tg(g):
    b = copy.deepcopy(brief0)
    b["dcf"]["terminal_growth"] = g
    v = copy.deepcopy(v0)
    v["associates"] = ASSOC_EX_JV + jv_value(KE0, g)   # PM's JV formula uses the same long-run growth
    return ps(run(v, b))


def by_lr_growth(g):   # FY27-30 growth AND terminal growth together (decision 6 ties them), JV consistent
    b = copy.deepcopy(brief0)
    b["dcf"]["organic_growth"] = [brief0["dcf"]["organic_growth"][0]] + [g] * 4
    b["dcf"]["terminal_growth"] = g
    v = copy.deepcopy(v0)
    v["associates"] = ASSOC_EX_JV + jv_value(KE0, g)
    return ps(run(v, b))


def by_margin(mg):
    v = copy.deepcopy(v0)
    v["base_margin"] = mg
    return ps(run(v))


def by_mkc_price(px):  # McCormick share price (USD) -> Foods consideration at today's value
    v = copy.deepcopy(v0)
    v["disposal_proceeds"] = (15_700 + 499.691175 * px) / usd_per_eur
    v["priced_at_valuation_date_meur"] = v["disposal_proceeds"] + TMICC   # still priced today, so not grown
    return ps(run(v))


w0 = base["wacc"]["wacc"]
flips = {}
for label, fn, lo, hi, now in [("beta_jv_consistent", by_beta, 0.2, 1.2, v0["beta"]),
                               ("wacc_shift_added_to_wacc", by_wacc_shift, -0.03, 0.02, 0.0),
                               ("terminal_growth", by_tg, 0.0, 0.04, G0),
                               ("long_run_growth_fy27_30_and_terminal", by_lr_growth, 0.0, 0.04, G0),
                               ("base_margin", by_margin, 0.12, 0.30, v0["base_margin"]),
                               ("mkc_share_price_usd", by_mkc_price, 1.0, 150.0, mkt["MKC"]["close"])]:
    out = {"base_value": now}
    for name, tgt in (("sell_to_hold", hold_floor), ("hold_to_buy", buy_floor)):
        x = solve(fn, lo, hi, tgt)
        out[name] = {"parameter": x, "value_check_pence": fn(x) if x is not None else None,
                     "status": "found" if x is not None else f"not reached in [{lo}, {hi}]"}
        if label.startswith("wacc") and x is not None:
            out[name]["wacc_level"] = w0 + x
    flips[label] = out
# extra non-operating value (or less tax/claims) needed, in today's euros
flips["extra_value_today_meur"] = {
    "sell_to_hold": (hold_floor - B) / pence(1.0), "hold_to_buy": (buy_floor - B) / pence(1.0),
    "note": "EUR m of value at today's date needed to reach each threshold (each EUR 1bn = 39.3p)."}

# ================= sensitivity grid centred on the brief's 1.6% terminal growth (JV held at base, as the engine) ======
waccs = [w0 + s for s in (-0.01, -0.005, 0.0, 0.005, 0.01)]
growths = [G0 - 0.005, G0, G0 + 0.005]
grid_ev = dcf.sensitivity(base["inputs"], waccs, growths, brief0["dcf"]["terminal_ronic"])
bb = dcf.Bridge(**base["bridge"])
grid = [[dcf.equity_bridge(ev, bb, shares, fx, base["roll"], "EUR")["per_share_gbp_pence"] for ev in row] for row in grid_ev]
assert abs(grid[2][1] - B) < 1e-6

# bear case: the engine shifts WACC +1 pt but leaves the JV value at the base cost of equity
bear = run(growth=brief0["scenarios"]["bear"]["organic_growth"], wacc_shift=brief0["scenarios"]["bear"]["wacc_shift"])
jv_bear = jv_value(KE0 + brief0["scenarios"]["bear"]["wacc_shift"], G0)
bear_note = {"bear_value_pence": ps(bear), "jv_value_if_ke_plus_1pt_meur": jv_bear,
             "jv_reduction_pence_today": pence(JV0 - jv_bear),
             "note": "If the bear's +1 pt applies to the cost of equity too, the JV value falls; the engine does not do this."}

out = {"units": "value per share in pence (GBp) unless labelled; money in EUR m",
       "base_value_pence_recheck": B, "price_pence": price,
       "rating_thresholds_pence": {"hold_if_at_least": hold_floor, "buy_if_at_least": buy_floor},
       "checks": checks, "a_foods_consideration_timing": timing, "roll_forward_of_run_date_values_flag": roll_flag,
       "b_tax_on_foods_cash": tax, "c_beta_sensitivity": beta_sens, "d_value_decomposition": decomp,
       "e_flip_points": flips,
       "sensitivity_grid_centred_pence": {"wacc": waccs, "terminal_growth": growths, "grid": grid,
                                          "note": "valuation.json's grid is now centred on 1.6% too (commit 3414aec; growth 1.1-2.6%); this copy is the same centre."},
       "bear_jv_consistency": bear_note}
(HERE / "sanity_checks.json").write_text(json.dumps(out, indent=2, default=float))
print(json.dumps(out, indent=1, default=float))
