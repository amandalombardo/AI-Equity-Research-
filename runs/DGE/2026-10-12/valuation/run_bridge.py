"""Step-by-step bridge from 1,448p to the Phase 3 value, one change at a time, using desk.valuation_run.build.

Steps 0-5 use book minorities (the method in force before the PM decision of 2026-10-13) so the history reproduces;
step 6 switches to the brief's proportionate method. The minorities figure is read from the engine result
(equity.minorities_deducted), never hard-coded."""
# Run from repo root: PYTHONPATH=. python3 runs/DGE/2026-10-12/valuation/run_bridge.py
# The old terminal year (last forecast UFCF x (1+g)) is reproduced only to measure step 1; it reproduces 1,448p exactly.
import copy, json, yaml
from pathlib import Path
from desk import dcf, valuation_run as vr

brief0 = yaml.safe_load(Path("briefs/DGE.yaml").read_text())
v, s = vr.load_inputs("runs/DGE/2026-10-12/inputs.yaml", vr.ROLL_FORWARD + vr.PROPORTIONATE)
vr.apply_brief_rules(brief0, v, s)
new_tv = dcf.terminal_year

def old_tv(inp, last):  # Gordon growth on the OLD (pre-Phase-3) terminal cash flow: last forecast-year UFCF x (1+g)
    t = new_tv(inp, last); t["ufcf"] = last["ufcf"] * (1 + inp.terminal_growth); return t

def run(fix_tv, ronic, ft, basis, restr, mino="proportionate"):
    b = copy.deepcopy(brief0); d = b["dcf"]
    d["bridge"]["minorities_method"] = mino  # book (PM rule until 2026-10-13) or proportionate (current brief)
    d["terminal_ronic"] = ronic; d["savings"]["flow_through"] = ft; d["valuation_basis"] = basis
    vv = dict(v); vv["restructuring_cash"] = restr
    dcf.terminal_year = new_tv if fix_tv else old_tv
    try:
        r = vr.build(b, vv)
    finally:
        dcf.terminal_year = new_tv
    return r
steps = [("Previous run (old terminal year, capex 7.1%, flow-through 50%, stub, no restructuring)", (False, None, 0.50, "stub", 0.0, "book")),
         ("1. Terminal-year fix (steady state, NWC at g)", (True, None, 0.50, "stub", 0.0, "book")),
         ("2. Terminal capex from RONIC 13.4%", (True, 0.134, 0.50, "stub", 0.0, "book")),
         ("3. Flow-through 46%", (True, 0.134, 0.46, "stub", 0.0, "book")),
         ("4. Value at 30 June + roll forward at Ke", (True, 0.134, 0.46, "balance_sheet_date", 0.0, "book")),
         ("5. Restructuring cash 850 deducted", (True, 0.134, 0.46, "balance_sheet_date", 850.0, "book")),
         ("6. Minorities: book 2,083 -> proportionate (PM decision 2026-10-13)", (True, 0.134, 0.46, "balance_sheet_date", 850.0, "proportionate"))]
prev = None; out = []
for name, a in steps:
    r = run(*a); p = r["equity"]["per_share_gbp_pence"]
    out.append({"step": name, "pence": p, "change_pence": None if prev is None else p - prev,
                "ev_musd": r["dcf"]["enterprise_value"], "tv_share": r["dcf"]["tv_share_of_ev"],
                "term_capex_pct": r["inputs"].terminal_capex_pct_sales,
                "minorities_deducted_musd": r["equity"]["minorities_deducted"]})
    prev = p
for o in out: print(o)
# one-at-a-time from the old base (order-independent check)
base_args = steps[0][1]; p0 = out[0]["pence"]
for i, name in enumerate(["tv_fix", "ronic", "ft", "basis", "restr", "minorities"]):
    a = list(base_args); a[i] = steps[-1][1][i]
    if i == 1: a[0] = True  # ronic only meaningful with new terminal year
    print("isolated", name, run(*a)["equity"]["per_share_gbp_pence"] - p0)
# break-evens with final setup
for ft in (0.40, 0.42, 0.44):
    print("ft", ft, run(True, 0.134, ft, "balance_sheet_date", 850.0)["equity"]["per_share_gbp_pence"])
for ro in (0.108, 0.12, 0.15, 0.184):
    r = run(True, ro, 0.46, "balance_sheet_date", 850.0)
    print("ronic", ro, r["equity"]["per_share_gbp_pence"], r["inputs"].terminal_capex_pct_sales)
Path("runs/DGE/2026-10-12/valuation/bridge.json").write_text(json.dumps(out, indent=1))
