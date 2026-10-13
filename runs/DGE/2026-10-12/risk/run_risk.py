"""Risk agent script: uses desk/risk.py only."""
import json
from pathlib import Path

import pandas as pd
import yaml

from desk import risk

RUN = Path(__file__).resolve().parents[1]
px = pd.read_csv(RUN / "data" / "prices.csv", index_col=0, parse_dates=True)
dge, ftse = px["DGE.L"].dropna(), px["^FTSE"].dropna()

# unit check: a pence/pound mix-up shows as a ~100x day-on-day jump
jumps = dge.pct_change().abs()
unit_jumps = jumps[jumps > 5].index.strftime("%Y-%m-%d").tolist()

end = dge.index[-1]
b5m = risk.beta(dge, ftse, "M")
b2w = risk.beta(dge[dge.index >= end - pd.DateOffset(years=2)], ftse[ftse.index >= end - pd.DateOffset(years=2)], "W")
b5w = risk.beta(dge, ftse, "W")
vol1 = risk.annualised_volatility(dge[dge.index >= end - pd.DateOffset(years=1)])
vol5 = risk.annualised_volatility(dge)
ftse_vol5 = risk.annualised_volatility(ftse)
dd = risk.max_drawdown(dge)
lev = 20869 / 6650  # adjusted net borrowings / adjusted EBITDA, FY26 20-F p.186
out = {"beta_5y_monthly": b5m, "beta_2y_weekly": b2w, "beta_5y_weekly": b5w,
       "volatility_1y_daily": vol1, "volatility_5y_daily": vol5, "ftse_volatility_5y_daily": ftse_vol5,
       "max_drawdown_5y": dd, "price_unit_jumps": unit_jumps,
       "leverage_adj_net_borrowings_to_adj_ebitda": lev, "leverage_target_range": [2.5, 3.0],
       "recommended_beta": None}
(Path(__file__).parent / "risk.json").write_text(json.dumps(out, indent=2, default=float))
# The valuation beta follows the PM's rule in the brief (bottom-up industry beta) and is written to
# inputs.yaml only by beta_evidence.py. This script reports regressions as cross-checks and never writes beta
# (Codex audit RISK-01, 12 Oct 2026: it used to overwrite the bottom-up beta with the peer median).
print(json.dumps(out, indent=1, default=float))

# ---- peer beta cross-check (step 3): 5y monthly beta vs each peer's home index, prices from Yahoo Finance
from desk.data_sources import prices  # noqa: E402

peers = {"Pernod Ricard": ("RI.PA", "^FCHI"), "Remy Cointreau": ("RCO.PA", "^FCHI"),
         "Campari": ("CPR.MI", "FTSEMIB.MI"), "Brown-Forman": ("BF-B", "^GSPC")}
peer_betas = {}
for name, (t, ix) in peers.items():
    b = risk.beta(prices(t), prices(ix), "M")
    peer_betas[name] = {"ticker": t, "index": ix, **b}
med = float(pd.Series([p["beta"] for p in peer_betas.values()]).median())
blume = 0.67 * b5m["beta"] + 0.33  # Blume adjustment: pulls a raw beta towards 1
out.update({"peer_betas_5y_monthly": peer_betas, "peer_median_beta": med, "dge_blume_adjusted_beta": blume})
out["recommended_beta"] = "see beta_evidence.json: bottom-up industry beta (PM rule in briefs/DGE.yaml)"
out["recommendation_reason"] = (f"DGE 5y monthly beta {b5m['beta']:.2f} has R2 {b5m['r_squared']:.2f} and the peer median is {med:.2f}; "
                                "both are cross-checks only. The valuation beta is set by the brief's bottom-up rule.")
(Path(__file__).parent / "risk.json").write_text(json.dumps(out, indent=2, default=float))
print({k: round(v["beta"], 3) for k, v in peer_betas.items()}, {k: round(v["r_squared"], 3) for k, v in peer_betas.items()}, "median", med, "blume", blume)
