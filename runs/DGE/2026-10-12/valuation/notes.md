# Valuation agent notes: Diageo (DGE), run 2026-10-12 (Phase 3 re-run; minorities re-run 2026-10-13)

**History of the base value:** 2,475p (first run, BUY) -> 2,141p (cost of debt fixed, BUY) -> 1,448p (bottom-up beta 0.96, SELL) -> 1,524p (Phase 3, HOLD) -> **1,545p (proportionate minorities, PM decision 2026-10-13, HOLD)**.

## Step 1: inputs check
`inputs.yaml` has every required value with a source, including beta 0.96 from the Risk agent the two Phase 3 inputs (`restructuring_cash` USD 850m; `dividends_ex_before_valuation_musd` 0) and, for the 2026-10-13 re-run, `minority_share_of_operating_profit` 2.566% (sourced to the 20-F p.210 and p.164). No STOP. I did not change `briefs/DGE.yaml` or `inputs.yaml`.

## Step 2: DCF (`valuation.json`, `dcf.xlsx`)
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

## Minorities (PM decision 2026-10-13)
**What changed.** Diageo owns most, but not all, of some subsidiaries (mainly United Spirits in India, 57%; EABL in Kenya, 65%, now being sold). The DCF values 100% of their cash flows, so we must take off the slice that belongs to the outside shareholders. Until now we took that slice at its **book value, USD 2,083m** (an accounting figure from the balance sheet). We now value it the same way as the rest of the business: **outside shareholders' share of operating profit (2.566%, ex-EABL) x enterprise value = USD 1,500m** (base case; USD 1,171m in the bear case, because it moves with EV). Effect: **+20p (GBp)**, from 1,524.4p to 1,544.8p (shown as +21p if you subtract the rounded 1,524p from 1,545p).

