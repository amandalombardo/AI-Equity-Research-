"""Valuation agent comps script for ULVR (run 2026-10-14). Uses desk/comps.py and desk/dcf.py only.

Money in EUR m (Unilever reports in euros); per-share values in pence (GBp, London price) and EUR.
Peer multiples are unit-free (each peer's EV and EBITDA are in its own currency).
Run from the repo root: PYTHONPATH=. python runs/ULVR/2026-10-14/valuation/run_comps.py

Method (brief comps section):
- EV/EBITDA LTM: median of the 7 core peers, with and without the distorted peers (KMB: pending Kenvue deal;
  CL: Q4 2025 Filorga impairment in LTM). Hindustan Unilever shown separately (brief optional_peers).
- The multiple is applied to the EBITDA of the business that REMAINS after the Foods sale (ex-perimeter), then
  the SAME non-operating items as the DCF are added/deducted (Foods consideration, stakes/JVs/investments, minorities
  proportionate, net debt, restructuring), so the comps value and the DCF value per share are comparable.
- Calendarisation: every peer's LTM ends 30 Jun 2026 (PG's own fiscal year ends then). To compare like with like,
  Unilever's ex-perimeter EBITDA is put on the same 12 months to June 2026 with desk.comps.calendarise (6/12 FY25 +
  6/12 FY26). Restating the peers onto December 2025 instead would need their H2 2025 figures, which are not in
  data/peers.csv (MISSING). Forward P/E is calendarised onto Unilever's December year end (FY27 = Dec 2027).
"""
import csv
import json
import re
from pathlib import Path

import yaml

from desk import comps, dcf, units
from desk.valuation_run import apply_brief_rules, build, extra_required, load_inputs

HERE = Path(__file__).resolve().parent
RUN = HERE.parent
ROOT = RUN.parents[2]
brief = yaml.safe_load((ROOT / "briefs" / "ULVR.yaml").read_text())
v, sources = load_inputs(str(RUN / "inputs.yaml"), extra_required(brief))
apply_brief_rules(brief, v, sources)
base = build(brief, v)
FYE = brief["company"]["fiscal_year_end_month"]          # 12 (December)
price_p = v["share_price_gbp_pence"]
shares, fx = v["shares_outstanding_m"], v["fx_eur_per_gbp"]
m_share = v["minority_share_of_operating_profit"]

fin = {}
with open(RUN / "data" / "financials.csv") as f:
    for r in csv.DictReader(f):
        fin[(r["item"], r["fiscal_year"])] = (float(r["value_meur"]), r["source"])

# ---------------- Unilever metric: EBITDA of the business that remains (ex-perimeter), EUR m ----------------
# PM basis (primary): EBIT at the 17.7% margin AFTER recurring restructuring + D&A at 2.6% of sales. Closest to the
# peers' GAAP (unadjusted) EBITDA, which is also after restructuring costs. FY25 = the engine's projection with zero
# growth (sales = FY25 ex-perimeter base); FY26 = the engine's first forecast year (base case).
fy25_inp = dcf.DcfInputs(**{**base["inputs"].__dict__, "growth": [0.0], "cumulative_savings": [0.0], "years": [2025]})
ebitda_pm = {2025: dcf.project(fy25_inp)[0]["ebitda"], 2026: base["dcf"]["rows"][0]["ebitda"]}
# Underlying basis (variant): ex-perimeter UOP 7,484 (= 10,084 - 2,600, before restructuring) + D&A at the PM's 2.6% of
# ex-perimeter sales (the perimeter's own D&A is not disclosed), FY26 grown with sales (+0.5%, brief).
uop_x = fin[("underlying_operating_profit", "2025")][0]   # Group UOP FY25 (FY25 results 6-K)
uop_x -= fin[("foods_perimeter_uop", "2025")][0]
ebitda_und = {2025: uop_x + v["base_sales"] * v["da_pct_sales"]}
ebitda_und[2026] = ebitda_und[2025] * (1 + brief["dcf"]["organic_growth"][0])
# calendarise Unilever onto the peers' window: 12 months to 30 Jun 2026 = 6/12 FY25 + 6/12 FY26
ulvr_ebitda = {"pm_basis_after_restructuring": comps.calendarise(ebitda_pm, FYE, 6, 2026),
               "underlying_before_restructuring": comps.calendarise(ebitda_und, FYE, 6, 2026)}

