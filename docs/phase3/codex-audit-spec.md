# Codex audit spec: maths audit of the equity research desk (Phase 3)

Paste everything below the line into Codex, with the repository `AIEquityResearch` and the branch **`main`** selected.

---

You are an independent auditor of the valuation maths in this repository. Another AI (Claude Code) wrote the code. Your job is to find errors, not to defend or improve the design. The portfolio manager (PM) is a finance student who does not code, so write every finding in plain finance language.

## What the desk does
Six AI agents value Diageo plc (LSE: DGE) and write a buy/hold/sell memo. All arithmetic is in Python in `desk/`. The PM's assumptions are in `briefs/DGE.yaml`. The latest run is in `runs/DGE/2026-10-12/`: inputs with sources in `inputs.yaml`, output in `valuation/valuation.json` and `valuation/dcf.xlsx`. The result was a value of 1,448p per share vs a price of 1,673p: SELL.

## Rules
1. **Do not change any code, assumption or run output.** Write one file only: `audits/codex-audit-2026-10.md`. Claude Code will make the fixes and the PM will approve them.
2. **Do not judge the PM's assumptions** (growth, savings, flow-through, beta rule, credit spread, ERP, terminal growth). Audit whether the code applies them correctly. If an assumption is internally inconsistent with another one, you may note it as "Assumption comment", separate from errors.
3. **Every finding must be shown, not asserted.** Give a small worked example with numbers (by hand or a short script) that shows the wrong result and the right one.
4. Units: Diageo reports in USD; London prices are in pence (GBp); 1 DEO ADR = 4 ordinary shares.

## What to check
Go through each file and each formula. At a minimum:

**`desk/dcf.py`**
- WACC and CAPM: formula, tax shield on debt, market-value weights.
- Free cash flow: NOPAT + D&A - capex - increase in net working capital. Signs, which year's sales each line uses.
- Savings: added on top of a constant base margin, times the flow-through. Check this matches the docstring and the brief.
- Discounting: the stub period (part of FY27 already elapsed at the valuation date), the mid-year option, the discount period of the terminal value.
- Terminal value: Gordon growth. Is the cash flow used in the terminal value consistent with steady growth at the terminal rate (working capital, capex vs D&A)?
- Equity bridge: which items are subtracted and added, and the USD to pence conversion. Is the net debt date consistent with the valuation date and the stub-period treatment?
- Sensitivity grid: does its centre cell equal the base case?

**`desk/valuation_run.py`**: the brief's rules (credit spread replacing the historic cost of debt), the bear case scenario, that the run stops when an input or its source is missing.

**`desk/comps.py`**: calendarising peers to Diageo's June year end; median and range.

**`desk/risk.py`**: beta (regression of returns, not prices), volatility annualisation, maximum drawdown.

**`desk/fundamentals.py`**: each ratio's numerator and denominator, and the year they belong to.

**`desk/units.py`, `desk/rating.py`**: pence/pounds/ADR conversions; the Buy/Hold/Sell thresholds and the boundaries.

**`desk/excel_export.py`**: every Excel formula computes the same thing as the Python code.

**`desk/data_sources.py`**: unit traps (USD vs GBP years, net sales vs revenue including excise, treasury shares).

**The Diageo run**: recompute the 1,448p value per share independently from `runs/DGE/2026-10-12/inputs.yaml` and `briefs/DGE.yaml`, without calling `desk/`. Report your number and the gap.

Run the tests with `python -m pytest` and report the result. If you think a test checks the wrong thing, say so.

## Output: `audits/codex-audit-2026-10.md`
1. **Summary**: number of findings by severity; your independent value per share vs 1,448p; test result.
2. **Findings table**: ID | file:line | severity | what is wrong (plain English) | finance concept | worked example | suggested fix | estimated effect on value per share (pence), if you can estimate it.
   - **High**: changes the value by more than 2% or could change the rating.
   - **Medium**: a real error with a smaller effect, or one that would matter for another company.
   - **Low**: presentation, labels, comments, untested edge cases.
3. **Assumption comments** (optional), kept separate.
4. **What you checked and found correct**, so the PM knows what the audit covered.

Then open a pull request containing only that file, titled "Codex maths audit, October 2026".
