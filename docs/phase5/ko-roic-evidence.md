# Coca-Cola: evidence for the terminal return on new investment (RONIC)

Prepared 13 Oct 2026 for the PM. The rule you set for Diageo: new investment after the forecast earns the company's latest return on invested capital (ROIC). Diageo publishes its ROIC (13.4% FY26). **Coca-Cola does not publish one** (searched the FY25 10-K and Q4 2025 results release), so it has to be calculated from the filings, and the definition matters.

## Definition used
- **NOPAT** = comparable (non-GAAP) operating income x (1 - tax rate). Comparable operating income strips out one-offs such as the fairlife remeasurement and BODYARMOR impairments, as Diageo's "before exceptionals" figure did.
- **Invested capital** = total equity (incl. minorities) + all borrowings + operating leases - cash - short-term investments - marketable securities - equity-method stakes. The stakes are taken out because their profits are not in operating income (they are valued separately in the bridge).
- Average of opening and closing invested capital.

Sources: comparable operating income and comparable tax rates from each year's Q4 results 8-K (accessions 0000021344-24-000004, 0000021344-25-000005, 0001628280-26-006642); balance sheet items from the 10-K XBRL files, read by the desk's own `desk/data_sources.py` (FY21-FY25 10-Ks).

| USD m | FY21 | FY22 | FY23 | FY24 | FY25 |
|---|---|---|---|---|---|
| Comparable operating income | | 12,345 | 13,336 | 14,085 | 15,013 |
| Comparable tax rate | | 19.0% | 19.0% | 18.6% | 20.6% |
| Invested capital (year end) | 38,869 | 36,534 | 37,572 | 39,449 | 45,448 |
| of which IRS deposit (non-operating) | | | | 6,000 | 6,000 |

## ROIC, three ways

| | FY22 | FY23 | FY24 | FY25 |
|---|---|---|---|---|
| A. Company's own tax rate | 26.5% | 29.2% | 29.8% | 28.1% |
| **B. DCF tax rate 23.7% (IRS case lost)** | **25.0%** | **27.5%** | **27.9%** | **27.0%** |
| C. As B, IRS deposit taken out of capital | 25.0% | 27.5% | 30.3% | 31.4% |

Notes:
- B uses the same 23.7% tax rate as the DCF, so the terminal year is internally consistent. That is why I recommend it over A.
- C is cleaner economically (the $6.0bn deposit is not operating capital), but the $6.1bn fairlife liability at end-2024 was debt-like too; adding it back pulls FY25 down to c.29%. The clean answer is about 29-31%, and the uncertainty over definitions is about 2 points.
- On every definition Coca-Cola earns about **twice** Diageo's 13.4%. A concentrate business needs little capital: bottlers own most plants and trucks.
- External benchmark: I did not find a published industry ROIC from a primary source, so none is used.

## Options
| Option | Terminal RONIC | Why |
|---|---|---|
| **1 (recommended)** | **27.0%** | Latest year (FY25), the same "latest ROIC" rule as Diageo, at the DCF's own tax rate. Reproducible from the 10-K, no judgement calls on the deposit or fairlife |
| 2 | 25.0% | Lowest of the four years (FY22). More conservative |
| 3 | 31.4% | FY25 with the IRS deposit removed. Economically cleaner, but adds a judgement call |

Higher RONIC means less reinvestment is needed for 2% growth, so more cash and a higher value. The valuation will show the impact of each option once the desk runs.
