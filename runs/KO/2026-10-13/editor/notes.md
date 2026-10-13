# Editor agent notes: The Coca-Cola Company (KO), run 2026-10-13

## What I did
- Read CLAUDE.md, .claude/agents/editor.md, briefs/KO.yaml, docs/phase5/*.md and every agent output in this run (data, risk including the 18:10 update, fundamentals, valuation, bear). inputs.yaml / valuation.json treated as authoritative over data/notes.md, which predates the PM's CCBA, stakes and IRS decisions.
- Wrote memo.md in the layout of the Diageo Phase 4 memo (runs/DGE/2026-10-12/editor/memo.md). Header: "Desk rating: SELL (PM review pending)", fair value $47.60, price $90.12 (13 Oct 2026), upside -47.2%, bear $37.99. No PM override yet; "PM to respond" is used where her judgement is needed (bear margin, tax on stake gains, beta choice, PM view).
- Football field (USD per share): DCF WACC 7.5-8.5% $43.93-$51.94; terminal growth 1.5-3.0% $45.28-$53.63; single bear changes $40.01-$47.38; single generous changes $48.02-$59.24; all four generous $79.45; bear scenario $37.99; comps $42.01-$107.05; markers share price $90.12 (first), DCF $47.60.
- Numbers taken only from valuation/valuation.json, valuation/notes.md, sanity_checks.json, comps.json, bear/challenges.md, bear_runs.json, risk/risk.json, risk/notes.md, fundamentals/notes.md and commentary.md. The sensitivity grid is valuation.json rounded to cents.
- memo_check: "All memo numbers trace to agent outputs." (On the first pass it flagged 3.63, MarketScreener's CCBA revenue, which exists only in docs/phase5. I removed it from the body.)
- PDF: `python -m desk.memo_pdf runs/KO/2026-10-13/editor/memo.md` produced 2 pages plus a Sources page. The body is about 1,190 words; the brief asks for about 900, and the extra covers the IRS, CCBA and "too harsh" sections the lead asked for.

## FLAGs
1. **The desk code's chart is pence-only.** In `desk/memo_pdf.py` `football()`, the labels are hard-coded with a "p" suffix (f"{a:,.0f}p") and the axis ticks step by 250, so the KO chart prints "48p" for $47.60 and an axis from 0p to 250p. The memo has an italic note under the chart saying the values are USD. Fix needed in desk code (on a branch with a PR, with Amanda's approval): use the brief's price_currency for the suffix and scale the tick step to the range. I did not edit desk code.
   **Resolved (desk code, PR #5):** `football()` now takes a `unit: USD` line, prints dollars ($47.60) and scales the axis ticks to the range ($30 to $110 in steps of $10). The italic note was removed and memo.pdf regenerated; memo_check still passes.
2. A third marker (the HOLD line at $81.11) overlapped the share-price label, so I took it out. The HOLD line is stated in the text instead.
3. memo_check matches numbers anywhere in the run folder, so it cannot confirm context. I checked the key figures by hand against valuation.json, bear_runs.json and risk.json.
4. The CCBA figures still rest on a web-search reading of Coca-Cola HBC's announcement. The PM is asked to verify them (the memo says so).

## Missing
KO forward EPS (forward P/E leg), peer NTM EBITDA, CCEP data, KO leverage target, an independent industry growth forecast: all MISSING upstream and shown as such.

## Confidence
High that the memo matches the agent outputs. The rating is robust: no single change tested leaves SELL. Pending the PM's call.
