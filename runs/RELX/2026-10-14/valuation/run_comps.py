"""Valuation agent comps script for RELX (run 2026-10-14). Uses desk/comps.py, desk/dcf.py and desk/units.py only.

Money in GBP m (RELX reports in pounds); value per share in pence (GBp, the London price) and GBP.
Peer multiples are unit-free (each peer's EV and EBITDA are in its own currency).
Run from the repo root: PYTHONPATH=. python runs/RELX/2026-10-14/valuation/run_comps.py

Method (brief comps section: multiples ev_ebitda_ntm, ev_ebitda_ltm, pe_ntm, fcf_yield; statistic median):
- EV/EBITDA LTM (primary): median of the 7 core peers. Informa (brief optional_peers) shown separately, not in the median.
- Calendarisation: six peers' LTM ends 30 Jun 2026; Experian's (fiscal year to March) ends 31 Mar 2026. Restating the
  peers onto RELX's December 2025 year would need their H2 2025 figures, which are not in data/peers.csv (MISSING). So,
  as in the Unilever run, RELX's EBITDA is put on the peers' window (12 months to June 2026) with desk.comps.calendarise
  (6/12 FY25 actual + 6/12 FY26 engine forecast), and checked against RELX's ACTUAL LTM to June 2026 (3,930: FY25 3,846
  - H1 2025 1,908 + H1 2026 1,992, H1 2026 results p.10). Experian's 3-month offset is left as is (flagged).
- Forward P/E: each peer's consensus EPS is calendarised onto RELX's December year end (Dec 2026 and Dec 2027).
  Multiple only: RELX has no consensus EPS in the data folder (MISSING), so no implied value is computed.
- The EV is turned into equity with the SAME non-operating items as the DCF (minorities 24 at book, venture capital and
  other investments 131), so the comps value and the DCF value per share are comparable. A market multiple prices the
  company TODAY, so there is no growth at the cost of equity. Primary bridge: net debt ex leases at 30 Jun 2026 (8,614,
  latest reported) plus the cash paid out after June and before the 25 Sep share count (buybacks 100 + 150 + 56.2,
  interim dividend 366). Low-bound variant at the DCF's dates: 31 Dec 2025 net debt 7,104 plus every dividend and buyback
  since (no credit for the cash earned in 2026).
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
brief = yaml.safe_load((ROOT / "briefs" / "RELX.yaml").read_text())
v, sources = load_inputs(str(RUN / "inputs.yaml"), extra_required(brief))
apply_brief_rules(brief, v, sources)
base = build(brief, v)
FYE = brief["company"]["fiscal_year_end_month"]          # 12 (December)
price_p = v["share_price_gbp_pence"]
shares = v["shares_outstanding_m"]
OPTIONAL = {p["ticker"]: p for p in brief["comps"]["optional_peers"]}

fin = {}
with open(RUN / "data" / "financials.csv") as f:
    for r in csv.DictReader(f):
        fin[(r["item"], r["fiscal_year"])] = (float(r["value_mgbp"]), r["source"])

H126 = ("RELX H1 2026 interim results 6-K ex 99.1 (accession 0000929869-26-000054, 23 Jul 2026, "
        "https://www.sec.gov/Archives/edgar/data/929869/000092986926000054/relx-20260723xex99d1.htm)")

# ---------------- RELX metrics, GBP m ----------------
ebitda_fy25 = fin[("adjusted_ebitda", "2025")][0]                     # 3,846, AR25 p.186
ebitda_fy26_engine = base["dcf"]["rows"][0]["ebitda"]                 # engine FY26: sales x (35.0% margin + 5.07% D&A)
# calendarise RELX onto the peers' window: 12 months to 30 Jun 2026 = 6/12 FY25 + 6/12 FY26
ebitda_cal = comps.calendarise({2025: ebitda_fy25, 2026: ebitda_fy26_engine}, FYE, 6, 2026)
# actual LTM to 30 Jun 2026 = FY25 - H1 2025 + H1 2026 (adjusted EBITDA, H1 2026 results p.10)
H1_25, H1_26 = 1908.0, 1992.0
ebitda_ltm_actual = ebitda_fy25 - H1_25 + H1_26
# reported basis (closest to the peers' unadjusted EBITDA): reported operating profit + all D&A, FY25 only
ebitda_fy25_reported = fin[("operating_profit_reported", "2025")][0] + fin[("depreciation_amortisation", "2025")][0]
# FY25 free cash flow on the peers' basis: operating cash flow - capex (RELX definition: PP&E + capitalised development)
fcf_fy25 = fin[("operating_cash_flow", "2025")][0] - fin[("capex_total_relx_definition", "2025")][0]
relx_metrics = {"ebitda_calendarised_ltm_jun2026": ebitda_cal, "ebitda_actual_ltm_jun2026": ebitda_ltm_actual,
                "ebitda_fy25_adjusted": ebitda_fy25, "ebitda_fy26_engine": ebitda_fy26_engine,
                "ebitda_fy25_reported_basis": ebitda_fy25_reported, "fcf_fy25_ocf_less_capex": fcf_fy25,
                "sources": {"ebitda_fy25_adjusted": fin[("adjusted_ebitda", "2025")][1],
                            "h1_ebitda": f"{H126} p.10 (adjusted EBITDA H1 2026 1,992; H1 2025 1,908), as cited by the Risk agent",
                            "ebitda_fy25_reported_basis": "operating_profit_reported 3,027 + depreciation_amortisation 752 "
                                                          "(financials.csv, 20-F XBRL)",
                            "fcf_fy25": "operating_cash_flow 2,836 - capex_total_relx_definition 525 (financials.csv, 20-F XBRL)"}}


# ---------------- Peers ----------------
def num(x):
    return float(x) if x not in ("", None) else None


def fwd_eps(src):
    """Consensus EPS for the current and next fiscal year, from the Data agent's source text (Yahoo earningsTrend)."""
    m = re.search(r"FY to (\d{4})-(\d{2})-\d{2}: ([\d.]+) / next FY: ([\d.]+)", src)
    y = int(m.group(1))
    return {y: float(m.group(3)), y + 1: float(m.group(4))}, int(m.group(2))


