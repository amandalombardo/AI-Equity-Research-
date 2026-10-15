# Data agent notes: RELX PLC (RELX / REL.L), run 2026-10-14

All money is **GBP m** unless labelled otherwise. The share price is in **pence (GBp)**. RELX reports in pounds, so the
valuation needs no exchange rate (pounds x 100 = pence). 1 RELX ADR = 1 ordinary share (not used).
Every value in `../inputs.yaml` carries its source (document + page, or URL). Scripts (re-runnable from the repo root):
`build_inputs.py` (financials.csv, tie_out.csv, market_data.json, `--write-inputs` for ../inputs.yaml) and `build_peers.py` (peers.csv).

**Status: inputs.yaml is complete except `beta`, which is left for the Risk agent** (the engine confirms only `beta` is missing).
No STOP.

## History of this run
1. First attempt: `python -m desk.data_sources` crashed (`KeyError: 'item'`). RELX's XBRL names its currency units
   `Unit_Standard_GBP_<hash>`, so the desk kept no numbers. RELX also tags revenue as `ifrs-full:RevenueFromContractsWithCustomers`
   and inventories as `relx:InventoriesAndPrepublicationCosts`. I stopped as the procedure requires.
2. The coordinator put the fix on PR #7 (same branch; Amanda approves the whole PR before merge). The desk now reads the
   currency from the unit's `iso4217` measure and knows both labels. I re-ran from step 1: 117 rows, FY21-25, no crash.
   (pytest is not installed in the Data agent's environment, so I could not re-run the tests; the coordinator reports 66 pass.
   I changed no desk code.)

## What I fetched
- `desk.data_sources`: five 20-F XBRL instances (FY25 0001104659-26-017277 back to FY21 0001193125-22-045453),
  REL.L and ^FTSE prices (prices.csv), FRED UK gilt monthly series, and the REL.L close: **2,771p on 13 Oct 2026**
  (market_inputs.json; it is the 13 Oct CLOSE, unadjusted, not an intraday 14 Oct price).
- Filing texts from SEC EDGAR (CIK 929869), read to re-check every value the valuation depends on:
  FY25 results 6-K (0000929869-26-000008), Annual Report 2025 (20-F ex 15.2) and 20-F main document (0001104659-26-017277),
  H1 2026 results 6-K (0000929869-26-000054), buyback 6-Ks of 23 Jul (-000056) and 7 Sep 2026 (-000068), dividend 6-Ks
  (-000041, -000064), voting rights 1 Sep 2026 (-000066 ex 99.5), weekly "Transactions in own shares" (-000066, -000071).
- FRED: DGS10 (US 10-year, 5.21% on 13 Oct), BAMLC0A3CA (A spread 0.70% on 13 Oct), BAMLC0A4CBBB (BBB 1.03%), DEXUSUK.
- Peers: SEC XBRL instances for TRI (40-F + H1 6-K), VRSK, SPGI, MCO (10-K + Q2 10-Q); Yahoo for prices, consensus EPS and the
  European peers.

## Tie-out (tie_out.csv) vs brief checks.published_fy25 (tolerance 0.5%)
| Item | Brief | Data agent | Diff | Flag |
|---|---|---|---|---|
| Revenue | 9,590 | 9,590 (XBRL RevenueFromContractsWithCustomers) | 0.00% | no |
| Adjusted operating profit | 3,342 | 3,342 (AR25 p.186; XBRL relx:AdjustedOperatingProfit) | 0.00% | no |
| Adjusted operating margin | 34.8% | 34.849% | +0.14% (rounding) | no |
| Net debt (RELX definition, incl. leases) | 7,201 | 7,201 = XBRL Borrowings 7,267 + derivative liabilities 60 + 5 - cash 131 | 0.00% | no |

No tie-out FLAGs.

