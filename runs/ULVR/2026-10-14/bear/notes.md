# Bear case agent notes: Unilever PLC (ULVR), run 2026-10-14 (re-run on PM decision 11 inputs)

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

## Results (each a separate engine run; impact vs base 3,855p unless stated)
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

## What changed vs the first bear run (risk-free 3.18%)
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
