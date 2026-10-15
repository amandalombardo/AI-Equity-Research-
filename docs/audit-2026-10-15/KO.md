# Coca-Cola (KO) evidence audit: run 2026-10-13

Audited 15 Oct 2026. Read-only: no repo file was changed. Audit question: "is every number based on evidence and justifiable?"

## Summary (5 lines)
1. **Verdict: mostly yes. The SELL holds.** Every input has a cited source. Every input I could reach matches the primary filings (13 inputs checked against SEC EDGAR, FRED, Yahoo and the betas.xls file). With all the value fixes below applied together, the fair value moves from USD 47.60 to USD 46.73 (-1.8%), still SELL against USD 90.12.
2. **Findings: 16 in total.** 2 change the value but not the rating, 6 are misleading, 8 are cosmetic. None changes the rating.
3. **Biggest issues:**
   - The memo's bear case (USD 37.99) leaves out your own decision to use a 31.9% bear margin. With it, the bear case is USD 36.48.
   - The IRS "assume lost" case leaves out the 3M appeal win that Coca-Cola's own 10-K calls "highly supportive".
   - Three value-heavy judgements have no external source: equity risk premium 5.0%, terminal growth 2.0%, and FY27-30 growth 3.0%.
4. **CCBA (open item):** EUR 3,357m revenue and EUR 246m EBIT (7.3%) are now corroborated by two separate web searches that read Coca-Cola HBC's own presentation and factsheet. KO's 41.52% stake sells for USD 1.3bn and the whole company is valued at USD 3.4bn. The PDFs themselves are still blocked from this environment, so the status is "sourced, not verified".
5. **Memo vs outputs:** every number in the memo traces to an agent file (memo_check passes; I checked about 30 key numbers by hand in context). Value and rating match valuation.json. The engine re-run reproduces USD 47.60 and USD 37.99.

## How I checked
- **Primary sources fetched:**
  - SEC EDGAR: KO companyfacts XBRL; FY25 10-K (0001628280-26-010047); Q2 2026 10-Q (0001628280-26-050503); Q4 2025 results 8-K (0001628280-26-006642); Q2 2026 results 8-K (0001628280-26-049922).
  - FRED: DGS10, BAMLC0A3CA and DEXUSEU.
  - Yahoo Finance: KO and the listed stakes, closes and dividends.
  - Damodaran: the betas.xls in the run folder (`runs/KO/2026-10-13/data/damodaran_betas_us_jan2026.xls`), read through LibreOffice.
  - CCBA: WebSearch only. coca-colahellenic.com, investors.coca-colacompany.com, investegate and ticker.app are all blocked for direct fetch.
- **Value impacts** come from the desk's own engine (`desk.valuation_run`) run on scratch copies of the brief and inputs, one change at a time (script and outputs in my session scratchpad). Bear-agent figures are quoted from `bear/bear_runs.json`. No valuation maths was done by hand.

## 1. Brief assumptions (briefs/KO.yaml and inputs.yaml): sources and justification

