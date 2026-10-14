"""Bear case agent (ULVR, run 2026-10-14): every value impact comes from re-running desk.valuation_run.

For each test the script copies briefs/ULVR.yaml and ../inputs.yaml into bear/scratch/<test>/, changes ONE thing (one
assumption, plus any input that must move with it for consistency, each stated in the source text), and runs
    python -m desk.valuation_run <scratch brief> <scratch inputs> <scratch out>
exactly as the Valuation agent did. The value per share (pence, GBp) is read back from that run's valuation.json.
The brief and the run's inputs.yaml are never edited. Money in EUR m unless labelled; values per share in pence (GBp).
Run from the repo root:  PYTHONPATH=. python runs/ULVR/2026-10-14/bear/run_bear.py
"""
import copy
import json
import math
import subprocess
import sys
from pathlib import Path

import pandas as pd
import yaml

from desk import dcf, risk

HERE = Path(__file__).resolve().parent
RUN = HERE.parent
ROOT = RUN.parents[2]
SCRATCH = HERE / "scratch"
BRIEF0 = yaml.safe_load((ROOT / "briefs" / "ULVR.yaml").read_text())
INP0 = yaml.safe_load((RUN / "inputs.yaml").read_text())
MKT = json.loads((RUN / "data" / "market_data.json").read_text())
V = {k: (x["value"] if isinstance(x, dict) else x) for k, x in INP0.items()}

ERP, G0 = BRIEF0["dcf"]["wacc"]["equity_risk_premium"], BRIEF0["dcf"]["terminal_growth"]
USD_PER_EUR = MKT["fred"]["USD_per_EUR"]                      # FRED DEXUSEU 9 Oct 2026, as inputs.yaml
PRICE = V["share_price_gbp_pence"]
HOLD_FLOOR = PRICE * (1 - BRIEF0["rating"]["sell_if_downside_at_least"])   # value (p) where SELL turns HOLD
BUY_FLOOR = PRICE * (1 + BRIEF0["rating"]["buy_if_upside_at_least"])      # value (p) where HOLD turns BUY

# ---------------- sourced figures used by the tests (each with its document) ----------------
JV_DIV = 229.0             # FY25 dividends received from JVs, 20-F note 11 p.158 (apply_pm_decision10.py)
GROUP_SALES = 50503.0      # FY25 turnover, FY25 results 6-K 0001654954-26-001155 / 20-F XBRL Revenue
GROUP_UOP = 10084.0        # FY25 underlying operating profit, same 6-K
RESTR = [(425, 51680), (710, 52479), (599, 50503)]   # FY23-25 restructuring / turnover, 20-F XBRL (margin evidence pack)
FOODS_CASH_USD = 15700.0   # USD m cash consideration (Form 425; McCormick 10-Q note 2)
MKC_NEW_SHARES_M = 499.691175   # new McCormick shares to Unilever + its holders (inputs.yaml disposal_proceeds source)
MKC_PRICE = MKT["MKC"]["close"]  # USD 44.64, Yahoo MKC close 13 Oct 2026
MKC_DEAL_REF = 57.84       # USD, one-month average behind the USD 44.8bn headline (brief section 3, item 3)
BREAK_FEE_USD = 420.0      # USD m, McCormick 10-Q to 31 Aug 2026 (0000063754-26-000329) note 2 'Pending Merger':
                           # 'A termination fee of $420 million ... may be payable by us to Unilever ... under specified circumstances'
TAX_STRESS = 0.25          # brief decision 5: 25% of the cash (UK main corporation tax rate, gov.uk), a labelled stress
HUL_OUTSIDE_MEUR = 15507.0 # 38.1% of HUL market value EUR 40,700.7m (inputs.yaml hul_market_value_meur source)
HUL_BOOK_NCI = 1569.0      # HUL non-controlling interest at book, 20-F note 15B p.162-163
NCI_BOOK = V["minority_interests"]   # 2,057 all minorities at book, 20-F p.131
NCI_GROUP_SHARE = 587.0 / 7403.0     # FY24 minorities' share of Group underlying net profit (Fundamentals notes; 20-F p.128, p.42, p.43)
HUL_SHARE_OF_NCI = 446.0 / 587.0     # HUL minorities' profit / all minorities' underlying profit, FY24 (20-F note 15B; Fundamentals notes)
AVG_IC = 39502.0           # FY25 average invested capital, FY25 results 6-K ROIC reconciliation / 20-F p.45
FOODS_GOODWILL = 7900.0    # Foods goodwill EUR 7.9bn of 17.7bn, 20-F p.153 (Fundamentals FLAG 7)
PERIM_SALES, PERIM_UOP = 10700.0, 2600.0   # Form 425 investor presentation slide 25
BETA_DAMO_5Y = 0.9998      # Damodaran 2020-24 average cash-corrected 0.8752 relevered at D/E 0.1924 (risk/notes.md)
BETA_OWN_WEEKLY = 0.54     # ULVR.L vs FTSE 100, 5y weekly (risk/notes.md, risk.json)
DATA_G_LOW = 0.011         # low end of Data agent's 1.1-1.6% euro market-growth reading (data/notes.md section 5)


