# Bear case: Diageo (DGE), run 2026-10-12 (final re-run 15 Oct 2026 after the evidence audit and the PM's bear responses)

## Final re-run 15 Oct 2026 (after the PM's bear-response decisions)
**Base case: 1,772.1p (GBp; USD 23.45 per share), +5.9% vs 1,673p (GBp, 12 Oct 2026 close, cum-dividend), HOLD**, WACC 7.92%. What changed since the morning re-run (1,808.8p): the PM accepted the bear responses on 15 Oct 2026 (`docs/audit-2026-10-15/bear-responses-2026-10-15.md`, "Accept all"): **diluted shares 2,231m** (debt weight 0.29311) and **FY30-31 growth 2.0%** (was 3.0%). Both are now in the base, so audit lines A1 and A3 show zero impact. **SELL below 1,505.7p (GBp): 266p of headroom. BUY above 1,923.95p (GBp): 152p away.** The engine bear scenario (no growth, 25% flow-through, WACC +1 point) gives **1,293.5p (GBp), -22.7%, SELL**.

Method unchanged (`run_challenges.py` -> `challenges.json`): one change at a time to an in-memory copy, through `desk.valuation_run.build`; the script stops if its base does not reproduce `valuation/valuation.json` (it does: 1,772.1p). Stacks are one engine run each.