# ---------------- Peers ----------------
def num(x):
    return float(x) if x not in ("", None) else None


def fwd_eps(src):
    """Consensus EPS for the current and next fiscal year, from the Data agent's source text (Yahoo earningsTrend)."""
    m = re.search(r"FY to (\d{4})-(\d{2})-\d{2}: ([\d.]+) / next FY: ([\d.]+)", src)
    y = int(m.group(1))
    return {y: float(m.group(3)), y + 1: float(m.group(4))}, int(m.group(2))


def price_eps_units(p):
    """Share price in the same unit as the EPS consensus: London prices are quoted in pence (GBp), EPS in pounds."""
    return units.pence_to_pounds(num(p["price"])) if p["ticker"].endswith(".L") else num(p["price"])


rows, optional = [], []
with open(RUN / "data" / "peers.csv") as f:
    for p in csv.DictReader(f):
        fye = int(p["fy_end_month"])
        eps, eps_m = fwd_eps(p["source"])
        assert eps_m == fye, p["ticker"]
        eps_fy27 = comps.calendarise(eps, fye, FYE, 2027)        # EPS for the 12 months to Dec 2027 (Unilever FY27)
        ev, mcap = num(p["ev_m"]), num(p["market_cap_m"])
        r = {"peer": p["name"], "ticker": p["ticker"], "ccy": p["ccy"], "fy_end_month": fye, "ltm_end": p["ltm_end"],
             "calendarised": ("LTM to Jun 2026 = PG fiscal year; Unilever EBITDA put on the same window"
                              if fye == 6 else "LTM to Jun 2026 (common window); Unilever EBITDA put on the same window"),
             "price": num(p["price"]), "market_cap_m": mcap, "ev_m": ev, "ebitda_ltm_m": num(p["ebitda_ltm_m"]),
             "ev_ebitda_ltm": ev / num(p["ebitda_ltm_m"]),               # EV / LTM EBITDA
             "ev_ebitda_ltm_csv": num(p["ev_ebitda_ltm"]),
             "ev_ebitda_ntm": None,                                       # MISSING: no NTM EBITDA consensus (data notes)
             "pe_ltm": num(p["pe_ltm"]), "pe_ntm_csv": num(p["pe_ntm"]),
             "eps_fy27_dec_calendarised": eps_fy27,
             # forward P/E = price / EPS calendarised to Dec 2027. Reckitt: price is in pence (GBp) although peers.csv
             # says GBP, while the consensus EPS is in pounds, so the price is converted to pounds first.
             "price_in_eps_units": price_eps_units(p),
             "pe_fy27_dec_calendarised": price_eps_units(p) / eps_fy27,
             "fcf_yield_ltm": num(p["fcf_yield_ltm"]),                    # FCF yield = LTM FCF / market cap
             "flag": p["flag"]}
        (optional if p["ticker"] == "HINDUNILVR.NS" else rows).append(r)
for r in rows + optional:
    assert abs(r["ev_ebitda_ltm"] / r["ev_ebitda_ltm_csv"] - 1) < 0.005, r["ticker"]   # ties to the Data agent's CSV

# ---------------- Bridges: the same non-operating items as the DCF ----------------
q2_dividend = 1004.8   # Q2 2026 dividend, ex 6 Aug 2026 (after 30 Jun): EUR 0.4664 x 2,154,327,344 shares (inputs.yaml
                       # dividends_ex_before_valuation_meur source; H1 2026 6-K note 10; TVR 6-K 3 Aug 2026)
