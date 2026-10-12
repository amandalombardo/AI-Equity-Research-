# Bear case: Diageo (DGE), run 2026-10-12 (Phase 3 re-run)

**Base case: 1,524p (USD 20.17), -8.9% vs 1,673p, HOLD** at a WACC of 8.46% (beta 0.96, terminal RONIC 13.4%, flow-through 46%, valued at 30 June 2026 and rolled forward to 12 Oct, restructuring cash USD 850m deducted). **SELL starts at 1,506p (1,505.7p), only 18.7p below the base.**
The engine's bear scenario (no organic growth, 25% flow-through, WACC +1 point) gives **1,076p (-35.7%, SELL)**: that combines three changes, so it is shown for reference, not as a single challenge.

Method: each challenge below is **one change** to an in-memory copy of the brief or `inputs.yaml`, re-run through `desk.valuation_run.build` (`run_challenges.py`, results in `challenges.json`). All values are pence per ordinary share (GBp); impacts are vs 1,524.4p. Under the PM's terminal rule, terminal capex is re-derived from RONIC in every run, so changes to profit or growth also move terminal capex (shown in `challenges.json`).

## 1. Savings flow-through: the record says most savings get reinvested (challenges the Valuation agent / PM assumption, 46%)
**Claim:** 46% is the flow-through that delivers the *low end* of management's FY27-29 guidance; it assumes Diageo hits guidance. Its own history keeps far less.
**Evidence:** 20-F FY26 CEO letter: "We will invest this back to advance innovation, our overall competitiveness and to protect underlying profitability." FY17 results 6-K (27 Jul 2017): "two thirds being reinvested" (about 33% kept). 20-F FY23: GBP 450m of savings and only +15bps of margin (about 5% kept). Operating margin fell from 31.1% (FY22) to 28.9% (FY26) despite USD 1.7bn of productivity (FY24 annual report, via search summary). Source pack: `docs/phase3/savings-flow-through-evidence.md`.

| Flow-through | Value | Impact | Rating |
|---|---|---|---|
| 40% | 1,505p (1,504.9p) | **-20p** | **SELL** (-10.0%, by 0.8p) |
| 33% (2017 rule) | 1,482p | **-42p** | **SELL** (-11.4%) |
| 25% (FY22-24 record, brief bear) | 1,456p | **-68p** | **SELL** (-13.0%) |

Phasing is not the issue: slowing the supply-chain savings to 25/50/75/100% over FY27-30 costs only -1p (HOLD). The risk is how much is kept, not when it arrives.

## 2. Terminal returns: ROIC has fallen 5 points in three years (challenges the Valuation agent / PM's terminal RONIC 13.4%)
**Claim:** the +65p terminal-capex step assumes new investment earns 13.4% forever, but ROIC has gone 18.4% (FY23) -> 15.8% -> 13.7% -> 13.4% (FY26) (20-F FY24-FY26 KPI tables, FY26 p.18), and the 5-year capex average (7.1% of sales) implies only 10.8%.
**Evidence:** `docs/phase3/terminal-capex-evidence.md`; capex/sales FY22-26 7.1%, 6.9%, 7.5%, 8.0%, 6.1% (20-F cash flow statements).

| Change | Terminal capex | Value | Impact | Rating |
|---|---|---|---|---|
| RONIC 10.8% | 7.07% of sales | 1,460p | **-65p** | **SELL** (-12.7%) |
| (check: 5-year average 7.11% held forever) | 7.11% | 1,457p | -67p | SELL |
| RONIC = WACC (8.46%): growth creates no value | 8.30% | 1,368p | **-157p** | **SELL** (-18.2%) |