def ke(beta):
    """Cost of equity (CAPM): risk-free + beta x equity risk premium (desk.dcf.cost_of_equity)."""
    return dcf.cost_of_equity(V["risk_free"], beta, ERP)


def jv_value(k, g):
    """Joint ventures by Gordon growth (PM decision 10, data/apply_pm_decision10.py): 229 x (1 + g) / (Ke - g)."""
    return JV_DIV * (1 + g) / (k - g)


JV0 = jv_value(ke(V["beta"]), G0)
ASSOC_EX_JV = V["associates"] - JV0      # TMICC + associates at book + other investments + Magnum balance


def setv(inp, key, value, why):
    """Change one input in a scratch copy and record why in its source (the loader needs a source for every key)."""
    inp[key] = {"value": float(value), "source": f"BEAR SCRATCH (bear/run_bear.py): {why}. Base value was {V.get(key)}; "
                                          f"base source: {INP0[key]['source'] if key in INP0 else 'n/a'}"}


def run(name, change_inputs=None, change_brief=None):
    """Write scratch copies, apply the change, run desk.valuation_run, return base and bear values in pence."""
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
                     "ev_meur": out[case]["enterprise_value_meur"], "wacc_used": out[case]["wacc"]["wacc_used"],
                     "minorities_deducted_meur": e["minorities_deducted"], "tv_share_of_ev": out[case]["tv_share_of_ev"]}
    return res


results = {}
control = run("00_control")
BASE, BEAR = control["base"]["value_pence"], control["bear"]["value_pence"]
VAL = json.loads((RUN / "valuation" / "valuation.json").read_text())   # the Valuation agent's current run
assert abs(BASE - VAL["base"]["equity"]["per_share_gbp_pence"]) < 1e-6 and \
    abs(BEAR - VAL["bear"]["equity"]["per_share_gbp_pence"]) < 1e-6, "scratch copy must reproduce the run"
# the JV inside the current associates must be the Gordon value at the current cost of equity (PM decision 11)
assert abs(JV0 + ASSOC_EX_JV - V["associates"]) < 1e-9 and abs(ASSOC_EX_JV - 3352.3) < 0.2, "associates must = JV at current Ke + 3,352.3"


def record(key, label, res, case="base", ref=None, notes=""):
    ref = BASE if ref is None else ref
    v = res[case]["value_pence"]
    results[key] = {"label": label, "case_read": case, "value_pence": v, "impact_vs_reference_pence": v - ref,
                    "reference_pence": ref, "rating": res[case]["rating"], "upside": res[case]["upside"],
                    "ev_meur": res[case]["ev_meur"], "minorities_deducted_meur": res[case]["minorities_deducted_meur"],
                    "notes": notes}


# ======================= REQUIRED TEST 1: the Foods deal FAILS, Foods stays in the DCF =======================
restr_avg = sum(r / s for r, s in RESTR) / len(RESTR)          # FY23-25 average restructuring % of turnover (1.12%)
group_margin = GROUP_UOP / GROUP_SALES - restr_avg               # whole-group underlying margin less recurring restructuring
TMICC_TODAY = V["priced_at_valuation_date_meur"] - V["disposal_proceeds"]   # TMICC stake at today's price (1,935.2)


def deal_fails(fee_usd=0.0, keep_stranded=False):
    def f(i):
        setv(i, "base_sales", GROUP_SALES, "deal fails: whole-group FY25 turnover 50,503 (FY25 results 6-K)")
        setv(i, "base_margin", round(group_margin, 5), f"deal fails: group underlying margin {GROUP_UOP/GROUP_SALES:.4%} "
             f"(10,084/50,503) less FY23-25 average restructuring {restr_avg:.4%} (margin evidence pack, same rule as decision 3)")
        fee_eur = fee_usd / USD_PER_EUR                           # break fee converted at FRED USD per EUR
        setv(i, "disposal_proceeds", round(fee_eur, 1), "deal fails: no consideration" +
             (f"; McCormick termination fee USD {fee_usd:.0f}m (McCormick 10-Q 0000063754-26-000329 note 2) / {USD_PER_EUR}"
              if fee_usd else "; no break fee (payable only 'under specified circumstances')"))
        setv(i, "priced_at_valuation_date_meur", round(TMICC_TODAY + fee_eur, 1),
             "deal fails: only the TMICC stake (and any fee) is priced today")
        if not keep_stranded:
            setv(i, "restructuring_cash", 0.0, "deal fails: no stranded-cost restructuring (Form 425 slide 19 ties it to the sale)")
        setv(i, "minority_share_of_operating_profit", round(NCI_GROUP_SHARE, 5),
             "deal fails: Group ratio 587/7,403 without the x10,084/7,484 ex-perimeter uplift (Fundamentals notes)")
    return f


