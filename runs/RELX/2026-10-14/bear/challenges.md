# Bear case: RELX PLC (RELX / REL.L), run 2026-10-14

Price **2,771p** (REL.L close 13 Oct 2026). Base case **1,621p, SELL (-41.5%)**, WACC 9.60%. Engine bear (growth 3%, WACC +1 point) **1,244p**.
HOLD starts at **2,494p** (-10%); BUY at 3,187p (+15%). Money in GBP m; values per share in pence (GBp). RELX reports in pounds, so no exchange rate is used.

**How each impact was measured.** `bear/run_bear.py` copies `briefs/RELX.yaml` and `inputs.yaml` into `bear/scratch/<test>/`, changes one assumption (or a stated stack), and runs `python -m desk.valuation_run` on the copy.
- An unchanged copy reproduces the Valuation agent's 1,621.5p and 1,243.9p exactly; the script asserts this.
- All results are in `bear/bear_results.json`.
- The brief and `inputs.yaml` were not changed.

The base case is already a SELL. So this file answers two questions, with the same rigour on each side:
- **Part A:** how far below the price the value could go.
- **Part B:** whether any sourced input breaks the SELL.

---

# Part A: the case against buying

## 1. The bear margin is milder than its label (Fundamentals agent FLAG 1; PM decision 3; mistakes log row 26)
**Claim.** The brief's bear margin, 33.1%, is labelled the "FY23 level". But that is the FY23 **group** margin, which includes print. The base margin of 35.0% **excludes** print. On the same basis as the base, FY23 was **32.4%**. So the agreed bear understates the stress by 0.7 points.

**Evidence.**
- FY23 adjusted OP 3,030 on revenue 9,161 (AR25 p.186).
- RELX's own restatement gives FY23 print as revenue 586 and adjusted OP 253 (AR25 note 1 p.145).
- So FY23 without print = (3,030 - 253) / (9,161 - 586) = **32.38%** (computed in `run_bear.py`).
- Print earns about 43-50% margins and is being run off: 46% in FY25, 50% in H1 2026 (margin evidence file).

| Test (one change) | Value | Impact | Rating |
|---|---|---|---|
| Margin 33.1% (brief, as labelled) | 1,498p | **-124p** | SELL |
| Margin 32.4% (FY23 without print, like-for-like) | 1,451p | **-170p** | SELL |

**Suggested response for the PM:** accept. Replace `bear_agent_margin` 0.331 with 0.324 and label it "FY23 without print (AR25 p.145)". Or keep 0.331 but relabel it "FY23 group incl. print, a milder stress". *Accept / reject: ____*

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

| Test | Value | Impact | Rating |
|---|---|---|---|
| Growth 3.0% every year (WACC unchanged) | 1,476p | **-146p** | SELL |
| Terminal growth 1.5% | 1,573p | **-49p** | SELL |
| **AI case:** growth 3% + margin 32.4% + terminal growth 1.5%, base WACC | 1,274p | **-347p** | SELL (-54.0%) |

**Suggested response for the PM:** accept the AI case as the scenario to show in the memo, labelled a stress test. The counter-evidence (Legal +10%) should sit next to it. *Accept / reject: ____*

## 3. Reinvestment is under-charged: RONIC, acquisitions and tax (Valuation agent; PM decisions 4, 9, 10)
**Claim.** The DCF credits RELX with organic-looking growth but charges no acquisitions. It also assumes new capital earns 15.4% forever, and the tax rate (22.8%) sits below RELX's own statutory mix (25.0%).

**Evidence.**
- **Acquisitions are a recurring cash cost.** RELX spent 254, 394, 124, 170 and 260 on acquisitions in FY21-25 (SEC XBRL `CashFlowsUsedInObtainingControlOfSubsidiariesOrOtherBusinesses...`, 20-F accessions in `run_bear.py`; extract in `scratch/downloads/acquisitions_xbrl.json`).
  - That is **2.73%** of revenue pooled, or 2.80% as a simple average. The brief's 2.7% is confirmed (the pooled ratio).
  - In FY25 acquisitions added only £14m of revenue in their first year (AR25 p.199) against £260m spent. The cash goes out, but the growth credited to it is small and appears later inside "underlying".
  - The test charges acquisitions as extra capex in FY26-30 only. Terminal reinvestment comes from RONIC, and RELX's 15.4% ROIC already counts acquisitions at cost, so adding them forever would double count.
