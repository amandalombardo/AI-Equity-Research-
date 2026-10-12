# Valuation agent notes: Diageo (DGE), run 2026-10-12

## Step 1: inputs check
`inputs.yaml` has every required value with a source, including beta from the Risk agent. No STOP.

## Step 2: DCF (`valuation.json`, `dcf.xlsx`)
**Re-run 2026-10-12 after the PM's decision:** the pre-tax cost of debt is now risk-free + 1.0% = 6.22% (credit_spread in the brief). The historic 3.81% is kept for reference only.

| | Base | Bear |
|---|---|---|
| WACC | 6.75% | 7.75% |
| Enterprise value (USD m) | 76,931 | |
| Equity value (USD m) | 62,969 | |
| Value per share | USD 28.34 / **2,141p** | **1,527p** |
| Upside vs 1,673p | **+28.0%** | -8.7% |
| Rating (engine) | **BUY** | HOLD |

WACC parts: risk-free 5.22%, beta 0.48, ERP 5.0%, cost of equity 7.60%, pre-tax cost of debt 6.22% (4.71% after tax), debt weight 29.4%.

I opened `dcf.xlsx` in LibreOffice, recalculated it, and compared every Excel formula with the Python value. They match (largest difference 0.00000001%).

## Step 3: comps (`comps.json`)
I could only use P/E, and only for two peers: Pernod Ricard 10.7x and Brown-Forman 17.4x, median 14.0x. Applied to Diageo's FY26 EPS before exceptionals (165.3 cents), that implies **1,753p** (range 1,334p to 2,172p). Diageo trades at 13.4x. Campari, Remy Cointreau and Constellation are missing (see Data notes). **Indicative only.**

## Step 4: sanity checks (`sanity_checks.json`)
- **FLAG: terminal value is 80.7% of EV** (threshold 75%). Most of the value sits beyond FY31, so the answer is very sensitive to WACC and terminal growth.
- **WACC of 6.75% is inside 6-9%.** It still rests on a low beta (0.48).
- **The implied exit multiple is 11.8x EBITDA.** EV/EBITDA comps are unavailable this run, so I cannot check it against peers. The market currently values Diageo at roughly 9.8x FY26 adjusted EBITDA (approximate; see `sanity_checks.json`), so the DCF's exit multiple is about a fifth above where the stock trades today.
- **DCF vs comps: the DCF (2,141p) is 22% above the comps value (1,753p).**

## For the PM (I have not changed any assumption)
1. **The BUY still rests on the discount rate.** On the sensitivity grid, at WACC 7.25% with 2% terminal growth, the value is 1,892p (+13%, a HOLD). A WACC of about 7.2% or more removes the BUY (a BUY needs 1,924p or more).
2. **Cost of debt: resolved.** The PM chose risk-free + 1% (2026-10-12).
3. **Terminal capex at 7.1% of sales vs D&A at 3.4%** depresses terminal cash flow. That works the other way (it lowers value). It is worth a deliberate decision.
4. **The savings are counted on top of a constant 29.4% base margin.** Management says the savings "will allow us to invest without reducing operating profit" (20-F p.21). Read literally, the savings fund reinvestment rather than lifting margins. Under the brief, the base FY28 EBIT margin rises from 29.4% to 31.9%.

## Savings schedule used (from the brief, PM assumption)
c.USD 1,000m in total: USD 850m from the operating framework (c.40% in FY27, the rest in FY28) and USD 150m from the supply chain (c.25% in FY27). Cumulative run-rate (USD m): 377.5, 962.5, 1,000, 1,000, 1,000. Source: Diageo Capital Markets Day 6-K, 6 Aug 2026.