### PM decisions of 15 Oct 2026 on the open bear points (D1-D5 in the bear-responses file)
| # | Bear point | PM decision 15 Oct 2026 | Effect on the final base (GBp) |
|---|---|---|---|
| D1 | Challenge 5, ERP: the upside rests on a 4.2% ERP seen only secondhand | **Keep 4.2%** once confirmed on Damodaran's site; the memo keeps showing the Kroll 5.0% value so readers see the upside depends on the ERP. | 0. **FLAG:** the response's reason ("HOLD at every sourced ERP") no longer holds after D3-D4: ERP 5.5% (Fernandez) now gives 1,494.9p, **SELL**; SELL if ERP above 5.44%. Kroll 5.0% gives 1,592.6p (HOLD). |
| D2 | Challenge 7a, disposal proceeds gross, not net of tax | **Accept, disclosure only.** Label the input "gross, tax MISSING"; show -3.5p per USD 100m of tax; deduct nothing until Diageo discloses the tax. | 0 now; -3.5p per USD 100m (A2'); no amount up to the full USD 3,318m flips the rating |
| D3 | Challenge 7b, diluted shares | **Accept:** 2,231m diluted (2,224m + 7m dilutive, 20-F FY26). | -6.8p with the debt weight moved to 0.29311 (valuation step table) |
| D4 | Line A1, FY30-31 growth 3% unsourced | **Accept 2%** (= terminal growth) unless a source for 3% is found. | -29.8p (valuation step table) |
| D5 | 13 Oct responses to challenges 1-6, and to beta 0.72 | **Keep all of them.** | 0 |

### Every single change, final values (pence per ordinary share, GBp)
| # | Change | Morning value (15 Oct) | **Final value** | Impact vs 1,772.1p | Rating | PM response |
|---|---|---|---|---|---|---|
| 1 | Flow-through 40% | 1,787.3p | **1,750.7p** | -21.4p | HOLD | 13 Oct, kept (PM decision 15 Oct 2026, D5): 46% is the low end of FY27-29 profit guidance; we will check it against FY27 interim margins. |
| 1 | Flow-through 33% (2017 "two thirds reinvested") | 1,762.2p | **1,725.8p** | -46.4p | HOLD | (same) |
| 1 | Flow-through 25% (FY22-24 record) | 1,733.6p | **1,697.2p** | -74.9p | HOLD | (same) |
| 1 | Supply-chain savings phased 25/50/75/100% | 1,808.0p | **1,771.4p** | -0.8p | HOLD | immaterial |
| 2 | Terminal RONIC 10.8% (capex 7.08% of sales) | 1,735.9p | **1,700.8p** | -71.3p | HOLD | 13 Oct, kept (D5): 13.4% is Diageo's lowest ROIC in four years, not a recovery; FY26 capex (6.1% of sales) is close to the 6.21% the rule implies. |
| 2 | Terminal RONIC = WACC (7.92%; capex 8.69%) | 1,599.0p | **1,567.1p** | **-205.0p** | HOLD (-6.3%) | (same) |
| 3 | Zero organic growth FY27-31 | 1,656.8p | **1,650.6p** | -121.5p | HOLD (-1.3%) | 13 Oct, kept (D5): the path is already the low end of guidance; five years of zero growth is the bear scenario, not the base. |
| 3 | FY30-31 growth 2% (A1) | 1,778.8p | in the base | 0 | HOLD | **Accepted (PM decision 15 Oct 2026, D4)** |
| 4 | Terminal growth 1.5% | 1,735.9p | **1,700.9p** | -71.2p | HOLD | 13 Oct, kept (D5): with 2.35% breakeven inflation, 2% nominal already means a small real decline; the IWSR figures are secondhand. |
| 5 | Credit spread 2.0% | 1,728.3p | **1,693.6p** | -78.6p | HOLD | 13 Oct, kept (D5): our 1% spread is about the BBB average (1.02%, vs 0.69% for A-rated). |
| 5 | Beta 1.00 | 1,766.0p | **1,730.2p** | -41.9p | HOLD | (same) |
| 5 | ERP 5.0% (Kroll), 10-year risk-free (A4a) | 1,625.5p | **1,592.6p** | -179.5p | HOLD (-4.8%) | **PM decision 15 Oct 2026 (D1): keep 4.2% once confirmed at source; show the Kroll value in the memo.** |
| 5 | ERP 5.0% with Kroll's 20-year 5.60% (A4b) | 1,545.7p | **1,514.4p** | -257.7p | HOLD (-9.5%, 9p above SELL) | (D1) |
| 5 | ERP 5.5% (Fernandez survey) (A4c) | 1,525.7p | **1,494.9p** | **-277.3p** | **SELL** (-10.6%; was HOLD) | (D1) FLAG: see table above |
| 6 | USL minority at market + others at book (USD 5,778m) | 1,666.8p | **1,629.8p** | -142.3p | HOLD (-2.6%) | 13 Oct, kept (D5): an upper bound: USL's minority at market but Diageo's 57.21% at the DCF multiple, and the USD 1,328m still includes EABL's 35%. |
| check | Old book minorities (USD 2,083m) | 1,795.5p | 1,758.1p | -14.0p | HOLD | |
| 7a | Disposal proceeds net of an illustrative USD 300m tax (A2) | 1,798.3p | **1,761.7p** | -10.4p | HOLD | **Accepted as disclosure only (PM decision 15 Oct 2026, D2):** gross, tax MISSING; nothing deducted |
| 7a | Per USD 100m of tax (A2') | 1,805.3p | 1,768.7p | -3.5p | HOLD | (D2) |
| 7b | Diluted shares 2,231m (A3) | 1,803.1p | in the base | 0 | HOLD | **Accepted (PM decision 15 Oct 2026, D3)** |
| for | Beta 0.72 (own 5y weekly regression) | 2,107.2p | **2,064.5p** | +292.3p | **BUY** (+23.4%) | 13 Oct, kept (D5): R-squared 0.15 (95% range 0.51 to 0.93): too weak to override the industry beta. |
| for | Restructuring cash after tax relief (USD 850m -> 643m) | 1,816.0p | 1,779.3p | +7.2p | HOLD | Would add 7p; tax relief not confirmed. |

**One single change now flips the rating to SELL: ERP 5.5% (Fernandez).** No single business challenge does. Kroll's 5.0% with its own 20-year pairing is 9p above the SELL line.

**Rating flip points (engine bisection, one input at a time; match `valuation/sanity_checks.json` and `valuation/steps_2026-10-15.json`):**
| Input | Used | SELL if (morning) | **SELL if (final)** | **BUY if (final)** |
|---|---|---|---|---|
| ERP | 4.2% | above 5.61% | **above 5.44%** | **below 3.62%** |
| Beta | 0.96 | above 1.282 | **above 1.244** | **below 0.828** |
| Savings flow-through | 46% | none | **none (0% stays HOLD)** | |
| Terminal RONIC | 13.4% | none | **none down to the WACC** (RONIC = WACC gives 1,567.1p) | |
| Terminal growth | 2.0% | none | **none down to 0%** | |
| Minorities (book basis, USD m) | USD 1,679m proportionate | above USD 10,403m | **above USD 9,352m** | |
| Disposal tax (USD m) | 0 | none | **none, up to the full USD 3,318m** | |
The market price (1,673p GBp) implies an ERP of about 4.62% (`valuation/steps_2026-10-15.json`).

### Stacked bear cases (one engine run each, GBp)
| # | Changes together | Morning | **Final** | Impact | Rating |
|---|---|---|---|---|---|
| S1 | Risk-free 5.24% (9 Oct) + USD 300m disposal tax (diluted shares now in the base) | 1,787.5p | **1,756.6p** | -15.5p | HOLD (+5.0%) |
| S5 | Business bear, ERP 4.2%: USD 300m tax + terminal growth 1.5% + flow-through 33% + beta 1.00 (growth and shares now in the base) | 1,609.6p | **1,608.6p** | -163.5p | HOLD (-3.8%) |
| S2 | USD 300m tax + **ERP 5.0%** + terminal growth 1.5% | 1,528.8p | **1,527.8p** | -244.3p | HOLD (-8.7%, 22p above SELL) |
| S4 | S2 + flow-through 33% + beta 1.00 | 1,449.8p | **1,448.9p** | -323.3p | **SELL** (-13.4%) |
| S3 | S2 with **ERP 5.5%** | 1,439.4p | **1,438.4p** | -333.7p | **SELL** (-14.0%) |
| B | Engine bear scenario (no growth, 25% flow-through, WACC +1 point) | 1,298.3p | **1,293.5p** | -478.6p | **SELL** (-22.7%) |

## Challenges (claim, evidence, value impact; final 15 Oct values, GBp)
1. **Savings flow-through (Valuation agent / PM, 46%).** History says most savings are reinvested (2017 "two thirds reinvested"; FY23 GBP 450m of savings for +15bps of margin). 33% costs **-46.4p**, 25% **-74.9p**. Evidence below.
2. **Terminal returns (Valuation agent / PM, RONIC 13.4%).** ROIC 18.4% -> 13.4% over FY23-26. RONIC 10.8% costs **-71.3p**; RONIC = WACC **-205.0p**.
3. **No recovery (Fundamentals agent / brief growth path).** Both 2023-26 incentive targets missed. Zero growth costs **-121.5p**. The unsourced FY30-31 3% is now 2% in the base (PM accepted, D4).
4. **Terminal growth 2% vs falling spirits volumes (Data agent's industry check).** 1.5% costs **-71.2p**.
5. **Cost of capital (Risk agent beta; PM ERP and credit spread).** Still the main challenge. Kroll's 5.0% gives 1,592.6p (-179.5p), 4.8% below the price; Kroll's own pairing with the 20-year gives 1,514.4p (-257.7p); the survey 5.5% gives **1,494.9p (-277.3p), SELL**. Beta 1.00 costs -41.9p; a 2% spread -78.6p. Leverage is 3.14x vs a 2.5-3.0x target (20-F p.186).
6. **Minorities (Valuation agent / PM method).** USL at market costs **-142.3p** (upper bound; see counter-argument below).
7. **Data inputs (audit).** Diluted shares accepted into the base (D3); disposal proceeds stay gross, tax MISSING (-3.5p per USD 100m, D2).

## Re-run 15 Oct 2026 morning (evidence audit) (SUPERSEDED by the final re-run above: 2,224m basic shares, FY30-31 growth 3.0%; kept for the record)
**Base case: 1,808.8p (GBp; USD 23.94 per share), +8.1% vs 1,673p (GBp, 12 Oct 2026 close, cum-dividend), HOLD**, WACC 7.92%. What changed (PM decisions, `valuation/notes.md` top section): equity risk premium (ERP) 5.0% (no source) -> **4.2%** (Damodaran implied, seen secondhand) and shares 2,222m -> **2,224m**. Was 1,627.3p (GBp), -2.7%, HOLD. **SELL below 1,505.7p (GBp): 303p of headroom (was 122p). BUY above 1,923.95p (GBp): 115p away (was 297p).** The engine bear scenario (no growth, 25% flow-through, WACC +1 point) gives **1,298.3p (GBp), -22.4%, SELL** (was 1,179.9p).

Method unchanged: one change at a time to an in-memory copy of `briefs/DGE.yaml` or `inputs.yaml`, re-run through `desk.valuation_run.build` (`run_challenges.py`, results in `challenges.json`). The script stops if its base does not reproduce `valuation/valuation.json`: it does (1,808.8p). Stacks (S rows) are one engine run with several changes at once, not sums of single impacts.

### Every single change, old vs new (pence per ordinary share, GBp)
| # | Change | 13 Oct value (ERP 5.0%) | **15 Oct value** | Impact vs 1,808.8p | Rating | PM response (Phase 4, 13 Oct 2026) |
|---|---|---|---|---|---|---|
| 1 | Flow-through 40% | 1,607.5p | **1,787.3p** | -21.5p | HOLD | 46% is the low end of FY27-29 profit guidance; we will check it against FY27 interim margins. |
| 1 | Flow-through 33% (2017 "two thirds reinvested") | 1,584.4p | **1,762.2p** | -46.5p | HOLD | (same) |
| 1 | Flow-through 25% (FY22-24 record) | 1,558.0p | **1,733.6p** | -75.2p | HOLD | (same) |
| 1 | Supply-chain savings phased 25/50/75/100% | 1,626.5p | **1,808.0p** | -0.8p | HOLD | (not addressed; immaterial) |
| 2 | Terminal RONIC 10.8% (capex 7.07% of sales) | 1,561.8p | **1,735.9p** | -72.9p | HOLD | 13.4% is Diageo's lowest ROIC in four years, not a recovery; FY26 capex (6.1% of sales) is already close to the 6.21% the rule implies. |
| 2 | Terminal RONIC = WACC (7.92%; capex 8.68%) | 1,468.3p SELL | **1,599.0p** | **-209.7p** | **HOLD** (was SELL) | (same) |
| 3 | Zero organic growth FY27-31 | 1,490.7p SELL | **1,656.8p** | **-151.9p** | **HOLD** (was SELL) | The path is already the low end of guidance (0% in FY27); five years of zero growth means North America never recovers, which is the bear scenario, not the base. |
| 4 | Terminal growth 1.5% | 1,571.6p | **1,735.9p** | -72.8p | HOLD | With 2.35% breakeven inflation, 2% nominal already means a small real decline; the IWSR figures are secondhand. |
| 5 | Credit spread 2.0% (cost of debt 7.22%) | 1,559.3p | **1,728.3p** | -80.4p | HOLD | Our 1% spread is already about the BBB average (1.02%, vs 0.69% for A-rated) for an A-band company. |
| 5 | Beta 1.00 | 1,584.5p | **1,766.0p** | -42.8p | HOLD | (same) |
| 6 | USL minority at market + others at book (USD 5,778m) | 1,480.0p SELL | **1,666.8p** | **-142.0p** | **HOLD** (was SELL) | An upper bound: it prices USL's minority at market but Diageo's own 57.21% at the DCF multiple, and the USD 1,328m still includes EABL's 35%. |
| check | Old book minorities (USD 2,083m) | 1,609.1p | 1,795.5p | -13.2p | HOLD | |
| for | Beta 0.72 (own 5y weekly regression) | 1,929.6p BUY | **2,107.2p** | +298.5p | **BUY** (+26.0%) | R-squared 0.15 (95% range 0.51 to 0.93): too weak to override the industry beta. |
| for | Restructuring cash after tax relief (USD 850m -> 643m) | 1,634.5p | 1,816.0p | +7.2p | HOLD | Would add 7p; tax relief not confirmed. |

**No single business challenge now flips the rating to SELL** (on 13 Oct three did: RONIC = WACC, zero growth, USL at market). Every value rose by about 10-11% because of the lower discount rate, not because anything about Diageo changed. The PM's Phase 4 responses are kept as given; they were written against the 13 Oct numbers.

### New lines from the evidence audit (docs/audit-2026-10-15/DGE.md), one change each
| # | Change (agent challenged) | Evidence | **Value** | Impact | Rating |
|---|---|---|---|---|---|
| A1 | Organic growth FY30-31 2% instead of 3% (Fundamentals / brief) | Brief's 3% is unsourced ("industry long-run nominal growth"); the Data agent's own IWSR evidence (secondhand: spirits volumes about -2% by 2035) "challenges, rather than supports, the 3%" (audit finding 2) | **1,778.8p** | -30.0p | HOLD |
| A2 | Disposal proceeds net of an **illustrative** USD 300m of tax and costs (Data) | Brief asks for "net proceeds"; the input (USD 3,318.3m) is gross (20-F p.85; RCB press). No sourced tax figure exists, so USD 300m is illustrative | **1,798.3p** | -10.5p | HOLD |
| A2' | Per USD 100m of tax (sensitivity) | as above | 1,805.3p | -3.5p per USD 100m | HOLD; no amount of tax up to the full USD 3,318m flips it |
| A3 | Diluted shares 2,231m (Data) | 20-F FY26: 2,224m basic + 7m dilutive (audit finding 8). Debt weight left at 0.29376 | **1,803.1p** | -5.7p | HOLD |
| A4a | ERP 5.0% (Kroll recommended US ERP) with the 10-year risk-free 5.22% (Valuation / PM) | Kroll, reaffirmed 2026 (secondhand, erp-evidence.md 2b). This is the old desk figure, now with a source | **1,625.5p** | **-183.3p** | HOLD (-2.8%) |
| A4b | ERP 5.0% with **Kroll's own pairing**: 20-year Treasury 5.60% (Valuation / PM) | Kroll pairs 5.0% with the spot 20-year yield (FRED DGS20, 13 Oct 2026, via erp-evidence.md). Cost of debt kept at 6.22% (10-year + 1%) | **1,545.7p** | **-263.1p** | HOLD (-7.6%) |
| A4c | ERP 5.5% (Fernandez 2025 survey: US 5.5%, UK 5.4%) (Valuation / PM) | erp-evidence.md section 1 (secondhand); survey answers were given against lower risk-free rates (about 4.1%) | **1,525.7p** | **-283.0p** | HOLD (-8.8%, 20p above SELL) |
| A5 | Terminal growth 1.5% (Valuation / Data) | = challenge 4 | **1,735.9p** | -72.8p | HOLD |

**Rating flip points (engine bisection, one input at a time; matches `valuation/notes.md`):**
| Input | Used | SELL if (13 Oct) | **SELL if (15 Oct)** | **BUY if (15 Oct)** |
|---|---|---|---|---|
| ERP | 4.2% | above 5.62% | **above 5.61%** | **below 3.76%** |
| Beta | 0.96 | above 1.078 | **above 1.282** | **below 0.860** |
| Savings flow-through | 46% | below 9.1% | **none (0% stays HOLD)** | |
| Terminal RONIC | 13.4% | below 9.26% | **none (even RONIC = WACC 7.92% gives 1,599.0p)** | |
| Terminal growth | 2.0% | not solved | **none down to 0%** (the RONIC rule cuts reinvestment as growth falls) | |
| Minorities (book basis, USD m) | USD 1,703m proportionate | above USD 5,041m | **above USD 10,403m** (USL at market + others = USD 5,778m) | |
| Disposal tax (USD m) | 0 | not solved | **none, up to the full USD 3,318m** | |

The market price (1,673p GBp) implies an ERP of about 4.78% (valuation notes), which sits between Damodaran's 4.2% and Kroll's 5.0%.

### Stacked bear cases (one engine run each, GBp)
| # | Changes together | **Value** | Impact | Rating |
|---|---|---|---|---|
| S1 | Audit's sourced small corrections: diluted 2,231m + risk-free 5.24% (FRED DGS10, 9 Oct) + USD 300m disposal tax | **1,787.5p** | -21.3p | HOLD (+6.8%) |
| S5 | **Business bear, ERP kept at 4.2%:** FY30-31 growth 2% + USD 300m disposal tax + diluted 2,231m + terminal growth 1.5% + flow-through 33% + beta 1.00 | **1,609.6p** | -199.2p | HOLD (-3.8%) |
| S2 | Audit bear lines: A1 + A2 + A3 + **ERP 5.0%** + terminal growth 1.5% | **1,528.8p** | -280.0p | HOLD (-8.6%, 23p above SELL) |
| S4 | S2 + flow-through 33% + beta 1.00 | **1,449.8p** | -359.0p | **SELL** (-13.3%) |
| S3 | S2 with **ERP 5.5%** (Fernandez) | **1,439.4p** | -369.4p | **SELL** (-14.0%) |
| B | Engine bear scenario (brief 5b: no growth, 25% flow-through, WACC +1 point) | **1,298.3p** | -510.5p | **SELL** (-22.4%) (was 1,179.9p) |

**What flips the rating now.** Nothing on its own except a discount-rate move: ERP above 5.61% or beta above 1.28 (SELL); ERP below 3.76% or beta below 0.86 (BUY). Getting to SELL takes a stack: the audit's own bear lines plus the Fernandez ERP (S3), or plus Diageo's 2017 reinvestment rule and beta 1.00 (S4). Without an ERP change, even a broad business bear (S5) leaves the stock at 1,609.6p (GBp): still HOLD, but 3.8% **below** the price.

## Challenges (claim, evidence, value impact; 15 Oct morning values, SUPERSEDED)
1. **Savings flow-through (Valuation agent / PM, 46%).** History says most savings are reinvested (2017 "two thirds reinvested"; FY23 GBP 450m of savings for +15bps of margin). 33% costs **-46.5p (GBp)**, 25% **-75.2p**. Evidence below.
2. **Terminal returns (Valuation agent / PM, RONIC 13.4%).** ROIC 18.4% -> 13.4% over FY23-26. RONIC 10.8% costs **-72.9p**; RONIC = WACC **-209.7p**.
3. **No recovery (Fundamentals agent / brief growth path).** Both 2023-26 incentive targets missed. Zero growth costs **-151.9p**; just trimming the unsourced FY30-31 3% to 2% costs **-30.0p** (A1).
4. **Terminal growth 2% vs falling spirits volumes (Data agent's industry check).** 1.5% costs **-72.8p**.
5. **Cost of capital (Risk agent beta; PM ERP and credit spread).** This is now the main challenge. The +181.5p (GBp) of the re-run is a discount-rate decision, made on a figure seen only in search summaries. Kroll's 5.0% (also secondhand, but a named published figure) gives 1,625.5p (-183.3p), 2.8% below the price; Kroll's own pairing with the 20-year gives 1,545.7p (-263.1p); the survey 5.5% gives 1,525.7p (-283.0p). Beta 1.00 costs -42.8p; a 2% spread -80.4p. Leverage is 3.14x vs a 2.5-3.0x target (20-F p.186).
6. **Minorities (Valuation agent / PM method).** USL at market costs **-142.0p** (upper bound; see counter-argument below).
7. **Data inputs (audit).** Gross disposal proceeds (-3.5p per USD 100m of tax) and diluted shares (-5.7p): small, all one way.

## Phase 4 re-run, 13 Oct 2026 (SUPERSEDED 15 Oct 2026: ERP 5.0%, 2,222m shares; kept for the record)

**Base case: 1,627p (1,627.3p GBp; USD 21.54 per share), -2.7% vs 1,673p, HOLD** at a WACC of 8.46% (beta 0.96, terminal RONIC 13.4%, flow-through 46%, valued at 30 June 2026 with **mid-year discounting** (PM decision 13 Oct 2026; was end-of-year, 1,545p) and rolled forward to 12 Oct, restructuring cash USD 850m deducted, minorities proportionate: 2.566% x EV = USD 1,562m). **SELL starts at 1,506p (1,505.7p GBp), 122p below the base** (was 39p).
The engine's bear scenario (no organic growth, 25% flow-through, WACC +1 point) gives **1,180p GBp (-29.5%, SELL)**: three changes combined, shown for reference.

Method unchanged: one change at a time to an in-memory copy of the brief or `inputs.yaml`, re-run through `desk.valuation_run.build` (`run_challenges.py`, results in `challenges.json`; the script stops if its base does not reproduce `valuation/valuation.json`: it does, 1,627.3p). SELL-flip thresholds (engine bisection, matching `valuation/sanity_checks.json`): **flow-through below 9.1%, beta above 1.078, terminal RONIC below 9.26%, minorities above USD 5,041m (book basis) / share above 8.28%.**

### Results of every single change (GBp, vs 1,627.3p) (SUPERSEDED)
| # | Change | Value | Impact | Rating |
|---|---|---|---|---|
| 1 | Flow-through 40% | 1,607.5p | -19.8p | HOLD |
| 1 | Flow-through 33% (2017 "two thirds reinvested") | 1,584.4p | -42.9p | HOLD |
| 1 | Flow-through 25% (FY22-24 record) | 1,558.0p | -69.3p | HOLD |
| 1 | Supply-chain savings phased 25/50/75/100% | 1,626.5p | -0.8p | HOLD |
| 2 | Terminal RONIC 10.8% (capex 7.07% of sales) | 1,561.8p | -65.5p | HOLD |
| 2 | Terminal RONIC = WACC (capex 8.30%) | 1,468.3p | **-158.9p** | **SELL** |
| 3 | Zero organic growth FY27-31 | 1,490.7p | **-136.5p** | **SELL** |
| 4 | Terminal growth 1.5% | 1,571.6p | -55.7p | HOLD |
| 5 | Credit spread 2.0% | 1,559.3p | -68.0p | HOLD |
| 5 | Beta 1.00 | 1,584.5p | -42.7p | HOLD |
| 6 | USL minority at market + others at book (USD 5,778m) | 1,480.0p | **-147.3p** | **SELL** (upper bound) |
| check | Old book minorities (USD 2,083m) | 1,609.1p | -18.2p | HOLD |
| for | Beta 0.72 (own 5y weekly regression) | 1,929.6p | +302.3p | **BUY** (+15.3%, 6p above the 1,924p BUY line) |
| for | Restructuring cash after tax relief (850 -> 643) | 1,634.5p | +7.2p | HOLD |

**Three of the eleven single bear changes now flip the rating to SELL** (RONIC = WACC, zero growth, USL at market); before mid-year discounting it was nine. The evidence for each challenge is unchanged and kept below; only the values moved (every value rises by about 5% because all cash flows, including the terminal value, are discounted half a year less).


## Evidence for each challenge (unchanged from Phase 3; the values quoted inside are Phase 3 end-of-year values, SUPERSEDED by the 15 Oct table at the top)

## 1. Savings flow-through: the record says most savings get reinvested (challenges the Valuation agent / PM assumption, 46%)
**Claim:** 46% is the flow-through that delivers the *low end* of management's FY27-29 guidance; it assumes Diageo hits guidance. Its own history keeps far less.
**Evidence:** 20-F FY26 CEO letter: "We will invest this back to advance innovation, our overall competitiveness and to protect underlying profitability." FY17 results 6-K (27 Jul 2017): "two thirds being reinvested" (about 33% kept). 20-F FY23: GBP 450m of savings and only +15bps of margin (about 5% kept). Operating margin fell from 31.1% (FY22) to 28.9% (FY26) despite USD 1.7bn of productivity (FY24 annual report, via search summary). Source pack: `docs/phase3/savings-flow-through-evidence.md`.

| Flow-through | Value (GBp) | Impact (GBp) | Rating |
|---|---|---|---|
| 40% | 1,526p (1,525.8p) | -19p | HOLD (-8.8%) |
| 33.6% | 1,506p | -39p | **SELL line** (engine-solved) |
| 33% (2017 "two thirds reinvested" rule) | 1,504p (1,503.6p) | **-41p** | **SELL** (-10.1%, by 2p) |
| 25% (FY22-24 record, brief bear) | 1,478p | **-67p** | **SELL** (-11.6%) |

The flip point has moved from c.40% (book minorities) to **33.6%**: 40% is no longer a SELL. But 33.6% is almost exactly the 2017 rule Diageo itself announced, so the HOLD now needs Diageo to keep more of its savings than its own stated policy last time. Phasing is not the issue: slowing the supply-chain savings to 25/50/75/100% over FY27-30 costs only -1p (-0.7p, HOLD).

### 2. Terminal returns: ROIC has fallen 5 points in three years (challenges the Valuation agent / PM's terminal RONIC 13.4%)
**Claim:** the +65p terminal-capex step assumes new investment earns 13.4% forever, but ROIC has gone 18.4% (FY23) -> 15.8% -> 13.7% -> 13.4% (FY26) (20-F FY24-FY26 KPI tables, FY26 p.18), and the 5-year capex average (7.1% of sales) implies only 10.8%.
**Evidence:** `docs/phase3/terminal-capex-evidence.md`; capex/sales FY22-26 7.1%, 6.9%, 7.5%, 8.0%, 6.1% (20-F cash flow statements).

| Change | Terminal capex | Value (GBp) | Impact (GBp) | Rating |
|---|---|---|---|---|
| RONIC 11.66% (SELL line) | 6.75% of sales | 1,506p | -39p | SELL line (engine-solved) |
| RONIC 10.8% | 7.07% of sales | 1,482p | **-63p** | **SELL** (-11.4%) |
| (check: 5-year average 7.11% held forever) | 7.11% | 1,479p | -65p | SELL |
| RONIC = WACC (8.46%): growth creates no value | 8.30% | 1,392p | **-153p** | **SELL** (-16.8%) |

### 3. No recovery: management has missed its growth targets (challenges the Fundamentals agent and the brief's growth path)
**Claim:** the brief's path (0%, 1.5%, 2.5%, 3%, 3%) needs North America (USD 7,249m, -8.4% organic in FY26) to recover. Organic growth was 6.5% (FY23), -0.6%, 1.7%, -2.0% (FY26) (`fundamentals/commentary.md`, 20-F regional reviews pp.27-31). Moderation and GLP-1 use are a structural headwind in the US, though I have no sourced number for them (not quantified separately).
**Change:** zero organic growth FY27-31 -> **1,414p GBp, -131p, SELL (-15.5%).**

### 4. Terminal growth 2% vs a shrinking spirits market (challenges the Data agent's industry check)
**Claim:** IWSR: global spirits volumes fell 3% in 2025 and are seen down about 2% by 2035 (secondhand: Drinks International, Federvini; `data/notes.md`). 2% nominal forever needs price/mix to offset falling volume indefinitely.
**Change:** terminal growth 1.5% -> **1,491p GBp, -53p, SELL (-10.9%).** (The RONIC rule also cuts terminal reinvestment when growth falls: terminal capex 6.2% -> 5.5% of sales, which softens the hit.)

### 5. Cost of capital: leverage after the dividend cut, and an unstable beta (challenges the Risk agent and the PM's 1% credit spread)
**Claim:** leverage is 3.14x, above the 2.5-3.0x range Diageo calls "broadly consistent with an A-band credit rating" (20-F p.186); the dividend was cut to defend it, and the EABL / RCB proceeds (c.USD 3.3bn gross) had not been received at 30 June. Interest cover fell from 13.6x (FY22) to 7.0x (FY26) (`fundamentals/commentary.md`). Volatility is 31.6% (1y), 2.5x the FTSE 100 (`risk/notes.md`), and beta is not stable: own regressions range 0.37-0.77 depending on window (`risk/beta_evidence.json`).
- **Credit spread 2.0%** (pre-tax cost of debt 7.22%): **1,478p GBp, -67p, SELL (-11.7%).**
- **Beta 1.00** (Risk agent FLAG 1): **1,502p GBp, -42p, SELL (-10.2%, by 3p).** The SELL line is beta 0.997, only 0.04 above the 0.96 we use.

### 6. Minorities: the new method takes the cheapest view of the outside shareholders (challenges the Valuation agent / PM decision of 2026-10-13)
**Claim:** proportionate minorities value the outside shareholders at the group's own DCF multiple: USD 1,500m is **10.8x** their USD 139m of operating profit (ex-EABL). The market values the largest of them far higher. United Spirits (USL) is listed: its 42.79% outside stake (100% - Diageo's 57.21%, `inputs.yaml`) x 727.35m shares x INR 1,362.5 / 95.285 INR per USD (Yahoo Finance, 12 Oct 2026) = **USD 4,450m** at market, versus USD 755m at book (20-F FY26 p.189) and about USD 1.5bn implied for *all* minorities by our method. USD 4,450m on its own is **31.9x** the operating profit of all minorities combined (ex-EABL), so whatever share of that profit is USL's, the market's multiple on it is at least 31.9x, vs our 10.8x (both in `challenges.json`).
**Change (one change, computed with `desk.valuation_run.build`, book-method bridge with minorities = USL outside stake at market USD 4,450m + other minorities at book USD 1,328m = USD 5,778m):** **1,395p GBp, -150p, SELL (-16.6%).** The rating flips at minorities of **USD 2,619m** on this basis (or a 4.48% share under the proportionate method).

| Minorities method | Minorities (USD m) | Value (GBp) | Impact (GBp) | Rating |
|---|---|---|---|---|
| Proportionate (base, PM decision) | 1,500 | 1,545p | 0 | HOLD (-7.7%) |
| Book (old method; includes EABL's 35%) | 2,083 | 1,524p | -20p | HOLD (-8.9%) |
| SELL line | 2,619 | 1,506p | -39p | SELL line |
| USL at market + others at book | 5,778 | 1,395p | **-150p** | **SELL** (-16.6%) |

**Counter-argument (and why I do not push this as the base case):** this mixes two valuations of the same profits. It deducts USL's minorities at USL's market multiple (c.51x earnings, the figure given with the PM decision; I have not verified it against USL's own filings), while our DCF values *all* of USL's profits, including Diageo's 57.21%, at roughly the group's 10.8x. If the market is right about USL, Diageo's own 57% is also worth far more than the DCF credits it with, and a consistent sum-of-the-parts would add that back; deducting only the outside slice at market takes the cost of the rich multiple without the benefit. In addition, the "others at book" USD 1,328m still contains EABL's 35% outside shareholders, the double count the PM removed (I have no sourced split, so the -150p is overstated by that amount), and the method ignores USL's net cash. So -150p is an **upper bound**. The honest bear point is narrower: the minorities line is a method choice worth up to 150p, the proportionate method sits at the low end of the range, and the HOLD depends on it staying there: the flip needs minorities of USD 2,619m vs the USD 1,500m used, well inside the USD 755m (book) to USD 4,450m (market) range for USL's stake alone.

### Against the bear (the strongest case for the stock, checked honestly)
- **Beta 0.72** (Diageo's own 5y weekly regression, s.e. 0.11, R-squared 0.15; `risk/beta_evidence.json`): **1,844p GBp, +299p, HOLD (+10.2%).** Still not a BUY (needs 1,924p; beta below 0.666). This remains the single largest lever in the model.
- **Restructuring cash after tax relief** at 24.3% (USD 850m -> 643m; tax relief is not confirmed by Diageo, Data agent): **1,552p GBp, +7p, HOLD.** Immaterial.
- **The proportionate minorities fix itself (+20p, 1,524p -> 1,545p) is a fair correction** of the EABL double count; I challenge only its level vs market (challenge 6), not the removal of EABL.

### Retired: old challenge 6 (deducting the FY26 final dividend)
Retired. The 30c final dividend goes ex on **15 Oct 2026**, after the 12 Oct valuation date, so the 1,673p price is cum-dividend and the buyer receives it (`data/notes.md`, Phase 3 additions; 20-F FY26). The number 6 is now used for the minorities challenge.

## Management's track record
- **Incentive targets 2023-26: all missed.** Organic sales CAGR -0.3% vs a 4.0% threshold; organic operating profit CAGR -3.4% vs 4.5% (20-F FY26 p.110).
- **Savings:** the 2017 programme planned to reinvest two thirds; FY23 converted GBP 450m of savings into +15bps of margin (sources in challenge 1).
- **Leverage:** target 2.5-3.0x, actual 3.35x (FY25) and 3.14x (FY26), ending in a dividend cut.
- **Capex:** peaked at 8.0% of sales in FY25 before management cut it to 6.1% in FY26, while ROIC fell to a four-year low.
Pattern: guidance has been met only at the low end or missed. The base case already assumes the low end of guidance is delivered, so it has no cushion.

## Not quantified (no sourced number for a single-change test)
- **Moet Hennessy (34%) at book, USD 5,107m**, tested at fair value less costs of disposal with headroom described as "sensitive" (20-F). Cognac and champagne are weak (Remy's depressed earnings). An impairment would cut the associates line, but I have no sourced fair value.
- **Disposal proceeds (USD 3,318m) are gross**, before tax and costs, and not yet received.
- **GLP-1 / moderation:** no sourced volume effect; it sits inside challenges 3 and 4.
- **Restructuring cash is undiscounted** (paid FY27-29): discounting would add a little; a case for the stock, not quantified.

## Which single challenges flip HOLD to SELL (SELL below 1,505.7p GBp)
Terminal RONIC = WACC; zero organic growth; USL minority at market (an upper bound). The other eight do not. On the other side, beta 0.72 (Diageo's own best regression) reaches BUY by 6p.


## Not quantified, update 15 Oct 2026
Moet Hennessy at book (USD 5,107m, "sensitive" impairment headroom), GLP-1 / moderation, USL net cash and the split of the USD 1,328m other minorities: still no sourced number. Disposal tax is now tested (A2) but only at an illustrative USD 300m. The UK or global implied ERP (our benchmark is the FTSE 100) was not checked.

**Strongest reason not to buy:** the HOLD rests on a 4.2% equity risk premium seen only in search summaries, not on anything Diageo has delivered: at Kroll's published 5.0% the value is 1,592.6p (GBp), below the 1,673p price, at the Fernandez survey's 5.5% it is 1,494.9p, a SELL, and the market itself is pricing an ERP of about 4.6%.
