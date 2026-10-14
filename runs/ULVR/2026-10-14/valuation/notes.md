# Valuation agent notes: Unilever PLC (ULVR), run 2026-10-14 (second run, corrected engine)

Units: money in EUR m (Unilever reports in euros). Value per share in pence (GBp, the London price) and EUR. EUR 1.18190 per GBP (FRED, 9 Oct 2026). 2,154.3m shares. Price 4,710.5p (ULVR.L close 13 Oct 2026).

**Why a second run:** the first run's FLAG 1 (the roll-forward grew run-date market values) and FLAG 5 (the grid was not centred on 1.6%) were fixed in desk/ (commit 3414aec, tests pass; mistakes log row 24). `inputs.yaml` now has `priced_at_valuation_date_meur` = 35,890.5 (TMICC 1,935.2 + Foods consideration 33,955.3), and the brief lists it. Every output in this folder was regenerated. **Value: 4,101p before the fix, 4,018p now (-84p, exactly the size reported in the first run). Still SELL.**

## What I did
1. **Input check:** every value in `../inputs.yaml` has a source, including `beta` 0.8844, `minority_share_of_operating_profit` 0.10684 and the new `priced_at_valuation_date_meur`. The engine's loader found nothing missing. `foods_perimeter_interim_cash_flows_meur` is null; it is informational and MISSING (sized below). I checked that 35,890.5 = TMICC + Foods consideration recomputed (35,890.51; the difference is TMICC rounded to 0.1).
2. **Engine:** `python -m desk.valuation_run briefs/ULVR.yaml runs/ULVR/2026-10-14/inputs.yaml runs/ULVR/2026-10-14/valuation` wrote `valuation.json` and `dcf.xlsx`. I recalculated `dcf.xlsx` in LibreOffice. Every line matches Python, with a largest relative difference of 8e-11 (tolerance 2%). That includes the new roll-forward formula `=(equity at 31 Dec - items priced today) x (1 + Ke)^0.786 + items priced today - dividends - buybacks`.
3. **Comps:** `run_comps.py` (desk/comps.py, desk/dcf.py, desk/units.py) wrote `comps.csv` and `comps.json`.
4. **Checks and sizes:** `run_sanity.py` wrote `sanity_checks.json`. It now also checks that the engine's equity equals a roll-forward built by hand. Every variant is an in-memory copy run through `desk.valuation_run.build`. The brief and inputs.yaml were not changed.
To re-run from the repo root: `PYTHONPATH=. python runs/ULVR/2026-10-14/valuation/run_comps.py`, then `.../run_sanity.py`.

## Base case (PM assumptions unchanged)
**WACC 6.84%** = 83.87% equity x cost of equity 7.60% (Bund 3.18% + beta 0.8844 x ERP 5.0%) + 16.13% debt x after-tax cost of debt 2.87% (Bund 3.18% + A spread 0.70% = 3.88%, x (1 - 26%)).

| EUR m | FY26 | FY27 | FY28 | FY29 | FY30 |
|---|---|---|---|---|---|
| Sales (ex-Foods perimeter) | 40,002 | 40,642 | 41,292 | 41,953 | 42,624 |
| EBIT at 17.7% | 7,080 | 7,194 | 7,309 | 7,426 | 7,544 |
| Unlevered FCF | 5,043 | 5,176 | 5,259 | 5,343 | 5,429 |
| PV at 6.84% (mid-year, from 31 Dec 2025) | 4,879 | 4,687 | 4,458 | 4,239 | 4,031 |

- Terminal value (Gordon growth, g 1.6%, terminal capex 3.97% of sales so that new investment earns RONIC 17.8%): **98,544**. PV 73,173.
- **EV 95,467** = PV of FCF 22,295 + PV of TV 73,173.