## inputs.yaml: values and confidence
| Input | Value | Basis (full citation in inputs.yaml) | Confidence |
|---|---|---|---|
| base_sales | 9,590 | FY25 revenue INCLUDING print 399 (FY25R p.26; AR25 p.186). Note: the margin decision (35.0%) is on H1 2026 ex print, but the DCF base is FY25 revenue, as the PM instructed | high |
| base_margin | 0.350 | brief (PM decision); FY25 actual incl. print 34.85% | high (sourced) |
| tax_rate | 0.228 | brief; H1 2026 ETR 22.8%, "best estimate of the annual tax rate" (H126 p.28 note 7, re-checked) | high |
| da_pct_sales | 0.0507 | brief; H126 p.10 and p.25 (193 + 12 + 42) / 4,871, re-checked | high |
| capex_pct_sales | 0.0710 | brief; H126 p.10 (292 + 54) / 4,871, quote re-checked | high |
| nwc_pct_sales | **-0.15527** | (311 + 2,468 - 4,268) / 9,590 = -1,489 / 9,590. AR25 p.141 balance sheet; note 20 p.176 (payables include deferred income 2,390) | high (FLAG 1) |
| risk_free | 0.0545 | brief: gilt close 13 Oct 2026, aggregators | medium (FLAG 2) |
| pre_tax_cost_of_debt | 0.039 | historic, reference only: RELX-stated 3.9% (FY25R p.13). Cross-check: finance costs 298 (AR25 p.156 note 7) / average gross debt 6,905.5 = 4.32%. Engine uses 5.45% + 0.70% = 6.15% | high (reference only) |
| debt_weight | 0.12818 | 7,104 / (7,104 + market cap 48,319.4 = 1,743.754727m x 2,771p). With 30 Jun 2026 net debt ex leases 8,614: 15.1% | high (FLAG 5) |
| net_debt | 7,104 | 7,201 - 97 leases (FY25R p.13, quote re-checked) | high |
| lease_liabilities | 0 | the 97 of leases is taken OUT of net debt and NOT added back (PM decision: lease cost is in cash flow) | high |
| minority_interests | 24 | book (FY25R p.22; AR25 p.141; XBRL) | high |
| pension_deficit | 0 | net SURPLUS 43 = 197 - 154 (AR25 p.141; XBRL -43) | high |
| associates | 131 | venture capital and other investments at fair value (AR25 p.167 note 15; p.141). JVs (book 164) NOT added | high (trap 4) |
| disposal_proceeds | 0 | no pending disposal; no held-for-sale items at 31 Dec 2025 | high |
| restructuring_cash | 0 | no programme | high |
| shares_outstanding_m | 1,743.754727 | ex treasury at 25 Sep 2026 (6-K 0000929869-26-000071 ex 99.6, quote re-checked) | high (FLAG 4) |
| share_price_gbp_pence | 2,771 | Yahoo REL.L close 13 Oct 2026 | high |
| stub_years | 0.78356 | 286 days, 31 Dec 2025 to 13 Oct 2026 (price date) / 365 | high |
| dividends_ex_before_valuation_mgbp | 1,217 | 2025 final 851 (ex 7 May, FY25R p.27; cash H126 p.20, p.25) + 2026 interim 366 (ex 6 Aug, paid 10 Sep, H126 p.25) | high / medium for the 366 (FLAG 3) |
| buybacks_after_balance_sheet_mgbp | 2,056.2 | 1,750 (H126 p.20, p.12) + 100 (BB 23 Jul) + 150 (BB 7 Sep) + 56.2 (7-25 Sep, recomputed: 2,225,133 shares x daily VWAP over 15 days = 56.18) | high / medium for the 56.2 |
| beta | (not set) | left for the Risk agent | n/a |

## FLAGs
1. **Payables GBP 8m difference.** The audited Annual Report shows current trade and other payables of 4,268 plus 1 non-current
   (AR25 p.141, note 20 p.176; XBRL also 4,268). The results release shows 4,260 plus 9 non-current (FY25R p.22).
   Both total 4,269: GBP 8m was moved between current and non-current. I used the audited 4,268. With 4,260 the ratio would be
   -15.44% instead of -15.53%. Immaterial.
2. **Risk-free 5.45% is from aggregators.** I could not re-check it myself. Trading Economics, Investing.com, the Bank of England
   and the DMO are all blocked from this environment (proxy 403 or DNS failure). The value is the PM's, per the brief comment.
   Reference values I could pull: FRED IRLTLT01GBM156N Aug 2026 = 4.99% (stale monthly average); FRED DGS10 (US 10-year) =
   5.21% on 13 Oct, which supports the fact that long yields are above 5%.
3. **Interim dividend £366m is RELX's "expected total cost of funding"** (H126 p.25 note 4). Payment on 10 Sep is confirmed
   (6-K 27 Aug 2026), but the actual cash figure appears only in the FY26 accounts. Any difference is likely under £5m.
   Distributions to minorities (9 in H1) are excluded.
4. **Shares include Employee Benefit Trust shares.** The 25 Sep count (1,743.75m) excludes only the parent company's treasury
   shares. The EBT held 4.89m shares at 31 Dec 2025 (AR25 p.179) and bought GBP 60m more in H1 (H126 p.12). The implied EBT
   holding at 30 Jun 2026 is about 6m (1,749.8m net of treasury and EBT, vs about 1,755.8m ex treasury only; computed). So the
   count is about 0.35% higher than RELX's own EPS basis. That is cautious: the EBT shares will go to employees. I kept the
   brief's count.
