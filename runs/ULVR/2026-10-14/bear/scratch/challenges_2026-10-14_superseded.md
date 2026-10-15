# Bear case: Unilever PLC (ULVR), run 2026-10-14 (re-run on PM decision 11 inputs)

Price **4,710.5p** (ULVR.L close 13 Oct 2026). Base case **3,855p, SELL (-18.2%)**. Engine bear **3,212p**. HOLD starts at 4,239p (-10%), BUY at 5,417p (+15%).
Inputs: risk-free **3.45%** (Bund on the run date, PM decision 11); cost of equity 7.872%; WACC 7.10%; associates EUR 7,061.8m, with the JVs at 3,709.6.
Money in EUR m; values per share in pence (GBp). EUR 1.18190 per GBP; USD 1.1193 per EUR (FRED, 9 Oct 2026); 2,154.3m shares.

**How each impact was measured.** `bear/run_bear.py` copies the current `briefs/ULVR.yaml` and `inputs.yaml` into `bear/scratch/<test>/`. It changes one assumption, plus any input that must move with it (stated below), and runs `python -m desk.valuation_run` on the copy.
- An unchanged copy reproduces the Valuation agent's 3,855.3p and 3,211.9p exactly. The script asserts this against `valuation/valuation.json`.
- Wherever the cost of equity or the growth rate changes, the JVs are re-valued by Gordon growth: 229 x (1 + g) / (Ke - g), the `data/apply_pm_decision10.py` formula.
- Items priced on the run date (the tax, the HUL market value, the McCormick price) are also netted in `priced_at_valuation_date_meur`, so the engine does not grow them.
- All results are in `bear/bear_results.json`. The brief and `inputs.yaml` were not changed.

The base case is already a SELL. The bear case therefore asks two questions: how far below the price the value could go, and whether any sourced test breaks the SELL.

---

## 1. The Foods consideration is worth less than the EUR 33,955m counted (Data agent: `disposal_proceeds`; PM decisions 1 and 5)
**Claim.** The deal at today's price is **1,334p, 35% of the value per share** (Valuation notes (d)). It is counted untaxed and free of market risk.

**Evidence.**
- **Tax is real and unpriced.** Management says synergies "fully offset Unilever's tax and separation costs" (Form 425, 0000217410-26-000027). The CFO said it was "premature to start making estimates" (Form 425 call transcript, 0000217410-26-000032). Only the US leg is "intended to be tax free" (ulvr-tax-evidence.md). Because the McCormick shares are valued at market, the synergies are already in that price; offsetting the tax with them would count them twice.
- **McCormick is moving against the deal.** MKC was USD 65.80 a year ago and is **USD 44.64** now (13 Oct 2026): **-32%** in a year and **-23%** against the USD 57.84 deal reference (brief section 3). Its 1-year annualised volatility is **30.5%** (Yahoo daily closes, `bear/scratch/mkc_1y_yahoo.csv`; `desk.risk.annualised_volatility`). The 499.7m shares are fixed, and closing is expected mid-2027, about 0.71 years away.
- **Timing.** Payment arrives at closing: **-16p** for the cash part at Bund + A spread (4.15%), up to -70p for the whole amount at Ke (Valuation notes (a)).

| Test (one change, engine re-run) | Value | Impact | Rating |
|---|---|---|---|
| **Required test 2:** tax at 25% of the USD 15.7bn cash = **EUR 3,507m** (USD 15,700m / 1.1193 x 25%), priced today | 3,718p | **-138p** | SELL (-21.1%) |
| McCormick 1 s.d. lower by closing: USD 44.64 x (1 - 30.5% x sqrt(0.71)) = **USD 33.15** | 3,654p | **-201p** | SELL (-22.4%) |

**Required test 1: the deal failing is not a bear outcome on our numbers. The value is slightly higher.** The test keeps Foods in the DCF:
- whole-group FY25 sales of EUR 50,503m;
- margin **18.85%** = group underlying 19.97% less the 1.12% FY23-25 restructuring average (the decision 3 rule, ulvr-margin-evidence.md);
- no consideration, and no EUR 500m stranded-cost restructuring;
- minorities at the group ratio of 7.93% (587 / 7,403, Fundamentals notes).

| Deal-fails variant | Value | Impact | Rating |
|---|---|---|---|
| No break fee, no stranded-cost restructuring | 3,877p | **+22p** | SELL (-17.7%) |
| Plus the **USD 420m termination fee** (EUR 375m). McCormick 10-Q to 31 Aug 2026 (0000063754-26-000329) note 2: "may be payable by us to Unilever ... under specified circumstances" | 3,892p | +37p | SELL (-17.4%) |
| No fee, EUR 500m restructuring still spent | 3,857p | +1p | SELL (-18.1%) |

