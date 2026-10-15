# Editor agent notes: Diageo (DGE), run 2026-10-12 (final re-run 15 Oct 2026 after the PM's bear responses)

## Final re-run 15 Oct 2026 (after the PM's bear-response decisions)
**What changed.** Rewrote memo.md after the PM accepted the bear responses (15 Oct 2026, "Accept all", docs/audit-2026-10-15/bear-responses-2026-10-15.md): diluted shares 2,231m (debt weight 0.29311) and FY30-31 growth 2.0% (was 3.0%). New numbers come only from the final outputs: valuation/valuation.json, sanity_checks.json, steps_2026-10-15.json, the top section of valuation/notes.md, bear/challenges.json, bear/challenges.md and bear/notes.md.
- Header: **HOLD | Fair value 1,772.1p (GBp) | Share price 1,673p (12 Oct 2026) | Upside +5.9% | Bear case 1,293.5p**, with "Desk rating: HOLD (PM confirmed; re-run 15 Oct 2026 after evidence audit)". SELL line 1,506p (266p below), BUY line 1,924p (152p above). Step line from 1,627.3p: ERP +183.5p, shares 2,224m -2.0p, 2,231m diluted -6.8p, growth -29.8p (valuation step table).
- Valuation: growth path 0.0/1.5/2.5/2.0/2.0%; WACC 7.92%, debt weight 29.311%; EV USD 65,441m, minorities USD 1,679m, equity USD 51,032m (30 June) / 52,323m (12 Oct), USD 23.45 per share, 2,231m diluted shares; terminal value 76.3% of EV; exit 10.0x vs c.9.78x; market-implied WACC 8.20% and ERP about 4.62%; DCF 23.3% below comps. Disposal proceeds labelled "gross, tax MISSING", 3.5p per USD 100m (PM decision D2). Sensitivity grid rebuilt from valuation.json (whole pence). Football chart rebuilt (unit GBp): WACC 1,603-1,973p, terminal growth 1,701-1,955p, ERP 5.5% to 5.0% 1,494.9-1,592.6p, single changes 1,567.1-2,064.5p, bear 1,293.5p, comps 1,334-3,163p (unchanged).
- Bear section: every "PM to respond" replaced with the PM's 15 Oct 2026 decisions: challenge 5 ERP (D1: keep 4.2% once confirmed at source; show the Kroll value), challenge 7 (D2 disclosure only; D3 diluted shares accepted), challenge 3 (D4 growth 2.0% accepted); the 13 Oct responses to challenges 1-6 confirmed (D5). Values updated to the final bear run. Removed the book-minorities what-if (1,758.1p) from the body to keep the memo at two pages; it is in valuation/notes.md.

**Checks run.** `python -m desk.memo_check runs/DGE/2026-10-12`: "All memo numbers trace to agent outputs." (pass). PDF rebuilt with `python -m desk.memo_pdf runs/DGE/2026-10-12/editor/memo.md`: 3 pages = 2 body pages + Sources page (page images checked; the sensitivity table is not split). Body is about 1,390 words (above the ~900 target, because of the audit disclosures). pytest could not run (not installed, no package index).

**FLAGs.**
1. **ERP: SELL now starts at 5.44%, so the Fernandez 5.5% gives a SELL (1,494.9p).** The PM's D1 decision (keep 4.2%) was recommended on the basis that the rating is HOLD at every sourced ERP; after D3-D4 that is true only for 4.2% and 5.0%. The memo states this plainly in challenge 5. The PM may want to revisit the D1 wording.
2. The 4.2% ERP is still seen only in search summaries; if Damodaran's page does not confirm it, the memo must be re-run before it is published.
3. Terminal value is 76.3% of EV (flag); the exit multiple (10.0x) is above the market's c.9.78x.
4. memo_check matches numbers anywhere in the run folder; I checked the key figures by hand against valuation.json, sanity_checks.json, steps_2026-10-15.json and bear/challenges.json.
5. The price (1,673p) is cum-dividend; any update after 15 Oct must use an ex-dividend price.

