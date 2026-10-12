# Valuation agent notes: Diageo (DGE), run 2026-10-12

## Step 1: inputs check
`inputs.yaml` has every required value with a source, including beta from the Risk agent. No STOP.

## Step 2: DCF (`valuation.json`, `dcf.xlsx`)
**Latest re-run (2026-10-12):** cost of debt = risk-free + 1% (PM rule), and beta 0.96 (bottom-up, see `risk/beta_evidence.json`). The first run, at beta 0.48 and historic debt cost, gave 2,475p (BUY). The second run, with debt fixed and beta still 0.48, gave 2,141p (BUY).

| | Base | Bear |
|---|---|---|
| WACC | 8.46% | 9.46% |
| Enterprise value (USD m) | 56,530 | 45,446 |
| Equity value (USD m) | 42,568 | |
| Value per share | USD 19.16 / **1,448p** | **1,071p** |
| Upside vs 1,673p | **-13.5%** | -36.0% |
| Rating (engine) | **SELL** | SELL |

WACC parts: risk-free 5.22%, beta 0.96, ERP 5.0%, cost of equity 10.02%, pre-tax cost of debt 6.22% (4.71% after tax), debt weight 29.4%.

## Step 3: comps (`comps.json`)
I could only use P/E, and only for two peers: Pernod Ricard 10.7x and Brown-Forman 17.4x, median 14.0x. Applied to Diageo's FY26 EPS before exceptionals (165.3 cents), that implies **1,753p** (range 1,334p to 2,172p). Diageo trades at 13.4x. Campari, Remy Cointreau and Constellation are missing (see Data notes). **Indicative only.**

## Step 4: sanity checks (`sanity_checks.json`)
- **Terminal value is 74.9% of EV**, just under the 75% flag.
- **WACC of 8.46% is inside 6-9%.**
- **The implied exit multiple is 8.6x EBITDA**, below the roughly 9.8x the market pays today (approximate). EV/EBITDA comps are unavailable this run.
- **DCF vs comps: the DCF (1,448p) is 17% below the comps value (1,753p).**
- **Market-implied WACC:** on the sensitivity grid, the share price (1,673p) sits between WACC 7.46% (1,800p) and 7.96% (1,609p) at 2% growth. The market is pricing a WACC of roughly 7.8%, below our 8.46%.

## For the PM (I have not changed any assumption)
1. **The rating rests on beta.** Beta 0.72 (Diageo's own best regression) gives 1,738p, a HOLD. Beta 0.96 gives a SELL. A BUY needs a beta below about 0.6, which is at or below the lowest precise estimate (0.60); it is a SELL from about 0.9 up.
2. **Cost of debt: resolved** (risk-free + 1%).
3. **Terminal capex at 7.1% of sales vs D&A at 3.4%** depresses terminal cash flow. It is worth a deliberate decision.
4. **Savings on top of a constant margin:** management says the savings fund reinvestment (20-F p.21).

## Savings schedule used (from the brief, PM assumption)
c.USD 1,000m in total: USD 850m from the operating framework (c.40% in FY27, the rest in FY28) and USD 150m from the supply chain (c.25% in FY27). Cumulative run-rate (USD m): 377.5, 962.5, 1,000, 1,000, 1,000. Source: Diageo Capital Markets Day 6-K, 6 Aug 2026.
