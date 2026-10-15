# Bear case: The Coca-Cola Company (KO), run 2026-10-13, re-run 15 Oct 2026 (evidence audit)

All values per share are in **US dollars (USD)**. Totals are **USD m**. The share price is USD 90.12 (Yahoo, 13 Oct 2026). Every "impact" comes from the desk engine: `python -m desk.valuation_run` run on a scratch copy of the brief and `inputs.yaml` with **one change**. The script is `bear/run_bear.py`, the results are in `bear/bear_runs.json`, and each copy is in `bear/scratch/<name>/`. The brief and `inputs.yaml` were not edited.

**Re-run 15 Oct 2026.** This file replaces the 13 Oct version. What changed (PM decisions after the evidence audit, `docs/audit-2026-10-15/KO.md`):
- equity risk premium **4.2%** (Damodaran implied; was 5.0%, unsourced), so WACC 8.00% -> **7.55%**;
- the listed stakes (USD 39,539.5m, already at 13 Oct 2026 prices) are **no longer grown** in the roll-forward;
- the PM's bear margin **31.9%** (`briefs/KO.yaml` scenarios.bear.bear_agent_margin) is now used in the **stacked bear case**.

Every figure below is new. The 13 Oct figure is shown in brackets as "(13 Oct: USD x)" where it helps; the 13 Oct results are kept in `bear/bear_runs_2026-10-13_superseded.json`. Scenarios that move the listed stakes (challenge 4) now move the not-grown run-date amount by the same figure, so the change is not grown again.

**Starting point** (`valuation/valuation.json`, 15 Oct 2026):
- **Base:** USD 50.76, SELL (-43.7%) (13 Oct: USD 47.60).
- **Engine bear case:** USD 39.91, SELL (-55.7%): the base plus 1% growth in FY27-30 plus 1 point on the WACC (8.55%). It keeps the 33.2% base margin (13 Oct: USD 37.99).
- **Stacked bear case (the reference bear figure for the memo):** engine bear case **plus the PM's 31.9% bear margin = USD 38.25, SELL (-57.6%)**, USD 12.51 below the base. The 13 Oct memo showed USD 37.99, which left the margin out (audit finding 1).
- **Rating lines:** HOLD needs at least USD 81.11, BUY at least USD 103.64.

The base is already a SELL, so the most useful question is still "**is the SELL just a harsh base case?**" Section B answers it. **The answer has changed: stacking the most generous assumptions now reaches HOLD (USD 84.19), though not BUY.**

---

## A. Challenges

### Summary table (USD per share, one change each vs the USD 50.76 base)

| # | challenge (agent challenged) | test | value | impact (15 Oct) | impact (13 Oct, superseded) | PM response (13 Oct 2026, kept) |
|---|---|---|---|---|---|---|
| 1 | Peak margin (Fundamentals) | 30.0% (FY24, includes CCBA) | USD 45.61 | **-USD 5.14** | -USD 4.79 | 30.0% includes CCBA but is applied to ex-CCBA sales |
| 1 | | 31.94% (FY24 ex-CCBA, like-for-like) | USD 48.74 | -USD 2.02 | -USD 1.88 | |
| 1 | | 31.9% (PM bear margin, as decided) | USD 48.68 | **-USD 2.08** | not run | **PM decision: bear margin 31.9%** |
| 2 | Currency drag (Valuation, growth path) | FY27-30 growth 1% | USD 47.18 | **-USD 3.58** | -USD 3.30 | Stress test; the growth evidence calls 1% too punitive |
| 2 | | FY26 growth 4.5% | USD 49.99 | -USD 0.76 | -USD 0.71 | |
| 3 | IRS and cash (Data) | add the USD 900m H1 2026 accrual | USD 50.53 | -USD 0.22 | -USD 0.22 | Loss already in base; model FY26 cash (USD 11,358m) reconciles to guidance (USD 12,400m) |
| 4 | Stakes at market (Data, bridge) | listed stakes at 31 Dec 2025 fair value | USD 49.54 | -USD 1.22 | -USD 1.30 | Small |
| 4 | | Monster stake -30% | USD 49.52 | -USD 1.24 | -USD 1.32 | |
| 4 | | 21% tax on the gain over book | USD 49.51 | -USD 1.25 | -USD 1.33 | **PM decision: no tax deducted** (tax basis not disclosed) |
| 5 | Beta at a low (Risk) | 0.868 (2022-26 average) | USD 43.10 | **-USD 7.66** (WACC 8.56%) | -USD 7.60 (WACC 9.20%) | **PM decision: keep 0.6091**, the current industry beta (as for Diageo) |
| 5 | | 0.741 (2024 level) | USD 46.55 | -USD 4.21 (WACC 8.06%) | -USD 4.21 | |
| audit | ERP (Valuation / PM brief) | ERP 5.0% (Kroll US recommended) | USD 47.01 | **-USD 3.74** (WACC 8.00%) | was the base | new; see stress lines below |
| audit | | ERP 5.5% (Fernandez 2025 survey, US) | USD 44.95 | **-USD 5.81** (WACC 8.28%) | not run | new |
| audit | FY26 growth (Valuation, growth path) | FY26 5.0% instead of 6.0% (non-CCBA disposals) | USD 50.25 | **-USD 0.51** | audit: -USD 0.47 (old basis) | new; PM has not decided |

