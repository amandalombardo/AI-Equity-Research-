# Valuation agent notes: Diageo (DGE), run 2026-10-12 (final re-run 15 Oct 2026 after the evidence audit and the PM's bear responses)

## Final re-run 15 Oct 2026 (after the PM's bear-response decisions)
**What changed and why.** The PM accepted all the recommended bear responses on 15 Oct 2026 (`docs/audit-2026-10-15/bear-responses-2026-10-15.md`, PM decision "Accept all"). Two of them change the base case. Both were already in the brief and `inputs.yaml` before this run; I did not edit either.
1. **Diluted shares 2,224m -> 2,231m** (D3): 2,224m basic + 7m dilutive potential shares (20-F FY26 EPS note). The **debt weight** moves from 0.29376 to **0.29311** (net debt USD 20,482m / (USD 20,482m + market cap USD 49,395m at 2,231m shares x 1,673p x 1.3234 USD/GBP)). Source: `inputs.yaml`, applied by `apply_audit_fixes_2026-10-15.py`.
2. **Organic growth FY30-31 3.0% -> 2.0%** (D4, `briefs/DGE.yaml` `dcf.organic_growth` = 0.0%, 1.5%, 2.5%, 2.0%, 2.0%): the 3.0% had no source; 2.0% is the terminal rate.
Nothing else changed: ERP 4.2%, beta 0.96, risk-free 5.22%, price 1,673p (GBp, 12 Oct 2026 close, cum-dividend), FX 1.3234 USD/GBP.

**What I re-ran.** `python -m desk.valuation_run` (`valuation.json`, `dcf.xlsx`), `run_bridge.py` (`bridge.json`), `run_sanity.py` (`sanity_checks.json`) and a new step script, `run_steps_2026-10-15.py` (`steps_2026-10-15.json`: the step table and ERP flip points, engine runs only). Comps not re-run: no comps input changed.

**Excel check.** I recalculated the live `dcf.xlsx` in LibreOffice and compared all 18 checked cells (14 valuation lines + 4 final-year forecast lines) with Python, as `tests/test_valuation_run.py` does. Largest relative difference 5e-10. Value per share **1,772.14p (GBp)** in both. `python -m pytest` could not run: pytest is not installed and cannot be installed here (no package index).

### Final base case (base and engine bear)
| | 15 Oct morning re-run | **Final (15 Oct)** |
|---|---|---|
| Cost of equity / WACC | 9.25% / 7.92% | 9.25% / **7.92%** (debt weight 29.311%) |
| Enterprise value at 30 June 2026 (USD m) | 66,356 | **65,441** |
| Minorities deducted (USD m, 2.566% x EV) | 1,703 | 1,679 |
| Equity value at 30 June 2026 / rolled to 12 Oct 2026 (USD m) | 51,923 / 53,236 | 51,032 / **52,323** |
| Shares (m, ordinary, NOT ADRs) | 2,224 basic | **2,231 diluted** |
| **Value per share** | USD 23.94 / 1,808.8p | **USD 23.45 / 1,772.1p (GBp)** |
| Upside vs 1,673p (GBp) | +8.1% | **+5.9%** |
| **Rating (engine)** | HOLD | **HOLD** |
| Bear case (WACC +1 pt, no growth, 25% flow-through) | 1,298.3p, SELL | **1,293.5p (GBp), -22.7%, SELL** |
| Terminal value share of EV | 76.7% | **76.3%** (FLAG, above 75%) |
| Implied exit multiple (EV / FY31 EBITDA) | 10.0x | **10.0x** (vs 9.78x at market today) |
| Market-implied WACC (g = 2%) / market-implied ERP | 8.30% / 4.78% | **8.20% / 4.62%** |
| DCF vs comps (median P/E value 2,311p GBp) | -21.7% | **-23.3%** |