def price_eps_units(p):
    """Share price in the same unit as the EPS consensus: London prices are quoted in pence (GBp), EPS in pounds
    (Experian's EPS is in US dollars, so its pence price is turned into pounds and then dollars at the CSV's own rate)."""
    px = num(p["price"])
    if not p["ticker"].endswith(".L"):
        return px
    pounds = units.pence_to_pounds(px)
    if p["ccy"] == "USD":   # Experian: market cap in the CSV was converted at FRED DEXUSUK 1.3229 (9 Oct 2026)
        return pounds * 1.3229
    return pounds


rows, optional = [], []
with open(RUN / "data" / "peers.csv") as f:
    for p in csv.DictReader(f):
        fye = int(p["fy_end_month"])
        eps, eps_m = fwd_eps(p["source"])
        assert eps_m == fye, p["ticker"]
        # EPS restated onto RELX's December year: 12 months to Dec 2026 needs the peer's FY ending Dec 2026 (Dec peers)
        # or 9/12 FY to Mar 2027 + 3/12 FY to Mar 2026 (Experian), which is not in the CSV; so only Dec 2027 is common to all
        eps_dec27 = comps.calendarise(eps, fye, FYE, 2027) if (2027 in eps and (fye == 12 or 2028 in eps)) else None
        eps_dec26 = comps.calendarise(eps, fye, FYE, 2026) if (fye == 12 or 2026 in eps) else None
        ev, mcap = num(p["ev_m"]), num(p["market_cap_m"])
        pxe = price_eps_units(p)
        r = {"peer": p["name"], "ticker": p["ticker"], "ccy": p["ccy"], "fy_end_month": fye, "ltm_end": p["ltm_end"],
             "calendarised": ("LTM to Mar 2026 (its fiscal year): 3 months earlier than the common window (FLAG); "
                              "forward EPS calendarised to Dec" if fye == 3 else
                              "LTM to Jun 2026 (common window); RELX EBITDA put on the same window; forward EPS = Dec FY"),
             "price": num(p["price"]), "market_cap_m": mcap, "ev_m": ev, "ebitda_ltm_m": num(p["ebitda_ltm_m"]),
             "ev_ebitda_ltm": ev / num(p["ebitda_ltm_m"]),               # EV / LTM EBITDA
             "ev_ebitda_ltm_csv": num(p["ev_ebitda_ltm"]),
             "ev_ebitda_ntm": None,                                       # MISSING: no NTM EBITDA consensus (data notes)
             "pe_ltm": num(p["pe_ltm"]), "pe_ntm_csv": num(p["pe_ntm"]),
             "price_in_eps_units": pxe,
             "eps_dec2026_calendarised": eps_dec26, "eps_dec2027_calendarised": eps_dec27,
             # forward P/E = price / EPS calendarised to RELX's December year
             "pe_dec2026_calendarised": pxe / eps_dec26 if eps_dec26 else None,
             "pe_dec2027_calendarised": pxe / eps_dec27 if eps_dec27 else None,
             "fcf_yield_ltm": num(p["fcf_yield_ltm"]),                    # FCF yield = LTM FCF / market cap
             "flag": p["flag"]}
        (optional if p["ticker"] in OPTIONAL else rows).append(r)