- **RONIC.** RELX's ROIC has risen from 11.9% to 15.4% (AR25 p.186), but it was 11.9-12.5% only four years ago. If new money earns only the cost of capital, growth adds no value.
- **Tax.**
  - The weighted statutory rate is 25.0% for FY25 and 24.7% for H1 2026 (AR25 p.159; H1 2026 note 7).
  - The adjusted rate was lifted in FY21 and FY23 by one-off credits from old tax matters.
  - The reported rate was 24.0% in FY24 and 24.4% in FY25.

| Test | Value | Impact | Rating |
|---|---|---|---|
| Terminal RONIC = WACC (9.60%) | 1,481p | **-140p** | SELL |
| Acquisitions 2.7% of revenue, FY26-30 | 1,549p | **-73p** | SELL |
| Tax 25.0% | 1,561p | **-60p** | SELL |

**Suggested response for the PM:**
- Accept acquisitions and tax as bear lines, as agreed.
- On RONIC = WACC: accept as a stress test only. RELX's ROIC has risen for five years, so a RONIC of 9.6% is harsh.

*Accept / reject: ____*

## 4. Risk: the discount rate, leverage and the price path (Risk agent; Data agent FLAGs 2 and 5)
**Claim.** The stock now behaves like a much riskier asset than its single-A credit suggests. On Damodaran's longer history, the industry beta is higher than the one used. Leverage is rising to fund buybacks.

**Evidence.**
- **Volatility and drawdown** (`risk/risk.json`):
  - 1-year volatility **36.0%**, three times the FTSE 100 (11.6%).
  - Max drawdown **-51.3%** over five years, against -13.4% for the FTSE 100.
  - The price is still 33% below its Feb 2025 peak.
  - Beta does not capture this (it is stock-specific), so it does not move the DCF. But it is a **price** risk for a holder. A 1-standard-deviation fall over one year would take the price to **1,774p**, and a repeat of the last drawdown to **1,349p** (price arithmetic in `run_bear.py`, not a DCF value).
- **Beta.** Damodaran's 2020-24 average unlevered beta for Information Services (1.0729, cash-corrected) relevers to **1.195** (risk/notes.md).
- **Leverage after buybacks.**
  - The 2026 buyback (£2,250m) is about 97% of FY25 free cash flow before dividends (relx-facts.md section 8).
  - Net debt/EBITDA rose from 1.8x (FY24) to 2.0x (FY25) and **2.3x** at June 2026 (H1 2026 p.12).
  - Fitch rates RELX **BBB+** (FWP 24 Mar 2025).
- **The gilt** (5.45%) comes from aggregators only (Data FLAG 2). It cuts both ways (see Part B).

| Test | Value | Impact | Rating |
|---|---|---|---|
| Engine bear: growth 3% + WACC +1 point | 1,244p | **-378p** | SELL |
| Beta 1.195 (Damodaran 5-year average, relevered) | 1,390p | **-231p** | SELL |
| Cost of debt at the BBB spread, 1.03% (FRED BAMLC0A4CBBB, 13 Oct) | 1,612p | **-9p** | SELL |
| Leverage at June 2026: beta 0.994 and debt weight 15.1% | 1,634p | **+12.5p** | SELL |
| June 2026 leverage + BBB spread | 1,623p | +1.5p | SELL |

**Honest note on leverage.** In this WACC framework, more debt slightly *raises* the value: more weight on cheap after-tax debt outweighs the higher beta. The leverage risk is real (a downgrade, refinancing at 6%+), but the engine cannot show it as a loss. It belongs in the memo's risk section, not in the value.

**Suggested response for the PM:**
- Show the volatility and drawdown in the memo as a position-sizing risk.
- Keep beta 0.973 for the base. The 1.195 figure is a bear sensitivity only.
- The BBB spread is immaterial (-9p).

*Accept / reject: ____*

## 5. Stacked bear
Engine bear (growth 3%, WACC +1 point), plus margin 32.4%, tax 25%, terminal growth 1.5%, RONIC = the stacked WACC (10.62%), acquisitions 2.7% and the BBB spread:

| Stack | Value | Impact vs base | Upside | Rating |
|---|---|---|---|---|
| **Full stack, margin 32.4% (like-for-like)** | **902p** | **-720p** | -67.5% | SELL |
| Full stack, margin 33.1% (brief label) | 938p | -684p | -66.2% | SELL |
| Stack without the +1 point WACC shift (WACC 9.62%) | 1,065p | -556p | -61.6% | SELL |

