# Bear case: Diageo (DGE), run 2026-10-12 (Phase 4 re-run, 13 Oct 2026: mid-year discounting)

**Base case: 1,627p (1,627.3p GBp; USD 21.54 per share), -2.7% vs 1,673p, HOLD** at a WACC of 8.46% (beta 0.96, terminal RONIC 13.4%, flow-through 46%, valued at 30 June 2026 with **mid-year discounting** (PM decision 13 Oct 2026; was end-of-year, 1,545p) and rolled forward to 12 Oct, restructuring cash USD 850m deducted, minorities proportionate: 2.566% x EV = USD 1,562m). **SELL starts at 1,506p (1,505.7p GBp), 122p below the base** (was 39p).
The engine's bear scenario (no organic growth, 25% flow-through, WACC +1 point) gives **1,180p GBp (-29.5%, SELL)**: three changes combined, shown for reference.

Method unchanged: one change at a time to an in-memory copy of the brief or `inputs.yaml`, re-run through `desk.valuation_run.build` (`run_challenges.py`, results in `challenges.json`; the script stops if its base does not reproduce `valuation/valuation.json`: it does, 1,627.3p). SELL-flip thresholds (engine bisection, matching `valuation/sanity_checks.json`): **flow-through below 9.1%, beta above 1.078, terminal RONIC below 9.26%, minorities above USD 5,041m (book basis) / share above 8.28%.**

## Results of every single change (GBp, vs 1,627.3p)
| # | Change | Value | Impact | Rating |
|---|---|---|---|---|
| 1 | Flow-through 40% | 1,607.5p | -19.8p | HOLD |
| 1 | Flow-through 33% (2017 "two thirds reinvested") | 1,584.4p | -42.9p | HOLD |
| 1 | Flow-through 25% (FY22-24 record) | 1,558.0p | -69.3p | HOLD |
| 1 | Supply-chain savings phased 25/50/75/100% | 1,626.5p | -0.8p | HOLD |
| 2 | Terminal RONIC 10.8% (capex 7.07% of sales) | 1,561.8p | -65.5p | HOLD |
| 2 | Terminal RONIC = WACC (capex 8.30%) | 1,468.3p | **-158.9p** | **SELL** |
| 3 | Zero organic growth FY27-31 | 1,490.7p | **-136.5p** | **SELL** |
| 4 | Terminal growth 1.5% | 1,571.6p | -55.7p | HOLD |
| 5 | Credit spread 2.0% | 1,559.3p | -68.0p | HOLD |
| 5 | Beta 1.00 | 1,584.5p | -42.7p | HOLD |
| 6 | USL minority at market + others at book (USD 5,778m) | 1,480.0p | **-147.3p** | **SELL** (upper bound) |
| check | Old book minorities (USD 2,083m) | 1,609.1p | -18.2p | HOLD |
| for | Beta 0.72 (own 5y weekly regression) | 1,929.6p | +302.3p | **BUY** (+15.3%, 6p above the 1,924p BUY line) |
| for | Restructuring cash after tax relief (850 -> 643) | 1,634.5p | +7.2p | HOLD |

**Three of the eleven single bear changes now flip the rating to SELL** (RONIC = WACC, zero growth, USL at market); before mid-year discounting it was nine. The evidence for each challenge is unchanged and kept below; only the values moved (every value rises by about 5% because all cash flows, including the terminal value, are discounted half a year less).

## Evidence for each challenge (unchanged from Phase 3; the values quoted inside were end-of-year values and are superseded by the table above)

## 1. Savings flow-through: the record says most savings get reinvested (challenges the Valuation agent / PM assumption, 46%)
**Claim:** 46% is the flow-through that delivers the *low end* of management's FY27-29 guidance; it assumes Diageo hits guidance. Its own history keeps far less.
**Evidence:** 20-F FY26 CEO letter: "We will invest this back to advance innovation, our overall competitiveness and to protect underlying profitability." FY17 results 6-K (27 Jul 2017): "two thirds being reinvested" (about 33% kept). 20-F FY23: GBP 450m of savings and only +15bps of margin (about 5% kept). Operating margin fell from 31.1% (FY22) to 28.9% (FY26) despite USD 1.7bn of productivity (FY24 annual report, via search summary). Source pack: `docs/phase3/savings-flow-through-evidence.md`.

| Flow-through | Value (GBp) | Impact (GBp) | Rating |
|---|---|---|---|
| 40% | 1,526p (1,525.8p) | -19p | HOLD (-8.8%) |
| 33.6% | 1,506p | -39p | **SELL line** (engine-solved) |
| 33% (2017 "two thirds reinvested" rule) | 1,504p (1,503.6p) | **-41p** | **SELL** (-10.1%, by 2p) |
| 25% (FY22-24 record, brief bear) | 1,478p | **-67p** | **SELL** (-11.6%) |

