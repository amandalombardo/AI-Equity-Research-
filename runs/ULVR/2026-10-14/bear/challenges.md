# Bear case: Unilever PLC (ULVR), run 2026-10-14

Price **4,710.5p** (ULVR.L close 13 Oct 2026). Base case **4,018p, SELL (-14.7%)**. Engine bear **3,323p**. HOLD starts at 4,239p (-10%), BUY at 5,417p (+15%).
Money in EUR m; values per share in pence (GBp). EUR 1.18190 per GBP; USD 1.1193 per EUR (FRED, 9 Oct 2026); 2,154.3m shares.

**How each impact was measured.** `bear/run_bear.py` copies `briefs/ULVR.yaml` and `inputs.yaml` into `bear/scratch/<test>/`, changes one assumption (plus any input that must move with it, stated below), and runs `python -m desk.valuation_run` on the copy. That is the same command the Valuation agent ran. An unchanged copy reproduces 4,017.8p and 3,323.2p exactly. All results are in `bear/bear_results.json`. Items priced on the run date (tax, the HUL market value, the McCormick price) are also netted in `priced_at_valuation_date_meur`, so the engine does not grow them at the cost of equity. The brief and `inputs.yaml` were not changed.

The base case is already a SELL. The bear case therefore asks two questions: how far below the price the value could go, and whether any sourced test breaks the SELL.

---

## 1. The Foods consideration is worth less than the EUR 33,955m counted (Data agent: `disposal_proceeds`; PM decisions 1 and 5)
**Claim.** A third of the value per share (1,334p, Valuation notes (d)) is the McCormick deal at today's price, with no tax and no market risk. Both of those are generous.

**Evidence.**
- **Tax is real and unpriced.** Management says synergies "fully offset Unilever's tax and separation costs" (Form 425, 0000217410-26-000027). The CFO said it would be "premature to start making estimates" (Form 425 call transcript, 0000217410-26-000032). The US leg is "intended to be tax free" and the other jurisdictions are not (ulvr-tax-evidence.md). We value the McCormick shares at market, so the synergies are already in that price. Counting the synergies against the tax would count them twice.
- **The McCormick price is moving against the deal.** MKC was USD 65.80 a year ago and is **USD 44.64** now (13 Oct 2026), down **32%** in a year and **23%** below the USD 57.84 deal reference (brief section 3). Its 1-year annualised volatility is **30.5%** (Yahoo daily closes, `bear/scratch/mkc_1y_yahoo.csv`; `desk.risk.annualised_volatility`). Unilever and its shareholders receive a fixed **499.7m shares**, so they carry that risk until closing (expected mid-2027, about 0.71 years away).
- The payment arrives at closing, not today: **-15p** for the cash part discounted at Bund + A spread, up to -68p for the whole amount at the cost of equity (Valuation notes (a)).

| Test (one change, engine re-run) | Value | Impact | Rating |
|---|---|---|---|
| **Required test 2:** tax at 25% of the USD 15.7bn cash = **EUR 3,507m** (USD 15,700m / 1.1193 x 25%), priced today | 3,880p | **-138p** | SELL (-17.6%) |
| McCormick falls one standard deviation to closing: USD 44.64 x (1 - 30.5% x sqrt(0.71)) = **USD 33.15** | 3,816p | **-201p** | SELL (-19.0%) |

**The deal failing is NOT a bear outcome on our numbers (required test 1).** With Foods kept in the DCF, the value goes **up**, because the market prices the McCormick consideration below what Foods is worth as part of Unilever. The test used the whole-group FY25 sales of EUR 50,503m and a margin of **18.85%**: the group underlying margin of 19.97% less the 1.12% FY23-25 restructuring average, the same rule as decision 3 (ulvr-margin-evidence.md). There is no consideration in the bridge and no EUR 500m stranded-cost restructuring. Minorities are at the group ratio of 7.93% (587 / 7,403, Fundamentals notes) instead of 10.68%.

| Deal-fails variant | Value | Impact | Rating |
|---|---|---|---|
| No break fee, no stranded-cost restructuring | 4,100p | **+82p** | SELL (-13.0%) |
| Plus the **USD 420m termination fee** (EUR 375m). Source: McCormick 10-Q to 31 Aug 2026 (0000063754-26-000329), note 2: "may be payable by us to Unilever ... under specified circumstances" | 4,115p | +97p | SELL (-12.6%) |
| No fee, EUR 500m restructuring still spent | 4,080p | +62p | SELL (-13.4%) |

