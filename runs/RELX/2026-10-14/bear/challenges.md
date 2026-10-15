# Bear case: RELX PLC (RELX / REL.L), run 2026-10-14, re-run 15 Oct 2026 (evidence audit)

> **Re-run 15 Oct 2026 (evidence audit, `docs/audit-2026-10-15/RELX.md`).** Two brief changes, both made by the PM:
> - **equity risk premium 4.2%** (Damodaran implied, PM decision 15 Oct 2026; was 5.0% with no source);
> - **bear margin 32.4%** (`bear_agent_margin`, PM bear responses, decision 14, 15 Oct 2026; was 33.1%).
>
> Every value in this file is new and comes from re-running `desk.valuation_run` on a scratch copy. The "14 Oct" column shows the old value at ERP 5.0%; the 14 Oct results file is kept in `bear/scratch/bear_results_erp5_2026-10-14.json`. Check: the scratch run at ERP 5.0% reproduces the old base (1,621.5p) and the old full stack (901.7p) exactly.

Price **2,771p** (REL.L close 13 Oct 2026). Base case **1,821p, SELL (-34.3%)**, WACC 8.92% (was 1,621p, -41.5%, WACC 9.60%). Engine bear (growth 3%, WACC +1 point, 9.92%) **1,386p (-50.0%)** (was 1,244p).
HOLD starts at **2,494p** (-10%); BUY at 3,187p (+15%). Money in GBP m; values per share in pence (GBp). RELX reports in pounds, so no exchange rate is used.

**How each impact was measured.** `bear/run_bear.py` copies `briefs/RELX.yaml` and `inputs.yaml` into `bear/scratch/<test>/`, changes one assumption (or a stated stack), and runs `python -m desk.valuation_run` on the copy.
- An unchanged copy reproduces the Valuation agent's 1,821.3p and 1,386.3p exactly; the script asserts this.
- All results are in `bear/bear_results.json`.
- The brief and `inputs.yaml` were not changed.

The base case is already a SELL. So this file answers two questions, with the same rigour on each side:
- **Part A:** how far below the price the value could go.
- **Part B:** whether any sourced input breaks the SELL.

---

# Part A: the case against buying

## 1. The bear margin: now 32.4%, like-for-like (Fundamentals agent FLAG 1; PM decision 14; mistakes log row 26)
**Claim (resolved).** The old bear margin, 33.1%, was the FY23 **group** margin including print, while the 35.0% base **excludes** print. On the same basis, FY23 was **32.4%**. The PM accepted this on 15 Oct 2026, and the brief's `bear_agent_margin` is now 0.324.

