# Evidence audit of all four companies, 15 Oct 2026

Four independent auditors re-checked every assumption and memo number against primary sources (SEC filings and XBRL, FRED, Yahoo, the Damodaran beta files). All 66 tests pass. Detailed reports: DGE.md, KO.md, ULVR.md, RELX.md, erp-evidence.md in this folder.

## Verdict

| Company | Current call | Numbers checked at source | Wrong numbers found | Rating after all sourced fixes |
|---|---|---|---|---|
| Diageo | HOLD 1,627p vs 1,673p | about 30 | 1 (share count, -1.5p) | HOLD (about 1,605p) |
| Coca-Cola | SELL USD 47.60 vs USD 90.12 | 13 | 0; bear case missed your 31.9% margin | SELL (USD 46.73) |
| Unilever | SELL 3,855p vs 4,710.5p | 38 | 0 | SELL (3,915p) |
| RELX | SELL 1,621p vs 2,771p | about 30 | 0 | SELL |

No finding changes a rating on its own. The input data is sound. The gaps are in judgement inputs that were never given a source.

## 1. The common gap: equity risk premium (ERP) 5.0%, no source for any company

| ERP | Diageo | Coca-Cola | Unilever | RELX |
|---|---|---|---|---|
| 4.20% (Damodaran implied, 1 Oct 2026) | 1,811p HOLD | USD 51.31 SELL | 4,234p SELL (-10.1%) | 1,821p SELL |
| 5.00% (current; Kroll's recommended US figure) | 1,627p HOLD | USD 47.60 SELL | 3,855p SELL | 1,621p SELL |
| 5.50% (Fernandez 2025 survey, US/UK) | 1,527p HOLD | USD 45.56 SELL | 3,657p SELL | 1,514p SELL |

Unilever turns HOLD below 4.19%. Every outside ERP figure was seen only in search summaries (Damodaran, Kroll, Fernandez and UBS sites are blocked here). Recommendation: 4.2% (Damodaran implied), because it is the only measure built to sit on top of today's bond yields, which the desk uses. Full pack: erp-evidence.md.

## 2. Other judgement inputs with weak or no source

- Diageo FY30-31 growth 3% (the desk's own IWSR evidence argues lower; 2% = -27p). Terminal growth 2% (all four) rests on the 2% inflation target only.
- Coca-Cola FY27-30 growth 3% rests on a "4-5% algorithm" never found in a primary source; FY26 6.0% ignores about 1 point of non-CCBA disposals (-USD 0.47).
- Unilever FY26 growth +0.5% includes Foods, which the model excludes; Home and Personal Care grew +2.0% (+54p).
- RELX gilt 5.45% and Unilever Bund 3.45% come only from aggregator websites (+40p RELX if 5.30%).

## 3. Clear errors to fix (value change, no rating change)

1. Coca-Cola bear case uses 33.2% margin, not your 31.9% (USD 37.99 should be USD 36.48).
2. Coca-Cola was not re-run after the listed-stakes fix (mistakes row 24): USD 47.01, not USD 47.60.
3. Diageo share count deducts 2m trust shares twice (-1.5p); dilution ignored (-6.6p).
4. Unilever pension: EUR 944m of plans in deficit hidden behind a net surplus (-29p after tax); McCormick dividends before closing can be sized (-17p to -25p).

## 4. Misleading or out-of-date write-ups (no value change)

- brief-diageo.md, brief-coca-cola.md, brief-unilever.md still show old figures that the yaml files later replaced.
- relx-capex-evidence.md gives the wrong reason for leaving out leases.
- Memos omit: RELX industry forecast MISSING; credit spreads are US-dollar indices added to gilt/Bund yields; Coca-Cola's 3M appeal win in the IRS case (KO at USD 54.90 if it wins, still SELL); Diageo leverage caveat.
- Agents' notes still show superseded tables and "PM review pending".
- memo_check only proves a number appears somewhere in the run folder, not that it means the same thing.

## Process slip

The RELX auditor's first SEC download sent Amanda's email as the contact header (SEC asks for one). It switched to a generic address after that.
