# Bear agent notes: The Coca-Cola Company (KO), run 2026-10-13

All values per share are in **US dollars (USD)**. Totals are in **USD m**. The share price is $90.12 (Yahoo, 13 Oct 2026).

## What I did
1. **Read the inputs.** I read CLAUDE.md, `.claude/agents/bear.md`, `briefs/KO.yaml`, `docs/phase5/*.md` and everything in this run. Where they differ, I used `inputs.yaml` as the authoritative input set: `data/notes.md` predates the PM's later CCBA, stakes and IRS decisions.
2. **Wrote `run_bear.py`.** For each of 25 scenarios it writes a scratch copy of the brief and `inputs.yaml` with **one change**. It saves them to `bear/scratch/<name>/` and runs `python -m desk.valuation_run` on them. Results are in `bear_runs.json`. I did not edit the brief, `inputs.yaml` or the desk code.
3. **Reproduced the base.** The base check reproduces $47.60, so the copies load exactly as the Valuation agent's did.
4. **Reconciled FY26 cash.** I matched the model's FY26 unlevered FCF (11,358) to KO's FY26 FCF guidance ($12.4bn), using figures sourced from the FY25 10-K and the Q2 2026 8-K and 10-Q. The arithmetic is in the script, commented.
5. **Checked the guidance record.** I compared guidance with outcomes for FY19-FY26, using the Q4 8-Ks:
   - pre-downloaded text in /tmp/claude-0/ko/;
   - the Q4 2019 release, fetched from EDGAR (accession 0000021344-20-000002), because it was not pre-downloaded.
6. **Checked the beta history.** I read Damodaran's `betas.xls` (supplied by the PM) with a small file reader, because `xlrd` is not installed. That gave the year-by-year soft-beverage unlevered betas.

## Results (impact vs the $47.60 base, USD per share, one change each)

| # | challenge (agent challenged) | impact |
|---|---|---|
| 1 | Margin 30.0% (FY24, includes CCBA) (Fundamentals) | -$4.79 |
| 1 | Like-for-like margin 31.94% (FY24 ex-CCBA) | -$1.88 |
| 2 | Growth 1% a year in FY27-30 (Valuation, growth path) | -$3.30 |
| 2 | FY26 growth 4.5% instead of 6.0% | -$0.71 |
| 3 | IRS: base already assumes a loss. Value if KO wins | +$7.29 ($54.90) |
| 3 | IRS: deduct the extra H1 2026 accrual | -$0.22 |
| 3 | FY26 FCF reconciliation (Data) | model 11,358 vs guidance 12,400; gap 1,042, unexplained residual +60 |
| 4 | Stakes back at 31 Dec 2025 values (Data, bridge) | -$1.30 |
| 4 | Monster stake -30% | -$1.32 |
| 4 | Stakes after 21% tax on the gain over book | -$1.33 |
| 5 | Beta 0.868, the 2022-26 Damodaran average (Risk) | -$7.60 (WACC 9.20%) |
| 5 | Beta 0.741, the 2024 level | -$4.21 |

**Too-harsh tests:**

| test | value |
|---|---|
| Regression beta 0.35 | +$11.64 |
| IRS win | +$7.29 |
| Terminal growth 3% | +$6.02 |
| Terminal RONIC 31.4% | +$0.41 |
| D&A at FY25's 2.19% (this one is a generous input, not a harsh one) | -$0.25 |
| **All four generous changes together** | **$79.45, still SELL** (HOLD needs $81.11) |

## FLAGs
1. **`risk/notes.md` is stale.** It still says "STOP: beta MISSING". `inputs.yaml` has since been filled with 0.6091 from the PM-supplied xls (`risk/beta_evidence.json`). The memo should cite beta_evidence.json, not risk/notes.md.
2. **The Valuation agent's 0.820485 average beta** was sourced only as "given by the lead agent" (`valuation/run_sanity.py`). I verified it against the xls: Beverage (Soft), "Average (2022-2026)" = 0.8204851. It is now sourced.
3. **Brief bear margin of 30.0% is on the wrong basis.** It includes CCBA but is applied to ex-CCBA sales. The like-for-like FY24 ex-CCBA figure is 31.94%, built from CCBA's calendar 2024 numbers, which is the same year. I recommend the PM consider 31.9% as the bear margin. I did not change it.
4. **FCF reconciliation uses FY25 actuals as FY26 proxies** (interest paid and received, investee dividends, stock-based compensation). The residual of +60 includes CCBA's part-year cash flow, which is not disclosed.
5. **The tax-leakage test on the stakes uses book value as a stand-in for tax basis.** The tax basis is not disclosed. The 21% is the US federal statutory rate.
6. **The Monster -30% and FY26 4.5% growth runs are stress tests, not forecasts.** No source gives either number.
7. **FY19 currency outcome not checked.** FY20 outcomes are Covid-distorted.

## Missing
- **GLP-1 and sugar-tax effects: MISSING.** I found no sourced quantification. Only the FY25 10-K risk-factor wording is available, so I did not run a separate scenario. The 1% growth run (challenge 2) is the nearest proxy.
- **Independent industry growth forecast: MISSING** (also flagged by the Data agent).
- **KO's long-term growth algorithm: MISSING.** It has not been found in a primary source.

## Confidence
- **High:** the impacts are mechanical engine runs on sourced single changes. The track-record table is quoted from the 8-Ks.
- **Medium:** the FCF reconciliation, because of the FY25 proxies.
- **Low:** the stakes tax-leakage and Monster stress magnitudes.

**On the conclusion:** I am highly confident that the SELL does not depend on the bear case. Even with every generous assumption stacked, the value stays below the HOLD line.

## Files
- `challenges.md`: the five challenges, the too-harsh test, the track record and the final line
- `run_bear.py`: the script that runs every scenario
- `bear_runs.json`: all results
- `scratch/<scenario>/`: the brief and inputs copies, plus the engine output for each scenario

Strongest reason not to buy: At $90.12 KO trades on a 3.2% free-cash-flow yield, about 2 points below the 5.22% Treasury, before any IRS payment. Even stacking every generous assumption, the engine gives $79.45, still a SELL.
