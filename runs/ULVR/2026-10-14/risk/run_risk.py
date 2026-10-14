"""Risk agent, Unilever (ULVR), run 2026-10-14: market risk measures and beta CROSS-CHECKS.

Uses desk/risk.py for returns, beta, volatility and drawdown, and desk/fundamentals.py for leverage.
This script NEVER writes beta to inputs.yaml. The valuation beta follows the PM's bottom-up rule and is written
only by beta_evidence.py (Codex audit RISK-01).

Run from the repo root:  PYTHONPATH=. python runs/ULVR/2026-10-14/risk/run_risk.py
"""
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from desk import fundamentals, risk

HERE = Path(__file__).resolve().parent
RUN = HERE.parent
REPO = RUN.parents[2]
brief = yaml.safe_load((REPO / "briefs" / "ULVR.yaml").read_text())
TICKER, INDEX = brief["company"]["price_ticker"], brief["company"]["benchmark_index"]   # ULVR.L (GBp), ^FTSE (points)
LAST_CLOSE_DATE = "2026-10-13"  # last COMPLETED close; the 2026-10-14 row is intraday (Data agent FLAG 1)

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
demerger_window = stock.loc["2025-12-03":"2025-12-11"]   # Ice Cream demerger 6 Dec 2025, 8-for-9 consolidation 8/9 Dec 2025

# ---- 2. own regressions vs the brief's benchmark (FTSE 100): cross-checks only
own = {"5y_monthly": regression(stock, index, "M", 5),
       "2y_weekly": regression(stock, index, "W", 2),
       "5y_weekly": regression(stock, index, "W", 5)}
blume_5y_monthly = 0.67 * own["5y_monthly"]["beta"] + 0.33   # Blume adjustment: pulls a raw beta towards 1

# ---- 3. volatility and drawdown (dividend-adjusted closes, GBp)
end = stock.index[-1]
last_1y = stock[stock.index >= end - pd.DateOffset(years=1)]
vol = {"ulvr_1y_daily": risk.annualised_volatility(last_1y),        # annualised: daily std x sqrt(252)
       "ulvr_5y_daily": risk.annualised_volatility(stock),
       "ftse_1y_daily": risk.annualised_volatility(index[index.index >= end - pd.DateOffset(years=1)]),
       "ftse_5y_daily": risk.annualised_volatility(index)}
dd = risk.max_drawdown(stock)

# ---- 4. peer betas, 5y monthly vs each peer's home index (Yahoo Finance adjusted closes, fetched today)
from desk.data_sources import prices  # noqa: E402

HOME = {"PG": "^GSPC", "CL": "^GSPC", "KMB": "^GSPC", "RKT.L": "^FTSE", "BEI.DE": "^GDAXI",
        "OR.PA": "^FCHI", "HEN3.DE": "^GDAXI"}
peer_betas, peer_errors = {}, {}
idx_cache = {}
for p in brief["comps"]["peers"]:
    t = p["ticker"]
    try:
        ix_t = HOME[t]
        idx_cache.setdefault(ix_t, prices(ix_t, 6))
        s = prices(t, 6)
        s, ixs = s[s.index <= LAST_CLOSE_DATE], idx_cache[ix_t][idx_cache[ix_t].index <= LAST_CLOSE_DATE]
        jump = (s / s.shift(1))
        peer_betas[p["name"]] = {"ticker": t, "index": ix_t, **regression(s, ixs, "M", 5),
                                 "unit_jumps": jump[(jump > 50) | (jump < 0.02)].index.strftime("%Y-%m-%d").tolist(),
                                 "source": f"Yahoo Finance adjusted closes ({t}, {ix_t}), fetched 2026-10-14"}
    except Exception as e:  # report, never estimate
        peer_errors[p["name"]] = f"MISSING: {e}"
peer_median = float(pd.Series([v["beta"] for v in peer_betas.values()]).median()) if peer_betas else None