5. **Timing of the debt weight.** It uses 31 Dec 2025 net debt with the 13 Oct share price and the post-buyback share count,
   as the brief defines it, matching the Risk agent's beta relevering. At 30 Jun 2026, net debt ex leases was 8,614
   (H126 p.11), giving a 15.1% weight.
6. **Buybacks after 25 Sep 2026 are not yet filed** (RELX files weekly notices monthly; the next batch is due in early November).
   They are left out of both cash and shares, which is consistent. The 7 Sep-21 Oct tranche is capped at GBP 125m
   (BB 7 Sep 2026), of which 56.2 was spent by 25 Sep. The 56.2 is computed from VWAPs, before 0.5% stamp duty and
   commission (about 0.3).
7. **Price momentum.** REL.L rose from 2,496p (30 Sep) to 2,771p (13 Oct). The +4.8% on 9 Oct has no matching 6-K
   (facts pack). There is no Q3 trading update yet; last year's came on 23 Oct.

## Traps and how I handled them
1. **New desk path for a pound reporter.** No FX input. Every money key ends `_mgbp` (`dividends_ex_before_valuation_mgbp`,
   `buybacks_after_balance_sheet_mgbp`), and the price is in pence. The engine's `extra_required` confirms exactly these keys.
2. **Price date.** I used the 13 Oct 2026 CLOSE for REL.L and all market data (the Unilever run used an intraday price by
   mistake). The build script asserts the price date. stub_years also runs to 13 Oct.
3. **Leases.** Net debt is 7,104 without the 97 of leases, and lease_liabilities is 0, so leases are not counted twice
   or put back.
4. **Joint ventures.** Not added. RELX's adjusted operating profit includes the JV share, grossed up for JV tax (+14) and
   finance income (-1) (FY25R p.26). RELX states the JV share of adjusted OP as 57 (AR25 p.206). Adding the JV book value (164)
   would double count. Only venture capital and other investments (131, fair value, outside operating profit) are added.
5. **Pension surplus not added** (brief rule): pension_deficit = 0.
6. **Adjusted vs reported.** Adjusted operating profit excludes acquired-intangible amortisation (248) and acquisition items
   (54). The tie-out uses adjusted, the brief's basis. financials.csv keeps reported operating profit (3,027) and the five-year
   adjusted figures side by side.
7. **Print.** base_sales includes print (399), while the margin is the ex-print H1 2026 figure, as instructed.
   A note for the PM, not a change to the brief: print earns about 46% (185 / 399), so applying 35.0% to revenue that includes
   print slightly understates FY26 profit while print still exists. This is consistent with the brief's reasoning that print
   is being run off.
8. **H1 2026 template residue.** The H1 2026 HTML contains hidden leftover H1 2025-style text ("4,499m", "550m share buyback").
   I took no figure from it. Every H1 figure was read from the visible pages with page headers.
9. **Buyback vs EBT purchases.** EBT purchases (60 in H1) are not in buybacks_after_balance_sheet, because EBT shares are
   still in the share count (FLAG 4).

## financials.csv
- 175 rows, FY21-25, `item, fiscal_year, value_mgbp, source`. XBRL rows give the filing accession and tag. Rows read from text
  give the document and page:
  - adjusted figures, five-year summary (AR25 p.186)
  - capitalised development spend 447 / 464 / 504 for FY23-25 (AR25 p.140 cash flow)
  - pre-publication spend 92 / 102 (XBRL relx:PrePublicationCostsCapitalized; FY25R p.11)
  - net debt and leases (FY25R p.13), finance costs (AR25 p.156), JV adjusted OP 57 (AR25 p.206), EBT shares (AR25 p.179)
- Desk labels RELX does not tag, and whether the valuation needs them (also in market_data.json):
  - **restructuring:** not needed. There is no programme, and adjusted OP is the base.
  - **capex_intangibles:** RELX does not use the label. Capitalised development spend is read from the text (above). Not
    needed for the DCF: the brief sets capex from H1 2026. FY21-22 development spend was not collected (facts pack: 309 / 400,
    FY21R and FY22R, not re-checked).
  - **other_current_financial_assets:** not in RELX's net debt definition. Not needed.
  - **held for sale:** none at FY25 (FY23 only: 44 / 14). This confirms disposal_proceeds 0.
- Note: XBRL `depreciation_amortisation` (752 for FY25) INCLUDES acquired-intangible amortisation (248) and lease depreciation
  (37). It is not the D&A the DCF uses.

