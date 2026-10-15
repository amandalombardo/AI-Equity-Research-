# Editor agent notes: The Coca-Cola Company (KO), run 2026-10-13

## Update 15 Oct 2026 (re-run after the evidence audit)

### What changed
- Rewrote memo.md for the PM decisions after the evidence audit (docs/audit-2026-10-15/KO.md, summary.md): ERP 4.2% (Damodaran implied, 1 Oct 2026; was 5.0%, unsourced), listed stakes no longer grown in the roll-forward, bear margin 31.9% now used in the stacked bear.
- Header: "Desk rating: SELL (PM confirmed; re-run 15 Oct 2026 after evidence audit)". Fair value USD 50.76 (was USD 47.60), price USD 90.12 (13 Oct 2026), upside -43.7% (was -47.2%), bear case USD 38.25 (stacked bear from bear/challenges.md; not the engine's USD 39.91, not the old USD 37.99).
- Valuation: WACC 7.55% (cost of equity 7.78%), EV USD 214,201m, equity USD 214,613m at 31 Dec 2025 and USD 218,356m at 13 Oct 2026; TV 76.7% of EV (FLAG); exit 12.0x EBITDA (the 13 Oct FLAG for being below peers is cleared); DCF 27.6% below the comps median. The sensitivity grid is now WACC 6.55%-8.55% (base +/-1 point) from valuation.json, rounded to cents.
- Thesis: the market-implied WACC is 5.14% (valuation/notes.md). The old "about 5.5%" was the HOLD breakeven WACC; that figure is now 5.49%. The beta HOLD breakeven is now 0.068.
- Disclosures added: the ERP source was seen only in search summaries (PM to confirm on Damodaran's site); the 8th Circuit reversed the 3M Tax Court ruling on the same rule (1 Oct 2025), so the memo shows KO loses USD 50.76 / halfway USD 54.48 / KO wins USD 58.20, all SELL; TV 76.7% of EV; CCBA EUR 3,357m revenue / EUR 246m EBIT confirmed by two search readings of Coca-Cola HBC's own presentation, PDF not opened.
- Bear table: new values from bear/challenges.md, with the PM's 13 Oct responses kept (margin 31.9%, no stake tax, beta 0.6091). Added row 6 (ERP: Kroll 5.0% USD 47.01, Fernandez 5.5% USD 44.95). "PM to respond" on FY26 5.0% growth (audit finding 3, not decided) and on confirming the ERP source.
- Generous case: beta 0.35 USD 62.01, IRS win USD 58.20, g 3% USD 58.16, RONIC 31.4% USD 51.21, all four USD 84.19 = HOLD (-6.6%). Replaced the old line "every generous assumption stacked stays SELL" with: the three big generous assumptions together reach HOLD (USD 83.01 without RONIC); leaving any one out gives SELL (USD 66.78 to USD 75.75); none reaches BUY.
- Football chart (USD): WACC 7.05%-8.05% USD 46.50-55.85; g 1.5%-3.0% USD 47.96-58.16; single bear USD 43.10-50.53; single generous USD 51.21-62.01; all four generous USD 84.19; bear USD 38.25; comps USD 42.01-107.05; markers price USD 90.12, DCF USD 50.76.
- Fundamentals and risk sections are unchanged apart from the beta breakeven (those agents were not re-run). I dropped the "2.00x reported" leverage figure and the minorities/USD 0.26 caveat to keep the memo at two pages; both remain in the agent notes.
- Sources: added the Damodaran implied ERP (via erp-evidence.md), the 3M ruling (10-K tax litigation note) and the audit documents.

### Checks run
- `python -m desk.memo_check runs/KO/2026-10-13`: "All memo numbers trace to agent outputs." (first pass, nothing to fix).
- `python -m desk.memo_pdf runs/KO/2026-10-13/editor/memo.md`: memo.pdf is 3 pages, two of body and Sources alone on page 3. I checked the page breaks and the chart (USD labels) by eye. The body is about 1,265 words against the target of about 900; the audit disclosures account for the extra.
- Checked the key numbers by hand against valuation.json, valuation/notes.md, bear/challenges.md and bear_runs.json (memo_check only proves that a number appears somewhere in the run folder).

### FLAGs
1. ERP 4.2% seen only in search summaries: PM to confirm on Damodaran's site. The generous stack sits just USD 3.08 above HOLD and depends on it.
2. TV share 76.7% of EV, above the 75% limit.
3. CCBA figures sourced, not verified (PDF not opened from this environment).
4. Open audit items the PM has not decided (not in the base): FY26 growth 5.0% (-USD 0.51 on the new basis), CCBA 25% at USD 783m, margin denominator, 13 Oct risk-free print.
5. Fundamentals and risk outputs were not re-run. Their figures are unaffected by the ERP and the roll-forward, so they still stand.

### Confidence
High that the memo matches the 15 Oct agent outputs. SELL is robust to every single change; only the three-way generous stack reaches HOLD.

---

# Original notes, 13 Oct 2026 (kept for the record; figures superseded)

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
- **PM final 13 Oct 2026 18:29:** SELL. Bear responses: margin 31.9%, no stake-gain tax, beta 0.6091 kept. Memo updated and PDF regenerated.
