"""Valuation agent sanity checks and rating-flip thresholds, all computed with desk.valuation_run.build.

Run from repo root: PYTHONPATH=. python3 runs/DGE/2026-10-12/valuation/run_sanity.py
Writes sanity_checks.json. Nothing here changes a PM assumption: each threshold moves ONE input in a copy of the
brief/inputs to find where the engine's rating changes (what-if only).
"""
import copy
import json
from pathlib import Path

import yaml

from desk import units, valuation_run as vr
from desk.rating import rating

HERE = Path(__file__).resolve().parent
RUN = HERE.parent
brief = yaml.safe_load(Path("briefs/DGE.yaml").read_text())
v, s = vr.load_inputs(str(RUN / "inputs.yaml"), vr.extra_required(brief))
vr.apply_brief_rules(brief, v, s)
res = json.loads((HERE / "valuation.json").read_text())
comps = json.loads((HERE / "comps.json").read_text())
base = vr.build(brief, v)
price = v["share_price_gbp_pence"]
# Rating lines in pence (GBp): SELL at or below price x (1 - 10%), BUY at or above price x (1 + 15%)
sell_line = price * (1 - brief["rating"]["sell_if_downside_at_least"])
buy_line = price * (1 + brief["rating"]["buy_if_upside_at_least"])


def pence(brief_=None, v_=None, **kw):
    return vr.build(brief_ or brief, v_ or v, **kw)["equity"]["per_share_gbp_pence"]


def solve(f, lo, hi, target, tol=1e-7):
    """Bisection: the input x in [lo, hi] at which value f(x) (pence) equals target (pence)."""
    flo = f(lo) - target
    if (f(hi) - target) * flo > 0:
        return None  # no crossing in the range searched
    for _ in range(200):
        mid = (lo + hi) / 2
        fm = f(mid) - target
        if abs(hi - lo) < tol:
            break
        if fm * flo > 0:
            lo, flo = mid, fm
        else:
            hi = mid
    return (lo + hi) / 2


def with_v(key, x):
    vv = dict(v); vv[key] = x; return vv


def with_brief(path, x):
    b = copy.deepcopy(brief); d = b
    for k in path[:-1]:
        d = d[k]
    d[path[-1]] = x
    return b


thr = {
    "sell_line_pence": sell_line, "buy_line_pence": buy_line,
    "base_value_pence": base["equity"]["per_share_gbp_pence"],
    "pence_above_sell_line": base["equity"]["per_share_gbp_pence"] - sell_line,
    # Cost of equity (CAPM) rises with beta, which lowers the value
    "sell_if_beta_above": solve(lambda x: pence(v_=with_v("beta", x)), 0.5, 1.5, sell_line),
    "buy_if_beta_below": solve(lambda x: pence(v_=with_v("beta", x)), 0.3, 1.5, buy_line),
    # WACC shift applied to the whole discount rate (as in the sensitivity grid)
    "sell_if_wacc_above": base["inputs"].wacc + solve(lambda x: pence(wacc_shift=x), -0.02, 0.02, sell_line),
    "buy_if_wacc_below": base["inputs"].wacc + solve(lambda x: pence(wacc_shift=x), -0.03, 0.02, buy_line),
    # Share of the c.USD 1bn savings that reaches operating profit
    "sell_if_flow_through_below": solve(lambda x: pence(flow_through=x), 0.0, 1.0, sell_line),
    # Return on new invested capital in the terminal year (sets terminal capex)
    "sell_if_terminal_ronic_below": solve(lambda x: pence(brief_=with_brief(["dcf", "terminal_ronic"], x)), 0.07, 0.30, sell_line),
    # Outside shareholders' share of operating profit (proportionate minorities)
    "sell_if_minority_share_above": solve(lambda x: pence(v_=with_v("minority_share_of_operating_profit", x)), 0.0, 0.2, sell_line),
}
thr["terminal_capex_pct_at_sell_ronic"] = vr.build(with_brief(["dcf", "terminal_ronic"], thr["sell_if_terminal_ronic_below"]), v)["inputs"].terminal_capex_pct_sales
# Book-method comparison (the method used until the PM decision of 2026-10-13)
book = vr.build(with_brief(["dcf", "bridge", "minorities_method"], "book"), v)
thr["book_method_value_pence"] = book["equity"]["per_share_gbp_pence"]
thr["book_method_rating"] = book["rating"]["rating"]

# Market-implied EV (USD m): market cap + net debt + minorities - associates - disposal proceeds, with minorities on the
# same proportionate basis (share x EV), so EV = (market cap + net debt - associates - disposals) / (1 - share)
mcap = v["shares_outstanding_m"] * units.pence_to_pounds(price) * v["fx_usd_per_gbp"]  # market capitalisation, USD m
share = v["minority_share_of_operating_profit"]
mkt_ev = (mcap + v["net_debt"] - v["associates"] - v["disposal_proceeds"]) / (1 - share)
ebitda_ex_assoc = 6650.0 - 218.0  # FY26 adjusted EBITDA less associates' share (20-F p.186), USD m; still includes EABL
w_shift = solve(lambda x: pence(wacc_shift=x), -0.03, 0.02, price)
dcf_px = res["base"]["equity"]["per_share_gbp_pence"]
comps_px = comps["implied_value_per_share_pence"]["implied_value"]

out = {
    "tv_share_of_ev": res["base"]["tv_share_of_ev"],
    "tv_flag_above_75pct": res["base"]["tv_share_of_ev"] > 0.75,
    "implied_exit_ev_ebitda": res["base"]["implied_exit_ev_ebitda"],
    "peer_ev_ebitda_range": None,
    "peer_ev_ebitda_note": "peer EV/EBITDA unavailable (peers.csv); compared with Diageo's own market multiple instead",
    "market_ev_to_fy26_adj_ebitda_ex_associates": mkt_ev / ebitda_ex_assoc,
    "market_implied_ev_musd": mkt_ev,
    "market_implied_minorities_musd": share * mkt_ev,
    "market_cap_musd": mcap,
    "wacc": res["base"]["wacc"]["wacc_used"],
    "wacc_within_6_to_9pct": 0.06 <= res["base"]["wacc"]["wacc_used"] <= 0.09,
    "market_implied_wacc_at_g_2pct": base["inputs"].wacc + w_shift,
    "minorities_method": "proportionate",
    "minorities_deducted_musd": res["base"]["equity"]["minorities_deducted"],
    "minorities_book_musd": v["minority_interests"],
    "dcf_value_pence": dcf_px,
    "comps_value_pence": comps_px,
    "dcf_vs_comps": dcf_px / comps_px - 1,
    "rating_thresholds": thr,
    "note": ("market EV = market cap + net debt + minorities (proportionate: 2.566% of EV) - associates - disposal proceeds; "
             "adj. EBITDA 6,650 less associates 218 (20-F p.186). Approximate: EBITDA still includes EABL. Market-implied "
             "WACC and all thresholds solved with desk.valuation_run.build (one input moved at a time)."),
}
(HERE / "sanity_checks.json").write_text(json.dumps(out, indent=2))
print(json.dumps(out, indent=1))