### Step table from the 13 Oct value (`steps_2026-10-15.json`, one change at a time with `desk.valuation_run.build`, GBp)
| Step | Value | Change | WACC | Rating |
|---|---|---|---|---|
| 13 Oct value (ERP 5.0%, 2,222m shares, debt weight 0.29395, FY30-31 growth 3.0%) | 1,627.3p | | 8.46% | HOLD |
| 1. ERP 5.0% -> 4.2% (PM decision 15 Oct 2026) | 1,810.7p | **+183.5p** | 7.92% | HOLD |
| 2. Shares 2,222m -> 2,224m basic, debt weight 0.29376 (audit finding 8) | 1,808.8p | -2.0p | 7.92% | HOLD |
| 3. Shares 2,224m -> 2,231m diluted, debt weight 0.29311 (PM decision 15 Oct, D3) | 1,802.0p | **-6.8p** | 7.92% | HOLD |
| 4. FY30-31 growth 3.0% -> 2.0% (PM decision 15 Oct, D4) | **1,772.1p** | **-29.8p** | 7.92% | **HOLD** |
| Total since 13 Oct / since the morning re-run | | +144.9p / -36.6p | | |
The old 1,627.26p and the morning 1,808.77p both reproduce exactly. (Step 3 is -6.8p, not the -5.7p in the bear responses, because the debt weight now moves with the share count; step 4 is -29.8p, not -30.0p, because it is measured after step 3.)

**Sensitivity grid (pence, GBp; WACC rows x terminal growth 1.5 / 2.0 / 2.5 / 3.0%)**: WACC 6.92%: 2,093 / 2,214 / 2,362 / 2,545; 7.42%: 1,881 / 1,973 / 2,083 / 2,217; **7.92%: 1,701 / 1,772 / 1,856 / 1,955**; 8.42%: 1,547 / 1,603 / 1,667 / 1,742; 8.92%: 1,415 / 1,458 / 1,507 / 1,564.

### Rating breakevens (engine, one input at a time; SELL line 1,505.7p, BUY line 1,923.95p, both GBp)
| Input | We use | Morning SELL flip | **Final SELL flip** | Morning BUY flip | **Final BUY flip** |
|---|---|---|---|---|---|
| Distance from the line (GBp) | 1,772.1p | 303p above SELL | **266p above SELL** | 115p below BUY | **152p below BUY** |
| Beta | 0.96 | above 1.282 | **above 1.244** | below 0.860 | **below 0.828** |
| WACC | 7.92% | above 8.85% | **above 8.75%** | below 7.63% | **below 7.53%** |
| ERP | 4.2% | above 5.61% | **above 5.44%** | below 3.76% | **below 3.62%** |
| Savings flow-through | 46% | none | **none (0% still HOLD)** | | |
| Terminal RONIC | 13.4% | none down to 7% | **below 7.06% (capex 9.43% of sales), i.e. below the WACC** | | |
| Minorities' share of operating profit | 2.566% | above 15.7% | **above 14.3%** | | |
Other what-ifs (GBp): ERP 5.0% (Kroll) = 1,592.6p (HOLD, -4.8%); **ERP 5.5% (Fernandez) = 1,494.9p (SELL, -10.6%)**. Book-method minorities = 1,758.1p (HOLD).

### Sanity checks (`sanity_checks.json`)
- **FLAG: terminal value is 76.3% of EV**, above the 75% flag.
- **WACC 7.92% is inside 6-9%.** No flag.
- **Implied exit multiple 10.0x FY31 EBITDA**, slightly above the c.9.78x the market pays for Diageo today (approximate; includes EABL). Peer EV/EBITDA still unavailable.
- **DCF vs comps:** DCF 1,772.1p is **23.3% below** the median P/E value (2,311p, GBp). Comps are weak (P/E only).
- **Market-implied WACC 8.20%** vs our 7.92%; market-implied ERP 4.62% vs our 4.2%.

