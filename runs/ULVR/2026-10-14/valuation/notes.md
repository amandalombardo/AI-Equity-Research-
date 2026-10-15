# Valuation agent notes: Unilever PLC (ULVR), run 2026-10-14 (fourth run: evidence audit re-run, 15 Oct 2026; final 4,258.5p HOLD)

Units: money in EUR m (Unilever reports in euros). Value per share in pence (GBp, the London price) and EUR. EUR 1.18190 per GBP (FRED, 9 Oct 2026). 2,154.3m shares. Price 4,710.5p (ULVR.L close 13 Oct 2026). Rating rule: SELL at -10% or worse (below 4,239.45p), BUY at +15% or better (5,417.1p and above).

## Re-run 15 Oct 2026 (evidence audit): FINAL figures, 4,258.5p HOLD

**Result: 4,258.5p (EUR 50.33) per share, -9.6% vs 4,710.5p: HOLD**, only 19.1p (0.4% of the price) above the SELL line of 4,239.45p. The old run (14 Oct) was 3,855p SELL. This replaces my earlier 15 Oct re-run (4,180p SELL), which used a stale JV value and FY26 growth of +0.5%.

**Why it changed.** The PM made five changes, all already in briefs/ULVR.yaml and inputs.yaml. I changed neither file.
1. **ERP 5.0% -> 4.2%.** Damodaran implied ERP, 4.20% at 1 Oct 2026. Brief FLAG: seen in search summaries only; the PM is to confirm it on Damodaran's site.
2. **Pension plans in deficit deducted after tax: EUR 698.6m** = EUR 944m (unfunded 844 + funded deficit 100, 20-F p.131) x (1 - 26%). The surplus in other plans is not added.
3. **McCormick dividends the new shares miss before closing: EUR 642.9m deducted** = 499,691,175 shares x USD 0.48 x 3 quarters / 1.1193 USD per EUR. Foods consideration EUR 33,955.3m -> 33,312.4m; items priced today EUR 35,890.5m -> 35,247.6m (not grown in the roll-forward).
4. **JV value recomputed at the new cost of equity** (runs/ULVR/2026-10-14/apply_audit_fixes_2026-10-15.py): 229 x 1.016 / (7.164% - 1.6%) = EUR 4,181.2m (was EUR 3,709.6m at 7.872%). `associates` EUR 7,061.8m -> **EUR 7,533.5m**. This closes FLAG 2 of my earlier re-run; the JV in inputs.yaml now matches this run's cost of equity (checked: implied Ke 7.164%).
5. **FY26 growth +0.5% -> +2.0%** (PM decision 15 Oct 2026, audit finding 3). +2.0% is the H1 2026 reported turnover change of the three businesses the DCF values (H1 2026 6-K). +0.5% was the whole Group including Foods, which the DCF leaves out. The bear case FY26 is also +2.0%. FY27-30 stay at +1.6% (bear +0.2%).

**What I did.**
- **Input check.** Every value in inputs.yaml has a source, including beta 0.8844 (Risk agent). The loader found nothing missing. `foods_perimeter_interim_cash_flows_meur` is still null; it is informational and MISSING, as before.
- **Engine.** I ran `python -m desk.valuation_run briefs/ULVR.yaml runs/ULVR/2026-10-14/inputs.yaml runs/ULVR/2026-10-14/valuation`. It rewrote valuation.json and dcf.xlsx: base 4,258.5p HOLD, bear 3,475.6p SELL.
- **Excel check.** I recalculated dcf.xlsx in LibreOffice. All 14 valuation lines match Python, from the cost of equity down to the upside; the largest relative difference is 3.7e-10. The DCF sheet shows FY26 growth 0.02. The Inputs sheet shows ERP 0.042, pension 698.6, associates 7,533.5, Foods consideration 33,312.4 and priced-today 35,247.6.
- **Comps.** I re-ran run_comps.py. Peer multiples are unchanged. The comps median rises from 3,858p to 3,902p for two reasons: the JV (+EUR 471.7m in associates), and FY26 growth, which lifts Unilever's calendarised EBITDA (12 months to June 2026) from EUR 8,100m to EUR 8,161m.
- **Sanity checks.** I re-ran run_sanity.py (writes sanity_checks.json) and added two outputs:
  - a step table from the old run to the final figure (`step_table_old_to_final`), built by undoing each PM decision in memory;
  - an FY26-growth breakeven (`e_flip_points.fy26_growth_only`).

  The first step reproduces the old 3,855p exactly, and the last step equals the engine's 4,258.5p.