The flip point has moved from c.40% (book minorities) to **33.6%**: 40% is no longer a SELL. But 33.6% is almost exactly the 2017 rule Diageo itself announced, so the HOLD now needs Diageo to keep more of its savings than its own stated policy last time. Phasing is not the issue: slowing the supply-chain savings to 25/50/75/100% over FY27-30 costs only -1p (-0.7p, HOLD).

### 2. Terminal returns: ROIC has fallen 5 points in three years (challenges the Valuation agent / PM's terminal RONIC 13.4%)
**Claim:** the +65p terminal-capex step assumes new investment earns 13.4% forever, but ROIC has gone 18.4% (FY23) -> 15.8% -> 13.7% -> 13.4% (FY26) (20-F FY24-FY26 KPI tables, FY26 p.18), and the 5-year capex average (7.1% of sales) implies only 10.8%.
**Evidence:** `docs/phase3/terminal-capex-evidence.md`; capex/sales FY22-26 7.1%, 6.9%, 7.5%, 8.0%, 6.1% (20-F cash flow statements).

| Change | Terminal capex | Value (GBp) | Impact (GBp) | Rating |
|---|---|---|---|---|
| RONIC 11.66% (SELL line) | 6.75% of sales | 1,506p | -39p | SELL line (engine-solved) |
| RONIC 10.8% | 7.07% of sales | 1,482p | **-63p** | **SELL** (-11.4%) |
| (check: 5-year average 7.11% held forever) | 7.11% | 1,479p | -65p | SELL |
| RONIC = WACC (8.46%): growth creates no value | 8.30% | 1,392p | **-153p** | **SELL** (-16.8%) |

### 3. No recovery: management has missed its growth targets (challenges the Fundamentals agent and the brief's growth path)
**Claim:** the brief's path (0%, 1.5%, 2.5%, 3%, 3%) needs North America (USD 7,249m, -8.4% organic in FY26) to recover. Organic growth was 6.5% (FY23), -0.6%, 1.7%, -2.0% (FY26) (`fundamentals/commentary.md`, 20-F regional reviews pp.27-31). Moderation and GLP-1 use are a structural headwind in the US, though I have no sourced number for them (not quantified separately).
**Change:** zero organic growth FY27-31 -> **1,414p GBp, -131p, SELL (-15.5%).**

### 4. Terminal growth 2% vs a shrinking spirits market (challenges the Data agent's industry check)
**Claim:** IWSR: global spirits volumes fell 3% in 2025 and are seen down about 2% by 2035 (secondhand: Drinks International, Federvini; `data/notes.md`). 2% nominal forever needs price/mix to offset falling volume indefinitely.
**Change:** terminal growth 1.5% -> **1,491p GBp, -53p, SELL (-10.9%).** (The RONIC rule also cuts terminal reinvestment when growth falls: terminal capex 6.2% -> 5.5% of sales, which softens the hit.)

### 5. Cost of capital: leverage after the dividend cut, and an unstable beta (challenges the Risk agent and the PM's 1% credit spread)
**Claim:** leverage is 3.14x, above the 2.5-3.0x range Diageo calls "broadly consistent with an A-band credit rating" (20-F p.186); the dividend was cut to defend it, and the EABL / RCB proceeds (c.USD 3.3bn gross) had not been received at 30 June. Interest cover fell from 13.6x (FY22) to 7.0x (FY26) (`fundamentals/commentary.md`). Volatility is 31.6% (1y), 2.5x the FTSE 100 (`risk/notes.md`), and beta is not stable: own regressions range 0.37-0.77 depending on window (`risk/beta_evidence.json`).
- **Credit spread 2.0%** (pre-tax cost of debt 7.22%): **1,478p GBp, -67p, SELL (-11.7%).**
- **Beta 1.00** (Risk agent FLAG 1): **1,502p GBp, -42p, SELL (-10.2%, by 3p).** The SELL line is beta 0.997, only 0.04 above the 0.96 we use.

### 6. Minorities: the new method takes the cheapest view of the outside shareholders (challenges the Valuation agent / PM decision of 2026-10-13)
**Claim:** proportionate minorities value the outside shareholders at the group's own DCF multiple: USD 1,500m is **10.8x** their USD 139m of operating profit (ex-EABL). The market values the largest of them far higher. United Spirits (USL) is listed: its 42.79% outside stake (100% - Diageo's 57.21%, `inputs.yaml`) x 727.35m shares x INR 1,362.5 / 95.285 INR per USD (Yahoo Finance, 12 Oct 2026) = **USD 4,450m** at market, versus USD 755m at book (20-F FY26 p.189) and about USD 1.5bn implied for *all* minorities by our method. USD 4,450m on its own is **31.9x** the operating profit of all minorities combined (ex-EABL), so whatever share of that profit is USL's, the market's multiple on it is at least 31.9x, vs our 10.8x (both in `challenges.json`).
**Change (one change, computed with `desk.valuation_run.build`, book-method bridge with minorities = USL outside stake at market USD 4,450m + other minorities at book USD 1,328m = USD 5,778m):** **1,395p GBp, -150p, SELL (-16.6%).** The rating flips at minorities of **USD 2,619m** on this basis (or a 4.48% share under the proportionate method).

