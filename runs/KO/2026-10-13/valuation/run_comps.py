"""Valuation agent comps script for KO (run 2026-10-13). Uses desk/comps.py and desk/dcf.py only.

All money in USD m, per-share values in US dollars (KO trades on the NYSE in USD; no FX, no ADR).
Run from the repo root: PYTHONPATH=. python runs/KO/2026-10-13/valuation/run_comps.py
"""
import csv
import json
from pathlib import Path

import yaml

from desk import comps, dcf
from desk.valuation_run import OPTIONAL_BRIDGE

HERE = Path(__file__).parent
RUN = HERE.parent
ROOT = RUN.parents[2]
brief = yaml.safe_load((ROOT / "briefs" / "KO.yaml").read_text())
raw = yaml.safe_load((RUN / "inputs.yaml").read_text())
v = {k: x["value"] for k, x in raw.items()}
price = v["share_price_usd"]
shares = v["shares_outstanding_m"]
KO_FYE = brief["company"]["fiscal_year_end_month"]

# ---- KO metrics, each from data/financials.csv (FY25 = LTM to 31 Dec 2025, the latest audited period) ----
fin = {}
with open(RUN / "data" / "financials.csv") as f:
    for r in csv.DictReader(f):
        fin[(r["item"], r["fiscal_year"])] = (float(r["value_musd"]), r["source"])
comp_oi, src_oi = fin[("comparable_operating_income", "2025")]
da, src_da = fin[("depreciation_amortisation", "2025")]
op_rep, src_op = fin[("operating_profit_reported", "2025")]
ni, src_ni = fin[("net_profit_to_owners", "2025")]
eps_comp, src_eps = fin[("comparable_eps_usd", "2025")]
CCBA_EBIT = 246 * 1.0819996  # FX conversion: CCBA 2024 EBIT EUR 246m x USD per EUR (same figure the PM adopted in inputs.yaml base_margin)

# EBITDA = operating income + depreciation & amortisation
ko_ebitda = {
    "comparable_ex_ccba": comp_oi - CCBA_EBIT + da,   # primary: matches the bridge, which adds CCBA sale proceeds + retained 25%
    "comparable_incl_ccba": comp_oi + da,              # as asked (LTM comparable EBITDA), but double counts CCBA with the bridge
    "gaap_incl_ccba": op_rep + da,                     # same (unadjusted GAAP) basis as the peers' EBITDA
}

# ---- Peers: all December year-ends like KO, so calendarisation is the identity (checked with desk/comps.calendarise) ----
peers, optional = [], []
with open(RUN / "data" / "peers.csv") as f:
    for r in csv.DictReader(f):
        (peers if r["ticker"] in ("PEP", "KDP", "MNST") else optional).append(r)


def num(x):
    return float(x) if x not in ("", None) else None


rows = []
for p in peers:
    fye = int(p["fy_end_month"])
    # calendarise: a peer whose fiscal year ends in KO's year-end month needs no time-weighting
    assert comps.calendarise({2025: 1.0}, fye, KO_FYE, 2025) == 1.0
    mcap = num(p["price_usd"]) * num(p["shares_m"])                     # market cap = price x shares
    ev = mcap + num(p["net_debt_musd"]) + num(p["nci_musd"])            # enterprise value = market cap + net debt + minorities
    rows.append({
        "peer": p["name"], "ticker": p["ticker"], "fy_end_month": fye, "calendarised": "not needed (December year end = KO)",
        "ltm_end": p["ltm_end"], "price_usd": num(p["price_usd"]), "shares_m": num(p["shares_m"]),
        "market_cap_musd_check": round(mcap, 1), "market_cap_musd_csv": num(p["market_cap_musd"]),
        "ev_musd": round(ev, 1), "ebitda_ltm_musd": num(p["ebitda_ltm_musd"]),
        "ev_ebitda_ltm": ev / num(p["ebitda_ltm_musd"]),               # EV / LTM EBITDA
        "pe_ltm": mcap / num(p["net_income_ltm_musd"]),                 # P/E = market cap / LTM net income
        "eps_ntm_usd": num(p["eps_ntm_consensus_usd"]),
        "pe_ntm": num(p["price_usd"]) / num(p["eps_ntm_consensus_usd"]),  # forward P/E = price / NTM EPS consensus
        "fcf_yield_ltm": num(p["fcf_ltm_musd"]) / mcap,                 # FCF yield = LTM FCF / market cap
        "ev_ebitda_ntm": None,                                           # MISSING: no NTM EBITDA consensus (data/notes.md)
        "flag": p["flag"]})

