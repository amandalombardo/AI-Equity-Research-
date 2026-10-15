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

## Beta evidence test (added 2026-10-12 at the PM's request: "it must be backed by evidence")
`beta_evidence.py` writes `beta_evidence.json`. Each estimate is shown with its standard error and 95% confidence interval.

| Estimate | Beta | Std error | 95% range | R-squared |
|---|---|---|---|---|
| FTSE 100, 5y monthly (first run's default) | 0.37 | 0.25 | -0.12 to 0.85 | 0.04 |
| FTSE 100, 5y weekly | 0.72 | 0.11 | 0.51 to 0.93 | 0.15 |
| FTSE 100, 10y monthly | 0.60 | 0.13 | 0.33 to 0.86 | 0.15 |
| FTSE 100, Oct 2016-Dec 2021 monthly | 0.77 | 0.13 | 0.51 to 1.02 | 0.37 |
| MSCI ACWI (USD), 5y weekly | 0.70 | 0.09 | 0.53 to 0.87 | 0.20 |
| MSCI ACWI (USD), 10y monthly | 0.66 | 0.11 | 0.44 to 0.89 | 0.22 |
| Peers, 5y weekly (Pernod 0.85, Remy 1.02, Campari 0.52, Brown-Forman 0.62) | median 0.73 | | | |
| **Bottom-up: industry unlevered 0.73, relevered at Diageo's D/E 0.416 and tax 24.3%** | **0.96** | | | |

**Verdict on 0.48: not justifiable.** It came from the noisiest estimate (standard error 0.25, a range that includes zero), via a median of peer monthly betas that are also unadjusted for leverage. Every precise estimate of Diageo's own beta lies between 0.60 and 0.77.

**Beta now in inputs.yaml: 0.96 (bottom-up).** This is the standard method when a company's own regression is unreliable. The industry beta averages 217 global alcoholic-beverage firms (Damodaran, Betas by Sector (Global), January 2026: unlevered 0.73 after the cash correction, 0.69 before it, which gives 0.91). It is relevered for Diageo's debt: Diageo's D/E of 42% is about twice the industry's 20%. Cross-check: Diageo's best own regression is 0.72 (5y weekly). 0.96 sits just above its 95% range (0.51-0.93), so the two methods disagree modestly. **PM chose 0.96 (2026-10-12).**

## FLAGS
1. **[SUPERSEDED by the beta evidence test above: 0.48 rejected, 0.96 used.]** DGE's own beta is unreliable, so the first run used the peer median (0.48). The default 5y monthly beta is 0.37, but the FTSE 100 explains only 4% of Diageo's monthly moves (R-squared 0.04). Diageo fell 67% while the FTSE 100 rose to record highs: the share price was driven by company and sector news, not the market. A regression with that fit says almost nothing about systematic risk. The peer median is also low (0.48) for the same reason: the whole spirits sector de-rated on its own. **Both numbers understate the risk an investor actually experienced.** Volatility is 2.5x the index. Using beta 1.0 instead would add 2.6 points to the cost of equity (the Bear agent quantifies this).
2. **Leverage is above target:** 3.1x vs 2.5-3.0x. Management expects about 2.75x in FY27, once EABL and RCB complete.
3. **Partial periods:** the last monthly and weekly returns run to 12 October (a partial month and week). `desk/risk.py` labels them with the period-end date (31 Oct / 16 Oct). This is cosmetic: the data stops at 12 October.

## Confidence
High on the calculations. Low on beta as a measure of Diageo's risk.


## Source check, 15 Oct 2026 (mistakes log row 33)
The industry beta was typed as 0.73 (0.69 before the cash correction), rounded from a search snippet. Damodaran's own file (betaGlobal.xls, 5 Jan 2026, uploaded by the PM; sheet "Industry Averages", Beverage (Alcoholic), 217 firms) gives **0.7250** (0.6884 before the cash correction). risk/fix_beta_2026-10-15.py relevers 0.7250 at Diageo's current market D/E 0.4146 (debt weight 0.29311, after the 15 Oct diluted share count) and tax 24.3%: **beta 0.9526** (was 0.9601). No prices re-downloaded; the regressions above are unchanged. The tables above still show the superseded 0.96.
