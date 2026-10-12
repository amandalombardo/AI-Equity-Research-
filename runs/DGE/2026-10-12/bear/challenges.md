# Bear case: Diageo (DGE), run 2026-10-12 (re-run after the PM's cost-of-debt decision)

Base case: 2,141p (+28.0% vs 1,673p, BUY) at a WACC of 6.75%, with the cost of debt at risk-free + 1% (PM rule). The engine's bear scenario (no growth, 25% flow-through, WACC +1 point) gives 1,527p (-8.7%, HOLD).
For each challenge, I re-ran `desk.valuation_run` with one change (`run_challenges.py`, results in `challenges.json`). For reference: the first run's historic cost of debt (3.81%) gave 2,475p.

## 1. Beta of 0.48 understates the risk (challenges the Risk agent): **-735p**
**Claim:** the stock fell 67% from peak to trough with 31.6% volatility, 2.5x the FTSE 100. A cost of equity of 7.6% (only 2.4 points over Treasuries) is not credible for that. The low beta comes from regressions that explain 4% of the price moves (R-squared 0.04).
**Evidence:** `risk/risk.json`.
**Impact:** with beta 1.0, WACC is 8.60% and the value is 1,407p (-735p): **SELL, -15.9%**.

## 2. A 1% credit spread may be too tight (challenges the PM's new debt rule): **-117p**
**Claim:** leverage is 3.1x, above the 2.5-3.0x range that management says is "broadly consistent with an A-band credit rating" (20-F p.186). If leverage stays above target, a wider spread is plausible.
**Impact:** a 2.0% spread gives WACC 6.97% and 2,024p (-117p). Still a BUY (+21.0%).

## 3. Savings flow-through: management says the savings will be reinvested (challenges the Valuation assumptions): **-124p to -248p**
**Claim:** the brief keeps 50% of c.$1bn of savings as profit, on top of a constant margin. Diageo itself says "these savings will allow us to invest without reducing operating profit" (20-F p.21). Under the brief, the EBIT margin rises from 29.4% (FY27 base) to 31.9% in FY28.
**Impact:** 25% flow-through gives 2,017p (-124p, still a BUY at +20.6%). **0% flow-through gives 1,893p (-248p): HOLD, +13.2%.** The supply-chain phasing assumption barely matters (-1p).

## 4. Terminal growth of 2% vs a shrinking spirits market (challenges the Data agent's industry check): **-211p**
**Claim:** IWSR reports that global spirits volumes fell 3% in 2025, and it sees volumes down about 2% by 2035 (secondhand, see data notes). GLP-1 weight-loss drugs and the moderation trend point the same way.
**Impact:** terminal growth of 1.5% gives 1,931p (-211p). That is +15.4%, a BUY by a hair. The terminal value is 80.7% of EV.

## 5. Management's track record does not support the growth path (challenges the Fundamentals agent): **-72p**
**Claim:** the 2023-26 incentive plan targeted 4.0-8.0% organic sales CAGR; the actual was **-0.3%**. It targeted 4.5-11.5% organic profit CAGR; the actual was **-3.4%**. Cumulative free cash flow was $8,738m vs a $9,400m threshold. Relative TSR ranked 15th of 17. Nothing vested (20-F p.110).
**Impact:** zero organic growth FY27-31 gives 2,069p (-72p).

## 6. Net debt is stale (challenges the Data agent): **-23p**
**Claim:** net debt is the 30 June 2026 figure. The 30c final dividend (about 667) goes out after the run date. Disposal proceeds (3,318) are gross and the deals have not closed.
**Impact:** deducting the dividend gives 2,119p (-23p).

## Other concerns not quantified
- Minority interests are deducted at book value (2,083). USL's 42.79% minority is worth much more at market.
- North America (37% of sales) is guided down by a mid-single-digit percentage in FY27. Tariffs remain.
- Leverage is 3.1x vs the 2.5-3.0x target, and the dividend has already been cut.

**Strongest reason not to buy: the 28% upside still needs a 0.48 beta; at beta 1.0 the same model gives 1,407p, a SELL, and two modest challenges (full reinvestment of savings, or 1.5% terminal growth) each take it to the edge of HOLD.**