No single change leaves SELL. Each one is also SELL when applied inside the engine bear case (`bear_block_*` fields in `bear_runs.json`; those use the 33.2% margin, except the margin runs).

### 1. Margin: the 33.2% base margin assumes the best year ever is the new normal (challenges the Fundamentals agent and brief item B)

- **Claim:** The model holds the FY25 ex-CCBA comparable margin of 33.2% flat for ever. That is a peak-year figure. It also excludes write-downs that keep coming back.
- **Evidence:**
  - **The margin has only just reached this level.** Comparable operating margin was 28.7%, 28.7%, 29.1%, 30.0% and 31.2% in FY21 to FY25 (`fundamentals/ratios.csv`; Q4 results 8-Ks 0000021344-22-000004 through 0001628280-26-006642).
  - **Part of the rise is mix, not efficiency.** It comes from selling low-margin bottlers (Fundamentals FLAG 9; brief section 5B).
  - **"Comparable" leaves out impairments that recur every year.** FY24 USD 886m (North America USD 760m) and FY25 USD 1,045m (North America USD 960m). On a reported basis FY25 was 28.7% against 31.2% comparable (Q4 2025 8-K 0001628280-26-006642 p.28; `fundamentals/commentary.md` FLAG 1).
- **Value impact (USD per share):**

  | test | margin | value | impact |
  |---|---|---|---|
  | Brief's literal bear: FY24 comparable margin (Q4 2024 8-K 0000021344-25-000005) | 30.0% | USD 45.61 | -USD 5.14 |
  | Like-for-like: FY24 margin **ex-CCBA**, (14,085 - 266.2) / (46,897 - 3,632.3) USD m | 31.94% | USD 48.74 | -USD 2.02 |
  | **PM bear margin** (brief scenarios.bear.bear_agent_margin) | 31.9% | **USD 48.68** | **-USD 2.08** |
  | Inside the stacked bear case (1% growth, WACC +1 point) | 31.9% | **USD 38.25** | -USD 12.51 vs base |

  Scratch runs: `scratch/c1_margin_300`, `c1_margin_fy24_ex_ccba`, `c1_margin_319`, `stacked_bear_319`.
- **Honesty note:** the 30.0% mixes a CCBA-inclusive margin with ex-CCBA sales, so -USD 5.14 overstates the bear case; the PM chose 31.9%. Recent trading argues against the bear: the Q2 2026 comparable margin was 35.6% against 34.7% a year earlier (Q2 2026 8-K 0001628280-26-049922).

### 2. Currency: dollar growth of 3% a year assumes currencies stop falling, and management has repeatedly got currency wrong (challenges the Valuation agent's growth path, brief item A)

- **Claim:** FY27-30 growth of 3.0% in USD assumes only a 1-point currency drag. Over 2020-25 the average drag was 3.2 points. FY26's +6.0% is also flattered by a currency tailwind, a one-off FIFA World Cup boost, and (audit finding 3) it leaves out about 1 point of non-CCBA disposals.
- **Evidence:**
  - **The drag history.** Currency took 2, +1 (a tailwind), 7, 4, 5 and 2 points in 2020-25 (`docs/phase5/ko-growth-evidence.md`, from the Q4 8-Ks).
  - **Management under-forecast the headwind in 3 of 5 years** (track-record table, section C).
  - **The FY26 tailwind is already shrinking**: cut from 1-2% to about 1% in July (Q2 2026 8-K 0001628280-26-049922).
  - **Non-CCBA disposals:** H1 2026 already shows a -1 point acquisitions-and-divestitures effect while CCBA is still consolidated, and the Q3 guide is about -1% before CCBA closes (Q2 2026 8-K revenue bridge; FY25 10-K names Nigeria finished goods, India territories and Ghana). Source: `docs/audit-2026-10-15/KO.md` finding 3.
  - **FY25 unit case volume was flat** (Q4 2025 8-K 0001628280-26-006642), so growth was all price and mix.
  - **The FY25 10-K risk factors name the long-term pressures:** "the effects or perceived effects of the usage of weight-loss drugs on consumption patterns" and "potential new or increased taxes on sweetened beverages" (10-K 0001628280-26-010047, Item 1A). No sourced quantification of GLP-1 or sugar-tax effects exists (MISSING); the 1% growth run is the nearest proxy.
  - **No independent industry forecast** could be obtained, and the "4-5% long-term algorithm" is not in a primary source (audit finding 8).
