"""Risk agent, RELX PLC (REL.L), run 2026-10-14: market risk measures and beta CROSS-CHECKS.

Uses desk/risk.py for returns, beta, volatility and drawdown, and desk/fundamentals.py for leverage.
This script NEVER writes beta to inputs.yaml. The valuation beta follows the PM's bottom-up rule and is written
only by beta_evidence.py (Codex audit RISK-01).

Run from the repo root:  PYTHONPATH=. python runs/RELX/2026-10-14/risk/run_risk.py
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from desk import fundamentals, risk
from desk.data_sources import prices

HERE = Path(__file__).resolve().parent
RUN = HERE.parent
REPO = RUN.parents[2]
brief = yaml.safe_load((REPO / "briefs" / "RELX.yaml").read_text())
TICKER, INDEX = brief["company"]["price_ticker"], brief["company"]["benchmark_index"]   # REL.L (GBp), ^FTSE (points)
LAST_CLOSE_DATE = "2026-10-13"  # price date of the run (13 Oct 2026 close)

px = pd.read_csv(RUN / "data" / "prices.csv", index_col=0, parse_dates=True)
px = px[px.index <= LAST_CLOSE_DATE]
stock, index = px[TICKER].dropna(), px[INDEX].dropna()


def regression(s: pd.Series, ix: pd.Series, freq: str, years: int | None = None) -> dict:
    """OLS beta via desk.risk.beta, plus the standard error of the slope and a 95% confidence interval."""
    if years:
        start = s.index[-1] - pd.DateOffset(years=years)
        s, ix = s[s.index >= start], ix[ix.index >= start]
    out = risk.beta(s, ix, freq)          # beta = Cov(stock, market) / Var(market), with R-squared and observations
    d = pd.concat([risk.returns(s, freq), risk.returns(ix, freq)], axis=1, join="inner").dropna()
    y, x = d.iloc[:, 0], d.iloc[:, 1]
    alpha = y.mean() - out["beta"] * x.mean()
    resid = y - alpha - out["beta"] * x
    # standard error of the regression slope: sqrt(residual variance / sum of squared market deviations)
    se = float(np.sqrt(resid.var(ddof=2) / ((x - x.mean()) ** 2).sum()))
    out.update({"std_error": se, "ci95": [out["beta"] - 1.96 * se, out["beta"] + 1.96 * se]})
    return out


# ---- 1. price unit check: a pence/pound mix-up shows as a ~100x (or 1/100x) day-on-day move
ratio = stock / stock.shift(1)
unit_jumps = ratio[(ratio > 50) | (ratio < 1 / 50)].index.strftime("%Y-%m-%d").tolist()
largest_moves = stock.pct_change().abs().nlargest(5)
level_range = [float(stock.min()), float(stock.max())]
unadjusted_last = float(stock.iloc[-1])

# ---- 2. own regressions vs the brief's benchmark (FTSE 100): cross-checks only
own = {"2y_weekly": regression(stock, index, "W", 2),
       "5y_weekly": regression(stock, index, "W", 5),
       "5y_monthly": regression(stock, index, "M", 5)}
blume_5y_monthly = 0.67 * own["5y_monthly"]["beta"] + 0.33   # Blume adjustment: pulls a raw beta towards 1

# ---- 3. volatility and drawdown (dividend-adjusted closes, GBp)
end = stock.index[-1]
one_year = lambda s: s[s.index >= end - pd.DateOffset(years=1)]  # noqa: E731
vol = {"relx_1y_daily": risk.annualised_volatility(one_year(stock)),     # annualised: daily std x sqrt(252)
       "relx_5y_daily": risk.annualised_volatility(stock),
       "ftse_1y_daily": risk.annualised_volatility(one_year(index)),
       "ftse_5y_daily": risk.annualised_volatility(index)}
dd = risk.max_drawdown(stock)
dd_ftse = risk.max_drawdown(index)

# ---- 4. peer betas, 5y monthly vs each peer's home index (Yahoo Finance adjusted closes, fetched today)
# TRI is the NYSE line (USD), so it is measured against the S&P 500 (same currency); its home market is also Toronto.
HOME = {"TRI": "^GSPC", "VRSK": "^GSPC", "SPGI": "^GSPC", "MCO": "^GSPC", "WKL.AS": "^AEX",
        "EXPN.L": "^FTSE", "LSEG.L": "^FTSE", "INF.L": "^FTSE"}
peer_list = brief["comps"]["peers"] + [dict(p, optional=True) for p in brief["comps"].get("optional_peers", [])]
peer_betas, peer_errors, idx_cache = {}, {}, {}
for p in peer_list:
    t = p["ticker"]
    try:
        ix_t = HOME[t]
        if ix_t not in idx_cache:
            idx_cache[ix_t] = prices(ix_t, 6)
        s = prices(t, 6)
        s, ixs = s[s.index <= LAST_CLOSE_DATE], idx_cache[ix_t][idx_cache[ix_t].index <= LAST_CLOSE_DATE]
        jump = s / s.shift(1)
        peer_betas[p["name"]] = {"ticker": t, "index": ix_t, "optional": bool(p.get("optional")),
                                 "currency": s.attrs.get("currency"), **regression(s, ixs, "M", 5),
                                 "unit_jumps": jump[(jump > 50) | (jump < 0.02)].index.strftime("%Y-%m-%d").tolist(),
                                 "source": f"Yahoo Finance adjusted closes ({t}, {ix_t}), fetched 2026-10-14"}
    except Exception as e:  # report, never estimate
        peer_errors[p["name"]] = f"MISSING: {e}"
core = [v["beta"] for v in peer_betas.values() if not v["optional"]]
peer_median = float(pd.Series(core).median()) if core else None   # median of the 7 core peers (Informa shown separately)

# ---- 5. leverage: net debt / EBITDA, GBP m (RELX's adjusted EBITDA = adjusted operating profit + D&A excl. acquired intangibles)
inp = yaml.safe_load((RUN / "inputs.yaml").read_text())
nd_dec_relx, nd_dec_exl = 7201.0, inp["net_debt"]["value"]   # RELX definition (incl. leases 97) / brief definition (ex leases)
ebitda_fy25, ebitda_h1_25, ebitda_h1_26 = 3846.0, 1908.0, 1992.0
nd_jun_relx, nd_jun_exl = 8733.0, 8614.0
ebitda_ltm_jun26 = ebitda_fy25 - ebitda_h1_25 + ebitda_h1_26   # last twelve months = FY25 - H1 25 + H1 26
FY25R = ("RELX FY2025 results 6-K ex 99.1 (0000929869-26-000008, 12 Feb 2026, "
         "https://www.sec.gov/Archives/edgar/data/929869/000092986926000008/relx-20260201xex99d1.htm)")
H126 = ("RELX H1 2026 results 6-K ex 99.1 (0000929869-26-000054, 23 Jul 2026, "
        "https://www.sec.gov/Archives/edgar/data/929869/000092986926000054/relx-20260723xex99d1.htm)")
lev = {
    "fy25": {"net_debt_relx_def_mgbp": nd_dec_relx, "net_debt_ex_leases_mgbp": nd_dec_exl, "ebitda_mgbp": ebitda_fy25,
             "ratio_relx_def_gbp": fundamentals.leverage(nd_dec_relx, ebitda_fy25),
             "ratio_ex_leases_gbp": fundamentals.leverage(nd_dec_exl, ebitda_fy25),
             "company_reported": "2.0x (net debt incl. pensions / EBITDA, calculated in US dollars)",
             "source": f"{FY25R} p.2 ('Net debt/EBITDA 2.0x (1.8x): Net debt at 31 December 2025 was GBP 7,201m ... EBITDA was "
                       f"GBP 3,846m'), p.11 (EBITDA = adjusted OP 3,342 + D&A 504), p.13 (leases 97; ratio 'calculated in US dollars'); "
                       f"Data agent financials.csv adjusted_ebitda 2025 = 3,846 (AR25 p.186)"},
    "jun26_ltm": {"net_debt_relx_def_mgbp": nd_jun_relx, "net_debt_ex_leases_mgbp": nd_jun_exl, "ebitda_ltm_mgbp": ebitda_ltm_jun26,
                  "ratio_relx_def_gbp": fundamentals.leverage(nd_jun_relx, ebitda_ltm_jun26),
                  "ratio_ex_leases_gbp": fundamentals.leverage(nd_jun_exl, ebitda_ltm_jun26),
                  "company_reported": "2.3x (twelve months to 30 Jun 2026, calculated in US dollars)",
                  "source": f"{H126} p.2 ('Net debt/EBITDA 2.3x (2.2x): Net debt at 30 June 2026 was GBP 8,733m'), p.10 (EBITDA H1 26 "
                            f"1,992, H1 25 1,908), p.11 (net debt ex leases 8,614, per Data agent inputs.yaml), p.12 (ratio text)"},
    "target": "NO numeric target range published. RELX 'seeks to maintain cash flow conversion of 90% or higher and credit rating "
              "agency metrics that are consistent with a solid investment grade credit rating' (RELX Annual Report 2025, 20-F ex 15.2, "
              "0001104659-26-017277, p.72). History FY21-25: 2.4x, 2.1x, 2.0x, 1.8x, 2.0x (AR25 p.67-68).",
    "rating": "Moody's A3, S&P A-, Fitch BBB+ (brief dcf.wacc.credit_spread comment: RELX Capital term sheet, 24 Mar 2025, "
              "0001193125-25-061449; not re-fetched by the Risk agent)",
}

out = {
    "ticker": TICKER, "benchmark_index": INDEX, "price_currency": "GBp (pence)",
    "data": f"runs/RELX/2026-10-14/data/prices.csv, Yahoo dividend-adjusted daily closes, {stock.index[0].date()} to {end.date()}",
    "price_unit_check": {"jumps_over_50x": unit_jumps,
                         "largest_daily_moves": {str(k.date()): float(v) for k, v in largest_moves.items()},
                         "adjusted_price_range_gbp_pence": level_range, "last_adjusted_close_gbp_pence": unadjusted_last,
                         "verdict": "No 100x jump: the series is in pence throughout (adjusted range shown; the 13 Oct 2026 "
                                    "adjusted close equals the 2,771p unadjusted close in inputs.yaml)."},
    "own_regressions_vs_ftse100": own, "blume_adjusted_5y_monthly": blume_5y_monthly,
    "volatility_annualised": vol, "max_drawdown_5y_gbp_pence": dd, "max_drawdown_5y_ftse_points": dd_ftse,
    "peer_betas_5y_monthly_home_index": peer_betas, "peer_beta_errors": peer_errors,
    "peer_median_beta_5y_monthly_core7": peer_median,
    "leverage": lev,
    "valuation_beta": "NOT set here. See beta_evidence.json (bottom-up, PM rule in briefs/RELX.yaml dcf.wacc.beta).",
}
(HERE / "risk.json").write_text(json.dumps(out, indent=2, default=float))
for k, r in own.items():
    print(f"{k:12s} beta {r['beta']:.3f} se {r['std_error']:.3f} R2 {r['r_squared']:.3f} n {r['observations']} {r['start']}..{r['end']}")
for k, r in peer_betas.items():
    print(f"{k:28s} {r['ticker']:8s} vs {r['index']:7s} beta {r['beta']:.3f} se {r['std_error']:.3f} R2 {r['r_squared']:.3f} "
          f"n {r['observations']} jumps {r['unit_jumps']}")
print("peer errors", peer_errors, "median core", peer_median, "blume", blume_5y_monthly)
print("vol", vol, "\ndd", dd, "\nftse dd", dd_ftse, "\nunit jumps", unit_jumps, "largest", largest_moves.to_dict(), level_range)
print({k: (v["ratio_relx_def_gbp"], v["ratio_ex_leases_gbp"]) for k, v in lev.items() if isinstance(v, dict)})