## 3. No recovery: management has missed its growth targets (challenges the Fundamentals agent and the brief's growth path)
**Claim:** the brief's path (0%, 1.5%, 2.5%, 3%, 3%) needs North America (USD 7,249m, -8.4% organic in FY26) to recover. Organic growth was 6.5% (FY23), -0.6%, 1.7%, -2.0% (FY26) (`fundamentals/commentary.md`, 20-F regional reviews pp.27-31). Moderation and GLP-1 use are a structural headwind in the US, though I have no sourced number for them (not quantified separately).
**Change:** zero organic growth FY27-31 -> **1,390p, -135p, SELL (-16.9%).** (Larger than last run's -49p; my reading is that the steady-state terminal year no longer lets lower growth release working capital in the terminal cash flow.)

## 4. Terminal growth 2% vs a shrinking spirits market (challenges the Data agent's industry check)
**Claim:** IWSR: global spirits volumes fell 3% in 2025 and are seen down about 2% by 2035 (secondhand: Drinks International, Federvini; `data/notes.md`). 2% nominal forever needs price/mix to offset falling volume indefinitely.
**Change:** terminal growth 1.5% -> **1,470p, -55p, SELL (-12.2%).** The impact is half last run's -110p because the RONIC rule also cuts terminal reinvestment when growth falls (capex 6.2% -> 5.5%).

## 5. Cost of capital: leverage after the dividend cut (challenges the Risk agent and the PM's 1% credit spread)
**Claim:** leverage is 3.14x, above the 2.5-3.0x range Diageo calls "broadly consistent with an A-band credit rating" (20-F p.186); the dividend was cut to defend it, and EABL / RCB proceeds (c.USD 3.3bn gross) had not been received at 30 June. Interest cover fell from 13.6x (FY22) to 7.0x (FY26) (`fundamentals/commentary.md`). Volatility is 31.6% (1y), 2.5x the FTSE 100 (`risk/notes.md`), and beta is not stable: own regressions range 0.37-0.77 depending on window.
- **Credit spread 2.0%** (pre-tax cost of debt 7.22%): **1,456p, -69p, SELL (-13.0%).**
- **Beta 1.00** (Risk agent FLAG 1): **1,481p, -44p, SELL (-11.5%).** Any beta above about 0.98 flips the rating (Valuation notes).

## Against the bear (the strongest case for the stock, checked honestly)
- **Beta 0.72** (Diageo's own 5y weekly regression, s.e. 0.11, R-squared 0.15; `risk/beta_evidence.json`): **1,832p, +307p, HOLD (+9.5%).** Still not a BUY (needs 1,924p). This is the single largest lever in the model, larger than all the bear challenges.
- **Restructuring cash after tax relief** at 24.3% (USD 850m -> 643m; tax relief is not confirmed by Diageo, Data agent): **1,532p, +7p, HOLD.** Immaterial.

## Retired: old challenge 6 (deducting the FY26 final dividend, -23p)
Retired. The 30c final dividend goes ex on **15 Oct 2026**, after the 12 Oct valuation date, so the 1,673p price is cum-dividend and the buyer receives it; nothing should be deducted (`data/notes.md`, Phase 3 additions; 20-F FY26). The valuation now rolls equity forward with `dividends_ex_before_valuation_musd` = 0, which is correct.

## Management's track record
- **Incentive targets 2023-26: all missed.** Organic sales CAGR -0.3% vs a 4.0% threshold; organic operating profit CAGR -3.4% vs 4.5% (20-F FY26 p.110).
- **Savings:** the 2017 programme planned to reinvest two thirds; FY23 converted GBP 450m of savings into +15bps of margin (sources in challenge 1).
- **Leverage:** target 2.5-3.0x, actual 3.35x (FY25) and 3.14x (FY26), ending in a dividend cut.
- **Capex:** peaked at 8.0% of sales in FY25 before management cut it to 6.1% in FY26, while ROIC fell to a four-year low.
Pattern: guidance has been met only at the low end or missed. The base case already assumes the low end of guidance is delivered, so it has no cushion.

## Not quantified (no sourced number for a single-change test)
- **Moet Hennessy (34%) at book, USD 5,107m**, tested at fair value less costs of disposal with headroom described as "sensitive" (20-F). Cognac and champagne are weak (Remy's depressed earnings). An impairment would cut the associates line, but I have no sourced fair value.
- **Minorities at book (USD 2,083m)**; USL's listed minority is likely worth more at market. **Disposal proceeds (USD 3,318m) are gross**, before tax and costs, and not yet received.
- **Restructuring cash is undiscounted** (paid FY27-29): discounting would add a little; it is a case for the stock, not quantified.

## Which single challenges flip HOLD to SELL (threshold 1,506p)
Flow-through 40% (by 0.8p), 33%, 25%; terminal RONIC 10.8% and RONIC = WACC; zero organic growth; terminal growth 1.5%; credit spread 2.0%; beta 1.00. **Nine of the eleven single bear changes flip the rating**; only the slower supply-chain phasing (-1p) does not. Neither upside test (beta 0.72, tax relief) reaches BUY.

**Strongest reason not to buy: the HOLD sits 18p above SELL and rests on Diageo delivering at least the low end of its own guidance with returns on new capital holding at 13.4% forever, when it has missed every 2023-26 target and its ROIC has fallen five points in three years.**
