# RELX: beta evidence (14 Oct 2026)

Method agreed for Unilever (decision 8): bottom-up beta = Damodaran global industry unlevered beta (corrected for cash), relevered at the company's market debt-to-equity and its tax rate (Hamada: levered = unlevered x (1 + (1 - tax) x D/E)). Script: phase5/data/relx_beta_check.py (regressions with the desk's own beta function).

## Industry betas (Damodaran betaGlobal.xls, updated 5 Jan 2026, the file you uploaded)
| Industry | Firms | Unlevered beta, corrected for cash | Fits |
|---|---|---|---|
| **Information Services** | 86 | **0.8737** | Risk and Legal (data and analytics); Damodaran's own home for RELX-type firms |
| Publishing & Newspapers | 307 | 0.7788 | STM (journals) and print |
| Business & Consumer Services | 994 | 0.9083 | Exhibitions |

## Relevered for RELX
Market value of equity: 2,771p x 1,747.0m shares = £48.4bn (13 Oct 2026). Tax 22.8% (agreed).

| Option | Unlevered | Net debt used | D/E | **Levered beta** |
|---|---|---|---|---|
| **A (recommended)** | 0.8737 Information Services | £7,201m (31 Dec 2025, the bridge date, as for Unilever) | 14.9% | **0.974** |
| B | 0.847 segment-weighted (FY25 revenue: Risk + Legal as Information Services, STM + print as Publishing, Exhibitions as Business Services) | £7,201m | 14.9% | 0.944 |
| C | 0.8737 | £8,733m (30 Jun 2026, after buybacks) | 18.0% | 0.995 |

## RELX's own regression betas vs the FTSE 100 (Yahoo, dividend-adjusted, to 13 Oct 2026)
| Window | Beta | R-squared |
|---|---|---|
| 2 years weekly | 0.67 | 0.08 |
| 5 years weekly | 0.66 | 0.12 |
| 5 years monthly | 0.38 | 0.04 |

The regressions explain 4-12% of RELX's moves, so they are too noisy to use (the same reason we rejected Unilever's own 0.54). The FTSE 100 is also a poor market proxy for a company earning 58% of revenue in North America.

Recommendation: **A, 0.974**. It is the agreed method, the industry that fits most of the profit, and Damodaran classifies data-and-analytics firms there. B gives STM a publishing beta, which understates its subscription-data character, but it is shown as a check (-0.03).
