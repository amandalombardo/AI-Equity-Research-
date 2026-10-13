# Valuation agent notes: The Coca-Cola Company (KO), run 2026-10-13

Every value per share is in **US dollars (USD)**. Totals are in **USD m**. KO trades on the NYSE in USD, so there is no ADR and no pence conversion. All figures come from the desk engine (`desk/dcf.py`, `desk/comps.py`) through the scripts in this folder. None of the arithmetic was done by hand.

## What I did
1. **Input check.** I checked `inputs.yaml`. Every required value is present and has a source, including `beta` 0.6091 from the Risk agent (Damodaran US Beverage (Soft) unlevered 0.5755, relevered at x1.0584). Note that `data/notes.md` is older than the PM's later decisions in `apply_pm_ccba_decision.py` and `apply_pm_audit_fixes.py` (base sales ex-CCBA, associates at run-date market value, contingent 14,000), so `inputs.yaml` is the version I relied on.
2. **Engine run.** I ran `python -m desk.valuation_run briefs/KO.yaml runs/KO/2026-10-13/inputs.yaml runs/KO/2026-10-13/valuation`. It produced `valuation.json` and `dcf.xlsx` (live formulas).
3. **Comps.** `run_comps.py` produced `comps.csv` and `comps.json`.
4. **Sanity checks, flip points and scenarios.** `run_sanity.py` produced `sanity_checks.json`. Each variant is run on a scratch copy in `scratch/`. The brief and `inputs.yaml` were never edited.

## Base case (PM assumptions)
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

## Comps (cross-check)
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

## Sanity checks
| check | result |
|---|---|
| Terminal value share of EV | **75.1%: FLAG** (just above the 75% limit) |
| Implied exit EV/EBITDA vs peers | **11.1x, below the peer range of 11.4x to 29.1x (median 19.1x): FLAG.** KO itself trades at 26.1x |
| WACC within 6-9% | 8.00%: OK |
| DCF vs comps | DCF $47.60 is **32% below** the comps median of $70.07, though inside the comps range ($42.01 to $107.05) |

## Where the rating flips (one variable at a time, everything else at base)
The value needed is at least $81.11 for HOLD and at least $103.64 for BUY.

| variable (base) | SELL to HOLD at | HOLD to BUY at |
|---|---|---|
| beta (0.6091) | 0.061 | -0.104 (not economically possible) |
| WACC (8.00%) | 5.52% | 4.76% |
| terminal growth (2.0%) | 5.17% | 5.91% |
| operating margin (33.2%) | 55.5% | 70.5% |

**In plain terms:** no reasonable change to any single assumption takes KO out of SELL. On the PM's assumptions, the market price implies something like a WACC of about 5.5%, or perpetual growth of about 5%.

## Scenarios (these are NOT the base case)
- **Beta from Damodaran's 2022-26 average soft-beverage unlevered beta.**
  - The unlevered 0.820485 x 1.0584 gives a beta of 0.8684, a cost of equity of 9.56% and a WACC of 9.20%.
  - Result: **$40.01 (-55.6%), SELL.** EV 166,190, TV 71.1% of EV, exit 9.3x.
  - On this beta the WACC is **above the 9% check range**.
- **KO WINS the IRS case.**
  - Contingent liability 0, the $6,000m deposit refunded (added with the stakes, so associates become 52,626), and a tax rate of 19.9%. Beta is left at 0.6091.
  - Result: **$54.90 (-39.1%), SELL.** WACC 8.01%, EV 207,941, TV 75.0%, exit 11.6x.
  - Not included: the $385m interest receivable, and relevering beta at 19.9% (both small).

## FLAGs
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

## For Amanda: assumptions I would question (not changed)
- **Discount rate vs market.** The 5.22% risk-free rate plus the 5.0% ERP gives a cost of equity of 8.27% for a stock whose own regressions show a beta of 0.1-0.35. The market price is consistent with a WACC of about 5.5%. The rating is driven almost entirely by this. It is worth deciding whether the 8.0% WACC, or the 2% perpetual growth for a business with 4-5% organic growth guidance, is the view you want to stand behind.
- **Capex 4.4% of sales includes CCBA**, a capital-heavy bottler, but the base sales exclude it. Ex-CCBA capex intensity is probably lower, and that would raise the value. D&A (2.68%, the FY21-25 average) is above FY25's 2.19% and works the other way. The two partly offset.
- **Tax 23.7% in perpetuity** assumes the Tax Court method applies forever. That is consistent with "IRS case lost", but it is a permanent 3.8-point drag on top of the 14,000 deduction.

## Confidence
- **High** that the engine and the bridge were applied correctly to the inputs.
- **Medium-low** on the comps: there are only 3 peers, KDP is distorted and the range is wide.
- The SELL rating is robust to every single-variable change tested. It depends mainly on the PM's discount rate and terminal-growth assumptions.

## Files
`valuation.json`, `dcf.xlsx`, `comps.csv`, `comps.json`, `sanity_checks.json`, `run_comps.py`, `run_sanity.py`, `scratch/` (scenario copies of the brief and inputs; not the base case)
