# Data agent notes: Diageo (DGE), run 2026-10-12

## What I fetched
- **SEC EDGAR:** the XBRL data inside the last five 20-F filings (FY22 to FY26). The FY26 20-F (accession 0001628280-26-057529, filed 2026-08-18) is the primary source. Raw: `financials_raw.csv`; with text items and regions: `financials.csv`.
- **Yahoo Finance:** 5 years of daily DGE.L (pence) and FTSE 100 prices (`prices.csv`, dividend-adjusted, for returns). Latest actual close: 1,673p on 2026-10-12. The KES/USD average for the EABL carve-out also comes from Yahoo.
- **FRED:** US 10-year Treasury 5.22% (2026-10-08) and GBP/USD 1.3234 (2026-10-02).
- **Web search, non-filing:** EABL FY26 results, RCB sale price, Pernod and Remy results, IWSR outlook. Every figure from these is labelled as a non-filing source.

## Tie-out vs the brief (tolerance 0.5%): all pass
| Item | Brief | Data agent | Diff |
|---|---|---|---|
| Net sales (USD m) | 19,643 | 19,643 | 0.00% |
| Operating profit before exceptionals (USD m) | 5,683 | 5,683 | 0.00% |
| Net debt (USD m) | 20,500 | 20,482 | -0.09% (the brief rounded) |
| Free cash flow (USD m) | 3,211 | 3,211 | 0.00% |
| EPS before exceptionals (cents) | 165.3 | 165.3 | 0.00% |

## How I handled each trap
- **USD vs pence vs ADR:** everything is in USD m. The share price is in pence (Yahoo confirms the currency is GBp). Shares are ordinary shares (2,222m), not ADRs.
- **Before-exceptionals:** the forecast base uses operating profit before exceptionals (5,683). Reported operating profit (3,156, after 2,527 of exceptional charges) is kept in financials.csv.
- **EABL:** removed from base sales and margin (see FLAG 1). Its debt is already outside net borrowings: it sits in "liabilities held for sale". So the sale proceeds are added once, in `disposal_proceeds`, and there is no double count.
- **June year end:** FY27 started 1 July 2026, so 103 days (0.2822 of a year) had passed at the run date.

## FLAGS
1. **EABL carve-out uses a non-filing source (confidence: medium).** Diageo's 20-F does not show EABL's own sales or profit. I used EABL's FY26 results (June year end, published 6 Aug 2026) as reported in the press: net revenue KES 145.96bn and EBIT KES 32.1bn. I converted at 128.32 KES per USD, the FY26 average of Yahoo's KES=X. That gives 1,137.5 of sales and 250.2 of EBIT, so the ex-EABL base is sales of 18,505.5 at a margin of 29.36%. This is cross-checked against Diageo's Africa region: 1,642 of sales, so EABL is about 69% of Africa. **PM: please check this against EABL's annual report.**
   **Checked 2026-10-12 (PM asked Claude to verify):** EABL's own 2026 Integrated Annual Report and results release give net sales KES 145.96bn (+13%) and EBIT KES 32.07bn (+27%, margin 22%). Our 32.1bn is the rounded figure; using 32.07bn would add about 0.1p a share, so the inputs are left unchanged. Sources: [EABL 2026 Integrated Annual Report](https://www.eabl.com/~/media/Files/E/eabl/documents/investor/agm/2026/eabl-2026-integrated-annual-report-web-version.pdf) (found via search; this environment cannot open eabl.com directly), [Kenyan Wall Street](https://kenyanwallstreet.com/eabl-fy26-results), [Food Business MEA](https://www.foodbusinessmea.com/eabl-net-profit-jumps-49-to-us140-7m-in-fy2026/). Also noted: Diageo keeps Guinness licence income after the sale, so removing all of EABL's EBIT slightly understates what Diageo keeps (small, not quantified). The sale is cleared by Kenya's Competition Authority (10 Sep 2026) but completion is not confirmed in a filing.
