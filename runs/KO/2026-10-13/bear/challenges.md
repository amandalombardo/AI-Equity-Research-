# Bear case: The Coca-Cola Company (KO), run 2026-10-13

All values per share are in **US dollars (USD)**. Totals are **USD m**. The share price is $90.12 (Yahoo, 13 Oct 2026). Every "impact" comes from the desk engine: `python -m desk.valuation_run` run on a scratch copy of the brief and `inputs.yaml` with **one change**. The script is `bear/run_bear.py`, the results are in `bear/bear_runs.json`, and each copy is in `bear/scratch/<name>/`. The brief and `inputs.yaml` were not edited.

**Starting point** (`valuation/valuation.json`):
- **Base:** $47.60, SELL (-47.2%).
- **Brief bear case:** $37.99, SELL (-57.8%). This is the base plus 1% growth in FY27-30 plus 1 point on the WACC (9.0%).
- **Rating lines:** HOLD needs at least $81.11, BUY at least $103.64.

The base is already a SELL, so the most useful question is not "can it get worse?" but "**is the SELL just a harsh base case?**" Section B answers that.

---

## A. Challenges

### 1. Margin: the 33.2% base margin assumes the best year ever is the new normal (challenges the Fundamentals agent and brief item B)

- **Claim:** The model holds the FY25 ex-CCBA comparable margin of 33.2% flat for ever. That is a peak-year figure. It also excludes write-downs that keep coming back.
- **Evidence:**
  - **The margin has only just reached this level.** Comparable operating margin was 28.7%, 28.7%, 29.1%, 30.0% and 31.2% in FY21 to FY25 (`fundamentals/ratios.csv`; Q4 results 8-Ks 0000021344-22-000004 through 0001628280-26-006642).
  - **Part of the rise is mix, not efficiency.** It comes from selling low-margin bottlers (Fundamentals FLAG 9; brief section 5B).
  - **"Comparable" leaves out impairments that recur every year.** Each year since FY24 has had a large one: FY24 $886m (North America $760m) and FY25 $1,045m (North America $960m). On a reported basis FY25 was 28.7% against 31.2% comparable (Q4 2025 8-K 0001628280-26-006642 p.28; `fundamentals/commentary.md` FLAG 1). Repeated brand write-downs are real capital lost on acquisitions, not "one-offs".
- **Value impact (USD per share):**

  | test | margin | value | impact |
  |---|---|---|---|
  | Brief's literal bear: FY24 comparable margin (Q4 2024 8-K 0000021344-25-000005) | 30.0% | **$42.82** | **-$4.79** |
  | Like-for-like: FY24 margin **ex-CCBA**, (14,085 - 266.2) / (46,897 - 3,632.3) | 31.94% | $45.73 | -$1.88 |

  Scratch runs: `scratch/c1_margin_300`, `scratch/c1_margin_fy24_ex_ccba`.
- **Honesty note:** The 30.0% includes CCBA, a bottler with a 7.3% margin, but the base sales exclude CCBA. So -$4.79 mixes two bases and overstates the bear case. The fair bear figure is the like-for-like **-$1.88**. Recent trading also argues against the bear: the Q2 2026 comparable margin was 35.6% against 34.7% a year earlier (Q2 2026 8-K 0001628280-26-049922).

### 2. Currency: dollar growth of 3% a year assumes currencies stop falling, and management has repeatedly got currency wrong (challenges the Valuation agent's growth path, brief item A)

- **Claim:** FY27-30 growth of 3.0% in USD assumes only a 1-point currency drag. Over 2020-25 the average drag was 3.2 points. FY26's +6.0% is also flattered by a currency tailwind and a one-off FIFA World Cup boost.
- **Evidence:**
  - **The drag history.** Currency took 2, +1 (a tailwind), 7, 4, 5 and 2 points in 2020-25 (`docs/phase5/ko-growth-evidence.md`, from the Q4 8-Ks).
  - **Management under-forecast the headwind in 3 of 5 years.** The guided figures are in the track-record table below. FY21 guided a +2-3% tailwind and delivered +1%. FY22 guided -2-3% and delivered -7%. FY23 guided -2-3% and delivered -4%. FY24 guided -2-3% and delivered -5%. FY25 guided -3-4% and delivered -2%.
  - **The FY26 tailwind is already shrinking.** It was cut from 1-2% to about 1% in July (Q2 2026 8-K 0001628280-26-049922).
  - **The Q2 2026 volume growth of 5% coincided with the World Cup.** The company ran its campaign "at unprecedented scale across more than 180 markets" (same 8-K), which makes FY27 a tough year to grow against.
  - **FY25 unit case volume was flat** ("was Even for the Full Year", Q4 2025 8-K 0001628280-26-006642), so growth was all price and mix.
  - **The FY25 10-K risk factors name the long-term pressures:** "the effects or perceived effects of the usage of weight-loss drugs on consumption patterns" and "potential new or increased taxes on sweetened beverages" (10-K 0001628280-26-010047, Item 1A).
  - **No independent industry forecast** could be obtained (`data/notes.md`, MISSING).
