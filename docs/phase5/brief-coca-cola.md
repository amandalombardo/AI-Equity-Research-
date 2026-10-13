# AI Equity Research Desk: Brief v1.0 (FINAL)
**Company:** The Coca-Cola Company (NYSE: KO, S&P 500)
**Portfolio manager:** Amanda
**Status:** Signed off by Amanda (PM) on 13 October 2026. Any change needs PM approval and a version bump.

---

## 1. The investment question
> Is Coca-Cola a **Buy, Hold or Sell** for a 12-month horizon at today's price, given a premium valuation, a pending court ruling on a c.$15bn US tax bill, and a business that is selling its bottlers to become "asset-light"?

## 2. Company snapshot (FY25, year ended 31 Dec 2025)
Sources: 10-K FY25 (SEC accession 0001628280-26-010047, filed 20 Feb 2026); Q4 2025 results 8-K (0001628280-26-006642, 10 Feb 2026); Q2 2026 results 8-K (0001628280-26-049922, 28 Jul 2026); Q2 2026 10-Q (0001628280-26-050503). The Data agent re-checks every figure.

| Item (USD) | FY25 | Note |
|---|---|---|
| Net revenues | $47.9bn, +2% | Organic (non-GAAP) +5%; unit case volume flat |
| Operating income (reported) | $13.8bn, margin 28.7% | Comparable (non-GAAP) margin 31.2% (FY24 30.0%, FY23 29.1%) |
| EPS | $3.04 reported; $3.00 comparable | |
| Cash from operations | $7.4bn | Depressed by the $6.1bn fairlife milestone payment. FCF ex-fairlife $11.4bn |
| FY24 cash from operations | $6.8bn | Depressed by the $6.0bn IRS tax deposit. FCF ex-deposit $10.8bn |
| Gross debt, 3 Jul 2026 | $43.5bn | $48m + $6,494m + $37,001m (10-Q balance sheet) |
| Cash, short-term investments and marketable securities, 3 Jul 2026 | $16.4bn | $13,529m + $2,842m |
| Equity method investments (bottlers, Monster) | $20.8bn at book | Listed stakes worth $34.3bn at market vs $14.0bn book (31 Dec 2025, 10-K) |
| Share price | $89.79 (12 Oct 2026, Yahoo) | c.4,303m shares, so c.$386bn market value |
| CEO | Henrique Braun | (Q2 2026 release) |

**FY26 guidance (raised 28 Jul 2026):** organic revenue c.5%; currency +1%; acquisitions/disposals -2% to -3%; underlying tax rate 19.9% (excludes the IRS case); comparable EPS +9-10%; FCF c.$12.4bn (cash from operations $14.6bn less capex $2.2bn).

## 3. Data traps (new ones the desk has not seen before)
1. **US accounting (10-K, US GAAP).** The desk's data code looks for Diageo's own labels. KO needs a new label map (e.g. `us-gaap:Revenues`, `us-gaap:OperatingIncomeLoss`). Code change on a branch with a PR.
2. **Prices in US dollars, no ADR.** Value per share in USD, benchmark S&P 500. No pence conversion.
3. **Two one-off cash hits.** FY24 ($6.0bn IRS deposit) and FY25 ($6.1bn fairlife payment) distort cash flow. Cash conversion and capex history must be shown with and without them.
4. **Argentina inflation inflates "organic" growth.** Organic growth was +12% in FY23 and FY24, but reported revenue grew only +6% and +3%. More than half of Q4 2024 price/mix came from inflationary pricing in Argentina (Q4 2024 release). In a USD DCF, inflation pricing is mostly cancelled by currency falls, so organic growth cannot be used directly (like Türkiye for Diageo, but much bigger).
5. **Refranchising.** KO keeps selling bottlers (Africa/CCBA to Coca-Cola HBC, pending, expected by end 2026). This shrinks revenue but lifts margins. Forecast ex-CCBA and add sale proceeds to the bridge (same rule as EABL).
6. **Equity income sits below operating income.** The DCF of operating cash flow excludes the bottler stakes and Monster, so they must be added in the bridge. Book value understates the listed stakes by c.$20bn.
7. **The IRS case.** See section 5c.
8. **Calendar year-end (31 Dec).** No calendarisation needed for US peers; Diageo's June year is the odd one out.

## 4. What each agent must produce
Same as Diageo (brief-diageo.md section 4), with the S&P 500 replacing the FTSE 100 for beta and benchmark, and USD replacing pence.

## 5. Valuation assumptions (agreed by PM, 13 Oct 2026)
Base year FY25 (latest audited). Forecast FY26 to FY30. USD throughout.