- **Value impact (USD per share):**

  | test | value | impact |
  |---|---|---|
  | FY27-30 growth 1.0% (full 3.2-point average drag), FY26 unchanged | USD 47.18 | **-USD 3.58** |
  | FY26 growth 5.0% (audit: non-CCBA disposals) | USD 50.25 | -USD 0.51 |
  | FY26 growth 4.5% (World Cup and currency tailwind fade) | USD 49.99 | -USD 0.76 |

  Scratch runs: `scratch/c2_growth_1pct`, `audit_fy26_5p0`, `c2_fy26_4p5`.
- **Honesty note:** the growth evidence paper calls 1% "too punitive" (it removes the Argentina currency fall but not the Argentina price rises). The 4.5% and 1% runs are stress tests, not forecasts. The 5.0% run has a sourced basis but is not a PM decision.

### 3. IRS case and FY26 cash: the market's "USD 12.4bn of free cash flow" is not the cash shareholders keep (challenges the Data agent's cash and tax inputs)

- **Claim:** The FY26 FCF guidance of about USD 12.4bn (Q2 2026 8-K 0001628280-26-049922) excludes the IRS case and includes dividends from stakes the DCF values separately. On a like-for-like basis KO's cash yield is well below the risk-free rate, and a loss would lift leverage sharply.
- **Evidence: the FY26 cash reconciliation (USD m; unchanged by the re-run, because the ERP and the roll-forward do not touch FY26 cash flow)**

  | item | USD m | source |
  |---|---|---|
  | Model FY26 unlevered FCF (ex-CCBA, 23.7% tax) | 11,358 | `valuation.json` |
  | + Extra tax from the IRS case that guidance leaves out (EBIT 15,589 x 3.8 points) | +592 | Q2 2026 8-K (19.9% "does not include the impact of ongoing tax litigation"); Q2 2026 10-Q 0001628280-26-050503 Note 9 |
  | + Dividends from equity investees (FY25 actual as proxy) | +993 | FY25 10-K 0001628280-26-010047, equity method note |
  | + Stock-based compensation (FY25) | +279 | FY25 10-K cash flow statement |
  | - Net interest after tax | -751 | interest paid 1,724 (FY25 10-K) - interest income 786 (XBRL), x (1 - 19.9%) |
  | - Guided capex USD 2.2bn vs model capex 2,069 | -131 | Q2 2026 8-K |
  | **Residual** (CCBA part-year cash flow, other items) | **+60** | |
  | **KO guidance** | **12,400** | Q2 2026 8-K |

  - The 1,042 gap is a difference of basis, so the Data inputs pass this test.
  - **FCF yield:** USD 12.4bn / USD 387.7bn market cap = **3.20%**, about 2.0 points below the 10-year Treasury at 5.22% (FRED DGS10), before the IRS tax.
  - **The IRS record:** KO has said since 2020 it "will ultimately prevail" (Q4 2020 8-K 0000021344-21-000003) and lost at the Tax Court twice. The potential liability rose from about USD 12bn (Dec 2020) to USD 14bn (Dec 2025, 10-K XBRL `ko:IncrementalTaxAndInterestLiability`), after USD 6.0bn already paid for 2007-09. The expected tax-rate uplift went from 3.5% to 3.8% (Q2 2026 10-Q). Interest keeps accruing until paid (FY25 10-K).
  - **Balance (audit finding 5):** the 8th Circuit reversed the 3M Tax Court decision on 1 Oct 2025 on the same blocked-income rule; KO's FY25 10-K calls it "highly supportive". The 11th Circuit heard KO's appeal on 25 Jun 2026; the ruling is pending. So a win is a real possibility, not just management talk.
  - **Leverage if the USD 14bn is paid in cash:** net debt / comparable EBITDA rises from 1.85x to **2.72x** (`desk.fundamentals.leverage`, net debt 29,686 + 14,000 over 16,063 USD m).
