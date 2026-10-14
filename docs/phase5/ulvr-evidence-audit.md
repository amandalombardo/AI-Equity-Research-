# Unilever: evidence audit of every input (14 Oct 2026, before the rating is set)

Same test as the Diageo and Coca-Cola audits: does each number have a primary source, is it the latest evidence, and is it justifiable? Inputs file: runs/ULVR/2026-10-14/inputs.yaml. Result: every input has a source, but **one fails the "latest evidence" test (the risk-free rate is two months old)**. Two are judgements you already agreed. None changes the SELL.

## The one that fails: the risk-free rate is stale
| | Value | Source | Date |
|---|---|---|---|
| Used in the run | **3.18%** | FRED IRLTLT01DEM156N (OECD monthly average) | **August 2026** average: the latest month FRED publishes |
| Latest daily readings | **3.45%** (14 Oct), 3.50% (9 Oct) | [Trading Economics](https://tradingeconomics.com/germany/government-bond-yield) (also on [Bloomberg rates](https://www.bloomberg.com/markets/rates-bonds)); [thetrading.tools](https://www.thetrading.tools/germany-10-year-yield) | October 2026 |

Bund yields rose about 0.3 points since August (markets now price another ECB rate rise, per Trading Economics). The Diageo and Coca-Cola runs used the US 10-year yield **on the run date** (FRED DGS10, daily), so using a two-month-old average for Unilever is inconsistent with the desk's own practice. Weakness of the fix: no primary daily source is reachable from here (Bundesbank and ECB data sites are blocked); the daily figures come from data aggregators, which agree within 0.05 points.

| Risk-free | Cost of equity | WACC | Value per share | Rating |
|---|---|---|---|---|
| 3.18% (run) | 7.60% | 6.84% | 4,018p | SELL |
| **3.45% (14 Oct)** | 7.87% | 7.10% | **3,855p** | SELL |
| 3.50% (9 Oct) | 7.92% | 7.15% | 3,827p | SELL |

(Engine re-runs with the joint ventures re-valued at each cost of equity, scratch copies; credit spread 0.70% unchanged, it is from 12 Oct.)

## Inputs that pass (primary source, latest available)
| Input | Value | Primary source |
|---|---|---|
| Base sales ex-Foods | EUR 39,803m | FY25 results 6-K (50,503) less Form 425 perimeter (10,700) |
| Margin, growth, tax, capex, D&A, working capital | 17.7%; 0.5% then 1.6%; 26.0%; 3.15%; 2.6%; -11.98% | PM decisions 2, 3, 9, 10, each from 20-F / 6-K figures (evidence packs) |
| Net debt | EUR 23,076m | FY25 20-F (checked) |
| Leases inside net debt; pension surplus | 0; 0 (surplus 3,518) | FY25 20-F notes 15C, 16B |
| Shares | 2,154.3m | Total Voting Rights 6-K, 1 Sep 2026 |
| Share price | 4,710.5p | ULVR.L close 13 Oct 2026 (checked) |
| EUR per GBP | 1.1819 | FRED official noon rates, 9 Oct 2026 (Yahoo 12 Oct differs by 0.15%) |
| Dividends ex before run date | EUR 3,038.8m | FY25 and H1 2026 6-Ks |
| Buyback | EUR 1,507m | H1 2026 6-K cash flow (checked) |
| Foods consideration | EUR 33,955m | McCormick 10-Q share count (checked), MKC close 13 Oct (checked), FRED EUR/USD |
| Magnum stake | EUR 1,935m | TMICC prospectus share count, MICC.AS close 13 Oct (checked) |
| Other investments, Magnum balances, associates | EUR 902m, 500m, 15m | FY25 20-F notes 11, 13, 14, 17A |
| Beta | 0.8844 | Damodaran file you uploaded, relevered with FY25 20-F net debt |
| Minorities' share | 10.68% | FY25 20-F income statement and note 15B (FY24 HUL year, the most cautious of three) |
| Credit spread | 0.70% | FRED BAMLC0A3CA, 12 Oct 2026 |

## Judgements already agreed, with their evidence
- **Joint ventures, EUR 3,876m (Gordon on EUR 229m of dividends, decision 10):** the dividends are sourced (20-F note 11); growing them forever at 1.6% is the same assumption as the rest of Unilever.
- **Foods tax:** MISSING (decision 5), shown as 39.3p per EUR 1bn.

## Weak but outside the base case (flagged in the memo)
- Hindustan Unilever's share count (bear line only) is from Yahoo, not a filing.
- Four of seven peers' figures are from Yahoo; comps are a cross-check only.
- No independent industry growth forecast could be reached (research sites blocked); Unilever's own Euromonitor reference implies about 1.1-1.6% in euros, so 1.6% sits at the top of that range.
