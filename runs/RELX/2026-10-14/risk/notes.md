# Risk agent notes: RELX PLC (RELX / REL.L), run 2026-10-14

Money in GBP m unless labelled. Share prices in pence (GBp). Index in points. Prices to the 13 Oct 2026 close.

## What I did
1. `run_risk.py` (desk/risk.py, desk/fundamentals.py, desk/data_sources.prices for peers) computes the cross-checks and writes `risk.json`. **It never writes beta.**
2. `beta_evidence.py` is **the only script that writes `beta` to `../inputs.yaml`**, and it follows the brief's rule (Codex audit RISK-01). It reads the Damodaran value from the PM's file itself (checks the file's sha256, the value, the 86-firm count and the 5 Jan 2026 date, and stops if any differ). It writes `beta_evidence.json` and adds only the `beta` entry to inputs.yaml (7 lines; the script asserts every other entry is unchanged).
   Run from the repo root: `PYTHONPATH=. python runs/RELX/2026-10-14/risk/run_risk.py`, then `... beta_evidence.py <betaGlobal.xlsx>`. The .xls was converted to .xlsx with LibreOffice (`soffice --headless --convert-to xlsx`) in a scratch folder.
3. Prices: `data/prices.csv`, Yahoo dividend-adjusted daily closes, 14 Oct 2021 to 13 Oct 2026 (no intraday row).

## Valuation beta (PM rule: bottom-up): **0.9729**
| Step | Value | Source |
|---|---|---|
| Industry unlevered beta corrected for cash | **0.873735946265916** (matches the PM) | Damodaran betaGlobal.xls dated 2026-01-05, sheet "Industry Averages", row "Information Services", 86 firms |
| Market cap | 1,743.754727m shares x 2,771p / 100 = **GBP 48,319.4m** | inputs.yaml: 6-K 0000929869-26-000071 (25 Sep 2026); REL.L close 13 Oct 2026 |
| Net debt | **GBP 7,104m** at 31 Dec 2025 = 7,201 less 97 leases (brief excludes leases) | FY25 results 6-K 0000929869-26-000008 p.13 |
| D/E (market) | 7,104 / 48,319.4 = **0.1470** | |
| Tax | 22.8% | brief dcf.tax_rate |
| **Relevered beta (Hamada)** | 0.8737 x (1 + 0.772 x 0.1470) = **0.9729** | |

Cost of equity (CAPM, `desk.dcf.cost_of_equity`) = 5.45% + 0.9729 x 5.0% = **10.31%**.

**Difference from the PM card (0.974):** the card used net debt 7,201 including leases (and 1,747.0m shares). At 7,201 with the inputs.yaml share count the beta is 0.9743; as printed on the card, 0.9741. At the brief's 7,104 it is **0.9729, i.e. 0.0012 lower** (about -0.006 points of cost of equity). Immaterial, but 0.9729 is the value consistent with the brief's lease decision.

Sensitivities (not used):
| Case | D/E | Beta | Cost of equity |
|---|---|---|---|
| Net debt ex leases 30 Jun 2026, 8,614 (after H1 buybacks) | 0.178 | 0.994 | 10.42% |
| Net debt RELX definition 30 Jun 2026, 8,733 (PM option C) | 0.181 | 0.996 | 10.43% |
| Unlevered beta without cash correction, 0.8265 | 0.147 | 0.920 | 10.05% |
| Damodaran 2020-24 average, cash-corrected, 1.0729 | 0.147 | 1.195 | 11.42% |
| Publishing & Newspapers, 0.7788 (307 firms) | 0.147 | 0.867 | 9.79% |
| Business & Consumer Services, 0.9083 (994 firms) | 0.147 | 1.011 | 10.51% |
The PM's segment-weighted option B (0.944) was not recomputed (segment revenues are not in the Data agent's files).

## Cross-checks (never used for the WACC)
REL.L vs FTSE 100 (`^FTSE`), via `desk.risk.beta`; standard errors computed in run_risk.py:
| Regression | Beta | Std error | 95% range | R-squared | Obs | PM evidence file |
|---|---|---|---|---|---|---|
| 2y weekly | 0.67 | 0.22 | 0.23 to 1.11 | 0.08 | 104 | 0.67 / 0.08: match |
| 5y weekly | 0.66 | 0.11 | 0.45 to 0.87 | 0.12 | 261 | 0.66 / 0.12: match |
| 5y monthly | 0.38 | 0.24 | -0.08 to 0.84 | 0.04 | 60 | 0.38 / 0.04: match |
| Blume-adjusted 5y monthly | 0.58 | | | | | |

Peer betas, 5y monthly vs home index (Yahoo adjusted closes fetched 14 Oct 2026, a non-filing source; raw, not relevered; 60 obs each, no 100x jumps):
Thomson Reuters 0.75 (S&P 500; NYSE line in USD), Verisk 0.69 (S&P 500), S&P Global 1.07 (S&P 500), Moody's 1.32 (S&P 500), Wolters Kluwer 0.58 (AEX), Experian 1.04 (FTSE 100), LSEG 0.60 (FTSE 100). **Median of the 7 core peers 0.75.** Informa (optional) 1.18. Standard errors 0.12 to 0.31.

