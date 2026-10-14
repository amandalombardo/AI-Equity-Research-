# Valuation agent notes: Unilever PLC (ULVR), run 2026-10-14

Units: money in EUR m (Unilever reports in euros). Value per share in pence (GBp, the London price) and EUR. EUR 1.18190 per GBP (FRED, 9 Oct 2026). 2,154.3m shares. Price 4,710.5p (ULVR.L close 13 Oct 2026).

## What I did
1. **Input check:** every value in `../inputs.yaml` has a source, including `beta` 0.8844 (Risk agent) and `minority_share_of_operating_profit` 0.10684 (Fundamentals agent). The engine's loader found nothing missing. One informational key is null: `foods_perimeter_interim_cash_flows_meur`. It is MISSING, the engine does not use it, and it is sized below.
2. **Engine:** `python -m desk.valuation_run briefs/ULVR.yaml runs/ULVR/2026-10-14/inputs.yaml runs/ULVR/2026-10-14/valuation` wrote `valuation.json` and `dcf.xlsx`. I recalculated `dcf.xlsx` in LibreOffice: every formula line matches the Python value exactly (0.00% difference, against the 2% tolerance).
3. **Comps:** `run_comps.py` (desk/comps.py, desk/dcf.py, desk/units.py) wrote `comps.csv` and `comps.json`.
4. **Sanity checks and sizings:** `run_sanity.py` wrote `sanity_checks.json`. Every variant is an in-memory copy run through the same engine (`desk.valuation_run.build`). Neither the brief nor inputs.yaml was changed.
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
| grown at Ke 7.60% for 0.786 years (x1.0593), less dividends gone ex 3,039 and the H1 buyback 1,507 | |
| **Equity at 14 Oct 2026** | **104,431** |

**Value per share: EUR 48.47 = 4,101p.** Against 4,710.5p that is **-12.9%: SELL** (rule: SELL at -10% or worse, BUY at +15% or better). The HOLD band runs from 4,239p to 5,417p, so **the base case is 138p (3.4 points) inside SELL**.
**Bear case** (FY27-30 growth 0.2%, WACC +1 pt to 7.84%): EV 76,772, **3,407p (-27.7%), SELL**.

## Sanity checks (sanity_checks.json `checks`)
| Check | Result | |
|---|---|---|
| Terminal value share of EV | **76.6%** | **FLAG (above 75%)**. Driven by the low WACC and the low-growth, steady forecast. Three quarters of the value depends on the years after 2030 |
| Implied exit EV/EBITDA (TV / FY30 EBITDA) | **11.4x** | Within the peer range 9.3x-21.2x and just below the peer median of 11.9x. OK |
| WACC within 6-9% | **6.84%** | OK. Not changed |
| DCF vs comps | DCF 4,101p vs comps median **3,918p** (range 3,173-6,548p) | DCF **4.7% above** comps. Close agreement |

## Comps (comps.csv, comps.json)
- **Method.** EV/EBITDA LTM, median of the 7 core peers. All peers' LTM periods end 30 Jun 2026 (for P&G that is its own fiscal year). Restating each peer onto Unilever's December year would need their H2 2025 figures, which are not in peers.csv (MISSING). So I used `calendarise` the other way round: Unilever's ex-perimeter EBITDA is put on the same 12 months to June 2026 (6/12 FY25 + 6/12 FY26). Forward P/E is calendarised onto Unilever's December year end (12 months to Dec 2027).
- **Unilever metric:** EBITDA of the business that **remains**, on the PM basis (17.7% margin after recurring restructuring + 2.6% D&A), calendarised = **EUR 8,100m**. This matches the peers' unadjusted EBITDA, which is also after restructuring. The underlying basis, before restructuring, is EUR 8,540m and is shown as a variant.
- **Same bridge as the DCF, so the two are comparable.** Median multiple x EBITDA gives the EV of the remaining business. I then deduct minorities proportionately (10.684% x EV) and the EUR 500m restructuring, and add the same associates/stakes (7,229) and the same Foods consideration (33,955). The one difference is the date. A market multiple prices the company **today**, so there is no growth at the cost of equity, and net debt is the latest reported (**EUR 25,961m at 30 Jun 2026**, H1 2026 6-K; already after the buyback, the Q4/Q1 dividends and the cash earned in H1), less the Q2 dividend paid after June (1,004.8). A low-bound variant uses the DCF's dates: 31 Dec 2025 net debt less all dividends and buybacks since, with no credit for cash earned in 2026. It gives 3,892p.

