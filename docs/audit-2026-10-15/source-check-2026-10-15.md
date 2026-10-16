# Source check of second-hand figures, 15 Oct 2026

Follow-up to today's evidence audit (summary.md). It covers only the figures that audit could see second-hand or had flagged. The other checked figures were already verified at source and were not redone. Values are re-run with the desk's own engine (`desk.valuation_run.build`), changing one input at a time.

**Result: no rating changes.** Final calls stay: Diageo HOLD 1,780.2p (GBp) after the beta fix (was 1,772p), Coca-Cola SELL USD 50.25, Unilever HOLD 4,259p (GBp, borderline), RELX SELL 1,821p (GBp).

Reachable from here: SEC EDGAR, FRED, Yahoo Finance, and the Damodaran files Amanda uploaded. Blocked here: coca-colahellenic.com (including its ba. subdomain and web.archive.org), eabl.com, Bank of England, Bundesbank, ECB, pages.stern.nyu.edu (Damodaran), LSE, Investing.com.

## 1. Now confirmed first-hand

| Company | Figure | Desk value | Primary source | Result |
|---|---|---|---|---|
| Diageo | Industry unlevered beta (cash-corrected), global alcoholic beverages | 0.73 | betaGlobal.xls (Damodaran, 5 Jan 2026), "Industry Averages": Beverage (Alcoholic), 217 firms, 0.6884 unlevered, **0.7250** cash-corrected | **Differs (rounding).** Fixed on Amanda's instruction (15 Oct): beta relevered at Diageo's current D/E is 0.9526 (was 0.9601). Fair value 1,772.1p becomes **1,780.2p (+8.1p), still HOLD** (pull request awaiting approval). Mistakes log row 33 |
| Coca-Cola | US soft-beverage unlevered beta | 0.5755 | betas.xls (Damodaran US, Jan 2026): Beverage (Soft) 0.5755 | Confirmed |
| Unilever | Global household products unlevered beta | 0.7741 | betaGlobal.xls: Household Products, 588 firms, 0.7741 | Confirmed |
| RELX | Global information services unlevered beta | 0.8737 | betaGlobal.xls: Information Services, 86 firms, 0.8737 | Confirmed |
| RELX | FY24 constant-currency growth (one of the three years in the 5.0% FY27-30 growth) | 6% | RELX 20-F FY24 (SEC 0001558370-25-001178): "giving total revenue growth at constant currency of 6%" | Confirmed |
| RELX | Bear margin, FY23 without print | 32.4% | RELX Annual Report 2025 (20-F exhibit 15.2, SEC 0001104659-26-017277), segment note: (3,030 - 253) / (9,161 - 586) = 32.38% (GBP m) | Confirmed |
| Unilever | McCormick one-month VWAP behind the USD 44.8bn headline | USD 57.84 | Unilever investor presentation, Form 425, 31 Mar 2026 (SEC 0000217410-26-000027), p.77 footnote | Confirmed (memo context only, not a model input) |
| Unilever | Other fair-value investments | EUR 902m | Unilever 20-F FY25 (SEC 0000217410-26-000007): FVOCI 2,216 less TMICC 1,655 = 561; non-current FVTPL "Other" 341 | Confirmed |
| Coca-Cola | CCBA 2024 revenue / EBIT; deal terms | EUR 3,357m / EUR 246m; USD 1.3bn for 41.52%; USD 3.4bn | Coca-Cola HBC CCBA presentation, 21 Oct 2025, slides 9 and 18 (PDF supplied by the PM) | Confirmed (see section 2 note on slide 13) |
| Coca-Cola | FY26 organic revenue range behind FY27-30 growth of 3.0% | 4-5% | Q4 2025 earnings release, 8-K exhibit 99.1, 10 Feb 2026 (SEC 0001628280-26-006642): "organic revenue (non-GAAP) growth of 4% to 5%". Raised to "approx. 5%" in the Q2 2026 release (SEC 0001628280-26-049922) | Range confirmed. Management's phrase "in line with our long-term growth algorithm" is still seen only in press reports of the call |
| Diageo | ROIC FY23 (memo: "18.4% to 13.4%") | 18.4% | Diageo 20-F FY24 (SEC 0000835403-24-000029): FY23 ROIC 18.4% on the restated basis (FY24 15.8%, "decreased 255bps") | Confirmed. The FY23 20-F originally reported 16.3% on the old basis, so the memo should say "restated" |