record("t1_deal_fails", "Deal fails: Foods stays in the DCF (no fee, no stranded-cost restructuring)", run("t1_deal_fails", deal_fails()))
record("t1b_deal_fails_with_fee", "Deal fails, McCormick pays the USD 420m termination fee", run("t1b_deal_fails_fee", deal_fails(BREAK_FEE_USD)))
record("t1c_deal_fails_keep_500", "Deal fails, EUR 500m restructuring still spent", run("t1c_deal_fails_keep500", deal_fails(0.0, True)))
results["t1_inputs"] = {"group_margin_used": group_margin, "restructuring_avg_fy23_25": restr_avg,
                        "minority_share_group": NCI_GROUP_SHARE, "break_fee_meur": BREAK_FEE_USD / USD_PER_EUR,
                        "growth": "unchanged (0.5%, then 1.6%): flatters this case, the perimeter's FY25 USG was 2.7% vs 3.5% Group"}

# ======================= REQUIRED TEST 2: tax at 25% of the USD 15.7bn cash, priced today =======================
cash_eur = FOODS_CASH_USD / USD_PER_EUR                          # USD 15.7bn in EUR at FRED 1.1193
tax_eur = TAX_STRESS * cash_eur                                  # 25% stress on the cash consideration


def tax(i):
    setv(i, "restructuring_cash", V["restructuring_cash"] + round(tax_eur, 1),
         f"tax stress {TAX_STRESS:.0%} x USD 15.7bn / {USD_PER_EUR} = EUR {tax_eur:,.1f}m added to the debt-like line (brief decision 5)")
    setv(i, "priced_at_valuation_date_meur", round(V["priced_at_valuation_date_meur"] - tax_eur, 1),
         "tax is a today amount: netted in the items not grown by the roll-forward (Valuation notes (b))")


record("t2_tax_25pct", f"Tax 25% of the cash = EUR {tax_eur:,.0f}m, priced today", run("t2_tax", tax))
results["t2_inputs"] = {"cash_meur": cash_eur, "tax_meur": tax_eur}

# ======================= REQUIRED TEST 3: minorities at 38.1% of HUL's market value =======================
def hul_market(i):
    setv(i, "minority_interests", HUL_OUTSIDE_MEUR + (NCI_BOOK - HUL_BOOK_NCI),
         "HUL outside 38.1% at market EUR 15,507m + other minorities at book (2,057 - 1,569) (minorities evidence pack)")
    setv(i, "priced_at_valuation_date_meur", round(V["priced_at_valuation_date_meur"] - HUL_OUTSIDE_MEUR, 1),
         "HUL market value is a 13 Oct 2026 price: netted in the items not grown")


def method_book(b):
    b["dcf"]["bridge"]["minorities_method"] = "book"


record("t3_hul_market", "Minorities: 38.1% of HUL at market + others at book", run("t3_hul_market", hul_market, method_book))

others_share = V["minority_share_of_operating_profit"] * (1 - HUL_SHARE_OF_NCI)   # non-HUL minorities' share of EV


def hul_market_others_prop(i):
    setv(i, "minority_share_of_operating_profit", round(others_share, 5),
         "non-HUL minorities only: 10.684% x (1 - 446/587)")
    setv(i, "restructuring_cash", V["restructuring_cash"] + HUL_OUTSIDE_MEUR,
         "HUL outside 38.1% at market EUR 15,507m carried on the debt-like line (scratch only)")
    setv(i, "priced_at_valuation_date_meur", round(V["priced_at_valuation_date_meur"] - HUL_OUTSIDE_MEUR, 1),
         "HUL market value is priced today")


record("t3b_hul_market_others_prop", "HUL at market + other minorities proportionate", run("t3b_hul_mkt_others_prop", hul_market_others_prop))