for r in rows + optional:
    assert abs(r["ev_ebitda_ltm"] / r["ev_ebitda_ltm_csv"] - 1) < 0.005, r["ticker"]   # ties to the Data agent's CSV
    if r["pe_dec2027_calendarised"] and r["ticker"] != "EXPN.L":
        # sanity: Dec-2027 P/E below the CSV's NTM P/E (EPS grows), and within a plausible band
        assert 5 < r["pe_dec2027_calendarised"] < r["pe_ntm_csv"] * 1.05, r["ticker"]

# ---------------- Bridges: the same non-operating items as the DCF ----------------
ND_JUN = 8614.0          # net debt ex leases at 30 Jun 2026 (H1 2026 results p.11; inputs.yaml debt_weight source)
AFTER_JUNE_BUYBACKS = 100.0 + 150.0 + 56.2   # 1-21 Jul, 23 Jul-4 Sep, 7-25 Sep (inputs.yaml buybacks source)
AFTER_JUNE_DIVIDEND = 366.0                  # 2026 interim, ex 6 Aug, paid 10 Sep (inputs.yaml dividends source)
assert abs(v["buybacks_after_balance_sheet_mgbp"] - 1750.0 - AFTER_JUNE_BUYBACKS) < 1e-6
assert abs(v["dividends_ex_before_valuation_mgbp"] - 851.0 - AFTER_JUNE_DIVIDEND) < 1e-6


def bridge(net_debt):
    return dcf.Bridge(net_debt=net_debt, lease_liabilities=v["lease_liabilities"], minority_interests=v["minority_interests"],
                      pension_deficit=v["pension_deficit"], associates=v["associates"],
                      disposal_proceeds=v["disposal_proceeds"], restructuring_cash=v["restructuring_cash"])


# Primary (latest): no growth at Ke (a market multiple prices the company today); cash paid out after June deducted
B_LATEST = (bridge(ND_JUN), {"cost_of_equity": 0.0, "years": 0.0, "dividends": AFTER_JUNE_DIVIDEND,
                             "buybacks": AFTER_JUNE_BUYBACKS})
# Low bound (DCF dates): 31 Dec 2025 net debt, every dividend and buyback since, no credit for cash earned in 2026
B_DEC = (bridge(v["net_debt"]), {"cost_of_equity": 0.0, "years": v["stub_years"],
                                 "dividends": v["dividends_ex_before_valuation_mgbp"],
                                 "buybacks": v["buybacks_after_balance_sheet_mgbp"]})


def per_share(ev, which=B_LATEST):
    e = dcf.equity_bridge(ev, which[0], shares, 1.0, which[1], "GBP")   # GBP reporter: 1 GBP per GBP, pence = GBP x 100
    return {"pence": e["per_share_gbp_pence"], "gbp": e["per_share_gbp"], "equity_mgbp": e["equity_value"]}


def leg(mults, metric, which=B_LATEST):
    r = comps.implied_values(mults, metric)   # lowest, median and highest peer multiple x RELX EBITDA = implied EV
    out = {"peers_used": r["peers_used"], "median_multiple": r["median_multiple"],
           "low_multiple": min(mults), "high_multiple": max(mults), "relx_metric_mgbp": metric,
           "implied_ev_mgbp": {k: r[k] for k in ("low", "implied_value", "high")}}
    for k in ("low", "implied_value", "high"):
        ps = per_share(r[k], which)
        out.setdefault("value_per_share_pence", {})[k] = ps["pence"]
        out.setdefault("value_per_share_gbp", {})[k] = ps["gbp"]
        out.setdefault("upside_vs_price", {})[k] = ps["pence"] / price_p - 1   # upside = value / price - 1
    return out


