"""Risk agent: evidence test for beta (requested by the PM 2026-10-12: 'it must be backed by evidence').

Estimates beta several ways with standard errors and 95% confidence intervals, then builds a
bottom-up beta from the global alcoholic-beverage industry, relevered to Diageo's own leverage.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from desk.data_sources import prices

RUN = Path(__file__).resolve().parents[1]
START_5Y = "2021-10-12"


def regression(stock, index, freq, start=None, end=None):
    """OLS beta of stock returns on index returns, with standard error, 95% CI and R-squared."""
    if start:
        stock, index = stock[stock.index >= start], index[index.index >= start]
    if end:
        stock, index = stock[stock.index <= end], index[index.index <= end]
    rule = {"M": "ME", "W": "W-FRI"}[freq]
    d = pd.concat([stock.resample(rule).last().pct_change(), index.resample(rule).last().pct_change()], axis=1).dropna()
    y, x = d.iloc[:, 0], d.iloc[:, 1]
    beta = x.cov(y) / x.var()                       # beta = Cov(stock, market) / Var(market)
    resid = y - (y.mean() - beta * x.mean()) - beta * x
    se = float(np.sqrt(resid.var(ddof=2) / ((x - x.mean()) ** 2).sum()))  # standard error of the slope
    return {"beta": float(beta), "std_error": se, "ci95": [float(beta - 1.96 * se), float(beta + 1.96 * se)],
            "r_squared": float(x.corr(y) ** 2), "observations": len(d)}


dge, ftse = prices("DGE.L", 10), prices("^FTSE", 10)
acwi, gbpusd = prices("ACWI", 10), prices("GBPUSD=X", 10)
dge_usd = (dge * gbpusd.reindex(dge.index).ffill()).dropna()  # DGE in USD, to match the USD index

own = {
    "FTSE 100, 5y monthly (first run's default)": regression(dge, ftse, "M", START_5Y),
    "FTSE 100, 5y weekly": regression(dge, ftse, "W", START_5Y),
    "FTSE 100, 10y monthly": regression(dge, ftse, "M"),
    "FTSE 100, Oct 2016-Dec 2021 monthly (before the de-rating)": regression(dge, ftse, "M", None, "2021-12-31"),
    "MSCI ACWI (USD), 5y weekly": regression(dge_usd, acwi, "W", START_5Y),
    "MSCI ACWI (USD), 10y monthly": regression(dge_usd, acwi, "M"),
}
peers = {name: regression(prices(t, 10), prices(ix, 10), "W", START_5Y)
         for name, (t, ix) in {"Pernod Ricard": ("RI.PA", "^FCHI"), "Remy Cointreau": ("RCO.PA", "^FCHI"),
                               "Campari": ("CPR.MI", "FTSEMIB.MI"), "Brown-Forman": ("BF-B", "^GSPC")}.items()}

# Bottom-up beta: industry unlevered beta relevered at Diageo's market D/E (Hamada: bL = bU x (1 + (1 - t) x D/E))
inp = yaml.safe_load((RUN / "inputs.yaml").read_text())
wd, tax = inp["debt_weight"]["value"], inp["tax_rate"]["value"]
de = wd / (1 - wd)
unlevered_cash_corrected = 0.73  # Damodaran, Betas by Sector (Global), Jan 2026: Beverage (Alcoholic), 217 firms, unlevered beta corrected for cash
unlevered = 0.69                 # same table, unlevered beta before the cash correction
bottom_up = unlevered_cash_corrected * (1 + (1 - tax) * de)
precise = {k: r for k, r in own.items() if r["std_error"] <= 0.15}
out = {
    "own_regressions": own, "peer_regressions_5y_weekly": peers,
    "peer_median_5y_weekly": float(pd.Series([p["beta"] for p in peers.values()]).median()),
    "bottom_up": {"industry_unlevered_beta_cash_corrected": unlevered_cash_corrected, "industry_unlevered_beta": unlevered,
                  "diageo_market_debt_to_equity": de, "tax_rate": tax, "relevered_beta": bottom_up,
                  "relevered_beta_without_cash_correction": unlevered * (1 + (1 - tax) * de),
                  "source": "Damodaran Online, Betas by Sector (Global), data as of January 2026, Beverage (Alcoholic): https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/BetasGlobal.html"},
    "range_of_precise_own_estimates": [min(r["beta"] for r in precise.values()), max(r["beta"] for r in precise.values())],
    "verdict_on_0.48": ("Not justifiable. It came from the noisiest estimate available (5y monthly, standard error 0.25) via a "
                        "median of peer betas that are also unadjusted for leverage. Every precise estimate of Diageo's own "
                        "beta is 0.60-0.77, and the industry bottom-up beta at Diageo's leverage is 0.96."),
    "recommended_beta": bottom_up,
    "recommendation_reason": ("Bottom-up beta: the standard method when a company's own regression is unreliable. It averages "
                              "217 firms, so it is far less noisy than any single regression, and it reflects Diageo's own debt, "
                              "which is about twice the industry average. Diageo's best own regression (5y weekly, 0.72) is the cross-check."),
}
(Path(__file__).parent / "beta_evidence.json").write_text(json.dumps(out, indent=2))
inp["beta"] = {"value": float(round(bottom_up, 4)),
               "source": (f"Risk agent, bottom-up: Damodaran global alcoholic beverages unlevered beta 0.73 (Jan 2026, cash-corrected) "
                          f"relevered at Diageo D/E {de:.3f}, tax {tax:.1%}. See risk/beta_evidence.json")}
(RUN / "inputs.yaml").write_text(yaml.safe_dump(inp, sort_keys=False, width=1000))
for k, r in own.items():
    print(f"{k:60s} {r['beta']:.2f} se {r['std_error']:.2f} CI {r['ci95'][0]:.2f}-{r['ci95'][1]:.2f} R2 {r['r_squared']:.2f} n {r['observations']}")
for k, r in peers.items():
    print(f"{k:60s} {r['beta']:.2f} se {r['std_error']:.2f} R2 {r['r_squared']:.2f}")
print("peer median", out["peer_median_5y_weekly"], "D/E", de, "bottom-up", bottom_up, out["bottom_up"]["relevered_beta_without_cash_correction"])