Growth was left at the base 1.6%. That flatters this case slightly: the sale perimeter's FY25 USG was 2.7%, against 3.5% for the Group (Form 425). This is a reason the deal is value-destructive at today's McCormick price. It is not a reason to fear that the deal breaks.

**Value impact: -138p (tax) to -201p (McCormick); the deal failing is +62p to +97p.**

## 2. The 17.7% margin assumes the remaining company holds its best-ever margin (PM decision 3; Fundamentals agent's margin base)
**Claim.** The DCF holds 17.7% flat for ever. That is 18.8% (FY25 ex-perimeter) less 1.1% restructuring, and FY25 is the peak of a ten-year range. The bear margin is the brief's **16.2%**: the c.17.3% 2023 level of the remaining company less 1.1%.

**Evidence.**
- The Group underlying margin was 17.5%, 18.4%, 19.1%, 18.5%, 18.4%, **16.1%**, 16.7%, 18.4% and 20.0% over FY17-25 (annual results 6-Ks; ulvr-margin-evidence.md section 2). It fell 2.3 points in one year (FY22) when input costs rose.
- The remaining company's margin rose "~+170bps" from 2023 to 2025 (Form 425 investor presentation). So it was about 17.3% two years ago. That is the desk's inference, labelled in the margin pack.
- **Stranded costs** are "c.EUR 400-500m gross" (Form 425, 0000217410-26-000027). That is about 1.0-1.3 points of the EUR 39.8bn remaining sales if mitigation fails. Management "is not calling any margin dilution" (31 Mar call).
- Fundamentals FLAG 5: part of the gross-margin step-up is portfolio mix from removing Ice Cream, not pricing power.
- Restructuring has never been below 0.8% of turnover in ten years (20-F XBRL `ExpenseOfRestructuringActivities`). See the track record below.

| Test | Value | Impact | Rating |
|---|---|---|---|
| **Required test 4:** margin 16.2% (brief `bear_agent_margin`) | 3,715p | **-303p** | SELL (-21.1%) |

**Value impact: -303p.**

## 3. Minorities: Hindustan Unilever's outside shareholders own far more than 10.7% of the DCF says (Fundamentals agent: `minority_share_of_operating_profit` 10.684%; PM decision 4)
**Claim.** The proportionate rule gives the 38.1% outside holders of HUL a share of value at Unilever's group multiple. In practice they own a listed stake worth **EUR 15,507m** today (38.1% of HUL's EUR 40,700.7m market value: 2,349.6m shares x INR 1,875.5 / 108.27 INR per EUR, inputs.yaml `hul_market_value_meur`). HUL trades at about 44x its 2025 profit, against about 18x for Unilever (ulvr-minorities-evidence.md). The Indian growth that earns that multiple is inside Unilever's DCF at 1.6%. The value that leaves the group is HUL's market value, not a DCF slice.

**Evidence.** Unilever owns 61.90% of HUL (20-F p.194). The HUL minorities took 446 of 1,167 of HUL profit in FY24, 38.2% (20-F note 15B). The Fundamentals agent's ratio already rests on two assumptions that overstate it slightly (A1, A2), so it is not too low for that reason. It is low because of the multiple.

| Test | Minorities deducted | Value | Impact | Rating |
|---|---|---|---|---|
| **Required test 3:** HUL at 38.1% of market + other minorities at book (488) | EUR 15,995m (vs 10,200 proportionate) | 3,813p | **-205p** | SELL (-19.1%) |
| HUL at market + other minorities proportionate (10.684% x (1 - 446/587) = 2.57% of EV) | EUR 15,507m + 2,450m | 3,731p | -287p | SELL (-20.8%) |

