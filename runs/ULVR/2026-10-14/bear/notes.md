# Bear case agent notes: Unilever PLC (ULVR), run 2026-10-14

## Re-run 15 Oct 2026 (evidence audit)

Money in EUR m unless labelled; values per share in pence (GBp); McCormick prices in USD. Price 4,710.5p (ULVR.L, 13 Oct 2026). SELL line 4,239.45p (-10%); BUY 5,417.1p (+15%).

### Why
Evidence audit of 15 Oct 2026 (docs/audit-2026-10-15/ULVR.md). The PM's decisions are all already in briefs/ULVR.yaml and inputs.yaml; I changed neither:
- ERP **4.2%** (Damodaran implied; was 5.0% with no source)
- pension plans in deficit deducted after tax: **EUR 698.6m**
- McCormick dividends before closing deducted: **EUR 642.9m** (3 quarters)
- JVs at the new Ke 7.164%: **EUR 4,181.2m**; associates EUR 7,533.5m
- FY26 growth **+2.0%** in the base and the bear (was +0.5%)

Valuation re-run: base **4,258.5p HOLD (-9.6%)**, 19.1p above the SELL line; engine bear **3,475.6p**; WACC **6.50%** (valuation/notes.md, new top section).

### What I did
1. Archived the 14 Oct outputs in `scratch/`: `bear_results_2026-10-14_superseded.json`, `challenges_2026-10-14_superseded.md` and `run_bear_2026-10-14_superseded.py`. Deleted every scratch test folder and rebuilt them all from the current brief and inputs.
2. Updated `run_bear.py`. Every number is still a full `python -m desk.valuation_run` run on a scratch copy.
   - The control copy reproduces 4,258.5p and 3,475.6p exactly (asserted against valuation/valuation.json).
   - New asserts: associates = JV at Ke 7.164% + EUR 3,352.3m; Foods consideration = cash + shares x USD 44.64 - EUR 642.9m of dividends.
   - **McCormick price tests now keep the dividend deduction.** Without it they would overstate the consideration by EUR 642.9m.
   - **Deal-fails tests use FY26 +0.5%** (whole Group incl. Foods, H1 2026 6-K). This is the matching perimeter once Foods stays, and the same logic the PM used to move to +2.0%.
   - JVs are re-valued at Gordon growth wherever Ke or g moves, including the stacked bear at bear Ke 8.164% (EUR 3,544.3m).
   - Added the audit stress lines: ERP 5.0% (Kroll), ERP 5.5% (Fernandez), Bund 3.50% (9 Oct), spread 1.0%, Foods consideration discounted to mid-2027 (cash at Kd; whole at WACC), and 2-quarter McCormick dividends.
   - Replaced the old SELL->HOLD flip-point checks with the new HOLD->SELL breakevens: beta 0.892, margin 17.61%, MKC USD 43.55. All three land on the line (4,238.2-4,239.4p).
3. Rewrote `challenges.md`:
   - five challenges with new values, the stacked bear and the audit stress lines;
   - the PM's 14 Oct responses with a "still holds?" column;
   - the risks to the bear view, the track record (unchanged) and the final line.
4. Wrote `bear_results.json`. Re-run from the repo root: `PYTHONPATH=. python runs/ULVR/2026-10-14/bear/run_bear.py`.