Growth was left at 1.6%. That flatters this case: the perimeter's FY25 USG was 2.7%, against 3.5% for the Group (Form 425). At the 3.45% Bund, Foods inside Unilever is worth about the same as the McCormick consideration (+1p to +37p). So the deal failing is now roughly neutral, not a bear risk.

**Value impact: -138p (tax) to -201p (McCormick); deal fails +1p to +37p.**

## 2. The 17.7% margin assumes the remaining company holds its best-ever margin (PM decision 3; Fundamentals agent's margin base)
**Claim.** The DCF holds 17.7% (18.8% FY25 ex-perimeter, less 1.1% restructuring) flat for ever, starting from the top of a ten-year range. The bear uses the brief's **16.2%**: the c.17.3% 2023 level of the remaining company less 1.1%.

**Evidence.**
- Group underlying margin FY17-25: 17.5%, 18.4%, 19.1%, 18.5%, 18.4%, **16.1%**, 16.7%, 18.4%, 20.0% (annual results 6-Ks; ulvr-margin-evidence.md). It fell 2.3 points in FY22 on input costs.
- The remaining company's margin rose "~+170bps" between 2023 and 2025 (Form 425), which puts it at about 17.3% in 2023 (the margin pack's inference).
- **Stranded costs** are "c.EUR 400-500m gross" (Form 425): 1.0-1.3 points of the EUR 39.8bn of remaining sales if the mitigation fails. Management "is not calling any margin dilution" (31 Mar call).
- Fundamentals FLAG 5: part of the gross-margin step-up is mix from removing Ice Cream.
- Restructuring has never been below 0.8% of turnover in ten years (20-F XBRL `ExpenseOfRestructuringActivities`).

| Test | Value | Impact | Rating |
|---|---|---|---|
| **Required test 4:** margin 16.2% (brief `bear_agent_margin`) | 3,566p | **-290p** | SELL (-24.3%) |

**Value impact: -290p.**

## 3. Minorities: Hindustan Unilever's outside holders own more than 10.7% of the DCF (Fundamentals agent: `minority_share_of_operating_profit` 10.684%; PM decision 4)
**Claim.** The proportionate rule values the 38.1% outside holders of HUL at Unilever's group multiple. Their listed stake is worth **EUR 15,507m** today: 38.1% of HUL's EUR 40,700.7m, which is 2,349.6m shares x INR 1,875.5 / 108.27 INR per EUR (inputs.yaml `hul_market_value_meur`). HUL trades at about 44x its 2025 profit, against about 18x for Unilever (ulvr-minorities-evidence.md).

**Evidence.**
- Unilever owns 61.90% of HUL (20-F p.194).
- In FY24 the HUL minorities took 446 of 1,167 of HUL's profit, 38.2% (20-F note 15B).
- The Fundamentals agent's assumptions A1 and A2 already lean high, so the gap comes from the multiple, not from the ratio.

| Test | Minorities deducted | Value | Impact | Rating |
|---|---|---|---|---|
| **Required test 3:** HUL at 38.1% of market + other minorities at book (488) | EUR 15,995m (vs 9,737 proportionate) | 3,632p | **-224p** | SELL (-22.9%) |
| HUL at market + other minorities proportionate (10.684% x (1 - 446/587) = 2.57% of EV) | EUR 15,507m + 2,339m | 3,555p | -301p | SELL (-24.5%) |