| Item | Value | Source given | Status | Evidence (my check) | Impact |
|---|---|---|---|---|---|
| Net revenues FY25 | USD 47,941m | 10-K XBRL us-gaap:Revenues | **verified** | XBRL 47,941,000,000, accession 0001628280-26-010047 | none |
| Reported operating income FY25 | USD 13,762m | 10-K XBRL | **verified** | XBRL 13,762,000,000 | none |
| Comparable operating income / comparable revenues FY25 | USD 15,013m / USD 48,062m (31.2%) | Q4 2025 8-K | **verified** | 8-K ex.99.1 reconciliation: "Comparable (Non-GAAP) 48,062 ... 15,013 ... 31.2%" | none |
| CCBA 2024 revenue / EBIT | EUR 3,357m / EUR 246m (USD 3,632m / USD 266m at 1.0820) | Coca-Cola HBC factsheet and presentation, 21 Oct 2025 (seen via web search) | **sourced, not verified** (corroborated) | Two separate WebSearch summaries of CCH's own presentation give "€3,357m, EBIT €246m, 7.3% margin". MarketScreener gives USD 3.63bn / USD 267m. The pro forma CCH+CCBA total is EUR 14.1bn revenue. The PDFs cannot be opened from here. The FRED DEXUSEU 2024 average is **verified** at 1.0820 (251 days). | Removes USD 3,632m of base revenue; margin 33.2% ex-CCBA (31.2% with CCBA) |
| Base sales ex-CCBA | USD 44,309m | 47,941 - 3,632 | sourced, not verified (depends on the CCBA row) | Arithmetic ties | see finding 11 |
| Base margin ex-CCBA | 33.191% | (15,013 - 266) / (48,062 - 3,632) | sourced, not verified (depends on CCBA) | The margin is computed on *comparable* revenue (48,062) but applied to *reported* revenue (47,941) | +USD 0.13 a share if the basis is aligned (finding 11) |
| FY26 growth | 6.0% (organic c.5% + currency c.+1%; the 2-3% disposal headwind is excluded as "mostly CCBA") | Q2 2026 8-K outlook | sourced; **justification weak** | The guidance is verified: organic approx. 5%, approx. 1% currency tailwind, 2-3% headwind from acquisitions and divestitures. **But H1 2026 already shows a -1 point divestiture effect while CCBA is still consolidated** (Q2 8-K revenue bridge: Q2 and H1 consolidated, acquisitions and divestitures (1)). The Q3 2026 guide is also approx. 1% headwind, before CCBA closes. The 10-K names the other disposals: Nigeria finished goods (Oct 2025), India territories (May 2025), Ghana. So about 1 point of the headwind is not CCBA. | FY26 5.0%: **USD 47.13 (-USD 0.47)**, SELL (finding 3) |
| FY27-30 growth | 3.0% a year | ko-growth-evidence.md: low end of the "4-5% long-term algorithm" minus a 1-point currency drag | **weak** | The currency history is sourced (Q4 8-Ks). The 4-5% "algorithm" is **not in a primary source**: the brief itself says so, and press summaries only. The independent industry forecast is MISSING. | 1% (bear): USD 44.31 (-USD 3.30); 4%: USD 49.32 (+USD 1.72). SELL either way (finding 8) |
| Savings | 0 | no programme announced | justified | 10-K Note 19: programme "substantially completed" | none |
| Tax rate | 23.7% = 19.9% + 3.8 points | Q2 2026 8-K + 10-Q Note 9 | **verified** | 10-Q: "effective tax rate in 2026 is expected to be approximately 19.9%"; "would increase the Company's effective tax rate by approximately 3.8%". Note: the 10-Q quantifies the 3.8 points **for 2026 only**; applying it forever is a PM judgement (it fits the "lost" case) | part of the IRS case below |
| IRS liability | USD 14,000m | 10-K (cites XBRL ko:IncrementalTaxAndInterestLiability) | **verified** (text) | 10-K and 10-Q: "could be approximately $14 billion as of December 31, 2025". The custom ko: tag is not in SEC companyfacts, so I checked the text instead. | - |
| IRS base case "KO loses" | 100% loss | PM decision; brief: "The only court ruling so far ... went against KO" | **justification incomplete** | The FY25 10-K says the 8th Circuit **reversed the 3M Tax Court decision on 1 Oct 2025** on the same blocked-income rule. KO calls this "highly supportive" and says it is "more likely than not" to prevail. The 11th Circuit heard KO's appeal on 25 Jun 2026; the ruling is pending. The memo mentions only the two Tax Court losses. | Win: USD 54.90 (+USD 7.29, bear_runs.json). Midpoint of the desk's lose and win results is USD 51.25. SELL either way (finding 5) |
| D&A % sales | 2.68% (FY21-25 pooled) | 10-K XBRL | sourced, not verified (FY25 D&A of USD 1,050m verified) | It uses a 5-year average, while capex uses the latest year: an inconsistent rule | FY25 2.19%: -USD 0.25 (bear) (finding 15) |
| Capex % sales | 4.41% (FY25) | 10-K XBRL; PM decision | **verified** | XBRL capex 2,112 / revenue 47,941. FY26 guidance capex approx. USD 2.2bn verified. Capex includes CCBA (a capital-heavy bottler) while sales exclude it (the Valuation agent flagged this) | small, partly offsets the D&A row |
| NWC % sales | -10.26% | FY25 10-K balance sheet | **verified** | XBRL inventories 4,425, receivables 3,038, prepaid 2,433, payables 14,813 | none |
| Terminal growth | 2.0% | "same as Diageo" | **unsourced** | No inflation, GDP or industry source is cited anywhere | 3.0%: USD 53.63 (+USD 6.02); 1.5%: USD 45.28 (-USD 2.32). SELL across the grid (finding 7) |
| Terminal RONIC | 27.0% | ko-roic-evidence.md (10-K XBRL + Q4 8-Ks) | sourced, reproduced by the Fundamentals agent (26.99%) | Comparable OI 15,013 verified | 31.4%: +USD 0.41 |
| Mid-year convention | 56% of FY26 FCF in H1 | Q2 2026 8-K | **verified** | "free cash flow (non-GAAP) ... $6.9 billion" year to date; guidance approx. USD 12.4bn | none |
| Risk-free | 5.22% (8 Oct 2026) | FRED DGS10 | **verified** | DGS10 8 Oct 5.22%. The run-date print (13 Oct) is now 5.21% (published after the run) | 5.21%: +USD 0.07 (finding 13) |
| Equity risk premium | 5.0% | none ("same rule as Diageo") | **unsourced** | No source in the brief, briefs or evidence packs. Damodaran's site is blocked, so I could not check an implied ERP | 4.5%: USD 49.85 (+USD 2.25); 5.5%: USD 45.56 (-USD 2.04). SELL (finding 6) |
| Beta | 0.6091 (unlevered 0.5755 relevered at D/E 0.0766, tax 23.7%) | Damodaran betas.xls (US), Jan 2026, Beverage (Soft) | **verified** | The file reads "Date updated 2026-01-05", "US companies", Beverage (Soft), 27 firms, "Unlevered beta corrected for cash" = 0.575465. The series is 1.116 (2022), 1.201 (2023), 0.70 (2024), 0.51 (2025); the 5-year average is 0.8205. The PM decision to keep the current value is recorded. Damodaran unlevers at the marginal tax rate; the desk relevers at 23.7% (immaterial) | 2022-26 average: USD 40.01 (-USD 7.60) (bear) |
| Credit spread | 0.69% (8 Oct) | FRED BAMLC0A3CA; A+ rating | **verified** | 0.69% on 8 Oct (0.70% on 13 Oct). The 10-K confirms "A+" from S&P and "A1" from Moody's | 0.70%: USD 0.00 |
| Historic cost of debt (reference only) | 3.675% | 10-K | verified (interest expense 1,654 per XBRL) | Not used by the engine | none |
| Debt weight | 7.11% | net debt / (net debt + 4,302m x USD 90.12) | verified (arithmetic) | - | none |
| Net debt | USD 29,686m | 10-K balance sheet | **verified** | XBRL NotesAndLoansPayable 1,551 + LTD current 1,822 + LTD 42,119 - cash 10,270 - OtherShortTermInvestments 3,602 - MarketableSecurities 1,934. The XBRL tag is LongTermDebt**AndCapitalLeaseObligations**, so any finance leases are already inside debt; data/notes.md says "none inside or outside" (finding 16) | none |
| Operating leases | USD 1,722m | 10-K Note 10 | **verified** | XBRL OperatingLeaseLiability 1,722 | none |
| Minorities | USD 2,106m (book) | 10-K | **verified** | XBRL MinorityInterest 2,106. It includes CCBA's other owner (Gutsche, 33.48%), which is not disclosed. Flagged by the desk. | Upper bound if removed: USD 47.89 (+USD 0.28) (finding 10) |
| Pension deficit | 0 (net surplus USD 183m) | 10-K Note 14 | **verified** | "Net asset (liability) recognized": pension 295, other post-retirement (112) | none |
| Listed stakes | USD 34,286m fair value at 31 Dec 2025 (book USD 13,999m), rolled to USD 39,540m | 10-K equity method table + Yahoo/FRED | **verified** | The 10-K table ties line by line (Monster 15,659 ... total 34,286 / 13,999). Yahoo closes for MNST, CCEP, KOF, CCH.L, 2579.T, CCOLA.IS and ANDINA-B match the CSV to within cents (intraday snapshot; unadjusted closes, correct) | see finding 2 |
| Unlisted stakes | USD 6,236m book | 20,235 - 13,999 | verified | XBRL EquityMethodInvestments 20,235 | none |
| Retained 25% of CCBA | USD 850m (25% x USD 3.4bn) | CCH announcement (web) | sourced, not verified | KO's own price (USD 1.3bn for **41.52%**) implies USD 3.13bn for 100%, so 25% is worth USD 783m | -USD 0.02 (finding 4) |
| CCBA proceeds | USD 1,300m | CCH announcement (web) | sourced, not verified (corroborated) | The search summary of CCH and KO material: KO sells 41.52% of its 66.52% for USD 1.3bn; GFI sells 33.48%. The 10-Q confirms the deal has not closed and is expected "by the end of 2026" | none |
| Restructuring cash | 0 | 10-K Note 19 | sourced, not verified | - | none |
| Shares | 4,302m | 10-K XBRL 7,040m - 2,738m | **verified** | Same tags; Q1 2026 10-Q treasury 2,737m | none |
| Share price | USD 90.12 (13 Oct) | Yahoo | **verified** (to USD 0.01) | Yahoo now shows a USD 90.11 close (the run used an intraday snapshot) | none |
| Dividends ex before run date | USD 6,840m (3 x USD 0.53 x 4,302m) | 10-K / 10-Qs / Yahoo | **verified** | Yahoo: USD 0.53 ex 13 Mar, 15 Jun and 15 Sep 2026 | none |
| Stub | 286 / 365 = 0.78356 | arithmetic | verified | 1 Jan to 13 Oct 2026 = 286 days | none |
| Bear scenario | growth 1% FY27-30, WACC +1 point | growth evidence option C | sourced | **The PM's bear margin of 31.9% (decision 13 Oct) is not applied to the bear scenario** | see finding 1 |
| Rating thresholds | BUY +15% / SELL -10% | PM decision | justified | - | none |

