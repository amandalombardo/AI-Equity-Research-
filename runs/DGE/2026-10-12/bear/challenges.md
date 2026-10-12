# Bear case: Diageo (DGE), run 2026-10-12

Base case: 2,475p (+48.0% vs 1,673p, BUY). The engine's bear scenario (no growth, 25% flow-through, WACC +1 point) gives 1,732p (+3.5%, HOLD).
For each challenge, I re-ran `desk.valuation_run` with one change (`run_challenges.py`, results in `challenges.json`).

## 1. The cost of debt is too low (challenges the Data and Valuation agents): **-334p**
**Claim:** 3.81% is the average interest on old, mostly fixed-rate bonds. New borrowing costs more than the 5.22% US Treasury yield. A company cannot borrow below its government's rate.
**Evidence:** 20-F p.211: net interest 812 / average net borrowings 21,336. FRED DGS10 at 5.22% on 2026-10-08. Diageo's recent bonds carried coupons of 5.125% and 5.625% (USD, issued FY25: 20-F, Financial review, "Movements in net borrowings" note 3).
**Impact:** with the cost of debt at Rf + 1% (6.22%), WACC is 6.75% and the value is 2,141p (-334p). Still a BUY (+28.0%).

## 2. Beta of 0.48 understates the risk (challenges the Risk agent): **-902p**
**Claim:** the stock fell 67% from peak to trough with 31.6% volatility, 2.5x the FTSE 100. A cost of equity of 7.6% (only 2.4 points over Treasuries) is not credible for that. The low beta comes from regressions that explain 4% of the price moves (R-squared 0.04).
**Evidence:** `risk/risk.json`.
**Impact:** with beta 1.0, WACC is 8.06% and the value is 1,573p (-902p): **HOLD, -6.0%**.
**Combined with challenge 1** (beta 1.0 and cost of debt 6.22%): WACC 8.60% and the value is 1,407p: **SELL, -15.9%**.

## 3. Savings flow-through: management says the savings will be reinvested (challenges the Valuation assumptions): **-140p to -280p**
**Claim:** the brief keeps 50% of c.$1bn of savings as profit, on top of a constant margin. Diageo itself says "these savings will allow us to invest without reducing operating profit" (20-F p.21). That sounds like the savings fund reinvestment, not margin expansion. Under the brief, the EBIT margin rises from 29.4% (FY27 base) to 31.9% in FY28.
**Impact:** 25% flow-through gives 2,335p (-140p). 0% flow-through gives 2,195p (-280p). The supply-chain phasing assumption (75% in FY28) barely matters: slowing it to 25/50/75/100% costs only 1p.

## 4. Terminal growth of 2% vs a shrinking spirits market (challenges the Data agent's industry check): **-270p**
**Claim:** IWSR reports that global spirits volumes fell 3% in 2025, and it sees volumes down about 2% by 2035 (secondhand, see data notes). Growing 2% a year forever needs price/mix to outrun falling volumes forever. GLP-1 weight-loss drugs and the moderation trend among younger drinkers point the same way.
**Impact:** terminal growth of 1.5% gives 2,206p (-270p). The terminal value is 82.7% of EV, so this assumption matters more than any single forecast year.

## 5. Management's track record does not support the growth path (challenges the Fundamentals agent): **-83p**
**Claim:** the last three-year plan missed every target. The 2023-26 incentive plan targeted 4.0-8.0% organic sales CAGR; the actual was **-0.3%**. It targeted 4.5-11.5% organic profit CAGR; the actual was **-3.4%**. Cumulative free cash flow was $8,738m vs a $9,400m threshold. Relative TSR ranked 15th of 17. Nothing vested (20-F p.110). The new plan again promises about $8bn of cash over three years.
**Impact:** zero organic growth FY27-31 (in line with the -0.3% record) gives 2,392p (-83p). The small impact is itself a warning: the value comes from the discount rate and the terminal value, not from the forecast.

## 6. Net debt is stale (challenges the Data agent): **-23p**
**Claim:** net debt is the 30 June 2026 figure. The 30c final dividend (about 667) goes out after the run date and is not deducted. Disposal proceeds (3,318) are gross, before tax and costs, and are counted before either deal has closed.
**Impact:** deducting the dividend gives 2,453p (-23p). Tax on the RCB and EABL gains is not quantified (no sourced rate).

## Other concerns not quantified
- Minority interests are deducted at book value (2,083). USL is listed, and its 42.79% minority is worth much more at market.
- North America (37% of sales) is guided down by a mid-single-digit percentage in FY27 (CMD, 6 Aug 2026). Tariffs on EU and UK spirits remain.
- Leverage is 3.1x vs the 2.5-3.0x target, and the dividend has already been cut. There is little room if the turnaround slips.

**Strongest reason not to buy: the 48% upside exists only at a 6.2% WACC, built from a 0.48 beta and a below-Treasury cost of debt; at a market cost of capital (beta 1.0, debt at Rf + 1%) the same model says 1,407p, a SELL.**