**Missing.** Peer EV/EBITDA and FCF yield, Constellation Brands EPS, calendarised peers, Moet Hennessy fair value, USL net cash, split of the USD 1,328m other minorities, tax on the disposals, UK or global implied ERP, Damodaran page not reached.

**Confidence.** High that the memo matches the agent outputs. Medium-low on the rating: HOLD at ERP 4.2% and 5.0%, SELL at 5.5%, and 4.2% is unconfirmed at source.

**History:** ... 1,627.3p HOLD (mid-year, 13 Oct) -> 1,808.8p HOLD (ERP 4.2%, 2,224m shares, 15 Oct morning) -> **1,772.1p HOLD (2,231m diluted shares, FY30-31 growth 2.0%, 15 Oct 2026 final)**.

## Re-run 15 Oct 2026 morning (evidence audit) (SUPERSEDED by the final re-run above)
**What changed.** Rewrote memo.md after the PM's decisions on the evidence audit (docs/audit-2026-10-15/DGE.md, summary.md): ERP 5.0% (no source) -> 4.2% (Damodaran implied ERP, 1 Oct 2026) and shares 2,222m -> 2,224m. New numbers come only from the re-run outputs: valuation/valuation.json, sanity_checks.json, comps.json, the top section of valuation/notes.md, bear/challenges.md, bear/notes.md and data/phase4_evidence.json.
- Header: **HOLD | Fair value 1,808.8p (GBp) | Share price 1,673p (12 Oct 2026) | Upside +8.1% | Bear case 1,298.3p**, with "Desk rating: HOLD (PM confirmed; re-run 15 Oct 2026 after evidence audit)". Was 1,627.3p, -2.7%. SELL line 1,506p (303p below), BUY line 1,924p (115p above).
- Valuation: WACC 7.92% (cost of equity 9.25%), EV USD 66,356m, minorities USD 1,703m, equity USD 51,923m (30 June) / 53,236m (12 Oct), USD 23.94 per share; sensitivity grid rebuilt from valuation.json (WACC 6.92-8.92%, whole pence). Football chart rebuilt (unit GBp): WACC range 1,636-2,014p, terminal growth 1,736-1,996p, new bar for ERP 5.5% to 5.0% (1,525.7-1,625.5p), single changes 1,599-2,107p, bear 1,298.3p, comps 1,334-3,163p.
- Audit disclosures added: ERP source and that it was seen only in search summaries (PM to confirm on Damodaran's site); Kroll 5.0% gives 1,625.5p (below the price); price implies ERP about 4.78% (valuation notes; the brief asked for "about 4.8%", I used the agent's 4.78% to avoid a new rounding) and WACC 8.30%; terminal value 76.7% of EV (above the 75% flag); price is the 12 Oct cum-dividend close, the 30c (about 22.6p) dividend went ex on 15 Oct; FX date (2 Oct) and risk-free date (8 Oct) now in the body; leverage "about 2.6x after disposals" now called a floor (before tax and still counting EABL's EBITDA); unsourced FY30-31 3% growth (2% = 1,778.8p); open MISSING list.
- Bear section: all challenges with the 15 Oct values; the PM's 13 Oct responses kept in substance (lightly shortened), labelled as written against the old values. "PM to respond" on the new ERP part of challenge 5 and on new challenge 7 (data inputs: gross proceeds, dilution). Added "What flips the rating" (discount rate only alone; stacks S3 1,439.4p and S4 1,449.8p reach SELL; business bear S5 1,609.6p HOLD).
- Removed the Phase 4 "PM view" paragraph: its year-end-convention value (1,545p) and market-implied WACC comparison were 13 Oct numbers with no 15 Oct equivalent for the year-end case.
- Sources: added FRED DGS20, the ERP sources (Damodaran, Kroll, Fernandez; secondhand) and the audit folder.

**Checks run.** `python -m desk.memo_check runs/DGE/2026-10-12`: "All memo numbers trace to agent outputs." PDF rebuilt with `python -m desk.memo_pdf runs/DGE/2026-10-12/editor/memo.md`: 3 pages = 2 body pages + Sources page (pypdf; page images checked; a sensitivity caption was added so the Fundamentals heading is not stranded at the foot of page 1). Body is about 1,260 words (above the ~900 target, because of the audit disclosures the PM asked for). pytest not run (no code changed; Valuation agent reports pytest is not installed here).

**FLAGs.**
1. The whole move from -2.7% to +8.1% is the ERP decision (+183.5p), on a figure seen only in search summaries. If Damodaran's page does not confirm 4.2%, the memo must be re-run before it is published.
2. The fair value is now nearer BUY (115p) than SELL (303p); beta 0.72 (own regression) gives BUY at 2,107p.
3. Terminal value is 76.7% of EV (flag) and the exit multiple (10.0x) is now above the market's c.9.75x.
4. The PM's bear responses were written on 13 Oct against the old values; challenges 2, 3 and 6 no longer flip to SELL, so the responses are stronger than needed, but she may want to reword them. ERP and data-input responses are "PM to respond".
5. memo_check matches numbers anywhere in the run folder; I checked the key figures by hand against valuation.json, sanity_checks.json and bear/challenges.md.
6. The price (1,673p) is cum-dividend; any update after 15 Oct must use an ex-dividend price and deduct the dividend in the roll-forward.

**Missing.** Peer EV/EBITDA and FCF yield, Constellation Brands EPS, calendarised peers, Moet Hennessy fair value, USL net cash, split of the USD 1,328m other minorities, tax on the disposals, UK or global implied ERP, Damodaran page not reached.

**Confidence.** High that the memo matches the agent outputs. Medium-low on the rating until the 4.2% ERP is confirmed at source.

**History:** ... 1,545p HOLD -> 1,627.3p HOLD (mid-year, 13 Oct) -> **1,808.8p HOLD (ERP 4.2%, 2,224m shares, 15 Oct 2026)**.

---
**Everything below is superseded 15 Oct 2026 (ERP 5.0%, 2,222m shares); kept for the record.**


## Phase 4 rewrite (13 Oct 2026): mid-year discounting, PM responses, new layout
- Rewrote memo.md after the PM's Phase 4 decisions: mid-year discounting (1,544.8p -> **1,627.3p, HOLD, -2.7%**) and the PM's responses to the six bear challenges (from docs/phase4/bear-responses-draft.md, source-checked in docs/phase4/evidence-phase4.md; numbers updated to the mid-year base). Every "PM to respond" is gone. Added a one-paragraph PM view. Removed internal file names from the body.
- New layout (desk/memo_pdf.py): rating strip (HOLD, fair value, price, upside, bear case), a valuation range chart (football field: DCF WACC range 1,481-1,798p, terminal growth range 1,572-1,767p, single changes 1,468-1,930p, bear 1,180p, comps 1,334-3,163p, with lines at the price and fair value), Sources on page 3 (not counted).
- New numbers come only from valuation/valuation.json, sanity_checks.json, notes.md, bear/challenges.json and data/phase4_evidence.json (first-half cash, breakeven inflation, credit spreads, leverage after disposals).
- memo_check: "All memo numbers trace to agent outputs." PDF: 2 pages + Sources page; body about 1,000 words (was 907; the brief asks for about 900, so I kept the extra words for the PM's responses).
- FLAG: the bull case now reaches BUY (beta 0.72: 1,930p, 6p above the BUY line). PM confirmed HOLD as her final rating on 13 Oct 2026 ("as long as it is backed by evidence and justifiable"); the PM view paragraph now gives the evidence (HOLD under both discounting conventions, market-implied WACC 8.3% vs 8.46%, BUY only via a beta with R-squared 0.15 and 95% range 0.51-0.93).

## Phase 3 notes (superseded values)
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


## Source check, 15 Oct 2026 (mistakes log row 33)
Memo updated for beta 0.9526 (was 0.9601): fair value 1,780.2p (was 1,772.1p), bear 1,298.8p, all bear-case values, sensitivity grid and flip points re-taken from valuation.json, steps_2026-10-15.json, sanity_checks.json and bear/challenges.json. memo_check passes. Rating unchanged: HOLD.