| Bridge at 31 Dec 2025 | EUR m |
|---|---|
| EV | 95,467 |
| less minorities, proportionate (10.684% x EV) | -10,200 |
| less net debt (leases inside) | -23,076 |
| less one-off restructuring for stranded costs | -500 |
| plus associates, stakes and investments (TMICC 1,935 + JVs 3,876 + associates 15 + other investments 902 + net Magnum balance 500) | +7,229 |
| plus Foods consideration at today's market value (untaxed) | +33,955 |
| **Equity at 31 Dec 2025** | **102,876** |
| Roll-forward: (102,876 - 35,890.5 priced today) grown at Ke 7.60% for 0.786 years (x1.0593), + 35,890.5, - dividends gone ex 3,039, - H1 buyback 1,507 | |
| **Equity at 14 Oct 2026** | **102,302** |

**Value per share: EUR 47.49 = 4,018p.** Against 4,710.5p that is **-14.7%: SELL** (rule: SELL at -10% or worse, BUY at +15% or better). The HOLD band runs from 4,239p to 5,417p, so the base case is **222p (4.7 points) inside SELL**.
**Bear case** (FY27-30 growth 0.2%, WACC +1 pt to 7.84%): EV 76,772, **3,323p (-29.5%), SELL**.
**Sensitivity grid in valuation.json** (now centred on 1.6%): WACC 5.84-7.84% x terminal growth 1.1/1.6/2.1/2.6%; the centre cell is 4,018p. The range runs from 3,360p (WACC 7.84%, g 1.1%) to 5,665p (WACC 5.84%, g 2.6%).

## Sanity checks (sanity_checks.json `checks`)
| Check | Result | |
|---|---|---|
| Terminal value share of EV | **76.6%** | **FLAG (above 75%)**: three quarters of EV depends on the years after 2030 |
| Implied exit EV/EBITDA (TV / FY30 EBITDA) | **11.4x** | Within the peer range 9.3x-21.2x and just below the peer median of 11.9x. OK |
| WACC within 6-9% | **6.84%** | OK. Not changed |
| DCF vs comps | DCF 4,018p vs comps median **3,918p** (range 3,173-6,548p) | DCF **2.6% above** comps. Close agreement |

## Comps (comps.csv, comps.json): unchanged by the engine fix
The comps bridge has no growth at Ke, so the fix does not affect it. Only the DCF-vs-comps gap moved.
- **Method.** EV/EBITDA LTM, median of the 7 core peers. Every peer's LTM ends 30 Jun 2026 (for P&G that is its own fiscal year). Restating the peers onto Unilever's December year would need their H2 2025 figures, which are not in peers.csv (MISSING). So `calendarise` puts Unilever's ex-perimeter EBITDA on the same 12 months to June 2026 (6/12 FY25 + 6/12 FY26). Forward P/E is calendarised onto Unilever's December year end (12 months to Dec 2027).
- **Unilever metric:** EBITDA of the business that **remains**, on the PM basis (17.7% margin after recurring restructuring + 2.6% D&A), calendarised = **EUR 8,100m**. This is comparable with the peers' unadjusted EBITDA. The underlying variant is EUR 8,540m.
- **Same bridge items as the DCF, so the two are comparable.** Median multiple x EBITDA gives the EV of the remaining business. Then: minorities proportionately (10.684% x EV), the EUR 500m restructuring, the same associates/stakes (7,229) and the same Foods consideration (33,955). A market multiple prices the company **today**, so there is no growth at Ke, and net debt is the latest reported (**25,961 at 30 Jun 2026**, H1 2026 6-K) less the Q2 dividend paid after June (1,004.8). A low-bound variant at the DCF's dates (31 Dec net debt less every dividend and buyback since, no credit for 2026 cash earned) gives 3,892p.

| Peer set | Median EV/EBITDA | Value per share, pence (low / median / high) |
|---|---|---|
| All 7 (primary) | 11.9x | 3,173 / **3,918** / 6,548 |
| ex KMB (Kenvue deal) | 14.2x | 3,173 / 4,586 / 6,548 |
| ex CL (Filorga impairment) | 11.9x | 3,173 / 3,911 / 6,548 |
| ex KMB and CL | 11.9x | 3,173 / 3,918 / 6,548 |
| All 7 x underlying EBITDA | 11.9x | 3,316 / 4,101 / 6,874 |

