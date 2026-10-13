# Bear agent notes: Diageo (DGE), run 2026-10-12 (Phase 3 re-run, refreshed 2026-10-13 for proportionate minorities)

## What I did
- Refreshed after the PM decision of 2026-10-13 (minorities valued proportionately: 2.566% x EV = USD 1,500m, replacing book USD 2,083m). New base **1,544.8p GBp, HOLD (-7.7%)**; SELL line 1,505.7p, **39p headroom** (was 18p); engine bear scenario 1,108.2p.
- Fixed `run_challenges.py`: inputs are now loaded with `valuation_run.extra_required(brief)` (roll-forward input **and** `minority_share_of_operating_profit`) instead of the hard-coded roll-forward list, so the run STOPs if the minorities input is missing. The script also STOPs if its base does not reproduce `valuation/valuation.json` (it matches: 1,544.8p). Nothing hard-coded book minorities; the bridge follows the brief's `minorities_method`.
- Re-ran every challenge against the new base with `desk.valuation_run.build` (one change each, in-memory copies). Added a bisection solver (engine calls only) for the SELL flips: flow-through 33.6%, beta 0.997, terminal RONIC 11.66%, minorities USD 2,619m on a book basis; these match `valuation/sanity_checks.json`.
- **New challenge 6 (minorities method):** USL's outside stake at market (42.79% x 727.35m shares x INR 1,362.5 / 95.285 INR per USD, Yahoo 12 Oct 2026 = USD 4,450m) + other minorities at book USD 1,328m = USD 5,778m -> **1,395.3p GBp, -149.5p, SELL**. Old book method check: 1,524.4p (-20.4p, HOLD). Counter-argument written up (it mixes USL's market multiple with our DCF's valuation of the same profits; the 1,328 still contains EABL's 35%), so I present -150p as an upper bound.
- `briefs/DGE.yaml` and `inputs.yaml` not changed by me. (`briefs/DGE.yaml` shows an uncommitted one-line comment edit about the flow-through flip point that was already in the working tree; not mine.)

## FLAGs
1. **The HOLD is still fragile:** 9 of 11 single bear changes flip it to SELL. Flow-through 40% is no longer a SELL (1,525.8p); the flip is at **33.6%**, i.e. essentially Diageo's own 2017 "two thirds reinvested" rule (33% gives 1,503.6p, SELL by 2p).
2. **Beta is a knife-edge:** SELL at beta 0.997 vs 0.96 used; beta 1.00 gives 1,502.5p (SELL). The upside case, beta 0.72, gives 1,844.1p (+299p, HOLD) and remains the largest lever.
3. **Minorities are a method choice worth up to 150p** (USD 1,500m proportionate -> USD 5,778m with USL at market). The HOLD needs minorities below USD 2,619m. I accept the EABL double-count fix but note the proportionate method sits at the low end of the range.
4. The c.51x USL multiple in the counter-argument is the figure given with the PM's instruction; I did not verify it against USL's filings. USL share count and price are Yahoo Finance (12 Oct 2026), as given; 42.79% = 100% - 57.21% (inputs.yaml).
5. I still disagree with the brief's 46% flow-through and 13.4% RONIC as base-case inputs (both assume management delivers); I have not changed them.

## Missing
No sourced number for GLP-1 / moderation effects, Moet Hennessy fair value, the split of the USD 1,328m "other" minorities between EABL and the rest, or USL's net cash; these are listed as not quantified. IWSR evidence is secondhand.

## Confidence
High on the impacts (engine output; base reproduces valuation.json; flip thresholds match sanity_checks.json). Medium on the minorities challenge (upper bound, inconsistent-method caveat). Medium on terminal growth evidence (secondhand IWSR) and flow-through history (one item via search summary).
