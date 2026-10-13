# Diageo after Phase 3 review: 12 October 2026

**Model output: HOLD. Fair value 1,545p vs share price 1,673p (-7.7%).** Bear scenario 1,108p.
**The HOLD is fragile:** SELL starts at 1,506p, only 39p below fair value. Any one of these flips it to SELL: savings flow-through below 33.6%, new investment earning below 11.7% instead of 13.4%, a beta above 0.997, terminal growth of 1.5%, a credit spread of 2%, or USL's minority valued at its market price.

Files: [memo PDF](diageo-memo-phase3.pdf), [dcf.xlsx](dcf.xlsx) (live formulas, recalculated: 1,544.8p, same as Python), [Codex audit](../phase3/codex-audit-2026-10.md). The code is in PR #3. Evidence audit of every input: [evidence-audit.md](../phase3/evidence-audit.md).

## How we got from 1,448p (SELL) to 1,545p (HOLD)
| Step | Who decided / found it | Value | Change |
|---|---|---|---|
| Start: first run after your beta and cost-of-debt decisions | | 1,448p | |
| 1. Terminal year made a true steady state (working capital grows at 2%, not 3%) | Claude's review; Codex found it independently | 1,474p | +27p |
| 2. Terminal capex set so new investment earns Diageo's ROIC 13.4% (6.21% of sales, was 7.11%) | **Your decision** | 1,540p | +65p |
| 3. Savings flow-through 46% (low end of FY27-29 profit guidance, was 50%) | **Your decision** | 1,527p | -13p |
| 4. Valued at the 30 June balance sheet date and rolled forward to 12 Oct at the cost of equity | Codex finding BRIDGE-01 | 1,554p | +27p |
| 5. USD 850m one-off restructuring cash deducted | Claude's review (Codex missed it) | 1,524p | -30p |
| 6. Minority interests valued proportionately (2.57% of EV = USD 1,500m, was book USD 2,083m incl. a double-counted EABL minority) | **Your decision** after the evidence audit | 1,545p | +20p |

## Key numbers to check against your Excel model (USD m unless stated)
| Item | Value | Source / note |
|---|---|---|
| Base net sales FY26, ex-EABL | 18,505.5 | unchanged |
| Base operating margin before exceptionals | 29.36% | unchanged |
| Tax rate | 24.3% | 20-F p.22 |
| D&A / capex (forecast) / NWC, % of sales | 3.38% / 7.11% / 37.58% | unchanged |
| **Terminal capex, % of sales** | **6.21%** | = D&A + (2% / 13.4% x NOPAT - NWC increase) / sales |
| **Savings flow-through** | **46%** | brief |
| WACC (Rf 5.22%, beta 0.96, ERP 5%, Ke 10.02%, Kd 6.22% pre-tax, debt weight 29.4%) | 8.46% | unchanged |
| FCF FY27 / FY28 / FY29 / FY30 / FY31 (full years, all counted now) | 3,554.0 / 3,704.8 / 3,732.6 / 3,798.8 / 3,902.3 | discounted from 30 June 2026 |
| Terminal-year FCF (FY32, steady state) | 4,241.2 | NOPAT 4,985.3 + D&A 703.6 - capex 1,294.1 - NWC 153.5 |
| Enterprise value at 30 June 2026 | 58,448 | terminal value is 74.9% of it |
| less net debt / minorities / restructuring cash | 20,482 / 1,500 / 850 | 20-F; minorities = 2.566% (minorities' share of operating profit ex-EABL, 20-F p.210, p.164) x EV; 6-K 6 Aug 2026 |
| plus associates / disposal proceeds | 5,284 / 3,318 | unchanged |
| Equity value at 30 June 2026 | 44,219 | |
| Equity value at 12 Oct 2026 | 45,427 | x (1 + 10.02%)^0.2822; no dividend ex in between (final dividend ex 15 Oct) |
| Shares / FX | 2,222m / USD 1.3234 per GBP | |
| **Value per share** | **USD 20.44 = 1,545p** | |
| Upside / rating | -7.7% / HOLD | |

## Phase 3 checklist
- **Codex maths audit: done.** It found 3 issues, all real: the terminal steady state (already fixed), the old Risk script overwriting your beta (fixed), and the net debt date (fixed). Codex's independent rebuild gave 1,447.59p vs our 1,448p.
- **Decision 1, terminal capex: ROIC 13.4%** (evidence: terminal-capex-evidence.md).
- **Decision 2, flow-through: 46%** (evidence: savings-flow-through-evidence.md).
- **Tidy-ups:** net debt date fixed (no dividend to deduct: ex-date 15 Oct is after the valuation date); restructuring cash added; comps now 4 of 4 peers (P/E only, two from press reports; median 18.5x implies 2,311p, so treat it as a weak cross-check).
- **Evidence audit of every input (your condition for merging):** one failure, minority interests at book; fixed with your decision (proportionate).
- **Mistakes log:** rows 9 to 14 added.
- **Tests:** 38 pass (stand-in runner, since pytest can't be installed here; the Excel-vs-Python check runs in LibreOffice).

## Still open (not blocking)
Peer EV/EBITDA, Constellation EPS, Moet Hennessy at fair value, and restructuring tax relief (up to +7p). USL's minority at market price is shown as a Bear challenge (1,395p, an upper bound).