# MNST split check: shares used must be post-split, consistent with the post-split price and post-split EPS consensus
mnst = next(r for r in rows if r["ticker"] == "MNST")
mnst_check = {"shares_m_used": mnst["shares_m"], "pre_split_cover_shares_m": 979.525882, "split": 2,
              "post_split_shares_m": 979.525882 * 2, "price_usd_post_split": mnst["price_usd"],
              "ltm_net_income_per_post_split_share_usd": 2128.0 / mnst["shares_m"], "eps_ntm_usd": mnst["eps_ntm_usd"],
              "market_cap_matches_csv_within_0.05pct": abs(mnst["market_cap_musd_check"] / mnst["market_cap_musd_csv"] - 1) < 0.0005}

bridge = dcf.Bridge(net_debt=v["net_debt"], **{k: v[k] for k in OPTIONAL_BRIDGE},
                    contingent_liabilities=v["contingent_liabilities"])


def per_share_from_ev(ev):
    """Same EV-to-equity bridge as the DCF (net debt, leases, minorities, IRS liability, + stakes, + CCBA proceeds).
    No roll-forward: a market multiple already prices KO today."""
    return dcf.equity_bridge(ev, bridge, shares, None, None)["per_share_usd"]


def ev_leg(mults, metric):
    r = comps.implied_values(mults, metric)  # median, low, high multiple x KO metric = implied EV
    return {"median_multiple": r["median_multiple"], "low_multiple": min(mults), "high_multiple": max(mults),
            "implied_ev_musd": {k: r[k] for k in ("low", "implied_value", "high")},
            "value_per_share_usd": {k: per_share_from_ev(r[k]) for k in ("low", "implied_value", "high")}}


def upside(x):
    return x / price - 1  # upside = value / price - 1


all3 = [r["ev_ebitda_ltm"] for r in rows]
ex_kdp = [r["ev_ebitda_ltm"] for r in rows if r["ticker"] != "KDP"]
legs = {}
for basis, e in ko_ebitda.items():
    legs[f"ev_ebitda_ltm_x_{basis}"] = {"ko_ebitda_musd": e, **ev_leg(all3, e)}
legs["ev_ebitda_ltm_ex_kdp_x_comparable_ex_ccba"] = {"ko_ebitda_musd": ko_ebitda["comparable_ex_ccba"],
                                                     **ev_leg(ex_kdp, ko_ebitda["comparable_ex_ccba"])}

# P/E legs: equity-level multiples, so value per share = multiple x KO earnings per share (no EV bridge)
pe_ntm = [r["pe_ntm"] for r in rows]
pe_ltm = [r["pe_ltm"] for r in rows]
r_ltm = comps.implied_values(pe_ltm, ni / shares)   # GAAP LTM P/E x KO FY25 GAAP net income per share
r_xc = comps.implied_values(pe_ntm, eps_comp)       # forward P/E x FY25 comparable EPS: mismatched basis, cross-check only
legs["pe_ntm_x_ko_forward_eps"] = {"status": "MISSING: KO forward (NTM) EPS consensus is not in the data folder "
                                   "(data/financials.csv has only FY25 comparable EPS $3.00). Not estimated.",
                                   "median_multiple": comps.implied_values(pe_ntm, 1.0)["median_multiple"]}
legs["pe_ltm_gaap_x_ko_fy25_gaap_eps_crosscheck"] = {
    "ko_eps_usd": ni / shares, "median_multiple": r_ltm["median_multiple"],
    "value_per_share_usd": {k: r_ltm[k] for k in ("low", "implied_value", "high")}}
legs["pe_ntm_x_ko_fy25_comparable_eps_crosscheck"] = {
    "ko_eps_usd": eps_comp, "note": "forward multiple on trailing EPS: understates value by about one year of EPS growth",
    "median_multiple": r_xc["median_multiple"], "value_per_share_usd": {k: r_xc[k] for k in ("low", "implied_value", "high")}}

# KO's own multiples at today's price, same EV definition as the peers (market cap + net debt + minorities)
ko_mcap = price * shares
ko_ev_mkt = ko_mcap + v["net_debt"] + v["minority_interests"]
ko_own = {"market_cap_musd": ko_mcap, "ev_musd_peer_definition": ko_ev_mkt,
          "ev_ebitda_ltm_comparable_incl_ccba": ko_ev_mkt / ko_ebitda["comparable_incl_ccba"],
          "ev_ebitda_ltm_gaap": ko_ev_mkt / ko_ebitda["gaap_incl_ccba"],
          "pe_ltm_gaap": ko_mcap / ni, "pe_on_fy25_comparable_eps": price / eps_comp}

