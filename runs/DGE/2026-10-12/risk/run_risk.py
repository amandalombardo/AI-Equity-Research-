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
       "recommended_beta": b5m["beta"]}
(Path(__file__).parent / "risk.json").write_text(json.dumps(out, indent=2, default=float))
inp_path = RUN / "inputs.yaml"
inp = yaml.safe_load(inp_path.read_text())
inp["beta"] = {"value": float(round(b5m["beta"], 4)),
               "source": f"Risk agent, 5y monthly vs FTSE 100, R2={b5m['r_squared']:.2f}, n={b5m['observations']}"}
inp_path.write_text(yaml.safe_dump(inp, sort_keys=False, width=1000))
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
# Recommendation: the DGE regression explains under 5% of its returns (R2 < 0.05), so it is not a reliable
# estimate. Use the peer median instead and flag it for the PM.
out["recommended_beta"] = med
out["recommendation_reason"] = (f"DGE 5y monthly beta {b5m['beta']:.2f} has R2 {b5m['r_squared']:.2f}: statistically meaningless. "
                                f"Using the peer median 5y monthly beta {med:.2f} instead. PM to confirm.")
(Path(__file__).parent / "risk.json").write_text(json.dumps(out, indent=2, default=float))
inp = yaml.safe_load(inp_path.read_text())
inp["beta"] = {"value": float(round(med, 4)),
               "source": (f"Risk agent: peer median 5y monthly beta (Pernod, Remy, Campari, Brown-Forman vs home indices). "
                          f"DGE's own 5y monthly vs FTSE 100 = {b5m['beta']:.2f}, R2={b5m['r_squared']:.2f}, n={b5m['observations']}, rejected as unreliable")}
inp_path.write_text(yaml.safe_dump(inp, sort_keys=False, width=1000))
print({k: round(v["beta"], 3) for k, v in peer_betas.items()}, {k: round(v["r_squared"], 3) for k, v in peer_betas.items()}, "median", med, "blume", blume)
