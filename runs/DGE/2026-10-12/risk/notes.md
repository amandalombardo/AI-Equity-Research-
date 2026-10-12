# Risk agent notes: Diageo (DGE), run 2026-10-12

## What I did
I ran `run_risk.py`, which uses `desk/risk.py` only, on `data/prices.csv` (DGE.L in pence, FTSE 100 in index points, daily, 5 years to 2026-10-12, dividend-adjusted). Results are in `risk.json`.

| Measure | Value |
|---|---|
| Beta, 5y monthly vs FTSE 100 | 0.37 (R-squared 0.04, 60 observations) |
| Beta, 2y weekly vs FTSE 100 | 0.60 (R-squared 0.07, 104 observations) |
| Beta, 5y weekly vs FTSE 100 | 0.72 (R-squared 0.15, 261 observations) |
| Peer 5y monthly betas | Pernod 0.63, Remy 0.84, Campari 0.29, Brown-Forman 0.32; **median 0.48** |
| Volatility, 1y daily (annualised) | 31.6% (FTSE 100 5y: 12.5%) |
| Volatility, 5y daily (annualised) | 24.1% |
| Max drawdown, 5y | -66.8%, from 4,098p (2022-01-04) to 1,362p (2026-03-24), dividend-adjusted |
| Leverage: adjusted net borrowings / adjusted EBITDA | 3.14x vs target 2.5-3.0x (20-F p.186: 20,869 / 6,650) |

## Unit check
No 100x day-on-day jump in DGE.L, so there is no pence/pound mix-up in the series.

## FLAGS
1. **DGE's own beta is unreliable, so I used the peer median (0.48) in inputs.yaml. PM to confirm.** The default 5y monthly beta is 0.37, but the FTSE 100 explains only 4% of Diageo's monthly moves (R-squared 0.04). Diageo fell 67% while the FTSE 100 rose to record highs: the share price was driven by company and sector news, not the market. A regression with that fit says almost nothing about systematic risk. The peer median is also low (0.48) for the same reason: the whole spirits sector de-rated on its own. **Both numbers understate the risk an investor actually experienced.** Volatility is 2.5x the index. Using beta 1.0 instead would add 2.6 points to the cost of equity (the Bear agent quantifies this).
2. **Leverage is above target:** 3.1x vs 2.5-3.0x. Management expects about 2.75x in FY27, once EABL and RCB complete.
3. **Partial periods:** the last monthly and weekly returns run to 12 October (a partial month and week). `desk/risk.py` labels them with the period-end date (31 Oct / 16 Oct). This is cosmetic: the data stops at 12 October.

## Confidence
High on the calculations. Low on beta as a measure of Diageo's risk.
