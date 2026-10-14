# Risk agent notes: Unilever PLC (ULVR), run 2026-10-14

## Update 14 Oct 2026: risk-free rate changed by PM decision 11 (supersedes the 7.60% below)
The PM changed the risk-free rate to **3.45%** (German 10-year Bund on the run date; source in `../inputs.yaml`, which flags that it comes from a data aggregator). **Beta is unchanged at 0.8844.**
Cost of equity (CAPM, via `desk.dcf.cost_of_equity`) = 3.45% + 0.8844 x 5.0% = **7.872%**. This supersedes the 7.60% figure below.
The sensitivities' costs of equity each rise by the same +0.27 points: June 2026 net debt 7.94%, no cash correction 7.70%, Damodaran 2020-24 average 8.45%.
`beta_evidence.json` still shows the old costs of equity (at 3.18%). I did not re-run it, as instructed. Its beta values are unaffected.

Money in EUR m unless labelled. Share prices in pence (GBp). Index in points.

## What I did
1. `run_risk.py` (desk/risk.py and desk/fundamentals.py) computes the cross-checks and writes `risk.json`. **It never writes beta.**
2. `beta_evidence.py` is **the only script that writes `beta` to `../inputs.yaml`**, and it follows the brief's rule (Codex audit RISK-01). It reads the Damodaran value from the PM's file itself and stops if the value, firm count or file date does not match. It writes `beta_evidence.json` and adds only the `beta` entry to inputs.yaml (6 lines added; the script checks that every other entry is unchanged).
   Run from the repo root: `PYTHONPATH=. python runs/ULVR/2026-10-14/risk/run_risk.py`, then `... beta_evidence.py <betaGlobal.xlsx>`. The .xls was converted to .xlsx with LibreOffice in a scratch folder.
3. Prices: `data/prices.csv`, Yahoo dividend-adjusted daily closes, 14 Oct 2021 to **13 Oct 2026**. I dropped the 14 Oct 2026 row because it is an intraday price (Data agent FLAG 1).

## Valuation beta (PM rule: bottom-up): **0.8844**
| Step | Value | Source |
|---|---|---|
| Industry unlevered beta corrected for cash | **0.774144424006051** (matches the brief) | Damodaran betaGlobal.xls dated 2026-01-05, sheet "Industry Averages", row "Household Products", 588 firms (PM upload 14 Oct 2026) |
| Market cap | 2,154.328m shares x 4,710.5p / 100 = **GBP 101,479.6m** x 1.18190 EUR per GBP = **EUR 119,938.7m** | inputs.yaml: TVR 6-K 31 Aug 2026; ULVR.L close 13 Oct 2026; FRED 9 Oct 2026 |
| Net debt | **EUR 23,076m** at 31 Dec 2025 (leases inside) | FY25 results 6-K 0001654954-26-001155; 20-F note 15C p.164 |
| D/E (market) | 23,076 / 119,938.7 = **0.1924** | |
| Tax | 26.0% | brief dcf.tax_rate |
| **Relevered beta (Hamada)** | 0.7741 x (1 + 0.74 x 0.1924) = **0.8844**, so cost of equity = 3.18% + 0.8844 x 5.0% = **7.60%** | |

Sensitivities (not used):
| Case | Beta | Cost of equity |
|---|---|---|
| Net debt at 30 Jun 2026, EUR 25,961m (H1 2026 6-K 0000217410-26-000057, "EUR 26.0 billion"), D/E 0.2165 | 0.8981 | 7.67% (+0.07 pt) |
| Unlevered beta without the cash correction, 0.7432 (same file) | 0.8490 | 7.42% |
| Damodaran 2020-24 average, cash-corrected, 0.8752 (same file) | 0.9998 | 8.18% |