nd_jun, nd_jun_src = fin[("net_debt_unilever_definition_30jun2026", "2026")]


def bridge(net_debt):
    return dcf.Bridge(net_debt=net_debt, lease_liabilities=v["lease_liabilities"], pension_deficit=v["pension_deficit"],
                      associates=v["associates"], disposal_proceeds=v["disposal_proceeds"],
                      restructuring_cash=v["restructuring_cash"], minority_share_of_ev=m_share)


# Primary (latest): a market multiple prices the company TODAY, so no growth at the cost of equity. Net debt at
# 30 Jun 2026 (latest reported; already after the H1 buyback and the Q4 2025 + Q1 2026 dividends, and after the cash
# earned in H1), less the Q2 2026 dividend paid after June.
B_LATEST = (bridge(nd_jun), {"cost_of_equity": 0.0, "years": 0.0, "dividends": q2_dividend, "buybacks": 0.0})
# Variant (DCF dates): net debt at 31 Dec 2025 as in the DCF, less every dividend and buyback since (no growth at Ke).
# Gives no credit for the cash earned Jan-Oct 2026, so it is a LOW bound.
B_DEC = (bridge(v["net_debt"]), {"cost_of_equity": 0.0, "years": v["stub_years"],
                                 "dividends": v["dividends_ex_before_valuation_meur"],
                                 "buybacks": v["buybacks_after_balance_sheet_meur"]})


def per_share(ev, which=B_LATEST):
    e = dcf.equity_bridge(ev, which[0], shares, fx, which[1], "EUR")
    return {"pence": e["per_share_gbp_pence"], "eur": e["per_share_eur"], "equity_meur": e["equity_value"],
            "minorities_meur": e["minorities_deducted"]}


def leg(mults, ebitda, which=B_LATEST):
    r = comps.implied_values(mults, ebitda)   # median, lowest and highest peer multiple x Unilever EBITDA = implied EV
    out = {"peers_used": r["peers_used"], "median_multiple": r["median_multiple"],
           "low_multiple": min(mults), "high_multiple": max(mults), "ulvr_ebitda_meur": ebitda,
           "implied_ev_meur": {k: r[k] for k in ("low", "implied_value", "high")}}
    for k in ("low", "implied_value", "high"):
        ps = per_share(r[k], which)
        out.setdefault("value_per_share_pence", {})[k] = ps["pence"]
        out.setdefault("value_per_share_eur", {})[k] = ps["eur"]
        out.setdefault("upside_vs_price", {})[k] = ps["pence"] / price_p - 1   # upside = value / price - 1
    return out


sets = {"all_7": [r for r in rows],
        "ex_KMB": [r for r in rows if r["ticker"] != "KMB"],
        "ex_CL": [r for r in rows if r["ticker"] != "CL"],
        "ex_KMB_and_CL": [r for r in rows if r["ticker"] not in ("KMB", "CL")]}
legs = {}
for name, s in sets.items():
    mults = [r["ev_ebitda_ltm"] for r in s]
    legs[f"ev_ebitda_ltm_{name}"] = {"peers": [r["ticker"] for r in s],
                                     **leg(mults, ulvr_ebitda["pm_basis_after_restructuring"])}
legs["ev_ebitda_ltm_all_7_x_underlying_ebitda"] = leg([r["ev_ebitda_ltm"] for r in rows],
                                                      ulvr_ebitda["underlying_before_restructuring"])
legs["ev_ebitda_ltm_all_7_dcf_dates_bridge_low_bound"] = leg([r["ev_ebitda_ltm"] for r in rows],
                                                             ulvr_ebitda["pm_basis_after_restructuring"], B_DEC)
