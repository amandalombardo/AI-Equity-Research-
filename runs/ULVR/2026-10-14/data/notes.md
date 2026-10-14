# Data agent notes: Unilever PLC (ULVR), run 2026-10-14

All money amounts are EUR m unless labelled otherwise. Share prices: ULVR in pence (GBp), MKC in USD, MICC.AS in EUR, HUL in INR.
Every value in `../inputs.yaml` carries its source (document + page/section, or URL). Scripts: `build_inputs.py`, `build_peers.py` (re-runnable from the repo root).

## 000. priced_at_valuation_date_meur added (14 Oct 2026, mistakes log row 24)
`add_priced_at_valuation_date.py` adds a single key to `../inputs.yaml`: **priced_at_valuation_date_meur = EUR 35,890.5m**. That is the TMICC stake at the 13 Oct 2026 MICC.AS close, **1,935.2** (component 1 of `associates`: 121,604,413 x EUR 15.914), plus the Foods consideration at the 13 Oct McCormick price, **33,955.3** (`disposal_proceeds`). Both are already at run-date market prices, so the engine must not grow them by the cost of equity in the roll-forward from 31 Dec 2025.
Left out because they are 31 Dec 2025 values: the JVs (Gordon growth on FY25 dividends, 3,876.4), associates at book (15), fair-value investments (902) and the Magnum transition balance (500).
The script checks that the TMICC figure matches the `associates` source and that no other key changed (verified by comparing the file before and after). If `associates` or `disposal_proceeds` is recomputed, re-run the script.

## 00. PM decision 10 applied (14 Oct 2026, docs/phase5/ulvr-run-flags.md items A-D)
Applied by `apply_pm_decision10.py`. It changes only these three keys in `../inputs.yaml`; every other key, including beta, minority_share_of_operating_profit and buybacks_after_balance_sheet_meur, is unchanged (checked by comparing the file before and after). `build_inputs.py --write-inputs` now leaves these three keys alone.

| Input | Was | Now | Arithmetic (script) |
|---|---|---|---|
| capex_pct_sales | 0.028 | **0.0315** | (PP&E 1,417 + intangibles 174) / 50,503 = 3.150% (20-F p.132; XBRL PurchaseOfPropertyPlantAndEquipment..., PurchaseOfIntangibleAssets...) |
| nwc_pct_sales | -0.07821 | **-0.11979** | (4,043 + (7,346 - 2,100 due from TMICC) - (16,939 - 1,600 due to TMICC)) / 50,503 = -11.98% (20-F p.131; note 13 p.159 "include EUR 2.1 billion due from TMICC"; note 14 p.160 "include EUR 1.6 billion due to TMICC") |
| associates | 2,044.2 | **7,228.7** | sum of the five parts below |

Associates, EUR m:
1. TMICC: 121,604,413 shares x EUR 15.914 (MICC.AS close, 13 Oct 2026) = **1,935.2**
2. Joint ventures, Gordon growth: 229 x 1.016 / (7.602% - 1.6%) = **3,876.4**. Cost of equity 7.602% = risk-free 3.18% + beta 0.8844 x ERP 5.0% (both from inputs.yaml).
   - **Source check:** the EUR 229m is in 20-F note 11, p.158: joint ventures "Dividends received/reductions (229)", associates nil. The cash-flow line on p.132, "Dividends from joint ventures, associates and other non-current investments", is **243**, because it also includes dividends from other investments. Those investments are valued in item 4, so 229 is the right figure and avoids double counting. The brief comment says "20-F cash flow" for 229; the figure is correct, but its location is note 11.
   - If the run's cost of equity changes (e.g. a new beta), this value must be recomputed: re-run the script.
3. Associates at book: **15** (note 11).
4. Other fair-value financial investments: equity investments at FVOCI excluding TMICC 561 (2,216 - 1,655) + non-current fair value through P&L "Other" 341 = **902** (note 17A, p.174, confirmed). Amortised-cost assets of 368 (including judicial deposits of 175) are excluded.
5. Net Magnum transition balance owed to Unilever: 2,100 - 1,600 = **500** (notes 13-14). Both amounts are disclosed rounded to EUR 0.1bn.