- Without KMB the median is the average of Reckitt 11.9x and P&G 16.6x, so it jumps to 14.2x. The middle of this peer set is thin.
- **Unilever's own market multiple:** at 4,710.5p, after taking out the Foods consideration and the stakes at the DCF's values, the market pays **14.7x** EBITDA for the business that remains. That is above the peer median (11.9x) and the DCF's exit multiple (11.4x).
- **Hindustan Unilever (optional, shown separately):** 29.3x EV/EBITDA, 36.2x forward P/E. Brief note: Unilever's 62%-owned Indian subsidiary, not in any median. It is already inside the consolidated DCF, with the 38.1% outside holders deducted as minorities.
- **P/E and FCF yield:** peer medians only (forward P/E to Dec 2027: 20.0x; LTM FCF yield 4.8%). No Unilever-side metric exists for the remaining business. EV/EBITDA NTM is MISSING.

## Sizes the PM asked for (base case NOT changed; all recomputed on the corrected engine)
**(a) Foods consideration received at closing (about 0.71 years, 30 Jun 2027) vs today's value (EUR 33,955m).** It is now correctly held at today's value in the engine (not grown).
| Discounting | PV, EUR m | Reduction |
|---|---|---|
| Cash part only (USD 15.7bn = EUR 14,027m) at 3.88% (Bund + A spread) | 13,653 | EUR 374m = **15p** |
| Whole consideration at WACC 6.84% | 32,398 | EUR 1,557m = 61p |
| Whole consideration at Ke 7.60% (upper bound) | 32,235 | EUR 1,720m = 68p |
Each 1 point of discount rate on the whole amount = **9.4p**. The cash-only line is the most defensible size: the McCormick share price today already is today's value of receiving the shares at closing, less any McCormick dividends before closing (MISSING). **Offset:** Foods' own cash flows from 1 Jan 2026 to closing belong to Unilever but are outside the DCF. MISSING; the Data agent's rough indicator is about EUR 2.9bn (about 113p) before capex and working capital.

**(b) Tax on the Foods cash: each EUR 1bn = 39.3p a share** (38.2p if paid at closing and discounted). The bear's 25% of the cash = EUR 3,507m = **138p**. If a tax figure is later entered in the bridge, it should also be counted in `priced_at_valuation_date` (it is a today amount). Otherwise the engine grows it to 41.6p per EUR 1bn.

**(c) Beta.** The JV value is recomputed at each cost of equity (Gordon growth, 229 x 1.016 / (Ke - 1.6%)); the debt weight is unchanged.
| Beta | Ke | WACC | JV value | EV | Value | Upside | Rating |
|---|---|---|---|---|---|---|---|
| 0.8844 bottom-up (base) | 7.60% | 6.84% | 3,876 | 95,467 | **4,018p** | -14.7% | SELL |
| 0.91 own 5y monthly | 7.73% | 6.95% | 3,795 | 93,621 | **3,948p** | -16.2% | SELL |
| 0.54 own 5y weekly | 5.88% | 5.39% | 5,436 | 130,442 | **5,330p** | +13.2% | HOLD |
At beta 0.54 the WACC (5.39%) is below the 6-9% check range and the TV share is 82%. Without recomputing the JV the 0.54 case would be 5,266p; the JV link is worth about 64p.