### FLAGs for the PM (final; I have not changed any assumption)
1. **The ERP response D1 rested on "HOLD at every sourced ERP". That is no longer true.** With the two accepted changes, the Fernandez 5.5% survey ERP gives **1,494.9p (GBp), SELL** (-10.6%), and SELL now starts at an ERP of 5.44% (was 5.61%). Kroll's 5.0% gives 1,592.6p (HOLD, -4.8%). The rating is HOLD at 4.2% and 5.0%, SELL at 5.5%. The 4.2% is still unconfirmed at source (seen in search summaries only).
2. **Terminal value 76.3% of EV** (above 75%).
3. **Implied ERP vs bottom-up beta and a FTSE 100 benchmark:** unchanged judgement point (see morning FLAG 2 below).
4. **`run_bridge.py` is not a history, and its step 1 now measures 0.0p.** It replays the Phase 3 steps with today's inputs; its "Previous run" row is 1,698.5p and its last row 1,772.1p (matches the base). Its "terminal-year fix" step shows no change, so the old-terminal-year patch in that script no longer takes effect. Use the step table above and the history line below. I did not edit the script.
5. **Disposal proceeds are gross, tax MISSING** (D2, PM: disclosure only). USD 3,318.3m is before tax and costs; nothing is deducted until Diageo discloses the tax; each USD 100m of tax costs about 3.5p (bear `challenges.json` A2').
6. **Price date:** 1,673p is the 12 Oct close, cum-dividend (30c final went ex on 15 Oct).
7. **Brief comment:** the FY30-31 growth comment in `briefs/DGE.yaml` is up to date. The `terminal_ronic` comment points to these notes for the flip point: it is now 7.06%, below the WACC.

**History of the base value (GBp):** 2,475p (BUY) -> 2,141p (BUY) -> 1,448p (SELL) -> 1,524p (HOLD) -> 1,545p (HOLD) -> 1,627p (mid-year, HOLD) -> 1,808.8p (ERP 4.2% and share count, 15 Oct morning, HOLD) -> **1,772.1p (diluted shares and FY30-31 growth 2.0%, 15 Oct 2026 final, HOLD)**.

**What's missing (unchanged):** peer EV/EBITDA and FCF yield, Constellation Brands EPS, calendarised peer figures, tax on the disposals.

**Confidence:** **Medium** on the mechanics (engine and Excel agree; old and morning values reproduce exactly). **Medium-low** on the rating: HOLD at ERP 4.2% and 5.0% but SELL at 5.5%, and 4.2% is not yet confirmed at source. **Low** on the comps.

## Re-run 15 Oct 2026 morning (evidence audit) (superseded by the final re-run above: 2,224m basic shares, FY30-31 growth 3.0%)
**What changed and why.** Two PM decisions after the evidence audit of 15 Oct 2026 (`docs/audit-2026-10-15/DGE.md`, `docs/audit-2026-10-15/summary.md`). I did not change the brief or `inputs.yaml`. Both were already updated before this run.
1. **Equity risk premium (ERP) 5.0% -> 4.2%** (`briefs/DGE.yaml`, `dcf.wacc.equity_risk_premium`). Source: Damodaran's implied ERP for the S&P 500, 4.20% at 1 Oct 2026 (4.23% at 1 Jan 2026). Evidence: `docs/audit-2026-10-15/erp-evidence.md`. The old 5.0% had no source. This is the premium the market is pricing over today's 10-year yield, so it matches the spot US 10-year risk-free rate (5.22%) we use.
2. **Share count 2,222m -> 2,224m ordinary shares** (the employee-trust shares had been deducted twice; 20-F FY26 p.188 and XBRL: 2,432m issued - 208m own shares; matches the 2,224m weighted average). The **debt weight** therefore moves from 0.29395 to **0.29376** (net debt USD 20,482m / (USD 20,482m + market cap USD 49,240m)). Applied by `runs/DGE/2026-10-12/apply_audit_fixes_2026-10-15.py`.

Nothing else changed: same price 1,673p (GBp, 12 Oct 2026 close), same FX 1.3234 USD/GBP, same beta 0.96, same cash flows.

**What I re-ran.** `python -m desk.valuation_run` (`valuation.json`, `dcf.xlsx`), then `run_bridge.py` (`bridge.json`), `run_comps.py` (`comps.json`, `comps.csv`) and `run_sanity.py` (`sanity_checks.json`). The comps are byte-identical: none of the comps fields depend on the DCF value, the WACC or the share count. The comps-vs-DCF gap is in `sanity_checks.json`.

**Excel check.** I recalculated the live `dcf.xlsx` in LibreOffice and compared all 18 checked cells (14 valuation lines + 4 final-year forecast lines) with Python. The largest difference is 3e-10 (relative). The value per share is **1,808.77p (GBp)** in both. `python -m pytest` could not run: pytest is not installed and could not be installed here (no package index). So I ran the same comparison the test does by hand.

### Old vs new (base case unless stated)
| | Old (13 Oct, Phase 4 memo) | New (15 Oct) | Change |
|---|---|---|---|
| Risk-free rate (US 10-year) | 5.22% | 5.22% | none |
| Beta (bottom-up) | 0.960 | 0.960 | none |
| Equity risk premium | 5.0% (no source) | **4.2%** (Damodaran implied) | -0.8 pt |
| Cost of equity (Ke = Rf + beta x ERP) | 10.02% | **9.25%** | -0.77 pt |
| Pre-tax / after-tax cost of debt | 6.22% / 4.71% | 6.22% / 4.71% | none |
| Debt weight / equity weight | 29.395% / 70.605% | 29.376% / 70.624% | rounding |
| **WACC** | 8.46% | **7.92%** | -0.54 pt |
| Enterprise value at 30 June 2026 (USD m) | 60,870 | **66,356** | +5,486 |
| Minorities deducted (USD m, 2.566% x EV) | 1,562 | 1,703 | +141 |
| Equity value at 30 June 2026 (USD m) | 46,579 | 51,923 | +5,345 |
| Equity value rolled to 12 Oct 2026 at Ke (USD m) | 47,851 | **53,236** | +5,385 |
| Shares (m, ordinary) | 2,222 | 2,224 | +2 |
| **Value per share** | USD 21.54 / **1,627.3p** | USD 23.94 / **1,808.8p** | **+181.5p** |
| Upside vs 1,673p (GBp) | -2.7% | **+8.1%** | |
| **Rating (engine)** | HOLD | **HOLD** | unchanged |
| Bear case (WACC +1 pt, no growth, 25% flow-through) | 1,179.9p (GBp), -29.5%, SELL | **1,298.3p (GBp), -22.4%, SELL** | +118.4p |
| Terminal value share of EV | 74.9% | **76.7%** (FLAG, above 75%) | +1.8 pt |
| Implied exit multiple (EV / FY31 EBITDA) | 9.2x | **10.0x** | +0.8x |
| Market-implied WACC (g = 2%) | 8.32% | **8.30%** | about the same |
| DCF vs comps (median P/E value 2,311p GBp) | -29.6% | **-21.7%** | |

**Where the +181.5p comes from** (`desk.valuation_run.build`, one change at a time, in order): ERP 5.0% -> 4.2% = **+183.5p** (1,627.3p -> 1,810.7p); share count 2,222m -> 2,224m with debt weight 0.29376 = **-2.0p** (-> 1,808.8p). The old 1,627.26p reproduces exactly with the old ERP, shares and debt weight.

**Sensitivity grid (pence, GBp; WACC rows x terminal growth 1.5 / 2.0 / 2.5 / 3.0%)**: WACC 6.92%: 2,137 / 2,261 / 2,411 / 2,599; 7.42%: 1,919 / 2,014 / 2,126 / 2,264; **7.92%: 1,736 / 1,809 / 1,894 / 1,996**; 8.42%: 1,579 / 1,636 / 1,701 / 1,778; 8.92%: 1,443 / 1,488 / 1,538 / 1,597.

### Rating flip points (solved with the engine, one input at a time; SELL line 1,505.7p, BUY line 1,923.95p, both GBp)
| Input | We use | Old SELL flip | **New SELL flip** | Old BUY flip | **New BUY flip** |
|---|---|---|---|---|---|
| Distance from the line (GBp) | 1,808.8p | 122p above SELL | **303p above SELL** | 297p below BUY | **115p below BUY** |
| Beta | 0.96 | above 1.078 | **above 1.282** | below 0.724 | **below 0.860** |
| WACC | 7.92% | above 8.87% | **above 8.85%** | below 7.64% | **below 7.63%** |
| ERP | 4.2% | above 5.62% (audit) | **above 5.61%** | below 3.77% (audit) | **below 3.76%** |
| Savings flow-through | 46% | below 9.1% | **none: 0% still gives 1,644p (HOLD)** | | |
| Terminal RONIC | 13.4% | below 9.26% | **none down to 7%: 1,532p (HOLD)** | | |
| Minorities' share of operating profit | 2.566% | above 8.28% | **above 15.7%** | | |

Other what-ifs (GBp): beta 0.72 (Diageo's own best regression) = 2,107p (BUY); beta 0.85 = 1,936p (BUY, just); beta 1.00 = 1,766p (HOLD). ERP 5.0% = 1,625p (HOLD); ERP 5.5% = 1,526p (HOLD). The market price of 1,673p implies an ERP of about **4.78%** (or a WACC of 8.30%). Book-method minorities would give 1,795.5p (HOLD).

### Sanity checks (`sanity_checks.json`)
- **FLAG: terminal value is 76.7% of EV**, above the 75% flag (was 74.9%). A lower discount rate gives more weight to the far-off years. Most of the value rests on the steady state after FY31 (terminal growth 2%, RONIC 13.4%).
- **WACC 7.92% is inside 6-9%.** No flag.
- **Implied exit multiple 10.0x FY31 EBITDA.** Peer EV/EBITDA is still unavailable, so there is no peer range to test it against. It is now slightly **above** the c.9.75x the market pays for Diageo today (FY26 adjusted EBITDA USD 6,650m less associates USD 218m; approximate, includes EABL). Before, it was slightly below. Not aggressive, but no longer conservative.
- **DCF vs comps:** the DCF (1,808.8p) is **21.7% below** the median P/E value (2,311p, GBp). The comps are unchanged and weak (P/E only, two press-sourced peers, only Pernod on a June year end).
- **Market-implied WACC 8.30%** vs our 7.92%: the market is pricing a discount rate about 0.4 points **above** ours (before the change it was 0.14 points below).

### FLAGs for the PM (I have not changed any assumption)
1. **The ERP now drives the result.** 0.8 points of ERP is worth +183.5p. That is the biggest single change since Phase 3, and it moves the stock from 2.7% below the price to 8.1% above it. The rating stays HOLD, but the base is now nearer BUY (115p, GBp, away) than SELL (303p). BUY needs beta below 0.86, WACC below 7.63% or ERP below 3.76%. The brief itself says the 4.2% figure was **seen in search summaries only** (Damodaran's site was blocked). Please confirm it on Damodaran's home page before publishing.
2. **Possible inconsistency: implied ERP with a bottom-up beta.** Damodaran's implied ERP is a US market (S&P 500) premium. Our beta is a global-industry beta relevered at Diageo's D/E, and the price is in London. The desk uses the same ERP for all four companies, which is consistent. But the FTSE 100 is our benchmark (brief), and no UK or global implied ERP was checked. This is a judgement for you, not an error.
3. **Terminal value share above 75%** (76.7%). See above.
4. **Brief comments are out of date** (I have not edited them). The `flow_through` comment points to `sanity_checks.json`, which is correct. But the `terminal_ronic` comment says "if returns fall to c.10.8%, capex 7.1% -> SELL". With the new ERP, RONIC 10.8% gives 1,736p (HOLD), and even 7% does not reach SELL.
5. **`bridge.json` is not a history.** `run_bridge.py` replays the Phase 3 steps with **today's** inputs (ERP 4.2%, mid-year convention). Its "Previous run" row is now 1,702.6p (GBp), not the historic 1,448p, and its last step is 1,808.8p. Use the history line below for the actual path. I did not edit the script, only re-ran it.
6. **Price date.** The 1,673p (GBp) price is the 12 Oct close, cum-dividend. The 30c final dividend went ex on 15 Oct (audit: about 22.6p), so prices from 15 Oct on are not like-for-like with this value.
7. **Other open audit items, not applied (not my decisions):** FY30-31 growth of 3% has no source (2% = -27p); disposal proceeds are gross, not net of tax (about -3.5p per USD 100m of tax); dilution (+7m options) ignored (about -6.6p). None of these flips the rating on its own.

**History of the base value (GBp):** 2,475p (BUY) -> 2,141p (BUY) -> 1,448p (SELL) -> 1,524p (HOLD) -> 1,545p (HOLD) -> 1,627p (mid-year, HOLD) -> **1,808.8p (ERP 4.2% and share count, 15 Oct 2026, HOLD)**.

**What's missing (unchanged):** peer EV/EBITDA and FCF yield, Constellation Brands EPS, and calendarised peer figures (only Pernod is on a June year end).

**Confidence:** **Medium** on the mechanics (the engine and Excel agree, and the old value reproduces exactly). **Medium-low** on the rating: it now hinges on the ERP and beta, and the 4.2% ERP has not yet been confirmed at its primary source. **Low** on the comps.

---
**Everything below this line is superseded 15 Oct 2026. It is kept for the record. Its numbers use ERP 5.0% and 2,222m shares.**

## Phase 4 re-run (13 Oct 2026) (superseded 15 Oct 2026)
**What changed.** PM decision (13 Oct 2026, evidence `docs/phase4/evidence-phase4.md`): the brief's `mid_year_convention` is now **true**. Each year's cash flow is discounted from the middle of the year (0.5, 1.5 ... 4.5 years from 30 June 2026) instead of its last day, because Diageo's free cash flow arrives through the year (61.7% of FY25 and 47.7% of FY26 came in the first half; `data/phase4_evidence.json`). The terminal value (Gordon growth) moves half a year too (4.5 years), after the engine fix logged as mistakes-log row 15; without that fix the switch would have given an inconsistent 1,566p.

| | Base | Bear |
|---|---|---|
| WACC | 8.46% | 9.46% |
| Enterprise value at 30 June 2026 (USD m) | 60,870 | 47,729 |
| Minorities deducted (USD m, 2.566% x EV) | 1,562 | 1,225 |
| Equity value at 30 June 2026 (USD m) | 46,579 | 33,775 |
| Equity value rolled to 12 Oct 2026 (USD m) | 47,851 | 34,697 |
| Value per share | USD 21.54 / **1,627p** | USD 15.62 / **1,180p** |
| Upside vs 1,673p | **-2.7%** | -29.5% |
| Rating (engine) | **HOLD** | SELL |

Effect: +82p (1,544.8p -> 1,627.3p). The whole EV rises by (1 + WACC)^0.5 - 1 = 4.1%, so the terminal value share (74.9%) and the implied exit multiple (9.2x FY31 EBITDA) are unchanged. Live Excel (`dcf.xlsx`) recalculated in LibreOffice: 1,627.26p, same as Python.
**SELL line 1,505.7p: 122p headroom** (was 39p). New SELL flips (`sanity_checks.json`): flow-through below 9.1%, beta above 1.078, WACC above 8.87%, terminal RONIC below 9.26%, minorities share above 8.28%. **BUY line 1,924p:** beta below 0.724 or WACC below 7.64%. Market-implied WACC at g = 2%: 8.32%.
Comps (unchanged): median P/E implies 2,311p; DCF is 29.6% below it.
FLAG: the HOLD is now less fragile, but the improvement is a timing convention, not new information about Diageo's business.


**History of the base value (superseded 15 Oct 2026):** 2,475p (first run, BUY) -> 2,141p (cost of debt fixed, BUY) -> 1,448p (bottom-up beta 0.96, SELL) -> 1,524p (Phase 3, HOLD) -> **1,545p (proportionate minorities, PM decision 2026-10-13, HOLD)**.

## Step 1: inputs check (superseded 15 Oct 2026)
`inputs.yaml` has every required value with a source, including beta 0.96 from the Risk agent the two Phase 3 inputs (`restructuring_cash` USD 850m; `dividends_ex_before_valuation_musd` 0) and, for the 2026-10-13 re-run, `minority_share_of_operating_profit` 2.566% (sourced to the 20-F p.210 and p.164). No STOP. I did not change `briefs/DGE.yaml` or `inputs.yaml`.

## Step 2: DCF (`valuation.json`, `dcf.xlsx`) (superseded 15 Oct 2026)
Valued at the 30 June 2026 balance sheet date (no stub), equity rolled forward to 12 Oct 2026 (0.2822 years) at the cost of equity, no dividend deducted (the 30c final goes ex on 15 Oct). Terminal year is a normalised steady state; terminal capex set from RONIC 13.4% = **6.21% of sales** (forecast years stay at 7.11%). Savings flow-through 46%.

| | Base | Bear |
|---|---|---|
| WACC | 8.46% | 9.46% |
| Enterprise value at 30 June 2026 (USD m) | 58,448 | 45,620 |
| Minorities deducted (USD m, proportionate: 2.566% x EV) | 1,500 | 1,171 |
| Equity value at 30 June 2026 (USD m) | 44,219 | 31,720 |
| Equity value rolled to 12 Oct 2026 (USD m) | 45,427 | 32,586 |
| Value per share | USD 20.44 / **1,545p** | USD 14.67 / **1,108p** |
| Upside vs 1,673p | **-7.7%** | -33.8% |
| Rating (engine) | **HOLD** | SELL |

WACC parts: risk-free 5.22% (US 10-year), beta 0.96, ERP 5.0%, cost of equity 10.02%; pre-tax cost of debt 6.22% (risk-free + 1%, PM rule), 4.71% after tax (tax 24.3%); debt weight 29.4%, equity weight 70.6%.

Bridge (USD m, at 30 June 2026): EV 58,448 - net debt 20,482 (incl. leases) - minorities 1,500 (proportionate) - pension 0 - restructuring cash 850 + associates 5,284 + disposal proceeds 3,318 = 44,219; x (1.1002)^0.2822 = 45,427; / 2,222m shares / 1.3234 USD per GBP = 1,545p (GBp).

The live Excel workbook (`dcf.xlsx`), recalculated in LibreOffice, gives the same 1,544.8p, so it matches the engine (its minorities cell is now share x EV, falling back to book if the share is blank).

## Minorities (PM decision 2026-10-13) (superseded 15 Oct 2026)
**What changed.** Diageo owns most, but not all, of some subsidiaries (mainly United Spirits in India, 57%; EABL in Kenya, 65%, now being sold). The DCF values 100% of their cash flows, so we must take off the slice that belongs to the outside shareholders. Until now we took that slice at its **book value, USD 2,083m** (an accounting figure from the balance sheet). We now value it the same way as the rest of the business: **outside shareholders' share of operating profit (2.566%, ex-EABL) x enterprise value = USD 1,500m** (base case; USD 1,171m in the bear case, because it moves with EV). Effect: **+20p (GBp)**, from 1,524.4p to 1,544.8p (shown as +21p if you subtract the rounded 1,524p from 1,545p).

**Why.** Book value failed your evidence test: (1) it is an accounting number, not a value (USL's minority is USD 755m at book vs c.USD 4.45bn at market); (2) it double counted EABL: EABL's 35% outside shareholders were inside the 2,083, yet EABL is already excluded from the forecast and only Diageo's own sale proceeds are added back.

**Weaknesses (it is an estimate, not a market price).**
- It assumes minorities are worth their share of *operating profit* times the group multiple. Subsidiaries with faster growth or a higher multiple (USL) are under-valued by this; slower ones over-valued.
- It ignores **USL's net cash** (and any subsidiary-level debt): outside shareholders own a slice of that cash too, which the operating-profit share does not capture.
- To strip out EABL it assumes **EABL's minorities share EABL's EBIT pro rata** (35% x USD 250.2m); the actual EABL profit attributable to minorities may differ (interest, tax, its own minorities).
- Sensitivity: the rating flips to SELL only if the minorities' share of operating profit is above about **4.48%** (vs 2.566%), i.e. minorities of roughly USD 2.6bn, so the method choice alone does not decide HOLD vs SELL. The old book method would also give HOLD (1,524p).

**Distance to SELL.** The SELL line is **1,506p (GBp)** (10% below 1,673p). The base is now **39p above it** (was 18p), i.e. 7.7% below the price vs the 10% trigger.

## Step 3: comps (`comps.csv`, `comps.json`) (superseded 15 Oct 2026)
P/E only (peer EV/EBITDA is still unavailable). All 4 core peers now have a P/E: Pernod Ricard 10.7x, Brown-Forman 17.4x, Campari 19.6x, Remy Cointreau 25.3x. **Median 18.5x**, applied to Diageo's FY26 EPS before exceptionals (165.3 cents) = **2,311p** (range 1,334p to 3,163p). Diageo trades at 13.4x. Only Pernod has a June year end; the others could not be calendarised (next fiscal years or half-years not yet found), so their gaps are 2 to 6 months. Campari and Remy come from press reports, not filings, and Remy's P/E is inflated by depressed cognac earnings. Constellation Brands (beer-heavy, shown separately) is still missing. **Indicative only.**

## Step 4: sanity checks (`sanity_checks.json`) (superseded 15 Oct 2026)
- **Terminal value is 74.9% of EV**, just under the 75% flag (no FLAG, but close).
- **WACC of 8.46% is inside 6-9%.**
- **Implied exit multiple: 9.2x FY31 EBITDA** (was 8.6x). Peer EV/EBITDA is unavailable, so I cannot test it against a peer range. It is a little below the roughly 9.7x the market pays for Diageo today (FY26 adjusted EBITDA ex associates; approximate, includes EABL; market EV now uses proportionate minorities, c.USD 1,608m at market), so it does not look aggressive.
- **Market-implied WACC: about 8.1%.** On the sensitivity grid at 2% growth, 1,673p sits between WACC 7.96% (1,714p) and 8.46% (1,545p); solving with the engine gives 8.07%. The market is pricing a WACC about 0.4 points below ours.
- **DCF vs comps: the DCF (1,545p) is 33% below the comps value (2,311p).** The gap widened from 17% (before Phase 3) because Campari and Remy (both on high P/Es) entered the median. The comps value is pulled up by Remy's depressed earnings; Pernod, the closest peer by year end and mix, is at 10.7x, below Diageo's 13.4x. I would not give the comps much weight.

## What changed vs 1,448p (computed with `desk.valuation_run.build`, one change at a time, cumulative; `run_bridge.py`, `bridge.json`; steps 0-5 use book minorities, step 6 switches to proportionate) (superseded 15 Oct 2026)

| Step | Value (p) | Change (p) |
|---|---|---|
| Previous run | 1,448 | |
| 1. Terminal-year fix: steady state, working capital grows at 2% (not FY31's 3%) | 1,474 | +27 |
| 2. Terminal capex from RONIC 13.4% (7.11% -> 6.21% of sales) | 1,540 | +65 |
| 3. Savings flow-through 46% (was 50%) | 1,527 | -13 |
| 4. Value at 30 June and roll equity forward at the cost of equity | 1,554 | +27 |
| 5. Restructuring cash USD 850m deducted | 1,524 | -30 |
| 6. Minorities: book USD 2,083m -> proportionate USD 1,500m (PM decision 2026-10-13) | 1,545 | +20 |
| **Total** | **1,545** | **+97** |

The step-0 run reproduces 1,448p exactly (old terminal formula: FY31 cash flow x 1.02). Measured one at a time from 1,448p instead of in sequence, the steps are +27, +92, -15, +27, -29, +22p; the order only matters much for terminal capex (it is worth more before the flow-through cut and the roll-forward).

## For the PM (I have not changed any assumption) (superseded 15 Oct 2026)
1. **FLAG: the HOLD is still close to SELL, but less so.** The value is 7.7% below the price; SELL starts at 10% (1,506p GBp), now 39p lower (was 18p). Thresholds solved with the engine (`run_sanity.py`, `sanity_checks.json`), one input at a time: SELL if **beta above 0.997** (we use 0.96), **WACC above 8.59%** (we use 8.46%), **savings flow-through below 33.6%** (we use 46%), **terminal RONIC below 11.7%** (we use 13.4%; terminal capex 6.75% of sales), or **minorities' share of operating profit above 4.48%** (we use 2.566%). BUY (1,924p GBp) would need a **beta below 0.666** or a **WACC below 7.44%**. Note: the brief's comment "Rating flips to SELL at c.40%" (flow-through) is now out of date: at 40% the value is 1,526p (HOLD); the flip is at c.34%. I have not edited the brief.
2. **Beta is still the biggest lever.** Beta 0.72 (Diageo's own best regression) gives 1,844p (HOLD); 0.85 gives 1,672p; 0.96 gives 1,545p (all GBp).
3. **Terminal capex below the 5-year history.** 6.2% of sales vs 7.1% actual over FY22-26, worth +65p. It is consistent with the 13.4% ROIC rule you chose, but it assumes the heavy maturing-stock and capacity spend of recent years is not repeated forever. Reasonable, but it is the largest single upward step.
4. **Restructuring cash is pre-tax and undiscounted** (USD 850m at 30 June, though paid over FY27-29). Tax relief (up to about USD 207m) and discounting would each add a little (Data agent: up to about 7p for tax). Conservative; I left it as is.
5. **Comps are weak** (P/E only, two press-sourced peers, no calendarisation except Pernod, no EV/EBITDA). The 34% gap to comps should not drive the decision.
6. Tests: `python -m pytest` could not run here (pytest is not installed in this environment). I changed no code in `desk/`; I changed only my own helper scripts (`run_bridge.py` now adds the minorities step and reads minorities from the engine; new `run_sanity.py` regenerates `sanity_checks.json` and the thresholds).

## What's missing (superseded 15 Oct 2026)
Peer EV/EBITDA and FCF yield; Constellation Brands EPS; calendarised peer figures (only Pernod is on a June year).

## Confidence (superseded 15 Oct 2026)
**Medium** on the DCF mechanics (engine and Excel agree; the 1,448p baseline reproduces exactly). **Medium-low** on the rating, because HOLD vs SELL sits within 39p and rests mainly on beta (SELL above 0.997) and WACC. **Medium** on the minorities figure (an estimate from operating profit shares, see above). **Low** on comps.

## Savings schedule used (from the brief, PM assumption) (superseded 15 Oct 2026)
c.USD 1,000m in total: USD 850m from the operating framework (c.40% in FY27, the rest in FY28) and USD 150m from the supply chain (c.25% in FY27). Cumulative run-rate (USD m): 377.5, 962.5, 1,000, 1,000, 1,000, of which 46% reaches operating profit. Source: Diageo Capital Markets Day 6-K, 6 Aug 2026.


## Source check, 15 Oct 2026 (mistakes log row 33)
Beta 0.9601 -> 0.9526 (Damodaran's exact 0.7250, see risk/notes.md). Re-ran desk.valuation_run, run_bridge.py, run_sanity.py and run_steps_2026-10-15.py (new step 5). Results: WACC 7.90% (was 7.92%), cost of equity 9.22%, **fair value 1,780.2p GBp (was 1,772.1p, +8.1p), HOLD, upside +6.4%**; engine bear 1,298.8p; TV 76.4% of EV; ERP SELL above 5.48%, BUY below 3.65%; at ERP 5.5% 1,502.9p (still SELL, 2.8p below the 1,505.7p line). run_sanity.py's RONIC search now starts at 5% (the SELL point moved just below 7%: 6.97%). Tables above show the superseded values.