| Peer set | Median EV/EBITDA | Value per share, pence (low / median / high) |
|---|---|---|
| All 7 (primary) | 11.9x | 3,173 / **3,918** / 6,548 |
| ex KMB | 14.2x | 3,173 / 4,586 / 6,548 |
| ex CL | 11.9x | 3,173 / 3,911 / 6,548 |
| ex KMB and CL | 11.9x | 3,173 / 3,918 / 6,548 |
| All 7 x underlying EBITDA | 11.9x | 3,316 / 4,101 / 6,874 |

- With 6 peers (ex KMB) the median is the average of Reckitt 11.9x and P&G 16.6x, so it jumps to 14.2x. That shows how thin the middle of this peer set is. Removing both distorted peers gives the same answer as all 7.
- **Unilever's own market multiple:** at 4,710.5p, after taking out the Foods consideration and the stakes at the DCF's values, the market pays **14.7x** EBITDA for the business that remains. That is above the peer median (11.9x) and the DCF's exit multiple (11.4x). Put differently, the share price assumes either a richer multiple for the remaining business or a higher value for the Foods consideration than the bridge uses.
- **Hindustan Unilever (optional, shown separately):** 29.3x EV/EBITDA, 36.2x forward P/E. Note from the brief: Unilever's 62%-owned Indian subsidiary, not in any median. It is already inside the consolidated DCF, with the 38.1% outside holders deducted as minorities.
- **P/E and FCF yield:** the peer medians are shown (forward P/E to Dec 2027: 20.0x; LTM FCF yield 4.8%). There is no Unilever-side metric for the remaining business (forward EPS and ex-perimeter FCF are not available), so no implied value. EV/EBITDA NTM is MISSING (no NTM EBITDA consensus).

## Sizes the PM asked for (base case NOT changed)
**(a) Foods consideration received at closing (about 0.71 years, 30 Jun 2027) vs today's value (EUR 33,955m).**
| Discounting | PV, EUR m | Reduction |
|---|---|---|
| Cash part only (USD 15.7bn = EUR 14,027m) at 3.88% (Bund + A spread) | 13,653 | EUR 374m = **15p** |
| Whole consideration at WACC 6.84% | 32,398 | EUR 1,557m = 61p |
| Whole consideration at Ke 7.60% (upper bound) | 32,235 | EUR 1,720m = 68p |
Each 1 point of discount rate on the whole amount = **9.4p**. The cash-only line is the most defensible size: the McCormick shares' price today already is today's value of receiving them at closing, less any McCormick dividends before closing (MISSING). **Offset:** the Foods perimeter's own cash flows from 1 Jan 2026 to closing belong to Unilever but are outside the DCF. MISSING; the Data agent's rough indicator is about EUR 2.9bn (about 113p) before capex and working capital. So the two sizes roughly offset or net positive, as the brief expected.

**(b) Tax on the Foods cash: each EUR 1bn = 39.3p a share** (38.2p if paid at closing and discounted). The bear agent's 25% of the cash = EUR 3,507m = **138p**. Through the engine's bridge line the figure is 41.6p, because the engine also grows bridge items at Ke (see FLAG 1).

**(c) Beta.** The JV value is recomputed at each cost of equity (Gordon growth, 229 x 1.016 / (Ke - 1.6%)); the debt weight is unchanged.
| Beta | Ke | WACC | JV value | EV | Value | Upside | Rating |
|---|---|---|---|---|---|---|---|
| 0.8844 bottom-up (base) | 7.60% | 6.84% | 3,876 | 95,467 | **4,101p** | -12.9% | SELL |
| 0.91 own 5y monthly | 7.73% | 6.95% | 3,795 | 93,621 | **4,033p** | -14.4% | SELL |
| 0.54 own 5y weekly | 5.88% | 5.39% | 5,436 | 130,442 | **5,395p** | +14.5% | HOLD (BUY at 0.536) |
At beta 0.54 the WACC (5.39%) falls below the 6-9% check range and the TV share rises to 82%. Without recomputing the JV the 0.54 case would be 5,331p, so the JV link is worth about 64p there.

**(d) Where the 4,101p comes from** (each 31 Dec item grown at Ke, as the engine does):
| Component | Pence | Share of value |
|---|---|---|
| DCF of the remaining business (EV 3,972p) less minorities (-424p) | **3,547p** | **86%** |
| Foods consideration | **1,413p** | **34%** |
| Other non-operating: JVs 161p, TMICC 81p, investments/associates/Magnum balance 59p | **301p** | **7%** |
| Net debt -960p, restructuring -21p, dividends since Dec -119p, buyback -59p | **-1,159p** | **-28%** |
Non-operating assets together (1,713p) are **42%** of the value per share; the Foods consideration alone is about a third.