- **Value impact (USD per share):**

  | test | value | impact |
  |---|---|---|
  | Base assumes a **loss**. Value if KO **wins** (no liability, USD 6.0bn refunded, 19.9% tax) | USD 58.20 | +USD 7.44 vs base |
  | of which: removing the USD 14bn liability alone | USD 54.21 | +USD 3.45 |
  | of which: the 19.9% tax rate alone | USD 53.27 | +USD 2.51 |
  | Bear add-on: also deduct the USD 900m H1 2026 accrual (Q2 2026 10-Q Note 9) | USD 50.53 | -USD 0.22 |

  Scratch runs: `scratch/c3_irs_win`, `c3_irs_liab_only`, `c3_irs_tax_only`, `c3_irs_plus900`.
- **Honesty note:** the PM excluded the USD 900m because the 23.7% tax rate already charges 2026 (mistakes log row 17), so the -USD 0.22 is partly double-counted. A loss is already in the base. **The IRS case is a reason the market price is too high, not a reason the desk value is too high**, and the 3M ruling makes a win more plausible than the 13 Oct version implied.

### 4. Equity stakes at market: USD 46.6bn of value depends on other companies' share prices, Monster most of all (challenges the Data agent's bridge input and the brief's stakes rule, item D)

- **Claim:** The bridge adds the listed stakes at their 13 Oct 2026 market value: USD 39,540m of the USD 46,626m total, after a +15% rally in 2026. 45% is Monster, a stock on about 40x earnings. It is before any tax KO would pay if it sold.
- **Evidence:** Monster USD 17,775m of USD 39,540m (`data/associates_rollforward_check.csv`); MNST LTM P/E 40.1x, EV/EBITDA 29.1x (`data/peers.csv`); listed stakes USD 34,286m fair value vs USD 13,999m book at 31 Dec 2025 (FY25 10-K equity method note); 21% tax on the gain over book = USD 5,364m (book as a stand-in for tax basis, not disclosed: FLAG); investee dividends USD 993m in FY25, about 2.5% of market value.
- **Value impact (USD per share):**

  | test | value | impact |
  |---|---|---|
  | Listed stakes back at 31 Dec 2025 fair value (the 2026 rally reverses) | USD 49.54 | -USD 1.22 |
  | Monster stake falls 30% (stress, not a forecast) | USD 49.52 | -USD 1.24 |
  | Stakes after a 21% tax on the gain over book | USD 49.51 | -USD 1.25 |

  Scratch runs: `scratch/c4_stakes_dec25`, `c4_monster_m30`, `c4_stakes_tax`.
- **Why the impacts are a little smaller than on 13 Oct:** the listed stakes are no longer grown at the cost of equity in the roll-forward, so a cut in them is no longer grown either.
- **Honesty note:** about USD 1.2 a share each. Adding the stakes is correct. They are not where the SELL comes from. PM decision (13 Oct): no tax deducted.

### 5. Beta: 0.61 is the soft-drinks industry's beta at a cyclical low (challenges the Risk agent)

- **Claim:** The 0.6091 beta uses the industry's January 2026 unlevered beta (0.575), which has more than halved in two years. If it reverts to its 5-year average, the WACC rises from 7.55% to 8.56%.
- **Evidence:** Damodaran `data/damodaran_betas_us_jan2026.xls`, "Industry Averages", "Beverage (Soft)", 27 firms, unlevered beta corrected for cash: 1.116 (2022), 1.201 (2023), 0.700 (2024), 0.510 (2025), 0.575 (current), **average 0.8205**. Relevered at KO's market D/E (x1.0584, `risk/beta_evidence.json`): 0.868. The audit verified this series (`docs/audit-2026-10-15/KO.md`, beta row).
- **Value impact (USD per share):**

  | test | WACC | value | impact |
  |---|---|---|---|
  | Beta 0.868 (2022-26 average) | 8.56% | **USD 43.10** | **-USD 7.66** |
  | Beta 0.741 (2024 level) | 8.06% | USD 46.55 | -USD 4.21 |

  Scratch runs: `scratch/c5_beta_avg_2022_26`, `c5_beta_y2024`.