## 2. Still second-hand, but better corroborated

**Coca-Cola: African bottler (CCBA), EUR 3,357m revenue and EUR 246m EBIT (2024): CONFIRMED first-hand** (15 Oct 2026, from the PDF Amanda downloaded and attached; the site blocks automated downloads). Coca-Cola HBC, "Q3 2025 update and acquisition of CCBA" presentation, 21 Oct 2025, published on Coca-Cola HBC's investor relations site (coca-colahellenic.com) and kept in the project's shared files as cch-ccba-acquisition-presentation-21oct2025.pdf:
- Slide 9 ("CCBA is a diversified African bottler", 2024 financial highlights): net sales revenue **EUR 3,357m**, EBIT **EUR 246m**, EBIT margin 7.3%. Footnote 2: "FY-December 2024 CCBA audited financials excluding Ghana (sale completed on 25 July 2025), converted in EUR using the average 2024 US$/EUR exchange rate of 0.92425". 0.92425 EUR per USD = USD 1.0820 per EUR, the rate the desk used, so the desk's USD 3,632m and USD 266m match.
- Slide 18 (deal terms): 75% of CCBA for USD 2.6bn; **USD 3.4bn implied equity value**; Coca-Cola sells **41.52% for USD 1.3bn**; Gutsche Family Investments sells 33.48%; option over the remaining 25% held by Coca-Cola. All match the desk's inputs.
- Inconsistency inside the deck: the pro forma table on slide 13 shows CCBA at EUR 3.43bn revenue and EUR 0.253bn EBIT (7.3%), with the same footnote. The desk keeps slide 9's exact figures. Using slide 13's instead would move Coca-Cola's value by about -USD 0.03 a share (USD 50.22 vs 50.25), still SELL.

**Diageo: EABL FY26 sales KES 146.0bn and EBIT KES 32.1bn.** Diageo's 20-F does not give EABL's sales (only the held-for-sale balance sheet). Four independent Kenyan and trade press reports of EABL's results agree: sales KES 146.0bn (+13%), EBIT KES 32.1bn, margin 22%. Status: **corroborated, not first-hand** (eabl.com is blocked).

**Unilever: German 10-year Bund 3.45% on 13 Oct.** Readings for 13 Oct: 3.43% (Bundesbank figure as quoted by Hypofriend) and 3.466% (Cbonds). The desk's 3.45% sits between them. At 3.43% the value is 4,271p (+12p), still HOLD. Status: **corroborated, not first-hand.**

**RELX: UK 10-year gilt 5.45% on 13 Oct.** The only close found again is Investing.com's 5.4542%. Vantage gives 5.39% intraday. No new primary source. Status unchanged (the audit's sensitivity stands: 5.30% would add 40p, still SELL).

**All four: ERP 4.20% (Damodaran implied, 1 Oct 2026).** A fresh search reads the same 4.20% from Damodaran's home page. Still not seen directly (site blocked). Status unchanged. **Update 16 Oct 2026: confirmed at source** (home page and ERPbymonth.xlsx read directly once pages.stern.nyu.edu was allowed; erp-evidence.md, section 0).

## 3. Could not be reached at all
- Coca-Cola's own CCBA press release (not needed now that CCH's presentation is confirmed).
- EABL's annual report; United Spirits' share count (Diageo comps only).
- Bank of England and Bundesbank daily yields; Damodaran's site.
