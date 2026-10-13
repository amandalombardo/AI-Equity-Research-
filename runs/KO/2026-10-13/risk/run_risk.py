"""Risk agent script for KO (cross-checks only). Uses desk/risk.py for beta, volatility and drawdown.

This script NEVER writes `beta` to inputs.yaml. The valuation beta follows the PM's rule in briefs/KO.yaml
(bottom-up industry beta) and is written only by beta_evidence.py (Codex audit RISK-01).
All prices are in US dollars (KO, peers) or index points (^GSPC); adjusted for dividends and splits.
"""
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from desk import risk
from desk.data_sources import prices

RUN = Path(__file__).resolve().parents[1]
brief = yaml.safe_load((RUN.parents[2] / "briefs" / "KO.yaml").read_text())
bench = brief["company"]["benchmark_index"]          # ^GSPC, S&P 500
assert brief["company"]["price_currency"] == "USD"

px = pd.read_csv(RUN / "data" / "prices.csv", index_col=0, parse_dates=True)
ko, spx = px["KO"].dropna(), px[bench].dropna()
end = ko.index[-1]


def std_error(stock, index, freq):
    """Standard error of the regression slope (beta): sqrt(residual variance / sum of squared index deviations)."""
    d = pd.concat([risk.returns(stock, freq), risk.returns(index, freq)], axis=1, join="inner").dropna()
    y, x = d.iloc[:, 0], d.iloc[:, 1]
    b = x.cov(y) / x.var()                             # beta = Cov(stock, market) / Var(market)
    resid = y - (y.mean() - b * x.mean()) - b * x      # what the market does not explain
    return float(np.sqrt(resid.var(ddof=2) / ((x - x.mean()) ** 2).sum()))


def reg(stock, index, freq, years=None):
    """desk.risk.beta plus standard error and 95% confidence interval (beta +/- 1.96 x standard error)."""
    if years:
        start = end - pd.DateOffset(years=years)
        stock, index = stock[stock.index >= start], index[index.index >= start]
    out = risk.beta(stock, index, freq)
    se = std_error(stock, index, freq)
    out.update({"std_error": se, "ci95": [out["beta"] - 1.96 * se, out["beta"] + 1.96 * se]})
    return out


# 1. Unit check: a pence/pound (or cents/dollar) mix-up shows as a ~100x day-on-day jump. Flag any move > 50%.
daily = ko.pct_change().abs()
unit_jumps = daily[daily > 0.5].index.strftime("%Y-%m-%d").tolist()
ratio_range = [float(ko.min()), float(ko.max())]

# 2. Regressions vs the S&P 500 (cross-checks)
own = {"5y_monthly": reg(ko, spx, "M"), "2y_weekly": reg(ko, spx, "W", 2),
       "5y_weekly": reg(ko, spx, "W"), "2y_monthly": None}
own.pop("2y_monthly")
blume = 0.67 * own["5y_monthly"]["beta"] + 0.33     # Blume adjustment: pulls a raw beta towards the market's 1.0

# 3. Volatility (annualised standard deviation of daily returns) and maximum drawdown
vol1 = risk.annualised_volatility(ko[ko.index >= end - pd.DateOffset(years=1)])
vol5 = risk.annualised_volatility(ko)
spx_vol5 = risk.annualised_volatility(spx)
dd = risk.max_drawdown(ko)

# 4. Peer betas (5y monthly vs home index; all US-listed, so ^GSPC). Prices: Yahoo Finance, live 13 Oct 2026.
peers_csv = pd.read_csv(RUN / "data" / "peers.csv").set_index("ticker")
US_STATUTORY_TAX = 0.21   # ASSUMPTION for peer unlevering only: US federal statutory rate (IRC s.11), not peer-specific
peer_out = {}
for t in ["PEP", "KDP", "MNST", "CCEP"]:
    try:
        r = reg(prices(t, 5), prices(bench, 5), "M")
    except Exception as e:  # noqa: BLE001
        peer_out[t] = {"error": str(e)}
        continue
    row = peers_csv.loc[t] if t in peers_csv.index else None
    if row is not None and not pd.isna(row["net_debt_musd"]):
        de = max(float(row["net_debt_musd"]), 0.0) / float(row["market_cap_musd"])   # market D/E (net debt, floor 0)
        r["net_debt_to_equity"] = de
        r["unlevered_beta"] = r["beta"] / (1 + (1 - US_STATUTORY_TAX) * de)          # Hamada: bU = bL / (1 + (1-t) D/E)
    r["optional_show_separately"] = t == "CCEP"
    peer_out[t] = r
core = [peer_out[t]["beta"] for t in ["PEP", "KDP", "MNST"] if "beta" in peer_out[t]]
core_u = [peer_out[t]["unlevered_beta"] for t in ["PEP", "KDP", "MNST"] if "unlevered_beta" in peer_out[t]]

# 5. Leverage: net debt / EBITDA (FY25, USD m). EBITDA = operating income + depreciation & amortisation.
inp = yaml.safe_load((RUN / "inputs.yaml").read_text())
fin = pd.read_csv(RUN / "data" / "financials.csv")
get = lambda item, fy=2025: float(fin[(fin["item"] == item) & (fin["fiscal_year"] == fy)]["value_musd"].iloc[0])  # noqa: E731
net_debt, leases = inp["net_debt"]["value"], inp["lease_liabilities"]["value"]
da = get("depreciation_amortisation")
ebitda_rep = get("operating_profit_reported") + da          # reported (GAAP) EBITDA
ebitda_cmp = get("comparable_operating_income") + da        # comparable (non-GAAP) EBITDA
lev = {"net_debt_musd": net_debt, "lease_liabilities_musd": leases, "da_musd": da,
       "ebitda_reported_musd": ebitda_rep, "ebitda_comparable_musd": ebitda_cmp,
       "net_debt_to_ebitda_reported": net_debt / ebitda_rep,
       "net_debt_to_ebitda_comparable": net_debt / ebitda_cmp,
       "net_debt_incl_leases_to_ebitda_reported": (net_debt + leases) / ebitda_rep,
       "interest_cover_reported": get("operating_profit_reported") / get("interest_expense"),  # EBIT / interest expense
       "company_target_range": "MISSING: no KO leverage target in the brief or data folder (not taken from memory)",
       "credit_rating": "A+ (briefs/KO.yaml dcf.wacc.credit_spread comment, agreed 2026-10-13)",
       "debt_weight": inp["debt_weight"]["value"]}

out = {"currency": "USD (KO, peers); index points (^GSPC)", "benchmark_index": bench,
       "price_window": [str(ko.index[0].date()), str(end.date())], "price_observations": len(ko),
       "price_unit_jumps_over_50pct": unit_jumps, "ko_price_range_usd_adjusted": ratio_range,
       "own_regressions": own, "ko_blume_adjusted_5y_monthly": blume,
       "volatility_1y_daily": vol1, "volatility_5y_daily": vol5, "sp500_volatility_5y_daily": spx_vol5,
       "max_drawdown_5y": dd,
       "peer_betas_5y_monthly": peer_out, "peer_median_beta_core": float(np.median(core)),
       "peer_median_unlevered_beta_core": float(np.median(core_u)) if core_u else None,
       "peer_unlevering_tax_assumption": US_STATUTORY_TAX,
       "leverage": lev,
       "recommended_beta": "see beta_evidence.json: bottom-up rule in briefs/KO.yaml (Damodaran US Beverage (Soft))"}
(Path(__file__).parent / "risk.json").write_text(json.dumps(out, indent=2, default=float))
print(json.dumps(out, indent=1, default=float))
