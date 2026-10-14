# Bear case agent notes: Unilever PLC (ULVR), run 2026-10-14

Money in EUR m unless labelled; values per share in pence (GBp); McCormick price in USD. Price 4,710.5p. Base 4,018p (SELL, -14.7%); engine bear 3,323p.

## What I did
1. Read CLAUDE.md, briefs/ULVR.yaml, docs/phase5/brief-unilever.md and the ULVR evidence packs (growth, margin, minorities, tax, stake/tax check, run flags), and every agent folder in this run (data, fundamentals, risk, valuation).
2. Wrote `run_bear.py`. For each test it copies the brief and `inputs.yaml` into `scratch/<test>/`, makes one change, and runs `python -m desk.valuation_run` (the Valuation agent's command). It then reads the value per share from that run's `valuation.json`. An unchanged copy (`scratch/00_control`) reproduces 4,017.8p and 3,323.2p exactly (the script asserts this). Results: `bear_results.json`. Re-run: `PYTHONPATH=. python runs/ULVR/2026-10-14/bear/run_bear.py` from the repo root.
3. Sourced two new facts. (a) The McCormick termination fee of **USD 420m**, McCormick 10-Q to 31 Aug 2026 (0000063754-26-000329), note 2 "Pending Merger", fetched from SEC EDGAR 14 Oct 2026. (b) Management's guidance history, from the FY17-FY25 annual results 6-Ks, fetched from SEC EDGAR (accessions in challenges.md).
4. Saved one year of MKC daily closes (Yahoo chart API, 14 Oct 2025 to 13 Oct 2026; **non-filing source**) as `scratch/mkc_1y_yahoo.csv`. Volatility comes from `desk.risk.annualised_volatility`: 30.5%.
5. Wrote `challenges.md`: five challenges, the stacked bear, the risks to the SELL, the track record, and the final line. Nothing outside `bear/` was changed.

## Results (each is a separate engine run; impact vs base 4,018p unless stated)
| Test | Value | Impact | Rating |
|---|---|---|---|
| 1. Deal fails, Foods in the DCF (no fee; no EUR 500m stranded-cost restructuring) | 4,100p | **+82p** | SELL |
| 1b. ... with the USD 420m fee / 1c. ... EUR 500m still spent | 4,115p / 4,080p | +97p / +62p | SELL |
| 2. Tax 25% of the cash (EUR 3,507m), priced today | 3,880p | **-138p** | SELL |
| 3. HUL at 38.1% of market + other minorities at book | 3,813p | **-205p** | SELL |
| 3b. HUL at market + others proportionate | 3,731p | -287p | SELL |
| 4. Margin 16.2% | 3,715p | **-303p** | SELL |
| 5. Engine bear with the JVs at Ke + 1 pt (vs 3,323p) | 3,300p | **-23p** | SELL |
| Terminal growth 1.1% (JVs at 1.1%) | 3,832p | -186p | SELL |
| Consistent bear: terminal growth 0.2% (vs 3,300p) | 3,017p | -283p | SELL |
| RONIC 16.5% / RONIC = WACC | 3,996p / 3,587p | -22p / -430p | SELL |
| Beta 0.9998 (Damodaran 2020-24 average), JVs consistent | 3,725p | -293p | SELL |
| McCormick 1 s.d. lower at closing (USD 33.15) | 3,816p | -201p | SELL |
| Stack: engine bear + JV fix + 16.2% + tax | 2,918p | -1,100p | SELL |
| Stack + HUL at market | 2,546p | -1,472p | SELL |
| Risk to SELL: beta 0.54 | 5,330p | +1,312p | **HOLD** |
| Risk to SELL: margin 18.8% / 18.2% | 4,240p / 4,119p | +222p / +101p | **HOLD** (boundary) / SELL |
| Risk to SELL: McCormick USD 57.84 | 4,249p | +231p | **HOLD** |

## FLAGs
1. **The deal failing raises the value (+62p to +97p).** On our numbers Foods is worth more inside Unilever than the McCormick consideration is worth at today's MKC price. The brief lists "deal fails" as a bear line; on this evidence it belongs with the risks to the SELL. Growth was left at 1.6% for the whole group. That flatters the case a little: the perimeter's FY25 USG was 2.7% vs the Group's 3.5%. The deal-fails margin of 18.85% (19.97% less the 1.12% restructuring average) is unrounded. The PM rounded the equivalent 17.68% to 17.7%.
2. **The engine's bear scenario is inconsistent in two ways (for the PM and a possible desk/ change on a branch).** (a) The JVs are not re-valued at the higher Ke (-23p; Valuation FLAG 4). (b) Terminal growth stays at 1.6% while the bear forecasts 0.2% (-283p if aligned). Minor: the bear roll-forward still uses the base Ke (`build` passes `w["cost_of_equity"]`, unshifted). Not sized.
3. **Scratch use of a bridge line.** The engine has no "tax on disposal" field, and in this brief it has no contingent-liabilities field either. So the 25% tax, and in test 3b and the stack the HUL market value, were carried on the debt-like `restructuring_cash` line, and were also netted in `priced_at_valuation_date_meur`. Mechanically this is identical to a separate line. It happens only in scratch copies.
4. **HUL at market (test 3)** switches the scratch brief to `minorities_method: book` with 15,507 + 488 = 15,995. The HUL share count is from Yahoo (Data agent: non-filing). Others at book (488) follows the minorities evidence pack.
5. **RONIC and Foods goodwill.** The caller's suggested challenge turns out weak. Removing Foods' goodwill from invested capital gives a LOW bound of 16.5% for the remaining ROIC, and removing more Foods capital raises it. The ex-perimeter ROIC is MISSING. RONIC = WACC is shown as an extreme, not as an estimate.
6. **Restructuring track record definition.** The FY21 6-K guided "around EUR 1.4bn" of restructuring "investment" for 2022. The 20-F XBRL `ExpenseOfRestructuringActivities` shows 777 for FY22. The two measures may differ (the investment may include items outside the P&L charge), so I do not call FY22 a beat or a miss. The comparison that matters, the "around 1% of turnover thereafter" guide against FY23-25, is like for like.
7. **McCormick volatility** is from Yahoo prices (not a filing). The 1 s.d. move is a labelled stress, not a forecast.
8. Beta 0.54 → 5,330p reproduces the Valuation agent's figure, and margin 18.8% and MKC USD 57.84 land at its flip points. This gives an independent check of the scratch method.

## Missing (stated, not estimated)
- Tax and separation costs on the Foods sale (only the 25% stress is used).
- The termination-fee trigger circumstances. The merger agreement is not read; the 10-Q says only "under specified circumstances".
- Foods perimeter cash flows from 1 Jan 2026 to closing (the Data agent's indicator, about +113p, is not used in any test).
- ROIC of the remaining company; an independent forward HPC market-growth forecast; HUL's share count from a filing.
- FY21 and FY23 numeric USG guidance. The FY20 6-K gives only the 3-5% framework, and the FY22 6-K says only "strong".

## Disagreements with the brief (for the PM; nothing changed)
- Decision 1's bear line, "deal fails", is upside on our numbers (FLAG 1).
- The engine's bear should move terminal growth and the JV value with its forecast growth and WACC (FLAG 2).
- Decision 4: I would show HUL at market in the memo as the main minorities risk, not a footnote. It costs 205-287p, about as much as the margin bear.

## Confidence
**High on the mechanics.** Every impact comes from a full engine run, the control matches the base exactly, and three risk tests reproduce the Valuation agent's flip points. **Medium on the size of the bear.** The tax rate, the McCormick move and the 16.2% margin are labelled stresses. The direction is clear: every sourced bear test stays SELL, and only beta 0.54 reaches HOLD with any room to spare. Margin 18.8% and McCormick at the USD 57.84 deal reference only reach the HOLD boundary.