# ======================= REQUIRED TEST 4: margin 16.2% =======================
record("t4_margin_162", "Operating margin 16.2% (brief bear_agent_margin)",
       run("t4_margin", lambda i: setv(i, "base_margin", BRIEF0["scenarios"]["bear"]["bear_agent_margin"],
                                        "brief scenarios.bear.bear_agent_margin (c.17.3% 2023 less 1.1%)")))

# ======================= REQUIRED TEST 5: engine bear with the JVs re-valued at Ke + 1 point =======================
k_bear = ke(V["beta"]) + BRIEF0["scenarios"]["bear"]["wacc_shift"]
jv_bear = jv_value(k_bear, G0)


def jv_at(kk, g):
    return lambda i: setv(i, "associates", round(ASSOC_EX_JV + jv_value(kk, g), 1),
                          f"JVs by Gordon growth at Ke {kk:.4%} and g {g:.1%} = {jv_value(kk, g):,.1f} (apply_pm_decision10.py formula)")


t5 = run("t5_bear_jv", jv_at(k_bear, G0))
record("t5_engine_bear_jv", "Engine bear (0.2% growth, WACC +1pt) with JVs at Ke +1pt", t5, case="bear", ref=BEAR)
results["t5_inputs"] = {"jv_base_meur": JV0, "jv_bear_meur": jv_bear, "ke_bear": k_bear}

# ======================= AGENT CHALLENGES =======================
# Valuation/PM: terminal growth 1.1% (JV growth moved with it)
def g_low(b):
    b["dcf"]["terminal_growth"] = DATA_G_LOW


record("c_terminal_g_11", "Terminal growth 1.1% (Data agent low end), JVs at g 1.1%",
       run("c_terminal_g", jv_at(ke(V["beta"]), DATA_G_LOW), g_low))

# Fundamentals: RONIC. Lower bound if Foods' capital were only its goodwill (ex-perimeter ROIC after restructuring)
nopat_ex = ((GROUP_UOP - PERIM_UOP) - restr_avg * (GROUP_SALES - PERIM_SALES)) * (1 - V["tax_rate"])  # NOPAT after recurring restructuring
ronic_low = nopat_ex / (AVG_IC - FOODS_GOODWILL)                 # ROIC = NOPAT / invested capital (Foods goodwill removed only)
record("c_ronic_low", f"Terminal RONIC {ronic_low:.1%} (ex-Foods-goodwill lower bound)",
       run("c_ronic_low", change_brief=lambda b: b["dcf"].__setitem__("terminal_ronic", round(ronic_low, 4))))
wacc0 = json.loads((SCRATCH / "00_control" / "out" / "valuation.json").read_text())["base"]["wacc"]["wacc"]
record("c_ronic_eq_wacc", "Terminal RONIC = WACC (growth adds no value)",
       run("c_ronic_wacc", change_brief=lambda b: b["dcf"].__setitem__("terminal_ronic", round(wacc0, 6))))
results["c_ronic_inputs"] = {"nopat_ex_perimeter_meur": nopat_ex, "ic_ex_foods_goodwill_meur": AVG_IC - FOODS_GOODWILL,
                             "ronic_low": ronic_low, "wacc": wacc0}

# Risk: beta at the Damodaran 2020-24 average (relevered), JV consistent
def beta_to(b_):
    def f(i):
        setv(i, "beta", b_, "risk/notes.md sensitivity")
        jv_at(ke(b_), G0)(i)
    return f


record("c_beta_damo_5y", "Beta 0.9998 (Damodaran 2020-24 average, relevered), JVs consistent", run("c_beta_1", beta_to(BETA_DAMO_5Y)))

# Data: McCormick price falls by one standard deviation of its own 1-year volatility before closing (~0.71 years)
mkc = pd.read_csv(HERE / "scratch" / "mkc_1y_yahoo.csv", parse_dates=["date"]).set_index("date")["close"]
mkc_vol = risk.annualised_volatility(mkc, "D")                    # annualised volatility of daily returns
t_close = 259 / 365                                               # 14 Oct 2026 to 30 Jun 2027 (valuation notes (a))
mkc_1sd = MKC_PRICE * (1 - mkc_vol * math.sqrt(t_close))          # one-standard-deviation fall over the time to closing


def mkc_at(p):
    def f(i):
        new = (FOODS_CASH_USD + MKC_NEW_SHARES_M * p) / USD_PER_EUR   # consideration = cash + shares x price, in EUR
        setv(i, "disposal_proceeds", round(new, 1), f"MKC at USD {p:.2f}")
        setv(i, "priced_at_valuation_date_meur", round(V["priced_at_valuation_date_meur"] - V["disposal_proceeds"] + new, 1),
             "consideration is priced today")
    return f


