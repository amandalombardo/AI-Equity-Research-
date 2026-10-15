# Bear agent notes: The Coca-Cola Company (KO), run 2026-10-13

## Re-run 15 Oct 2026 (evidence audit)

Every value per share is in **US dollars (USD)**; totals in **USD m**. Price USD 90.12 (Yahoo, 13 Oct 2026). HOLD line USD 81.11, BUY line USD 103.64.

### What I did
1. Read the audit (`docs/audit-2026-10-15/KO.md`, `erp-evidence.md`), the new top section of `valuation/notes.md`, the updated `briefs/KO.yaml` and `inputs.yaml`. I did not edit the brief, `inputs.yaml` or `desk/`.
2. Updated `run_bear.py` (header explains the changes) and re-ran it: `PYTHONPATH=. python runs/KO/2026-10-13/bear/run_bear.py`. Every value is a `desk.valuation_run` CLI run on a scratch copy with one change.
   - Base check reproduces **USD 50.76** (SELL, WACC 7.55%) and the engine bear **USD 39.91**, as in `valuation.json`.
   - Scenarios that move the **listed** stakes now cut `priced_at_valuation_date_musd` by the same amount, so run-date market values are not grown again (mistakes log row 24). The IRS-win deposit refund is added to the grown part, as the Valuation agent did.
   - New runs: the PM bear margin 31.9% alone; the **stacked bear case** (brief bear + 31.9%); ERP 5.0% (Kroll) and 5.5% (Fernandez); FY26 growth 5.0%; leave-one-out runs on the generous case.
3. Saved the 13 Oct results as `bear_runs_2026-10-13_superseded.json`; `bear_runs.json` now holds the 15 Oct results. Rewrote `challenges.md` with the new values, the 13 Oct figures alongside, and the PM's 13 Oct bear responses kept in the summary table.

### Main new numbers (USD per share)
| item | 15 Oct | 13 Oct (superseded) |
|---|---|---|
| Base | 50.76 SELL (-43.7%) | 47.60 SELL |
| Engine bear (33.2% margin) | 39.91 SELL | 37.99 |
| **Stacked bear (engine bear + PM margin 31.9%)** | **38.25 SELL (-57.6%)** | not run (memo showed 37.99, margin missed) |
| Stacked bear + FY26 5.0% (information only) | 37.86 | - |
| 1. Margin 30.0% / 31.94% / 31.9% | -5.14 / -2.02 / -2.08 | -4.79 / -1.88 / - |
| 2. Growth 1% FY27-30 / FY26 4.5% | -3.58 / -0.76 | -3.30 / -0.71 |
| 3. IRS +USD 900m accrual / IRS win | -0.22 / +7.44 (USD 58.20) | -0.22 / +7.29 (USD 54.90) |
| 4. Stakes Dec 2025 / Monster -30% / 21% tax | -1.22 / -1.24 / -1.25 | -1.30 / -1.32 / -1.33 |
| 5. Beta 0.868 / 0.741 | -7.66 (WACC 8.56%) / -4.21 (WACC 8.06%) | -7.60 (9.20%) / -4.21 |
| Audit: ERP 5.0% Kroll / 5.5% Fernandez | -3.74 (USD 47.01) / -5.81 (USD 44.95) | - |
| Audit: FY26 growth 5.0% | -0.51 (USD 50.25) | - |
| Generous: beta 0.35 / IRS win / g 3% / RONIC 31.4% | +11.26 / +7.44 / +7.40 / +0.45 | +11.64 / +7.29 / +6.02 / +0.41 |
| **All four generous together** | **84.19, HOLD (-6.6%)** | 79.45, SELL |
| All generous except RONIC | 83.01 HOLD | - |
| All generous except beta / IRS / g 3% | 66.78 / 75.75 / 70.50, all SELL | - |

FY26 FCF reconciliation, FCF yield (3.20%) and leverage (1.85x -> 2.72x) are unchanged: the ERP and roll-forward do not touch them.

### FLAGs (15 Oct 2026)
1. **The 13 Oct conclusion "even every generous assumption stacked stays SELL" no longer holds.** With ERP 4.2%, regression beta 0.35 + IRS win + terminal growth 3% gives USD 83.01 (USD 84.19 with RONIC 31.4%), just above HOLD (USD 81.11). All three are needed; none reaches BUY. The memo text and the final line must change.
2. **The memo's bear figure must be the stacked USD 38.25**, not the engine's USD 39.91 nor the old USD 37.99. It is USD 0.26 above the old memo figure because the ERP cut outweighs the margin.
3. **ERP stress lines keep the 10-year 5.22% risk-free.** Kroll pairs 5.0% with the 20-year (5.60%); that two-change case was not run. All ERP figures are secondhand (erp-evidence.md).
4. **Beta 2022-26 average now gives an 8.56% WACC, inside the 6-9% range** (it was 9.20% on 13 Oct). The honesty argument against challenge 5 is weaker.
5. **The 8th Circuit 3M ruling** (audit finding 5) is now cited in challenge 3 and the track record: a win is more plausible than the 13 Oct text implied.
6. Unchanged from 13 Oct: stake tax uses book as tax basis; FCF reconciliation uses FY25 proxies; Monster -30% and FY26 4.5% are stress tests; GLP-1 / sugar-tax quantification, industry growth forecast and the long-term algorithm are MISSING.
7. `python -m pytest`: not run; no code in `desk/` was changed.

### Confidence
High on the mechanics (engine reproduces the base, engine bear and the Valuation agent's USD 38.25 and USD 43.10 to the cent). High that the SELL survives every single change. Medium on how close the generous stack sits to HOLD: it is within USD 3.08 of the line and depends on the unconfirmed 4.2% ERP.

Strongest reason not to buy: At USD 90.12 the market is pricing KO at a 5.14% WACC and a 3.2% free-cash-flow yield, about 2 points below the 5.22% Treasury before any IRS payment; the stacked bear case is USD 38.25, and even the regression beta, an IRS win and 3% perpetual growth together only reach USD 84.19, below the price and far below BUY.

---

# Original run, 13 Oct 2026 (SUPERSEDED by the 15 Oct re-run above; kept for the record)

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

## Results (impact vs the $47.60 base, USD per share, one change each): SUPERSEDED 15 Oct 2026

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

**Too-harsh tests (SUPERSEDED 15 Oct 2026: the all-four case is now USD 84.19, HOLD):**

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

Superseded 13 Oct final line: At $90.12 KO trades on a 3.2% free-cash-flow yield, about 2 points below the 5.22% Treasury, before any IRS payment. Even stacking every generous assumption, the engine gives $79.45, still a SELL.