core = [r["ev_ebitda_ltm"] for r in rows]
legs = {
    "ev_ebitda_ltm_x_calendarised_ebitda (PRIMARY)": leg(core, ebitda_cal),
    "ev_ebitda_ltm_x_actual_ltm_ebitda": leg(core, ebitda_ltm_actual),
    "ev_ebitda_ltm_ex_experian_x_calendarised": leg([r["ev_ebitda_ltm"] for r in rows if r["ticker"] != "EXPN.L"], ebitda_cal),
    "ev_ebitda_ltm_x_fy25_reported_basis_ebitda": leg(core, ebitda_fy25_reported),
    "ev_ebitda_ltm_x_calendarised_dcf_dates_bridge_low_bound": leg(core, ebitda_cal, B_DEC),
}
# FCF yield: equity value = FCF / median peer yield. FY25 RELX FCF (a December year, half a year before the peers' window)
fy = sorted(r["fcf_yield_ltm"] for r in rows)
fcf_med = comps.implied_values(fy, 1.0)["median_multiple"]
# implied equity = FCF / yield; a LOW yield means a HIGH value, so the high value comes from the lowest yield
fcf_leg = {"median_yield": fcf_med, "low_yield": fy[0], "high_yield": fy[-1], "relx_fcf_fy25_mgbp": fcf_fy25,
           "value_per_share_pence": {"low": units.pounds_to_pence(fcf_fy25 / fy[-1] / shares),
                                     "implied_value": units.pounds_to_pence(fcf_fy25 / fcf_med / shares),
                                     "high": units.pounds_to_pence(fcf_fy25 / fy[0] / shares)},
           "note": "Secondary. RELX FCF is FY25 (Dec 2025), half a year before the peers' LTM; RELX's operating cash flow "
                   "is after interest and tax (IFRS), peers' bases differ (Yahoo for four). Equity comes directly, no bridge."}
legs["fcf_yield_ltm"] = fcf_leg
legs["pe_dec2027_calendarised"] = {
    "status": "MULTIPLE ONLY: no RELX consensus EPS in the data folder (MISSING). Not estimated.",
    "median_core": comps.implied_values([r["pe_dec2027_calendarised"] for r in rows], 1.0)["median_multiple"],
    "range_core": [min(r["pe_dec2027_calendarised"] for r in rows), max(r["pe_dec2027_calendarised"] for r in rows)]}
legs["pe_dec2026_calendarised"] = {
    "status": "MULTIPLE ONLY (Experian excluded: its FY to Mar 2026 EPS consensus is not in the CSV).",
    "median_core_ex_experian": comps.implied_values([r["pe_dec2026_calendarised"] for r in rows
                                                     if r["pe_dec2026_calendarised"]], 1.0)["median_multiple"]}
legs["ev_ebitda_ntm"] = {"status": "MISSING: no NTM EBITDA consensus for any peer (data/notes.md, Peers)."}

# RELX's own market multiple: EV that the market pays today on the primary bridge (equity = EV + constant)
mcap = units.pence_to_pounds(price_p) * shares                 # market cap (GBP m) = price (GBP) x shares
e0 = dcf.equity_bridge(0.0, B_LATEST[0], shares, 1.0, B_LATEST[1], "GBP")["equity_value"]
ev_mkt = mcap - e0
own = {"market_cap_mgbp": mcap, "market_implied_ev_mgbp": ev_mkt,
       "market_ev_ebitda_calendarised_ltm": ev_mkt / ebitda_cal, "market_ev_ebitda_actual_ltm": ev_mkt / ebitda_ltm_actual,
       "market_fcf_yield_fy25": fcf_fy25 / mcap,
       "note": "What the market pays for RELX on the same bridge as the primary comps leg (net debt 30 Jun 2026 + cash "
               "paid out since, minorities 24, investments 131)."}