**(d) Where the 4,018p comes from** (31 Dec items grown at Ke; Foods and TMICC at today's value, not grown):
| Component | Pence | Share of value |
|---|---|---|
| DCF of the remaining business (EV 3,972p) less minorities (-424p) | **3,547p** | **88%** |
| Foods consideration | **1,334p** | **33%** |
| Other non-operating: JVs 161p, TMICC 76p, investments/associates/Magnum balance 59p | **296p** | **7%** |
| Net debt -960p, restructuring -21p, dividends since Dec -119p, buyback -59p | **-1,159p** | **-29%** |
Non-operating assets together (1,630p) are **41%** of the value per share; the Foods consideration alone is a third.

**(e) Flip points** (one variable at a time; SELL to HOLD at 4,239p, HOLD to BUY at 5,417p):
| Variable (base) | HOLD at | BUY at |
|---|---|---|
| Beta, JV consistent (0.8844) | 0.809 | 0.524 |
| WACC (6.84%) | 6.52% (-0.32 pt) | 5.32% (-1.52 pt) |
| Terminal growth (1.6%) | 2.10% | 3.70% |
| FY27-30 and terminal growth together (1.6%) | 1.99% | 3.39% |
| Operating margin (17.7%) | 18.8% | 24.6% |
| McCormick share price (USD 44.64) | USD 57.28 (+28%) | USD 124.44 |
| Extra value today (or less tax / fewer claims) | EUR 5.6bn | EUR 35.6bn |
The SELL is firmer than in the first run (222p from HOLD instead of 138p), but it is still within reach. A 0.3-point lower WACC, a beta of 0.81, or a margin of 18.8% (the ex-perimeter underlying margin before restructuring) would make it HOLD. BUY needs a large move.

## FLAGs
1. ~~**The roll-forward grows run-date market values once too often (about 84p).**~~ **RESOLVED** in desk/ (commit 3414aec, mistakes log row 24) with the new `priced_at_valuation_date_meur` input. `sanity_checks.json` confirms that the engine's equity equals a hand-built roll-forward (102,302) and that the input equals TMICC + Foods consideration. Value change: -83.6p, as sized in the first run.
2. **TV share 76.6% > 75%.**
3. **Beta is the swing factor.** Unilever's own 5y weekly beta (0.54) gives HOLD at 5,330p; the bottom-up 0.88 gives SELL at 4,018p. The PM rule (bottom-up) is followed. See the Risk agent FLAG 1.
4. **Bear case and sensitivity grids hold the JV value at the base cost of equity.** If the bear's +1 point also applies to Ke, the JV value falls from 3,876 to 3,323 (-22p). For the Bear agent.
5. ~~**valuation.json's sensitivity grid does not include the base growth.**~~ **RESOLVED** (commit 3414aec): growth is now 1.1/1.6/2.1/2.6%, and the centre cell equals the base case (4,018p).
6. **Foods timing and interim cash flows** (see (a)): -15p to -68p vs +about 113p (MISSING, indicator only). **Tax on the Foods cash** MISSING, not deducted: each EUR 1bn = 39p.
7. **WACC uses pre-sale leverage.** The debt weight (16.1%) and the relevered beta use 31 Dec 2025 net debt. After closing, the cash cuts net debt while the Foods earnings leave. Not sized.
8. **Comps data:** peers.csv labels Reckitt's currency "GBP", but its price (5,258) is in pence. It is converted with `desk.units.pence_to_pounds` for the forward P/E (14.6x, not 1,459x); its EV/EBITDA was already consistent. Four of the seven peers' figures come from Yahoo (not filings). KMB and CL are distorted (shown with and without). The ex-perimeter D&A is not disclosed (the PM's 2.6% is used). The 30 Jun net debt includes the Foods perimeter's H1 cash.
9. **Magnum transition balance (+500) is a 31 Dec figure.** Part may have been settled into June net debt, so the comps bridge may double count a small amount (under EUR 0.5bn, under 20p).

## For the PM (disagreements; nothing changed)
- With FLAGs 1 and 5 fixed I have no remaining objection to the mechanics.
- The rating is SELL at -14.7%. The beta evidence (own regressions 0.43-0.91) spans SELL to HOLD, and almost BUY at 0.52. I would present the call as "SELL, moderate conviction" and show the beta table and the flip points in the memo.

## Missing
Tax on the Foods cash; Foods perimeter cash flows to closing; McCormick dividends before closing; NTM EBITDA for all peers; peers' H2 2025 figures (for a December calendarisation); Unilever forward EPS and FCF for the remaining business; ex-perimeter D&A.

## Confidence
**High on the mechanics.** Excel matches Python, the hand-built roll-forward matches the engine, and the decomposition and flip points re-check to the base value.
**Medium on the value.** Three quarters of EV is terminal value, a third of the value per share is the untaxed Foods consideration at today's market price, and the rating sits 222p from HOLD.
**Comps: medium-low.** The median is thin and four of the seven peers use Yahoo data. They agree with the DCF within 3%.