## Cross-checks (never used for the WACC)
ULVR.L vs FTSE 100 (`^FTSE`, the brief's benchmark):
| Regression | Beta | Std error | 95% range | R-squared | Obs |
|---|---|---|---|---|---|
| 5y monthly | 0.91 | 0.19 | 0.55 to 1.28 | 0.30 | 60 |
| 2y weekly | 0.43 | 0.15 | 0.15 to 0.72 | 0.08 | 104 |
| 5y weekly | 0.54 | 0.08 | 0.37 to 0.70 | 0.14 | 261 |
| Blume-adjusted 5y monthly | 0.94 | | | | |

Peer betas, 5y monthly vs home index (Yahoo adjusted closes fetched 14 Oct 2026: a non-filing source; raw, not relevered). P&G 0.39 (S&P 500), Colgate 0.34 (S&P 500), Kimberly-Clark 0.28 (S&P 500), Reckitt 0.80 (FTSE 100), Beiersdorf 0.45 (DAX), L'Oreal 0.87 (CAC 40), Henkel pref 0.67 (DAX). **Median 0.45.** Standard errors are 0.15 to 0.23, and no peer series has a 100x jump.

Other risk measures (ULVR.L, GBp, dividend-adjusted):
| Measure | Value |
|---|---|
| Volatility, 1y daily, annualised | 22.4% (FTSE 100: 11.6%) |
| Volatility, 5y daily, annualised | 19.2% (FTSE 100: 12.5%) |
| Max drawdown, 5y | **-25.5%**: from 5,470.6p (24 Feb 2026) to 4,077.7p (4 Jun 2026), both adjusted prices. The fall spans the Foods/McCormick announcement (31 Mar 2026) |

## Price unit check
**No 100x jump.** The series is in pence throughout. The largest daily move is 9.4% (31 May 2022). The 8-for-9 share consolidation at the Ice Cream demerger (6-9 Dec 2025; FY25 20-F p.152 and p.163) shows no break: 4,679p on 8 Dec to 4,845p on 9 Dec, +3.6%.

## Leverage (Unilever's definition: net debt / underlying EBITDA)
| Date | Net debt | UEBITDA | Ratio | Company says |
|---|---|---|---|---|
| 31 Dec 2025 | EUR 23,076m | EUR 11,394m (op. profit 9,037 + D&A 1,310 + non-underlying 1,047; FY25 results 6-K) | **2.03x** | 2.0x |
| 30 Jun 2026 | EUR 25,961m | EUR 11,454m LTM (11,394 - H1 25 5,752 + H1 26 5,812; H1 2026 6-K) | **2.27x** | 2.3x |

Target: c.2x (FY25 20-F p.14, financial framework; H1 2026 6-K: "around 2x" for FY26). Rating: **A+/A1** long-term, A1/P1 short-term, with an aim of at least A/A2 (FY25 20-F p.162). Leverage is at target at year-end and 0.3x above it in June, after the EUR 1.5bn buyback.

## FLAGs
1. **The bottom-up beta (0.88) is above Unilever's own weekly betas.** It sits outside the 95% range of both the 5y weekly (0.37-0.70) and the 2y weekly (0.15-0.72) regressions. Only the 5y monthly regression (0.91, range 0.55-1.28) agrees with it. With the most precise own estimate (5y weekly, 0.54) the cost of equity would be about 1.7 points lower (5.86% vs 7.60%). I follow the PM's rule: a 588-firm industry average is less noisy than one stock's regression, and the R-squared values here are low (0.08-0.30). But the gap is material, and the PM should know it.
2. **D/E mixes dates.** Net debt is at 31 Dec 2025 (before the EUR 1.5bn H1 buyback), while the share count is after it. Using June net debt raises beta by only 0.014 (+0.07 pt cost of equity). After the Foods sale closes (expected mid-2027), the USD 15.7bn cash will cut net debt, but the Foods EBITDA leaves too. The base case D/E does not reflect that.
3. **`desk/` has no relever (Hamada) function and no standard error for beta.** Both are computed in `beta_evidence.py` / `run_risk.py`, with a comment naming each formula, the same way as for Diageo. Suggest adding `risk.relever_beta` and a `std_error` field in `risk.beta`, on a branch with tests, for Amanda's approval (CLAUDE.md rule 1).
4. **Peer betas are low and noisy.** The three US peers are measured against the S&P 500, which is now dominated by technology stocks, so they read 0.28-0.39. They are raw (not relevered) and come from Yahoo (not a filing). They should not be used for the WACC.
5. **The last monthly and weekly returns are partial** (to 13 Oct). desk/risk.py labels them with the period-end date (31 Oct, 16 Oct). This is cosmetic.
6. **Tests:** pytest is not installed in this environment, so `python -m pytest` could not run. I changed no code in `desk/`.

## Missing
Nothing needed for beta or leverage is missing.

## Confidence
High on the bottom-up calculation and the leverage figures (each matches the company's own ratio). Medium on beta as a measure of Unilever's risk: the own-regression evidence ranges from 0.43 to 0.91 (FLAG 1).