# multiples only (no Unilever-side metric available)
legs["pe_fy27_dec_calendarised"] = {
    "status": "MULTIPLE ONLY: Unilever's forward EPS for the business that remains is not available (no consensus in "
              "the data folder, and group EPS still includes Foods). Not estimated.",
    **{name: {"median": comps.implied_values([r["pe_fy27_dec_calendarised"] for r in s], 1.0)["median_multiple"]}
       for name, s in sets.items()}}
legs["fcf_yield_ltm"] = {
    "status": "MULTIPLE ONLY: free cash flow of the business that remains is not disclosed. Not estimated.",
    **{name: {"median": comps.implied_values([r["fcf_yield_ltm"] for r in s], 1.0)["median_multiple"]}
       for name, s in sets.items()}}
legs["ev_ebitda_ntm"] = {"status": "MISSING: no NTM EBITDA consensus for any peer (data/notes.md FLAG 13)."}

# Unilever's own market-implied multiple for the business that remains: the EV that makes the primary bridge equal
# today's market cap. Equity is linear in EV: equity = EV x (1 - minority share) + equity at EV 0.
mcap_eur = price_p / 100 * fx * shares                         # market cap (EUR m) = price (GBP) x EUR per GBP x shares
e0 = dcf.equity_bridge(0.0, B_LATEST[0], shares, fx, B_LATEST[1], "EUR")["equity_value"]
ev_mkt = (mcap_eur - e0) / (1 - m_share)
own = {"market_cap_meur": mcap_eur, "market_implied_ev_remaining_business_meur": ev_mkt,
       "market_implied_ev_ebitda_ltm_pm_basis": ev_mkt / ulvr_ebitda["pm_basis_after_restructuring"],
       "market_implied_ev_ebitda_ltm_underlying": ev_mkt / ulvr_ebitda["underlying_before_restructuring"],
       "note": "What the market pays for the business that remains, after taking out the Foods consideration and the "
               "stakes at the same values as the DCF (primary bridge)."}

dcf_p = base["equity"]["per_share_gbp_pence"]
primary = legs["ev_ebitda_ltm_all_7"]
out = {
    "units": "multiples unit-free; EBITDA, EV, equity in EUR m; value per share in pence (GBp) and EUR",
    "price_pence": price_p, "fx_eur_per_gbp": fx, "shares_m": shares,
    "method": __doc__.split("Method (brief comps section):")[1].strip(),
    "ulvr_ebitda_meur": {"fy25_pm_basis": ebitda_pm[2025], "fy26_pm_basis_engine": ebitda_pm[2026],
                         "fy25_underlying": ebitda_und[2025], "fy26_underlying": ebitda_und[2026],
                         "calendarised_ltm_jun2026": ulvr_ebitda},
    "bridge_primary": {"net_debt_30jun2026_meur": [nd_jun, nd_jun_src], "q2_2026_dividend_deducted_meur": q2_dividend,
                       "minority_share_of_ev": m_share, "associates_meur": v["associates"],
                       "disposal_proceeds_meur": v["disposal_proceeds"], "restructuring_cash_meur": v["restructuring_cash"],
                       "roll_forward_at_cost_of_equity": "none (a market multiple already prices the company today)"},
    "bridge_variant_dcf_dates": {"net_debt_31dec2025_meur": v["net_debt"],
                                 "dividends_and_buybacks_deducted_meur": v["dividends_ex_before_valuation_meur"]
                                 + v["buybacks_after_balance_sheet_meur"]},
    "peers": rows, "optional_peers_shown_separately": [
        {**o, "note": "Unilever's 62%-owned Indian subsidiary, show separately (brief optional_peers); not in any median. "
                      "Its 29.3x reflects Indian market growth and valuation; it is already inside Unilever's DCF "
                      "(consolidated), with the 38.1% outside holders deducted as minorities."} for o in optional],
    "legs": legs, "ulvr_own_multiples": own,
    "comps_range_pence_primary": primary["value_per_share_pence"],
    "dcf_value_pence": dcf_p,
    "dcf_vs_comps_median": dcf_p / primary["value_per_share_pence"]["implied_value"] - 1,   # gap = DCF / comps - 1
    "flags": [
        "KMB: price reflects the pending Kenvue acquisition, LTM figures do not (11.9x). CL: LTM EBITDA depressed by the "
        "USD 919m Filorga impairment, so 20.8x is overstated. Medians with and without both are shown.",
        "Peer EBITDA is GAAP/Yahoo unadjusted (after restructuring); Unilever primary metric is after recurring restructuring "
        "(PM 17.7% margin) to match. Underlying variant shown.",
        "peers.csv labels Reckitt's currency GBP but its price (5,258) is in pence (GBp); the forward P/E converts it to "
        "pounds with desk.units.pence_to_pounds (14.6x, not 1,459x). Market cap and EV in peers.csv are in GBP m (checked "
        "against the Data agent's EV/EBITDA).",
        "Four European peers' figures are from Yahoo (non-filing source); not checked to annual reports.",
        "Ex-perimeter D&A is not disclosed: Unilever's ex-perimeter EBITDA uses the PM's 2.6% D&A ratio.",
        "EV/EBITDA NTM MISSING (no NTM EBITDA consensus). P/E and FCF yield: multiples shown, no Unilever-side metric for "
        "the remaining business.",
        "Wide peer range (9.3x to 21.2x): L'Oreal and P&G are premium-growth names; treat comps as a cross-check."]}
