# Valuation agent notes: RELX PLC (RELX / REL.L), run 2026-10-14

Units: money in **GBP m** (RELX reports in pounds). Value per share in **pence (GBp)** and GBP; pence = pounds x 100, so no exchange rate is used. 1,743.754727m shares (ex treasury, 25 Sep 2026). Price **2,771p** (REL.L close 13 Oct 2026).

## What I did
1. **Checked the inputs.** All 22 values in `../inputs.yaml` have a source, including `beta` 0.9729 from the Risk agent. The engine's loader reported nothing missing. As a cross-check, debt weight 0.12818 = 7,104 / (7,104 + 48,319.4) is correct. No STOP.
2. **Ran the engine.** `python -m desk.valuation_run briefs/RELX.yaml runs/RELX/2026-10-14/inputs.yaml runs/RELX/2026-10-14/valuation` wrote `valuation.json` (base, bear, sensitivity grid, rating) and `dcf.xlsx`. It used the new pound-reporter path: no FX input, and the workbook's "GBP per GBP" cell is 1.
3. **Checked the Excel.** I recalculated `dcf.xlsx` in LibreOffice and compared all **74** formula cells with Python: every forecast line for every year, plus WACC through to upside. The largest relative difference is **6e-11**, against a 2% tolerance. Pass.
4. **Built the comps.** `run_comps.py` uses `desk.comps.calendarise` and `implied_values`, and writes `comps.csv` and `comps.json`.
5. **Ran the checks.** `run_sanity.py` writes `sanity_checks.json`. It covers the sanity checks, the flip points, value per 1 point, beta card vs run, and the Excel check.

I did not change the brief, inputs.yaml or `desk/`. To re-run from the repo root: the engine command above, then `PYTHONPATH=. python runs/RELX/2026-10-14/valuation/run_comps.py`, then `.../run_sanity.py`.

## Key numbers (base case, PM assumptions unchanged)
| Item | Value |
|---|---|
| Base sales FY25 (incl. print 399) | GBP 9,590m |
| Operating margin (flat, H1 2026 ex print) | 35.0% |
| Tax rate | 22.8% |
| Risk-free (UK 10y gilt, 13 Oct 2026) | 5.45% |
| Beta (bottom-up, relevered ex leases) | 0.9729 |
| Equity risk premium | 5.0% |
| Cost of equity = 5.45% + 0.9729 x 5.0% | **10.31%** |
| Pre-tax cost of debt = gilt 5.45% + A spread 0.70% | 6.15% (historic 3.9% for reference only) |
| After-tax cost of debt = 6.15% x (1 - 22.8%) | 4.75% |
| Weights: equity / debt (market) | 87.18% / 12.82% |
| **WACC** | **9.60%** |
| Terminal growth / terminal RONIC | 2.0% / 15.4% (terminal capex 8.88% of sales) |

| GBP m | FY26 | FY27 | FY28 | FY29 | FY30 |
|---|---|---|---|---|---|
| Growth | 3.0% | 5.0% | 5.0% | 5.0% | 5.0% |
| Sales | 9,877.7 | 10,371.6 | 10,890.2 | 11,434.7 | 12,006.4 |
| EBIT at 35.0% | 3,457.2 | 3,630.1 | 3,811.6 | 4,002.1 | 4,202.2 |
| NOPAT | 2,669.0 | 2,802.4 | 2,942.5 | 3,089.6 | 3,244.1 |
| + D&A 5.07% | 500.8 | 525.8 | 552.1 | 579.7 | 608.7 |
| - Capex 7.10% | 701.3 | 736.4 | 773.2 | 811.9 | 852.5 |
| - Increase in NWC (negative NWC, so cash comes in) | -44.7 | -76.7 | -80.5 | -84.5 | -88.8 |
| **Unlevered FCF** | **2,513.1** | **2,668.5** | **2,802.0** | **2,942.1** | **3,089.2** |
| PV at 9.60% (mid-year, from 31 Dec 2025) | 2,400.5 | 2,325.7 | 2,228.1 | 2,134.5 | 2,044.9 |