### Step table: old 14 Oct run -> final (value per share in pence, GBp; upside vs 4,710.5p)

| Step (each on top of the one above) | Change | Value | Upside | Rating |
|---|---|---|---|---|
| Old run 14 Oct (ERP 5.0%) | | 3,855.3p | -18.2% | SELL |
| 1. ERP 5.0% -> 4.2% | +379.1p | 4,234.4p | -10.1% | SELL |
| 2. Pension deficit after tax, EUR 698.6m (grown at Ke to today) | -29.0p | 4,205.4p | -10.7% | SELL |
| 3. McCormick dividends before closing, EUR 642.9m (not grown) | -25.2p | 4,180.2p | -11.3% | SELL (my earlier re-run) |
| 4. JV recomputed at Ke 7.164% (associates EUR 7,061.8m -> 7,533.5m) | +19.6p | 4,199.7p | -10.8% | SELL |
| 5. FY26 growth +0.5% -> +2.0% | +58.8p | **4,258.5p** | **-9.6%** | **HOLD** |
| **Total** | **+403.3p** | | | |

Steps 1 and 5 depend a little on the order they are applied in (each is sized at the inputs above it), but the total does not.

### Final key numbers

| | Old (14 Oct) | **Final (15 Oct)** |
|---|---|---|
| Cost of equity (Ke) = Bund 3.45% + beta 0.8844 x ERP | 7.872% | **7.164%** |
| After-tax cost of debt = (3.45% + 0.70%) x (1 - 26%) | 3.071% | 3.071% |
| Weights equity / debt | 83.87% / 16.13% | 83.87% / 16.13% |
| **WACC** | 7.10% | **6.50%** |
| FY26 sales (ex-Foods perimeter), EUR m | 40,002 | 40,599 |
| PV of FCF FY26-30, EUR m | 22,165 | 22,868 |
| Terminal value (Gordon growth, g 1.6%), EUR m | 93,907 | 106,840 |
| PV of terminal value, EUR m | 68,975 | 80,461 |
| **EV, EUR m** | 91,140 | **103,329** |
| Minorities (proportionate 10.684% x EV), EUR m | -9,737 | -11,040 |
| Pension plans in deficit after tax, EUR m | 0 | -698.6 |
| Associates and stakes, EUR m | 7,061.8 | 7,533.5 |
| Foods consideration (today's value), EUR m | 33,955.3 | 33,312.4 |
| Equity at 31 Dec 2025, EUR m | 98,844 | 108,861 |
| **Equity at 14 Oct 2026, EUR m** | 98,163 | **108,431** |
| **Value per share** | EUR 45.57 = 3,855p | **EUR 50.33 = 4,258.5p** |
| **Upside vs 4,710.5p** | -18.2% | **-9.6%** |
| **Rating** | SELL | **HOLD (19.1p above the SELL line of 4,239.45p; BUY starts at 5,417.1p)** |
| Bear (FY26 +2.0%, FY27-30 +0.2%, WACC +1 pt to 7.50%) | 3,212p (-31.8%) SELL | **3,475.6p (-26.2%) SELL** |
| **Terminal value share of EV** | 75.7% | **77.9% (FLAG)** |
| Implied exit EV/EBITDA (TV / FY30 EBITDA) | 10.9x | 12.2x |
| **Market-implied WACC** (DCF value = 4,710.5p, all else unchanged) | 5.96% | **5.97%** |
| Comps (EV/EBITDA LTM, all 7 peers) low / median / high | 3,166 / 3,911 / 6,541p | 3,152 / **3,902** / 6,552p |
| DCF vs comps median | 1.4% below | **9.1% above** |
| Sensitivity grid (valuation.json): WACC 5.50-7.50% x terminal growth 1.1-2.6% | 3,254p to 5,296p | 3,504p to 6,273p |

### Breakevens: what turns the HOLD back into a SELL (one input at a time, value = 4,239.45p)

The cushion is **19.1p, or about EUR 486m of value today** (each EUR 1bn = 39.3p).

| Input | Used | HOLD -> SELL at | Distance |
|---|---|---|---|
| **ERP** (JV recomputed at each Ke / JV held as in inputs) | 4.20% | **4.234% / 4.236%** | +0.03 pt. Damodaran's January figure of 4.23% would still give HOLD (4,241.6p), by about 2p |
| **Risk-free (Bund)**; moves Ke, cost of debt and JV | 3.45% | **3.476%** (JV held: 3.477%) | **+0.03 pt (about 3 basis points)**. The 9 Oct cross-check of 3.50% gives **4,222p, SELL** |
| **FY26 growth only** (FY27-30 unchanged) | +2.0% | **+1.51%** | -0.49 pt |
| Long-run growth (FY27-30 and terminal together, JV consistent) | 1.6% | 1.569% | -0.03 pt |
| Terminal growth only (JV consistent) | 1.6% | 1.560% | -0.04 pt |
| **McCormick share price** (dividend deduction kept) | USD 44.64 | **USD 43.55** | -2.4% (USD 1.09) |
| WACC (added directly) | 6.50% | 6.53% | +0.03 pt |
| Beta (JV consistent) | 0.8844 | 0.892 | +0.007 |
| Operating margin | 17.7% | 17.61% | -0.09 pt |

BUY (5,417.1p) would need an ERP of 2.63%, a risk-free rate of 2.24%, a WACC of 5.33%, or a McCormick price of USD 110.72. FY26 growth alone cannot reach BUY.

### Sanity checks (final)
| Check | Result | |
|---|---|---|
| Terminal value share of EV | **77.9%** | **FLAG (above 75%)** |
| Implied exit EV/EBITDA | **12.2x** | OK: within the peer range 9.3x-21.2x, just above the peer median of 11.9x. The market pays 14.7x for Unilever's remaining business |
| WACC within 6-9% | **6.50%** | OK, close to the floor. Not changed |
| DCF vs comps | DCF 4,258.5p vs comps median 3,902p (range 3,152-6,552p) | DCF **9.1% above** comps. On these comps the value is SELL (-17.2%), while the DCF gives HOLD. Without KMB the comps median is 4,575p (HOLD) |

### Other sizes (sanity_checks.json, final inputs)
- **Value breakdown (pence):** DCF of the remaining business after minorities 3,827p; Foods consideration 1,308p; other stakes 308p (JVs 173p, TMICC 76p, other 59p); net debt -957p, restructuring -21p, pension -29p, dividends since December -119p, buyback -59p. Total 4,258.5p.
- **Beta (JV recomputed):** own 5-year monthly 0.91 gives 4,191p (-11.0%) SELL. Own 5-year weekly 0.54 gives **5,486p (+16.5%) BUY** at WACC 5.29%, which is below the 6-9% range.
- **McCormick dividends, 2 quarters instead of 3** (closing before the July 2027 ex-date): **4,267p (+8.4p), -9.4%, HOLD.**
- **Foods timing (not in the base, as before):** cash part discounted at the cost of debt -16p; whole consideration at WACC -57p. Either would make it SELL.
- **Foods tax (MISSING, not deducted):** each EUR 1bn costs 39.3p. Any tax above about EUR 0.49bn makes it SELL. The bear's 25% of the cash costs 138p.
- **Credit spread 1.0% instead of 0.70%:** 4,232p, SELL.

### FLAGs (final)
1. **HOLD by 19.1p (0.4% of the price): a borderline call.** It flips to SELL with:
   - ERP 0.03 points higher;
   - a Bund 3 basis points higher (the 9 Oct reading of 3.50% gives SELL);
   - McCormick 2.4% lower;
   - a credit spread of 1.0%;
   - any discount for the Foods consideration arriving in mid-2027;
   - Foods tax above about EUR 0.49bn.

   The memo should present this as a borderline HOLD that leans SELL, not as a firm HOLD.
2. **Terminal value is 77.9% of EV** (above 75%).
3. **WACC 6.50% is near the bottom of the 6-9% range.** The market-implied WACC is 5.97%.
4. **The ERP (4.2%) is not yet confirmed at the source,** and the risk-free rate (3.45%) is from an aggregator. Each one alone decides the rating within a few basis points.
5. **Comps and DCF give different ratings.** Comps median 3,902p (SELL, -17.2%); DCF 4,258.5p (HOLD).
6. **The FY26 +2.0% is the H1 reported growth, not a full-year figure,** and it is worth +58.8p. If H2 currency drag or the business mix pulls the full year below +1.51%, the rating is SELL.
7. **Bear case** still holds the JV at the base Ke. At Ke +1 point the JV would be EUR 3,544m, about -25p (bear stays SELL).
8. **Still open from earlier runs:** Foods tax MISSING; Foods interim cash flows MISSING; credit spread is a USD index on a EUR Bund; McCormick dividend rate and the 2 vs 3 quarters timing; leverage date; comps data quality.

### For the PM (nothing changed)
- I agree with all five changes; each has a source. The JV recompute follows the input's own rule. FY26 +2.0% fixes a real mismatch, because the DCF excludes Foods.
- Before the memo is final, I would ask for two things:
  - confirmation of the 4.2% ERP and of the Bund on the run date at primary sources;
  - a view on Foods tax and closing timing.

  Each of these is bigger than the 19.1p cushion.

### Confidence
**High on the mechanics.** Excel matches Python, the step table reproduces the old 3,855p and the final 4,258.5p exactly, and the value breakdown adds up to 4,258.5p.
**Low on the rating.** HOLD vs SELL depends on inputs whose normal uncertainty is several times the 19.1p margin.

---

**Everything below is the 14 Oct 2026 run (ERP 5.0%, no pension or McCormick deductions): superseded 15 Oct 2026.** It is kept for the audit trail. The method notes still apply; the numbers do not.

# Run 3 (14 Oct 2026, PM decision 11): superseded 15 Oct 2026


**History of this folder** (Run 4, 15 Oct 2026, is at the top: final 4,258.5p HOLD):
- **Run 1:** 4,101p, SELL.
- **Run 2** (engine fix 3414aec: run-date market values no longer grown in the roll-forward; grid centred on 1.6%): 4,018p, SELL.
- **Run 3 (this one, PM decision 11):**
  - Risk-free changes from 3.18% (FRED OECD monthly average for Aug 2026) to **3.45%**, the Bund on the run date. The source is an aggregator (Trading Economics), and the PM has flagged that.
  - Associates change to **7,061.8**, because the JV Gordon value is re-valued at the new 7.872% cost of equity (JVs 3,709.6, was 3,876.4).
  - **Value: 3,855p. Still SELL, now firmer (-18.2%).**

## [Superseded 15 Oct 2026] What I did
1. **Input check:** every value in `../inputs.yaml` has a source. The engine's loader found nothing missing. `foods_perimeter_interim_cash_flows_meur` is null; it is informational and MISSING (sized below). I checked that associates 7,061.8 = TMICC 1,935.2 + JVs 229 x 1.016 / (7.872% - 1.6%) = 3,709.6 + associates 15 + investments 902 + Magnum 500. I also checked that `priced_at_valuation_date_meur` (35,890.5) = TMICC + Foods consideration (unchanged by decision 11).
2. **Engine:** `python -m desk.valuation_run briefs/ULVR.yaml runs/ULVR/2026-10-14/inputs.yaml runs/ULVR/2026-10-14/valuation` wrote `valuation.json` and `dcf.xlsx`. I recalculated `dcf.xlsx` in LibreOffice: all 17 checked lines match Python (largest relative difference 2e-10, tolerance 2%). The workbook shows risk-free 3.45%, pre-tax cost of debt 4.15% and associates 7,061.8.
3. **Comps:** `run_comps.py` was re-run; it writes `comps.csv` and `comps.json`. The net debt items are unchanged. Associates 7,061.8 flows through the same bridge.
4. **Checks and sizes:** `run_sanity.py` was re-run; it writes `sanity_checks.json`. The JV is recomputed at every cost of equity in the beta sensitivity and flip points. Two script fixes in this run:
   - The terminal-growth search range now runs up to just below the WACC (the BUY flip lay above 4%).
   - The roll-forward check now reports the size of the engine fix on today's inputs.

   The brief and inputs.yaml were not changed.

To re-run from the repo root: `PYTHONPATH=. python runs/ULVR/2026-10-14/valuation/run_comps.py`, then `.../run_sanity.py`.

## [Superseded 15 Oct 2026] Base case (PM assumptions unchanged)
**WACC 7.10%** = 83.87% equity x cost of equity 7.872% (Bund 3.45% + beta 0.8844 x ERP 5.0%) + 16.13% debt x after-tax cost of debt 3.07% (Bund 3.45% + A spread 0.70% = 4.15%, x (1 - 26%)).

| EUR m | FY26 | FY27 | FY28 | FY29 | FY30 |
|---|---|---|---|---|---|
| Sales (ex-Foods perimeter) | 40,002 | 40,642 | 41,292 | 41,953 | 42,624 |
| EBIT at 17.7% | 7,080 | 7,194 | 7,309 | 7,426 | 7,544 |
| Unlevered FCF | 5,043 | 5,176 | 5,259 | 5,343 | 5,429 |
| PV at 7.10% (mid-year, from 31 Dec 2025) | 4,873 | 4,671 | 4,431 | 4,203 | 3,988 |

- Terminal value (Gordon growth, g 1.6%, terminal capex 3.97% of sales so that new investment earns RONIC 17.8%): **93,907**. PV 68,975.
- **EV 91,140** = PV of FCF 22,165 + PV of TV 68,975.

| Bridge at 31 Dec 2025 | EUR m |
|---|---|
| EV | 91,140 |
| less minorities, proportionate (10.684% x EV) | -9,737 |
| less net debt (leases inside) | -23,076 |
| less one-off restructuring for stranded costs | -500 |
| plus associates, stakes and investments (TMICC 1,935 + JVs 3,710 + associates 15 + other investments 902 + net Magnum balance 500) | +7,062 |
| plus Foods consideration at today's market value (untaxed) | +33,955 |
| **Equity at 31 Dec 2025** | **98,844** |
| Roll-forward: (98,844 - 35,890.5 priced today) grown at Ke 7.872% for 0.786 years, + 35,890.5, - dividends gone ex 3,039, - H1 buyback 1,507 | |
| **Equity at 14 Oct 2026** | **98,163** |

**Value per share: EUR 45.57 = 3,855p.** Against 4,710.5p that is **-18.2%: SELL** (rule: SELL at -10% or worse, BUY at +15% or better). The HOLD band runs from 4,239p to 5,417p, so the base case is **384p (8.2 points) inside SELL**.
**Bear case** (FY27-30 growth 0.2%, WACC +1 pt to 8.10%): EV 73,861, **3,212p (-31.8%), SELL**.
**Sensitivity grid in valuation.json** (centred on 1.6%): WACC 6.10-8.10% x terminal growth 1.1/1.6/2.1/2.6%. The centre cell is 3,855p; the range runs from 3,254p to 5,296p.

## [Superseded 15 Oct 2026] Sanity checks (sanity_checks.json `checks`)
| Check | Result | |
|---|---|---|
| Terminal value share of EV | **75.7%** | **FLAG (above 75%, just)**: down from 76.6% at the higher discount rate |
| Implied exit EV/EBITDA (TV / FY30 EBITDA) | **10.9x** | Within the peer range 9.3x-21.2x, below the peer median of 11.9x. OK |
| WACC within 6-9% | **7.10%** | OK. Not changed |
| DCF vs comps | DCF 3,855p vs comps median **3,911p** (range 3,166-6,541p) | DCF **1.4% below** comps. Close agreement |

## [Superseded 15 Oct 2026] Comps (comps.csv, comps.json)
- **Method (unchanged).** EV/EBITDA LTM, median of the 7 core peers. Every peer's LTM ends 30 Jun 2026 (P&G: its own fiscal year). Restating the peers onto December would need their H2 2025 figures, which are not in peers.csv (MISSING). So `calendarise` puts Unilever's ex-perimeter EBITDA on the same 12 months to June 2026 (6/12 FY25 + 6/12 FY26). Forward P/E is calendarised to December 2027.
- **Unilever metric:** EBITDA of the business that **remains**, on the PM basis (17.7% margin after recurring restructuring + 2.6% D&A), calendarised = **EUR 8,100m** (underlying variant 8,540m).
- **Same bridge items as the DCF, so the two are comparable.** Median multiple x EBITDA gives the EV of the remaining business. Then: minorities proportionately (10.684% x EV), the EUR 500m restructuring, the same associates/stakes (now 7,062) and the same Foods consideration (33,955). A market multiple prices the company **today**, so there is no growth at Ke, and net debt is the latest reported (**25,961 at 30 Jun 2026**, H1 2026 6-K) less the Q2 dividend paid after June (1,004.8). A low-bound variant at the DCF's dates gives 3,885p.

| Peer set | Median EV/EBITDA | Value per share, pence (low / median / high) |
|---|---|---|
| All 7 (primary) | 11.9x | 3,166 / **3,911** / 6,541 |
| ex KMB (Kenvue deal) | 14.2x | 3,166 / 4,579 / 6,541 |
| ex CL (Filorga impairment) | 11.9x | 3,166 / 3,905 / 6,541 |
| ex KMB and CL | 11.9x | 3,166 / 3,911 / 6,541 |
| All 7 x underlying EBITDA | 11.9x | 3,310 / 4,095 / 6,868 |

- Without KMB the median becomes the average of Reckitt 11.9x and P&G 16.6x (14.2x). The middle of this peer set is thin.
- **Unilever's own market multiple:** at 4,710.5p, after taking out the Foods consideration and the stakes at the DCF's values, the market pays **14.7x** EBITDA for the business that remains. Peer median 11.9x; DCF exit 10.9x.
- **Hindustan Unilever (optional, shown separately):** 29.3x EV/EBITDA, 36.2x forward P/E. Brief note: Unilever's 62%-owned Indian subsidiary, not in any median. It is already inside the consolidated DCF, with the 38.1% outside holders deducted as minorities.
- **P/E and FCF yield:** peer medians only (forward P/E to Dec 2027: 20.0x; LTM FCF yield 4.8%). No Unilever-side metric for the remaining business. EV/EBITDA NTM is MISSING.

## [Superseded 15 Oct 2026] Sizes the PM asked for (base case NOT changed; all on the decision 11 inputs)
**(a) Foods consideration received at closing (about 0.71 years, 30 Jun 2027) vs today's value (EUR 33,955m).**
| Discounting | PV, EUR m | Reduction |
|---|---|---|
| Cash part only (USD 15.7bn = EUR 14,027m) at 4.15% (Bund + A spread) | 13,628 | EUR 399m = **16p** |
| Whole consideration at WACC 7.10% | 32,343 | EUR 1,613m = 63p |
| Whole consideration at Ke 7.872% (upper bound) | 32,178 | EUR 1,778m = 70p |
Each 1 point of discount rate on the whole amount = **9.4p**. The cash-only line is the most defensible size: the McCormick share price today already is today's value of receiving the shares at closing, less McCormick dividends before closing (MISSING). **Offset:** Foods' own cash flows from 1 Jan 2026 to closing belong to Unilever but are outside the DCF. MISSING; the Data agent's rough indicator is about EUR 2.9bn (about 113p) before capex and working capital.

**(b) Tax on the Foods cash: each EUR 1bn = 39.3p a share** (38.2p if paid at closing and discounted). The bear's 25% of the cash = EUR 3,507m = **138p**. If a tax figure is entered in the bridge, it should also be counted in `priced_at_valuation_date` (a today amount). Otherwise the engine grows it to 41.7p per EUR 1bn.

**(c) Beta.** The JV value is recomputed at each cost of equity (Gordon growth, 229 x 1.016 / (Ke - 1.6%)); risk-free 3.45%; the debt weight is unchanged.
| Beta | Ke | WACC | JV value | EV | Value | Upside | Rating |
|---|---|---|---|---|---|---|---|
| 0.8844 bottom-up (base) | 7.87% | 7.10% | 3,710 | 91,140 | **3,855p** | -18.2% | SELL |
| 0.91 own 5y monthly | 8.00% | 7.20% | 3,635 | 89,462 | **3,792p** | -19.5% | SELL |
| 0.54 own 5y weekly | 6.15% | 5.65% | 5,114 | 122,348 | **5,027p** | +6.7% | HOLD |
At beta 0.54 the WACC (5.65%) is below the 6-9% check range and the TV share is 81%. Without recomputing the JV the 0.54 case would be 4,970p; the JV link is worth about 58p.

**(d) Where the 3,855p comes from** (31 Dec items grown at Ke; Foods and TMICC at today's value, not grown):
| Component | Pence | Share of value |
|---|---|---|
| DCF of the remaining business (EV 3,799p) less minorities (-406p) | **3,393p** | **88%** |
| Foods consideration | **1,334p** | **35%** |
| Other non-operating: JVs 155p, TMICC 76p, investments/associates/Magnum balance 59p | **290p** | **8%** |
| Net debt -962p, restructuring -21p, dividends since Dec -119p, buyback -59p | **-1,161p** | **-30%** |
Non-operating assets together (1,623p) are **42%** of the value per share; the Foods consideration alone is about a third.

**(e) Flip points** (one variable at a time; SELL to HOLD at 4,239p, HOLD to BUY at 5,417p; JV recomputed where the cost of equity or growth moves):
| Variable (base) | HOLD at | BUY at |
|---|---|---|
| Beta, JV consistent (0.8844) | 0.748 | 0.462 |
| WACC (7.10%) | 6.52% (-0.58 pt) | 5.32% (-1.78 pt) |
| Terminal growth (1.6%) | 2.50% | 4.05% |
| FY27-30 and terminal growth together (1.6%) | 2.30% | 3.70% |
| Operating margin (17.7%) | 19.7% | 25.8% |
| McCormick share price (USD 44.64) | USD 66.55 (+49%) | USD 133.72 |
| Extra value today (or less tax / fewer claims) | EUR 9.8bn | EUR 39.8bn |
The SELL is now well inside its band. HOLD needs a WACC about 0.6 points lower, a beta of 0.75 or below, or a margin of 19.7%. The WACC level at which the call flips (6.52%) is unchanged, because the call depends on the WACC level, not on how the WACC is built.

## [Superseded 15 Oct 2026] FLAGs
1. ~~**The roll-forward grew run-date market values (about 84p).**~~ **RESOLVED** (commit 3414aec, mistakes log row 24). The engine's equity equals a hand-built roll-forward (98,163). On today's inputs the fix is worth -86.5p (the old engine would give 3,942p).
2. **TV share 75.7% > 75%** (marginal).
3. **Risk-free source (decision 11).** 3.45% comes from a data aggregator (Trading Economics/Bloomberg page), not a primary source. The PM flagged this, and it is noted here. Each +0.1 point on the risk-free rate moves both the cost of equity and the cost of debt. From 3.18% to 3.45% (+0.27 pt) the value fell 163p (4,018p to 3,855p, including the JV re-valuation).
4. **Beta is still the main swing factor.** The own 5y weekly beta (0.54) gives HOLD at 5,027p; the bottom-up 0.88 gives SELL at 3,855p. The PM rule is followed. See the Risk agent FLAG 1.
5. **Bear case and sensitivity grids hold the JV value at the base cost of equity.** If the bear's +1 point also applies to Ke, the JV value falls from 3,710 to 3,199 (-20p). For the Bear agent.
6. ~~**Grid not centred on 1.6%.**~~ **RESOLVED** (commit 3414aec).
7. **Foods timing and interim cash flows** (see (a)): -16p to -70p vs +about 113p (MISSING, indicator only). **Tax on the Foods cash** MISSING, not deducted: each EUR 1bn = 39p.
8. **WACC uses pre-sale leverage.** The debt weight (16.1%) and the relevered beta use 31 Dec 2025 net debt. After closing, the cash cuts net debt while the Foods earnings leave. Not sized.
9. **Comps data:** peers.csv labels Reckitt's currency "GBP", but its price (5,258) is in pence. It is converted with `desk.units.pence_to_pounds` for the forward P/E (14.6x, not 1,459x). Four of the seven peers' figures come from Yahoo. KMB and CL are distorted (shown with and without). The ex-perimeter D&A is not disclosed (the PM's 2.6% is used). The 30 Jun net debt includes the Foods perimeter's H1 cash.
10. **Magnum transition balance (+500) is a 31 Dec figure.** Part may already be in June net debt, so the comps bridge may double count a small amount (under 20p).

## [Superseded 15 Oct 2026] For the PM (disagreements; nothing changed)
- No remaining objection to the mechanics.
- With the run-date Bund the SELL is firmer (-18.2%, 384p from HOLD). Only the low own-regression betas (0.43-0.54) give HOLD; nothing in the evidence gives BUY. I would present it as "SELL" with the beta table and flip points in the memo.

## [Superseded 15 Oct 2026] Missing
Tax on the Foods cash; Foods perimeter cash flows to closing; McCormick dividends before closing; NTM EBITDA for all peers; peers' H2 2025 figures (for a December calendarisation); Unilever forward EPS and FCF for the remaining business; ex-perimeter D&A; a primary-source run-date Bund yield.

## [Superseded 15 Oct 2026] Confidence
**High on the mechanics.** Excel matches Python, the hand-built roll-forward matches the engine, and the decomposition and flip points re-check to the base value.
**Medium on the value.** Three quarters of EV is terminal value, a third of the value per share is the untaxed Foods consideration at today's market price, and the risk-free rate comes from an aggregator.
**Comps: medium-low.** The median is thin and four of the seven peers use Yahoo data. They agree with the DCF within 1.5%.