The HUL share count comes from Yahoo, not a filing (Data agent FLAG). **Value impact: -224p (the brief's definition) to -301p.**

## 4. Growth and the terminal value: 1.6% for ever is the top of the evidence, and the engine's bear snaps back to it (Valuation agent; PM decisions 2 and 6; Fundamentals agent's RONIC flag)
**Claim.** The 1.6% is the low end of 4-6% USG less a 2.4-point currency drag, held for ever. That suits a portfolio that is about to become more exposed to emerging markets, not less:
- **62%** of the remaining company's turnover is in emerging markets (Form 425), against 59.4% for the Group in FY25 (30,008 / 50,503, 20-F p.138).
- In FY25, emerging-market turnover fell **6.3%** in euros on +3.5% USG; developed-market turnover rose 0.2% (`segments.csv`, 20-F p.138).

**Evidence.**
- **History:** euro growth before deals was 1.8% a year over FY17-25, reported growth 1.2%, and **0.2%** excluding FY22 (ulvr-growth-evidence.md).
- **Market reading:** the Data agent reads euro market growth at **1.1-1.6%** and puts the PM's 1.6% "at the top of that range" (data/notes.md section 5). An independent forward forecast is MISSING.
- **The engine bear is inconsistent:** it forecasts 0.2% for FY27-30 and then uses 1.6% terminal growth (`desk/valuation_run.py` `build`).
- **RONIC:** the 17.8% is the Group's FY25 ROIC after restructuring, on capital that includes Foods, and Foods holds EUR 7.9bn of the EUR 17.7bn of goodwill (20-F p.153). The remaining company's ROIC is MISSING.
  - Honest finding: removing Foods' capital probably raises that ROIC. If Foods' only capital were its goodwill, the remaining ROIC would be (7,484 - 1.12% x 39,803) x 0.74 / (39,502 - 7,900) = **16.5%**, and that is the low bound.
  - RONIC = WACC is shown only as an extreme case.

| Test | Value | Impact | Rating |
|---|---|---|---|
| Terminal growth **1.1%** (Data agent low end); JV growth at 1.1% too | 3,690p | **-166p** | SELL (-21.7%) |
| Consistent bear: engine bear with the JV fix (challenge 5) and terminal growth 0.2% | 2,934p | **-257p** vs the engine bear with the JV fix | SELL (-37.7%) |
| Terminal RONIC 16.5% (ex-Foods-goodwill low bound) | 3,835p | -20p | SELL |
| Terminal RONIC = WACC 7.10% (growth creates no value; extreme) | 3,473p | -383p | SELL (-26.3%) |

**Value impact: -166p (terminal growth 1.1%); RONIC -20p to -383p.**

## 5. The discount rate: the bear under-shifts it, and the beta has an upper side (Risk agent: beta 0.8844; Valuation agent's bear)
**Claim.** The engine bear raises WACC by 1 point but keeps the JVs (EUR 3,710m, mainly the Pepsi Lipton tea partnerships) at the base Ke. The Risk agent's own file also contains a higher sourced beta.

**Evidence.**
- **JVs:** 229 x 1.016 / (Ke - 1.6%) (PM decision 10). At Ke 7.872% + 1 point = 8.872%, the value falls from EUR 3,710m to **EUR 3,199m**.
- **Beta:** Damodaran's 2020-24 average cash-corrected Household Products unlevered beta of **0.8752** (same betaGlobal.xls), relevered at D/E 0.1924, gives **0.9998**: Ke 8.45% at the 3.45% Bund (risk/notes.md).
- **Leverage:** on 30 Jun 2026 net debt (EUR 25,961m after the EUR 1.5bn buyback; 2.27x against the "around 2x" target), the base beta would already be 0.898 (risk/notes.md).
- Not sized: the WACC uses leverage from before the sale (Valuation FLAG, Risk FLAG 2).

| Test | Value | Impact | Rating |
|---|---|---|---|
| **Required test 5:** engine bear (0.2% growth, WACC +1 pt) with the JVs at Ke + 1 pt | **3,191p** | **-21p** vs 3,212p | SELL (-32.3%) |
| Beta 0.9998 (Damodaran 2020-24 average); JVs at the new Ke | 3,588p | **-267p** | SELL (-23.8%) |
| (Cross-check) Beta 0.91, own 5y monthly regression | 3,792p | -63p | SELL |

**Value impact: -21p (JV fix to the bear); -267p (beta 0.9998).**

---

## Stacked bear (deal closes)
| Stack | Value | vs base | Rating |
|---|---|---|---|
| Engine bear + JV fix + margin 16.2% + 25% tax | **2,817p** | -1,038p | SELL (-40.2%) |
| The same + HUL at market (others proportionate) | **2,437p** | -1,419p | SELL (-48.3%) |

Each stack was computed in a single engine run. The tests interact through EV and minorities, so they do not simply add.

## Risks to the SELL (what would make it wrong), each re-run through the engine
HOLD flip points from Valuation notes (e), now further away: **beta 0.748**, WACC 6.52% (-0.58 pt), terminal growth 2.50%, **margin 19.7%**, **McCormick USD 66.55** (+49%), or EUR 9.8bn of extra value today.

| Risk | Value | Impact | Rating |
|---|---|---|---|
| **Beta 0.54** (own 5y weekly vs FTSE 100, the most precise own regression; JVs at the new Ke) | **5,027p** | +1,172p | **HOLD (+6.7%)** |
| Beta 0.748 (the flip point; JVs consistent) | 4,238p | +383p | at the HOLD boundary (-10.0%) |
| Margin 19.7% (the flip point; above any margin in the evidence for the remaining company: 18.8% FY25, management's pro forma ">19%") | 4,242p | +386p | HOLD (-10.0%), boundary |
| Margin 18.8% (restructuring treated as one-off) | 4,068p | +213p | SELL (-13.6%) |
| Margin 18.2% (18.8% less management's 0.6% guide) | 3,952p | +97p | SELL (-16.1%) |
| McCormick at USD 66.55 (the flip point; above its 52-week range except Feb 2026, high USD 71.65) | 4,239p | +384p | boundary |
| McCormick back to the USD 57.84 deal reference | 4,087p | +231p | SELL (-13.2%) |
| The deal fails (with the USD 420m fee) | 3,892p | +37p | SELL |
| Foods' cash flows from 1 Jan 2026 to closing belong to Unilever (MISSING; Data agent indicator about EUR 2.9bn) | about +113p (indicator only) | | SELL |

**The SELL is now 384p (8.2 points) from HOLD.** Of the sourced alternatives, only Unilever's own low weekly betas (0.43-0.54) reach HOLD. No sourced margin or McCormick price in the evidence does. Nothing reaches BUY. The main risk to the call is still beta: the bottom-up 0.88 against an own-regression range of 0.43-0.91.

## Management track record: guidance vs outcome
| Year | Guidance (source) | Outcome | Verdict |
|---|---|---|---|
| FY17 target | "underlying operating margin of 20% by 2020", EUR 6bn savings (FY17 results 6-K 0001654954-18-000934) | FY20 margin **18.5%** (FY20 6-K 0001654954-21-001146) | **Missed by 1.5 points**; target dropped |
| FY18 | USG "in the 3% - 5% range" (FY17 6-K) | 2.9% | Missed (below the range) |
| FY19 | "lower half of our multi-year 3-5% range" (FY18 6-K 0001654954-19-000903) | 2.9% | Missed (below the range) |
| FY20 | "lower half of the multi-year 3-5% range" (FY19 6-K 0001654954-20-000935) | 1.9% | Missed (Covid) |
| FY22 | USG 4.5-6.5%; margin "between 16% and 17%" (FY21 6-K 0001654954-22-001398) | USG 9.0%; margin 16.1% | Sales beat (inflation pricing); margin at the bottom of the range |
| FY23 | "strong" USG, "improved margin" (FY22 6-K 0001654954-23-001506) | 7.0%; 16.7% | Met (qualitative) |
| FY24 | USG within 3-5%, "modest improvement" in margin (FY23 6-K 0001654954-24-001469) | 4.2%; 18.4% (+1.7 points) | Met / beat |
| FY25 | USG within 3-5%, "modest improvement" vs 18.4% (FY24 6-K 0001654954-25-001439) | 3.5%; 20.0% ex Ice Cream (not like for like) | Met |
| FY26 | 4-6% range, "bottom end" (FY25 6-K 0001654954-26-001155); upgraded in July: H2 4-5% (H1 2026 6-K) | H1 4.8% | On track |
| Restructuring | 2022 "around EUR 1.4bn", then "around 1% of turnover" (FY21 6-K) | FY23-25: 0.8%, 1.4%, 1.2% (average 1.1%); FY26 guide "around 1.0%" (H1 2026 6-K) | Roughly met at 1%. The **new 0.6% guide** (31 Mar 2026 call) has never been reached in ten years (lowest 0.8%) |

**Reading.** One-year guides are usually met, because they are qualitative or wide ranges. The **multi-year promises** are the weak spot:
- the 20% margin by 2020 was missed;
- the USG range was missed three years running (FY18-20);
- restructuring has never fallen below 0.8% of turnover.

The Foods deal rests on exactly this kind of promise: "no margin dilution" from EUR 400-500m of stranded costs, restructuring of 0.6%, and synergies that "fully offset" an undisclosed tax bill.

---

**Strongest reason not to buy:** at 4,710.5p the market already pays 14.7x EBITDA for the business that remains (peer median 11.9x; DCF exit 10.9x). Every sourced bear test lowers the value further: 25% tax 138p, McCormick's own volatility 201p, HUL at market 224p, the 2023 margin 290p. Even HOLD needs a 19.7% margin the remaining business has never earned, McCormick at USD 66.55, or a beta of 0.75 or below, so the price already assumes a best case that Unilever's record on multi-year promises does not support.