dcf_val = json.loads((HERE / "valuation.json").read_text())["base"]["equity"]["per_share_usd"]
primary = legs["ev_ebitda_ltm_x_comparable_ex_ccba"]["value_per_share_usd"]
out = {
    "currency": "USD (per share), USD m (totals)", "price_usd": price, "price_source": raw["share_price_usd"]["source"],
    "method": ("EV/EBITDA LTM (median of PEP, KDP, MNST) x KO FY25 comparable EBITDA ex-CCBA, then the DCF's EV-to-equity "
               "bridge without roll-forward. Forward P/E leg MISSING (no KO forward EPS in the data folder). All peers have "
               "December year ends like KO, so calendarise() is the identity. EV/EBITDA NTM MISSING (no NTM EBITDA)."),
    "ko_metrics": {"comparable_operating_income_fy25": [comp_oi, src_oi], "da_fy25": [da, src_da],
                   "operating_profit_reported_fy25": [op_rep, src_op], "net_profit_to_owners_fy25": [ni, src_ni],
                   "comparable_eps_fy25_usd": [eps_comp, src_eps],
                   "ccba_ebit_removed_musd": [CCBA_EBIT, raw["base_margin"]["source"]],
                   "ebitda_musd": ko_ebitda},
    "peers": rows, "mnst_split_check": mnst_check, "legs": legs, "ko_own_multiples": ko_own,
    "comps_range_usd_primary": primary,
    "dcf_value_usd": dcf_val,
    "dcf_vs_comps_median": dcf_val / primary["implied_value"] - 1,     # gap = DCF / comps - 1
    "comps_median_upside": upside(primary["implied_value"]),
    "optional_peers_shown_separately": [
        {"ticker": "CCEP", "note": "bottler (lower margin), show separately", "status": "MISSING: no XBRL companyfacts, site blocked (data/peers.csv)"},
        {"ticker": "DEO", "note": "out-of-sector cross-check, show separately",
         "pe_ltm_at_current_price": json.loads((ROOT / "runs/DGE/2026-10-12/valuation/comps.json").read_text())["diageo_pe_at_current_price"],
         "source": "runs/DGE/2026-10-12/valuation/comps.json (June FY26 EPS before exceptionals; not calendarised to December; EV/EBITDA not available)"}],
    "flags": [
        "KDP: LTM EV includes JDE Peet's debt and NCI but EBITDA has only about one quarter of JDE Peet's, so 19.1x is inflated; KDP is the median of three. Ex-KDP median shown.",
        "MNST: 2-for-1 split 11 Aug 2026; shares used 1,959.1m = 979.5m pre-split x 2, consistent with the post-split price and EPS consensus.",
        "Peer EBITDA is GAAP unadjusted; KO primary is comparable (non-GAAP). GAAP variant shown.",
        "Timing: KO LTM = FY25 (to 31 Dec 2025); peers' LTM ends Jun/Sep 2026. KO H1 2026 not in the data folder.",
        "CCBA D&A is not disclosed, so ex-CCBA EBITDA removes CCBA EBIT only (slightly overstated).",
        "Only 3 core peers, wide range (11.4x to 29.1x): treat comps as a cross-check."]}
(HERE / "comps.json").write_text(json.dumps(out, indent=2, default=float))
with open(HERE / "comps.csv", "w", newline="") as f:
    cols = ["peer", "ticker", "fy_end_month", "calendarised", "ltm_end", "price_usd", "shares_m", "market_cap_musd_check",
            "ev_musd", "ebitda_ltm_musd", "ev_ebitda_ltm", "ev_ebitda_ntm", "pe_ltm", "eps_ntm_usd", "pe_ntm", "fcf_yield_ltm", "flag"]
    w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
    w.writeheader()
    for r in rows:
        w.writerow({k: (round(x, 4) if isinstance(x, float) else x) for k, x in r.items()})
    for o in out["optional_peers_shown_separately"]:
        w.writerow({"peer": f"(optional, shown separately) {o['ticker']}", "ticker": o["ticker"],
                    "pe_ltm": round(o["pe_ltm_at_current_price"], 2) if "pe_ltm_at_current_price" in o else "",
                    "flag": f"{o['note']}; {o.get('status', o.get('source'))}"})
print(json.dumps({"ebitda": ko_ebitda, "legs": legs, "ko_own": ko_own, "mnst": mnst_check,
                  "dcf_vs_comps": out["dcf_vs_comps_median"], "comps_upside": out["comps_median_upside"],
                  "peers": [(r["ticker"], round(r["ev_ebitda_ltm"], 2), round(r["pe_ltm"], 2), round(r["pe_ntm"], 2)) for r in rows]},
                 indent=1, default=float))
