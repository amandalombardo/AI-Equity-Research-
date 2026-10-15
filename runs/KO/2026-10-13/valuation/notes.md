# Valuation agent notes: The Coca-Cola Company (KO), run 2026-10-13

## Re-run 15 Oct 2026 (evidence audit)

Every value per share is in **US dollars (USD)**; totals are in **USD m**. All figures come from the desk engine (`python -m desk.valuation_run`, `run_comps.py`, `run_sanity.py`). No arithmetic was done by hand. The brief and `inputs.yaml` were not edited by me.

### What changed and why
The evidence audit of 15 Oct 2026 (`docs/audit-2026-10-15/KO.md`, `docs/audit-2026-10-15/summary.md`) led to two PM decisions that change the value:
1. **Equity risk premium 5.0% -> 4.2%** (`briefs/KO.yaml`, PM decision 15 Oct 2026). Source: Damodaran's implied ERP for the S&P 500, 4.20% at 1 Oct 2026 (`docs/audit-2026-10-15/erp-evidence.md`). The 5.0% had no source. On its own: USD 47.60 -> USD 51.31.
2. **Listed stakes are no longer grown in the roll-forward** (mistakes log row 24). New input `priced_at_valuation_date_musd` = USD 39,539.5m (the listed stakes, already at 13 Oct 2026 market prices), added to `inputs.yaml` by `runs/KO/2026-10-13/apply_audit_fixes_2026-10-15.py`. On its own: USD 47.60 -> USD 47.01.
3. The brief also now has `scenarios.bear.bear_agent_margin` 0.319. It is for the Bear agent's stacked case, **not** the engine, so the engine's bear case below still uses the 33.2% base margin. For information only, I also ran the engine's bear case at 31.9% (table below).

Both changes together: **USD 50.76, SELL** (matches the expected figure).

Input check: every value in `inputs.yaml` has a source, including `beta` 0.6091 (Risk agent) and the new `priced_at_valuation_date_musd`.

### Old vs new key numbers
| item | 13 Oct 2026 (old) | 15 Oct 2026 (new) |
|---|---|---|
| Risk-free (FRED DGS10, 8 Oct 2026) | 5.22% | 5.22% |
| Beta | 0.6091 | 0.6091 |
| Equity risk premium | 5.0% (unsourced) | **4.2%** (Damodaran implied) |
| **Cost of equity** | 8.27% | **7.78%** |
| Cost of debt, pre-tax / after 23.7% tax | 5.91% / 4.51% | 5.91% / 4.51% |
| Weights equity / debt | 92.9% / 7.1% | 92.9% / 7.1% |
| **WACC** | 8.00% | **7.55%** |
| PV of forecast cash flows (USD m) | 49,363 | 49,864 |
| PV of terminal value (USD m) | 149,092 | 164,337 |
| **Enterprise value at 31 Dec 2025 (USD m)** | 198,455 | **214,201** |
| Bridge (USD m, unchanged): net debt -29,686; leases -1,722; minorities -2,106; IRS -14,000; stakes +46,626; CCBA proceeds +1,300 | same | same |
| Equity value at 31 Dec 2025 (USD m) | 198,867 | 214,613 |
| Equity value at 13 Oct 2026 (USD m), after USD 6,840m dividends | 204,794 (everything grown at 8.27%) | **218,356** (listed stakes USD 39,540m not grown; rest grown at 7.78%) |
| Shares | 4,302m | 4,302m |
| **Value per share** | USD 47.60 | **USD 50.76** |
| Price (Yahoo, 13 Oct 2026) | USD 90.12 | USD 90.12 |
| **Upside** | -47.2% | **-43.7%** |
| **Rating** | SELL | **SELL** |
| Bear case, engine (growth 1% FY27-30, WACC +1 point, margin 33.2%) | USD 37.99 (-57.8%), WACC 9.00%, EV USD 159,609m | **USD 39.91 (-55.7%)**, WACC 8.55%, EV USD 170,191m |
| Bear case, engine, at PM bear margin 31.9% (information only) | not run (audit: USD 36.48) | USD 38.25 (-57.6%), SELL |
| **Terminal value share of EV** | 75.1% (FLAG) | **76.7% (FLAG)** |
| **Implied exit EV/EBITDA** | 11.1x (below peers: FLAG) | **12.0x** (inside the peer range 11.4x to 29.1x) |
| **Market-implied WACC** (WACC at which the DCF equals USD 90.12) | 5.17% | **5.14%** |
| DCF vs comps median (USD 70.07) | -32.1% | -27.6% |
| Sensitivity grid (WACC +/-1 point x g 1.5-3.0%) | USD 39.19 to USD 66.93, all SELL | **USD 41.02 to USD 74.59, all SELL** |