dcf_p = base["equity"]["per_share_gbp_pence"]
primary = legs["ev_ebitda_ltm_x_calendarised_ebitda (PRIMARY)"]
out = {
    "units": "multiples unit-free; EBITDA, EV, equity in GBP m; value per share in pence (GBp) and GBP",
    "price_pence": price_p, "shares_m": shares,
    "method": __doc__.split("Method (brief comps section")[1].split(":", 1)[1].strip(),
    "relx_metrics_mgbp": relx_metrics,
    "bridge_primary": {"net_debt_ex_leases_30jun2026_mgbp": ND_JUN, "buybacks_after_june_mgbp": AFTER_JUNE_BUYBACKS,
                       "interim_dividend_after_june_mgbp": AFTER_JUNE_DIVIDEND,
                       "minorities_book_mgbp": v["minority_interests"], "investments_mgbp": v["associates"],
                       "roll_forward_at_cost_of_equity": "none (a market multiple already prices the company today)"},
    "bridge_low_bound_dcf_dates": {"net_debt_31dec2025_mgbp": v["net_debt"],
                                   "dividends_and_buybacks_deducted_mgbp": v["dividends_ex_before_valuation_mgbp"]
                                   + v["buybacks_after_balance_sheet_mgbp"]},
    "peers": rows,
    "optional_peers_shown_separately": [{**o, "note": OPTIONAL[o["ticker"]]["note"] + " (brief optional_peers): not in any median"}
                                        for o in optional],
    "legs": legs, "relx_own_multiples": own,
    "comps_range_pence_primary": primary["value_per_share_pence"],
    "dcf_value_pence": dcf_p,
    "dcf_vs_comps_median": dcf_p / primary["value_per_share_pence"]["implied_value"] - 1,   # gap = DCF / comps - 1
    "flags": [
        "Peers' LTM is to 30 Jun 2026 (Experian 31 Mar 2026); RELX's EBITDA is put on the June window rather than the "
        "peers on December, because the peers' H2 2025 figures are not in peers.csv (MISSING).",
        "Peer EBITDA is reported operating income + D&A (unadjusted, after acquisition costs); RELX's is adjusted EBITDA. "
        "FY25 reported-basis RELX EBITDA is 3,779 vs adjusted 3,846 (-1.7%); variant shown.",
        "Three of seven core peers (WKL, EXPN, LSEG) and Informa are Yahoo-only figures, not checked to annual reports.",
        "Experian: LTM ends March 2026; its EPS is in USD and its price in pence, so the price is converted to USD at the "
        "Data agent's 1.3229 USD/GBP before the forward P/E.",
        "TRI: LTM still includes Global Print (51% sale to KKR pending). SPGI: EV includes the redeemable minority.",
        "EV/EBITDA NTM MISSING (no consensus). Forward P/E is a multiple only: RELX consensus EPS MISSING.",
        "US peers' EBITDA does not add back operating-lease cost, IFRS peers' and RELX's do (RELX lease depreciation 37 "
        "in FY25): a small mismatch, not adjusted."]}
(HERE / "comps.json").write_text(json.dumps(out, indent=2, default=float))

cols = ["peer", "ticker", "ccy", "fy_end_month", "ltm_end", "calendarised", "price", "market_cap_m", "ev_m", "ebitda_ltm_m",
        "ev_ebitda_ltm", "ev_ebitda_ntm", "pe_ltm", "pe_ntm_csv", "eps_dec2026_calendarised", "pe_dec2026_calendarised",
        "eps_dec2027_calendarised", "pe_dec2027_calendarised", "fcf_yield_ltm", "in_median", "flag"]
with open(HERE / "comps.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
    w.writeheader()
    rnd = lambda r: {k: (round(x, 4) if isinstance(x, float) else x) for k, x in r.items()}  # noqa: E731
    for r in rows:
        w.writerow({**rnd(r), "in_median": "yes"})
    L = primary
    w.writerow({"peer": "MEDIAN (7 core peers)", "ev_ebitda_ltm": round(L["median_multiple"], 4),
                "pe_dec2027_calendarised": round(legs["pe_dec2027_calendarised"]["median_core"], 4),
                "pe_dec2026_calendarised": round(legs["pe_dec2026_calendarised"]["median_core_ex_experian"], 4),
                "fcf_yield_ltm": round(fcf_med, 4),
                "flag": "RELX implied value per share (pence) low / median / high, EV/EBITDA x calendarised LTM EBITDA "
                        f"{ebitda_cal:,.0f}: " + " / ".join(f"{L['value_per_share_pence'][k]:.0f}" for k in ("low", "implied_value", "high"))})
    for r in optional:
        w.writerow({**rnd(r), "peer": f"(optional, shown separately) {r['peer']}", "in_median": "no",
                    "flag": OPTIONAL[r["ticker"]]["note"] + "; " + r["flag"]})

print(json.dumps({"relx": relx_metrics | {"sources": "..."}, "own": own, "dcf_vs_comps": out["dcf_vs_comps_median"],
                  "legs": {k: {kk: L.get(kk) for kk in ("median_multiple", "median_yield", "value_per_share_pence", "median_core",
                                                         "median_core_ex_experian")} for k, L in legs.items()},
                  "peers": [(r["ticker"], round(r["ev_ebitda_ltm"], 2), r["pe_dec2026_calendarised"] and round(r["pe_dec2026_calendarised"], 2),
                             r["pe_dec2027_calendarised"] and round(r["pe_dec2027_calendarised"], 2)) for r in rows + optional]},
                 indent=1, default=float))
