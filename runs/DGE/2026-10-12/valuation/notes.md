# Valuation agent notes: Diageo (DGE), run 2026-10-12

## Step 1: inputs check
`inputs.yaml` has every required value with a source, including beta from the Risk agent. No STOP.

## Step 2: DCF (`valuation.json`, `dcf.xlsx`)
| | Base | Bear |
|---|---|---|
| WACC | 6.21% | 7.21% |
| Enterprise value (USD m) | 86,751 | 64,885 |
| Equity value (USD m) | 72,789 | 50,923 |
| Value per share | USD 32.76 / **2,475p** | USD 22.92 / **1,732p** |
| Upside vs 1,673p | **+48.0%** | +3.5% |
| Rating (engine) | **BUY** | HOLD |

WACC parts: risk-free 5.22%, beta 0.48, ERP 5.0%, cost of equity 7.60%, pre-tax cost of debt 3.81% (2.88% after tax), debt weight 29.4%.

I opened `dcf.xlsx` in LibreOffice, recalculated it, and compared every Excel formula with the Python value. The largest difference is 0.00000004%, so they match.

## Step 3: comps (`comps.json`)
I could only use P/E, and only for two peers: Pernod Ricard 10.7x and Brown-Forman 17.4x, median 14.0x. Applied to Diageo's FY26 EPS before exceptionals (165.3 cents), that implies **1,753p** (range 1,334p to 2,172p). Diageo trades at 13.4x. Campari, Remy Cointreau and Constellation are missing (see Data notes). **Indicative only.**

## Step 4: sanity checks (`sanity_checks.json`)
- **FLAG: terminal value is 82.7% of EV** (threshold 75%). Most of the value sits beyond FY31, so the answer is very sensitive to WACC and terminal growth.
- **WACC of 6.21% is inside 6-9%, but only just**, and only because of two low inputs: beta 0.48 and cost of debt 3.81% (below the 5.22% risk-free). I have not changed either.
- **The implied exit multiple is 13.3x EBITDA.** EV/EBITDA comps are unavailable this run, so I cannot check it against peers. The market currently values Diageo at roughly 9.8x FY26 adjusted EBITDA (approximate; see `sanity_checks.json`), so the DCF's exit multiple is about a third above where the stock trades today.
- **DCF vs comps: the DCF (2,475p) is 41% above the comps value (1,753p).**

## For the PM (I have not changed any assumption)
1. **The BUY rests on the discount rate.** On the sensitivity grid, at WACC 7.21% (the bear WACC) with 2% terminal growth, the value is 1,909p (+14%, a HOLD). A WACC of about 7.2% or more removes the BUY.
2. **The cost of debt is below the risk-free rate**, which cannot be right for new borrowing. I suggest the brief specifies Rf + credit spread.
3. **Terminal capex at 7.1% of sales vs D&A at 3.4%** depresses terminal cash flow. That works the other way (it lowers value). It is worth a deliberate decision.
4. **The savings are counted on top of a constant 29.4% base margin.** Management says the savings "will allow us to invest without reducing operating profit" (20-F p.21). Read literally, the savings fund reinvestment rather than lifting margins. Under the brief, the base FY28 EBIT margin rises from 29.4% to 31.9%.

## Savings schedule used (from the brief, PM assumption)
c.USD 1,000m in total: USD 850m from the operating framework (c.40% in FY27, the rest in FY28) and USD 150m from the supply chain (c.25% in FY27). Cumulative run-rate (USD m): 377.5, 962.5, 1,000, 1,000, 1,000. Source: Diageo Capital Markets Day 6-K, 6 Aug 2026.