The 13 Oct notes said the market price implies a WACC of "about 5.5%". That was the WACC at which the rating turns HOLD (5.52%), not the WACC that gives USD 90.12. The correct market-implied figure was 5.17% then and is 5.14% now. It fell slightly because not growing the stakes lowers the value.

### Breakevens (one variable at a time, everything else at base)
HOLD needs a value of at least USD 81.11 (USD 90.12 x 0.90). BUY needs at least USD 103.64 (x 1.15).

| variable (base) | SELL to HOLD, old -> new | HOLD to BUY, old -> new |
|---|---|---|
| beta (0.6091) | 0.061 -> **0.068** | -0.104 -> **-0.126** (not economically possible) |
| WACC (7.55%) | 5.52% -> **5.49%** | 4.76% -> **4.73%** |
| terminal growth (2.0%) | 5.17% -> **4.64%** | 5.91% -> **5.40%** |
| operating margin (33.2%) | 55.5% -> **52.0%** | 70.5% -> **66.0%** |

No reasonable single change takes KO out of SELL.

### IRS case sensitivity (engine runs on scratch copies, `scratch/scenario_irs_*`)
Why: the audit found that the memo leaves out the 8th Circuit's reversal of the 3M Tax Court decision (1 Oct 2025, the same blocked-income rule). KO's FY25 10-K calls that ruling "highly supportive". The 11th Circuit heard KO's appeal on 25 Jun 2026, and its ruling is pending.

| case | IRS liability deducted | 2007-09 deposit refunded | tax rate | value per share | upside | rating |
|---|---|---|---|---|---|---|
| **KO loses (base, PM decision)** | USD 14,000m | 0 | 23.7% | **USD 50.76** | -43.7% | SELL |
| Halfway (every lever at the midpoint) | USD 7,000m | USD 3,000m | 21.8% | **USD 54.48** | -39.5% | SELL |
| **KO wins** | 0 | USD 6,000m | 19.9% | **USD 58.20** | -35.4% | SELL |
| 50/50 probability-weighted (average of lose and win) | - | - | - | USD 54.48 | -39.5% | SELL |

- Win minus lose: **+USD 7.44 a share** (old basis: +USD 7.29, USD 47.60 -> USD 54.90). Even a full win is USD 22.91 short of the HOLD level of USD 81.11.
- The value is almost linear in the IRS outcome, so the halfway run and the 50/50 average agree to within USD 0.01.
- Simplifications, same as 13 Oct:
  - beta is still relevered at 23.7%;
  - the USD 385m interest receivable is not added in the win case;
  - the refunded deposit is grown in the roll-forward like the unlisted stakes.
- **For Amanda:** the IRS outcome is worth about USD 7.4 a share either way, but it cannot change the rating. Because the 3M ruling went KO's way, I would disclose it in the memo, and show at least the 50/50 figure next to the "assume lost" base.

### Sanity checks (new)
| check | result |
|---|---|
| Terminal value share of EV | **76.7%: FLAG** (above 75%; it rose because a lower WACC puts more weight on the far years) |
| Implied exit EV/EBITDA vs peers | 12.0x, **inside** the peer range (PEP 11.4x to MNST 29.1x, median 19.1x), but still at the bottom of it and far below KO's own 26.1x. The 13 Oct FLAG is cleared. |
| WACC within 6-9% | 7.55%: OK |
| DCF vs comps | DCF USD 50.76 is **27.6% below** the comps median of USD 70.07, and inside the comps range (USD 42.01 to USD 107.05) |

### Other scenarios (not the base case; new run)
- **Beta from Damodaran's 2022-26 average (0.8684):** USD 43.10 (-52.2%), SELL. WACC 8.56%, EV USD 182,005m. Old figure: USD 40.01.
- **Engine bear at 31.9% margin:** USD 38.25 (see the table above). The Bear agent's stacked case remains the reference figure.

### Excel check
I recalculated `dcf.xlsx` (live formulas) in LibreOffice and compared every line of the "Valuation" block with the Python column. All 13 lines match. The largest difference is 1e-10 relative, on the upside line, where the Python figure is rounded. Value per share: USD 50.7568 in Excel, USD 50.7568 in Python.

