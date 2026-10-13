# Data agent notes: The Coca-Cola Company (KO), run 2026-10-13

All money figures are **US dollars, millions (USD m)** unless stated. KO's share price is in USD (NYSE). There is no ADR and no pence conversion.

## Status in one line
**STOP on `base_sales`**: no KO filing discloses the revenue of CCBA (the African bottler being sold). Without that figure the brief's ex-CCBA base year can't be built, so `base_sales` is left **MISSING (null)** in `inputs.yaml`. The valuation engine will refuse to run until Amanda decides how to fill it (options below). Every other input is filled and sourced.

## What I fetched
- `python -m desk.data_sources briefs/KO.yaml runs/KO/2026-10-13/data` with SEC_CONTACT_EMAIL set. It ran without errors and wrote `financials_raw.csv` (191 rows, FY21-FY25 from the 10-Ks for FY22-FY25), `prices.csv` (KO and ^GSPC, 5 years) and `market_inputs.json` (DGS10 5.22% at 2026-10-08; KO close $90.12 at 2026-10-13). Missing XBRL items: `irs_potential_liability` FY21-23 (the tag only starts in FY24) and `treasury_shares_m` FY21. Neither is needed.
- SEC filings (CIK 21344): FY25 10-K 0001628280-26-010047; Q4 2025 release 8-K 0001628280-26-006642; Q2 2026 release 8-K 0001628280-26-049922; Q2 2026 10-Q 0001628280-26-050503; Q1 2026 10-Q 0001628280-26-028802; Q3 2025 10-Q 0001628280-25-046054; Q3 2025 release 8-K 0001628280-25-045577; 8-K of 16 Jul 2026 0001628280-26-048466 (the fairlife ransomware event, which is not a dividend notice); Q4 releases for FY21-FY24 (0000021344-22-000004, -23-000005, -24-000004, -25-000005) for comparable margins.
- Peers: SEC XBRL companyfacts for PEP (CIK 77476), KDP (1418135) and MNST (865752); Yahoo Finance prices, split events and consensus EPS.
- Scripts (re-runnable from the repo root with `PYTHONPATH=.`): `build_inputs.py` writes financials.csv, tie_out.csv and ../inputs.yaml. `build_peers.py` writes peers.csv and associates_rollforward_check.csv.
- Network: only SEC (www/data.sec.gov), Yahoo and FRED can be reached. Company websites, the LSE, news sites, research houses and SEC full-text search (efts.sec.gov) are all blocked by the proxy policy.

## Tie-out vs `checks.published_fy25` (tolerance 0.5%): all pass
| item | brief | data agent | diff |
|---|---|---|---|
| net sales | 47,941 | 47,941 (XBRL us-gaap:Revenues) | 0.00% |
| reported operating income | 13,762 | 13,762 | 0.00% |
| comparable operating margin | 31.2% | 31.24% (15,013 / 48,062) | +0.13% |
| free cash flow | 5,300 | 5,296 (OCF 7,408 - capex 2,112) | -0.08% |
| comparable EPS | $3.00 | $3.00 (Q4 2025 8-K) | 0.00% |