**(e) Flip points** (one variable at a time; SELL to HOLD at 4,239p, HOLD to BUY at 5,417p):
| Variable (base) | HOLD at | BUY at |
|---|---|---|
| Beta, JV consistent (0.8844) | 0.836 | 0.536 |
| WACC (6.84%) | 6.64% (-0.20 pt) | 5.38% (-1.46 pt) |
| Terminal growth (1.6%) | 1.92% | 3.62% |
| FY27-30 and terminal growth together (1.6%) | 1.85% | 3.31% |
| Operating margin (17.7%) | 18.4% | 24.2% |
| McCormick share price (USD 44.64) | USD 52.07 (+17%) | USD 115.48 |
| Extra value today (or less tax / fewer claims) | EUR 3.5bn | EUR 33.5bn |
**The SELL is fragile.** Small changes flip it to HOLD: a 0.2-point lower WACC, a beta of 0.84 instead of 0.88, or margin 0.7 points higher. BUY needs a much larger move (for example the 5y weekly beta).

## FLAGs
1. **The roll-forward grows run-date market values once too often (about 84p).** The engine grows the whole 31 Dec 2025 equity at Ke for 0.786 years. Two items in it are already valued at 13 Oct 2026 prices: the Foods consideration (33,955) and the TMICC stake (1,935). Growing them adds EUR 2,128m = **84p** that is not there. Corrected value: **4,018p (still SELL)**. This is a consistency issue in the engine (like the buyback, mistakes row 22), not a PM assumption. Suggested fix, on a branch with tests and for Amanda's approval: add run-date-valued items after the roll-forward (or deflate them to 31 Dec). Base not changed.
2. **TV share 76.6% > 75%.**
3. **Beta is the swing factor.** Unilever's own 5y weekly beta (0.54) gives HOLD at 5,395p; the bottom-up 0.88 gives SELL. The PM rule (bottom-up) is followed. See the Risk agent FLAG 1.
4. **Bear case and sensitivity grids hold the JV value at the base cost of equity.** If the bear's +1 point also applies to Ke, the JV value falls from 3,876 to 3,323 (-22p). For the Bear agent.
5. **valuation.json's sensitivity grid does not include the base growth.** The engine hard-codes terminal growth 1.5-3.0%, so the grid's centre is not the base case. `sanity_checks.json` has a grid centred on 1.6% (WACC 5.84-7.84% x g 1.1/1.6/2.1%; centre = 4,101p). Suggest the engine centre the grid on the brief's g (code change on a branch).
6. **Foods timing and interim cash flows** (see (a)): -15p to -68p vs +about 113p (MISSING, indicator only). **Tax on the Foods cash** MISSING, not deducted: each EUR 1bn = 39p.
7. **WACC uses pre-sale leverage.** The debt weight (16.1%) and the relevered beta use 31 Dec 2025 net debt. After closing, the USD 15.7bn cash cuts net debt, while the Foods earnings leave. Not sized (it depends on how the cash is used); noted for the PM.
8. **Comps data:** peers.csv labels Reckitt's currency "GBP", but its price (5,258) is in pence. I converted it with `desk.units.pence_to_pounds` for the forward P/E (14.6x, not 1,459x). Its EV/EBITDA was already consistent. The four European peers come from Yahoo (not filings). KMB and CL are distorted (shown with and without). The ex-perimeter D&A is not disclosed, so the PM's 2.6% is used. The 30 Jun net debt includes the Foods perimeter's H1 cash.
9. **Magnum transition balance (+500) is a 31 Dec figure.** Part may have been settled in 2026; in the comps bridge, any settled amount would already be in June net debt (a possible small double count, under EUR 0.5bn = under 20p).

## For the PM (disagreements; nothing changed)
- FLAG 1 is the only item I think is wrong rather than a judgement. It overstates value by 84p. It does not change the rating, but it widens the gap to HOLD from 138p to 222p.
- The SELL sits 3.4 points from HOLD, and the beta evidence (0.43-0.91) spans SELL to almost BUY. I would present the call as "SELL, low conviction" and show the beta table in the memo.

## Missing
Tax on the Foods cash; Foods perimeter cash flows to closing; McCormick dividends before closing; NTM EBITDA for all peers; peers' H2 2025 figures (for a December calendarisation); Unilever forward EPS and FCF for the remaining business; ex-perimeter D&A.

## Confidence
High on the mechanics: Excel matches Python exactly, and the decomposition and flip points re-check to the base value. Medium on the value. Three quarters of EV is terminal value, a third of the value per share is the untaxed Foods consideration at today's market price, and the rating sits 138p from HOLD. Comps: medium-low (thin median, Yahoo data for 4 of 7 peers). They agree with the DCF within 5%.