| Minorities method | Minorities (USD m) | Value (GBp) | Impact (GBp) | Rating |
|---|---|---|---|---|
| Proportionate (base, PM decision) | 1,500 | 1,545p | 0 | HOLD (-7.7%) |
| Book (old method; includes EABL's 35%) | 2,083 | 1,524p | -20p | HOLD (-8.9%) |
| SELL line | 2,619 | 1,506p | -39p | SELL line |
| USL at market + others at book | 5,778 | 1,395p | **-150p** | **SELL** (-16.6%) |

**Counter-argument (and why I do not push this as the base case):** this mixes two valuations of the same profits. It deducts USL's minorities at USL's market multiple (c.51x earnings, the figure given with the PM decision; I have not verified it against USL's own filings), while our DCF values *all* of USL's profits, including Diageo's 57.21%, at roughly the group's 10.8x. If the market is right about USL, Diageo's own 57% is also worth far more than the DCF credits it with, and a consistent sum-of-the-parts would add that back; deducting only the outside slice at market takes the cost of the rich multiple without the benefit. In addition, the "others at book" USD 1,328m still contains EABL's 35% outside shareholders, the double count the PM removed (I have no sourced split, so the -150p is overstated by that amount), and the method ignores USL's net cash. So -150p is an **upper bound**. The honest bear point is narrower: the minorities line is a method choice worth up to 150p, the proportionate method sits at the low end of the range, and the HOLD depends on it staying there: the flip needs minorities of USD 2,619m vs the USD 1,500m used, well inside the USD 755m (book) to USD 4,450m (market) range for USL's stake alone.

### Against the bear (the strongest case for the stock, checked honestly)
- **Beta 0.72** (Diageo's own 5y weekly regression, s.e. 0.11, R-squared 0.15; `risk/beta_evidence.json`): **1,844p GBp, +299p, HOLD (+10.2%).** Still not a BUY (needs 1,924p; beta below 0.666). This remains the single largest lever in the model.
- **Restructuring cash after tax relief** at 24.3% (USD 850m -> 643m; tax relief is not confirmed by Diageo, Data agent): **1,552p GBp, +7p, HOLD.** Immaterial.
- **The proportionate minorities fix itself (+20p, 1,524p -> 1,545p) is a fair correction** of the EABL double count; I challenge only its level vs market (challenge 6), not the removal of EABL.

### Retired: old challenge 6 (deducting the FY26 final dividend)
Retired. The 30c final dividend goes ex on **15 Oct 2026**, after the 12 Oct valuation date, so the 1,673p price is cum-dividend and the buyer receives it (`data/notes.md`, Phase 3 additions; 20-F FY26). The number 6 is now used for the minorities challenge.

## Management's track record
- **Incentive targets 2023-26: all missed.** Organic sales CAGR -0.3% vs a 4.0% threshold; organic operating profit CAGR -3.4% vs 4.5% (20-F FY26 p.110).
- **Savings:** the 2017 programme planned to reinvest two thirds; FY23 converted GBP 450m of savings into +15bps of margin (sources in challenge 1).
- **Leverage:** target 2.5-3.0x, actual 3.35x (FY25) and 3.14x (FY26), ending in a dividend cut.
- **Capex:** peaked at 8.0% of sales in FY25 before management cut it to 6.1% in FY26, while ROIC fell to a four-year low.
Pattern: guidance has been met only at the low end or missed. The base case already assumes the low end of guidance is delivered, so it has no cushion.

## Not quantified (no sourced number for a single-change test)
- **Moet Hennessy (34%) at book, USD 5,107m**, tested at fair value less costs of disposal with headroom described as "sensitive" (20-F). Cognac and champagne are weak (Remy's depressed earnings). An impairment would cut the associates line, but I have no sourced fair value.
- **Disposal proceeds (USD 3,318m) are gross**, before tax and costs, and not yet received.
- **GLP-1 / moderation:** no sourced volume effect; it sits inside challenges 3 and 4.
- **Restructuring cash is undiscounted** (paid FY27-29): discounting would add a little; a case for the stock, not quantified.

## Which single challenges flip HOLD to SELL (SELL below 1,505.7p GBp)
Terminal RONIC = WACC; zero organic growth; USL minority at market (an upper bound). The other eight do not. On the other side, beta 0.72 (Diageo's own best regression) reaches BUY by 6p.

**Strongest reason not to buy:** the base case already assumes the low end of guidance is delivered by a management team that missed both of its 2023-26 incentive targets, and the case for a BUY rests on a beta (0.72) with an R-squared of 0.15.
