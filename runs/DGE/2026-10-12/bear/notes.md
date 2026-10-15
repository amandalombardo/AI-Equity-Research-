# Bear agent notes: Diageo (DGE), run 2026-10-12 (final re-run 15 Oct 2026 after the PM's bear responses)

## Final re-run 15 Oct 2026 (after the PM's bear-response decisions)
**What I did.** Re-ran `run_challenges.py` after the PM accepted the bear responses (15 Oct 2026, "Accept all", `docs/audit-2026-10-15/bear-responses-2026-10-15.md`): diluted shares 2,231m and debt weight 0.29311 (`inputs.yaml`), FY30-31 growth 2.0% (`briefs/DGE.yaml`). The base reproduces `valuation/valuation.json` exactly (1,772.1p GBp) and the engine bear scenario matches (1,293.5p GBp). Script change: only the run label and docstring. Recorded the PM's decisions D1-D5 in `challenges.md` ("PM decision 15 Oct 2026"). I did not edit the brief, `inputs.yaml` or `desk/`. Nothing committed.

| | Morning re-run (15 Oct) | **Final (15 Oct)** |
|---|---|---|
| Base / upside vs 1,673p / rating | 1,808.8p / +8.1% / HOLD | **1,772.1p / +5.9% / HOLD** |
| Headroom to SELL (1,505.7p) / gap to BUY (1,923.95p) | 303p / 115p | **266p / 152p** |
| Engine bear scenario | 1,298.3p SELL | **1,293.5p SELL (-22.7%)** |
| Single changes that flip to SELL | 0 | **1: ERP 5.5% (1,494.9p)** |
| ERP 5.0% Kroll / Kroll with 20-year / 5.5% Fernandez | 1,625.5p / 1,545.7p / 1,525.7p | **1,592.6p / 1,514.4p / 1,494.9p SELL** |
| SELL if ERP above / beta above | 5.61% / 1.282 | **5.44% / 1.244** |
| BUY if ERP below / beta below | 3.76% / 0.860 | **3.62% / 0.828** |
| Beta 0.72 (bull) | 2,107.2p BUY | **2,064.5p BUY (+23.4%)** |