These supersede section 3 FLAGs 3 (working capital), 5 (joint ventures), 6 (other investments) and 10 (capex), and the corresponding rows of section 4. Confidence: capex high; working capital medium (both Magnum amounts rounded to EUR 0.1bn); associates medium (the JV part depends on the cost of equity and on dividends continuing at the FY25 level). New source rows in financials.csv: receivable_due_from_tmicc_in_trade_receivables, dividends_from_jvs_associates_and_other_investments_cash_flow, other_equity_investments_fvoci_ex_tmicc, other_financial_assets_fvtpl_noncurrent, financial_assets_amortised_cost_noncurrent.

## 0. Corrections after hand-off (14 Oct 2026)
**Continuing vs total figures in financials.csv (reported by the Fundamentals agent; verified against the FY25 20-F).** Two XBRL tags hold group TOTALS that include the discontinued Ice Cream business, but the rows were labelled as continuing operations: `ifrs-full:ProfitLossAttributableToOwnersOfParent` and `ifrs-full:CashFlowsFromUsedInOperatingActivities`. FY25 profit also includes the EUR 3,373m demerger gain. Corrected rows (EUR m):

| Row | Was (total) | Now (continuing) | Source |
|---|---|---|---|
| net_profit_to_owners FY23 | 6,487 | 6,002 | 20-F p.128 income statement, "Total profit attributable to shareholders' equity arises from: Continuing operations" |
| net_profit_to_owners FY24 | 5,744 | 5,430 | same (not in the coordinator's list: same error) |
| net_profit_to_owners FY25 | 9,469 | 5,682 | same |
| operating_cash_flow FY23 | 9,426 | 8,393 | 20-F p.132 cash flow statement, "Net cash flow from continuing operating activities" (after tax paid) |
| operating_cash_flow FY24 | 9,519 | 8,461 | same |
| operating_cash_flow FY25 | 8,350 | 8,052 | same |

The totals are kept as separate rows: `net_profit_to_owners_total_incl_discontinued` and `operating_cash_flow_total_incl_discontinued` (FY23-25, labelled "NOT for forecasting"). The FY21-22 rows remain Group totals as first reported (including Ice Cream). Their source now says they are not comparable with FY23-25.
I checked the other XBRL flow items: income tax (`...ContinuingOperations`), profit before tax, D&A, capex, restructuring and revenue are on the continuing basis, so they are unchanged.
**inputs.yaml did not depend on these rows** (the FCF tie-out uses the 6-K continuing figure of 10,772; no input uses net profit or the XBRL operating cash flow). The fix is in `build_inputs.py`, which checks that the replaced value equals the XBRL total.
**Process note:** re-running `build_inputs.py` briefly overwrote the shared `../inputs.yaml` and removed the Risk agent's `beta` and the Fundamentals agent's `minority_share_of_operating_profit`. I restored it at once from git (commit f26cb99), so it is unchanged. The script now writes inputs.yaml only with `--write-inputs`, and then keeps every key it does not own. Its buyback key now matches the committed name `buybacks_after_balance_sheet_meur`. Since hand-off that buyback is deducted in the engine's roll-forward (mistakes row 22), so FLAG 2 below is resolved.

## 1. What I did and fetched
1. `python -m desk.data_sources briefs/ULVR.yaml runs/ULVR/2026-10-14/data` (with SEC_CONTACT_EMAIL set) ran without errors: `financials_raw.csv` (XBRL from the FY21-FY25 20-Fs), `prices.csv` (ULVR.L, ^FTSE), `market_inputs.json` (Bund 3.18% Aug 2026; EUR per GBP 1.18190 on 9 Oct 2026). The script listed some XBRL items as missing: equity-method investments (Unilever does not use that tag), held-for-sale assets, and FY21 gross borrowings. I took the ones I needed from the 20-F text instead.
2. Primary filings read (text copies already downloaded, re-cited with their accession numbers): FY25 20-F (0000217410-26-000007), FY25 results 6-K (0001654954-26-001155), H1 2026 6-K (0000217410-26-000057), Foods/McCormick Form 425 investor presentation (0000217410-26-000027) and call transcript (0000217410-26-000032), McCormick 10-Q to 31 Aug 2026 (0000063754-26-000329), FY21-FY24 results 6-Ks.
3. Fetched live from SEC EDGAR today: Unilever's filing index (latest filing 25 Sep 2026), the Total Voting Rights 6-Ks for Mar, Apr, May, Aug and Sep 2026, the buyback 6-K (0001654954-26-004088), every TMICC filing since April 2026 (CIK 0002071668: 6-Ks, 424B3 supplements, 13G/A), McCormick's filing index and 8-Ks, the Kimberly-Clark Q2 2026 10-Q and its Kenvue 8-Ks, and the 10-K/20-F texts of PG, CL, Church & Dwight, Coty, Estée Lauder, Kenvue and Haleon (for the industry forecast). Peer figures come from SEC XBRL companyfacts.
4. Yahoo Finance: closes on 13 Oct 2026 for ULVR.L, MKC, MICC.AS, HINDUNILVR.NS, EURUSD=X and EURGBP=X; MICC.AS on 30 Jun 2026; peer prices, consensus EPS, and the European peers' figures. FRED: DEXUSEU, DEXUSUK, DEXINUS (9 Oct 2026), IRLTLT01DEM156N, BAMLC0A3CA.
5. Could not reach: Statista, McKinsey, Euromonitor, research-firm sites, the company websites (Unilever, L'Oreal, Beiersdorf, Henkel, Reckitt, HUL), and the SEC full-text search (403). Only SEC, Yahoo and FRED work from this environment.

## 2. Tie-out (base year FY25 vs brief `checks.published_fy25`, tolerance 0.5%): `tie_out.csv`
| Item | Brief | Data agent | Diff | Result |
|---|---|---|---|---|
| Turnover | 50,503 | 50,503 (XBRL ifrs-full:Revenue = 6-K) | 0.00% | OK |
| Underlying operating profit | 10,084 | 10,084 (6-K: operating profit 9,037 + non-underlying 1,047) | 0.00% | OK |
| Underlying margin | 20.0% | 19.97% | -0.16% | OK (rounding) |
| Free cash flow | 5,900 | 5,921 (6-K FCF reconciliation) | +0.36% | OK (brief rounds to EUR 0.1bn) |
| Net debt | 23,100 | 23,076 (6-K net debt reconciliation) | -0.10% | OK (rounding) |

All five tie out within 0.5%, so no tie-out FLAG.

## 3. FLAGs
1. **The share price written by desk.data_sources was an intraday price.** It wrote 4,737p "close" dated 14 Oct 2026, but at download time (about 08:50 UTC) the London session had only just opened. I used the last completed close: **4,710.5p on 13 Oct 2026**. MICC.AS and HINDUNILVR.NS prices are also 13 Oct closes, so all prices share one date. Code fix suggested for Amanda (on a branch): `last_close` should drop today's bar while the market is open.
2. **The EUR 1.5bn share buyback in H1 2026 is not in the bridge (about 59p a share).** Net debt is at 31 Dec 2025 (before the buyback), but `shares_outstanding_m` (2,154.3m, as instructed) is after it: 30,703,780 shares were bought back for EUR 1,507m (H1 2026 cash flow) and are now held in treasury. The engine deducts only dividends when it rolls the value forward, so this mismatch overstates value by about EUR 1,507m / 2,154.3m / 1.1819 = **about 59p a share**. Two consistent fixes: add 1,507 to the roll-forward deduction, or use the 2,184.9m shares in issue before the buyback (TVR 6-K at 31 Mar 2026). I recorded it as `buyback_after_balance_sheet_meur` (the engine does not read this field). This is for the valuation agent and the PM to decide.
3. **Working capital trap (nwc_pct_sales).** The brief's formula, applied to the XBRL items, gives (4,043 + 7,346 - 16,939) / 50,503 = **-10.99%**. But FY25 payables include a one-off **EUR 1.6bn due to TMICC** (inventory subsidy and transitional services, 20-F note 14, p.160). That balance comes from the demerger and will be paid out, not repeated. I entered **-7.82%** (without it). On trade items only (trade receivables 4,852, trade payables 10,994) the ratio would be -4.16%. Payables also include accruals of 4,649 (mostly operating, e.g. promotions), which I kept. Prepayments jumped from 506 to 1,369 (reason not explained). The FY25 balance sheet still includes the Foods perimeter. The impact is small (about EUR 20m of cash a year at 1.6% growth), but the PM should confirm.
4. **The EUR 1.6bn payable to TMICC may be debt-like (about 63p a share).** If it is settled in cash, it is a claim on value that sits in neither net debt nor the forecast. Not added; for the PM to decide.
5. **Joint ventures valued at book (94 + 15) although they earn EUR 245m a year.** That share of profit sits below operating profit, so the DCF does not include it. Most of it is in Foods (224, mainly the Pepsi Lipton tea partnerships), and the perimeter EXCLUDES "Lipton Ready-to-Drink", so those partnerships appear to stay with Unilever. FY25 dividends received: 229. Each 10x multiple on 245 = EUR 2.45bn = **about 96p a share**. I followed the brief rule (book value); the PM should review.
6. **Other non-current financial investments not in the bridge: about EUR 1.27bn** (20-F note 17A, p.174: non-current financial assets 3,065, less derivatives 140 already in net debt, less TMICC 1,655). These include other equity investments at fair value (561), assets at fair value through profit or loss (341) and assets at amortised cost (368, of which judicial deposits 175). About 50p a share. Not added (not in the brief).
7. **Timing of the Foods consideration (for the valuation agent).** The base case counts EUR 33,955m (consideration at today's market value) as if received today. Closing is expected mid-2027, about 0.71 years after the run date. Each 1 point of annual discount rate on that delay = about EUR 239m = **about 9p a share**; at an illustrative 6% it is about EUR 1.4bn (about 54p). The McCormick shares also carry market risk until closing.
8. **Foods cash flows until closing: MISSING.** The perimeter's cash flows from 1 Jan 2026 to closing are not disclosed (not in the H1 2026 6-K, the Form 425 deck or McCormick's filings; no S-4 filed yet). Indicator only, my own arithmetic and not a filing figure: perimeter FY25 UOP of 2,600 x 1.5 years x (1 - 26%) = about EUR 2.9bn before capex and working capital (about 113p a share), if the economics until closing belong to Unilever. The merger agreement terms ("subject to certain adjustments") are not checked. H1 2026: the Foods business group (wider than the perimeter) had turnover EUR 6.3bn and a 23.3% UOM. Items 7 and 8 work in opposite directions and partly offset, as the brief expects.
9. **Tax on the USD 15.7bn cash: MISSING, not deducted** (PM decision 5). I searched the 20-F, the H1 2026 6-K, the Form 425s and McCormick's 10-Q: there is no figure. Each EUR 1bn of tax = 1,000 / 2,154.3m / 1.1819 = **39.3p a share**.
10. **Capex excludes intangibles.** The PM's 2.8% is PP&E only. Software and intangibles purchases were 174 in FY25: including them, capex would be 3.15% of sales instead of 2.81%, while the 2.6% D&A already includes amortisation. For the PM; brief not changed.
11. **The five-year table mixes bases.** In financials.csv, FY21-FY22 are the Group as first reported (including Ice Cream). FY23-FY25 income items are re-presented without Ice Cream, but balance sheets up to FY24 still include Ice Cream. The source column labels the basis of each row (net profit and operating cash flow corrected to continuing for FY23-25, see section 0). For example, D&A was 1,746 in FY21 against 1,147 in FY23. Averages across those years are not like for like (that is why the PM uses FY25 ratios).
12. **Debt weight.** 16.1% uses net debt at 31 Dec 2025 (23,076) against today's market cap (EUR 119,939m). With the latest net debt (30 Jun 2026: 25,961) it would be 17.8%. For the Risk agent.
13. **Peers.** Kimberly-Clark is distorted by its pending Kenvue acquisition (the price reflects the deal, the LTM figures do not) and its pending IFP joint venture. Colgate's LTM EBITDA and earnings are depressed by the Q4 2025 Filorga impairment (USD 919m before tax). Henkel has two share lines (I added the ordinary HEN.DE to the preferred HEN3.DE; without that, EV/EBITDA read 4.3x). Reckitt's LTM P/E may include disposal effects. All European peer figures come from Yahoo (marked as non-filing sources). NTM EBITDA is MISSING for all peers. PG's LTM is FY26 (to 30 Jun 2026).
14. **Restructuring guide** (supports the PM's 1.1%): the H1 2026 6-K expects FY26 restructuring of "around 1.0% of turnover", against management's 0.6% medium-term guide.

## 4. Inputs and confidence
| Input | Value | How | Confidence |
|---|---|---|---|
| base_sales | EUR 39,803m | 50,503 (6-K / XBRL) - 10,700 perimeter (Form 425 slide 25) | Medium-high (perimeter rounded to EUR 0.1bn, preliminary carve-out) |
| base_margin | 0.177 | PM decision 3: 18.80% ex-perimeter less 1.12% FY23-25 restructuring | Medium (perimeter UOP rounded) |
| tax_rate | 0.26 | PM decision 9; H1 2026 underlying ETR 26.0%, guide "around 26%" | High |
| da_pct_sales | 0.026 | PM; FY25 1,310 / 50,503 = 2.59% | High |
| capex_pct_sales | 0.028 | PM; FY25 1,417 / 50,503 = 2.81% (PP&E only, FLAG 10) | High on the figure, medium on the definition |
| nwc_pct_sales | -0.0782 | Without the TMICC 1.6bn (FLAG 3) | Medium |
| risk_free | 0.0318 | FRED IRLTLT01DEM156N, Aug 2026 | High |
| pre_tax_cost_of_debt | 0.0377 | Historic: 1,098 / average gross debt 29,126 (reference; engine uses 3.18% + 0.70%) | High |
| debt_weight | 0.1614 | 23,076 / (23,076 + 119,939) | Medium (FLAG 12) |
| net_debt | EUR 23,076m | Unilever definition, leases INSIDE | High |
| lease_liabilities | 0 | EUR 1,326m is inside net debt | High |
| minority_interests | EUR 2,057m (book) | Reference only (proportionate method; Fundamentals agent supplies the ratio) | High (book value) |
| pension_deficit | 0 | Net surplus EUR 3,518m | High |
| associates | EUR 2,044.2m | TMICC 121,604,413 x EUR 15.914 = 1,935.2 + JVs 94 + associates 15 | High for TMICC (30 Jun cross-check: book 1,852 / 121.6m = EUR 15.23 vs MICC.AS close EUR 15.236); low for the JVs (FLAG 5) |
| disposal_proceeds | EUR 33,955.3m | USD 15,700m + 499,691,175 MKC shares x USD 44.64 = USD 38,006m / 1.1193 | Medium (market value moves daily; untaxed; received mid-2027) |
| restructuring_cash | EUR 500m | Brief / Form 425 slide 19 | Medium (management estimate) |
| shares_outstanding_m | 2,154.327621 | TVR 6-K, 31 Aug 2026 (no later TVR on EDGAR) | High (but see FLAG 2) |
| fx_eur_per_gbp | 1.18190 | FRED cross rate, 9 Oct 2026 (Yahoo 13 Oct: 1.1837) | High |
| share_price_gbp_pence | 4,710.5 | ULVR.L close 13 Oct 2026 | High |
| stub_years | 0.78630 | 287 / 365 | High |
| dividends_ex_before_valuation_meur | EUR 3,038.8m | 2,034 (Q4 25 + Q1 26, H1 equity statement) + 0.4664 x 2,154.3m (Q2 26) | High |
| beta | not filled | Left for the Risk agent | n/a |

Extra fields for other agents: `buyback_after_balance_sheet_meur` 1,507; `tmicc_payable_meur` 1,600; `hul_market_value_meur` 40,700.7. That is 2,349.6m shares (Yahoo, not from a filing) x INR 1,875.5 / 108.27 INR per EUR, so the 38.1% outside holders' share = **EUR 15,507m** (bear line). `foods_perimeter_interim_cash_flows_meur` is MISSING. Unilever's 61.90% stake in HUL is from the 20-F related undertakings list (p.194; p.183 rounds it to 62%).

The sale terms checked against McCormick's 10-Q: Unilever shareholders get 55.1% of the enlarged company, Unilever keeps 9.9%, McCormick's current holders keep 35.0%, plus a USD 15.7bn cash payment "subject to certain adjustments". McCormick's existing shares are 14,522,864 voting + 254,541,615 non-voting = 269,064,479. New shares = 269,064,479 x 65/35 = 499,691,175 (the brief's "about 500m").

TMICC sell-down check: no sale found. Unilever's 6-Ks to 25 Sep 2026 contain only voting rights and director dealings. TMICC's 6-Ks from August to September 2026 are share purchases for its incentive plans, director dealings and an AGM update; the 424B3 supplements still cover "up to 121,604,413" shares. The H1 2026 6-K carries the stake at EUR 1,852m.

## 5. Independent industry forecast (long-run growth check)
**An independent FORWARD forecast for the household and personal care market is MISSING.** Every research publisher's site (Euromonitor, Statista, McKinsey, Circana, NielsenIQ, Grand View and others) is blocked from this environment, and the US peers' 10-Ks give no market forecasts. The closest third-party data I could source:
- **Euromonitor, as cited by Unilever:** "2.0% 3YR CAGR market volume growth", the turnover-weighted market volume growth of the remaining HPC portfolio (Form 425 investor presentation 0000217410-26-000027, slide 11). It is backward-looking, volume only and chosen by the company. Not independent in the strict sense.
- **Haleon FY25 20-F** (accession 0001104659-26-027443, "Haleon at a glance", p.2-3), based on Nicholas Hall, GlobalData, IQVIA, Circana and NIQ data: consumer health "combined category growth at 3-4%". This is an adjacent category (OTC health, oral care), not HPC.

**Reading against the brief (my own arithmetic, labelled):** market volume of about 2% plus price of about 1.5-2% gives about 3.5-4% local-currency market growth, which matches the low end of Unilever's 4-6% USG target. Less the brief's 2.4-point FY17-25 currency drag, that is about **1.1-1.6% a year in euros**. The PM's 1.6% (FY27-30 and terminal) is at the top of that range: it needs Unilever to grow at least in line with its markets and currency drag not to worsen. **Supports, does not challenge** the 1.6%, with no room for a higher rate. The 0.2% bear growth is below the market-only path.

## 6. Missing items (each stopped there; nothing estimated silently)
- Tax and separation costs on the Foods sale (PM decision 5: not deducted).
- Foods perimeter cash flows from 1 Jan 2026 to closing (indicator only, FLAG 8).
- NTM EBITDA for all peers (no free consensus source).
- Independent forward HPC market forecast (section 5).
- HUL share count from a filing (HUL's own filings are not reachable; Yahoo's figure is used and marked as non-filing).
- No Total Voting Rights 6-K for 30 Sep 2026 on EDGAR at the run date. I used the latest one, at 31 Aug 2026.

## 7. Files
`financials_raw.csv` (desk.data_sources), `financials.csv` (171 rows, FY21-FY25 plus filing-text items, each with document and page), `tie_out.csv`, `market_inputs.json`, `market_data.json` (all closes and FX used), `prices.csv`, `peers.csv`, `build_inputs.py`, `build_peers.py`; run-level `../inputs.yaml`. A test load of inputs.yaml in `desk.valuation_run` worked, using a placeholder beta and minority ratio in a scratch copy only (no valuation was written to the run folder).