### Comps
Peer multiples and implied values are unchanged: they use neither the WACC nor the roll-forward. The low / median / high are still USD 42.01 / USD 70.07 / USD 107.05, which is -22.2% at the median. `comps.json` was regenerated. Only `dcf_value_usd` (USD 50.76) and `dcf_vs_comps_median` (-27.6%) changed.

### FLAGs (15 Oct 2026)
1. **The ERP of 4.2% was seen in search summaries only** (Damodaran's site is blocked here). PM to confirm it on Damodaran's home page.
2. **TV share is 76.7% (> 75%).** It is higher than on 13 Oct.
3. **The DCF value is still far below both the comps median and the price.** The gap is driven by the discount rate: the WACC of 7.55% compares with a market-implied 5.14%.
4. **The engine's bear case ignores the PM's 31.9% bear margin by design.** The field is for the Bear agent. The memo's bear figure must come from the Bear agent's re-run, not from `valuation.json`.
5. **IRS:** the base case assumes a full loss. See the sensitivity table above (USD 50.76 / USD 54.48 / USD 58.20).
6. **Not re-run here:** the other audit findings that the PM has not yet decided are still open. They are FY26 growth (-USD 0.47), the CCBA 25% stake at USD 783m (-USD 0.02), the margin denominator (+USD 0.13) and the risk-free 13 Oct print (+USD 0.07).
7. **Tests:** I changed no code in `desk/`. `run_sanity.py` (in this folder) gained the IRS halfway case, the market-implied WACC and the information-only bear-margin run. `python -m pytest` could not be run in this environment because pytest is not installed.

### Confidence
- **High** that the engine applied the new inputs correctly: the Excel matches Python, and the result matches the expected USD 50.76.
- The SELL rating is robust to every single-variable change tested and to either IRS outcome.

### Files
`valuation.json`, `dcf.xlsx`, `comps.json` (`comps.csv` unchanged), `sanity_checks.json`, `run_sanity.py`, `scratch/` (scenario copies only).

---

# Original run, 13 Oct 2026 (kept for the record; superseded figures marked)

Every value per share is in **US dollars (USD)**. Totals are in **USD m**. KO trades on the NYSE in USD, so there is no ADR and no pence conversion. All figures come from the desk engine (`desk/dcf.py`, `desk/comps.py`) through the scripts in this folder. None of the arithmetic was done by hand.

## What I did
1. **Input check.** I checked `inputs.yaml`. Every required value is present and has a source, including `beta` 0.6091 from the Risk agent (Damodaran US Beverage (Soft) unlevered 0.5755, relevered at x1.0584). Note that `data/notes.md` is older than the PM's later decisions in `apply_pm_ccba_decision.py` and `apply_pm_audit_fixes.py` (base sales ex-CCBA, associates at run-date market value, contingent 14,000), so `inputs.yaml` is the version I relied on.
2. **Engine run.** I ran `python -m desk.valuation_run briefs/KO.yaml runs/KO/2026-10-13/inputs.yaml runs/KO/2026-10-13/valuation`. It produced `valuation.json` and `dcf.xlsx` (live formulas).
3. **Comps.** `run_comps.py` produced `comps.csv` and `comps.json`.
4. **Sanity checks, flip points and scenarios.** `run_sanity.py` produced `sanity_checks.json`. Each variant is run on a scratch copy in `scratch/`. The brief and `inputs.yaml` were never edited.

## Base case (PM assumptions): superseded 15 Oct 2026 (see the re-run section at the top)
| item | value |
|---|---|
| **Value per share** | **$47.60** vs price $90.12 (Yahoo, 13 Oct 2026) |
| Upside | **-47.2%** |
| **Rating** | **SELL** (the rule is SELL at -10% or worse, BUY at +15% or better) |
| Cost of equity | 5.22% risk-free + 0.6091 x 5.0% equity risk premium = 8.27% |
| Cost of debt | 5.22% + 0.69% spread = 5.91% pre-tax, 4.51% after 23.7% tax |
| Weights | equity 92.9% / debt 7.1% |
| **WACC** | **8.00%** |
| Enterprise value at 31 Dec 2025 | 198,455 |
| PV of forecast cash flows / PV of terminal value | 49,363 / 149,092 (TV is 75.1% of EV) |
| Bridge: less net debt | -29,686 |
| Bridge: less operating leases | -1,722 |
| Bridge: less minorities at book | -2,106 |
| Bridge: less IRS liability | -14,000 |
| Bridge: plus equity stakes at market | +46,626 |
| Bridge: plus CCBA sale proceeds | +1,300 |
| Bridge: pension and restructuring | 0 |
| Equity value at 31 Dec 2025 | 198,867 |
| Rolled forward to 13 Oct 2026 | x(1.0827)^0.784 less 6,840 of dividends = 204,794 |
| Shares | 4,302m |
| Implied exit EV/EBITDA | 11.1x |
| Terminal capex | 4.76% of sales (set so new investment earns the brief's 27% RONIC) |
| **Bear case** (brief: growth 1% from FY27, WACC +1 pt = 9.0%) | **$37.99** (-57.8%), SELL. EV 159,609 |

The WACC x terminal growth sensitivity grid is in `valuation.json`. It runs from $39.19 (WACC 9.0%, g 1.5%) to $66.93 (WACC 7.0%, g 3.0%). **Every cell is a SELL.**

## Comps (cross-check): peer multiples and implied values still current; only the DCF comparison is superseded 15 Oct 2026
- **Peers:** PEP, KDP and MNST all have December year ends, like KO. `calendarise()` is therefore the identity: no time-weighting is needed.
- **Multiples used:** EV/EBITDA NTM is MISSING (there is no NTM EBITDA consensus), so the comps use EV/EBITDA LTM. EV = market cap + net debt + minorities, excluding leases.
  - PEP 11.4x
  - KDP 19.1x
  - MNST 29.1x
  - **median 19.1x**
- **KO metric:** FY25 comparable EBITDA ex-CCBA = 15,013 - CCBA EBIT 266 + D&A 1,050 = 15,797.
  - I removed CCBA because the bridge already adds the CCBA sale proceeds and the retained 25% stake. Leaving CCBA's EBITDA in would count it twice.
  - The implied EV goes through the same bridge as the DCF, but **without** the roll-forward, because market multiples already price the company today.
- **Implied value: $42.01 / $70.07 / $107.05** (low / median / high). The median is -22% vs the price.

| Variant (USD per share) | low | median | high |
|---|---|---|---|
| **Primary: EV/EBITDA LTM x comparable ex-CCBA** | **42.01** | **70.07** | **107.05** |
| Excluding KDP (median 20.3x) | 42.01 | 74.53 | 107.05 |
| x comparable incl. CCBA (16,063; double counts CCBA) | 42.72 | 71.25 | 108.86 |
| x GAAP EBITDA (14,812; same basis as peers) | 39.40 | 65.71 | 100.39 |
| **Forward P/E x KO forward EPS** | MISSING | MISSING | MISSING |
| Cross-check: GAAP P/E LTM (median 31.2x) x KO FY25 GAAP EPS $3.05 | 48.31 | 95.09 | 122.04 |
| Cross-check: forward P/E (median 14.7x) x FY25 comparable EPS $3.00 (mismatched basis) | 39.61 | 44.20 | 102.54 |

- **Forward P/E leg is MISSING.** The data folder has no KO forward EPS consensus (only FY25 comparable EPS of $3.00), so I did not estimate one. The peer forward P/E median is 14.7x (PEP).
- **KO's own multiples at $90.12:**
  - EV/EBITDA LTM 26.1x (comparable) / 28.3x (GAAP)
  - P/E 29.6x (GAAP) / 30.0x (comparable)
- **Optional peers, shown separately:**
  - **CCEP** (bottler, lower margin): MISSING. There are no XBRL companyfacts and its site is blocked.
  - **DEO** (out-of-sector cross-check; June year end, not calendarised): P/E LTM 13.4x, from `runs/DGE/2026-10-12/valuation/comps.json`. EV/EBITDA is not available.

## Sanity checks: superseded 15 Oct 2026
| check | result |
|---|---|
| Terminal value share of EV | **75.1%: FLAG** (just above the 75% limit) |
| Implied exit EV/EBITDA vs peers | **11.1x, below the peer range of 11.4x to 29.1x (median 19.1x): FLAG.** KO itself trades at 26.1x |
| WACC within 6-9% | 8.00%: OK |
| DCF vs comps | DCF $47.60 is **32% below** the comps median of $70.07, though inside the comps range ($42.01 to $107.05) |

## Where the rating flips (one variable at a time, everything else at base): superseded 15 Oct 2026
The value needed is at least $81.11 for HOLD and at least $103.64 for BUY.

| variable (base) | SELL to HOLD at | HOLD to BUY at |
|---|---|---|
| beta (0.6091) | 0.061 | -0.104 (not economically possible) |
| WACC (8.00%) | 5.52% | 4.76% |
| terminal growth (2.0%) | 5.17% | 5.91% |
| operating margin (33.2%) | 55.5% | 70.5% |

**In plain terms:** no reasonable change to any single assumption takes KO out of SELL. On the PM's assumptions, the market price implies something like a WACC of about 5.5%, or perpetual growth of about 5%.

## Scenarios (these are NOT the base case): superseded 15 Oct 2026
- **Beta from Damodaran's 2022-26 average soft-beverage unlevered beta.**
  - The unlevered 0.820485 x 1.0584 gives a beta of 0.8684, a cost of equity of 9.56% and a WACC of 9.20%.
  - Result: **$40.01 (-55.6%), SELL.** EV 166,190, TV 71.1% of EV, exit 9.3x.
  - On this beta the WACC is **above the 9% check range**.
- **KO WINS the IRS case.**
  - Contingent liability 0, the $6,000m deposit refunded (added with the stakes, so associates become 52,626), and a tax rate of 19.9%. Beta is left at 0.6091.
  - Result: **$54.90 (-39.1%), SELL.** WACC 8.01%, EV 207,941, TV 75.0%, exit 11.6x.
  - Not included: the $385m interest receivable, and relevering beta at 19.9% (both small).

## FLAGs (13 Oct; 1 to 3 superseded 15 Oct 2026, 4 to 8 still apply)
1. **TV share 75.1% > 75%.** Most of the value sits in the terminal value.
2. **Exit multiple 11.1x is below every peer** (PEP 11.4x is the lowest) and far below KO's own 26.1x. The DCF prices KO like a slower, lower-quality business than the market does.
3. **DCF is 32% below comps, and both are below the price.** The DCF gives -47%, the comps median -22%.
4. **KDP's LTM EV/EBITDA is distorted.** The JDE Peet's acquisition is fully in EV (debt and NCI) but only about a quarter of it is in EBITDA. KDP also happens to be the median of the three. Without KDP the median is 20.3x and the value $74.53.
5. **MNST split checked.** The 2-for-1 split on 11 Aug 2026 is handled: shares used are 1,959.1m = 979.5m x 2. That is consistent with the post-split price ($43.51) and EPS consensus ($1.273), and the market cap ties to `peers.csv` within 0.05%.
6. **KO forward EPS is MISSING.** The forward P/E leg is not computed. **EV/EBITDA NTM is MISSING** for all peers. **CCEP is MISSING.**
7. **Basis mismatches in comps:**
   - Peer EBITDA is GAAP, while KO's is comparable. The GAAP variant is shown above.
   - KO's LTM is FY25 (to Dec 2025), while peers' LTM ends Jun/Sep 2026.
   - CCBA's D&A is not disclosed, so ex-CCBA EBITDA removes only CCBA's EBIT.
8. **Upstream flags carried forward:**
   - The CCBA figures come from Coca-Cola HBC's announcement, seen via web search and not verified (PM asked to verify).
   - Minorities of 2,106 include CCBA's outside shareholder (up to about $1.1bn deducted too much, roughly $0.26 per share).
   - The equity stakes are rolled forward from 31 Dec 2025 fair values using price and FX changes, not actual run-date holdings.

## For Amanda: assumptions I would question (13 Oct; the numbers in the first point are superseded 15 Oct 2026)
- **Discount rate vs market.** The 5.22% risk-free rate plus the 5.0% ERP gives a cost of equity of 8.27% for a stock whose own regressions show a beta of 0.1-0.35. The market price is consistent with a WACC of about 5.5%. The rating is driven almost entirely by this. It is worth deciding whether the 8.0% WACC, or the 2% perpetual growth for a business with 4-5% organic growth guidance, is the view you want to stand behind.
- **Capex 4.4% of sales includes CCBA**, a capital-heavy bottler, but the base sales exclude it. Ex-CCBA capex intensity is probably lower, and that would raise the value. D&A (2.68%, the FY21-25 average) is above FY25's 2.19% and works the other way. The two partly offset.
- **Tax 23.7% in perpetuity** assumes the Tax Court method applies forever. That is consistent with "IRS case lost", but it is a permanent 3.8-point drag on top of the 14,000 deduction.

## Confidence
- **High** that the engine and the bridge were applied correctly to the inputs.
- **Medium-low** on the comps: there are only 3 peers, KDP is distorted and the range is wide.
- The SELL rating is robust to every single-variable change tested. It depends mainly on the PM's discount rate and terminal-growth assumptions.

## Files
`valuation.json`, `dcf.xlsx`, `comps.csv`, `comps.json`, `sanity_checks.json`, `run_comps.py`, `run_sanity.py`, `scratch/` (scenario copies of the brief and inputs; not the base case)
