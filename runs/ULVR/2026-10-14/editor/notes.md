# Editor agent notes: Unilever PLC (ULVR), run 2026-10-14

## What I did
- Read CLAUDE.md, briefs/ULVR.yaml, docs/phase5/brief-unilever.md and every agent output in this run: data, risk, fundamentals, valuation, bear. The layout follows runs/KO/2026-10-13/editor/memo.md.
- **Rewrite after PM decision 11** (risk-free = Bund on the run date, 3.45%, from an aggregator). I rewrote memo.md from the current valuation/notes.md, valuation.json, sanity_checks.json, comps.json, bear/challenges.md and bear_results.json. I grepped the memo for the main numbers of the previous run, and none remain.
- **Header:** SELL from valuation.json, PM review pending, no override. Fair value 3,855p; price 4,710.5p (13 Oct 2026 close); upside -18.2%; engine bear 3,212p.
- **Thesis:** a firm SELL, 384p (8.2 points) from HOLD (4,239p). The only sourced input that reaches HOLD is the own 5y weekly beta 0.54 (5,027p). Margin 18.8% (4,068p) and McCormick at USD 57.84 (4,087p) stay SELL.
- **Sum of the parts:** explained in plain words. The EUR m bridge runs EV 91,140 to EUR 45.57 = 3,855p. The decomposition from valuation notes (d) is 3,393p + 1,334p + 290p - 1,161p.
- **MISSING:** tax on the Foods cash (39.3p per EUR 1bn; 25% stress 138p); Foods cash flows to closing (indicator about EUR 2.9bn, about 113p); no primary source for the run-date Bund yield.
- **Engine fixes, one line:** the buyback is deducted, and run-date prices are not grown (-86.5p on today's inputs).
- **Football (`unit: GBp`):** markers are the share price 4,710.5 (first) and the DCF 3,855. Bars:

  - WACC 6.60-7.60%: 3,583-4,182
  - Terminal growth 1.1-2.6%: 3,702-4,262
  - Single bear changes: 3,555-3,835 (HUL at market with others proportionate, to RONIC 16.5%). This excludes the labelled extreme RONIC = WACC (3,473) and "deal fails", which is roughly neutral.
  - Margin 18.8% / McCormick USD 57.84: 4,068-4,087
  - Own weekly beta 0.54: 5,027
  - Engine bear: 3,212
  - Stacked bear: 2,437-2,817
  - Comps: 3,166-6,541
- **Sensitivity grid:** valuation.json (WACC 6.10-8.10% x g 1.1-2.6%), rounded to whole pence.
- **Bear section:** all five challenges with "PM to respond". The PM view also reads "PM to respond".
- **memo_check:** "All memo numbers trace to agent outputs."
- **PDF:** 2 pages plus a Sources page. I rendered it to PNG and checked it: the chart is in pence and the share-price marker reads 4,710.5p (desk code now keeps half pence). To fit two pages I merged the HOLD flip points into the beta bullet and dropped the track-record sentence. The track record is still in bear/challenges.md.

## FLAGs
1. **The risk-free rate (3.45%) comes from an aggregator** (Trading Economics/Bloomberg page), not a primary source. The memo states this under MISSING and in Sources.
2. **risk/notes.md predates decision 11.** It still shows a cost of equity at the old Bund. The memo takes Ke 7.872% from valuation.json.
3. Dashed marker lines cross some bar labels in the chart. They are still readable.
4. memo_check matches numbers anywhere in the run folder, so it cannot confirm context. I checked the key figures by hand against valuation.json, valuation/notes.md and bear/challenges.md.

## Missing (upstream, shown as such)
- Tax on the Foods cash
- Foods perimeter cash flows to closing
- A primary-source run-date Bund yield
- McCormick dividends before closing
- Peer NTM EBITDA
- Ex-Foods ROIC
- An independent HPC growth forecast

## Confidence
High that the memo matches the current agent outputs. SELL, pending the PM's responses to the bear challenges.