The HUL share count is from Yahoo, not a filing (Data agent FLAG). **Value impact: -205p (the brief's definition) to -287p.**

## 4. Growth and the terminal value: 1.6% for ever is the top of the evidence, and the engine's bear case snaps back to it (Valuation agent; PM decisions 2 and 6; Fundamentals agent's RONIC flag)
**Claim.** 77% of EV is terminal value (Valuation FLAG 2). The 1.6% assumes the low end of 4-6% USG less a 2.4-point currency drag, held for ever. The remaining company has **62%** of its turnover in emerging markets (Form 425), against 59.4% for the Group in FY25 (30,008 / 50,503, 20-F p.138). In FY25 emerging-market turnover fell **6.3%** in euros while USG was +3.5%; developed-market turnover rose 0.2% (Fundamentals `segments.csv`, 20-F p.138). A more emerging-market portfolio carries more of the currency drag, not less.

**Evidence.**
- Over FY17-25 euro growth before deals was 1.8% a year, reported growth 1.2%, and **0.2%** excluding FY22 (ulvr-growth-evidence.md).
- The Data agent's own market reading puts euro growth at **1.1-1.6%** and says the PM's 1.6% is "at the top of that range ... no room for a higher rate" (data/notes.md section 5). No independent forward HPC forecast is available (MISSING).
- **The engine bear is internally inconsistent.** It forecasts 0.2% for FY27-30, then returns to 1.6% terminal growth for ever (`desk/valuation_run.py` `build` always uses the brief's terminal growth).
- **RONIC.** The 17.8% is the Group's FY25 ROIC after restructuring, on capital that includes Foods. Foods carries EUR 7.9bn of the EUR 17.7bn goodwill (20-F p.153). The remaining company's ROIC is not disclosed (MISSING). An honest finding: removing Foods' capital probably RAISES the remaining ROIC. If Foods' only capital were its goodwill, the remaining ROIC would be (7,484 - 1.12% x 39,803) x (1 - 26%) / (39,502 - 7,900) = **16.5%**. That is the low bound, so the goodwill point is weak. The stronger RONIC challenge is that Unilever's growth increasingly comes from acquisitions bought at full prices, whose incremental return is close to the cost of capital. That is an argument, not a sourced number, so it is shown only as the extreme case.

| Test | Value | Impact | Rating |
|---|---|---|---|
| Terminal growth **1.1%** (Data agent low end); JV Gordon growth moved to 1.1% too | 3,832p | **-186p** | SELL (-18.7%) |
| Consistent bear: engine bear (with the JV fix in 5) and terminal growth 0.2% | 3,017p | **-283p** vs the engine bear with JV fix | SELL (-36.0%) |
| Terminal RONIC 16.5% (ex-Foods-goodwill low bound) | 3,996p | -22p | SELL |
| Terminal RONIC = WACC 6.84% (growth creates no value; extreme) | 3,587p | -430p | SELL (-23.8%) |

**Value impact: -186p (terminal growth 1.1%); RONIC -22p to -430p.**

## 5. The discount rate: the bear case under-shifts it, and the beta has an upper side too (Risk agent: beta 0.8844; Valuation agent FLAG 4)
**Claim.** The engine bear raises WACC by 1 point but leaves the joint ventures (EUR 3,876m by Gordon growth, mainly the Pepsi Lipton tea partnerships) at the base cost of equity. Separately, the Risk agent's own file gives a higher sourced beta than the one used.

**Evidence.**
- JVs: 229 x 1.016 / (Ke - 1.6%) (PM decision 10; `data/apply_pm_decision10.py`). At Ke 7.60% + 1 point = 8.60%, the value falls from EUR 3,876m to **EUR 3,323m**.
- Beta: Damodaran's 2020-24 average cash-corrected Household Products unlevered beta, **0.8752** (same betaGlobal.xls, PM upload), relevered at D/E 0.1924, gives **0.9998** and Ke 8.18% (risk/notes.md). On 30 Jun 2026 net debt (EUR 25,961m, after the EUR 1.5bn buyback, leverage 2.27x against the "around 2x" target) the base beta would already be 0.898 (risk/notes.md).
- Not sized (Valuation FLAG 7, Risk FLAG 2): the WACC uses leverage from before the sale.

| Test | Value | Impact | Rating |
|---|---|---|---|
| **Required test 5:** engine bear (0.2% growth, WACC +1 pt) with the JVs at Ke + 1 pt | **3,300p** | **-23p** vs 3,323p | SELL (-29.9%) |
| Beta 0.9998 (Damodaran 2020-24 average), JVs at the new Ke | 3,725p | **-293p** | SELL (-20.9%) |

**Value impact: -23p (JV fix to the bear); -293p (beta 0.9998).**

---

## Stacked bear (deal closes)
Engine bear + JV fix + margin 16.2% + 25% tax: **2,918p (-38.1%)**, -1,100p vs base.
The same plus HUL at market (others proportionate): **2,546p (-46.0%)**, -1,472p vs base.
These do not simply add: each test interacts with the others through EV and minorities. The engine computed each stack in a single run.

## Risks to the SELL (what would make it wrong), each re-run through the engine
| Risk | Value | Impact | Rating |
|---|---|---|---|
| **Beta 0.54** (Unilever's own 5y weekly vs FTSE 100, the most precise own regression; JVs at the new Ke) | **5,330p** | +1,312p | **HOLD (+13.2%)**, near BUY |
| McCormick back to the USD 57.84 deal reference | 4,249p | +231p | **HOLD (-9.8%)** |
| Margin **18.8%** (restructuring treated as one-off; management's pro forma is ">19%") | 4,240p | +222p | **HOLD (-10.0%)**, at the boundary |
| Margin 18.2% (18.8% less management's 0.6% restructuring guide) | 4,119p | +101p | SELL (-12.6%) |
| The deal fails (with the USD 420m fee) | 4,115p | +97p | SELL |
| Foods cash flows from 1 Jan 2026 to closing belong to Unilever (MISSING; Data agent's indicator about EUR 2.9bn before capex) | about +113p (Valuation notes, indicator only) | | SELL |

HOLD flip points (Valuation notes (e)): beta **0.809**, WACC -0.32 points, terminal growth 2.10%, margin 18.8%, MKC USD 57.28, or EUR 5.6bn of extra value today.
**The SELL is only 222p (4.7 points) from HOLD.** One sourced alternative (beta 0.54) moves it to HOLD, and two more land on the boundary. No sourced test reaches BUY.

## Management track record: guidance vs outcome
| Year | Guidance (source) | Outcome | Verdict |
|---|---|---|---|
| FY17 target | "underlying operating margin of 20% by 2020", EUR 6bn savings (FY17 results 6-K 0001654954-18-000934) | FY20 margin **18.5%** (FY20 results 6-K 0001654954-21-001146) | **Missed by 1.5 points**; the target was dropped |
| FY18 | USG "in the 3% - 5% range" (FY17 6-K) | 2.9% | Missed (below the range) |
| FY19 | "lower half of our multi-year 3-5% range" (FY18 6-K 0001654954-19-000903) | 2.9% | Missed (below the range) |
| FY20 | "lower half of the multi-year 3-5% range" (FY19 6-K 0001654954-20-000935) | 1.9% | Missed (Covid) |
| FY22 | USG 4.5-6.5%; margin "between 16% and 17%" (FY21 6-K 0001654954-22-001398) | USG 9.0%; margin 16.1% | Sales beat (inflation pricing); margin at the bottom |
| FY23 | "strong" USG, "improved margin" (FY22 6-K 0001654954-23-001506) | 7.0%; 16.7% | Met (qualitative) |
| FY24 | USG within 3-5%, "modest improvement" in margin (FY23 6-K 0001654954-24-001469) | 4.2%; 18.4% (+1.7 points) | Met / beat |
| FY25 | USG within 3-5%, "modest improvement" vs 18.4% (FY24 6-K 0001654954-25-001439) | 3.5%; 20.0% ex Ice Cream (not like for like) | Met |
| FY26 | 4-6% range, "bottom end" (FY25 6-K 0001654954-26-001155); upgraded July: H2 4-5% (H1 2026 6-K) | H1 4.8% | On track |
| Restructuring | 2022 "around EUR 1.4bn", "returning to pre-2017 levels of around 1% of turnover thereafter" (FY21 6-K) | FY23-25: 0.8%, 1.4%, 1.2% (avg 1.1%); FY26 guide "around 1.0%" (H1 2026 6-K) | Roughly met at 1%. The **new 0.6% guide** (31 Mar 2026 call) has never been reached in ten years (lowest 0.8%) |

**Reading.** One-year guides are usually met, because they are qualitative or wide ranges. The **multi-year promises** are the weak spot: the 20% margin by 2020 was missed, the USG range was missed three years running (FY18-20), and the medium-term restructuring level has never fallen below 0.8%. The Foods deal rests on exactly this kind of multi-year promise: "no margin dilution" from EUR 400-500m of stranded costs, restructuring of 0.6%, and synergies that "fully offset" an undisclosed tax bill.

---

**Strongest reason not to buy:** at 4,710.5p the market already pays 14.7x EBITDA for the business that remains (peer median 11.9x). Every sourced bear test lowers the value further: the 25% tax costs 138p, McCormick's own volatility 201p, HUL at market 205p and the 2023 margin 303p. The only route back to the price is a 0.54 beta, so the shares already price in a best case that Unilever's record of missing multi-year promises does not support.