### Old (14 Oct) vs new (15 Oct): each a separate engine run; impact vs the base unless stated
| Test | 14 Oct (base 3,855.3p SELL) | 15 Oct (base 4,258.5p HOLD) | Rating flip |
|---|---|---|---|
| Engine bear | 3,211.9p | 3,475.6p | SELL both |
| 1. Deal fails (no fee / USD 420m fee / EUR 500m still spent) | 3,877 / 3,892 / 3,857p (+22 / +37 / +1p) | 4,394.3 / 4,409.0 / 4,373.5p (**+135.7 / +150.5 / +115.0p**) | SELL -> HOLD (now upside) |
| 2. Tax 25% of the Foods cash (EUR 3,507m) | 3,717.6p (-137.7p) | 4,120.8p (**-137.7p**) | **HOLD -> SELL** |
| 3. HUL at 38.1% of market + others at book | 3,631.8p (-223.5p) | 4,087.1p (**-171.4p**) | **HOLD -> SELL** |
| 3b. HUL at market + others proportionate | 3,554.7p (-300.6p) | 3,997.4p (-261.2p) | **HOLD -> SELL** |
| 4. Margin 16.2% | 3,565.6p (-289.7p) | 3,932.2p (**-326.3p**) | **HOLD -> SELL** |
| 5. Engine bear + JVs at Ke +1 pt (vs engine bear) | 3,190.7p (-21.3p) | 3,449.2p (**-26.4p**) | SELL both |
| Terminal growth 1.1% | 3,689.8p (-165.5p) | 4,037.5p (-221.1p) | **HOLD -> SELL** |
| Consistent bear, terminal g 0.2% (vs the JV-fixed bear) | 2,934.0p (-256.7p) | 3,121.0p (-328.2p) | SELL both |
| RONIC 16.5% / RONIC = WACC | 3,835.0 / 3,472.8p | 4,235.0 / 3,747.3p (-23.6 / -511.2p) | **HOLD -> SELL** (both) |
| Beta 0.9998 (Damodaran 2020-24) | 3,588.1p (-267.2p) | 3,971.9p (-286.7p) | **HOLD -> SELL** |
| Beta 0.91 (own monthly) | 3,792.1p (-63.2p) | 4,191.0p (-67.6p) | **HOLD -> SELL** |
| McCormick 1 s.d. lower (USD 33.15) | 3,653.9p (-201.4p) | 4,057.2p (-201.4p) | **HOLD -> SELL** |
| **Stack: engine bear + JV fix + 16.2% + tax** | 2,817.2p | **3,051.0p** (-1,207.6p) | SELL both |
| **Stack + HUL at market** | 2,436.7p | **2,694.9p** (-1,563.6p) | SELL both |
| *Audit:* ERP 5.0% (Kroll) | n/a (was the base) | 3,854.1p (-404.4p) | **HOLD -> SELL** |
| *Audit:* ERP 5.5% (Fernandez) | n/a | 3,642.4p (-616.1p) | **HOLD -> SELL** |
| *Audit:* Bund 3.50% (9 Oct) | n/a | 4,222.4p (-36.1p) | **HOLD -> SELL** |
| *Audit:* credit spread 1.0% | n/a | 4,231.8p (-26.8p) | **HOLD -> SELL** |
| *Audit:* Foods cash discounted at Kd 4.15% to 30 Jun 2027 (EUR 398.9m) | n/a | 4,242.9p (-15.7p) | stays HOLD (3.5p above the line) |
| *Audit:* whole Foods consideration at WACC 6.50% (EUR 1,456.7m) | n/a | 4,201.3p (-57.2p) | **HOLD -> SELL** |
| *Audit:* McCormick dividends 2 quarters (upside) | n/a | 4,267.0p (+8.4p) | stays HOLD |
| Risk: beta 0.54 (own weekly) | 5,027.4p HOLD | 5,486.2p (+1,227.7p) | HOLD -> **BUY** |
| Risk: margin 18.8% / 18.2% | 4,067.7 / 3,951.9p SELL | 4,497.9 / 4,367.3p | SELL -> HOLD |
| Risk: McCormick USD 57.84 | 4,086.7p SELL | 4,490.0p (+231.4p) | SELL -> HOLD |
| Breakevens: beta 0.892 / margin 17.61% / MKC USD 43.55 | n/a | 4,238.2 / 4,239.0 / 4,239.4p | on the line |

### What flips the rating
- **Now HOLD -> SELL on its own:** all five challenges, plus terminal growth 1.1% and both RONIC tests. Specifically:
  - tax -137.7p; McCormick 1 s.d. -201.4p; HUL at market -171.4p to -261.2p; margin 16.2% -326.3p
  - terminal growth 1.1% -221.1p; RONIC 16.5% -23.6p; RONIC = WACC -511.2p
  - beta 0.9998 -286.7p and beta 0.91 -67.6p
  - ERP 5.0% -404.4p and 5.5% -616.1p; Bund 3.50% -36.1p; spread 1.0% -26.8p; whole Foods consideration at WACC -57.2p