## Other risk measures (REL.L, GBp, dividend-adjusted)
| Measure | Value |
|---|---|
| Volatility, 1y daily, annualised | **36.0%** (FTSE 100: 11.6%) |
| Volatility, 5y daily, annualised | 23.2% (FTSE 100: 12.5%) |
| Max drawdown, 5y | **-51.3%**: from 4,133p (13 Feb 2025) to 2,012p (11 Feb 2026), adjusted prices. The 13 Oct 2026 close (2,771p) is still 33% below the peak. FTSE 100 max drawdown over the same 5 years: -13.4% (Mar-Apr 2025) |
| Largest daily moves | -14.4% (3 Feb 2026), +10.0% (13 Feb 2026), -7.8% (7 Apr 2025), -6.9% (30 Jul 2026) |

## Price unit check
**No 100x jump.** The series is in pence throughout (adjusted range 2,012p to 4,133p; the last adjusted close equals the 2,771p unadjusted close in inputs.yaml). The largest daily move is -14.4%.

## Leverage (net debt / adjusted EBITDA)
| Date | Net debt (RELX def., incl. leases) | Net debt ex leases | EBITDA | Ratio (GBP, incl. / ex leases) | RELX reports |
|---|---|---|---|---|---|
| 31 Dec 2025 | 7,201 | 7,104 | 3,846 (FY25R p.2, p.11; AR25 p.186) | **1.87x / 1.85x** | 2.0x |
| 30 Jun 2026 | 8,733 | 8,614 | 3,930 LTM (3,846 - H1 25 1,908 + H1 26 1,992; H126 p.10) | **2.22x / 2.19x** | 2.3x |

RELX's own ratio is higher because it includes pensions and is "calculated in US dollars" (FY25R p.13; H126 p.12), not in pounds. History: 2.4x, 2.1x, 2.0x, 1.8x, 2.0x for FY21-25 (AR25 p.67-68).
**Target: none published as a number.** RELX "seeks to maintain ... credit rating agency metrics that are consistent with a solid investment grade credit rating" (Annual Report 2025, 20-F ex 15.2, 0001104659-26-017277, p.72).
**Rating:** Moody's A3, S&P A-, Fitch BBB+ (from the brief: RELX Capital term sheet, 24 Mar 2025, 0001193125-25-061449; I did not re-fetch it). Leverage at 2.2-2.3x after the GBP 2.25bn buyback is moderate for a single-A-minus credit.

## FLAGs
1. **The bottom-up beta (0.97) is well above RELX's own regressions (0.38-0.67).** It lies outside the 95% range of the 5y weekly (0.45-0.87) and 5y monthly (-0.08-0.84) regressions, and inside only the 2y weekly range (0.23-1.11). With the 5y weekly beta (0.66) the cost of equity would be about 1.6 points lower (8.75% vs 10.31%). I follow the PM's rule: R-squared is only 0.04-0.12, so the regressions explain little, and the FTSE 100 is a poor proxy for a business earning most of its revenue in North America. The peer median (0.75, raw) is also below 0.97. The gap is material and the PM should know it.
2. **RELX is now much more volatile than its regression beta suggests.** 1-year volatility is 36% (3x the FTSE 100) and the stock fell 51% from Feb 2025 to Feb 2026 (largest one-day fall -14.4% on 3 Feb 2026). This is stock-specific (AI-disruption) risk, which beta does not capture by design; it supports the bear case rather than a higher beta.
3. **D/E mixes dates** (as the brief defines it): 31 Dec 2025 net debt with the 25 Sep 2026 post-buyback share count and the 13 Oct price. June 2026 net debt would raise beta by 0.02 (+0.1 point cost of equity).
4. **PM card 0.974 vs 0.9729:** the card included 97 of leases in net debt; the brief now excludes them. Difference -0.0012.
5. **No numeric leverage target**, so leverage cannot be compared with a company range. `desk/fundamentals.leverage`'s docstring still says "the company's own target range is 2.5 to 3.0x" (Diageo's); it does not apply to RELX. Suggest fixing the docstring on a branch for Amanda's approval.
6. **`desk/` has no relever (Hamada) function and no standard error for beta.** Both are computed in my scripts, with a comment naming each formula (as for Diageo and Unilever). Suggest adding `risk.relever_beta` and a `std_error` field in `risk.beta`, on a branch with tests, for Amanda's approval (CLAUDE.md rule 1).
7. **Peer betas are raw, from Yahoo, and measured against different indices** (US peers vs the S&P 500, now dominated by technology). They are not relevered and should not be used for the WACC. TRI is measured on its NYSE line vs the S&P 500, not on Toronto.
8. **The last monthly and weekly returns are partial** (to 13 Oct). desk/risk.py labels them with the period-end date (31 Oct, 16 Oct). Cosmetic.
9. **Tests:** pytest is not installed in this environment, so `python -m pytest` could not run. I changed no code in `desk/`.

## Missing
- A numeric leverage target (RELX does not publish one; FLAG 5).
- The rating was taken from the brief, not re-checked against a rating agency (agency sites not tried; the term sheet is the brief's source).
Nothing needed for beta is missing.

## Confidence
High on the bottom-up calculation (file value checked, own regressions match the PM's evidence file to 2 decimals) and on the leverage arithmetic. Medium on beta as a measure of RELX's risk: own and peer evidence (0.38-0.75) sits below 0.97 (FLAG 1).