- **Value impact (USD per share):**

  | test | value | impact |
  |---|---|---|
  | FY27-30 growth 1.0% (full 3.2-point average drag), FY26 unchanged | **$44.31** | **-$3.30** |
  | FY26 growth 4.5% instead of 6.0% (World Cup and currency tailwind fade) | $46.89 | -$0.71 |

  Scratch runs: `scratch/c2_growth_1pct`, `scratch/c2_fy26_4p5`.
- **Honesty note:** The growth evidence paper calls 1% "too punitive". It removes the Argentina currency fall but not the Argentina price rises that went with it. The -$3.30 is a stress test, not a forecast.

### 3. IRS case and FY26 cash: the market's "$12.4bn of free cash flow" is not the cash shareholders keep (challenges the Data agent's cash and tax inputs)

- **Claim:** The headline FY26 FCF guidance of about $12.4bn (Q2 2026 8-K 0001628280-26-049922) excludes the IRS case. It also includes dividends from stakes that the DCF values separately. On a like-for-like basis KO's cash yield is far below the risk-free rate, and a loss in the IRS case would lift leverage sharply.
- **Evidence: the FY26 cash reconciliation (USD m, script `run_bear.py`, inputs sourced as shown)**

  | item | USD m | source |
  |---|---|---|
  | Model FY26 unlevered FCF (ex-CCBA, 23.7% tax) | 11,358 | `valuation.json` |
  | + Extra tax from the IRS case that guidance leaves out (EBIT 15,589 x 3.8 points) | +592 | guidance tax 19.9% "does not include the impact of ongoing tax litigation" (Q2 2026 8-K); +3.8 points (Q2 2026 10-Q 0001628280-26-050503 Note 9) |
  | + Dividends from equity investees (in KO's cash flow; the DCF values the stakes in the bridge instead) | +993 | FY25 10-K 0001628280-26-010047, equity method note (FY25 actual used as proxy) |
  | + Stock-based compensation (non-cash, added back in KO's cash from operations) | +279 | FY25 10-K cash flow statement |
  | - Net interest after tax (KO's FCF is after interest; the DCF is before) | -751 | interest paid 1,724 (FY25 10-K) - interest income 786 (XBRL), x (1 - 19.9%) |
  | - Guided capex $2.2bn vs model capex 2,069 | -131 | Q2 2026 8-K |
  | **Residual** (CCBA's part-year cash flow, other items) | **+60** | |
  | **KO guidance** | **12,400** | Q2 2026 8-K |

  - **What the reconciliation shows:** the 1,042 gap between guidance and the model is almost entirely a difference of basis. There is no hidden cash and no double count. The model's FY26 cash is consistent with guidance, so the Data inputs pass this test.
  - **What it means for a buyer:** the market's headline FCF yield is 3.20% ($12.4bn / $387.7bn market cap). That is already 2.0 points below the 10-year Treasury at 5.22% (FRED DGS10). It is even lower once the IRS tax is taken out.
  - **The IRS track record:**
    - KO has said since 2020 that it "will ultimately prevail" (Q4 2020 8-K 0000021344-21-000003). It has lost at the Tax Court twice.
    - The potential liability has risen from about $12bn (December 2020, same 8-K) to $14bn (December 2025, 10-K XBRL `ko:IncrementalTaxAndInterestLiability`), after the $6.0bn already paid for 2007-09.
    - The expected rise in the tax rate went from 3.5% (Q4 2020 8-K and FY25 10-K) to 3.8% (Q2 2026 10-Q).
    - Interest "would continue to accrue until the time any such potential liability ... were to be paid" (FY25 10-K).
  - **Leverage if the $14bn is paid in cash:** net debt / comparable EBITDA rises from 1.85x to **2.72x** (`desk.fundamentals.leverage`, net debt 29,686 + 14,000 over 16,063).
- **Value impact (USD per share):**

  | test | value | impact |
  |---|---|---|
  | The base already assumes a **loss**. For a buyer who prices in management's view of a **win** (no liability, $6.0bn deposit refunded, 19.9% tax), the difference is | $54.90 if it wins | **-$7.29** |
  | of which: removing the $14bn liability alone | | +$3.46 |
  | of which: the 19.9% tax rate alone | | +$2.35 |
  | Bear add-on: also deduct the $900m H1 2026 accrual (Q2 2026 10-Q Note 9) | $47.38 | -$0.22 |

  Scratch runs: `scratch/c3_irs_win`, `c3_irs_liab_only`, `c3_irs_tax_only`, `c3_irs_plus900`.
- **Honesty note:** The PM excluded the $900m because the 23.7% tax rate already charges 2026 (mistakes log row 17), so the -$0.22 is partly double-counted. A loss is already in the base case. **The IRS case is a reason the market price is too high, not a reason the desk value is too high.**

### 4. Equity stakes at market: $46.6bn of value depends on other companies' share prices, Monster most of all (challenges the Data agent's bridge input and the brief's stakes rule, item D)

- **Claim:** The bridge adds the listed stakes at their 13 Oct 2026 market value: 39,540 of the 46,626 total. That figure is after a +15% rally in 2026. It is 45% Monster, a stock on about 40x earnings. It is also before any tax KO would pay if it sold.
- **Evidence:**
  - **Monster:** 17,775 of 39,540 (`data/associates_rollforward_check.csv`). MNST's LTM P/E is 40.1x and EV/EBITDA 29.1x (`data/peers.csv`).
  - **Book vs market:** listed stakes were 34,286 at fair value vs 13,999 at book on 31 Dec 2025 (FY25 10-K, equity method note).
  - **Tax on the gain:** a 21% US statutory tax on the gain over book is 5,364 (book used as a stand-in for tax basis, which is not disclosed: FLAG).
  - **Cash these stakes actually pay:** dividends from investees were $993m in FY25 (10-K), about 2.5% of their market value.
- **Value impact (USD per share):**

  | test | value | impact |
  |---|---|---|
  | Listed stakes back at 31 Dec 2025 fair value (the 2026 rally reverses) | $46.30 | -$1.30 |
  | Monster stake falls 30% (stress, not a forecast) | $46.29 | -$1.32 |
  | Stakes after a 21% tax on the gain over book | $46.28 | **-$1.33** |

  Scratch runs: `scratch/c4_stakes_dec25`, `c4_monster_m30`, `c4_stakes_tax`.
- **Honesty note:** This lever is small, about $1.3 a share each. Adding the stakes is correct, because their income is outside operating income. They are not where the SELL comes from.

### 5. Beta: 0.61 is the soft-drinks industry's beta at a cyclical low (challenges the Risk agent)

- **Claim:** The 0.6091 beta uses the industry's unlevered beta in January 2026 (0.575). That number has more than halved in two years. If it reverts to its own 5-year average, the WACC rises from 8.0% to 9.2%.
- **Evidence:** I read Damodaran's file (`data/damodaran_betas_us_jan2026.xls`, sheet "Industry Averages", row "Beverage (Soft)", 27 firms, unlevered beta corrected for cash) with a small reader. The year columns give 1.116 (2022), 1.201 (2023), 0.700 (2024), 0.510 (2025), 0.575 (current) and an **average of 0.8205** (2022-26). That confirms the 0.820485 the Valuation agent used, which had been recorded only as "given by the lead agent". Relevering at KO's market D/E (x1.0584, `risk/beta_evidence.json`) gives 0.868.
- **Value impact (USD per share):**

  | test | WACC | value | impact |
  |---|---|---|---|
  | Beta 0.868 (2022-26 average) | 9.20% | **$40.01** | **-$7.60** |
  | Beta 0.741 (2024 level) | 8.61% | $43.40 | -$4.21 |

  Scratch runs: `scratch/c5_beta_avg_2022_26`, `scratch/c5_beta_y2024`.
- **Honesty note:** KO's own regressions point the other way: 0.13 (2-year weekly), 0.30 (5-year monthly), 0.35 (5-year weekly), all with R-squared of 1-12% (`risk/risk.json`). At 9.2% the WACC is above the desk's 6-9% sanity range.

---

## B. Is the SELL just a harsh base case? (assumptions most likely too harsh)

Each test is one change, using the engine (`bear_runs.json`, the `harsh_*` keys):

| desk assumption that may be too harsh | generous alternative (source) | value | impact |
|---|---|---|---|
| Beta 0.61 (industry bottom-up) | 0.35, KO 5-year weekly regression (`risk/risk.json`) | $59.24 | **+$11.64** |
| IRS case lost | Win: liability 0, $6.0bn refunded, 19.9% tax | $54.90 | +$7.29 |
| Terminal growth 2.0% | 3.0%, the FY27-30 rate | $53.63 | +$6.02 |
| Terminal RONIC 27.0% | 31.4%, IRS deposit removed from capital (ko-roic-evidence.md option 3) | $48.02 | +$0.41 |
| **All four together** | | **$79.45** | **+$31.85, still SELL** (HOLD needs $81.11) |

Not run, but each is likely a little harsh too:
- **Capex of 4.41% of sales includes CCBA**, a capital-heavy bottler, applied to ex-CCBA sales.
- **Minorities over-deducted** by up to about $0.26 a share (CCBA's outside owner, `docs/phase5/ko-ccba-evidence.md`).
- **No margin expansion is allowed**, although Q2 2026 reached 35.6%.

One input is slightly **generous**: D&A uses the 2.68% average against FY25's 2.19%. Using FY25 changes the value by -$0.25.

**Conclusion:** the bear case is not just the base case: it is $9.61 lower ($37.99 vs $47.60). More importantly, the SELL does not depend on it. Even stacking the four most generous assumptions the evidence allows, the engine gives $79.45, below the HOLD line. The desk's biggest single harshness is the beta. Even the regression beta alone ($59.24) leaves KO 34% below the price.

---

## C. Management's guidance track record (Q4 results 8-Ks, exhibit 99.1)

| FY | Guided in (accession) | Organic growth guided / actual | Comparable EPS growth guided / actual | Currency on revenue guided / actual | FCF guided / actual (USD bn) |
|---|---|---|---|---|---|
| 2019 | 0000021344-19-000010 | c.4% / **6%** | -1% to +1% / **+1%** ($2.11) | -3% to -4% / not checked | CFO at least 8.0 / **10.5** |
| 2020 | 0000021344-20-000002 | c.5% / **-9%** (Covid) | c.$2.25 / **$1.95** | 0 to -1% / -2% | c.8.0 / **8.7** |
| 2021 | 0000021344-21-000003 | high single digit / **16%** | high single to low double digit / **+19%** | +2 to +3% / **+1%** | at least 8.5 / **11.3** |
| 2022 | 0000021344-22-000004 | 7-8% / **16%** | 5-6% / **+7%** | -2 to -3% / **-7%** | c.10.5 / **9.5 (miss)** |
| 2023 | 0000021344-23-000005 | 7-8% / **12%** | 4-5% / **+8%** | -2 to -3% / **-4%** | c.9.5 / **9.7** |
| 2024 | 0000021344-24-000004 | 6-7% / **12%** | 4-5% / **+7%** | -2 to -3% / **-5%** | c.9.2 / **10.8** ex IRS deposit (4.7 reported) |
| 2025 | 0000021344-25-000005 | 5-6% / **5% (low end)** | 2-3% / **+4%** | -3 to -4% / **-2%** | c.9.5 ex fairlife / **11.4** |
| 2026 | 0001628280-26-006642, raised in 0001628280-26-049922 | 4-5%, raised to c.5% / H1 Q2 +6% | 7-8%, raised to 9-10% / not yet known | +1%, then 1-2%, now c.1% / not yet known | 12.2, raised to 12.4 / H1 6.9 |

Outcomes come from the following year's Q4 8-K headline (FY25 outcome: 0001628280-26-006642). Currency actuals are from ko-growth-evidence.md. FY19 currency actual was not checked.

**Reading:**
1. **EPS guidance is conservative.** It was met or beaten every year except Covid-hit 2020. This is a point *against* the bear: management sandbags.
2. **The organic beats in FY21-24 were inflation-driven.** Argentina pricing produced more than half of Q4 2024 price/mix (Q4 2024 8-K). Currency then took most of it back, and management under-called that headwind in FY21-24.
3. **FY25 was the first year organic growth landed only at the low end** of guidance (5% vs 5-6%), with flat volume.
4. **On the IRS, management's confidence has been wrong at every court stage so far.** The liability estimate has only gone up.

---

**Strongest reason not to buy:** At $90.12 the market is paying about 30x earnings for a 3.2% free-cash-flow yield, about 2 points below a 5.22% risk-free Treasury, before any IRS payment. Even if every generous assumption the evidence allows is stacked together (regression beta, an IRS win, 3% perpetual growth, a 31% return on new capital), the engine still values KO at $79.45, below the HOLD line.
