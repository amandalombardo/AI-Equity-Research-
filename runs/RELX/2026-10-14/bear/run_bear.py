"""Bear case agent (RELX, run 2026-10-14): every value impact comes from re-running desk.valuation_run.

For each test the script copies briefs/RELX.yaml and ../inputs.yaml into bear/scratch/<test>/, changes ONE assumption
(or a stated stack of them), and runs
    python -m desk.valuation_run <scratch brief> <scratch inputs> <scratch out>
exactly as the Valuation agent did. The value per share (pence, GBp) is read back from that run's valuation.json.
The brief and the run's inputs.yaml are never edited. Money in GBP m; values per share in pence (GBp).
Run from the repo root:  PYTHONPATH=. python runs/RELX/2026-10-14/bear/run_bear.py

Re-run 15 Oct 2026 (evidence audit, docs/audit-2026-10-15/RELX.md): the brief now has ERP 4.2% (Damodaran implied, PM
decision 15 Oct 2026) and bear_agent_margin 32.4% (PM bear responses, decision 14). Everything below reads those from the
brief. Added: the audit stress lines (ERP 5.0% Kroll, ERP 5.5% Fernandez survey, gilt 5.30% press, gilt 5.21% = US 10y)
and the stacked bear at the old 5.0% ERP. The 14 Oct results are kept in bear/scratch/bear_results_erp5_2026-10-14.json.

Downloaded evidence (SEC companyfacts, past results releases, FRED series) sits in bear/scratch/downloads/ and is
read as data only.
"""
import copy
import json
import subprocess
import sys
from pathlib import Path

import yaml

from desk import dcf, valuation_run

HERE = Path(__file__).resolve().parent
RUN = HERE.parent
ROOT = RUN.parents[2]
SCRATCH = HERE / "scratch"
DL = SCRATCH / "downloads"
BRIEF0 = yaml.safe_load((ROOT / "briefs" / "RELX.yaml").read_text())
INP0 = yaml.safe_load((RUN / "inputs.yaml").read_text())
V = {k: (x["value"] if isinstance(x, dict) else x) for k, x in INP0.items()}
RISK = json.loads((RUN / "risk" / "risk.json").read_text())
SAN = json.loads((RUN / "valuation" / "sanity_checks.json").read_text())

PRICE = V["share_price_gbp_pence"]                                        # 2,771p, REL.L close 13 Oct 2026
HOLD_FLOOR = PRICE * (1 - BRIEF0["rating"]["sell_if_downside_at_least"])   # value (p) where SELL turns HOLD
BUY_FLOOR = PRICE * (1 + BRIEF0["rating"]["buy_if_upside_at_least"])      # value (p) where HOLD turns BUY
ERP = BRIEF0["dcf"]["wacc"]["equity_risk_premium"]                         # 4.2% (Damodaran implied, PM 15 Oct 2026)
BEAR_MARGIN = BRIEF0["scenarios"]["bear"]["bear_agent_margin"]            # 32.4% (PM bear responses, 15 Oct 2026)


def fred_last(series, date="2026-10-13"):
    """Value of a FRED series on the price date, from the CSV downloaded to bear/scratch/downloads (percent)."""
    for line in (DL / f"{series}.csv").read_text().splitlines()[1:]:
        d, v = line.split(",")
        if d == date and v:
            return float(v) / 100
    raise SystemExit(f"FRED {series} has no value on {date}: MISSING, stop")


