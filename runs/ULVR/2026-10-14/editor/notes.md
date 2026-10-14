# Editor agent notes: Unilever PLC (ULVR), run 2026-10-14

## What I did
- Read CLAUDE.md, briefs/ULVR.yaml, docs/phase5/brief-unilever.md and every agent output in this run: data (notes.md), risk (notes.md, risk.json), fundamentals (notes.md, commentary.md), valuation (notes.md, valuation.json, sanity_checks.json, comps.json), bear (notes.md, challenges.md, bear_results.json). The layout follows runs/KO/2026-10-13/editor/memo.md.
- Wrote memo.md. Header: SELL (from valuation.json; no PM override), fair value 4,018p, price 4,710.5p (13 Oct 2026 close), upside -14.7%, engine bear 3,323p. The SELL is labelled moderate conviction: 222p from HOLD (4,239p). HOLD if beta 0.54 (5,330p), McCormick at USD 57.84 (4,249p) or margin 18.8% (4,240p).
- Sum of the parts explained in plain words, with the EUR m bridge and the pence decomposition from valuation/notes.md (d): 3,547p + 1,334p + 296p - 1,159p.
- MISSING items stated: tax on the Foods cash (39.3p per EUR 1bn; 25% stress 138p); Foods cash flows to closing (indicator about EUR 2.9bn, about 113p). The engine fixes are in one line: the buyback is deducted (mistakes row 22) and run-date prices are not grown (row 24, -84p). Both are recorded in data/notes.md and valuation/notes.md.
- Football field (pence, `unit: GBp`). Markers: share price 4,710.5 (first) and DCF 4,018. Bars:
  - DCF, WACC 6.34-7.34%: 3,720-4,378
  - DCF, terminal growth 1.1-2.6%: 3,845-4,483
  - Single bear changes: 3,715-3,996 (margin 16.2% to RONIC 16.5%). This excludes the labelled extreme RONIC = WACC (3,587) and "deal fails", which is upside.
  - Single changes reaching HOLD: 4,240-5,330
  - Engine bear: 3,323
  - Stacked bear: 2,546-2,918
  - Comps: 3,173-6,548
- Sensitivity grid = valuation.json, rounded to whole pence.
- Bear section: each of the five challenges in challenges.md, with "PM to respond" as the response. The PM view also reads "PM to respond".
- memo_check: "All memo numbers trace to agent outputs." (first pass and final pass).
- PDF: 2 pages plus a Sources page. I rendered it to PNG and checked it: the chart labels and axis are in pence. The body is about 1,140 words against the target of about 900. The extra covers the sum-of-the-parts table and the MISSING items the lead asked for.

## FLAGs
1. **The chart rounds the share price marker to "4,710p".** `desk/memo_pdf.py` `money_format` prints pence with no decimals, so 4,710.5p shows as 4,710p in the chart label. The memo text and header show 4,710.5p. This is display rounding in desk code. A fix (one decimal when the value is not whole) would go on a branch for Amanda's approval. I did not edit desk code.
2. The "3,720p to 4,378p" and "3,845p to 4,483p" bar labels are crossed by the dashed marker lines. They are still readable.
3. memo_check matches numbers anywhere in the run folder, so it cannot confirm context. I checked the key figures by hand against valuation.json, sanity_checks.json, bear_results.json and risk.json.

## Missing (upstream, shown as such)
Tax on the Foods cash; Foods perimeter cash flows to closing; McCormick dividends before closing; peer NTM EBITDA; ex-Foods ROIC; an independent HPC growth forecast.

## Confidence
High that the memo matches the agent outputs. The rating is SELL with moderate conviction, pending the PM's responses to the bear challenges.
