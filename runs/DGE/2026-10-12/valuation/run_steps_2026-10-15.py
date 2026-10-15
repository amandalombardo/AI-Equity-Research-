"""Valuation agent, 15 Oct 2026 (final): step table from the 13 Oct value (1,627.3p) to the final base, one change at a
time with desk.valuation_run.build, plus ERP rating-flip points. Nothing in the brief or inputs.yaml is changed: each
step overrides an in-memory copy.
Run from repo root: PYTHONPATH=. python3 runs/DGE/2026-10-12/valuation/run_steps_2026-10-15.py  (writes steps_2026-10-15.json)
"""
import copy, json
from pathlib import Path
import yaml
from desk import valuation_run as vr

HERE = Path(__file__).resolve().parent
brief = yaml.safe_load(Path("briefs/DGE.yaml").read_text())
v, s = vr.load_inputs(str(HERE.parent / "inputs.yaml"), vr.extra_required(brief))
vr.apply_brief_rules(brief, v, s)
price = v["share_price_gbp_pence"]
sell_line = price * (1 - brief["rating"]["sell_if_downside_at_least"])  # SELL at or below price x (1 - 10%), pence
buy_line = price * (1 + brief["rating"]["buy_if_upside_at_least"])      # BUY at or above price x (1 + 15%), pence


def value(erp, shares, dw, growth, beta=None):
    """Value per share (pence, GBp) with the ERP, share count, debt weight, growth path and beta set as given."""
    b = copy.deepcopy(brief)
    b["dcf"]["wacc"]["equity_risk_premium"] = erp
    b["dcf"]["organic_growth"] = growth
    vv = dict(v, shares_outstanding_m=shares, debt_weight=dw, beta=v["beta"] if beta is None else beta)
    r = vr.build(b, vv)
    return r["equity"]["per_share_gbp_pence"], r["wacc"]["wacc_used"], r["rating"]["rating"]


B_OLD = 0.9601  # beta used until the source check of 15 Oct 2026 (from a rounded industry beta of 0.73)
g_old = brief["dcf"]["organic_growth"][:3] + [0.03, 0.03]   # FY30-31 at 3.0% (brief before the PM decision of 15 Oct)
g_new = brief["dcf"]["organic_growth"]                       # FY30-31 at 2.0% (brief now)
steps = [("13 Oct value (ERP 5.0%, 2,222m shares, debt weight 0.29395, FY30-31 growth 3.0%)", (0.050, 2222.0, 0.29395, g_old, B_OLD)),
         ("1. ERP 5.0% -> 4.2% (PM decision 15 Oct 2026)", (0.042, 2222.0, 0.29395, g_old, B_OLD)),
         ("2. Shares 2,222m -> 2,224m basic, debt weight 0.29376 (audit finding 8)", (0.042, 2224.0, 0.29376, g_old, B_OLD)),
         ("3. Shares 2,224m -> 2,231m diluted, debt weight 0.29311 (PM decision 15 Oct, D3)", (0.042, 2231.0, 0.29311, g_old, B_OLD)),
         ("4. FY30-31 growth 3.0% -> 2.0% (PM decision 15 Oct, D4)", (0.042, 2231.0, 0.29311, g_new, B_OLD)),
         ("5. Beta 0.9601 -> 0.9526: Damodaran's exact 0.7250, not a rounded 0.73 (source check 15 Oct, mistakes row 33)",
          (0.042, 2231.0, 0.29311, g_new))]
out, prev = [], None
for name, a in steps:
    p, w, rt = value(*a)
    out.append({"step": name, "pence": p, "change_pence": None if prev is None else p - prev, "wacc": w, "rating": rt})
    prev = p


def solve(fn, lo, hi):
    """Bisection: the ERP at which value per share crosses a rating line."""
    flo = fn(lo)
    for _ in range(100):
        mid = (lo + hi) / 2
        if (fn(mid) > 0) == (flo > 0):
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


final = steps[-1][1]
erp = lambda e: value(e, *final[1:])[0]
res = {"steps": out, "final_pence": out[-1]["pence"],
       "sell_if_erp_above": solve(lambda e: erp(e) - sell_line, 0.042, 0.08),
       "buy_if_erp_below": solve(lambda e: erp(e) - buy_line, 0.02, 0.042),
       "market_implied_erp": solve(lambda e: erp(e) - price, 0.03, 0.07),   # ERP at which the DCF value equals the price
       "value_at_erp_5pct_pence": erp(0.05), "value_at_erp_5_5pct_pence": erp(0.055),
       "sell_line_pence": sell_line, "buy_line_pence": buy_line,
       # total change since 13 Oct, and since the morning re-run of 15 Oct (after step 2), pence per share
       "total_change_since_13_oct_pence": out[-1]["pence"] - out[0]["pence"],
       "change_since_morning_rerun_pence": out[-1]["pence"] - out[2]["pence"],
       # upside vs price at the alternative ERPs (DCF value / price - 1)
       "upside_at_erp_5pct": erp(0.05) / price - 1, "upside_at_erp_5_5pct": erp(0.055) / price - 1}
(HERE / "steps_2026-10-15.json").write_text(json.dumps(res, indent=1))
print(json.dumps(res, indent=1))