## inputs.yaml values and confidence
| input | value | confidence | note |
|---|---|---|---|
| base_sales | **MISSING** | n/a | STOP: see FLAG 1 |
| base_margin | 0.31237 | medium | FY25 comparable margin, **including CCBA** (FLAG 2) |
| tax_rate | 0.237 | high (as a PM decision) | 19.9% (Q2 2026 8-K) + 3.8 pts (Q2 2026 10-Q **Note 9**, not note 12 as the brief comment says) |
| da_pct_sales | 0.02682 | high | FY21-25 pooled: D&A 5,965 / revenue 222,415 |
| capex_pct_sales | 0.03992 | high (history); medium (forward) | FY21-25 pooled: capex 8,879 / revenue 222,415. FY26 guidance $2.2bn is about 4.4% of guided revenue |
| nwc_pct_sales | -0.10256 | medium | FY25: 4,425 + 3,038 + 2,433 - 14,813 = -4,917. FY24 ex-fairlife: -4,291 = -9.1% |
| risk_free | 0.0522 | high | FRED DGS10, 2026-10-08 (latest observation) |
| pre_tax_cost_of_debt | 0.03675 | high (reference only) | 1,654 / avg gross debt (44,522 + 45,492)/2. Engine uses 5.22% + 0.69% |
| debt_weight | 0.07112 | high | 29,686 / (29,686 + 4,302m x $90.12 = 387,696) |
| net_debt | 29,686 | high | 1,551 + 1,822 + 42,119 - 10,270 - 3,602 - 1,934. No finance-lease liability disclosed |
| lease_liabilities | 1,722 | high | operating leases, not in net debt |
| minority_interests | 2,106 | medium | book; includes CCBA's outside shareholders (FLAG 4) |
| pension_deficit | 0 | high | net surplus 183 (pension +295, other post-retirement -112) |
| associates | 40,522 | medium | 34,286 listed at 31 Dec 2025 fair value + 6,236 unlisted at book (FLAG 3) |
| disposal_proceeds | 0 | **low** | not disclosed (FLAG 1) |
| restructuring_cash | 0 | high | 10-K Note 19: programme "substantially completed" |
| contingent_liabilities | 14,900 | high (as a PM decision) | 14,000 (10-K) + 900 (10-Q Note 9) |
| shares_outstanding_m | 4,302 | high | 7,040 - 2,738. 10-Q cover: 4,302.5m at 27 Jul 2026 |
| share_price_usd | 90.12 | high | Yahoo KO close 2026-10-13 |
| stub_years | 0.78356 | high | 286 days / 365 |
| dividends_ex_before_valuation_musd | 6,840.2 | high | 3 x $0.53 x 4,302m (ex 13 Mar, 15 Jun, 15 Sep 2026) |
| beta | not set | n/a | left for the Risk agent |

