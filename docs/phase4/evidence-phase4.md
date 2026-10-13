# Phase 4 evidence pack (13 Oct 2026)

Your rule: everything must be backed by evidence and justifiable. This covers the two open items: (A) when in the year Diageo's cash arrives (the mid-year question) and (B) a source check of every claim in the draft bear responses. Values are pence per ordinary share (GBp) unless stated.

## A. When does Diageo's cash arrive?

**The question.** The model assumes each year's free cash flow arrives in one lump on 30 June, the last day of the year (end-of-year discounting). The alternative assumes it arrives evenly through the year, so on average at the half-year point (mid-year discounting).

**Evidence: Diageo's own half-year cash flows** (free cash flow, Diageo's definition, USD m)

| Year | First half (Jul-Dec) | Full year | Share in first half | Average arrival point in the year* |
|---|---|---|---|---|
| FY25 | 1,696 | 2,748 | 61.7% | 0.44 years |
| FY26 | 1,532 | 3,211 | 47.7% | 0.51 years |

\* First-half cash counted at 0.25 years, second-half at 0.75 years (each half's midpoint). Our arithmetic.

Sources: FY26 interim results 6-K, 25 Feb 2026 (SEC accession 0001654954-26-001518), summary table: "Free cash flow $1,532m $(164)m", so H1 FY25 = 1,696; FY25 interim 6-K (accession 0001654954-25-001149): "Free cash flow increased by $0.1 billion to $1.7 billion"; full years from the 20-F FY26 "Movements in net borrowings" table (fundamentals/ratios.csv).

**What it shows.** In both years at least half the cash arrived by the end of December. On average the cash lands about half-way through the year (0.44 and 0.51 years), not on the last day (1.0). End-of-year discounting therefore waits about six months too long for the money, which understates value. Mid-year discounting matches the evidence.

**The terminal value must move too.** This part is maths, not opinion: a cash flow of 20 a year forever, received mid-year, at 10%, is worth 20 / 0.10 x 1.10^0.5 = 209.8. Moving only the five forecast years (and leaving the terminal value at year-end) gives 201.7, which is wrong. The engine had that error; it is fixed and tested (mistakes log row 15). Note: practitioner guides disagree on this point for the *exit-multiple* method, but our terminal value uses the Gordon growth formula, where the maths above applies.

| Option | Value | Rating | Above SELL line (1,505.7p) | Bear scenario |
|---|---|---|---|---|
| End-of-year (today) | 1,545p | HOLD (-7.7%) | 39p | 1,108p |
| **Mid-year, consistent (recommended)** | **1,627p** | **HOLD (-2.7%)** | **122p** | **1,180p** |
| Mid-year on the forecast only (inconsistent) | 1,566p | HOLD | 60p | not shown |

**Caveat (against my recommendation).** This change is a convention, not new information about Diageo's business, and it happens to make the HOLD sturdier. Your Excel model, if it uses year-end discounting, will now differ from the desk by about 5%. That is why I asked you to do the Excel check on today's basis first. Mid-year is then a one-line change.

## B. Source check of the draft bear responses

| # | Claim in the draft | Source | Status |
|---|---|---|---|
| 1 | 46% is the low end of FY27-29 profit guidance | briefs/DGE.yaml; CMD 6-K 6 Aug 2026 | Verified |
| 1 | 2017 rule: two thirds reinvested (about 33% kept); SELL line 33.6% | FY17 results 6-K 27 Jul 2017; valuation/sanity_checks.json | Verified |
| 1 | We can check FY27 interim margins in Feb 2027 | Diageo reported FY26 interims on 25 Feb 2026 (6-K above); Feb 2027 is inferred from that pattern | Inferred, labelled |
| 2 | ROIC 18.4%, 15.8%, 13.7%, 13.4% (FY23-26) | 20-F FY24-FY26 KPI tables | Verified |
| 2 | FY26 capex 6.1% of sales | 1,197 / 19,643 = 6.09%, 20-F FY26 cash flow statement | Verified |
| 3 | Management missed "every" 2023-26 target | 20-F p.110: both incentive metrics missed (organic sales CAGR -0.3% vs 4.0%; organic operating profit CAGR -3.4% vs 4.5%) | **Corrected** to "both" |
| 4 | 2% nominal growth implies little or no real growth | US 10-year breakeven inflation 2.35% on 8 Oct 2026 (FRED T10YIE), so 2% nominal is about -0.35% a year in real terms | **Now sourced** |
| 5 | Beta 0.96 is above "every reliable" own regression (0.60-0.77) | risk/beta_evidence.json: all six own regressions are 0.37 to 0.77; only the pre-2022 window's 95% range (0.51 to 1.02) reaches 0.96 | **Corrected** wording and range |
| 5 | 1% spread suits an A-band issuer; 2% prices in a downgrade | FRED, ICE BofA option-adjusted spreads on 8 Oct 2026: A-rated 0.69%, BBB 1.02%, high yield 3.15%. So 1% is already about the BBB average (cautious for an A-band company); 2% sits between BBB and high yield | **Now sourced**; the spreads are index averages across maturities, not 10-year only |
| 5 | After the disposals, leverage about 2.6x | Adjusted net debt about 3.14 x 6,650 = USD 20,881m (20-F p.186 ratio x adjusted EBITDA) less proceeds 3,318 = 17,563; / 6,650 = 2.64x. But proceeds are gross (before tax) and EABL's EBITDA leaves (its D&A is not sourced), so the true figure is higher | **Corrected** to "about 2.6x before tax and before EABL leaves, so somewhat higher in practice (our arithmetic)" |
| 6 | Bear agent calls -150p an upper bound | bear/challenges.md, challenge 6 | Verified |

Nothing in the draft changes the valuation; the corrections are to wording and sources.