record("c_mkc_1sd", f"McCormick at USD {mkc_1sd:.2f} (1 s.d. fall to closing)", run("c_mkc_1sd", mkc_at(mkc_1sd)))
results["c_mkc_inputs"] = {"change_1y": float(mkc.iloc[-1] / mkc.iloc[0] - 1),   # 1-year price change
                           "change_vs_deal_ref": MKC_PRICE / MKC_DEAL_REF - 1, "vol_1y": mkc_vol, "years_to_close": t_close, "price_1sd": mkc_1sd,
                           "price_1y_ago": float(mkc.iloc[0]), "price_low": float(mkc.min()), "price_high": float(mkc.max())}

# Valuation: the engine bear forecasts 0.2% a year but keeps 1.6% terminal growth; a consistent bear uses 0.2% for both
BEAR_G = BRIEF0["scenarios"]["bear"]["organic_growth"][-1]


def g_bear(b):
    b["dcf"]["terminal_growth"] = BEAR_G


record("c_bear_terminal_g", "Engine bear + JV fix + terminal growth 0.2% (= bear forecast)",
       run("c_bear_terminal_g", jv_at(k_bear, BEAR_G), g_bear), case="bear", ref=results["t5_engine_bear_jv"]["value_pence"])

# ======================= STACKED BEAR (deal closes) =======================
def stack(with_hul):
    def fi(i):
        jv_at(k_bear, G0)(i)
        setv(i, "base_margin", BRIEF0["scenarios"]["bear"]["bear_agent_margin"], "bear margin")
        restr = V["restructuring_cash"] + tax_eur + (HUL_OUTSIDE_MEUR if with_hul else 0.0)
        setv(i, "restructuring_cash", round(restr, 1), "500 + 25% tax" + (" + HUL at market (debt-like line)" if with_hul else ""))
        setv(i, "priced_at_valuation_date_meur", round(V["priced_at_valuation_date_meur"] - tax_eur - (HUL_OUTSIDE_MEUR if with_hul else 0.0), 1),
             "tax and HUL are today amounts")
        if with_hul:
            setv(i, "minority_share_of_operating_profit", round(others_share, 5), "non-HUL minorities only")
    return fi


record("s_stack_no_hul", "Stack: engine bear + JV fix + margin 16.2% + 25% tax", run("s_stack_no_hul", stack(False)), case="bear", ref=BASE)
record("s_stack_hul", "Stack: as above + HUL at market (others proportionate)", run("s_stack_hul", stack(True)), case="bear", ref=BASE)

# ======================= RISKS TO THE SELL (bull side) =======================
record("r_beta_054", "Beta 0.54 (own 5y weekly), JVs consistent", run("r_beta_054", beta_to(BETA_OWN_WEEKLY)))
record("r_margin_182", "Margin 18.2% (18.8% less management's 0.6% guide)",
       run("r_margin_182", lambda i: setv(i, "base_margin", 0.182, "margin evidence pack option A2")))
record("r_margin_188", "Margin 18.8% (restructuring treated as one-off)",
       run("r_margin_188", lambda i: setv(i, "base_margin", 0.188, "margin evidence pack option B")))
record("r_margin_197", "Margin 19.7% (Valuation agent HOLD flip point)",
       run("r_margin_197", lambda i: setv(i, "base_margin", 0.197, "valuation/notes.md flip point (e)")))
record("r_mkc_deal_ref", f"McCormick back to USD {MKC_DEAL_REF} (deal reference price)", run("r_mkc_ref", mkc_at(MKC_DEAL_REF)))
record("r_mkc_6655", "McCormick at USD 66.55 (Valuation agent HOLD flip point)", run("r_mkc_6655", mkc_at(66.55)))
record("r_beta_0748", "Beta 0.748 (Valuation agent HOLD flip point), JVs consistent", run("r_beta_0748", beta_to(0.748)))
record("r_beta_091", "Beta 0.91 (own 5y monthly), JVs consistent", run("r_beta_091", beta_to(0.91)))

out = {"base_pence": BASE, "engine_bear_pence": BEAR, "share_price_pence": PRICE, "hold_floor_pence": HOLD_FLOOR,
       "buy_floor_pence": BUY_FLOOR, "results": results}
(HERE / "bear_results.json").write_text(json.dumps(out, indent=2, default=float))
for k, r in results.items():
    if "value_pence" in r:
        print(f"{k:28s} {r['value_pence']:8.1f}p  impact {r['impact_vs_reference_pence']:+8.1f}p  {r['rating']:4s} {r['upside']:+.1%}  | {r['label']}")
print(json.dumps({k: v for k, v in results.items() if k.endswith('inputs')}, indent=1, default=float))
