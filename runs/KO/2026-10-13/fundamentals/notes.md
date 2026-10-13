# Fundamentals agent notes: The Coca-Cola Company (KO), run 2026-10-13

All money figures are **USD m** unless stated. Years are calendar FY21-FY25 (base year FY25, per `briefs/KO.yaml`).

## What I did
- `build_ratios.py` (in this folder; run it from the repo root with `PYTHONPATH=.`) reads `../data/financials.csv`. Every ratio goes through `desk/fundamentals.py` (`growth`, `margin`, `roic`, `cash_conversion`, `leverage`, `interest_cover`).
  - The script writes `ratios.csv` (item, year, value, unit, formula, inputs used, source) and `segments.csv`.
- The script also uses a few figures I read myself from the SEC filings, because they are not in financials.csv. Each is coded with its source:
  - organic growth as published;
  - comparable tax rates;
  - comparable interest expense;
  - FY20 revenue ($33,014m);
  - the IRS deposit in cash flow ($6,041m);
  - the fairlife payment ($6,069m).
- These come from the Q4 results 8-K exhibits 99.1:
  - FY21: 0000021344-22-000004
  - FY22: 0000021344-23-000005
  - FY23: 0000021344-24-000004
  - FY24: 0000021344-25-000005
  - FY25: 0001628280-26-006642
- Segment data comes from the FY25 10-K (0001628280-26-010047). Page numbers are the filing's printed page numbers.

## Checks (all pass)
- **Comparable operating margin:** my calculated figure equals the published one to 4 decimal places in every year (28.74 / 28.68 / 29.13 / 30.03 / 31.24%).
- **FCF:** my figures match the 8-K reconciliations: 11,258 / 9,534 / 9,747 / 4,741 / 5,296. Excluding the one-offs: FY24 10,782 and FY25 11,365.
- **Invested capital and ROIC:** these reproduce `docs/phase5/ko-roic-evidence.md` exactly. The brief's terminal RONIC of 27.0% (FY25, DCF tax rate 23.7%) is confirmed at 26.99%.

## Key ratios (from ratios.csv)
| | FY21 | FY22 | FY23 | FY24 | FY25 |
|---|---|---|---|---|---|
| Revenue growth, reported (USD) | 17.1% | 11.3% | 6.4% | 2.9% | 1.9% |
| Organic growth, published | 16% | 16% | 12% | 12% | 5% |
| Gross margin (reported) | 60.3% | 58.1% | 59.5% | 61.1% | 61.6% |
| Operating margin, reported | 26.7% | 25.4% | 24.7% | 21.2% | 28.7% |
| Operating margin, comparable | 28.7% | 28.7% | 29.1% | 30.0% | 31.2% |
| ROIC (comparable OI, 23.7% tax) | MISSING | 25.0% | 27.5% | 27.9% | 27.0% |
| ROIC (company comparable tax) | MISSING | 26.5% | 29.2% | 29.8% | 28.1% |
| ROIC (23.7%, ex $6.0bn IRS deposit) | MISSING | 25.0% | 27.5% | 30.3% | 31.4% |
| Cash conversion (FCF / net profit) | 115% | 100% | 91% | 45% | 40% |
| Cash conversion, ex IRS deposit / fairlife | 115% | 100% | 91% | 101% | 87% |
| Net debt (USD m, leases excluded) | 30,136 | 27,518 | 28,401 | 29,951 | 29,686 |
| Net debt / comparable EBITDA | 2.40x | 2.02x | 1.96x | 1.98x | 1.85x |
| Net debt / reported EBITDA | 2.56x | 2.26x | 2.28x | 2.71x | 2.00x |
| Interest cover, reported OI / net interest | 7.8x | 25.2x | 18.2x | 15.0x | 15.9x |
| Interest cover, comparable OI / comparable interest expense | 14.3x | 13.6x | 8.6x | 8.4x | 8.9x |

## Segment table (Coca-Cola's own operating segments, FY25 vs FY24, USD m)
**Sources:**
- Revenue and reported operating income: FY25 10-K Note 20, pp.116-117.
- Comparable revenue, reported and organic % change: Q4 2025 8-K ex.99.1, p.26. Organic is as published; the reported % change is also in 10-K MD&A p.45.
- Comparable operating income: Q4 2025 8-K, p.28.

The template regions (Europe, Africa) do not exist as separate segments: Africa sits inside EMEA and Bottling Investments.

| Segment | Revenue FY25 | Revenue FY24 | Reported % | Organic % (published) | Comparable OI FY25 | Comparable OI FY24 | Comparable margin FY25 |
|---|---|---|---|---|---|---|---|
| EMEA | 11,513 | 10,958 | +5% | +6% | 4,335 | 4,210 | 37.5% |
| Latin America | 6,334 | 6,471 | -2% | +10% | 3,831 | 3,872 | 60.1% |
| North America | 19,586 | 18,869 | +4% | +4% | 5,910 | 5,372 | 30.2% |
| Asia Pacific | 5,638 | 5,594 | +1% | +5% | 2,111 | 2,098 | 37.3% |
| Bottling Investments | 5,735 | 6,223 | -8% | +1% | 426 | 497 | 7.4% |
| Corporate | 144 | 110 | +30% | +30% | -1,600 | -1,964 | n/a |
| Eliminations | -1,009 | -1,164 | n/a | n/a | n/a | n/a | n/a |
| **Consolidated** | **47,941** | **47,061** | **+2%** | **+5%** | **15,013** | **14,085** | **31.2%** |

Segment revenue includes intersegment sales (EMEA 680, Asia Pacific 310). Segment margins are on comparable segment revenue.

## FLAGs
The FLAGs are listed in full in `commentary.md` under "Flags". In short:
1. FY24 reported margin of 21.2% is depressed by the fairlife remeasurement ($3,109m) and impairments ($886m).
2. Net profit in FY24 and FY25 distorts cash conversion.
3. Reported interest expense in FY21 and FY22 is not comparable (FY22 net cover 25.2x is an outlier).
4. FY25 net debt excludes CCBA's held-for-sale debt and cash (1,435 / 178).
5. There are no Europe or Africa segments, and Global Ventures was sunset on 1 Jan 2025.
6. Organic growth is published only in whole percent.
7. FY21 ROIC is MISSING.
8. The `desk/fundamentals.py` `leverage()` docstring cites Diageo's 2.5-3.0x target range.
9. The comparable margin rise includes the disposal mix effect.

## Missing
- **FY21 ROIC:** MISSING. It needs FY20 invested capital, which is not in the data folder.
- **Organic growth below whole-percent precision:** not published.
- **Segment organic growth before FY24:** not computed, because the segments were re-cut in 2025.
- **CCBA's own figures:** not in KO's filings. See data/notes.md FLAG 1 and docs/phase5/ko-ccba-evidence.md.

## Confidence
- **High** for the reported ratios and the comparable margin and ROIC, all tied to filings.
- **Medium** for the cash conversion interpretation, because the net-profit denominator includes non-cash items.
- **Medium** for comparability of segments across years.