The stack is an extreme, all-at-once case. Each line is sourced; together they assume AI hurts growth, margin, pricing power and returns at the same time.

---

# Part B: challenges AGAINST the SELL (same rigour)

The SELL rests almost entirely on the discount rate. The Valuation agent's flip points show this:
- **Inputs that cannot realistically flip the call:**
  - margin would need 48.4%;
  - FY27-30 growth would need 15.2% a year;
  - terminal growth would need 6.1%.
- **Inputs that could:**
  - the gilt at 3.11%;
  - beta at 0.449;
  - the WACC at 7.41%.

## B1. The market-implied WACC is 6.95%, against the 9.60% used (Valuation agent)
**Evidence.** On these cash flows the 2,771p price implies a 6.95% WACC (`valuation/notes.md`). At a 5.45% gilt and 5% ERP, that needs a beta of **0.365** (`desk.dcf.wacc` solved in `run_bear.py`). That is almost exactly RELX's own 5-year monthly regression beta (0.38). So the market is pricing RELX as a low-beta bond-like compounder; the desk is pricing it as an average-risk information-services firm.
**Impact:** see B3: beta 0.38 gives **2,673p (HOLD)**.
**Bear's reading:** the market-implied figure is not evidence. It is the price restated as a rate. The 0.38 regression has an R-squared of 0.04 and a 95% range of -0.08 to 0.84.
**Suggested response:** reject as an input; show it in the memo as "what the price assumes". *Accept / reject: ____*

## B2. Is 2.0% terminal growth consistent with a 5.45% gilt? (Fisher equation)
**Evidence.** Fisher: (1 + nominal) = (1 + real) x (1 + inflation).
- The base case pairs a 5.45% gilt with 2.0% perpetual inflation. That implies a **3.38% real** risk-free rate forever.
- The US 10-year TIPS real yield is **2.88%**, and Fisher on the US nominal yield (5.21%) and breakeven (2.33%) gives **2.81%** (FRED DFII10, DGS10, T10YIE, 13 Oct 2026; downloads in `scratch/downloads/`).
- If UK real rates equal US real rates, the gilt embeds about **2.50%** UK inflation, not 2.0%. Equivalently, a gilt consistent with 2.0% inflation would be **4.94%**.
- **The UK breakeven is MISSING.** The Bank of England and DMO sites are blocked (proxy 403), and FRED has no UK breakeven series. "UK real = US real" is an **assumption**, not a source.