| Item | Value |
|---|---|
| Sum of PV of FCF | GBP 11,133.7m |
| Terminal-year FCF (FY31, normalised) | GBP 2,879.3m |
| **Terminal value** (Gordon growth, end FY30) | **GBP 37,880.4m**; PV 25,075.5 |
| **Enterprise value** (31 Dec 2025) | **GBP 36,209.2m** (9.4x FY25 adjusted EBITDA) |
| less net debt ex leases / minorities, plus investments | -7,104 / -24 / +131 |
| Equity at 31 Dec 2025 | GBP 29,212.2m |
| Rolled forward at Ke 10.31% for 0.7836 years, less dividends 1,217 and buybacks 2,056.2 | |
| **Equity value** (13 Oct 2026) | **GBP 28,274.7m** |
| **Value per share** | **GBP 16.21 = 1,621p** |
| Price | 2,771p |
| **Upside** | **-41.5%** |
| **Rating** | **SELL** (rule: SELL at -10% or worse; HOLD from 2,494p, BUY from 3,187p) |

- **Bear case (engine):** growth 3% every year and WACC +1 point (10.60%) give **1,244p (-55.1%), SELL**. The Bear agent's other lines (margin 33.1%, tax 25%, and the rest) are not in the engine run.
- **Sensitivity grid** (`valuation.json`): WACC 8.6-10.6% x terminal growth 1.5-3.0% gives **1,339p to 2,136p**. Every cell is SELL.
- **Where the 1,621p comes from:**
  - PV of FY26-30 cash flows: 690p
  - PV of terminal value: 1,553p
  - net debt: -440p
  - minorities: -1p
  - investments: +8p
  - dividends since December: -70p
  - buybacks since December: -118p

  The 31 Dec items are grown at Ke.

## Sanity checks (sanity_checks.json `checks`)
| Check | Result | |
|---|---|---|
| Terminal value share of EV | **69.3%** | OK (below 75%) |
| Implied exit EV/EBITDA (TV / FY30 EBITDA 4,811) | **7.9x** | **FLAG: below the whole peer range.** Peers run 11.1x (WKL) to 20.7x (MCO), median 15.7x. Informa is 13.6x. RELX trades at 14.6x today |
| WACC within 6-9% | **9.60%** | **FLAG: above 9%.** Not changed |
| DCF vs comps | DCF 1,621p vs comps median **2,990p** (range 1,955-4,111p) | **DCF 45.8% below comps** |

## Comps (comps.csv, comps.json)
- **Window.**
  - Six peers' LTM ends 30 Jun 2026; Experian's ends 31 Mar 2026 (its fiscal year).
  - Restating the peers onto RELX's December 2025 year would need their H2 2025 figures, which are not in `data/peers.csv` (MISSING).
  - So, as in the Unilever run, `calendarise` puts RELX's EBITDA on the June 2026 window: 6/12 FY25 actual 3,846 + 6/12 FY26 engine 3,958 = **3,902**.
  - Check: RELX's actual LTM to June 2026 is **3,930** (3,846 - 1,908 + 1,992, H1 2026 results p.10).
- **Forward P/E.** Calendarised onto RELX's December year: Dec 2027 for all 7 peers, Dec 2026 for 6 (Experian's FY Mar-2026 EPS is not in the CSV).
- **Bridge.** It uses the same non-operating items as the DCF (minorities 24, investments 131). There is no growth at Ke, because a market multiple prices the company today. Net debt ex leases at 30 Jun 2026 is **8,614**, plus the cash paid out after June: buybacks 306.2 and interim dividend 366.