# ---------------- sourced figures used by the tests (each with its document) ----------------
# FY23 margin WITHOUT print, RELX's own restatement (AR25 note 1 p.145): group revenue 9,161 and adj. OP 3,030
# (AR25 p.186), print revenue 586 and print adj. OP 253 (AR25 p.145; Fundamentals FLAG 1, ratios.csv)
FY23_REV, FY23_AOP, FY23_PRINT_REV, FY23_PRINT_AOP = 9161.0, 3030.0, 586.0, 253.0
MARGIN_FY23_EX_PRINT = (FY23_AOP - FY23_PRINT_AOP) / (FY23_REV - FY23_PRINT_REV)   # operating margin = profit / revenue
assert abs(round(MARGIN_FY23_EX_PRINT, 3) - BEAR_MARGIN) < 1e-9, "brief bear margin should be FY23 ex print"
MARGIN_OLD_LABEL = 0.331       # the brief's bear margin until 15 Oct 2026: FY23 GROUP incl. print (AR25 p.186)
# Audit stress lines (docs/audit-2026-10-15/erp-evidence.md section 2b-2c; RELX.md finding V1). All secondhand except FRED.
ERP_KROLL = 0.050              # Kroll recommended US ERP, effective 2 Sep 2025, reaffirmed 2026 (pairs with the 20y UST)
ERP_FERNANDEZ = 0.055          # Fernandez et al. 2025 survey, US 5.5% (UK 5.4%), SSRN 5260463
RF_PRESS = 0.0530              # press reports of the 10y gilt at about 5.30-5.35% in mid-Sep 2026 (audit V1)
# Acquisition cash spend FY21-25, SEC XBRL ifrs-full:CashFlowsUsedInObtainingControlOfSubsidiariesOrOtherBusinesses...
# (20-F accessions 0001558370-24-001468 (FY21 as re-presented), 0001558370-25-001178 (FY22), 0001104659-26-017277 (FY23-25))
ACQ = {2021: 254.0, 2022: 394.0, 2023: 124.0, 2024: 170.0, 2025: 260.0}
REV = {2021: 7244.0, 2022: 8553.0, 2023: 9161.0, 2024: 9434.0, 2025: 9590.0}        # AR25 p.186 five-year summary
ACQ_PCT_POOLED = sum(ACQ.values()) / sum(REV.values())        # acquisitions as % of revenue, FY21-25 pooled
ACQ_PCT_SIMPLE = sum(ACQ[y] / REV[y] for y in ACQ) / len(ACQ)  # simple average of the yearly ratios
ACQ_PCT_BRIEF = 0.027                                          # brief comment: FY21-25 average, SEC XBRL
# Segment revenue FY25 (FY25R p.4, p.26) and H1 2026 underlying growth (H126 p.3-8): the AI case halves STM and Legal
SEG_REV = {"Risk": 3485.0, "STM": 2714.0, "Legal": 1806.0, "Exhibitions": 1186.0}
SEG_G = {"Risk": 0.08, "STM": 0.06, "Legal": 0.10, "Exhibitions": 0.06}
# Market data on the price date (FRED, downloaded 15 Oct 2026; bear/scratch/downloads)
US10Y = fred_last("DGS10")          # US 10-year Treasury, 5.21%
US_BE = fred_last("T10YIE")         # US 10-year breakeven inflation, 2.33% on 13 Oct (2.35% on 14 Oct)
US_REAL = fred_last("DFII10")       # US 10-year TIPS real yield, 2.88%
BBB = fred_last("BAMLC0A4CBBB")     # ICE BofA BBB spread, 1.03%
# Betas (risk/risk.json; risk/notes.md)
REG = RISK["own_regressions_vs_ftse100"]
PEERS = [p["beta"] for p in RISK["peer_betas_5y_monthly_home_index"].values() if not p.get("optional")]
PEER_MEDIAN = sorted(PEERS)[len(PEERS) // 2]                   # median of the 7 core peers (odd count)
BETA_DAMO_5Y = 1.195           # Damodaran 2020-24 average cash-corrected unlevered 1.0729 relevered (risk/notes.md)
BETA_JUN26 = 0.994             # Damodaran 0.8737 relevered at 30 Jun 2026 net debt ex leases 8,614 (risk/notes.md)
DEBT_W_JUN26 = 0.1513          # 8,614 / (8,614 + 48,319.4) (data/notes.md FLAG 5)
RF_FRED_AUG = 0.049886         # FRED IRLTLT01GBM156N Aug 2026 monthly average (riskfree evidence option C)
RF_BBG = 0.0539                # Bloomberg early-trading 13 Oct 2026 (riskfree evidence option B)
RONIC_BOOK = 0.251             # ROIC on book capital employed FY25 (ronic evidence option B)
MARGIN_H1_GROUP = 0.355        # H1 2026 group adjusted margin incl. print (margin evidence option C; H126 p.1)
MARGIN_STEP = 0.009                 # record +0.9 pt a year (margin evidence file; AR25 p.186), used only for a labelled judgement
GROWTH_UNDERLYING = 0.07       # RELX underlying growth FY24, FY25, H1 2026 (growth evidence option C)


def setv(inp, key, value, why):
    """Change one input in a scratch copy and record why in its source (the loader needs a source for every key)."""
    inp[key] = {"value": float(value), "source": f"BEAR SCRATCH (bear/run_bear.py): {why}. Base value was {V.get(key)}; "
                                                f"base source: {INP0[key]['source'] if key in INP0 else 'n/a'}"}


def run(name, change_inputs=None, change_brief=None):
    """Write scratch copies, apply the change, run desk.valuation_run, return base and bear results in pence."""
    d = SCRATCH / name
    d.mkdir(parents=True, exist_ok=True)
    b, i = copy.deepcopy(BRIEF0), copy.deepcopy(INP0)
    if change_brief:
        change_brief(b)
    if change_inputs:
        change_inputs(i)
    (d / "brief.yaml").write_text(yaml.safe_dump(b, sort_keys=False, width=160))
    (d / "inputs.yaml").write_text(yaml.safe_dump(i, sort_keys=False, width=160, allow_unicode=True))
    subprocess.run([sys.executable, "-m", "desk.valuation_run", str(d / "brief.yaml"), str(d / "inputs.yaml"),
                    str(d / "out")], cwd=ROOT, check=True, capture_output=True)
    out = json.loads((d / "out" / "valuation.json").read_text())
    res = {}
    for case in ("base", "bear"):
        e, r = out[case]["equity"], out[case]["rating"]
        res[case] = {"value_pence": e["per_share_gbp_pence"], "rating": r["rating"], "upside": r["upside"],
                     "ev_mgbp": out[case]["enterprise_value_mgbp"], "wacc_used": out[case]["wacc"]["wacc_used"],
                     "tv_share_of_ev": out[case]["tv_share_of_ev"],
                     "implied_exit_ev_ebitda": out[case]["implied_exit_ev_ebitda"]}
    return res


results = {}
control = run("00_control")
BASE, BEAR = control["base"]["value_pence"], control["bear"]["value_pence"]
VAL = json.loads((RUN / "valuation" / "valuation.json").read_text())   # the Valuation agent's run
assert abs(BASE - VAL["base"]["equity"]["per_share_gbp_pence"]) < 1e-6 and \
    abs(BEAR - VAL["bear"]["equity"]["per_share_gbp_pence"]) < 1e-6, "scratch copy must reproduce the run"
WACC0 = control["base"]["wacc_used"]


def record(key, label, res, case="base", ref=None, side="bear", evidence=""):
    ref = BASE if ref is None else ref
    r = res[case]
    results[key] = {"side": side, "label": label, "case_read": case, "value_pence": r["value_pence"],
                    "impact_vs_reference_pence": r["value_pence"] - ref, "reference_pence": ref,
                    "rating": r["rating"], "upside": r["upside"], "wacc_used": r["wacc_used"],
                    "ev_mgbp": r["ev_mgbp"], "implied_exit_ev_ebitda": r["implied_exit_ev_ebitda"],
                    "reaches_hold": r["value_pence"] >= HOLD_FLOOR, "evidence": evidence}


# brief edits
def g_all(rate):
    return lambda b: b["dcf"].__setitem__("organic_growth", [rate] * 5)


def g_fy27_30(rate):
    return lambda b: b["dcf"].__setitem__("organic_growth", [b["dcf"]["organic_growth"][0]] + [rate] * 4)


def tg(rate):
    return lambda b: b["dcf"].__setitem__("terminal_growth", rate)


def ronic(rate):
    return lambda b: b["dcf"].__setitem__("terminal_ronic", rate)


def spread(s):
    return lambda b: b["dcf"]["wacc"].__setitem__("credit_spread", s)


def chain(*fs):
    def f(x):
        for fn in fs:
            fn(x)
    return f


# input edits
def margin(m, why):
    return lambda i: setv(i, "base_margin", m, why)


def tax(t):
    return lambda i: setv(i, "tax_rate", t, "brief bear line: weighted statutory rate 25.0% (AR25 p.159)")


def acquisitions(pct):
    # Acquisitions treated as extra capital spending in the forecast years (cash out, growth unchanged = no revenue
    # credited). The terminal year is NOT changed: its reinvestment comes from RONIC, and RELX's 15.4% ROIC already
    # counts acquisitions at cost, so adding them again forever would double count.
    return lambda i: setv(i, "capex_pct_sales", V["capex_pct_sales"] + pct,
                          f"brief bear line: capex 7.10% + acquisitions {pct:.2%} of revenue (FY21-25, SEC XBRL)")


def beta(bv, why):
    return lambda i: setv(i, "beta", bv, why)


def rf(r, why):
    return lambda i: setv(i, "risk_free", r, why)


# ======================= BEAR LINES, ONE AT A TIME (vs base 1,621p) =======================
record("b_growth_3", "Growth 3.0% every year (brief bear growth), WACC unchanged", run("b_growth_3", change_brief=g_all(0.03)),
       evidence="brief scenarios.bear; growth evidence 'AI pressure halves Legal and STM growth'")
record("b_margin_331", "Margin 33.1% (old brief label until 15 Oct 2026, FY23 GROUP incl. print)",
       run("b_margin_331", margin(MARGIN_OLD_LABEL, "old bear_agent_margin, FY23 group incl. print")), evidence="AR25 p.186")
record("b_margin_324", f"Margin {BEAR_MARGIN:.1%} (brief bear_agent_margin: FY23 WITHOUT print, like-for-like with the 35.0% base)",
       run("b_margin_324", margin(round(MARGIN_FY23_EX_PRINT, 5), "FY23 ex print (3,030-253)/(9,161-586), AR25 p.145, p.186")),
       evidence="AR25 p.145 note 1 restatement; Fundamentals FLAG 1; mistakes log row 26")
record("b_tax_25", "Tax 25.0% (weighted statutory)", run("b_tax_25", tax(0.25)), evidence="AR25 p.159")
record("b_tg_15", "Terminal growth 1.5%", run("b_tg_15", change_brief=tg(0.015)), evidence="terminal growth evidence, bear")
record("b_ronic_wacc", f"Terminal RONIC = WACC ({WACC0:.3%})", run("b_ronic_wacc", change_brief=ronic(round(WACC0, 6))),
       evidence="ronic evidence, bear")
record("b_acq_27", f"Acquisitions {ACQ_PCT_BRIEF:.1%} of revenue, FY26-30", run("b_acq_27", acquisitions(ACQ_PCT_BRIEF)),
       evidence="SEC XBRL CashFlowsUsedInObtainingControl FY21-25")
record("b_bbb", f"Cost of debt at the BBB spread ({BBB:.2%})", run("b_bbb", change_brief=spread(BBB)),
       evidence="FRED BAMLC0A4CBBB 13 Oct 2026; Fitch BBB+ (FWP25)")
# ---- audit stress lines (15 Oct 2026): sourced alternatives to the 4.2% ERP and the 5.45% gilt ----
def erp(e):
    return lambda b: b["dcf"]["wacc"].__setitem__("equity_risk_premium", e)


record("a_erp_kroll", "ERP 5.0% (Kroll recommended US ERP; the desk's old figure)", run("a_erp_kroll", change_brief=erp(ERP_KROLL)),
       evidence="erp-evidence.md 2b (secondhand: Kroll Jan 2026 executive summary; BVWire)")
record("a_erp_fernandez", "ERP 5.5% (Fernandez 2025 survey, US; UK 5.4%)", run("a_erp_fernandez", change_brief=erp(ERP_FERNANDEZ)),
       evidence="erp-evidence.md 2c (secondhand: SSRN 5260463)")
record("a_rf_press", "Gilt 5.30% (press, mid-Sep 2026)", run("a_rf_press", rf(RF_PRESS, "audit V1: press 5.30-5.35% mid-Sep 2026")),
       side="generous", evidence="docs/audit-2026-10-15/RELX.md V1 (secondhand)")
record("a_rf_us10y", f"Gilt {US10Y:.2%} (US 10y on 13 Oct, FRED DGS10, as a proxy)",
       run("a_rf_us10y", rf(US10Y, "audit V1: US 10y FRED DGS10 13 Oct 2026")), side="generous", evidence="FRED DGS10")
record("a_erp_kroll_bbb", "ERP 5.0% (Kroll) + BBB spread 1.03%", run("a_erp_kroll_bbb", change_brief=chain(erp(ERP_KROLL), spread(BBB))),
       evidence="Kroll + FRED BAMLC0A4CBBB")

# engine bear (growth 3% + WACC +1 pt), as the Valuation agent ran it
results["b_engine_bear"] = {"side": "bear", "label": "Engine bear: growth 3% + WACC +1 pt", "value_pence": BEAR,
                            "impact_vs_reference_pence": BEAR - BASE, "reference_pence": BASE,
                            "rating": control["bear"]["rating"], "upside": control["bear"]["upside"],
                            "reaches_hold": False, "evidence": "valuation/valuation.json"}

# Risk agent: beta at the Damodaran 5-year average; leverage after the 2026 buybacks (beta and debt weight at June 2026)
record("b_beta_damo5y", f"Beta {BETA_DAMO_5Y} (Damodaran 2020-24 average, relevered)",
       run("b_beta_damo5y", beta(BETA_DAMO_5Y, "risk/notes.md sensitivity: Damodaran 2020-24 average 1.0729 relevered")),
       evidence="risk/notes.md")


def jun26(i):
    setv(i, "beta", BETA_JUN26, "risk/notes.md: 0.8737 relevered at 30 Jun 2026 net debt ex leases 8,614")
    setv(i, "debt_weight", DEBT_W_JUN26, "data/notes.md FLAG 5: 8,614 / (8,614 + 48,319.4)")


record("b_leverage_jun26", "Leverage after buybacks: beta 0.994 and debt weight 15.1% (30 Jun 2026 net debt)",
       run("b_leverage_jun26", jun26), evidence="H126 p.11; risk/notes.md; data/notes.md")
record("b_leverage_jun26_bbb", "Leverage after buybacks + BBB spread", run("b_leverage_jun26_bbb", jun26, spread(BBB)),
       evidence="as above + FRED BAMLC0A4CBBB")

# ======================= AI-DISRUPTION CASE (Legal and STM pricing) =======================
w = sum(SEG_REV.values())
mix_now = sum(SEG_REV[s] * SEG_G[s] for s in SEG_REV) / w                         # revenue-weighted underlying growth
mix_ai = sum(SEG_REV[s] * SEG_G[s] * (0.5 if s in ("STM", "Legal") else 1.0) for s in SEG_REV) / w
AI_DRAG = mix_now - mix_ai                                                          # points of group growth lost
results["ai_inputs"] = {"weighted_underlying_now": mix_now, "weighted_underlying_ai": mix_ai, "growth_drag": AI_DRAG,
                        "base_fy27_30": 0.05, "implied_fy27_30": 0.05 - AI_DRAG,
                        "stm_legal_share_of_revenue_ex_print": (SEG_REV["STM"] + SEG_REV["Legal"]) / w}
ai_brief = chain(g_all(0.03), tg(0.015))
record("ai_case", f"AI case: growth 3%, margin {BEAR_MARGIN:.1%} (FY23 ex print), terminal growth 1.5%, base WACC",
       run("ai_case", margin(round(MARGIN_FY23_EX_PRINT, 5), "AI case: FY23 ex-print margin"), ai_brief),
       evidence="H126 p.15-16 principal risks (AI, IP circumvention 'may impact demand for and pricing'); 3 Feb 2026 -14.4%")

# ======================= VOLATILITY / DRAWDOWN (price risk, from risk.json; not a DCF value) =======================
vol1y = RISK["volatility_annualised"]["relx_1y_daily"]
dd = RISK["max_drawdown_5y_gbp_pence"]["max_drawdown"]
results["price_risk"] = {"vol_1y": vol1y, "one_sd_down_1y_pence": PRICE * (1 - vol1y),   # price after a 1 s.d. fall
                         "repeat_max_drawdown_pence": PRICE * (1 + dd),                    # price after a repeat of -51.3%
                         "max_drawdown": dd, "low_close_pence": RISK["max_drawdown_5y_gbp_pence"]["trough_price"]}

# ======================= STACKED BEAR =======================
def bear_wacc(tax_rate, credit_spread, erp_used=ERP):
    """WACC the engine bear uses: desk.dcf.wacc at the changed tax and spread, plus the brief's +1 point shift."""
    return dcf.wacc(dcf.WaccInputs(V["risk_free"], erp_used, V["beta"], V["risk_free"] + credit_spread, tax_rate,
                                   V["debt_weight"]))["wacc"] + BRIEF0["scenarios"]["bear"]["wacc_shift"]


W_STACK = bear_wacc(0.25, BBB)


def stack(m, with_ai_terminal=True, erp_used=None):
    w_ronic = W_STACK if erp_used is None else bear_wacc(0.25, BBB, erp_used)
    def fb(b):
        tg(0.015)(b)
        ronic(round(w_ronic, 6))(b)
        spread(BBB)(b)
        if erp_used is not None:
            erp(erp_used)(b)
    def fi(i):
        margin(m, "stacked bear margin")(i)
        tax(0.25)(i)
        acquisitions(ACQ_PCT_BRIEF)(i)
    return fi, fb


fi, fb = stack(round(MARGIN_FY23_EX_PRINT, 5))
s324 = run("s_stack_324", fi, fb)
record("s_stack_324", "STACK: engine bear (3% growth, WACC +1) + margin 32.4% + tax 25% + g 1.5% + RONIC = WACC + "
       "acquisitions 2.7% + BBB", s324, case="bear")
fi, fb = stack(0.331)
s331 = run("s_stack_331", fi, fb)
record("s_stack_331", "STACK as above with the old 33.1% margin label", s331, case="bear")
fi, fb = stack(round(MARGIN_FY23_EX_PRINT, 5), erp_used=ERP_KROLL)
record("s_stack_324_erp50", "STACK (margin 32.4%) at the Kroll 5.0% ERP (reproduces the 14 Oct stack)",
       run("s_stack_324_erp50", fi, fb), case="bear")
fi, fb = stack(round(MARGIN_FY23_EX_PRINT, 5), erp_used=ERP_FERNANDEZ)
record("s_stack_324_erp55", "STACK (margin 32.4%) at the Fernandez 5.5% ERP", run("s_stack_324_erp55", fi, fb), case="bear")
# the stack without the +1 point WACC shift (only the cash-flow and terminal lines): read the 'bear' run's base side is
# not right because growth differs, so run the stack with growth 3% inside the base case
fi, fb = stack(round(MARGIN_FY23_EX_PRINT, 5))
W_NOSHIFT = W_STACK - BRIEF0["scenarios"]["bear"]["wacc_shift"]
s_noshift = run("s_stack_324_no_wacc_shift", fi,
                chain(fb, g_all(0.03), ronic(round(W_NOSHIFT, 6))))
record("s_stack_324_no_shift", "STACK without the +1 pt WACC shift (growth 3% in the base case, RONIC = that WACC)", s_noshift)
results["stack_inputs"] = {"erp": ERP, "bear_margin_brief": BEAR_MARGIN, "wacc_stack_bear": W_STACK,
                           "wacc_stack_bear_erp50": bear_wacc(0.25, BBB, ERP_KROLL),
                           "wacc_stack_bear_erp55": bear_wacc(0.25, BBB, ERP_FERNANDEZ), "wacc_stack_no_shift": W_NOSHIFT,
                           "margin_fy23_ex_print": MARGIN_FY23_EX_PRINT, "acq_pct_brief": ACQ_PCT_BRIEF,
                           "acq_pct_pooled": ACQ_PCT_POOLED, "acq_pct_simple": ACQ_PCT_SIMPLE, "bbb_spread": BBB}

# ======================= CHALLENGES AGAINST THE SELL (generous side) =======================
for key, bv, why in [("g_beta_peer", PEER_MEDIAN, "raw peer median, 7 core peers (risk.json)"),
                     ("g_beta_5yw", REG["5y_weekly"]["beta"], "own 5y weekly vs FTSE 100, R2 0.12"),
                     ("g_beta_blume", RISK["blume_adjusted_5y_monthly"], "Blume-adjusted 5y monthly"),
                     ("g_beta_5ym", REG["5y_monthly"]["beta"], "own 5y monthly vs FTSE 100, R2 0.04")]:
    record(key, f"Beta {bv:.2f} ({why})", run(key, beta(round(bv, 4), why)), side="generous", evidence="risk/risk.json")

record("g_rf_fred_aug", "Risk-free 4.99% (FRED Aug 2026 monthly average; stale)",
       run("g_rf_fred_aug", rf(RF_FRED_AUG, "riskfree evidence option C")), side="generous", evidence="FRED IRLTLT01GBM156N")
record("g_rf_bbg", "Risk-free 5.39% (Bloomberg early 13 Oct)", run("g_rf_bbg", rf(RF_BBG, "riskfree evidence option B")),
       side="generous", evidence="riskfree evidence")

# Fisher: (1 + nominal) = (1 + real) x (1 + inflation)
REAL_IN_GILT = (1 + V["risk_free"]) / (1 + BRIEF0["dcf"]["terminal_growth"]) - 1   # real rate the base case implies
US_REAL_FISHER = (1 + US10Y) / (1 + US_BE) - 1                                      # US real from nominal and breakeven
GILT_IMPLIED_INFL = (1 + V["risk_free"]) / (1 + US_REAL) - 1                         # UK inflation if UK real = US TIPS real
RF_AT_2PCT = (1 + US_REAL) * (1 + BRIEF0["dcf"]["terminal_growth"]) - 1               # gilt consistent with 2% inflation
results["fisher"] = {"gilt": V["risk_free"], "terminal_growth": BRIEF0["dcf"]["terminal_growth"],
                     "real_rate_implied_by_base": REAL_IN_GILT, "us10y": US10Y, "us_breakeven": US_BE, "us_tips_real": US_REAL,
                     "us_real_by_fisher": US_REAL_FISHER, "gilt_implied_inflation_if_uk_real_eq_us_real": GILT_IMPLIED_INFL,
                     "gilt_consistent_with_2pct_inflation_at_us_real": RF_AT_2PCT,
                     "uk_breakeven": "MISSING: Bank of England and DMO blocked (proxy 403); not on FRED"}
record("g_tg_us_be", f"Terminal growth {US_BE:.2%} (US 10y breakeven, FRED T10YIE 13 Oct)",
       run("g_tg_us_be", change_brief=tg(round(US_BE, 4))), side="generous", evidence="FRED T10YIE")
record("g_tg_gilt_infl", f"Terminal growth {GILT_IMPLIED_INFL:.2%} (inflation inside the 5.45% gilt if UK real = US TIPS 2.88%)",
       run("g_tg_gilt_infl", change_brief=tg(round(GILT_IMPLIED_INFL, 4))), side="generous",
       evidence="FRED DFII10 + gilt 5.45%; ASSUMPTION UK real = US real")
record("g_rf_fisher", f"Risk-free {RF_AT_2PCT:.2%} (US TIPS real 2.88% + 2.0% inflation: the rate consistent with g = 2%)",
       run("g_rf_fisher", rf(round(RF_AT_2PCT, 6), "Fisher: US 10y TIPS real (FRED DFII10) x 2% inflation")), side="generous",
       evidence="FRED DFII10; ASSUMPTION UK real = US real")
record("g_tg_3", "Terminal growth 3.0% (option C, no direct source)", run("g_tg_3", change_brief=tg(0.03)), side="generous",
       evidence="terminal growth evidence option C (unsourced)")
record("g_ronic_book", "Terminal RONIC 25.1% (book ROIC)", run("g_ronic_book", change_brief=ronic(RONIC_BOOK)), side="generous",
       evidence="ronic evidence option B; FY25R p.13-14")
record("g_margin_355", "Margin 35.5% (H1 2026 group incl. print)", run("g_margin_355", margin(MARGIN_H1_GROUP, "margin option C")),
       side="generous", evidence="H126 p.1")
M_TREND = round(0.35 + 4 * MARGIN_STEP, 4)   # FY30 margin if the FY21-25 +0.9 pt/yr continued for FY27-30 (judgement)
record("g_margin_trend", f"Margin {M_TREND:.1%} from FY26 (FY21-25 trend carried to FY30; JUDGEMENT, overstates)",
       run("g_margin_trend", margin(M_TREND, "trend +0.9 pt/yr x 4 on 35.0%; not a source")), side="generous",
       evidence="AR25 p.186 record; not a forecast")
record("g_growth_7", "Growth 7% FY27-30 (underlying, option C)", run("g_growth_7", change_brief=g_fy27_30(GROWTH_UNDERLYING)),
       side="generous", evidence="growth evidence option C; FY25R p.3")


# market-implied WACC and the beta it needs (desk.dcf.wacc, solved by bisection)
def wacc_at_beta(bv):
    return dcf.wacc(dcf.WaccInputs(V["risk_free"], ERP, bv, V["risk_free"] + BRIEF0["dcf"]["wacc"]["credit_spread"],
                                   V["tax_rate"], V["debt_weight"]))["wacc"]


W_MKT = SAN["flip_points"]["market_implied_wacc"]["wacc"]   # WACC at which the DCF = 2,771p (Valuation agent)
lo, hi = 0.0, 1.0
for _ in range(60):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if wacc_at_beta(mid) < W_MKT else (lo, mid)
BETA_MKT = (lo + hi) / 2
results["market_implied"] = {"wacc": W_MKT, "beta_needed_at_gilt_5_45": BETA_MKT, "erp": ERP,
                             "flip_points": {k: SAN["flip_points"][k]["sell_to_hold"]["parameter"]
                                             for k in ("wacc_shift_added_to_wacc", "beta", "base_margin", "risk_free_gilt",
                                                       "equity_risk_premium", "terminal_growth", "growth_fy27_30")}}

# terminal growth that gives the lowest peer exit multiple (WKL 11.1x) at the base WACC (engine in-process)
v_in, s_in = valuation_run.load_inputs(str(RUN / "inputs.yaml"), valuation_run.extra_required(BRIEF0))
valuation_run.apply_brief_rules(BRIEF0, v_in, s_in)


def exit_at(g):
    b = copy.deepcopy(BRIEF0)
    b["dcf"]["terminal_growth"] = g
    return valuation_run.build(b, v_in)["dcf"]["implied_exit_ev_ebitda"]


PEER_LOW = SAN["checks"]["implied_exit_ev_ebitda"]["peer_low"]
lo, hi = 0.02, 0.09
for _ in range(60):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if exit_at(mid) < PEER_LOW else (lo, mid)
G_EXIT = (lo + hi) / 2
record("g_exit_wkl", f"Terminal growth {G_EXIT:.2%} = what the {WACC0:.2%} WACC needs for an 11.1x exit (WKL, lowest peer)",
       run("g_exit_wkl", change_brief=tg(round(G_EXIT, 6))), side="generous", evidence="sanity_checks.json peer_low; diagnostic")

# ======================= STACKED GENEROUS =======================
def gen_stack(bv):
    fi = chain(beta(round(bv, 4), "stack"), rf(RF_FRED_AUG, "stack"), margin(MARGIN_H1_GROUP, "stack"))
    fb = chain(tg(round(US_BE, 4)), ronic(RONIC_BOOK), g_fy27_30(GROWTH_UNDERLYING))
    return fi, fb


fi, fb = gen_stack(PEER_MEDIAN)
record("gs_peer_beta", "GENEROUS STACK: beta 0.75 + gilt 4.99% + g 2.33% + RONIC 25.1% + margin 35.5% + growth 7%",
       run("gs_peer_beta", fi, fb), side="generous")
fi, fb = gen_stack(REG["5y_weekly"]["beta"])
record("gs_5yw_beta", "GENEROUS STACK with own 5y weekly beta 0.66", run("gs_5yw_beta", fi, fb), side="generous")
fi, fb = gen_stack(REG["5y_monthly"]["beta"])
record("gs_5ym_beta", "GENEROUS STACK with own 5y monthly beta 0.38", run("gs_5ym_beta", fi, fb), side="generous")
# the same stack WITHOUT any beta change (only cash-flow and rate inputs)
fi = chain(rf(RF_FRED_AUG, "stack"), margin(MARGIN_H1_GROUP, "stack"))
fb = chain(tg(round(US_BE, 4)), ronic(RONIC_BOOK), g_fy27_30(GROWTH_UNDERLYING))
record("gs_no_beta", "GENEROUS STACK, beta kept at 0.973", run("gs_no_beta", fi, fb), side="generous")

# stricter generous stacks: drop the stale August gilt (rejected for Unilever, decision 11) and/or the 7% growth (which
# leaves out print run-off and disposals, so it overstates the revenue valued)
def strict(bv, growth7):
    fi = chain(beta(round(bv, 4), "stack"), margin(MARGIN_H1_GROUP, "stack"))
    fb = chain(tg(round(US_BE, 4)), ronic(RONIC_BOOK), *([g_fy27_30(GROWTH_UNDERLYING)] if growth7 else []))
    return fi, fb


fi, fb = strict(PEER_MEDIAN, True)
record("gs_strict_peer_g7", "GENEROUS STACK, gilt kept at 5.45%: beta 0.75 + g 2.33% + RONIC 25.1% + margin 35.5% + growth 7%",
       run("gs_strict_peer_g7", fi, fb), side="generous")
fi, fb = strict(PEER_MEDIAN, False)
record("gs_strict_peer_g5", "GENEROUS STACK, gilt 5.45% and growth 5%: beta 0.75 + g 2.33% + RONIC 25.1% + margin 35.5%",
       run("gs_strict_peer_g5", fi, fb), side="generous")
fi, fb = strict(REG["5y_weekly"]["beta"], False)
record("gs_strict_5yw_g5", "GENEROUS STACK, gilt 5.45% and growth 5%, beta 0.66 (own 5y weekly)",
       run("gs_strict_5yw_g5", fi, fb), side="generous")

out = {"rerun": "15 Oct 2026 (evidence audit): ERP 4.2%, bear margin 32.4%; 14 Oct results in scratch/bear_results_erp5_2026-10-14.json",
       "erp": ERP, "bear_agent_margin": BEAR_MARGIN, "base_pence": BASE, "engine_bear_pence": BEAR, "share_price_pence": PRICE, "hold_floor_pence": HOLD_FLOOR,
       "buy_floor_pence": BUY_FLOOR, "wacc_base": WACC0, "results": results}
(HERE / "bear_results.json").write_text(json.dumps(out, indent=2, default=float))
for k, r in results.items():
    if "value_pence" in r:
        print(f"{k:24s} {r['value_pence']:8.1f}p  impact {r['impact_vs_reference_pence']:+8.1f}p  {r['rating']:4s} "
              f"{r['upside']:+.1%}  | {r['label']}")
print(json.dumps({k: v for k, v in results.items() if k in ('ai_inputs', 'price_risk', 'stack_inputs', 'fisher',
                                                           'market_implied')}, indent=1, default=float))
