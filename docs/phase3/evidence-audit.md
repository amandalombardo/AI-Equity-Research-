# Evidence audit of every model input (13 Oct 2026, before merging Phase 3)

The test is the PM's: every input must be backed by evidence and be justifiable. Values are in pence per share; the result before this audit was 1,524p (HOLD); after the minorities fix it is 1,545p (HOLD).

## Passes (sourced to a filing, a market price, or a PM rule with recorded evidence)
| Input | Value | Evidence |
|---|---|---|
| Base sales and margin ex-EABL | USD 18,505.5m, 29.36% | 20-F FY26; EABL annual report (checked) |
| Growth path | 0 / 1.5 / 2.5 / 3 / 3% | Low end of management guidance (PM, Phase 1) |
| Savings and flow-through | USD 1,000m, 46% | CMD 6-K 6 Aug 2026; low end of profit guidance (PM, Phase 3) |
| Tax, D&A, forecast capex, working capital | 24.3%, 3.38%, 7.11%, 37.58% | 20-F FY22-26 |
| Terminal capex | 6.21% (RONIC 13.4%) | 20-F ROIC history; value driver formula (PM, Phase 3) |
| Risk-free, beta, cost of debt | 5.22%, 0.96, Rf + 1% | FRED; Damodaran bottom-up; PM rules with evidence (first run) |
| Net debt, associates, shares, FX, price | as in results.md | 20-F notes; FRED; Yahoo |
| Disposal proceeds | USD 3,318m | 20-F p.85; USL/press for RCB (gross, flagged) |
| Restructuring cash | USD 850m | CMD 6-K (pre-tax, conservative) |
| Valuation date and dividend | 30 June, rolled forward; 0 dividend | 20-F: ex-date 15 Oct, after the valuation date |

## Supporting evidence only (secondhand, but it does not set any number in the DCF)
Damodaran capex by industry; the Guinness $670m capex figure; FY22-24 $1.7bn productivity; IWSR volumes; Campari and Remy EPS (comps only, which do not set the rating).

## PM assumptions agreed in Phase 1, still flagged by the Bear agent (unchanged in Phase 3)
Terminal growth 2% (IWSR sees falling volumes; 1.5% gives 1,470p, a SELL) and ERP 5%. These were your decisions with the brief; they are shown as risks in the memo.

## FIXED: minority interests (was USD 2,083m at book value; failed the test)

**Decision (PM, 13 Oct 2026): proportionate.** Minorities now = 2.57% x enterprise value = USD 1,500m. Result 1,545p, HOLD (-7.7%). Mistakes log row 14.
Two problems, both found in this audit:
1. **Book value is an accounting number, not what the minority stakes are worth.** USL (42.79% minority) is listed: at INR 1,362.5 (Yahoo, 12 Oct 2026) x 727.35m shares / 95.285 INR per USD, the minority's stake is worth USD 4,450m, against a book value of USD 755m.
2. **Double count:** the USD 2,083m includes the 35% outside shareholders of EABL (Diageo owns 65% through Diageo Kenya, 20-F). We removed all of EABL's profit and add only Diageo's sale proceeds, so deducting EABL's minority as well counts it twice. EABL's minority book value is not disclosed separately.

### Options
| Method | Minorities deducted | Value | Rating |
|---|---|---|---|
| **Proportionate (recommended):** minorities' share of operating profit (USD 227m, 20-F ROIC table, less EABL's 35% x USD 250m = USD 88m) = 2.57% of operating profit ex-EABL, applied to our enterprise value | USD 1,500m | **1,545p** | **HOLD (-7.7%)** |
| Book value (today) | USD 2,083m | 1,524p | HOLD (-8.9%) |
| USL minority at market price, other minorities at book | USD 5,778m | 1,395p | SELL (-16.6%) |

**Why proportionate:** it values the minorities' share of the business the same way the DCF values the whole business (Damodaran's recommended approach when the DCF uses consolidated cash flows), and it removes the EABL double count.

**Why not market:** USL trades at about 51x its profit (USD 10.4bn market value vs USD 202m profit, 20-F), while our DCF values those same profits at Diageo's multiple. Deducting the minority at the Indian market's price, but counting USL's profit at ours, mixes two valuations. If we used market prices consistently, we would also have to add Diageo's own 57% of USL at market (about USD 5.95bn), which would push the value up, not down.

**Weakness of proportionate:** it is an estimate. It uses operating profit shares, ignores USL's net cash, and assumes EABL's minorities are 35% of EABL's EBIT (EABL's own subsidiaries have minorities too).
