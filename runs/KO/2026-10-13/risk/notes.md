# Risk agent notes: KO, run date 2026-10-13

All prices are in **US dollars (USD)**: KO and its peers trade on US exchanges. The S&P 500 (^GSPC) is in index points. Prices are adjusted for dividends and splits (Yahoo Finance, from `data/prices.csv` for KO and ^GSPC, and fetched live on 13 Oct 2026 for the peers). Money figures are USD m.

## STOP: beta for the WACC is MISSING

- **Brief rule** (`briefs/KO.yaml` dcf.wacc.beta): use the bottom-up beta. Take Damodaran's US "Beverage (Soft)" unlevered beta (Betas by Sector (US), January 2026) and relever it at KO's market debt-to-equity (D/E). KO's own regressions are only a cross-check.
- **What I tried:** I could not reach the source. The network proxy refused all of these with HTTP CONNECT 403 (organisation policy) on 13 Oct 2026:
  - `https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/Betas.html`
  - `.../pc/datasets/betas.xls`
  - the same page over http (the hostname would not resolve)
  - `www.stern.nyu.edu`
  - the web.archive.org copy

  The attempts are logged in `beta_evidence.json`. Nothing in the repo holds the US soft-beverage number. The Diageo run used Damodaran's *Global Alcoholic* table, which is a different industry. I did **not** use a number from memory.
- **inputs.yaml** now has `beta: {value: null, status: MISSING - STOP, ...}`. The valuation should not run until this is filled.
- **Ready for when the number arrives:** KO's market D/E = 0.07112 / (1 - 0.07112) = **0.0766**. With tax at 23.7%, the Hamada relevering factor is 1 + (1 - 0.237) x 0.0766 = **1.0584**. So the levered beta = Damodaran unlevered beta x 1.0584. To finish, set `UNLEVERED_FROM_SOURCE` in `beta_evidence.py`, cite the source, and rerun it. It is the only script that writes `beta` (Codex audit RISK-01). `run_risk.py` never writes it.
- **Ways to unblock (PM decision):**
  - Amanda downloads betas.xls (US, Jan 2026) and puts it in the run folder, or
  - the proxy allow-list is changed to include pages.stern.nyu.edu.

## Cross-checks (not used for the WACC)

The "se" column is the standard error. The 95% range is beta +/- 1.96 x standard error.

| KO vs S&P 500 | beta | se | 95% range | R-squared | n |
|---|---|---|---|---|---|
| 5y monthly | 0.30 | 0.13 | 0.04 to 0.56 | 0.08 | 60 |
| 2y weekly | 0.13 | 0.11 | -0.09 to 0.34 | 0.01 | 104 |
| 5y weekly | 0.35 | 0.06 | 0.23 to 0.46 | 0.12 | 261 |

- **These betas are not reliable.** R-squared is 1-12%, so the market explains very little of KO's moves. The 2-year weekly beta is not statistically different from zero. That is why the brief's bottom-up rule exists.
- The Blume-adjusted 5y monthly beta (0.67 x raw + 0.33) is 0.53.
- The last month (October) and the last week are part-periods ending 13 Oct 2026.
- **Peer betas** (5y monthly vs the S&P 500, n = 60 each):

  | Peer | beta | se | R-squared |
  |---|---|---|---|
  | PepsiCo | 0.33 | 0.13 | 0.10 |
  | Keurig Dr Pepper | 0.39 | 0.16 | 0.09 |
  | Monster | 0.54 | 0.19 | 0.13 |

  - The core median is **0.39**.
  - CCEP (optional peer, a bottler, shown separately) has a beta of 0.56.
  - Unlevered with each peer's net-debt D/E from `data/peers.csv`, the median is 0.28. **ASSUMPTION:** this step uses the 21% US statutory tax rate, for the cross-check only.
  - All peer regressions are as noisy as KO's own.

## Volatility and drawdown (KO, USD)

- **Annualised volatility, daily returns:** 18.9% over 1 year and 16.7% over 5 years. The S&P 500 was 17.0% over 5 years.
- **Maximum drawdown over 5 years:** -17.3%. The peak was 22 Apr 2022 at $58.08 (adjusted) and the trough was 5 Oct 2023 at $48.05 (adjusted).

## Price units

- KO is quoted in USD (`company.price_currency`), and there is no ADR.
- No day-on-day move was larger than 50%, so there is no sign of a 100x unit jump (a cents/dollar mix-up).
- The adjusted price range is $45.53 to $91.44.

## Leverage (FY25, USD m, FY25 10-K figures via `data/`)

- **Net debt** is 29,686. It excludes CCBA debt held for sale and excludes operating leases.
- **EBITDA**, defined as operating income + D&A 1,050:
  - reported: 13,762 + 1,050 = 14,812, giving **2.00x** net debt / EBITDA
  - comparable: 15,013 + 1,050 = 16,063, giving **1.85x**
- **Including leases** of 1,722, the reported ratio is 2.12x.
- **Interest cover** (reported EBIT / interest expense 1,654) is 8.3x.
- **Rating:** A+, as stated in the brief (credit_spread comment). This leverage is consistent with a single-A credit.
- **KO's own leverage target: MISSING.** There is none in the brief or the data folder, and I did not take it from memory. Diageo's 2.5-3.0x range does not apply to KO.
- **FLAG:** EBITDA includes CCBA, but net debt excludes CCBA's debt (1,435) and cash (178). The ratio mixes the two bases slightly.
- **Debt weight:** the market debt weight is 7.1%. That is low, so relevering adds only about 6% to the unlevered beta.

## Files

- `run_risk.py`: cross-checks only, uses `desk/risk.py`, writes `risk.json`
- `beta_evidence.py`: the only script that writes `beta` to inputs.yaml, writes `beta_evidence.json`
- `risk.json`, `beta_evidence.json`

## Confidence

- **High:** the regressions, volatility and drawdown. They are mechanical, computed with desk functions on sourced prices.
- **Medium:** leverage, because of the CCBA basis mismatch and the missing target.
- **The valuation beta: none.** It is MISSING (STOP).

## Update 2026-10-13 18:10 (Claude, after the PM supplied the source file)
The STOP above is resolved. The PM uploaded Damodaran's betas.xls (saved as data/damodaran_betas_us_jan2026.xls; sheet "Industry Averages", updated 2026-01-05). Row "Beverage (Soft)", 27 firms: unlevered beta corrected for cash 0.5755 (2022-26 average 0.8205). `beta_evidence.py` was re-run with that value: beta = 0.5755 x 1.0584 = **0.6091**, now in inputs.yaml.