2. **[RESOLVED 2026-10-12: the PM set cost of debt = risk-free + 1% in the brief.] Cost of debt is below the risk-free rate (confidence: low; affects WACC).** Interest / average net borrowings = 812 / 21,336 = **3.81%**. That is Diageo's *historic* cost, mostly fixed-rate bonds issued when rates were lower. The US 10-year is 5.22%, and a new Diageo bond would cost more than the Treasury. The brief allows this method, so I used it. Using Rf + 1% (6.22%) would be more realistic. The Bear agent quantifies the difference.
3. **Tax rate before exceptionals is 24.3%**, not the c.23% the brief proposed (20-F p.22; FY25 was 24.9%).
4. **Capex at 7.1% of sales vs D&A at 3.4%, held forever.** This is the 5-year average, inflated by the capacity build-out and the FY24-25 spending peak. Management guides c.$3.75bn of capex over FY27-29, about 6.8% of ex-EABL sales a year (1,250 / 18,505). In the terminal year, capex at twice D&A permanently depresses free cash flow. The method follows the brief, but **PM to decide** whether the terminal year should use a lower capex ratio.
5. **Share count trap.** XBRL "EntityCommonStockSharesOutstanding" says 2,432m, but that figure **includes 208m treasury shares**. I used 2,432 - 208 - 2 (employee trusts) = 2,222m.
6. **Minority interests at book value (2,083).** USL (42.79% minority) is listed in India, so its minority stake is worth far more at market than its 755 book value. Book value understates the deduction. This is also not adjusted for the EABL minority that leaves on completion (amount not disclosed).
7. **Pension:** the net position is a surplus of 627, so the brief's rule gives 0. Diageo's own leverage measure adds back the 387 liability of deficit plans.
8. **Associates (5,284):** Moet Hennessy (34%) is carried at 5,107. The 20-F says its impairment test uses fair value and is "sensitive" (a 1x lower EBITDA multiple means a 312 charge), so book value is close to fair value. Others: 177.
9. **Disposal proceeds (3,318) are gross, before tax and costs.** EABL is "approximately $2.3 billion" (20-F p.85). For RCB, USL sells for INR 166.6bn (about $1.78bn, press); Diageo's 57.21% share is 1,018. Neither deal has completed yet (both expected H2 calendar 2026).
10. **Net debt is at 30 June 2026** and is not rolled forward to the run date. The FY26 final dividend of 30c (about 667) will be paid after the run date.
11. **FY22 balances partly missing:** gross borrowings, maturing inventories, adjusted EBITDA and lease liabilities for FY22 are not in the FY23/FY24 XBRL in USD. They are not needed for the valuation.
12. **FY24 "depreciation, amortisation and impairment" (493) is below plain D&A (677).** This is probably an impairment reversal. I did not use it (I used D&A excluding impairment).

## Industry forecast (step 5)
I could not reach IWSR directly. The press reports IWSR's 2026 release as follows: global **spirits volumes fell 3% in 2025**, and its ten-year outlook has spirits volumes **down about 2% by 2035**. That is secondhand: [Drinks International](https://m.drinksint.com/news/fullstory.php/aid/12352/Spirits_overtake_wine_in_total_global_volumes.html), [Federvini](https://www.federvini.it/en/news-en/iwsr-projects-stable-growth-in-wine-and-spirits,-highlighting-emerging-markets). The brief's 3% for FY30-31 is value growth, and it needs about 3% a year of price/mix on flat-to-falling volumes. That is achievable historically, but it is **not** supported by the industry volume outlook. It challenges, rather than supports, the 3%.

## Peers (`peers.csv`)
Only two usable P/E figures: Pernod Ricard 10.7x (press, FY26) and Brown-Forman 17.4x (SEC 10-K, year to April 2026). Campari, Remy Cointreau and Constellation are **missing**: their share counts and full-year EBITDA come from company websites this environment cannot reach. EV/EBITDA comps are not possible on this run.

## Confidence
High: all 20-F figures, tie-outs, share count, net debt, tax rate, price, FX, risk-free. Medium: EABL carve-out, associates, disposal proceeds. Low: cost of debt, peer data.

## Phase 3 additions (12 Oct 2026, after the PM's decisions and the Codex audit)
- **FLAG 10 resolved (net debt date, Codex BRIDGE-01):** the brief now values the business at the 30 June 2026 balance sheet date and rolls equity forward to 12 Oct at the cost of equity. The FY26 final dividend (30c) goes ex on **15 October 2026** (20-F FY26), *after* the valuation date, so the 1,673p price is cum-dividend and `dividends_ex_before_valuation_musd` = 0. The earlier idea of deducting it (Bear challenge 6, -23p) was wrong for this date.
- **New input `restructuring_cash` = 850 (USD m):** c.$800m + c.$50m of exceptional restructuring cash in FY27, and c.$850m over FY27-29 (Capital Markets Day 6-K, 6 Aug 2026). The forecast is before exceptionals and net debt is at 30 June, so this cash was missing from the valuation. Pre-tax and undiscounted; tax relief is not confirmed, so it is not counted (it would add up to about 7p).
- **Peers:** Campari (adjusted EPS EUR 0.32, FY Dec 2025) and Remy Cointreau (EPS excl. non-recurring EUR 1.71, FY Mar 2026) added from press reports of their results (non-filing source; company sites unreachable). Constellation is still missing: diluted EPS is not tagged in its XBRL.