## FLAGs
1. **CCBA revenue and sale proceeds are not in any KO filing (STOP for base_sales; disposal_proceeds = 0 is low confidence).**
   - **Where I looked:** 10-K Note 2 (held-for-sale table: assets 5,342, liabilities 2,570, impairment 1,274; balance sheet only), the segment note, and every XBRL fact on `ko:BottlingOperationsInAfricaMember` (impairment, supplier finance and debt only, no revenue). Also the Q3 2025 10-Q and release, the Q4 2025 release, the Q1 and Q2 2026 10-Qs and the Q2 2026 release. KO filed no 8-K for the deal. Coca-Cola HBC's announcement is not on EDGAR, and its website and the LSE are blocked here.
   - **The nearest disclosed figure is not usable:** the Bottling Investments segment (revenue 5,735, comparable operating income 426, 7.4% margin) also contains India (40% sold to Jubilant in July 2025, still consolidated) and other consolidated bottlers.
   - **Options for Amanda:**
     - (a) Get CCBA's revenue from Coca-Cola HBC's October 2025 deal announcement or its H1 2026 report (non-filing for KO; someone with web access has to fetch it).
     - (b) Use reported FY25 revenue 47,941 including CCBA, set disposal_proceeds = 0 and keep CCBA in the forecast. That is internally consistent, but CCBA's net debt (1,435) and cash (178) sit in held-for-sale, outside net debt, so that debt would need adding back.
     - (c) Use the brief's guidance-based disposal headwind instead. The brief rejects this.
   - **Proceeds:** the held-for-sale net assets of 2,772 (5,342 - 2,570) are carried at fair value less costs to sell, on a 100% basis (including the Gutsche family's stake). This is the only filing-based value, but it is not KO's cash proceeds: KO's ownership share and the price are not disclosed. Trap 5 (same rule as EABL): if base_sales excludes CCBA, the bridge must add KO's proceeds plus its retained 25% stake. Leaving 0 would undervalue KO.
2. **Base margin includes CCBA.** I used 31.237% (15,013 / 48,062, Q4 2025 8-K), which is the brief's PM rule. CCBA's operating income is not disclosed, so I can't compute an ex-CCBA margin. CCBA is a lower-margin bottler (the Bottling Investments segment earns 7.4%), so an ex-CCBA margin would be **higher**. Upper bound only (not an input): removing the whole Bottling Investments segment gives (15,013 - 426) / (48,062 - 5,735) = 34.5%. If Amanda later fills base_sales ex-CCBA, the margin must be re-based at the same time, otherwise the forecast mixes an ex-CCBA revenue with a with-CCBA margin.
3. **Equity stakes at 31 Dec 2025 fair value, not run-date market value.** The brief asks for market value on the run date, but the 10-K gives no share counts or ownership percentages (only fair value and book per investee), so I used 34,286 as you instructed.
   - Cross-check (`associates_rollforward_check.csv`, not an input): rolling each fair value forward by Yahoo price change x FX change gives **39,540 at 13 Oct 2026, +5,254 (+15%)**, about +$1.22 per KO share. This assumes holdings are unchanged; the H1 2026 10-Q shows only $1m of equity-investment disposals.
   - The biggest moves are Monster 15,659 to 17,785, CCEP 7,163 to 8,338 and FEMSA 5,543 to 6,724. Monster split 2-for-1 on 11 Aug 2026; Yahoo prices are split-adjusted, so the ratio is unaffected.
   - Recommend Amanda decide whether to use 39,540 + 6,236 = 45,776 instead.
4. **Minority interests (2,106) include CCBA's outside shareholders.** NCI rose from 1,516 to 2,106 in FY25, mainly from the 40% India stake sold in July 2025 (+$1.1bn of equity). The CCBA part is not disclosed. If CCBA is removed from the base, its NCI should also come out of the deduction. Can't quantify from filings.
5. **NWC ratio.** FY25 balances already exclude CCBA's working capital (inside held-for-sale: receivables 389, inventory 466, prepaid 147, payables 816), but the denominator (47,941) includes CCBA's revenue, so the ratio slightly understates how negative NWC is. "Prepaid and other current assets" (2,433) also holds some non-operating items (e.g. derivatives) that the 10-K doesn't split out. The FY24 fairlife liability (6,126, Note 8) is excluded from the FY24 cross-check; FY25 has none.
6. **D&A and capex averages** cover FY21-25, when KO still owned more bottlers (Philippines, Bangladesh, Vietnam, India territories, now CCBA). Bottlers are capital-heavy, so ex-CCBA intensity is probably lower. FY25 alone: D&A 2.19%, capex 4.41%. The forward capex guidance (about $2.2bn) is above the 5-year average.
7. **Brief citation:** the 3.8-point tax sentence is in **10-Q Note 9 (Commitments and Contingencies)** and Part II Item 1. Note 12 is "Significant operating and nonoperating items". The value is unchanged.
8. **Risk-free 5.22%** is the latest FRED DGS10 print (2026-10-08). It is used as given.

## Traps (brief section 3) and how I handled each
1. **US GAAP:** desk US_GAAP_TAGS map (us-gaap:Revenues, OperatingIncomeLoss, etc.). Non-GAAP comparable figures come from the Q4 release reconciliations, with FY21-25 typed into financials.csv with accessions.
2. **USD price, no ADR:** `share_price_usd` only. No FX or pence fields.
3. **Cash hits:**
   - FY24 OCF includes the $6.0bn IRS deposit. FCF was 4,741 reported vs $10.8bn excluding the deposit (Q4 2024 8-K).
   - FY25 OCF includes the $6,069m fairlife payment. FCF was 5,296 reported vs 11,365 excluding it (Q4 2025 8-K).
   - Capex is not affected by either. The fairlife liability is excluded from FY24 NWC.
4. **Argentina:** not used in any data input. Growth is the PM's (in USD). I supply no organic growth figures for the forecast.
5. **CCBA sale:** see FLAGs 1, 2, 4 and 5. Net debt excludes CCBA's debt (1,435) and cash (178), which are in held-for-sale.
6. **Equity stakes at market:** FLAG 3. Unlisted stakes at book (6,236). Equity income sits below operating income, so there is no double count with the DCF.
7. **IRS case:** contingent 14,900 and tax rate 23.7% (PM decisions). The $6.0bn deposit and $385m interest receivable are not added back (base case = lose).
8. **Calendar year-end:** no calendarisation for US peers. PEP's year is 52/53 weeks (FY25 ended 27 Dec 2025).

## Industry forecast (step 5): MISSING
I could not get an independent industry forecast. Euromonitor, GlobalData, Beverage Marketing Corp, Grand View, Mordor, Statista and news sites are all blocked from this environment, and SEC full-text search is blocked too. The only third-party industry figure I found in a filing is historical, not a forecast: **Monster's FY25 10-K (accession 0001104659-26-020831) quotes Beverage Marketing Corporation: US "alternative" beverage wholesale sales of about $76.8bn in 2025, up about 2.4% on 2024 (USD, nominal)**. That is one US sub-category. For what it's worth, it sits below KO's 4-5% organic algorithm and slightly below the brief's 3.0% USD growth for FY27-30, which leans towards the brief being not too low. It does not test the 2.0% terminal rate. Confidence: low. I recommend someone with web access pull a Euromonitor or IWSR-style global non-alcoholic ready-to-drink forecast.

## Peers (peers.csv)
Built from SEC XBRL (FY25 10-K + latest 10-Q year-to-date; LTM = FY25 + 2026 YTD - 2025 YTD).
- EV = market cap + debt - cash and short-term investments + NCI. Leases are excluded, matching KO's net debt.
- EBITDA = GAAP operating income + D&A (unadjusted).
- Rows flagged `non-filing source` where that applies: prices and NTM EPS (Yahoo consensus, time-weighted FY26/FY27).

| peer | LTM to | EV | EBITDA LTM | EV/EBITDA LTM | P/E LTM | P/E NTM | FCF yield |
|---|---|---|---|---|---|---|---|
| PEP | 5 Sep 2026 | 213,688 | 18,720 | 11.4x | 15.9x | 14.7x | 6.1% |
| KDP | 30 Jun 2026 | 77,199 | 4,051 | 19.1x | 31.2x | 13.2x | 4.4% |
| MNST | 30 Jun 2026 | 81,829 | 2,809 | 29.1x | 40.1x | 34.2x | 2.5% |

- **EBITDA NTM: MISSING** for all peers. There is no free EBITDA consensus, so ev_ebitda_ntm can't be computed. The comps agent should use pe_ntm or the LTM multiples.
- **KDP:** LTM is distorted by the JDE Peet's acquisition. The EV includes the post-deal debt and NCI (net debt 28.5bn, NCI 4.2bn at 30 Jun 2026), but EBITDA has only about one quarter of JDE Peet's in it. GAAP earnings are depressed by deal costs.
- **MNST:** the 2-for-1 split on 11 Aug 2026 is applied to the 10-Q cover share count (979.5m to 1,959.1m). Without it, the market cap would be halved.
- **CCEP: MISSING.** It is a foreign private issuer with no XBRL companyfacts, and its site is blocked.
- **DEO:** see the DGE run (runs/DGE/2026-10-12/data). Not recomputed here; June year end.
- Prices were pulled live on 13 Oct 2026 and can differ by a few cents between runs.

## Files
`financials.csv`, `financials_raw.csv`, `tie_out.csv`, `market_inputs.json`, `prices.csv`, `peers.csv`, `associates_rollforward_check.csv`, `build_inputs.py`, `build_peers.py`, `../inputs.yaml`

## Update 2026-10-13 17:54 (Claude, after the PM's CCBA decision)
The `base_sales` STOP above is resolved. CCBA's 2024 figures come from the buyer's announcement (Coca-Cola HBC, 21 Oct 2025: net sales revenue EUR 3,357m, EBIT EUR 246m, converted at 1.082), corroborated by MarketScreener (USD 3.63bn revenue, USD 267m EBIT). Evidence: docs/phase5/ko-ccba-evidence.md. `apply_pm_ccba_decision.py` wrote base_sales 44,308.7 and base_margin 33.191% to inputs.yaml. The PM was asked to verify the slides directly, because coca-colahellenic.com is not reachable from this environment.