### FLAGs (final)
1. **PM decision D1 (keep ERP 4.2%) was made on the basis that the rating is HOLD at every sourced ERP. After D3 and D4 that is no longer true:** the Fernandez 5.5% gives 1,494.9p (GBp), SELL, and Kroll's 5.0% with its 20-year pairing is only 9p above SELL (1,514.4p). I have recorded the decision as made; the PM may want to revisit the wording that supported it.
2. The 4.2% ERP is still seen only in search summaries (unconfirmed at Damodaran's site).
3. D2: the disposal proceeds stay gross, tax MISSING; the USD 300m in A2 is illustrative only.
4. Terminal value 76.3% of EV (Valuation FLAG).

### Missing (final)
Unchanged: Moet Hennessy fair value, GLP-1 / moderation volume effect, USL net cash, the split of the USD 1,328m other minorities, tax on the disposals, UK or global implied ERP.

### Confidence (final)
High on the impacts (engine output; base, bear and flip points match the Valuation agent's files). Medium-low on the ERP evidence (all secondhand). `python -m pytest` could not run (pytest not installed, no package index).

## Re-run 15 Oct 2026 morning (evidence audit) (SUPERSEDED by the final re-run above)
**What I did.** Re-ran `run_challenges.py` against the updated brief (ERP 4.2%) and `inputs.yaml` (2,224m shares, debt weight 0.29376), using only `desk.valuation_run.build`. The base reproduces `valuation/valuation.json` exactly (1,808.8p GBp) and the engine bear scenario matches (1,298.3p GBp). Script changes: (a) the flip solver now returns "none" when a rating line is not crossed in the tested range (before, it would have returned a meaningless end point, because flow-through and RONIC no longer flip); (b) added BUY-flip solves (beta, ERP) and SELL-flip solves for ERP, terminal growth and disposal tax; (c) added audit lines A1-A5 and stacked cases S1-S5; (d) each result now records its changes. I did not edit `briefs/DGE.yaml`, `inputs.yaml` or `desk/`. Nothing committed.

### Old vs new (pence per ordinary share, GBp)
| | 13 Oct (ERP 5.0%, 2,222m) | **15 Oct (ERP 4.2%, 2,224m)** |
|---|---|---|
| Base / upside vs 1,673p / rating | 1,627.3p / -2.7% / HOLD | **1,808.8p / +8.1% / HOLD** |
| WACC | 8.46% | **7.92%** |
| Headroom to SELL (1,505.7p) / gap to BUY (1,923.95p) | 122p / 297p | **303p / 115p** |
| Engine bear scenario | 1,179.9p SELL | **1,298.3p SELL (-22.4%)** |
| Single bear changes that flip to SELL | 3 of 11 | **0 of 11** |
| Zero organic growth FY27-31 | 1,490.7p SELL | 1,656.8p HOLD |
| Terminal RONIC = WACC | 1,468.3p SELL | 1,599.0p HOLD |
| USL minority at market (USD 5,778m) | 1,480.0p SELL | 1,666.8p HOLD |
| Flow-through 25% / 33% | 1,558.0p / 1,584.4p | 1,733.6p / 1,762.2p |
| Beta 1.00 / credit spread 2% / terminal growth 1.5% | 1,584.5p / 1,559.3p / 1,571.6p | 1,766.0p / 1,728.3p / 1,735.9p |
| Beta 0.72 (bull) | 1,929.6p BUY | **2,107.2p BUY (+26.0%)** |
| SELL if flow-through below / RONIC below / beta above | 9.1% / 9.26% / 1.078 | **none / none / 1.282** |
| SELL if ERP above / BUY if ERP below / BUY if beta below | 5.62% / 3.77% / 0.724 | **5.61% / 3.76% / 0.860** |

**Audit lines (one change each, vs 1,808.8p):** FY30-31 growth 2%: 1,778.8p (-30.0p); disposal proceeds net of an illustrative USD 300m tax: 1,798.3p (-10.5p; -3.5p per USD 100m; no tax amount flips it); diluted shares 2,231m: 1,803.1p (-5.7p); ERP 5.0% (Kroll): 1,625.5p (-183.3p); ERP 5.0% with Kroll's 20-year 5.60% risk-free: 1,545.7p (-263.1p); ERP 5.5% (Fernandez): 1,525.7p (-283.0p); terminal growth 1.5%: 1,735.9p (-72.8p). All HOLD.

**Stacks (one engine run each):** S1 audit's small sourced corrections (2,231m + Rf 5.24% + USD 300m tax): 1,787.5p HOLD. S5 business bear with ERP 4.2% (growth 2% FY30-31, tax 300m, 2,231m shares, g 1.5%, flow-through 33%, beta 1.00): 1,609.6p HOLD (-3.8% vs price). S2 audit bear lines with ERP 5.0%: 1,528.8p HOLD (23p above SELL). S4 = S2 + flow-through 33% + beta 1.00: **1,449.8p SELL**. S3 = S2 with ERP 5.5%: **1,439.4p SELL**.

**What flips the rating.** No single business challenge now reaches SELL. Single-input flips are discount-rate only: SELL if ERP > 5.61% or beta > 1.282; BUY if ERP < 3.76% or beta < 0.860 (beta 0.72, Diageo's own regression, gives BUY at 2,107.2p). SELL needs a stack that includes a higher ERP (S3) or a weaker business plus beta 1.00 (S4).

**PM's Phase 4 bear responses** (13 Oct, from `editor/memo.md`) are kept, unchanged, in the main table of `challenges.md`; they were written against the 13 Oct values.

### FLAGs (15 Oct)
1. **The re-run's whole gain is a discount-rate decision.** +183.5p (GBp) of the +181.5p comes from ERP 5.0% -> 4.2%, and the 4.2% was seen only in search summaries (`briefs/DGE.yaml` FLAG). Kroll's 5.0% (also secondhand) puts the value below the price (1,625.5p). The price implies an ERP of about 4.78%. I disagree with treating the 4.2% as settled before it is confirmed at the source; the brief is not mine to change.
2. **Kroll pairing.** If the desk ever reverts to 5.0% citing Kroll, Kroll pairs it with the 20-year yield (5.60%), which gives 1,545.7p, 40p above SELL. Cost of debt was left at 10-year + 1% in that test.
3. **The A2 tax amount (USD 300m) is illustrative.** No sourced tax on the EABL and RCB disposals exists; only the per-USD-100m sensitivity (-3.5p) is a firm number.
4. **A3 dilution:** I changed the share count only; the debt weight was left at 0.29376 (moving it would change the value by well under 1p, audit table A).
5. Terminal value is 76.7% of EV (Valuation FLAG): the lower ERP pushes more of the value into the years after FY31, which is where challenges 2 and 4 bite.

### Missing (15 Oct)
Unchanged: Moet Hennessy fair value, GLP-1 / moderation volume effect, USL net cash, the split of the USD 1,328m other minorities, tax on the disposals. New: no UK or global implied ERP checked (the benchmark is the FTSE 100); Damodaran's page not reached.

### Confidence (15 Oct)
High on the impacts (engine output; base and bear reproduce `valuation.json`; flip points match `valuation/notes.md`). Medium-low on the ERP evidence on both sides (Damodaran, Kroll and Fernandez figures are all secondhand). `python -m pytest` not run by me (no code in `desk/` changed; the Valuation agent reports pytest is not installed here).

---
**Everything below this line is superseded 15 Oct 2026 and kept for the record.**

## Phase 4 re-run (13 Oct 2026) (SUPERSEDED 15 Oct 2026: ERP 5.0%, 2,222m shares)
- Re-ran `run_challenges.py` after the PM switched to mid-year discounting. Base **1,627.3p GBp, HOLD (-2.7%)**, 122p above SELL; engine bear scenario 1,179.9p (SELL).
- **Only 3 of 11 single changes now flip to SELL**: terminal RONIC = WACC (1,468.3p), zero organic growth (1,490.7p), USL minority at market (1,480.0p, an upper bound). Flow-through 33% (1,584.4p) and 25% (1,558.0p), beta 1.00 (1,584.5p), credit spread 2% (1,559.3p), terminal growth 1.5% (1,571.6p) and RONIC 10.8% (1,561.8p) all stay HOLD.
- **New: the bull case reaches BUY.** Beta 0.72 gives 1,929.6p (+15.3%), 6p above the BUY line (1,923.95p); BUY if beta is below 0.724.
- FLAG (bear view): mid-year discounting is correct in principle (cash does arrive through the year), but it moved every value by 5% without any change in Diageo's prospects. The downside challenges that matter are now the structural ones: returns on new capital and no recovery.
- `briefs/DGE.yaml` and `inputs.yaml` not changed by me.


## Phase 3 notes (superseded values; also SUPERSEDED by the 15 Oct re-run)
### What I did
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