## 2. Memo numbers: tracing
- `python -m desk.memo_check runs/KO/2026-10-13` reports "All memo numbers trace to agent outputs". Because that tool matches a number anywhere in the run folder, I also checked these by hand, in context:
  - from valuation.json: fair value, bear case, grid, HOLD/BUY lines (USD 81.11 / USD 103.64 = USD 90.12 x 0.90 / 1.15), WACC, bridge, TV share, exit multiple;
  - from comps.json: the comps figures;
  - from bear_runs.json and challenges.md: the bear and generous runs, and the 2.72x leverage;
  - from risk notes and risk.json: beta, volatility and drawdown;
  - from fundamentals notes and commentary: ratios and the USD 1,045m impairments;
  - the 3.20% FCF yield is USD 12,400m / USD 387,696m.
- **No untraced numbers found.** The CCBA EUR figures trace to inputs.yaml, which traces to a web-search reading (see above). The MarketScreener USD 3.63bn sits only in docs/phase5 and was correctly removed from the memo body.
- The memo PDF in the shared folder and dcf.xlsx are byte-identical to the repo copies.

## 3. Consistency
- **Value and rating:** the memo (USD 47.60, -47.2%, SELL; bear USD 37.99) matches valuation.json. My re-run of the engine reproduces both to the cent.
- **Currency labels:** fine. The memo states that per-share values are in USD and totals in USD m, and the CCBA figures are labelled EUR. The chart unit bug (pence) was fixed in PR #5.
- **Unresolved FLAGs and MISSING items** (all disclosed in the memo): CCBA slides not seen directly; TV share 75.1% (just above the 75% limit); minorities include CCBA's outside owner; KO forward EPS, peer NTM EBITDA, CCEP data, the leverage target and the industry growth forecast are all MISSING.
- **Stale and not disclosed:**
  - The roll-forward fix (mistakes log row 24, PR #6) was not applied to KO (finding 2).
  - The tables in data/notes.md and risk/notes.md were never rewritten (finding 12).
  - brief-coca-cola.md v1.1 contradicts the yaml (finding 9).

## 4. Findings, ranked

| # | Finding | Severity | Value impact (desk engine) |
|---|---|---|---|
| 1 | **The bear case shown (USD 37.99) ignores the PM's bear margin decision (31.9%, FY24 ex-CCBA).** The brief's `scenarios.bear` has no margin field, so the engine kept 33.2%. The memo headline and chart both show USD 37.99. | Misleading | Bear with 31.94%: **USD 36.48 (-USD 1.51)**. Still SELL |
| 2 | **Listed stakes are grown again at the cost of equity in the roll-forward,** although they are already priced on 13 Oct (mistakes log row 24: "KO: small, rating unaffected"). The engine was fixed (PR #6) but KO was not re-run and the memo does not mention it. | Changes value (rating unchanged) | priced_at_valuation_date = USD 39,540m: **USD 47.01 (-USD 0.59)**. Adding the CCBA amounts: USD 46.98 |
| 3 | **FY26 growth of 6.0% excludes the whole 2-3% disposal headwind as "mostly CCBA",** but about 1 point is other disposals (H1 2026 already -1 point while CCBA is still consolidated; Q3 guide approx. -1%). | Changes value (rating unchanged) | FY26 5.0%: **USD 47.13 (-USD 0.47)** |
| 4 | **CCBA figures: corroborated but still not seen first-hand.** Two independent search readings of CCH's slides match EUR 3,357m / EUR 246m and USD 1.3bn for 41.52%. Small precision points: the stake is 41.52%, not 41.5%; the retained 25% at KO's own price is USD 783m, not USD 850m. **Action:** Amanda (or anyone with normal web access) opens the CCH factsheet once to close the item. | Cosmetic | 25% at USD 783m: -USD 0.02. If CCBA revenue were 10% different, base revenue would move by about USD 363m (about 0.8%) |
| 5 | **IRS "assume lost" rests on one-sided evidence.** The memo says KO "has lost at the Tax Court twice" but omits the Oct 2025 8th Circuit reversal in 3M, which KO's 10-K calls "highly supportive". The +3.8-point tax drag is applied forever, while the 10-Q quantifies it for 2026 only. Consider a probability-weighted case, or at least disclose the 3M ruling. | Misleading | Win: USD 54.90 (+USD 7.29). Midpoint of lose/win: USD 51.25. SELL either way |
| 6 | **Equity risk premium of 5.0% has no source.** | Misleading (unsourced input) | 4.5%: USD 49.85; 5.5%: USD 45.56 |
| 7 | **Terminal growth of 2.0% has no source** ("same as Diageo"). | Misleading (unsourced input) | 3.0%: USD 53.63; 1.5%: USD 45.28 |
| 8 | **FY27-30 growth of 3.0% rests on an unverified "4-5% algorithm"**, with no independent industry forecast (MISSING). The memo discloses the MISSING forecast but not that the algorithm itself is unverified. | Misleading | 4%: USD 49.32; 1%: USD 44.31 |
| 9 | **brief-coca-cola.md v1.1 "FINAL" contradicts briefs/KO.yaml:** margin 31.2% (yaml 33.2% ex-CCBA), IRS USD 14.9bn and "10-Q Note 12" (yaml USD 14.0bn, Note 9), capex as a 5-year average (yaml FY25), bear margin 30.0% (PM later chose 31.9%), "only court ruling went against KO". The yaml header still cites "v1.0". | Misleading (documentation) | none (the yaml governs) |
| 10 | Minorities of USD 2,106m include CCBA's outside owner (Gutsche 33.48%); the amount is not disclosed. Already flagged in the memo. | Cosmetic | upper bound +USD 0.28 |
| 11 | The margin denominator (comparable revenue 48,062) differs from the base revenue (reported 47,941). | Cosmetic | +USD 0.13 |
| 12 | The data/notes.md table is stale (base_sales MISSING, stakes 40,522, IRS 14,900, capex 3.99%, proceeds 0); its update note covers only CCBA. The risk/notes.md body still says "STOP: beta MISSING", with the fix appended. | Cosmetic | none |
| 13 | The risk-free rate is the 8 Oct print (disclosed). The 13 Oct value is now 5.21%; the spread is 0.70%. | Cosmetic | +USD 0.07 / USD 0.00 |
| 14 | The share price snapshot is USD 90.12; Yahoo now shows a USD 90.11 close. | Cosmetic | none (rating unaffected) |
| 15 | D&A uses a 5-year average (2.68%) but capex uses FY25 (4.41%), and capex includes CCBA while sales exclude it. The rules for the two lines are inconsistent (the Valuation agent noted this). | Cosmetic | D&A FY25: -USD 0.25 |
| 16 | Net debt note: the XBRL debt tag includes capital (finance) leases, so "no finance lease inside" is imprecise. The CCBA proceeds and retained stake are grown in the roll-forward rather than discounted to closing. | Cosmetic | about -USD 0.03 |

**Combined fixes 2, 3, 4 (25% stake), 11 and 13:** USD **46.73** (-USD 0.87), SELL. HOLD would need USD 81.11.

## 5. What I could not verify
- **The CCBA slide PDFs** (coca-colahellenic.com) and **KO's own CCBA press release** (investors.coca-colacompany.com): DNS and proxy blocked. Search-engine readings only.
- **Damodaran's implied ERP** (site blocked): the 5.0% could not be benchmarked.
- **KO's XBRL custom tag** ko:IncrementalTaxAndInterestLiability: it is not in companyfacts; checked in the filing text instead.
- **Peer EV/EBITDA inputs** (PEP, KDP, MNST), **comparable organic growth history FY20-24** and **the FY19-26 guidance track record**: not re-checked. These are low weight in the rating.