- **Stays HOLD:** Foods cash discounted at Kd (-15.7p, 3.5p above the line) and 2-quarter dividends (+8.4p).
- **Was SELL, now HOLD:** deal fails (+115p to +151p), margin 18.2% and 18.8%, McCormick USD 57.84.
- **Was HOLD, now BUY:** beta 0.54.
- **The PM's 14 Oct bear responses:** all five rested on "stays SELL". None of those conclusions still holds, although the method choices behind them (keep 17.7%, proportionate minorities, beta 0.8844, tax not deducted) are unchanged. See challenges.md for the table.

### FLAGs (re-run)
1. **The bear case now argues against the HOLD.** The HOLD survives only at the lowest sourced ERP (4.2%, secondhand) and the aggregator Bund (3.45%). Every sourced alternative for the ERP, the Bund and the spread gives SELL.
2. **Correction to valuation/notes.md ("Other sizes", Foods timing):** it says the cash-part discount at the cost of debt (-16p) "would make it SELL". The engine re-run gives **4,242.9p, HOLD by 3.5p**. Only the whole-consideration discount at WACC (-57.2p) gives SELL alone. I did not edit the Valuation agent's file.
3. **Foods timing method.** The cash-at-Kd test is the cleaner one. The share part is priced at market, and the missed dividends are already deducted, so discounting it again at WACC partly double-counts. The -57.2p is therefore an upper bound.
4. **Deal-fails growth.** I set FY26 to +0.5% (Group incl. Foods) in the deal-fails scratch briefs (base and bear). Using the PM's +2.0% HPC figure there would mix perimeters. The test still flatters: FY27+ stays 1.6%, though the perimeter grew more slowly (2.7% vs 3.5% USG in FY25).
5. **Still open from the 14 Oct run** (FLAGs 2-8 below): the engine bear's JV, terminal growth and roll-forward inconsistencies; scratch use of the `restructuring_cash` line for the tax and HUL; HUL share count from Yahoo; McCormick volatility from Yahoo; the aggregator risk-free rate.
6. **The ERP sources are all secondhand** (erp-evidence.md): Kroll 5.0%, Fernandez 5.5% and Damodaran 4.2% alike. The stress lines inherit that.

### Missing (stated, not estimated)
Unchanged from 14 Oct, except that the McCormick dividends are now sized (deducted in inputs.yaml):
- tax on the Foods sale;
- the termination-fee trigger circumstances;
- Foods perimeter cash flows to closing;
- the remaining company's ROIC;
- an independent forward HPC growth forecast;
- HUL's share count from a filing;
- numeric USG guidance for FY21 and FY23;
- the full-year FY26 HPC euro growth (only H1 +2.0% is known).

### Confidence (re-run)
**High on the mechanics.** The control matches the Valuation run exactly, and all three HOLD->SELL breakevens land on the line by engine re-run.

**High that the HOLD is fragile.** 15 of the 16 single downside tests turn it into SELL on their own; only the Foods cash discounted at Kd leaves it HOLD.

**Medium on the size of the bear.** The tax rate, the McCormick move and the 16.2% margin are labelled stresses.

---

**Everything below is the 14 Oct 2026 bear run (base 3,855p SELL, ERP 5.0%): SUPERSEDED 15 Oct 2026.** It is kept for the audit trail. The method notes still apply; the numbers and ratings do not.

## SUPERSEDED (14 Oct 2026): re-run on PM decision 11 inputs

Money in EUR m unless labelled; values per share in pence (GBp); McCormick price in USD. Price 4,710.5p.
Current base **3,855p** (SELL, -18.2%); engine bear **3,212p**. Risk-free 3.45%, Ke 7.872%, WACC 7.10%, associates 7,061.8 (PM decision 11).