- **Honesty note:** KO's own regressions point the other way: 0.13 (2-year weekly), 0.30 (5-year monthly), 0.35 (5-year weekly), R-squared 1-12% (`risk/risk.json`). With the lower ERP, the 8.56% WACC is now **inside** the desk's 6-9% range (it was 9.20%, outside, on 13 Oct). PM decision (13 Oct): keep 0.6091.

### Audit stress lines: the equity risk premium (challenges the PM brief / Valuation agent's WACC)

- **Claim:** The 4.2% ERP is the lowest of the sourced estimates and was seen only in search summaries (Damodaran's site is blocked here). The two other published US figures are higher.
- **Evidence (`docs/audit-2026-10-15/erp-evidence.md`, all secondhand):** Kroll recommended US ERP **5.0%** (from 2 Sep 2025, reaffirmed 2026; Kroll pairs it with the 20-year Treasury, 5.60% on 13 Oct 2026, FRED DGS20). Fernandez et al. 2025 survey (SSRN 5260463), US average ERP used **5.5%** (with a 4.1% risk-free rate).
- **Value impact (USD per share, one change each, risk-free kept at the 10-year 5.22%):**

  | test | WACC | value | impact | stacked bear at that ERP |
  |---|---|---|---|---|
  | ERP 5.0% (Kroll) | 8.00% | USD 47.01 | -USD 3.74 | USD 37.40 (engine bear, 33.2% margin) |
  | ERP 5.5% (Fernandez) | 8.28% | USD 44.95 | -USD 5.81 | USD 36.00 (engine bear, 33.2% margin) |

  Scratch runs: `scratch/audit_erp_kroll_5p0`, `audit_erp_fernandez_5p5`.
- **Honesty note:** Kroll's 5.0% on Kroll's own 20-year risk-free would be harsher still; that two-change case was not run. Survey ERPs were given with lower risk-free rates, so pairing 5.5% with a 5.22% yield overstates the cost of equity. The rating is SELL at every one of them.

### Stacked bear case (the figure for the memo)

| case | value | upside | rating | WACC |
|---|---|---|---|---|
| Engine bear (brief scenarios.bear: 1% growth FY27-30, WACC +1 point, 33.2% margin) | USD 39.91 | -55.7% | SELL | 8.55% |
| **Stacked bear: engine bear + PM bear margin 31.9%** (PM decisions 13 Oct: no stake tax, beta 0.6091 kept, so neither is stacked) | **USD 38.25** | **-57.6%** | **SELL** | 8.55% |
| Information only: stacked bear + FY26 5.0% (audit finding 3, not decided) | USD 37.86 | -58.0% | SELL | 8.55% |
| Superseded: memo bear 13 Oct (ERP 5.0%, margin missed) | USD 37.99 | -57.8% | SELL | 9.00% |

The stacked bear matches the Valuation agent's information-only run (USD 38.25). Scratch runs: `scratch/stacked_bear_319`, `stacked_bear_319_fy26_5`. The new stacked bear is USD 0.26 **higher** than the old memo figure: the lower ERP adds more than the 31.9% margin takes away.

---

## B. Is the SELL just a harsh base case? (assumptions most likely too harsh)

Each test is one change, using the engine (`bear_runs.json`, the `harsh_*` and `generous_*` keys):

| desk assumption that may be too harsh | generous alternative (source) | value | impact | 13 Oct (superseded) |
|---|---|---|---|---|
| Beta 0.61 (industry bottom-up) | 0.35, KO 5-year weekly regression (`risk/risk.json`) | USD 62.01 | **+USD 11.26** | USD 59.24 |
| IRS case lost | Win: liability 0, USD 6.0bn refunded, 19.9% tax | USD 58.20 | +USD 7.44 | USD 54.90 |
| Terminal growth 2.0% | 3.0%, the FY27-30 rate | USD 58.16 | +USD 7.40 | USD 53.63 |
| Terminal RONIC 27.0% | 31.4%, IRS deposit removed from capital (ko-roic-evidence.md option 3) | USD 51.21 | +USD 0.45 | USD 48.02 |
| **All four together** | | **USD 84.19 (-6.6%)** | **+USD 33.43: HOLD** | USD 79.45, SELL |

**Which of the four does HOLD need? (all four, leaving one out)**

| left out | value | upside | rating |
|---|---|---|---|
| beta 0.35 | USD 66.78 | -25.9% | SELL |
| IRS win | USD 75.75 | -15.9% | SELL |
| terminal growth 3% | USD 70.50 | -21.8% | SELL |
| RONIC 31.4% | USD 83.01 | -7.9% | HOLD |

So HOLD needs **all three** big generous assumptions at once (KO's own regression beta, an IRS win and 3% perpetual growth). None of the combinations reaches BUY (USD 103.64).

Not run, but each is likely a little harsh too: capex of 4.41% of sales includes CCBA; minorities over-deducted by up to about USD 0.26 a share (CCBA's outside owner); no margin expansion allowed although Q2 2026 reached 35.6%. One input is slightly **generous**: D&A uses the 2.68% average against FY25's 2.19% (USD 50.50, -USD 0.25).

**Conclusion (changed from 13 Oct):** the stacked bear case is USD 12.51 below the base (USD 38.25 vs USD 50.76). The SELL is robust to every single change, bear or generous. **But it is no longer true that "every generous assumption stacked stays SELL":** with the 4.2% ERP, regression beta + IRS win + 3% terminal growth gives USD 83.01-84.19, just above the HOLD line of USD 81.11. That combination needs a 0.35 beta with an R-squared of a few percent, a court win that is still pending, and perpetual growth at the FY27-30 rate. Even then the value is 6.6% below the price.

---

## C. Management's guidance track record (Q4 results 8-Ks, exhibit 99.1; unchanged by the re-run)

| FY | Guided in (accession) | Organic growth guided / actual | Comparable EPS growth guided / actual | Currency on revenue guided / actual | FCF guided / actual (USD bn) |
|---|---|---|---|---|---|
| 2019 | 0000021344-19-000010 | c.4% / **6%** | -1% to +1% / **+1%** (USD 2.11) | -3% to -4% / not checked | CFO at least 8.0 / **10.5** |
| 2020 | 0000021344-20-000002 | c.5% / **-9%** (Covid) | c.USD 2.25 / **USD 1.95** | 0 to -1% / -2% | c.8.0 / **8.7** |
| 2021 | 0000021344-21-000003 | high single digit / **16%** | high single to low double digit / **+19%** | +2 to +3% / **+1%** | at least 8.5 / **11.3** |
| 2022 | 0000021344-22-000004 | 7-8% / **16%** | 5-6% / **+7%** | -2 to -3% / **-7%** | c.10.5 / **9.5 (miss)** |
| 2023 | 0000021344-23-000005 | 7-8% / **12%** | 4-5% / **+8%** | -2 to -3% / **-4%** | c.9.5 / **9.7** |
| 2024 | 0000021344-24-000004 | 6-7% / **12%** | 4-5% / **+7%** | -2 to -3% / **-5%** | c.9.2 / **10.8** ex IRS deposit (4.7 reported) |
| 2025 | 0000021344-25-000005 | 5-6% / **5% (low end)** | 2-3% / **+4%** | -3 to -4% / **-2%** | c.9.5 ex fairlife / **11.4** |
| 2026 | 0001628280-26-006642, raised in 0001628280-26-049922 | 4-5%, raised to c.5% / H1 Q2 +6% | 7-8%, raised to 9-10% / not yet known | +1%, then 1-2%, now c.1% / not yet known | 12.2, raised to 12.4 / H1 6.9 |

Outcomes come from the following year's Q4 8-K headline (FY25 outcome: 0001628280-26-006642). Currency actuals are from ko-growth-evidence.md. FY19 currency actual was not checked.

**Reading:**
1. **EPS guidance is conservative**, met or beaten every year except Covid-hit 2020. This is a point *against* the bear.
2. **The organic beats in FY21-24 were inflation-driven** (Argentina pricing was more than half of Q4 2024 price/mix, Q4 2024 8-K), and currency took most of it back; management under-called that headwind in FY21-24.
3. **FY25 was the first year organic growth landed only at the low end** of guidance (5% vs 5-6%), with flat volume.
4. **On the IRS, management's confidence has been wrong at both Tax Court stages and the liability estimate has only gone up**, but the 3M appeal ruling (8th Circuit, Oct 2025) is the first outside evidence on its side.

---

**Strongest reason not to buy:** At USD 90.12 the market is pricing KO at a 5.14% WACC (desk 7.55%) and a 3.2% free-cash-flow yield, about 2 points below a 5.22% risk-free Treasury, before any IRS payment; the stacked bear case is USD 38.25, and even KO's own regression beta, an IRS win and 3% perpetual growth all together only reach USD 84.19, still below the price and far below BUY.
