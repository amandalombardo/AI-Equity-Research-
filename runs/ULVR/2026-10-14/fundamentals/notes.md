# Fundamentals agent: Unilever (ULVR), run 2026-10-14

## What I did
- Wrote `run_fundamentals.py`, which calls `desk/fundamentals.py` (growth, margin, roic, cash_conversion, leverage, interest_cover). To re-run it: `PYTHONPATH=. python runs/ULVR/2026-10-14/fundamentals/run_fundamentals.py`.
- `ratios.csv` (88 rows) records, for each ratio: item, year, value, unit, formula, inputs, basis and source (filing + page). Every money input is in EUR m and every ratio is a decimal.
- `segments.csv` (22 rows): Unilever's four business groups, which are its operating segments (FY25 20-F p.137), and its geographic split. The geographic split is "additional information", not a segment (p.138). The file also has country rows (US, India, UK; p.138) and the Foods sale perimeter (Form 425 slide 25).
- `commentary.md` is 287 words.
- Added `minority_share_of_operating_profit` = **0.10684** to `../inputs.yaml`. No other key was changed.
- Checks: my ratios reproduce Unilever's published figures. ROIC: 17.2%, 16.0%, 16.2%, 18.0/18.1% (FY24 incl. Ice Cream), 19.1% (FY24 ex Ice Cream), 19.0% (FY25). Net debt/UEBITDA: 2.2x, 2.1x, 2.1x, 1.9x, 2.0x. FY25 gross margin is 46.9%, underlying margin 20.0%.

## Bases (each row in ratios.csv is labelled)
- FY21-22: the Group including Ice Cream, as first reported.
- FY23-25: continuing operations re-presented without Ice Cream (FY25 20-F).
- FY23 ROIC, FCF, net debt and UEBITDA exist only including Ice Cream, so they are labelled that way. The FY23-24 margins and growth are given on both bases.
- Reported sales growth is always calculated on the same basis for both years. FY23 is -0.8% including Ice Cream, because no FY22 figure without Ice Cream exists.

## Minority share (proportionate method): how it was built
`m = FY24 minorities' share of Group underlying net profit x Group UOP FY25 / (Group UOP FY25 - Foods perimeter UOP)`
- Minorities' underlying profit, FY24 = 609 (NCI share of continuing profit, 20-F p.128) - 22 (NCI share of non-underlying items, p.42) = EUR 587m.
- Group underlying profit, FY24 = 6,816 (shareholders, p.43) + 587 = EUR 7,403m. Minorities' share = **7.93%**.
- Converting to the remaining company: x 10,084 / (10,084 - 2,600) = x 1.3474. Result: **10.68%**.
- HUL is the main part. Its minorities took 446 of 1,167 (38.2%, p.162 note 15B), which matches the 38.1% outside holding (61.90%, p.194). HUL alone is 6.0% of Group profit; the rest is other subsidiaries such as PT Unilever Indonesia (85% owned, p.183).
- Cross-checks: FY25 gives 10.39%; H1 2026 gives 9.46%. I chose FY24, as instructed. It is also the highest of the three, so the most cautious.
- FLAG, assumption A1: I treat the minorities' share of operating profit as equal to their share of net profit. HUL has net cash, so this slightly overstates their share of operating profit.
- FLAG, assumption A2: I assume no minority profit leaves with the Foods perimeter. HUL, including India Foods, stays, but the Foods businesses of other part-owned subsidiaries (e.g. Indonesia) do go. This also overstates slightly. It cannot be quantified because the perimeter is not split by subsidiary.
- FLAG: FY25 HUL is distorted. Minorities' share of profit was 539 against HUL profit of 940, i.e. 57%, linked to HUL's ice cream demerger (EUR 199m non-cash dividend). Not used.
- The Diageo run used pre-tax "profit before exceptionals attributable to NCI" from its ROIC table. Unilever discloses no equivalent, so this ratio is built at net-profit level. Suggestion for Amanda: add a `minority_share()` helper to `desk/fundamentals.py` on a branch, so this step goes through desk/ like the rest.

## FLAGs
1. **Data agent labels (financials.csv).** `net_profit_to_owners` FY23 (6,487) and FY25 (9,469) are TOTAL profit, including discontinued operations, but are labelled "continuing". Continuing figures: 6,002 and 5,682 (20-F p.128). `operating_cash_flow` FY24 (9,519) and FY25 (8,350) are also totals; continuing figures are 8,461 and 8,052. FY25 total profit includes a EUR 3,373m non-cash demerger gain. Anyone using these rows for cash conversion would get the wrong answer.
2. **FY22 reported margin (17.9%) is above underlying (16.1%).** This comes from a EUR 1,072m net non-underlying gain, mainly the Tea (ekaterra) sale. The same gain cuts FY22 cash conversion to 68%; Unilever's own measure, which excludes disposals, is 97%.
3. **FY24 reported margin is 16.8% against 19.4% underlying.** The gap is EUR 1,369m of disposal losses and productivity programme costs. FY24 cash conversion of 116% is flattered because continuing net profit is depressed (Unilever's measure: 104%).
4. **FY24 leverage:** 1.9x as first reported, but 2.1x when Ice Cream EBITDA is removed while the debt stays. The FY25 ratio (2.0x) is on the new basis.
5. **The gross margin step-up partly reflects the Ice Cream removal.** FY23 is 43.5% without Ice Cream against 42.2% with it, and FY24 is 46.7% against 45.0%. Some of the FY21-25 rise is portfolio mix, not pricing.
6. **Restructuring is recurring:** 0.8-1.4% of turnover in every year from FY21 to FY25. This supports the brief's deduction from the underlying margin.
7. **The Foods perimeter margin (24.3%) is above the Foods business group (22.6%) and the Group (20.0%).** The remaining company earns 18.8%. The ROIC of the remaining company is not disclosed, and Foods holds EUR 7.9bn of the EUR 17.7bn goodwill (20-F p.153), so ROIC after the sale may differ from 17.8%. This is the same point as the brief's FLAG.
8. **Interest cover** uses reported net finance costs, which are reduced by the pension interest credit (the plan is in surplus). Cover would be a little lower on gross bond interest.

## Missing
- Africa: no separate turnover or USG figure; it is inside "Asia Pacific Africa" (20-F p.12 says only "low single-digit"). The brief's five-region template (NA / Europe / APAC / LatAm / Africa) does not match Unilever's split. I used its own: Asia Pacific Africa, The Americas (North America + Latin America) and Europe.
- USG for Asia Pacific Africa (4.6%) and The Americas (3.3%) is not in the 20-F text, so it is taken from the FY25 results 6-K geographic table. US and UK USG are not published.
- FY23 USG and FY24 business-group USG without Ice Cream are not published; the figures used are as first reported (labelled).
- FY24 opening and closing invested capital without Ice Cream: only the average (39,559) is disclosed, so it is passed to roic() as both opening and closing.
- `python -m pytest` could not run: pytest is not installed in this environment. No desk/ code was changed.

## Confidence
- Ratios: high. Every value ties to Unilever's published numbers within rounding.
- Segments: high for turnover and margins (20-F p.137-138). Medium for regional USG, because two figures come from the 6-K.
- Minority share: medium. The inputs are fully sourced, but the result depends on assumptions A1 and A2, both of which push it slightly up. The range across periods is 9.5-10.7%.