| Test | Value | Impact | Rating |
|---|---|---|---|
| Terminal growth 2.33% (US 10y breakeven, FRED T10YIE 13 Oct; the evidence file's 2.35% is the 14 Oct reading) | 1,657p | **+36p** | SELL |
| Terminal growth 2.50% (gilt-implied inflation, assuming UK real = US TIPS real) | 1,677p | **+55p** | SELL |
| Risk-free 4.94% (US TIPS real 2.88% + 2.0% inflation) | 1,765p | **+144p** | SELL |

**Reading:** the inconsistency is real. The fix most consistent with the evidence is to lift terminal growth to about 2.3-2.5%, which is worth **+36p to +55p**. Fixing it through the rate instead is worth up to +144p. Neither reaches HOLD.
**Suggested response:** consider terminal growth 2.35% (evidence option B) as the consistent pair to a market gilt. Rating unchanged. *Accept / reject: ____*

## B3. Beta 0.973 vs own regressions (0.38-0.67) and the peer median (0.75) (Risk agent FLAG 1)
| Test | Value | Impact | Rating |
|---|---|---|---|
| Peer median 0.75 (raw, 7 core peers, `risk/risk.json`) | 1,918p | **+296p** | SELL |
| Own 5-year weekly 0.66 (R-squared 0.12) | 2,067p | **+445p** | SELL |
| Blume-adjusted 5-year monthly 0.58 | 2,207p | **+585p** | SELL |
| **Own 5-year monthly 0.38 (R-squared 0.04)** | **2,673p** | **+1,051p** | **HOLD (-3.5%)** |

**Evidence for a lower beta.**
- The bottom-up 0.97 is outside the 95% range of the 5-year weekly regression (0.45-0.87).
- The FTSE 100 is a poor proxy for a business with 58% North American revenue. That argues for *ignoring* FTSE regressions, though, not for *using* them.
- Peer betas are raw and measured against different indices.

**Bear's reading:** the desk rejected own regressions for Unilever (0.54) for the same low R-squared. Using 0.38 for RELX would break that rule for the one input that flips the call.
**Suggested response:** keep the bottom-up beta. Show 0.66-0.75 as the realistic low range, worth +296p to +445p, still SELL. *Accept / reject: ____*

## B4. The implied exit multiple of 7.9x is below every peer (11.1x-20.7x) (Valuation agent FLAG 2)
**Evidence.**
- The DCF's terminal value is 7.9x FY30 EBITDA. RELX trades at 14.6x today, and the cheapest peer (Wolters Kluwer) at 11.1x.
- At the 9.60% WACC, terminal growth would have to be **5.46%** forever to reach 11.1x. Even that gives only **2,256p (SELL, -18.6%)**.

| Test | Value | Impact | Rating |
|---|---|---|---|
| Terminal RONIC 25.1% (book ROIC, evidence option B) | 1,711p | **+90p** | SELL |
| Terminal growth 5.46% (the 11.1x exit; diagnostic, not sourced) | 2,256p | +634p | SELL |

**Reading:** the low multiple is a *symptom* of the 9.6% WACC, not a separate error. No sourced terminal assumption closes the gap.
**Suggested response:** show it in the memo as the clearest sign that the DCF and the market disagree on the discount rate. Do not change terminal inputs to hit a multiple. *Accept / reject: ____*

## B5. A flat 35.0% margin vs a record of rising margins and management's guidance (Valuation agent; Fundamentals FLAG 3)
**Evidence.**
- The adjusted margin rose every year: 30.5%, 31.4%, 33.1%, 33.9%, 34.8%, and 35.5% in H1 2026 (AR25 p.186; H1 2026 p.1).
- Every segment's FY26 outlook says profit growth will exceed revenue growth (H1 2026 p.5-8). There is no number.

| Test | Value | Impact | Rating |
|---|---|---|---|
| Margin 35.5% (H1 2026 group incl. print, evidence option C) | 1,654p | **+33p** | SELL |
| Margin 38.6% from FY26 (35.0% + 0.9 pt x 4 years; **judgement**, overstates because it applies from year 1) | 1,856p | +234p | SELL |

HOLD would need a 48.4% margin.
**Suggested response:** keep 35.0% flat (the engine cannot phase a margin rise, and there is no numeric guidance). Note in the memo that this is cautious by about +33p to +234p. *Accept / reject: ____*

## B6. 5% growth vs 7% underlying (Data agent cross-check; Fundamentals FLAG 3)
**Evidence.**
- Underlying growth has been 7-9% every year since FY21.
- Thomson Reuters guides about 8% organic for 2026 (6-K 0001193125-26-333835).
- But the 7% figure leaves out print run-off (-£109m in FY25), disposals (-£91m) and exhibition cycling (AR25 p.199). So 7% overstates the revenue the DCF values.

| Test | Value | Impact | Rating |
|---|---|---|---|
| Growth 7% for FY27-30 (evidence option C) | 1,775p | **+154p** | SELL |

**Suggested response:** keep 5.0%. Print is about 3% of revenue and shrinking, so the gap will narrow, but not to zero while disposals continue. *Accept / reject: ____*

## B7. Comps value 2,990p (Valuation agent)
**Evidence.** The peer-median EV/EBITDA of 15.7x gives **2,990p**, which is +7.9% vs the price: **HOLD** territory (`valuation/comps.json`; range 1,955-4,111p).
**Bear's reading:**
- The peers (TRI, WKL, LSEG, EXPN) suffered the same AI de-rating in February 2026, so comps show RELX is not expensive *relative* to an AI-exposed sector. They do not show the sector is cheap.
- Four of the seven peers are Yahoo-only data.

**Suggested response:** report comps as the main counterweight in the memo. The desk rates on the DCF. *Accept / reject: ____*

## B8. Other risk-free readings (Data FLAG 2)
| Test | Value | Impact | Rating |
|---|---|---|---|
| Gilt 5.39% (Bloomberg, early 13 Oct) | 1,637p | +16p | SELL |
| Gilt 4.99% (FRED August average; stale, rejected under Unilever decision 11) | 1,750p | +128p | SELL |

## Stacked generous case
| Stack | Value | Impact | Upside | Rating |
|---|---|---|---|---|
| Beta 0.75 (peer median) + gilt 4.99% (stale) + terminal growth 2.33% + RONIC 25.1% + margin 35.5% + growth 7% | **2,548p** | +926p | -8.1% | **HOLD** |
| Same, beta 0.66 (own 5-year weekly) | 2,765p | +1,143p | -0.2% | HOLD |
| Same, beta 0.38 (own 5-year monthly) | 3,689p | +2,068p | +33.1% | BUY |
| Same, beta kept at 0.973 | 2,127p | +505p | -23.2% | SELL |
| **Gilt kept at 5.45%** (no stale rate): beta 0.75 + g 2.33% + RONIC 25.1% + margin 35.5% + growth 7% | **2,336p** | +714p | -15.7% | **SELL** |
| Gilt 5.45%, growth 5%: beta 0.75 + g 2.33% + RONIC 25.1% + margin 35.5% | 2,142p | +520p | -22.7% | SELL |
| Gilt 5.45%, growth 5%, beta 0.66 | 2,315p | +694p | -16.5% | SELL |

## Does anything reach HOLD (2,494p)?
- **Single sourced input:** only **one**. RELX's own 5-year monthly beta of **0.38** gives 2,673p. It is also the weakest statistic in the file (R-squared 0.04, 95% range -0.08 to 0.84). Every other single input stays SELL. The largest of the rest is beta 0.58 (Blume), at 2,207p.
- **Stacked:** **yes, but only with a lower beta AND the stale August gilt.**
  - Peer-median beta 0.75 + gilt 4.99% + g 2.33% + RONIC 25.1% + margin 35.5% + growth 7% gives 2,548p, just over the HOLD line.
  - Keep the run-date gilt (5.45%) and the same stack is 2,336p, **SELL**.
  - With beta at 0.973, the full generous stack is 2,127p, SELL.
- **Comps:** the comps median (2,990p) is in HOLD territory.
- **Conclusion:** the SELL is robust to every cash-flow and terminal assumption. It is **not** robust to the discount rate. A beta in the 0.66-0.75 range, combined with a lower gilt and generous growth, reaches HOLD. The PM should present the SELL as "SELL on the desk's discount rate", with the beta and gilt flip points beside it.

---

# Management track record: guidance vs outcomes
RELX gives only **qualitative** guidance, so it is hard to miss. Outlook statements are quoted from each February results release (SEC 6-K ex 99.1; text extracts in `scratch/downloads/`). Outcomes come from the next year's release and AR25 p.186.

| Guidance given in | For | What RELX said | Outcome: underlying revenue / adj. OP growth | Met? |
|---|---|---|---|---|
| FY21 results (0001564590-22-004516) | 2022 | growth "to remain above historical trends" | +9% / +15% | Yes |
| FY22 results (0000929869-23-000048) | 2023 | "remain above historical trends" | +8% / +13% | Yes |
| FY23 results (0000929869-24-000016) | 2024 | "another year of strong underlying growth" | +7% / +10% | Yes |
| FY24 results (0000929869-25-000010) | 2025 | "another year of strong underlying growth" | +7% / +9% | Yes |
| FY25 results (0000929869-26-000008) | 2026 | "another year of strong underlying growth" (reaffirmed H1 2026) | H1 2026: +7% / +9% | On track |

**What this means.**
- **For the bull:** management has met its outlook every year, and the margin rose every year (+0.9, +1.7, +0.8, +0.9 points, FY22-25).
- **For the bear:**
  - The wording was **downgraded** after 2023, from "above historical trends" to "strong".
  - Underlying profit growth has **slowed each year**: +15%, +13%, +10%, +9%, +9%.
- **Capital allocation:** the 2025 buyback (£1,500m) was done at an average **3,797p**. Today's price is 27% lower, so that buyback is worth about a quarter less than RELX paid. The H1 2026 buyback averaged 2,529p (FY25 results p.14; H1 2026 p.12).
- **The guidance gives no number to hold management to on margin, tax or capex.**

---

Strongest reason not to buy: at 2,771p the price only works if RELX's cost of capital is about 7% (a beta near 0.37 at today's 5.45% gilt), which is a bet that AI will never dent Legal and STM pricing, the same risk RELX now names in its own principal risks and that cut the shares 51% peak to trough. On the desk's discount rate the value is 1,621p, and only the weakest beta statistic in the file (0.38, R-squared 0.04) reaches HOLD on its own.