| # | Assumption | Proposal | Evidence / why | Status |
|---|---|---|---|---|
| A | Revenue growth (USD) | FY26 +3.5% (guidance: 5% organic +1% FX -2.5% disposals); FY27-30 **3.0%** a year (low end of 4-5% organic range minus a 1-point currency drag) | Evidence in ko-growth-evidence.md: currency cost 1 point a year outside the Argentina years, 3.2 points on average 2020-25 | **Agreed** 13 Oct 2026 |
| B | Operating margin | Comparable margin 31.2% (FY25), held flat; bear 30.0% (FY24) | Margin rose c.1 point a year FY23-25, partly from selling low-margin bottlers. Holding flat avoids paying for gains not yet earned | Agreed 13 Oct 2026 |
| C | IRS tax dispute | Base case: **KO loses**. Deduct the c.$14.9bn potential liability ($14bn to Dec 2025 + $0.9bn H1 2026, 10-Q Note 12) and use a 23.7% tax rate (19.9% + 3.8 points, 10-Q). Bull: KO wins, $6bn deposit refunded | The only court ruling so far (US Tax Court 2020, 2023) went against KO. Appeal heard 25 Jun 2026, ruling pending. Management's own guidance excludes it, so the market price may not | **Agreed** 13 Oct 2026 |
| D | Bottler and Monster stakes | Listed stakes at **market value** on the run date (was $34.3bn, 31 Dec 2025); unlisted at book | Same logic you applied to Diageo's minorities: book value failed the evidence test | Agreed 13 Oct 2026 |
| E | Tax rate (if KO wins) | 19.9% underlying (FY26 guidance) | Q2 2026 release | Agreed 13 Oct 2026 |
| F | Capex, D&A, working capital | 5-year averages ex one-offs, from the Data agent; FY26 capex $2.2bn per guidance | 10-Ks | Agreed 13 Oct 2026 |
| G | Beta | Bottom-up: Damodaran US soft drinks/beverage unlevered beta, relevered at KO's market D/E; regressions vs S&P 500 as cross-check | Same rule as Diageo | Agreed 13 Oct 2026 |
| H | Risk-free, ERP, cost of debt | US 10-year (5.22%, FRED, 8 Oct 2026); ERP 5.0%; cost of debt = risk-free + spread for KO's A+ rating (ICE BofA A OAS was 0.69% on 8 Oct 2026) | Same rule as Diageo, but KO is rated higher | Agreed 13 Oct 2026 |
| I | Terminal growth / terminal capex | 2.0%; terminal capex via RONIC = KO's latest ROIC (Data agent) | Same rule as Diageo | Agreed 13 Oct 2026 |
| J | Mid-year discounting | Yes | H1 2026 FCF $6.9bn of $12.4bn guided = 56% in the first half (Q2 2026 release) | Agreed 13 Oct 2026 |
| K | Valuation basis | 31 Dec 2025 balance sheet, rolled forward to run date at cost of equity less dividends paid | Same as Diageo | Agreed 13 Oct 2026 |
| L | Rating rule | Buy >= +15%, Sell <= -10% | Same as Diageo, so the portfolio is consistent | Agreed 13 Oct 2026 |

### Comparables (proposal)
PepsiCo, Keurig Dr Pepper, Monster Beverage, Coca-Cola Europacific Partners (bottler, flagged), plus Diageo as an out-of-sector cross-check. EV/EBITDA, P/E, FCF yield; medians.

### Not yet verified
- KO's long-term growth algorithm. Management called the 4-5% FY26 organic guidance "in line with our long-term growth algorithm" (Q4 2025 call, per press summaries), but I have not found the algorithm in a primary source. Until then, only the FY26 guidance is used.

## 6. Checks
Same as Diageo: independent Excel check within 2%, source check of 5 random numbers, mistakes log.

## 7. Decisions
| # | Decision | Status |
|---|---|---|
| 1 | Companies for Phase 5: KO, Unilever, RELX, one at a time, KO first | **Agreed** 13 Oct 2026 |
| 2 | IRS case: base case assumes KO loses (deduct c.$14.9bn, tax rate 23.7%); bull case shows a win | **Agreed** 13 Oct 2026 |
| 3 | Growth: FY26 +3.5%, FY27-30 3.0% a year in USD; bear 1.0% | **Agreed** 13 Oct 2026, evidence in ko-growth-evidence.md |
| 4 | Margin flat 31.2% (bear 30.0%), listed stakes at market, mid-year discounting | **Agreed** 13 Oct 2026 |
| 5 | Benchmark: S&P 500 | **Agreed** 13 Oct 2026 |
