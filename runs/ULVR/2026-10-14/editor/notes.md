# Editor agent notes: Unilever PLC (ULVR), run 2026-10-14

## Update 15 Oct 2026: memo rewritten after the evidence audit (final 4,258.5p HOLD, borderline)

### What I did
- Read CLAUDE.md, briefs/ULVR.yaml, docs/audit-2026-10-15/ULVR.md, summary.md and bear-responses-2026-10-15.md (U1-U6), and the new top sections of valuation/notes.md, valuation.json, sanity_checks.json, comps.json, bear/notes.md, bear/challenges.md and bear_results.json. Nothing outside editor/ was changed. Nothing was committed.
- **Rewrote memo.md** with the final numbers. The rating strip shows HOLD from valuation.json; there is no override. The line under it reads "Desk rating: HOLD, borderline (PM confirmed 15 Oct 2026 after evidence audit; was SELL)". Fair value 4,258.5p, price 4,710.5p (13 Oct 2026 close), upside -9.6%, engine bear 3,475.6p.
- **The summary says plainly that the call leans SELL.** HOLD is 19.1p (about EUR 486m) above the SELL line of 4,239.45p. Each of these alone makes it SELL:
  - each of the five bear challenges;
  - Kroll's 5.0% ERP (3,854.1p);
  - the 9 Oct Bund of 3.50% (4,222.4p);
  - a 1.0% spread (4,231.8p).

  Damodaran's January 4.23% keeps HOLD (4,241.6p). The summary also states that the PM kept the desk rule rather than override to SELL, so all four companies are rated by the same rule.
- **New tables:** the step table from 3,855.3p to 4,258.5p (sanity_checks.json `step_table_old_to_final`); breakevens (ERP 4.234%, Bund 3.476%, FY26 +1.51%, terminal growth 1.560%, MKC USD 43.55, margin 17.61%, beta 0.892, Foods tax about EUR 0.49bn); and the bear table, whose response column is "PM decision 15 Oct 2026". That column records U1-U6: keep each method, withdraw each "stays SELL" conclusion, and treat each challenge as a rating risk.
- **Disclosures paragraph:**
  - the ERP was seen only in search summaries (PM to confirm on Damodaran's site);
  - the Bund 3.45% comes from aggregators only;
  - the 0.70% spread is a USD index added to a EUR yield;
  - terminal value is 77.9% of EV;
  - comps say SELL (3,902p) while the DCF says HOLD;
  - Foods tax and Foods interim cash flows are MISSING;
  - McCormick dividends are taken for 3 quarters (2 quarters gives 4,267.0p);
  - FY26 +2.0% is an H1 figure;
  - Foods timing is not in the base: -15.7p (cash at Kd) still gives HOLD, -57.2p (whole at WACC) gives SELL.
- **Football (`unit: GBp`):**
  - markers: share price 4,710.5 (first), DCF 4,258.5;
  - WACC 6.00-7.00%: 3,917-4,678; terminal growth 1.1-2.6%: 4,053-4,825 (valuation.json grid);
  - ERP 5.5% to 5.0%: 3,642.4-3,854.1;
  - single bear changes: 3,932.2-4,235.0 (margin 16.2% to RONIC 16.5%; excludes the labelled extreme RONIC = WACC, 3,747.3);
  - upside risks: 4,367.3-4,497.9 (margin 18.2% to margin 18.8%; covers deal fails and MKC USD 57.84);
  - own beta 0.54: 5,486.2;
  - engine bear 3,475.6;
  - stacked bear 2,694.9-3,051.0;
  - comps 3,152-6,552.
- **Sensitivity grid:** valuation.json, WACC 6.00-7.00% x g 1.1-2.6%, rounded to whole pence except the base cell. To fit two pages I dropped the 5.50% and 7.50% rows; they are in valuation.json (3,504p to 6,273p).
- **memo_check:** "All memo numbers trace to agent outputs."
- **PDF:** rebuilt with desk/memo_pdf.py. It is 2 pages plus a Sources page; I rendered it to PNG and checked it. The step table breaks across pages 1 and 2. To fit, I shortened the fundamentals and risks bullets (merged ROIC and mix; merged volatility and drawdown).

### FLAGs
1. **Borderline.** The rating rests on two inputs not confirmed at the primary source: the ERP (4.2%, search summaries) and the Bund (3.45%, aggregators). Each one alone decides HOLD vs SELL within about 3 basis points.
2. **valuation/notes.md says the -16p Foods cash discount "would make it SELL".** The Bear agent's engine re-run gives 4,242.9p, which is HOLD by 3.5p. The memo uses the engine figure (bear/notes.md FLAG 2). I did not edit the Valuation agent's file.
3. **The bear engine scenario still keeps the JV at the base Ke.** The memo shows both 3,475.6p and the JV-fixed 3,449.2p.
4. **risk/notes.md** still shows a cost of equity at ERP 5.0% (7.872%). The memo takes Ke 7.164% from valuation.json.
5. **memo_check matches numbers anywhere in the run folder** (including superseded scratch files). I checked the key figures by hand against valuation.json, sanity_checks.json, valuation/notes.md and bear/challenges.md.

### Missing (upstream, shown as such)
- Foods tax
- Foods interim cash flows to closing
- primary-source ERP and Bund
- a euro single-A spread
- full-year FY26 HPC growth
- ex-Foods ROIC
- peer NTM EBITDA

### Confidence
High that the memo matches the final agent outputs. The rating itself is low-conviction: HOLD by 19.1p, leaning SELL.

---

**Everything below is the 14 Oct 2026 editor run (3,855p SELL): superseded 15 Oct 2026.**

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

## 16 Oct 2026: ERP confirmed at source

- Damodaran's implied ERP of 4.20% (1 Oct 2026) was read directly on his home page and in ERPbymonth.xlsx once the PM allowed pages.stern.nyu.edu (docs/audit-2026-10-15/erp-evidence.md, section 0). Memo wording changed from "seen only in search summaries / PM to confirm" to "confirmed at source"; no number, value or rating changed; memo.pdf rebuilt. The earlier FLAGs about the ERP being unconfirmed are closed.
