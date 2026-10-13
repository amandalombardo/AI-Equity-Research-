# Coca-Cola: taking the African bottler (CCBA) out of the base year

Prepared 13 Oct 2026. The Data agent STOPPED: Coca-Cola's own filings never give CCBA's revenue (only its assets and liabilities held for sale: $5,342m and $2,570m, FY25 10-K). The buyer, Coca-Cola HBC, did publish it.

## What the buyer published (deal announcement, 21 Oct 2025)
Found by web search. The PDFs sit on coca-colahellenic.com, which this environment cannot open, so **please open the first link and check the two numbers yourself** (slide "CCBA at a glance" or the factsheet):
- CCBA 2024 **net sales revenue €3,357m, EBIT €246m (7.3% margin)**: [CCBA factsheet](https://www.coca-colahellenic.com/content/dam/cch/us/documents/investors-and-financial/2026-q1-trading-update/coca-cola-hbc-factsheet-ccba-acquisition-q1-2026.pdf.downloadasset.pdf), [acquisition presentation](https://www.coca-colahellenic.com/content/dam/cch/us/documents/investors-and-financial/results-reports-and-presentations/2025/q3/coca-cola-hbc-2025-q3-update-and-acquisition-of-ccba-presentation.pdf.downloadasset.pdf)
- Price: 75% for $2.6bn, i.e. $3.4bn for 100%. Coca-Cola sells **41.5% for $1.3bn** and keeps **25%**, which Coca-Cola HBC has an option to buy. Completion expected in H2 2026, not yet done.

## What it means for the model (USD m)
| Item | Value | How |
|---|---|---|
| CCBA revenue in USD | 3,632 | €3,357m x 1.082 (2024 average USD per EUR, FRED DEXUSEU, 251 days) |
| CCBA EBIT in USD | 266 | €246m x 1.082 |
| Base-year revenue ex-CCBA | 44,309 | FY25 reported 47,941 - 3,632 |
| Comparable margin ex-CCBA | 33.2% | (15,013 - 266) / (48,062 - 3,632). Was 31.2% with CCBA in |
| Sale proceeds (added in bridge) | 1,300 | Coca-Cola's 41.5%, not yet received |
| Retained 25% stake (added in bridge) | 850 | 25% x $3.4bn deal value |

## Caveats (FLAGs)
1. CCBA's figures are for calendar 2024, Coca-Cola's base year is 2025. One year's growth is missing from what is removed: small.
2. Coca-Cola's $2,106m minority interests include CCBA's other owner (Gutsche family, 33.5%), whose share is not disclosed. Deducting all $2,106m is conservative: it could remove too much by up to c.$1.1bn (33.5% x $3.4bn), about $0.26 per share. Same trap as Diageo's EABL minorities (mistakes log row 14), but here the amount cannot be split, so it is flagged rather than fixed.

## Alternative
Keep CCBA in: base revenue $47,941m at 31.2% margin, no proceeds. But then FY26 growth should be the reported +3.5% (with the disposal headwind) and CCBA would stay in FY27-30 although it is being sold. It undoes your 6% decision, so I do not recommend it.
