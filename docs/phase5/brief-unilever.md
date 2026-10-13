# AI Equity Research Desk: Brief v0.1 (DRAFT)
**Company:** Unilever PLC (LSE: ULVR, FTSE 100; NYSE ADR: UL, 1 ADR = 1 share)
**Portfolio manager:** Amanda
**Status:** v0.1 draft for PM review, 13 October 2026. Nothing below is agreed until the PM signs it off.

---

## 1. The investment question
> Is Unilever a **Buy, Hold or Sell** for a 12-month horizon at today's price, now that Ice Cream has gone and Foods is being sold to McCormick, leaving a Home and Personal Care (HPC) company?

## 2. Company snapshot (FY25, year ended 31 Dec 2025, continuing operations, i.e. without Ice Cream)
Sources: FY25 20-F (SEC accession 0000217410-26-000007, filed 12 Mar 2026); FY25 results 6-K (0001654954-26-001155, 12 Feb 2026); H1 2026 results 6-K (0000217410-26-000057, 28 Jul 2026); Foods/McCormick investor presentation, Form 425 (0000217410-26-000027); McCormick 10-Q to 31 Aug 2026 (0000063754-26-000329). The Data agent re-checks every figure.

| Item (EUR unless stated) | FY25 | Note |
|---|---|---|
| Turnover | €50.5bn (€50,503m), -3.8% | Underlying sales growth (USG, Unilever's "organic") +3.5% (volume +1.5%, price +2.0%); currency -5.9%; disposals -1.2% |
| Underlying operating profit (UOP) | €10.1bn (€10,084m), margin 20.0% (+60bps) | Reported operating profit €9,037m (17.9%); restructuring €599m (1.2% of turnover) |
| By business group (turnover / UOP, €m) | Beauty & Wellbeing 12,848 / 2,471; Personal Care 13,161 / 2,973; Home Care 11,565 / 1,718; Foods 12,929 / 2,922 | FY25 results 6-K, note 2 |
| Free cash flow | €5.9bn (100% cash conversion) | Down €0.4bn on tax from the Ice Cream demerger |
| Net debt | €23.1bn (31 Dec 2025); €26.0bn (30 Jun 2026) | 2.0x / 2.3x underlying EBITDA. FY26 target c.2x |
| Pensions | €3.5bn **surplus** (31 Dec 2025); €3.7bn (30 Jun 2026) | A surplus, not a deficit |
| Non-controlling interests (book) | €2,057m | Mainly Hindustan Unilever (listed in India; Unilever's stake to be verified by the Data agent) |
| Shares | 2,154.3m with voting rights (31 Aug 2026, 6-K 0001654954-26-008017) | After a share consolidation at the demerger; €6bn of buybacks planned 2026-29 |
| Share price | **4,710.5p** (13 Oct 2026, Yahoo ULVR.L); ADR $62.63 | Market value c.£101.5bn = c.€120bn at €1 = £0.845 |

**FY26 outlook (upgraded 28 Jul 2026):** USG within the 4-6% multi-year range, with c.3% volume; H2 USG 4-5%; "modest improvement" in underlying operating margin on 20.0%. H1 2026: USG 4.8%, turnover +0.5% after -4.9% currency, margin 20.3%.

## 3. Data traps (new ones the desk has not seen before)
1. **Reports in euros, priced in pence.** Diageo reported in USD and KO is priced in USD. Unilever needs a EUR-to-GBP conversion (€1 = £0.845 on 13 Oct 2026). Small code change on a branch with a PR.
2. **Foods is being sold (signed 31 Mar 2026, closing expected mid-2027).** McCormick takes Unilever Foods (excluding India, Nepal, Portugal, Lifestyle & Nutrition, Buavita, Lipton Ready-to-Drink). Unilever gets **$15.7bn cash**; Unilever's shareholders get **55.1%** of the enlarged McCormick and Unilever keeps **9.9%** (McCormick 10-Q). The sale perimeter had FY25 sales of **€10.7bn** and UOP of **€2.6bn (24% margin)** (Form 425). See decision 1.
3. **McCormick's share price has fallen 23% since the deal**, from the $57.84 one-month average used for the $44.8bn headline to **$44.44** (13 Oct 2026). The shares are a fixed number (about 500m: 65% of the enlarged company, with McCormick's 269.1m shares being 35%), so the deal is worth less to Unilever today than the headline.
4. **Ice Cream already gone; a 19.85% stake kept** in The Magnum Ice Cream Company (TMICC, listed; €15.91 on 13 Oct 2026). Valued at market in the bridge, like KO's listed stakes.
5. **Hindustan Unilever is a large listed minority.** The book value of minorities (€2.1bn) is likely far below their share of value, the same trap as Diageo's Indian subsidiary. Proposal: the same proportionate rule you chose for Diageo.
6. **Emerging-market currencies.** 62% of the remaining company's turnover is in emerging markets (FY25 pro forma, Form 425 investor presentation). Currency cut turnover by 5.9% in FY25 and 4.9% in H1 2026, so USG cannot be used as euro growth directly (like Argentina for KO). Growth evidence pack to follow.
7. **Restructuring is recurring.** €599m in FY25 and €710m in FY24 sit outside "underlying" profit. The DCF must include a realistic ongoing cost, not treat it as one-off.
8. **Tax on the $15.7bn cash: MISSING.** Management says Unilever's share of deal synergies "fully offsets Unilever's tax and separation costs" (Form 425) but gives no tax figure. The Data agent searches the 20-F and H1 report; if it is not disclosed, this goes to the PM.

## 4. What each agent must produce
Same as Diageo (brief-diageo.md section 4). Benchmark FTSE 100 (as Diageo). Values in pence per share, totals in EUR m.

## 5. Valuation assumptions (proposals, to be agreed one at a time)
Base year FY25 (latest audited). Forecast FY26 to FY30. EUR, converted to pence at the run-date rate.

| # | Assumption | Proposal | Evidence / why | Status |
|---|---|---|---|---|
| A | How to value Foods | **Sum of the parts:** DCF of Unilever without the sale perimeter, plus the deal consideration at today's market value ($15.7bn cash + c.500m McCormick shares at $44.44 = $37.9bn = **€33.8bn, c.1,327p a share, 28% of the price**). Bear: the deal fails and Foods stays in the DCF | Signed deal with fixed terms; McCormick's own share price is the best evidence of what the shares are worth | **Decision 1, sent** |
| B | Revenue growth (EUR, ex-perimeter) | FY26 **+0.5%** (H1 2026 actual reported change); FY27-30 **1.6%** a year (low end of 4-6% USG less the 9-year 2.4-point currency drag); bear 0.2% | ulvr-growth-evidence.md (FY17-25 results 6-Ks) | **Agreed** 13 Oct 2026 |
| C | Operating margin | **17.7% flat**: FY25 underlying 18.8% without the sale perimeter, less 1.1% ongoing restructuring (FY23-25 actual; management's new 0.6% guide not used, never achieved in 10 years); **plus the €500m one-off stranded-cost restructuring (2027-29) deducted in the bridge**; bear 16.2% | ulvr-margin-evidence.md | **Agreed** 13 Oct 2026, re-confirmed after the stranded-cost correction (mistakes row 19) |
| D | Minorities | **Proportionate** (Diageo rule): minorities' share of profit x DCF value, ratio for the remaining company computed by the Fundamentals agent; HUL at market (38% = c.€15.7bn) shown as a bear line | ulvr-minorities-evidence.md (20-F notes 15B, 27) | **Agreed** 13 Oct 2026 |
| E | Listed stakes | TMICC 19.85% at market; after the deal, the 9.9% McCormick stake is inside item A | Same rule as KO | Pending |
| F | Tax | Operating tax **25.7%** (FY25 underlying ETR). Tax and separation costs on the Foods cash: MISSING, **not deducted in the base case**; memo states each €1bn = 39p a share; bear case deducts a 25%-of-cash stress (€3.5bn, 137p) | ulvr-tax-evidence.md | **Agreed** 13 Oct 2026 (tax on cash); 25.7% pending sign-off |
| G | Capex, D&A, working capital, restructuring | 5-year averages ex one-offs, ex-perimeter where disclosed; restructuring as an ongoing cash cost | 20-F | Pending |
| H | Beta | Bottom-up: Damodaran Europe household/personal products unlevered beta, relevered at Unilever's D/E; regressions vs FTSE 100 as cross-check | Same rule as Diageo and KO | Pending |
| I | Risk-free, ERP, cost of debt | UK 10-year gilt (as Diageo, since the price is in pence); ERP 5.0%; cost of debt = risk-free + spread for Unilever's credit rating (rating to be sourced by the Data agent) | Same rule as Diageo | Pending |
| J | Terminal growth / RONIC | 2.0%; RONIC = Unilever's ex-perimeter ROIC at the DCF tax rate | Same rule as Diageo and KO | Pending |
| K | Mid-year discounting, valuation basis | Yes; 31 Dec 2025 balance sheet rolled forward at cost of equity less dividends | Same as Diageo and KO | Pending |
| L | Rating rule | Buy >= +15%, Sell <= -10% | Same as the rest of the portfolio | Pending |

### Comparables (proposal)
HPC peers: Procter & Gamble, Colgate-Palmolive, Reckitt, Beiersdorf, L'Oreal, Henkel (consumer), Kimberly-Clark; Hindustan Unilever flagged separately. EV/EBITDA, P/E, FCF yield; medians.

## 6. Checks
Same as Diageo: independent Excel check within 2%, source check of 5 random numbers, mistakes log.

## 7. Decisions
| # | Decision | Status |
|---|---|---|
| 1 | How to value Foods (sum of the parts at today's deal value, whole-group DCF, or headline deal value) | **Sent** 13 Oct 2026 |
| 2 | Growth: FY26 +0.5%, FY27-30 1.6% a year in EUR; bear 0.2% | **Agreed** 13 Oct 2026, evidence in ulvr-growth-evidence.md |
| 5 | Tax on Foods cash: left out of base (MISSING), shown as 39p per €1bn; 25% stress in bear | **Agreed** 13 Oct 2026, evidence in ulvr-tax-evidence.md |
| 4 | Minorities proportionate (Diageo rule); HUL at market as bear line | **Agreed** 13 Oct 2026, evidence in ulvr-minorities-evidence.md |
| 3 | Margin 17.7% flat (underlying less recurring restructuring); bear 16.2% | **Agreed** 13 Oct 2026, evidence in ulvr-margin-evidence.md |