## Industry forecast (step 5): MISSING, with a substitute cross-check
- **No independent industry forecast could be obtained.** Every likely source is blocked from this environment (proxy 403 or
  DNS failure): Gartner, Outsell, the STM association, Statista, Research and Markets, OECD, IMF, World Bank, ONS, ECB, BIS,
  Wikipedia. RELX's 20-F cites "market research ... and industry publications" for its competitive position but gives no
  market-growth number. I did not estimate one.
- **Substitute (not independent of the industry, but primary and filed):** Thomson Reuters, the closest legal and tax peer,
  "raised full-year 2026 total and organic revenue growth outlook to approximately 8.0% for the total company, and to a range
  of 9.5% to 10.0% for the 'Big 3' segments". This is from its Q2 2026 results, 6-K ex 99.1, accession 0001193125-26-333835,
  5 Aug 2026. Its H1 organic growth was 8%, while Global Print fell 3-4%.
- **Read-across to the brief:**
  - 5.0% constant-currency growth for FY27-30 sits well below TRI's 8% organic outlook and RELX's own 7% underlying growth.
    The difference is print run-off, disposals and exhibition cycling, which the 5.0% includes. The peer evidence therefore
    supports 5.0% as cautious, not aggressive.
  - Terminal growth of 2.0% (inflation) is far below current industry growth, which is conservative. It only matters if
    AI erodes growth (the bear case).
  - Confidence that this cross-check validates growth: **low**, because it is not an independent market forecast.

## Peers (peers.csv)
| Peer | Source | EV/EBITDA LTM | P/E LTM | P/E NTM | FCF yield |
|---|---|---|---|---|---|
| Thomson Reuters | SEC 40-F + H1 6-K XBRL; price, shares, EPS Yahoo | 14.5x | 27.4x | 21.3x | 4.9% |
| Verisk | SEC 10-K + Q2 10-Q XBRL; price, EPS Yahoo | 16.4x | 26.0x | 20.8x | 5.4% |
| S&P Global | SEC 10-K + Q2 10-Q XBRL; price, EPS Yahoo | 16.4x | 24.6x | 20.8x | 4.6% |
| Moody's | SEC 10-K + Q2 10-Q XBRL; price, EPS Yahoo | 20.7x | 28.8x | 25.1x | 3.7% |
| Wolters Kluwer | Yahoo only (flag) | 11.1x | 13.1x | 13.0x | 7.1% |
| Experian (FY to March, USD) | Yahoo only (flag) | 14.5x | 21.1x | 16.8x | 2.9% |
| LSEG | Yahoo only (flag) | 15.7x | 28.4x | 15.6x | 4.3% |
| Informa (optional, show separately) | Yahoo only (flag) | 13.6x | 54.2x | 13.7x | 7.5% |

- LTM for the SEC peers runs to 30 Jun 2026 (FY25 + H1 2026 - H1 2025), read from each filing's own XBRL file. I did not use
  SEC companyfacts, because it lagged at Q1 2026 for VRSK and SPGI. EBITDA is reported operating income + D&A, unadjusted.
- **ebitda_ntm is MISSING for every peer:** there is no free EBITDA consensus. NTM P/E uses Yahoo consensus EPS, time-weighted
  over the current and next fiscal year (flag: non-filing source). Prices are the 13 Oct 2026 close for all peers.
- Peer flags:
  - SPGI: EV includes the 5,024 redeemable minority interest (S&P Dow Jones Indices).
  - TRI: shares come from Yahoo; the sale of 51% of its print business to a KKR joint venture is pending.
  - Experian: market cap converted to USD at FRED DEXUSUK 1.3229 (9 Oct 2026).
  - LSEG and Informa: LTM P/E uses reported profit, so prefer NTM P/E.
- European peer figures (Yahoo LTM) are not checked against annual reports, which are blocked here. Comps confidence:
  **medium** for SEC peers, **low** for Yahoo-only peers.

## What is missing
- beta (the Risk agent's job, by design).
- An independent industry forecast (above).
- A primary daily gilt yield for 13 Oct 2026 (FLAG 2).
- Buybacks and share count from 28 Sep to 13 Oct 2026 (not yet filed; FLAG 6).
- NTM EBITDA for peers.
- FY21-22 capitalised development spend from the filings (not needed by the valuation).

## Files
- `financials_raw.csv`, `prices.csv`, `market_inputs.json`: desk.data_sources output.
- `financials.csv`, `tie_out.csv`, `market_data.json`: build_inputs.py output.
- `peers.csv`: build_peers.py output.
- `../inputs.yaml`.
