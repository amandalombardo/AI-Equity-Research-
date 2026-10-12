# AI Equity Research Desk

A team of six AI agents that produces a two-page buy/hold/sell investment memo on a listed company.
**Portfolio manager: Amanda.** She writes the brief, sets the assumptions, challenges the outputs and makes the final call.
Claude Code builds the desk, Codex independently audits the maths, and Amanda validates the key numbers against her own Excel model.

First company: **Diageo plc** (LSE: DGE).

## How to run it
1. Open this repository in Claude Code.
2. Type `/run-desk DGE`.
3. Claude Code runs the six agents in order and finishes with a key-numbers table to check against Excel, every warning raised, and links to the memo PDF and the DCF spreadsheet.

Results are saved in `runs/DGE/<date>/`, with one folder per agent. If a number in the memo looks wrong, open the agent folders to see exactly where it came from.

## The agents
| Agent | Job | Key output |
|---|---|---|
| Data | Downloads Diageo's SEC filings, share prices, interest rates and FX, and records a source for every number | `inputs.yaml`, `financials.csv` |
| Fundamentals | Growth, margins, returns, cash conversion, leverage | `ratios.csv`, `commentary.md` |
| Valuation | DCF (in USD, converted to pence at the end) and comparable companies | `valuation.json`, `dcf.xlsx` |
| Risk | Beta vs the FTSE 100, volatility, drawdown | `risk.json` |
| Bear case | Argues against buying and puts a pence-per-share value on each challenge | `challenges.md` |
| Editor | Writes the two-page memo using only numbers the other agents produced | `memo.pdf` |

## Why the AI doesn't do the maths
AI models are good at reading filings and writing, but unreliable at arithmetic. All calculations (DCF, WACC, beta, ratios) are fixed formulas in the `desk/` folder, which means:
- Codex can audit the formulas line by line
- the automated tests in `tests/` check them against answers calculated by hand
- `dcf.xlsx` contains live Excel formulas, and a test confirms the Excel and Python results agree exactly.

## What's where
| Path | What it is |
|---|---|
| `briefs/DGE.yaml` | The PM's assumptions for Diageo, each with its source |
| `.claude/agents/` | The instructions for each of the six agents |
| `.claude/commands/run-desk.md` | The `/run-desk` command |
| `desk/dcf.py` | WACC, DCF, terminal value, EV-to-equity bridge, sensitivity |
| `desk/comps.py` | Comparables, including calendarising peers to a June year end |
| `desk/risk.py` | Beta, volatility, maximum drawdown |
| `desk/fundamentals.py` | Financial ratios |
| `desk/units.py` | Pence/pounds and ADR conversions |
| `desk/rating.py` | The Buy/Hold/Sell rule (Buy at 15% or more upside, Sell at 10% or more downside) |
| `desk/excel_export.py` | Writes the DCF to Excel with live formulas |
| `desk/memo_check.py` | Checks that every number in the memo traces back to an agent output |
| `desk/data_sources.py` | Downloads data from SEC EDGAR, Yahoo Finance and FRED |
| `tests/` | Automated checks. Run with `python -m pytest` |

## Setup (one-off)
`pip install -r requirements.txt`. Set `SEC_CONTACT_EMAIL` to your email: the SEC refuses automated downloads (HTTP 403) that do not identify themselves. The data download needs internet access to `data.sec.gov`, `www.sec.gov`, `query1.finance.yahoo.com`, `query2.finance.yahoo.com`, `fc.yahoo.com` and `fred.stlouisfed.org`.
