# Coca-Cola: evidence audit of every input (13 Oct 2026, before the valuation runs)

Same test as the Diageo audit in Phase 3: does each number have a primary source, does it match what the DCF includes, and is it justifiable? Inputs file: runs/KO/2026-10-13/inputs.yaml.

## Verdicts
| Input | Value | Source | Verdict |
|---|---|---|---|
| Base revenue ex-CCBA | $44,309m | 10-K $47,941m less CCBA $3,632m (Coca-Cola HBC deal slides €3,357m x 1.082) | **Passes, now corroborated.** An independent data provider (MarketScreener) gives CCBA's 2024 revenue as $3.63bn and EBIT $267m, matching our conversion ($3,632m / $266m). The deal's pro forma total (€14.1bn) also adds up. The slide link is still worth a glance |
| Base margin ex-CCBA | 33.2% | Q4 2025 8-K comparable figures less CCBA | Passes (same corroboration) |
| Tax rate | 23.7% | 19.9% (Q2 2026 8-K) + 3.8 points (Q2 2026 10-Q, note 9) | Passes. Brief comment said note 12; corrected to note 9 |
| **IRS liability** | **$14,900m** | $14,000m to 31 Dec 2025 (10-K) + $900m for H1 2026 (10-Q) | **Fails: counts 2026 twice.** The $900m is the extra tax (and interest) from applying the court's method to 2026. The 23.7% tax rate already charges that extra tax on every year from FY26, and the valuation is at the 31 Dec 2025 balance sheet date. Fix: **$14,000m**, the liability at the balance sheet date. Impact c.+$0.21 a share |
| **Capex % of sales** | **3.99%** | 5-year average FY21-25 (10-K XBRL) | **Weak.** The average includes 2021 (3.5%, Covid-era spending). FY25 was 4.41%, and FY26 guidance ($2.2bn) is about 4.3-4.7% of sales. So the average looks too low, which flatters value. Fix: use **FY25's 4.41%**, the latest actual and closest to guidance. (Terminal capex is set by your 27% RONIC rule, so this only affects FY26-30.) |
| D&A % of sales | 2.68% | 5-year average | Passes (stable: 2.2-3.8%) |
| Working capital | -10.3% of sales | FY25 10-K | Passes. FY24 without the fairlife liability was -9.1%, so it is stable. Negative means growth releases cash |
| Net debt | $29,686m | 10-K balance sheet 31 Dec 2025 | Passes. CCBA's own debt is outside it, consistent with adding CCBA's sale price (an equity value) |
| Leases, pension, restructuring | $1,722m / 0 / 0 | 10-K notes | Pass |
| Minorities | $2,106m | 10-K, book | **Flag (conservative).** Includes CCBA's other owner, not disclosed separately. Could over-deduct by up to $1.1bn (c.$0.26 a share). Book value is used because outside shareholders are only 0.5% of value |
| Equity stakes | $46,626m | Listed at today's prices $39,540m (10-K fair values x price and FX change, Yahoo/FRED) + unlisted at book $6,236m + kept 25% of CCBA $850m | Passes. The Q2 10-Q discloses no sale of any stake, so holdings are taken as unchanged |
| CCBA proceeds | $1,300m | Deal terms | Passes (not yet received; sale not closed) |
| Shares, price, dividends | 4,302m / $90.12 / $6,840m | 10-K, 10-Q cover, Yahoo, dividend declarations | Pass |
| Risk-free | 5.22% | FRED DGS10 | Passes |
| **Beta** | **missing** | Damodaran site blocked | **STOP.** Needs the betas.xls file from you |
| Industry growth forecast | missing | research sites blocked | Flag. Only weak support (US alternative beverages +2.4% in 2025, Monster 10-K) for the 3% |
| Peer forward EBITDA | missing | no free consensus source | Flag. Comps will use trailing EV/EBITDA and forward P/E |
