# Fundamentals agent: RELX PLC (RELX / REL.L), run 2026-10-14

All money is **GBP m** (RELX reports in pounds). Ratios are decimals. Nothing in `briefs/`, `desk/` or other agents' folders was changed.

## What I did
- Wrote `run_fundamentals.py`. Every ratio goes through `desk/fundamentals.py` (growth, margin, roic, cash_conversion, leverage, interest_cover). Re-run from the repo root: `PYTHONPATH=. python runs/RELX/2026-10-14/fundamentals/run_fundamentals.py`.
- **Sources.** I read the primary filings directly from SEC EDGAR (CIK 929869) and cite document and page for each:
  - Annual Reports 2025, 2024, 2022 and 2021 (20-F ex 15.2)
  - FY21-FY25 results releases and the H1 2026 interim results (6-K ex 99.1)
  - Page numbers come from the page headers in each document. Every value I used from the Data agent's `financials.csv` agrees with these filings.
- `ratios.csv` (130 rows): item, year, value, unit, formula, inputs, basis, source. Covers FY21-25, plus H1 2025 and H1 2026 where useful.
- `segments.csv` (47 rows):
  - RELX's five operating segments (Risk, STM, Legal, Exhibitions, Print & print-related) for FY23 restated, FY24 restated, FY25, H1 2025 and H1 2026: revenue, adjusted operating profit (adj. OP), margin, change in GBP, and underlying and constant-currency growth as published.
  - FY24 underlying growth on the old segment basis.
  - The three geographic markets.
  - Placeholder rows for the template regions that RELX does not report.
- `brief_checks.csv` (11 rows): each brief assumption next to the record. The brief is read from file, not changed.
- `commentary.md`: 287 words.

## Checks
My calculations reproduce every figure RELX publishes:
- **ROIC:** 11.9%, 12.5%, 14.0%, 14.8%, 15.4%.
- **Adjusted cash flow conversion:** 101%, 101%, 98%, 97%, 99%.
- **Adjusted margins:** 30.5% to 34.8%.
- **FY25 and H1 2026 ex-print margins:** 34.3% and 35.0%, which match the brief's margin evidence file.

## Definitions used
- **Organic growth:** RELX's published "underlying" growth. It excludes currency, acquisitions for 12 months, disposals and exhibition cycling, and from 2025 also print. I also show constant-currency growth, which still includes print run-off, disposals and cycling. Neither is recomputed.
- **Operating margin before exceptionals:** RELX's adjusted operating profit (non-GAAP). It excludes amortisation of acquired intangibles and acquisition/disposal items, and grosses up the joint-venture share for JV tax and interest. The reported (IFRS) margin is shown alongside it.
- **Margins with and without print:**
  - FY23 and FY24 come from RELX's own restatement (AR25 note 1 p.145; note 2 p.146).
  - The facts pack listed FY23 ex-print as missing, but **it is in AR25 p.145**: print revenue 586, adj. OP 253.
- **ROIC, two measures:**
  - (a) RELX's definition: adjusted OP x (1 - adjusted ETR) / average invested capital. Invested capital adds back all accumulated acquired-intangible amortisation and goodwill impairment, so it counts acquisitions at cost. RELX publishes only the average, so I pass it to `roic()` as both opening and closing.
  - (b) Book ROIC: the same NOPAT over the average of opening and closing net capital employed (FY20 9,536 to FY25 10,322; AR21 p.63, AR22 p.85, AR24 p.206, AR25 p.204).
- **Cash conversion:**
  - Desk definition: RELX's "free cash flow before dividends" (after capex, lease principal, interest, tax and acquisition costs) / reported net profit attributable to shareholders.
  - Also shown: FCF / adjusted net profit, and RELX's own KPI (adjusted cash flow / adjusted OP).