**Why.** Book value failed your evidence test: (1) it is an accounting number, not a value (USL's minority is USD 755m at book vs c.USD 4.45bn at market); (2) it double counted EABL: EABL's 35% outside shareholders were inside the 2,083, yet EABL is already excluded from the forecast and only Diageo's own sale proceeds are added back.

**Weaknesses (it is an estimate, not a market price).**
- It assumes minorities are worth their share of *operating profit* times the group multiple. Subsidiaries with faster growth or a higher multiple (USL) are under-valued by this; slower ones over-valued.
- It ignores **USL's net cash** (and any subsidiary-level debt): outside shareholders own a slice of that cash too, which the operating-profit share does not capture.
- To strip out EABL it assumes **EABL's minorities share EABL's EBIT pro rata** (35% x USD 250.2m); the actual EABL profit attributable to minorities may differ (interest, tax, its own minorities).
- Sensitivity: the rating flips to SELL only if the minorities' share of operating profit is above about **4.48%** (vs 2.566%), i.e. minorities of roughly USD 2.6bn, so the method choice alone does not decide HOLD vs SELL. The old book method would also give HOLD (1,524p).

**Distance to SELL.** The SELL line is **1,506p (GBp)** (10% below 1,673p). The base is now **39p above it** (was 18p), i.e. 7.7% below the price vs the 10% trigger.

## Step 3: comps (`comps.csv`, `comps.json`)
P/E only (peer EV/EBITDA is still unavailable). All 4 core peers now have a P/E: Pernod Ricard 10.7x, Brown-Forman 17.4x, Campari 19.6x, Remy Cointreau 25.3x. **Median 18.5x**, applied to Diageo's FY26 EPS before exceptionals (165.3 cents) = **2,311p** (range 1,334p to 3,163p). Diageo trades at 13.4x. Only Pernod has a June year end; the others could not be calendarised (next fiscal years or half-years not yet found), so their gaps are 2 to 6 months. Campari and Remy come from press reports, not filings, and Remy's P/E is inflated by depressed cognac earnings. Constellation Brands (beer-heavy, shown separately) is still missing. **Indicative only.**

## Step 4: sanity checks (`sanity_checks.json`)
- **Terminal value is 74.9% of EV**, just under the 75% flag (no FLAG, but close).
- **WACC of 8.46% is inside 6-9%.**
- **Implied exit multiple: 9.2x FY31 EBITDA** (was 8.6x). Peer EV/EBITDA is unavailable, so I cannot test it against a peer range. It is a little below the roughly 9.7x the market pays for Diageo today (FY26 adjusted EBITDA ex associates; approximate, includes EABL; market EV now uses proportionate minorities, c.USD 1,608m at market), so it does not look aggressive.
- **Market-implied WACC: about 8.1%.** On the sensitivity grid at 2% growth, 1,673p sits between WACC 7.96% (1,714p) and 8.46% (1,545p); solving with the engine gives 8.07%. The market is pricing a WACC about 0.4 points below ours.
- **DCF vs comps: the DCF (1,545p) is 33% below the comps value (2,311p).** The gap widened from 17% (before Phase 3) because Campari and Remy (both on high P/Es) entered the median. The comps value is pulled up by Remy's depressed earnings; Pernod, the closest peer by year end and mix, is at 10.7x, below Diageo's 13.4x. I would not give the comps much weight.

## What changed vs 1,448p (computed with `desk.valuation_run.build`, one change at a time, cumulative; `run_bridge.py`, `bridge.json`; steps 0-5 use book minorities, step 6 switches to proportionate)

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

## For the PM (I have not changed any assumption)
1. **FLAG: the HOLD is still close to SELL, but less so.** The value is 7.7% below the price; SELL starts at 10% (1,506p GBp), now 39p lower (was 18p). Thresholds solved with the engine (`run_sanity.py`, `sanity_checks.json`), one input at a time: SELL if **beta above 0.997** (we use 0.96), **WACC above 8.59%** (we use 8.46%), **savings flow-through below 33.6%** (we use 46%), **terminal RONIC below 11.7%** (we use 13.4%; terminal capex 6.75% of sales), or **minorities' share of operating profit above 4.48%** (we use 2.566%). BUY (1,924p GBp) would need a **beta below 0.666** or a **WACC below 7.44%**. Note: the brief's comment "Rating flips to SELL at c.40%" (flow-through) is now out of date: at 40% the value is 1,526p (HOLD); the flip is at c.34%. I have not edited the brief.
2. **Beta is still the biggest lever.** Beta 0.72 (Diageo's own best regression) gives 1,844p (HOLD); 0.85 gives 1,672p; 0.96 gives 1,545p (all GBp).
3. **Terminal capex below the 5-year history.** 6.2% of sales vs 7.1% actual over FY22-26, worth +65p. It is consistent with the 13.4% ROIC rule you chose, but it assumes the heavy maturing-stock and capacity spend of recent years is not repeated forever. Reasonable, but it is the largest single upward step.
4. **Restructuring cash is pre-tax and undiscounted** (USD 850m at 30 June, though paid over FY27-29). Tax relief (up to about USD 207m) and discounting would each add a little (Data agent: up to about 7p for tax). Conservative; I left it as is.
5. **Comps are weak** (P/E only, two press-sourced peers, no calendarisation except Pernod, no EV/EBITDA). The 34% gap to comps should not drive the decision.
6. Tests: `python -m pytest` could not run here (pytest is not installed in this environment). I changed no code in `desk/`; I changed only my own helper scripts (`run_bridge.py` now adds the minorities step and reads minorities from the engine; new `run_sanity.py` regenerates `sanity_checks.json` and the thresholds).

## What's missing
Peer EV/EBITDA and FCF yield; Constellation Brands EPS; calendarised peer figures (only Pernod is on a June year).

## Confidence
**Medium** on the DCF mechanics (engine and Excel agree; the 1,448p baseline reproduces exactly). **Medium-low** on the rating, because HOLD vs SELL sits within 39p and rests mainly on beta (SELL above 0.997) and WACC. **Medium** on the minorities figure (an estimate from operating profit shares, see above). **Low** on comps.

## Savings schedule used (from the brief, PM assumption)
c.USD 1,000m in total: USD 850m from the operating framework (c.40% in FY27, the rest in FY28) and USD 150m from the supply chain (c.25% in FY27). Cumulative run-rate (USD m): 377.5, 962.5, 1,000, 1,000, 1,000, of which 46% reaches operating profit. Source: Diageo Capital Markets Day 6-K, 6 Aug 2026.
