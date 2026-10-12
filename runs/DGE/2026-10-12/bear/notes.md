# Bear agent notes: Diageo (DGE), run 2026-10-12 (Phase 3 re-run)

## What I did
- Updated `run_challenges.py` for Phase 3: inputs loaded with `valuation_run.load_inputs(path, valuation_run.ROLL_FORWARD)` (brief uses `valuation_basis: balance_sheet_date`); the base reproduces the Valuation agent's 1,524.4p. Each challenge is one change to an in-memory copy; `briefs/DGE.yaml`, `inputs.yaml` and `desk/` are unchanged. Results in `challenges.json`; write-up in `challenges.md`.
- Challenged every agent: Valuation/PM (flow-through, terminal RONIC, credit spread), Fundamentals (no organic growth, track record), Data (terminal growth vs IWSR; restructuring tax relief as an upside), Risk (beta 1.00 and the 0.72 upside case).
- **Retired old challenge 6** (deducting the 30c final dividend): it goes ex on 15 Oct 2026, after the 12 Oct valuation date, so the price is cum-dividend.

## FLAGs
1. **The HOLD is fragile:** 9 of 11 single bear changes flip it to SELL (threshold 1,505.7p). Flow-through 40% gives 1,504.9p, a SELL by 0.8p, i.e. the flip point is almost exactly 40%.
2. **The RONIC rule changes the size of other challenges.** Terminal growth 1.5% now costs -55p (was -110p) because reinvestment falls with growth; zero organic growth now costs -135p (was -49p), which I attribute to the steady-state terminal year (explanation is my reading, the numbers are engine output).
3. **Beta remains the largest lever:** 0.72 gives 1,832p (+307p), bigger than any bear change.
4. I disagree with the brief's 46% flow-through and 13.4% RONIC as base-case inputs (both assume management delivers); I have not changed them.

## Missing
No sourced number for GLP-1 / moderation effects, Moet Hennessy fair value, or USL minority at market value; these are listed as not quantified. IWSR evidence is secondhand.

## Confidence
High on the impacts (engine output, base reproduces exactly). Medium on the evidence for terminal growth (secondhand IWSR) and flow-through history (one item via search summary).
