# Editor agent notes: Diageo (DGE), run 2026-10-12 (refreshed 2026-10-13 for proportionate minorities)

## What I did
- Rewrote memo.md after the PM decision of 2026-10-13 to value minority interests proportionately (2.566% share of operating profit ex-EABL x EV = USD 1,500m, replacing book USD 2,083m, which double counted EABL's 35% minority). Numbers taken only from valuation/valuation.json, valuation/notes.md, valuation/sanity_checks.json, valuation/bridge.json and bear/challenges.json, challenges.md, notes.md. Fundamentals and Risks sections are unchanged (their source files did not change), except beta 0.72 now gives 1,844p.
- Header: **HOLD | Fair value 1,544.8p | Share price 1,673p (12 Oct 2026) | Upside -7.7%.** Engine rating; no PM override.
- Headroom: SELL line 1,505.7p, 39p below fair value (was 18p). SELL-flip thresholds from sanity_checks.json: flow-through below 33.6%, terminal RONIC below 11.7%, beta above 0.997, WACC above 8.59%, minorities share above 4.48%. The old "flow-through flip at about 40%" is gone: 40% now gives 1,526p (HOLD).
- Valuation: new minorities bullet; bridge now deducts USD 1,500m (equity USD 44,219m at 30 June, 45,427m at 12 Oct, 1,545p); bear scenario 1,108.2p (-33.8%, SELL); market-implied WACC about 8.1%. Sensitivity table rebuilt from valuation.json, now with all four terminal growth columns in the grid (1.5% to 3.0%), rounded to whole pence as before. The step bridge is cut to the one new step (1,524p -> +20p) to keep two pages; the earlier steps are in bridge.json.
- Bear: all six challenges from bear/challenges.md, with refreshed values (zero growth now 1,414p, terminal growth 1.5% 1,491p, RONIC 10.8% 1,482p, credit spread 1,478p, beta 1.00 1,502p) and the new challenge 6, "USL minority at market" (USD 4,450m + other minorities at book USD 1,328m) = 1,395.3p (-150p, SELL), with the Bear agent's counter-argument (upper bound; prices USL's minority at market but Diageo's 57.21% at the DCF's 10.8x; USD 1,328m still includes EABL's 35%). "PM to respond" on every challenge.
- memo_check: "All memo numbers trace to agent outputs." PDF regenerated with `python -m desk.memo_pdf runs/DGE/2026-10-12/editor/memo.md` (reportlab); checked with pypdf: 2 pages including the Sources appendix. Body is 907 words.
- To fit two pages I shortened responses, the comps paragraph and the Sources lines (merged the last two; added 20-F p.164 and p.210 and Yahoo USL/INR data used for minorities).
- Did not change briefs/ or inputs.yaml. Not committed.

## FLAGs
1. The rating is still fragile: 9 of 11 single bear changes flip it to SELL. Flow-through 33% (Diageo's own 2017 rule) gives 1,504p, SELL by 2p.
2. Minorities are a method choice worth up to 150p; the HOLD needs minorities below USD 2,619m (book basis).
3. The c.51x USL multiple in the Bear counter-argument is unverified (Bear notes); I left that figure out of the memo.
4. The brief's comment "Rating flips to SELL at c.40%" is now out of date (Valuation agent); for the PM to edit.
5. memo_check matches numbers anywhere in the run folder, so it cannot confirm context. I checked the key figures by hand against valuation.json, sanity_checks.json, bridge.json and challenges.json.

## Missing
Peer EV/EBITDA, Constellation Brands EPS, Moet Hennessy fair value, split of the USD 1,328m other minorities (EABL vs rest), USL net cash.

## Confidence
High that the memo matches the agent outputs. Medium-low on the rating (39p headroom). Medium on the minorities figure.

## History
2,475p BUY (first run) -> 2,141p BUY (cost of debt fixed) -> 1,448p SELL (beta 0.96) -> 1,524p HOLD (Phase 3) -> 1,544.8p HOLD (proportionate minorities, 13 Oct 2026).