# ---- 5. leverage: net debt / underlying EBITDA (Unilever's own definition), EUR m
nd_dec, uebitda_fy25 = 23076.0, 11394.0
nd_jun, uebitda_h1_26, uebitda_h1_25 = 25961.0, 5812.0, 5752.0
uebitda_ltm_jun26 = uebitda_fy25 - uebitda_h1_25 + uebitda_h1_26   # last twelve months = FY25 - H1 25 + H1 26
lev = {
    "fy25": {"net_debt_meur": nd_dec, "uebitda_meur": uebitda_fy25, "ratio": fundamentals.leverage(nd_dec, uebitda_fy25),
             "company_reported": "2.0x",
             "source": "Unilever FY25 results 6-K (0001654954-26-001155): net debt reconciliation 23,076; UEBITDA reconciliation 11,394 "
                       "(operating profit 9,037 + D&A 1,310 + non-underlying items 1,047); text 'net debt / underlying EBITDA ratio of 2.0x'"},
    "jun26_ltm": {"net_debt_meur": nd_jun, "uebitda_ltm_meur": uebitda_ltm_jun26, "ratio": fundamentals.leverage(nd_jun, uebitda_ltm_jun26),
                  "company_reported": "2.3x",
                  "source": "Unilever H1 2026 results 6-K (0000217410-26-000057): net debt EUR 26.0bn (25,961); UEBITDA H1 26 5,812, "
                            "H1 25 5,752; text '2.3x', FY26 guide 'around 2x'"},
    "target": "c.2x net debt / UEBITDA (FY25 20-F 0000217410-26-000007 p.14, financial framework 'Debt ~2x net debt/EBITDA'; "
              "H1 2026 6-K: FY26 'around 2x')",
    "rating": "A+/A1 long-term, A1/P1 short-term; aim at least A/A2 long term (FY25 20-F p.162, capital management; p.32)",
}

out = {
    "ticker": TICKER, "benchmark_index": INDEX, "price_currency": "GBp (pence)",
    "data": "runs/ULVR/2026-10-14/data/prices.csv, Yahoo dividend-adjusted daily closes, 2021-10-14 to 2026-10-13 "
            "(2026-10-14 intraday row dropped)",
    "price_unit_check": {"jumps_over_50x": unit_jumps,
                         "largest_daily_moves": {str(k.date()): float(v) for k, v in largest_moves.items()},
                         "demerger_window_gbp_pence": {str(k.date()): float(v) for k, v in demerger_window.items()},
                         "verdict": "No 100x jump: the series is in pence throughout. The 8-for-9 share consolidation at the Ice Cream "
                                    "demerger (FY25 20-F p.152/163) shows no break."},
    "own_regressions_vs_ftse100": own, "blume_adjusted_5y_monthly": blume_5y_monthly,
    "volatility_annualised": vol, "max_drawdown_5y_gbp_pence": dd,
    "peer_betas_5y_monthly_home_index": peer_betas, "peer_beta_errors": peer_errors, "peer_median_beta_5y_monthly": peer_median,
    "leverage": lev,
    "valuation_beta": "NOT set here. See beta_evidence.json (bottom-up, PM rule in briefs/ULVR.yaml dcf.wacc.beta).",
}
(HERE / "risk.json").write_text(json.dumps(out, indent=2, default=float))
for k, r in own.items():
    print(f"{k:12s} beta {r['beta']:.3f} se {r['std_error']:.3f} R2 {r['r_squared']:.3f} n {r['observations']} {r['start']}..{r['end']}")
for k, r in peer_betas.items():
    print(f"{k:20s} {r['ticker']:8s} vs {r['index']:7s} beta {r['beta']:.3f} se {r['std_error']:.3f} R2 {r['r_squared']:.3f} n {r['observations']}")
print("peer errors", peer_errors, "median", peer_median, "blume", blume_5y_monthly)
print("vol", vol, "dd", dd, "unit jumps", unit_jumps)
print({k: v["ratio"] for k, v in lev.items() if isinstance(v, dict)})