- **Leverage:**
  - Net debt as published (RELX definition, includes leases; AR25 p.186) / adjusted EBITDA, in GBP.
  - Also shown ex leases (the brief's basis), and RELX's published USD ratio for reference.
  - 30 Jun 2026: LTM EBITDA = FY25 - H1 2025 + H1 2026.
- **Interest cover:** adjusted OP / adjusted net interest, and IFRS OP / reported net finance costs.

## FLAGs
1. **Bear margin label.** The brief's bear margin of 33.1% is called "FY23 level". That is the FY23 **group** margin, including print. On the brief's own ex-print basis, FY23 was **32.4%**. Applied as an ex-print margin, 33.1% is a milder stress than the label suggests: 0.7 points less severe (ratios.csv `bear_margin_minus_fy23_ex_print_margin`). For the Bear agent and Amanda. I have not changed the brief.
2. **Margin base vs revenue base (also raised by the Data agent).** The 35.0% margin excludes print, but it is applied to FY25 revenue of 9,590, which includes print of 399. Print earned 46.4% in FY25 and 49.7% in H1 2026. This slightly understates near-term profit while print still exists, so it is cautious. It is consistent with the run-off reasoning.
3. **Growth (FY27-30 at 5.0%) looks cautious, not aggressive.**
   - Underlying growth has been 7-9% every year.
   - The constant-currency figure that the 5.0% is based on carried a print drag of 1.2 points in FY25. That drag shrinks as print shrinks: print revenue fell 22.8% in FY25 and 16.9% in H1 2026.
   - Disposals (1.0 point) and exhibition cycling (0.5 point) are lumpy and also cut FY25 growth.
   - The FY21-25 average reported GBP growth was 6.3%, inflated by FY22 (+18.1%, including +7 points of currency and the Exhibitions recovery).
4. **Capex at 7.10% is the highest level on record.** Capex including pre-publication spend was 6.1% (FY24), 6.5% (FY25), 6.3% (H1 2025) and 7.1% (H1 2026). It is cautious relative to history. D&A on the brief's basis was 4.9% in FY25 against 5.07% in the brief. Consistent.
5. **Terminal RONIC 15.4%** equals RELX's own ROIC. Recomputed at the brief's 22.8% tax rate it is 15.36%, which is immaterial. Book ROIC is 24.8%. The brief takes the cautious measure, so this is consistent.
6. **FY21 adjusted OP includes a £35m one-off real-estate charge** (FY21 results p.2). The margin without it is 31.0%, against 30.5% as reported. Margin expansion from FY21 to FY25 is therefore 3.9 points without the charge, against 4.3 points as reported (ratios.csv `adjusted_margin_change_*`).
7. **FY25 gross margin rose 1.3 points (65.0% to 66.3%; ratios.csv `gross_margin_change`) while cost of sales fell in pounds (3,300 to 3,233, AR25 p.138).** The likely cause is the print run-off (print is lower-margin at gross level), but RELX does not explain it. **Not verified.**
8. **Leverage basis.** My GBP ratio (1.87x FY25) is below RELX's published 2.0x. RELX's figure is calculated in USD, adds unfunded pensions (154) and removes JV EBITDA (57) (AR25 p.205-206). Leverage rises to 2.2x at June 2026 because of the £1,750m H1 buyback. Adjusted EBITDA includes lease depreciation, so the ex-lease ratio slightly understates leverage. Immaterial (97 of leases).
9. **Interest cover dropped in FY23** (adjusted 13.8x to 9.6x) when net interest rose from 194 to 314 on higher rates. It has since recovered to 11.8x.
10. **Exhibitions FY25:** constant-currency growth was -2% while underlying was +8%, because of cycling (biennial shows). Its H1 2026 margin (39.3%) is seasonal and not comparable with the full year.

## Missing
- **The five-region template (North America, Europe, Asia Pacific, Latin America & Caribbean, Africa) does not fit RELX.** RELX reports only North America, Europe (including the UK) and Rest of world, by geographic market (AR25 note 2 p.146-147; H1 2026 p.24). Asia Pacific, Latin America and Africa are **not published**. I used RELX's own split. RELX's operating segments are business areas, not regions, and those are in `segments.csv`.
- **Organic (underlying) growth by region is not published.** Only the change in GBP is shown.
- FY21-FY22 segment figures on the new ex-print basis (RELX restated back to FY23 only). FY21-23 margins ex print before FY23 cannot be built.
- Segment underlying growth for FY23-24 on the restated basis (not published). FY24 growth on the old basis is in `segments.csv`, labelled.
- Opening and closing invested capital on RELX's definition for FY21-23. Only averages are published, so they are used.
- `python -m pytest` could not run because pytest is not installed in this environment. I changed no code in `desk/`.

## Confidence
- **Ratios: high.** Every input is sourced to a primary filing page, and every ratio RELX publishes is reproduced.
- **Segments and geography: high** for revenue and adjusted OP (AR25 note 2; H1 2026 p.4 and p.24).
- **Brief tests: high** on the arithmetic. The judgement that growth and capex are cautious is mine (medium).