(HERE / "comps.json").write_text(json.dumps(out, indent=2, default=float))

cols = ["peer", "ticker", "ccy", "fy_end_month", "ltm_end", "calendarised", "price", "market_cap_m", "ev_m", "ebitda_ltm_m",
        "ev_ebitda_ltm", "ev_ebitda_ntm", "pe_ltm", "pe_ntm_csv", "eps_fy27_dec_calendarised", "pe_fy27_dec_calendarised",
        "fcf_yield_ltm", "in_median", "flag"]
with open(HERE / "comps.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
    w.writeheader()
    for r in rows:
        w.writerow({**{k: (round(x, 4) if isinstance(x, float) else x) for k, x in r.items()},
                    "in_median": "yes (excluded in the ex-KMB / ex-CL variants)" if r["ticker"] in ("KMB", "CL") else "yes"})
    for r in optional:
        w.writerow({**{k: (round(x, 4) if isinstance(x, float) else x) for k, x in r.items()},
                    "peer": f"(optional, shown separately) {r['peer']}", "in_median": "no"})
    for name, s in sets.items():
        L = legs[f"ev_ebitda_ltm_{name}"]
        w.writerow({"peer": f"MEDIAN {name}", "ev_ebitda_ltm": round(L["median_multiple"], 4),
                    "pe_fy27_dec_calendarised": round(legs["pe_fy27_dec_calendarised"][name]["median"], 4),
                    "fcf_yield_ltm": round(legs["fcf_yield_ltm"][name]["median"], 4),
                    "flag": "implied value per share (pence) low/median/high: " + " / ".join(
                        f"{L['value_per_share_pence'][k]:.0f}" for k in ("low", "implied_value", "high"))})

print(json.dumps({"ebitda": out["ulvr_ebitda_meur"], "own": own, "dcf_vs_comps": out["dcf_vs_comps_median"],
                  "legs": {k: {kk: L.get(kk) for kk in ("median_multiple", "value_per_share_pence")} for k, L in legs.items()
                           if "median_multiple" in L},
                  "pe": legs["pe_fy27_dec_calendarised"], "fcfy": legs["fcf_yield_ltm"],
                  "peers": [(r["ticker"], round(r["ev_ebitda_ltm"], 2), round(r["pe_fy27_dec_calendarised"], 2),
                             round(r["eps_fy27_dec_calendarised"], 3)) for r in rows + optional]}, indent=1, default=float))