| Leg (7 core peers, median) | Multiple | Value per share, pence (low / median / high) |
|---|---|---|
| **EV/EBITDA LTM x calendarised EBITDA 3,902 (primary)** | 15.7x | 1,955 / **2,990** / 4,111 |
| EV/EBITDA LTM x actual LTM EBITDA 3,930 | 15.7x | 1,973 / 3,015 / 4,144 |
| ex Experian (3-month offset) | 16.0x | 1,955 / 3,064 / 4,111 |
| x FY25 reported-basis EBITDA 3,779 (peers' unadjusted basis) | 15.7x | 1,877 / 2,879 / 3,965 |
| Low bound: DCF-date bridge (no credit for 2026 cash earned) | 15.7x | 1,892 / 2,927 / 4,049 |
| FCF yield LTM x RELX FY25 FCF 2,311 (secondary) | 4.61% | 1,861 / 2,875 / 4,602 |
| P/E to Dec 2027 (multiple only; RELX EPS MISSING) | 20.3x | n/a |
| P/E to Dec 2026, ex Experian (multiple only) | 22.9x | n/a |
| EV/EBITDA NTM | MISSING | no consensus |

- **Peers, EV/EBITDA LTM:** TRI 14.5x, VRSK 16.4x, SPGI 16.4x, MCO 20.7x, WKL 11.1x, EXPN 14.5x, LSEG 15.7x.
- **Informa (optional, shown separately):** 13.6x EV/EBITDA, 13.2x P/E to Dec 2027. Brief note: "exhibitions and academic publishing, show separately". It is not in any median.
- **RELX's own market multiple on the same bridge:** 14.6x actual LTM EBITDA; FY25 FCF yield 4.8%.

## Flip points (one input at a time; sanity_checks.json `flip_points`)
| Input (base) | HOLD at (2,494p) | BUY at (3,187p) |
|---|---|---|
| **WACC** (9.60%) | **7.41%** (-2.19 pt) | **6.40%** (-3.20 pt) |
| **Beta** (0.9729) | **0.449** (WACC 7.32%) | **0.214** (WACC 6.29%) |
| **Operating margin** (35.0%) | **48.4%** | **59.0%** |
| Risk-free gilt (5.45%; moves Ke and Kd) | 3.11% | 2.05% |
| Equity risk premium (5.0%) | 2.31% | 1.10% |
| Terminal growth (2.0%) | 6.08% | 7.15% |
| FY27-30 growth (5.0%) | 15.2% a year | 21.8% a year |

**The market price (2,771p) implies a WACC of 6.95%** on these cash flows. Margin and growth cannot realistically flip the call; only the discount rate can.

## Value per 1 point of each key input (pence per share; + / -)
| Input | +1 pt | -1 pt |
|---|---|---|
| WACC | -250p | +326p |
| Risk-free gilt (Ke and Kd) | -233p | +300p |
| Equity risk premium | -205p | +256p |
| Beta (per 0.10) | -111p | +124p |
| Terminal growth | +118p | -93p |
| Growth FY26-30 (each year) | +99p | -96p |
| Growth FY27-30 (each year) | +76p | -74p |
| Operating margin | +65p | -65p |
| Tax rate | -27p | +27p |
| Capex % of sales (forecast years) | -27p | +27p |
| D&A % of sales | +27p | -27p |
| Terminal RONIC | +14p | -16p |
| Debt weight (beta not relevered) | +16p | -16p |
| NWC % of sales | -1p | +1p |

## Beta: PM card 0.974 vs run 0.9729
The card used net debt **including** the 97 of leases (7,201). The brief now excludes leases (7,104), and the bridge is consistent with that, so the run uses 0.9729.

| Beta | Cost of equity | WACC | Value | Upside | Rating |
|---|---|---|---|---|---|
| 0.9729 (run) | 10.31% | 9.601% | 1,621.5p | -41.5% | SELL |
| 0.974 (card) | 10.32% | 9.606% | 1,620.2p | -41.5% | SELL |

**Difference: the card beta would give 1.3p a share less** (-0.08%). Immaterial; no effect on the rating.

Other betas from the Risk agent's evidence (cross-checks only, not used):
| Beta | Value | Rating |
|---|---|---|
| Peer median, raw (0.75) | 1,920p | SELL |
| Own 5y weekly (0.66) | 2,067p | SELL |
| Blume-adjusted 5y monthly (0.58) | 2,213p | SELL |
| Own 5y monthly (0.38; R-squared 0.04) | 2,668p | HOLD |

## FLAGs
1. **WACC 9.60% is above the 6-9% check range.** Not changed. The cause is the run-date gilt (5.45%) plus a 0.97 beta, which gives a 10.31% cost of equity. The market price implies 6.95%.
2. **Implied exit multiple 7.9x is below every peer (11.1-20.7x) and well below RELX's 14.6x today.** The DCF values RELX at 9.4x FY25 EBITDA. A long-term multiple below the lowest peer means the DCF assumes RELX deserves a lower rating than Wolters Kluwer, the cheapest peer.
3. **The DCF is 46% below comps (2,990p) and 41.5% below the price.** Even the bottom of the comps range (1,955p, WKL's 11.1x) is above the DCF. The SELL comes from the discount rate, not from the cash flows. RELX's FY26 FCF of 2,513 is a 6.9% unlevered yield on the DCF EV, against 4.4% on the market EV.
4. **The terminal RONIC rule lowers the terminal cash flow.** At 15.4%, terminal capex rises from 7.10% to 8.88% of sales, so FY31 FCF (2,879) is below FY30 (3,089). Without the rule (capex held at 7.10%) the value would be 1,739p (+118p), and the implied return on new investment 31%. The PM chose the cautious measure; this shows its size.
5. **Comps data quality.**
   - WKL, EXPN, LSEG and Informa are Yahoo-only figures.
   - Experian's LTM ends 3 months earlier than the others.
   - Peer EBITDA is unadjusted, while RELX's is adjusted (reported-basis variant shown: -111p on the median).
   - TRI still includes print.
   - US peers do not add back lease costs in EBITDA.
   - EV/EBITDA NTM and RELX forward EPS are MISSING, so P/E is a multiple only.
6. **The engine's bear case covers growth and WACC only.** The agreed bear lines (margin 33.1%, tax 25%, terminal growth 1.5%, RONIC = WACC, acquisitions 2.7%, BBB spread) are for the Bear agent.
7. **pytest is not installed** in this environment, so `python -m pytest` could not be run. I changed no code in `desk/`.

## For the PM (disagreements; nothing changed)
- **The discount rate decides this rating, and each part of it is at the cautious end at the same time.**
  - The run-date gilt is 5.45%, from an aggregator.
  - The bottom-up beta is 0.97, while own regressions give 0.38-0.67 and the raw peer median is 0.75.
  - The full 5.0% ERP is added on top of a gilt that is itself high.

  Each choice is documented, but together they give a 9.6% WACC, above the desk's 6-9% range. This is a business with single-A credit, 35% margins and negative working capital. A HOLD needs a WACC of about 7.4% (beta 0.45, or a gilt of 3.1%). I would present the SELL with the WACC flip points and the comps gap side by side, not as a firm call.
- **The 35.0% flat margin is cautious against history.** The adjusted margin rose every year: 30.5%, 31.4%, 33.1%, 33.9%, 34.8% (FY21-25), and management guides further expansion. Each point is worth 65p. But even 48% would only reach HOLD, so the margin does not change the call.
- No objection to the mechanics. Leases, JVs, the pension surplus, the buyback roll-forward and the share count are all treated consistently.

## Missing
- NTM EBITDA consensus for the peers.
- RELX consensus EPS (needed for a P/E value).
- The peers' H2 2025 figures (needed for a December calendarisation).
- Experian's FY Mar-2026 EPS consensus.
- A primary-source gilt yield for 13 Oct 2026 (Data agent FLAG 2).
- Buybacks after 25 Sep 2026 (not yet filed; consistent with the share count).

## Confidence
- **High on the mechanics.** The Excel recalculates to Python on 74 cells, and the value decomposition re-adds to 1,621p.
- **Medium-low on the value as a rating signal.** Every SELL-to-HOLD path runs through the discount rate, which sits outside the desk's own range. The DCF also disagrees with the comps and with the market by more than 40%.
- **Comps: medium.** Four of the seven peers are SEC-sourced, and the median (15.7x) is close to RELX's own 14.6x.