**Evidence.**
- FY23 adjusted OP 3,030 on revenue 9,161 (AR25 p.186).
- RELX's own restatement gives FY23 print as revenue 586 and adjusted OP 253 (AR25 note 1 p.145).
- So FY23 without print = (3,030 - 253) / (9,161 - 586) = **32.38%** (computed in `run_bear.py`, which asserts the brief's 0.324 matches).
- Print earns about 43-50% margins and is being run off: 46% in FY25, 50% in H1 2026 (margin evidence file).

| Test (one change) | Value, 15 Oct (ERP 4.2%) | Impact | Rating | 14 Oct (ERP 5.0%) |
|---|---|---|---|---|
| **Margin 32.4% (brief bear margin, FY23 without print)** | **1,636p** | **-185p** | SELL | 1,451p (-170p) |
| Margin 33.1% (old label, FY23 group incl. print) | 1,687p | -134p | SELL | 1,498p (-124p) |

## 2. AI disruption of Legal and STM: growth, pricing and the terminal rate (PM decisions 1-3; Data agent's growth cross-check)
**Claim.** About half of RELX's revenue is exposed to generative AI. STM and Legal are 49% of FY25 revenue without print. The bear case is not "AI kills RELX". It is that AI caps price rises in those two segments. Three things follow:
- growth falls back to about 3%;
- the margin gives back the FY23-25 gains;
- pricing power fades in perpetuity.

**Evidence (for).**
- **RELX's own risk wording got stronger in 2026.**
  - The demand risk now names "advances in artificial intelligence, workflow tools" and the need to "effectively integrate evolving technologies" (H1 2026 results p.15).
  - The IP risk says: "proprietary rights and copyright protections could be infringed or circumvented, including by companies leveraging technology tools and AI, **which may impact demand for and pricing of our products and services**" (H1 2026 p.15; FY25 results p.16).
  - Large language model providers are now a named supply-chain dependency (H1 2026 p.16).
- **The market has priced this risk once already.**
  - -14.4% on 3 Feb 2026, the day after an AI legal tool was launched (`risk/risk.json`; press reports in relx-facts.md section 8). Peers Wolters Kluwer, Thomson Reuters and LSEG also fell.
  - Max drawdown -51.3% (4,133p in Feb 2025 to 2,012p in Feb 2026).
- **The brief's 3% bear growth matches the segment arithmetic.**
  - Halving STM growth (+6% to 3%) and Legal growth (+10% to 5%), from H1 2026 underlying growth (H1 2026 p.3), cuts revenue-weighted underlying growth from 7.54% to 5.68%. That is a **1.87-point drag** (FY25 segment revenue weights, FY25 results p.26; computed in `run_bear.py`).
  - Taking that off the agreed 5.0% gives **3.1%**, which is consistent with the brief's 3.0%.
- **Profit growth has slowed every year** (see "Management track record" below): underlying adjusted OP growth was +15%, +13%, +10%, +9% and +9% (FY22 to H1 2026).

**Evidence (against, stated honestly).**
- Legal growth is **accelerating**: +9% (FY25), then +10% in H1 2026, with "double-digit growth" in Law Firms & Corporate Legal from Lexis+ with Protégé (H1 2026 p.7).
- STM "stepped up" to +6%.
- The Legal margin rose from 20.9% to 21.7%.
- So far, AI is a tailwind in RELX's reported numbers. This case is a stress test, not a forecast.

| Test | Value, 15 Oct (ERP 4.2%) | Impact | Rating | 14 Oct (ERP 5.0%) |
|---|---|---|---|---|
| Growth 3.0% every year (WACC unchanged) | 1,661p | **-160p** | SELL | 1,476p (-146p) |
| Terminal growth 1.5% | 1,756p | **-65p** | SELL | 1,573p (-49p) |
| **AI case:** growth 3% + margin 32.4% + terminal growth 1.5%, base WACC 8.92% | **1,432p** | **-389p** | SELL (-48.3%) | 1,274p (-347p) |

The lower discount rate makes every cash-flow and terminal line **bigger** in pence: distant cash flows are now worth more, so losing them costs more.

## 3. Reinvestment is under-charged: RONIC, acquisitions and tax (Valuation agent; PM decisions 4, 9, 10)
**Claim.** The DCF credits RELX with organic-looking growth but charges no acquisitions. It also assumes new capital earns 15.4% forever, and the tax rate (22.8%) sits below RELX's own statutory mix (25.0%).

**Evidence.**
- **Acquisitions are a recurring cash cost.** RELX spent 254, 394, 124, 170 and 260 (GBP m) on acquisitions in FY21-25 (SEC XBRL `CashFlowsUsedInObtainingControlOfSubsidiariesOrOtherBusinesses...`, 20-F accessions in `run_bear.py`; extract in `scratch/downloads/acquisitions_xbrl.json`).
  - That is **2.73%** of revenue pooled, or 2.80% as a simple average. The brief's 2.7% is confirmed (the pooled ratio).
  - In FY25 acquisitions added only GBP 14m of revenue in their first year (AR25 p.199) against GBP 260m spent.
  - The test charges acquisitions as extra capex in FY26-30 only. Terminal reinvestment comes from RONIC, and RELX's 15.4% ROIC already counts acquisitions at cost, so adding them forever would double count.
- **RONIC.** RELX's ROIC has risen from 11.9% to 15.4% (AR25 p.186), but it was 11.9-12.5% only four years ago. If new money earns only the cost of capital, growth adds no value. **At the lower 8.92% WACC this line is bigger than before**: the spread between 15.4% and the WACC is wider, so taking it away costs more.
- **Tax.** The weighted statutory rate is 25.0% for FY25 and 24.7% for H1 2026 (AR25 p.159; H1 2026 note 7). The reported rate was 24.0% in FY24 and 24.4% in FY25.

| Test | Value, 15 Oct (ERP 4.2%) | Impact | Rating | 14 Oct (ERP 5.0%) |
|---|---|---|---|---|
| Terminal RONIC = WACC (8.92%) | 1,632p | **-189p** | SELL | 1,481p (-140p, at 9.60%) |
| Acquisitions 2.7% of revenue, FY26-30 | 1,748p | **-73p** | SELL | 1,549p (-73p) |
| Tax 25.0% | 1,757p | **-65p** | SELL | 1,561p (-60p) |

## 4. The discount rate itself: the 4.2% ERP, the gilt, beta and leverage (Valuation agent / PM decision 15 Oct; Risk agent; Data agent FLAGs 2 and 5)
**Claim.** The audit replaced one unsourced number (ERP 5.0%) with the **lowest** of the sourced ERPs on the table. Every other published premium the audit found is higher. The 4.2% implied ERP is a reading of how expensive the US market is today; using it builds part of today's market optimism into the desk's own discount rate. RELX's price has also behaved like a much riskier asset than its credit rating suggests.

**Evidence.**
- **ERP alternatives** (`docs/audit-2026-10-15/erp-evidence.md` sections 2b-2c; all seen secondhand because the sites are blocked):
  - **Kroll recommended US ERP 5.0%** (effective 2 Sep 2025, reaffirmed 2026). Kroll pairs it with the **20-year** US Treasury (5.60% on 13 Oct, FRED DGS20), so used as Kroll intends it would be harsher still. A UK 20-year gilt yield is MISSING (BoE blocked), so I did not run that version.
  - **Fernandez et al. 2025 survey** of the ERP practitioners actually use: US 5.5%, UK 5.4% (SSRN 5260463). Caveat: respondents paired it with a risk-free rate of about 4.1%.
  - The 4.2% itself was seen only in search summaries (Valuation FLAG 4); the PM still has to confirm it on Damodaran's site.
- **Credit spread.** The A spread (0.70%) and the BBB spread (1.03%) are US-dollar indices (FRED BAMLC0A3CA / BAMLC0A4CBBB, 13 Oct 2026; audit M3). Fitch rates RELX **BBB+** (FWP 24 Mar 2025).
- **Volatility and drawdown** (`risk/risk.json`): 1-year volatility **36.0%** vs 11.6% for the FTSE 100; max drawdown **-51.3%** vs -13.4%. A 1-standard-deviation fall over one year would take the price to **1,774p**, a repeat of the last drawdown to **1,349p** (price arithmetic in `run_bear.py`, not a DCF value; unchanged by the ERP).
- **Beta.** Damodaran's 2020-24 average unlevered beta for Information Services (1.0729, cash-corrected) relevers to **1.195** (risk/notes.md).
- **Leverage after buybacks.** Net debt/EBITDA rose from 1.8x (FY24) to 2.0x (FY25) and **2.3x** at June 2026 (H1 2026 p.12). The 2026 buyback (GBP 2,250m) is about 97% of FY25 free cash flow before dividends.

| Test | Value, 15 Oct (ERP 4.2%) | Impact | Rating | 14 Oct (ERP 5.0%) |
|---|---|---|---|---|
| **ERP 5.0% (Kroll US; the old desk figure)** | **1,621p** | **-200p** | SELL (-41.5%) | (was the base) |
| **ERP 5.5% (Fernandez 2025 survey, US)** | **1,514p** | **-308p** | SELL (-45.4%) | 1,514p (audit table) |
| ERP 5.0% + BBB spread 1.03% | 1,612p | -209p | SELL | n/a |
| Cost of debt at the BBB spread, 1.03% (FRED BAMLC0A4CBBB, 13 Oct) | 1,810p | **-11p** | SELL | 1,612p (-9p) |
| Engine bear: growth 3% + WACC +1 point (9.92%) | 1,386p | **-435p** | SELL (-50.0%) | 1,244p (-378p) |
| Beta 1.195 (Damodaran 5-year average, relevered) | 1,586p | **-235p** | SELL | 1,390p (-231p) |
| Leverage at June 2026: beta 0.994 and debt weight 15.1% | 1,835p | **+13p** | SELL | 1,634p (+12.5p) |
| June 2026 leverage + BBB spread | 1,822p | +0.2p | SELL | 1,623p (+1.5p) |

**Honest note on leverage.** In this WACC framework, more debt slightly *raises* the value: more weight on cheap after-tax debt outweighs the higher beta. The leverage risk is real (a downgrade, refinancing at 6%+), but the engine cannot show it as a loss. It belongs in the memo's risk section, not in the value.

**Bear's reading.** The PM's choice is defensible (the implied ERP is the only measure built to sit on today's bond yields). But it is the most generous of the sourced premiums, and it moved the value by +200p with no change to RELX's business. The SELL survives every ERP in the evidence pack (4.2% to 5.5% gives 1,821p to 1,514p).

## 5. Stacked bear
Engine bear (growth 3%, WACC +1 point), plus margin 32.4%, tax 25%, terminal growth 1.5%, RONIC = the stacked WACC, acquisitions 2.7% and the BBB spread:

| Stack | Value, 15 Oct | Impact vs base 1,821p | Upside | Rating | 14 Oct (ERP 5.0%) |
|---|---|---|---|---|---|
| **Full stack, margin 32.4%, ERP 4.2% (stacked WACC 9.94%)** | **1,002p** | **-819p** | -63.8% | SELL | 902p (-720p, WACC 10.62%) |
| Full stack, margin 33.1% (old label) | 1,040p | -781p | -62.5% | SELL | 938p |
| Full stack at ERP 5.0% (Kroll; WACC 10.62%) | 902p | -920p | -67.5% | SELL | (same: reproduces 901.7p) |
| Full stack at ERP 5.5% (Fernandez; WACC 11.04%) | 845p | -976p | -69.5% | SELL | n/a |
| Stack without the +1 point WACC shift (WACC 8.94%) | 1,189p | -632p | -57.1% | SELL | 1,065p |

The stack is an extreme, all-at-once case. Each line is sourced; together they assume AI hurts growth, margin, pricing power and returns at the same time.

---

# Part B: challenges AGAINST the SELL (same rigour)

The SELL rests almost entirely on the discount rate. The Valuation agent's new flip points (`valuation/sanity_checks.json`) show this:
- **Inputs that cannot realistically flip the call:** margin would need 44.5% (was 48.4%); FY27-30 growth 12.4% a year (was 15.2%); terminal growth 4.89% (was 6.08%).
- **Inputs that could:** the gilt at **3.80%** (was 3.11%); beta at **0.535** (was 0.449); the WACC at **7.38%** (was 7.41%); the ERP at **2.31%** (unchanged).

## B1. The market-implied WACC is 6.93%, against the 8.92% used (Valuation agent)
**Evidence.** On these cash flows the 2,771p price implies a 6.93% WACC (was 6.95%). At a 5.45% gilt and the 4.2% ERP, that needs a beta of **0.429** (was 0.365 at ERP 5.0%; `desk.dcf.wacc` solved in `run_bear.py`). That is below every core peer (lowest: Wolters Kluwer 0.58) and just below the bottom of the 95% range of RELX's own 5-year weekly regression (0.446).
**Impact:** see B3: beta 0.38 gives **2,844p (HOLD)**.
**Bear's reading:** the market-implied figure is not evidence. It is the price restated as a rate.

## B2. Is 2.0% terminal growth consistent with a 5.45% gilt? (Fisher equation)
**Evidence.** Fisher: (1 + nominal) = (1 + real) x (1 + inflation).
- The base case pairs a 5.45% gilt with 2.0% perpetual inflation, which implies a **3.38% real** risk-free rate forever.
- The US 10-year TIPS real yield is **2.88%**; Fisher on the US nominal (5.21%) and breakeven (2.33%) gives **2.81%** (FRED DFII10, DGS10, T10YIE, 13 Oct 2026; downloads in `scratch/downloads/`).
- If UK real rates equal US real rates, the gilt embeds about **2.50%** UK inflation; a gilt consistent with 2.0% inflation would be **4.94%**.
- **The UK breakeven is MISSING** (Bank of England and DMO blocked). "UK real = US real" is an **assumption**.

| Test | Value, 15 Oct | Impact | Rating | 14 Oct (ERP 5.0%) |
|---|---|---|---|---|
| Terminal growth 2.33% (US 10y breakeven, FRED T10YIE 13 Oct) | 1,869p | **+48p** | SELL | 1,657p (+36p) |
| Terminal growth 2.50% (gilt-implied inflation, assuming UK real = US TIPS real) | 1,896p | **+75p** | SELL | 1,677p (+55p) |
| Risk-free 4.94% (US TIPS real 2.88% + 2.0% inflation) | 1,995p | **+174p** | SELL | 1,765p (+144p) |

## B3. Beta 0.973 vs own regressions (0.38-0.67) and the peer median (0.75) (Risk agent FLAG 1)
Betas unrounded from `risk/risk.json` (0.7516, 0.6601, 0.5834, 0.3783); values agree with `valuation/notes.md` (audit finding C5 resolved).

| Test | Value, 15 Oct | Impact | Rating | 14 Oct (ERP 5.0%) |
|---|---|---|---|---|
| Peer median 0.75 (raw, 7 core peers) | 2,117p | **+296p** | SELL (-23.6%) | 1,918p |
| Own 5-year weekly 0.66 (R-squared 0.12) | 2,264p | **+443p** | SELL (-18.3%) | 2,067p |
| Blume-adjusted 5-year monthly 0.58 | 2,400p | **+579p** | SELL (-13.4%) | 2,207p |
| **Own 5-year monthly 0.38 (R-squared 0.04)** | **2,844p** | **+1,022p** | **HOLD (+2.6%)** | 2,673p HOLD |

**Bear's reading:** the beta that flips the call is now 0.535, only 0.05 below the Blume-adjusted 0.58. The gap between "SELL" and "HOLD" on beta is now small. But the desk rejected own regressions for Unilever (0.54) for the same low R-squared, and 0.38 is still the only single beta that crosses.

## B4. The implied exit multiple of 8.6x is below every peer (11.1x-20.7x) (Valuation agent FLAG 1)
- The DCF's terminal value is 8.6x FY30 EBITDA (was 7.9x). RELX trades at 14.6x; the cheapest peer (Wolters Kluwer) at 11.1x.
- At the 8.92% WACC, terminal growth would have to be **4.38%** forever to reach 11.1x (was 5.46%). That gives **2,314p (SELL, -16.5%)**.

| Test | Value, 15 Oct | Impact | Rating | 14 Oct (ERP 5.0%) |
|---|---|---|---|---|
| Terminal RONIC 25.1% (book ROIC, evidence option B) | 1,922p | **+101p** | SELL | 1,711p (+90p) |
| Terminal growth 4.38% (the 11.1x exit; diagnostic, not sourced) | 2,314p | +493p | SELL | 2,256p (at 5.46%) |

## B5. A flat 35.0% margin vs a record of rising margins (Valuation agent; Fundamentals FLAG 3)
- The adjusted margin rose every year: 30.5%, 31.4%, 33.1%, 33.9%, 34.8%, and 35.5% in H1 2026 (AR25 p.186; H1 2026 p.1). No numeric guidance.

| Test | Value, 15 Oct | Impact | Rating | 14 Oct (ERP 5.0%) |
|---|---|---|---|---|
| Margin 35.5% (H1 2026 group incl. print) | 1,857p | **+35p** | SELL | 1,654p (+33p) |
| Margin 38.6% from FY26 (**judgement**, overstates) | 2,076p | +255p | SELL | 1,856p (+234p) |

HOLD would need a 44.5% margin.

## B6. 5% growth vs 7% underlying (Data agent cross-check; Fundamentals FLAG 3)
The 7% leaves out print run-off (-GBP 109m in FY25), disposals (-GBP 91m) and exhibition cycling (AR25 p.199). The audit adds that **no independent industry growth forecast exists** in the run (audit M2).

| Test | Value, 15 Oct | Impact | Rating | 14 Oct (ERP 5.0%) |
|---|---|---|---|---|
| Growth 7% for FY27-30 | 1,990p | **+169p** | SELL | 1,775p (+154p) |

## B7. Comps value 2,990p (Valuation agent; unchanged by the ERP)
Peer-median EV/EBITDA 15.7x gives **2,990p** (+7.9% vs price, HOLD territory; range 1,955-4,111p). The DCF is now 39.1% below it (was 45.8%). The peers fell on the same AI fears in February 2026, so comps are not independent of the risk.

## B8. Other risk-free readings (Data FLAG 2; audit V1)
| Test | Value, 15 Oct | Impact | Rating | 14 Oct (ERP 5.0%) |
|---|---|---|---|---|
| Gilt 5.39% (Bloomberg, early 13 Oct) | 1,840p | +19p | SELL | 1,637p (+16p) |
| **Gilt 5.30% (press, mid-Sep 2026; audit V1)** | **1,870p** | **+48p** | SELL | audit: +40p |
| **Gilt 5.21% (US 10y on 13 Oct, FRED DGS10, as a proxy; audit V1)** | **1,900p** | **+78p** | SELL | audit: +65p |
| Gilt 4.99% (FRED August average; stale, rejected under Unilever decision 11) | 1,977p | +155p | SELL | 1,750p (+128p) |

Each gilt move changes both the cost of equity and the cost of debt. HOLD needs 3.80%.

## Stacked generous case
| Stack | Value, 15 Oct | Impact | Upside | Rating | 14 Oct (ERP 5.0%) |
|---|---|---|---|---|---|
| Beta 0.75 + gilt 4.99% (stale) + terminal growth 2.33% + RONIC 25.1% + margin 35.5% + growth 7% | 2,840p | +1,018p | +2.5% | HOLD | 2,548p HOLD |
| Same, beta 0.66 | 3,058p | +1,237p | +10.4% | HOLD | 2,765p HOLD |
| Same, beta 0.38 | 3,962p | +2,141p | +43.0% | BUY | 3,689p BUY |
| Same, beta kept at 0.973 | 2,409p | +588p | -13.1% | SELL | 2,127p SELL |
| **Gilt kept at 5.45%:** beta 0.75 + g 2.33% + RONIC 25.1% + margin 35.5% + growth 7% | **2,586p** | +765p | -6.7% | **HOLD (new)** | 2,336p SELL |
| Gilt 5.45%, growth 5%: beta 0.75 + g 2.33% + RONIC 25.1% + margin 35.5% | 2,374p | +553p | -14.3% | SELL | 2,142p SELL |
| **Gilt 5.45%, growth 5%, beta 0.66** | **2,546p** | +725p | -8.1% | **HOLD (new)** | 2,315p SELL |

## Does anything reach HOLD (2,494p)?
- **Single sourced input:** still only **one**, beta 0.38 (2,844p; R-squared 0.04). The nearest others: Blume beta 0.58 at 2,400p and the 11.1x-exit diagnostic at 2,314p.
- **Stacked: what changed.** On 14 Oct the generous stack reached HOLD only with the **stale** August gilt. **At ERP 4.2% it reaches HOLD with the run-date 5.45% gilt**, if a lower beta (0.66-0.75) is combined with the other generous lines. With the base beta (0.973) every stack is still SELL (best 2,409p).
- **Conclusion:** the SELL is still robust to every cash-flow and terminal assumption and to every sourced ERP and gilt reading. It now depends on beta more than before: the margin of safety on beta has shrunk from 0.97 vs 0.45 to 0.97 vs 0.535.

---

# PM bear responses (decision 14, agreed 15 Oct 2026), checked against the re-run
The responses are the PM's, quoted from `docs/phase5/relx-bear-responses.md` (written at ERP 5.0%). The last column is the Bear agent's check at ERP 4.2%; the PM's wording is not changed.

| Challenge | PM response (15 Oct 2026, at ERP 5.0%) | Still holds at ERP 4.2%? (new values) |
|---|---|---|
| A1. Bear margin 33.1% includes print | **Accepted: bear margin becomes 32.4%**, the FY23 margin without print. -170p, SELL | Yes. Now in the brief. -185p, 1,636p, SELL |
| A2. AI caps Legal and STM pricing | Accepted as the main risk, not a base change. AI case 1,274p, SELL | Yes. AI case 1,432p (-389p), SELL |
| A3. Reinvestment under-charged | Keep: RONIC 15.4%, acquisitions out, tax 22.8%. SELL either way | Yes. RONIC = WACC -189p, acquisitions -73p, tax -65p; all SELL |
| A4. Discount rate, leverage, price path | Keep the agreed rate (beta 0.973). SELL either way | Yes. Beta 1.195 -235p; new audit lines ERP 5.0% 1,621p and ERP 5.5% 1,514p; all SELL |
| A5. Stacked bear | Noted: 902p, SELL | Now 1,002p (-819p), SELL; 902p is the same stack at ERP 5.0% |
| B1. Market-implied cost of capital 6.95% | Rejected as a basis: needs a beta of 0.365, below every peer and below RELX's own weekly regressions | Yes. Now 6.93%, needs beta 0.429, still below every peer (0.58) and the weekly 95% range (0.446) |
| B2/B8. 2.0% terminal growth vs a 5.45% gilt | Partly accepted: worth +36p to +144p. SELL either way | Yes. Now +48p to +174p; gilt 5.30% / 5.21% +48p / +78p; all SELL |
| B3. Beta 0.973 vs regressions and peers | Keep 0.973. Even 0.75 gives SELL | Yes, 0.75 gives 2,117p SELL. But HOLD now needs 0.535 (was 0.449) |
| B4. Implied exit multiple 7.9x | Noted: a symptom of the discount rate | Now 8.6x; same reading |
| B5. Flat margin vs a rising record | Keep flat. 35.5% gives +33p, SELL | Yes. +35p, SELL |
| B6. 5% growth vs 7% underlying | Keep 5%. 7% gives +154p, SELL | Yes. +169p, SELL |
| B7. Comps 2,990p | Noted as a cross-check | Unchanged 2,990p; DCF now 39.1% below |
| PM view | "SELL on the desk's discount rate ... would reach HOLD if the gilt fell to 3.11%". Conviction: moderate | Rating holds. **The gilt trigger is now 3.80%**, and a generous stack now reaches HOLD at the run-date gilt (see above) |

---

# Management track record: guidance vs outcomes (unchanged by the re-run)
RELX gives only **qualitative** guidance, so it is hard to miss. Outlook statements are quoted from each February results release (SEC 6-K ex 99.1; text extracts in `scratch/downloads/`). Outcomes come from the next year's release and AR25 p.186.

| Guidance given in | For | What RELX said | Outcome: underlying revenue / adj. OP growth | Met? |
|---|---|---|---|---|
| FY21 results (0001564590-22-004516) | 2022 | growth "to remain above historical trends" | +9% / +15% | Yes |
| FY22 results (0000929869-23-000048) | 2023 | "remain above historical trends" | +8% / +13% | Yes |
| FY23 results (0000929869-24-000016) | 2024 | "another year of strong underlying growth" | +7% / +10% | Yes |
| FY24 results (0000929869-25-000010) | 2025 | "another year of strong underlying growth" | +7% / +9% | Yes |
| FY25 results (0000929869-26-000008) | 2026 | "another year of strong underlying growth" (reaffirmed H1 2026) | H1 2026: +7% / +9% | On track |

- **For the bull:** management has met its outlook every year, and the margin rose every year (+0.9, +1.7, +0.8, +0.9 points, FY22-25).
- **For the bear:** the wording was **downgraded** after 2023, from "above historical trends" to "strong"; underlying profit growth has **slowed each year**: +15%, +13%, +10%, +9%, +9%.
- **Capital allocation:** the 2025 buyback (GBP 1,500m) was done at an average **3,797p**; today's price (2,771p) is 27% lower. The H1 2026 buyback averaged 2,529p (FY25 results p.14; H1 2026 p.12).
- **The guidance gives no number to hold management to on margin, tax or capex.**

---

Strongest reason not to buy: at 2,771p the price still needs a cost of capital of about 6.9% (a beta near 0.43 even on the generous 4.2% ERP), which is a bet that AI will never dent Legal and STM pricing, the risk RELX now names in its own principal risks and that cut the shares 51% peak to trough; on the desk's discount rate the value is 1,821p (-34.3%), and at the Kroll or Fernandez premiums it is 1,621p or 1,514p.