## What I did
1. Read CLAUDE.md, briefs/ULVR.yaml, docs/phase5/brief-unilever.md and the ULVR evidence packs, and every agent folder in this run.
2. `run_bear.py` copies the CURRENT brief and `inputs.yaml` into `scratch/<test>/` for each test. It makes one change, runs `python -m desk.valuation_run` (the Valuation agent's command), and reads the value per share back from that run's `valuation.json`.
   - `scratch/00_control` reproduces the Valuation agent's 3,855.3p and 3,211.9p exactly. The script asserts this against `valuation/valuation.json`.
   - The script also asserts that `associates` = the JV Gordon value at the current Ke (3,709.6) + 3,352.3.
   - Wherever the cost of equity or growth moves, the JVs are re-valued at 229 x (1 + g) / (Ke - g).
   - Results are in `bear_results.json`. Re-run from the repo root: `PYTHONPATH=. python runs/ULVR/2026-10-14/bear/run_bear.py`.
3. **Re-run 14 Oct 2026 after PM decision 11.** The scratch copies were deleted and rebuilt from the current inputs, and every test was re-run. The risk tests now check the Valuation agent's new flip points: beta 0.748, margin 19.7% and MKC USD 66.55. All three land on the HOLD boundary (4,238-4,242p against 4,239p), which confirms the scratch method.
4. New sources:
   - McCormick termination fee **USD 420m**: McCormick 10-Q to 31 Aug 2026 (0000063754-26-000329), note 2, from SEC EDGAR.
   - Guidance history: FY17-FY25 annual results 6-Ks, from SEC EDGAR.
   - One year of MKC daily closes from Yahoo (non-filing source), saved as `scratch/mkc_1y_yahoo.csv`. Volatility 30.5% via `desk.risk.annualised_volatility`.
5. Wrote `challenges.md` (five challenges, the stacked bear, the risks to the SELL, the track record and the final line) and this file. Nothing outside `bear/` was changed.

## Results (SUPERSEDED 15 Oct 2026; each a separate engine run; impact vs base 3,855p unless stated)
| Test | Value | Impact | Rating |
|---|---|---|---|
| 1. Deal fails, Foods in the DCF (no fee; no EUR 500m stranded-cost restructuring) | 3,877p | **+22p** | SELL |
| 1b. ... with the USD 420m fee / 1c. ... EUR 500m still spent | 3,892p / 3,857p | +37p / +1p | SELL |
| 2. Tax 25% of the cash (EUR 3,507m), priced today | 3,718p | **-138p** | SELL |
| 3. HUL at 38.1% of market + other minorities at book | 3,632p | **-224p** | SELL |
| 3b. HUL at market + others proportionate | 3,555p | -301p | SELL |
| 4. Margin 16.2% | 3,566p | **-290p** | SELL |
| 5. Engine bear with the JVs at Ke + 1 pt (vs 3,212p) | 3,191p | **-21p** | SELL |
| Terminal growth 1.1% (JVs at 1.1%) | 3,690p | -166p | SELL |
| Consistent bear: terminal growth 0.2% (vs 3,191p) | 2,934p | -257p | SELL |
| RONIC 16.5% / RONIC = WACC | 3,835p / 3,473p | -20p / -383p | SELL |
| Beta 0.9998 (Damodaran 2020-24 average), JVs consistent | 3,588p | -267p | SELL |
| McCormick 1 s.d. lower at closing (USD 33.15) | 3,654p | -201p | SELL |
| Stack: engine bear + JV fix + 16.2% + tax | 2,817p | -1,038p | SELL |
| Stack + HUL at market | 2,437p | -1,419p | SELL |
| Risk to SELL: beta 0.54 | 5,027p | +1,172p | **HOLD** |
| Risk to SELL: beta 0.748 / margin 19.7% / MKC USD 66.55 (flip points) | 4,238p / 4,242p / 4,239p | +383p to +386p | HOLD boundary |
| Risk to SELL: margin 18.8% / 18.2% | 4,068p / 3,952p | +213p / +97p | SELL |
| Risk to SELL: MKC USD 57.84 | 4,087p | +231p | SELL |

## What changed vs the first bear run (risk-free 3.18%) (SUPERSEDED 15 Oct 2026)
- The base fell 163p, from 4,018p to 3,855p, and the SELL moved from 222p to **384p** from HOLD.
- Margin 18.8% and MKC USD 57.84 were HOLD and are now SELL. Only beta 0.54 still gives HOLD (5,027p).
- The deal-fails test fell from +82p to +22p. At the higher discount rate, Foods inside Unilever is worth almost exactly the McCormick consideration.
- The bear impacts are broadly unchanged: tax -138p (it is priced today, so the discount rate does not affect it), HUL -224p (was -205p), margin -290p (was -303p).

## FLAGs
1. **The deal failing is roughly neutral to slightly positive (+1p to +37p).** The brief's "deal fails" bear line does not lower the value on our numbers. Growth was left at 1.6% for the whole group, which flatters the case a little (the perimeter's FY25 USG was 2.7% vs the Group's 3.5%). The 18.85% margin is unrounded; the PM rounded the equivalent 17.68% to 17.7%.
2. **The engine's bear scenario is inconsistent (for the PM; a possible desk/ change on a branch):**
   - (a) the JVs are not re-valued at the higher Ke (-21p);
   - (b) terminal growth stays at 1.6% while the bear forecasts 0.2% (-257p if aligned);
   - (c) the bear's roll-forward still uses the base Ke. Not sized.
3. **Scratch use of a bridge line.** The engine has no "tax on disposal" field, and the brief has no contingent-liabilities field. The 25% tax, and in test 3b and the stack the HUL market value, were therefore carried on the debt-like `restructuring_cash` line and netted in `priced_at_valuation_date_meur`. Mechanically this is the same as a separate line, and it is used only in the scratch copies.
4. **HUL at market (test 3)** sets the scratch brief to `minorities_method: book` with 15,507 + 488 = 15,995. The HUL share count is from Yahoo (non-filing). Others at book follows the minorities evidence pack.
5. **RONIC and Foods goodwill.** Removing Foods' goodwill gives a LOW bound of 16.5% for the remaining ROIC, so this challenge is weak. The ex-perimeter ROIC is MISSING. RONIC = WACC is an extreme case, not an estimate.
6. **Restructuring definition.** The FY21 6-K's "around EUR 1.4bn" of 2022 restructuring "investment" may not match the 20-F XBRL charge (777 in FY22), so I do not grade FY22. The "around 1% thereafter" guide against FY23-25 is a like-for-like comparison.
7. **McCormick volatility** comes from Yahoo prices. The 1 s.d. move is a labelled stress, not a forecast.
8. **Risk-free source.** The 3.45% comes from a data aggregator, not a primary source (Valuation notes FLAG 3). The bear figures inherit that.

## Missing (stated, not estimated)
- Tax and separation costs on the Foods sale (only the 25% stress is used).
- The termination-fee trigger circumstances (the merger agreement was not read).
- Foods perimeter cash flows to closing (the indicator of about +113p is not used in any test).
- The remaining company's ROIC.
- An independent forward HPC growth forecast.
- HUL's share count from a filing.
- Numeric USG guidance for FY21 and FY23.

## Disagreements with the brief (for the PM; nothing changed)
- Decision 1's bear line "deal fails" is neutral to slightly positive on our numbers (FLAG 1).
- The engine's bear should move terminal growth and the JV value with its forecast growth and WACC (FLAG 2).
- Decision 4: HUL at market (-224p to -301p) is as large as the margin bear and deserves the main memo, not a footnote.

## Confidence
**High on the mechanics.** Every impact is a full engine run, the control matches the current valuation exactly, and three flip-point tests land on the HOLD boundary.

**Medium on the size of the bear.** The tax rate, the McCormick move and the 16.2% margin are labelled stresses. The direction is clear: every sourced bear test stays SELL, and only Unilever's own low weekly beta (0.54) reaches HOLD.
