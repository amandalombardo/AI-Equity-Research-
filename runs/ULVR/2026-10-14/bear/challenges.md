# Bear case: Unilever PLC (ULVR), run 2026-10-14

## Re-run 15 Oct 2026 (evidence audit)

**This version replaces the 14 Oct 2026 bear (base 3,855p SELL), which is superseded.** The old file is kept, unchanged, at `bear/scratch/challenges_2026-10-14_superseded.md`.

**Inputs.** Brief and inputs after the PM's evidence-audit decisions of 15 Oct 2026 (docs/audit-2026-10-15/ULVR.md):
- ERP **4.2%** (Damodaran implied; was 5.0% with no source)
- pension plans in deficit deducted after tax: **EUR 698.6m**
- McCormick dividends before closing deducted: **EUR 642.9m** (3 quarters)
- JVs at the new cost of equity: **EUR 4,181.2m**; associates EUR 7,533.5m
- FY26 growth **+2.0%** in the base and the bear

**Valuation.** Price **4,710.5p** (ULVR.L close 13 Oct 2026). Base **4,258.5p, HOLD (-9.6%)**, only **19.1p above the SELL line of 4,239.45p**. Engine bear **3,475.6p**. BUY starts at 5,417.1p.

**Discount rate.** Cost of equity 7.164% = Bund 3.45% + beta 0.8844 x ERP 4.2%. WACC 6.50%.

**Units.** Money in EUR m; values per share in pence (GBp); McCormick prices in USD. EUR 1.18190 per GBP and USD 1.1193 per EUR (FRED, 9 Oct 2026). 2,154.3m shares.

**How each impact was measured.** `bear/run_bear.py` copies the current `briefs/ULVR.yaml` and `inputs.yaml` into `bear/scratch/<test>/`, changes one assumption (plus any input that must move with it, stated below) and runs `python -m desk.valuation_run` on the copy.
- An unchanged copy reproduces the Valuation agent's 4,258.5p and 3,475.6p exactly. The script asserts this against `valuation/valuation.json`.
- The script also checks two inputs. The associates must equal the JV value at Ke 7.164% plus EUR 3,352.3m. The Foods consideration must equal the cash plus the shares at today's price, less 3 quarters of McCormick dividends.
- Wherever the cost of equity or growth moves, the JVs are re-valued at 229 x (1 + g) / (Ke - g).
- Every McCormick price test keeps the dividend deduction.
- Items priced today are netted in `priced_at_valuation_date_meur`.
- Results are in `bear/bear_results.json`. The brief and `inputs.yaml` were not changed.

**What the re-run changes.** The base is now a HOLD by 19.1p, so the question is no longer "how far below SELL". It is "does any sourced bear test reach SELL". Almost all of them do:
- **Every one of the five challenges turns HOLD into SELL.**
- **All four audit rate stresses** turn it into SELL as well: ERP 5.0%, ERP 5.5%, Bund 3.50% and spread 1.0%. So does discounting the whole Foods consideration at WACC.
- Only the Foods cash part discounted at the cost of debt (-15.7p) leaves it HOLD, by 3.5p.

---

## 1. The Foods consideration is worth less than the EUR 33,312m counted (Data agent: `disposal_proceeds`; PM decisions 1 and 5)
**Claim.** The deal at today's price is about **1,308p, 31% of the value per share** (Valuation notes, value breakdown). It is counted untaxed, free of market risk and as if paid today.

**Evidence.**
- **Tax is real and unpriced.**
  - Management says synergies "fully offset Unilever's tax and separation costs" (Form 425, 0000217410-26-000027).
  - The CFO said it was "premature to start making estimates" (Form 425 call transcript, 0000217410-26-000032).
  - Only the US leg is "intended to be tax free" (ulvr-tax-evidence.md).
  - The McCormick shares are valued at market, so the synergies are already in that price. Offsetting the tax with them counts them twice.
  - **At the new base, any tax above about EUR 0.49bn makes it SELL** (Valuation notes).
- **McCormick is moving against the deal.**
  - MKC was USD 65.80 a year ago and is **USD 44.64** now (13 Oct 2026): **-32%** in a year, and **-23%** against the USD 57.84 deal reference (brief section 3).
  - Its 1-year annualised volatility is **30.5%** (Yahoo daily closes, `bear/scratch/mkc_1y_yahoo.csv`; `desk.risk.annualised_volatility`).
  - The 499.7m shares are fixed. Closing is expected mid-2027, about 0.71 years away.
  - **A fall of only 2.4%, to USD 43.55, makes it SELL** (re-run: 4,239.4p).

| Test (one change, engine re-run) | Value | Impact vs 4,258.5p | Rating |
|---|---|---|---|
| **Required test 2:** tax at 25% of the USD 15.7bn cash = **EUR 3,507m** (USD 15,700m / 1.1193 x 25%), priced today | 4,120.8p | **-137.7p** | **SELL (-12.5%)**, was HOLD |
| McCormick 1 s.d. lower by closing: USD 44.64 x (1 - 30.5% x sqrt(0.71)) = **USD 33.15**; dividend deduction kept | 4,057.2p | **-201.4p** | **SELL (-13.9%)**, was HOLD |

**Required test 1: the deal failing is now an upside risk, not a bear outcome.** The test keeps Foods in the DCF:
- whole-group FY25 sales of EUR 50,503m;
- margin **18.85%** = group underlying 19.97% less the 1.12% FY23-25 restructuring average (the decision 3 rule);
- no consideration and no McCormick dividend deduction;
- no EUR 500m stranded-cost restructuring;
- minorities at the group ratio of 7.93% (587 / 7,403);
- **FY26 growth +0.5%**, the whole Group including Foods (H1 2026 6-K). This is the right perimeter when Foods stays, so I reversed the PM's +2.0% here, consistently.

| Deal-fails variant | Value | Impact | Rating |
|---|---|---|---|
| No break fee, no stranded-cost restructuring | 4,394.3p | **+135.7p** | HOLD (-6.7%) |
| Plus the **USD 420m termination fee** (EUR 375m; McCormick 10-Q 0000063754-26-000329 note 2, payable "under specified circumstances") | 4,409.0p | +150.5p | HOLD (-6.4%) |
| No fee, EUR 500m restructuring still spent | 4,373.5p | +115.0p | HOLD (-7.2%) |

At the lower 4.2% ERP, Foods inside Unilever is worth more than the McCormick consideration net of dividends: about +115p to +151p. Growth after FY26 was left at 1.6%, which still flatters this case: the perimeter's FY25 USG was 2.7%, against 3.5% for the Group (Form 425).

**Value impact: -137.7p (tax) to -201.4p (McCormick); each alone turns HOLD into SELL. A failed deal is +115p to +151p (upside).**

## 2. The 17.7% margin assumes the remaining company holds its best-ever margin (PM decision 3; Fundamentals agent's margin base)
**Claim.** The DCF holds 17.7% flat for ever (18.8% FY25 ex-perimeter, less 1.1% restructuring), starting from the top of a ten-year range. The bear uses the brief's **16.2%**: the c.17.3% 2023 level of the remaining company less 1.1%. **The HOLD survives only if the margin stays at or above 17.61%, 0.09 points below the base** (re-run: 17.61% gives 4,239.0p, SELL by 0.4p).

**Evidence.**
- Group underlying margin FY17-25: 17.5%, 18.4%, 19.1%, 18.5%, 18.4%, **16.1%**, 16.7%, 18.4%, 20.0% (annual results 6-Ks; ulvr-margin-evidence.md). It fell 2.3 points in FY22 on input costs. Note that FY21-22 include Ice Cream and FY23-25 do not (audit finding 10).
- The remaining company's margin rose "~+170bps" between 2023 and 2025 (Form 425), which implies about 17.3% in 2023.
- **Stranded costs** are "c.EUR 400-500m gross" (Form 425): 1.0-1.3 points of the EUR 39.8bn of remaining sales if mitigation fails. Management "is not calling any margin dilution" (31 Mar call).
- Fundamentals FLAG 5: part of the gross-margin step-up is mix from removing Ice Cream.
- Restructuring has never been below 0.8% of turnover in ten years (20-F XBRL `ExpenseOfRestructuringActivities`).

| Test | Value | Impact | Rating |
|---|---|---|---|
| **Required test 4:** margin 16.2% (brief `bear_agent_margin`) | 3,932.2p | **-326.3p** | **SELL (-16.5%)**, was HOLD |

**Value impact: -326.3p.**

## 3. Minorities: Hindustan Unilever's outside holders own more than 10.7% of the DCF (Fundamentals agent: `minority_share_of_operating_profit` 10.684%; PM decision 4)
**Claim.** The proportionate rule values the 38.1% outside holders of HUL at Unilever's group multiple. Their listed stake is worth **EUR 15,507m** today:
- 38.1% of HUL's EUR 40,700.7m market value;
- that market value is 2,349.6m shares x INR 1,875.5 / 108.27 INR per EUR (inputs.yaml `hul_market_value_meur`).

HUL trades at about 44x its 2025 profit, against about 18x for Unilever (ulvr-minorities-evidence.md).

**Evidence.**
- Unilever owns 61.90% of HUL (20-F p.194).
- In FY24 the HUL minorities took 446 of HUL's 1,167 profit, 38.2% (20-F note 15B).
- At the lower WACC the proportionate deduction rises to EUR 11,040m (10.684% x EV 103,329). The gap to market value therefore narrows a little, but it is still larger than the 19.1p cushion.

| Test | Minorities deducted | Value | Impact | Rating |
|---|---|---|---|---|
| **Required test 3:** HUL at 38.1% of market + other minorities at book (EUR 488m) | EUR 15,995m (vs 11,040 proportionate) | 4,087.1p | **-171.4p** | **SELL (-13.2%)**, was HOLD |
| HUL at market + other minorities proportionate (10.684% x (1 - 446/587) = 2.57% of EV) | EUR 15,507m + 2,651m | 3,997.4p | -261.2p | **SELL (-15.1%)** |

The HUL share count comes from Yahoo, not a filing (Data agent FLAG). **Value impact: -171.4p (the brief's definition) to -261.2p.**

## 4. Growth and the terminal value: 1.6% for ever is the top of the evidence, and the terminal value is now 77.9% of EV (Valuation agent; PM decisions 2 and 6; Fundamentals agent's RONIC flag)
**Claim.** The 1.6% is the low end of 4-6% USG less a 2.4-point currency drag, held for ever. The remaining portfolio is more exposed to emerging markets, not less:
- **62%** of the remaining company's turnover is in emerging markets (Form 425), against 59.4% for the Group (30,008 / 50,503, 20-F p.138).
- In FY25, emerging-market turnover fell **6.3%** in euros on +3.5% USG (`segments.csv`, 20-F p.138).

At WACC 6.50% the terminal value is **77.9% of EV** (was 75.7%), so the call rests even more on the for-ever assumptions. **The HOLD breaks at terminal growth of 1.560%, 0.04 points lower** (Valuation breakevens).

**Evidence.**
- **History:** euro growth before deals was 1.8% a year over FY17-25, and **0.2%** excluding FY22 (ulvr-growth-evidence.md).
- **Market reading:** the Data agent reads euro market growth at **1.1-1.6%** and puts 1.6% "at the top of that range" (data/notes.md section 5). An independent forward forecast is MISSING.
- **FY26 +2.0% is an H1 figure,** the reported change of the three HPC business groups (H1 2026 6-K). It is not a full-year number. Below +1.51% for the year, the rating is SELL (Valuation FLAG 6).
- **The engine bear is inconsistent:** it forecasts 0.2% for FY27-30 and then uses 1.6% terminal growth.
- **RONIC:** 17.8% is the Group's FY25 ROIC on capital that includes Foods (EUR 7.9bn of the EUR 17.7bn of goodwill, 20-F p.153). The low bound without Foods' goodwill is (7,484 - 1.12% x 39,803) x 0.74 / (39,502 - 7,900) = **16.5%**. **Even that low bound now gives SELL**, by 4.4p.

| Test | Value | Impact | Rating |
|---|---|---|---|
| Terminal growth **1.1%** (Data agent low end); JV growth at 1.1% too | 4,037.5p | **-221.1p** | **SELL (-14.3%)**, was HOLD |
| Consistent bear: engine bear + JV fix (challenge 5) + terminal growth 0.2% | 3,121.0p | **-328.2p** vs the engine bear with the JV fix (3,449.2p) | SELL (-33.7%) |
| Terminal RONIC 16.5% (ex-Foods-goodwill low bound) | 4,235.0p | -23.6p | **SELL (-10.1%)**, was HOLD |
| Terminal RONIC = WACC 6.50% (growth creates no value; extreme) | 3,747.3p | -511.2p | SELL (-20.4%) |

**Value impact: -221.1p (terminal growth 1.1%); RONIC -23.6p to -511.2p.**

## 5. The discount rate: the HOLD exists only at the lowest sourced ERP, and every other sourced rate gives SELL (Risk agent: beta 0.8844; PM's ERP 4.2%; Valuation agent's bear)
**Claim.**
- The move from SELL to HOLD comes almost entirely from the ERP cut, 5.0% to 4.2% (+379.1p of the +403.3p step; Valuation step table).
- That 4.2% is the **lowest** of the sourced ERPs: Damodaran implied 4.20%, against Kroll 5.0% and the Fernandez survey 5.5%. It has been seen in search summaries only (brief FLAG; erp-evidence.md).
- The HOLD breaks at an **ERP of 4.234%**, a **Bund of 3.476%**, or a **beta of 0.892** (Valuation breakevens).
- The engine bear also keeps the JVs at the base Ke.

**Evidence.**
- **ERP.** Kroll's recommended US ERP is 5.0%, reaffirmed through 2026. It pairs that with the 20-year Treasury (5.60%), not the 10-year, so the 5.0% here is a conservative reading of Kroll. Fernandez et al. 2025 survey: US 5.5%, UK and Germany 5.4%. All secondhand (erp-evidence.md 2b-2c).
  - **ERP 5.0% gives 3,854.1p**, almost exactly the old 3,855p base: the other four audit fixes net to almost nothing.
- **Bund.** The brief's own cross-check of **3.50% on 9 Oct 2026** (thetrading.tools) gives SELL. The 3.45% is from an aggregator (audit finding 2).
- **Credit spread.** 0.70% is the US-dollar single-A index (FRED BAMLC0A3CA) added to a euro Bund (audit finding 8). A 1.0% spread gives SELL.
- **Beta.** Damodaran's 2020-24 average cash-corrected Household Products unlevered beta, **0.8752** (same betaGlobal.xls), relevered at D/E 0.1924, gives **0.9998** (risk/notes.md). Unilever's own 5-year monthly regression gives 0.91. On 30 Jun 2026 net debt (2.27x, against the "around 2x" target), the bottom-up beta would be 0.898, above the 0.892 breakeven (risk/notes.md; audit finding 9 put this at +13p because it also moves the debt weight).
- **JVs in the bear:** 229 x 1.016 / (Ke - 1.6%). At Ke 7.164% + 1 point = 8.164%, the value falls from EUR 4,181.2m to **EUR 3,544.3m**.

| Test | Value | Impact | Rating |
|---|---|---|---|
| **ERP 5.0% (Kroll)**, JVs at Ke 7.872% | 3,854.1p | **-404.4p** | **SELL (-18.2%)**, was HOLD |
| ERP 5.5% (Fernandez 2025 survey), JVs at Ke 8.314% | 3,642.4p | -616.1p | SELL (-22.7%) |
| **Bund 3.50% (9 Oct 2026)**; Ke, cost of debt and JVs all move | 4,222.4p | **-36.1p** | **SELL (-10.4%)**, was HOLD |
| **Credit spread 1.0%** (cost of debt 4.45%) | 4,231.8p | **-26.8p** | **SELL (-10.2%)**, was HOLD |
| Beta 0.9998 (Damodaran 2020-24 average); JVs at the new Ke | 3,971.9p | **-286.7p** | **SELL (-15.7%)**, was HOLD |
| Beta 0.91 (own 5y monthly), JVs consistent | 4,191.0p | -67.6p | **SELL (-11.0%)** |
| **Required test 5:** engine bear (0.2% growth, WACC +1 pt) with the JVs at Ke + 1 pt | **3,449.2p** | **-26.4p vs the engine bear of 3,475.6p** (not vs the base) | SELL (-26.8%) |

**Value impact: -26.8p to -404.4p from sourced alternatives (spread, Bund, ERP); -286.7p (beta 0.9998); -26.4p (JV fix to the engine bear, measured against the bear).**

---

## Stacked bear (deal closes; bear margin 16.2%, brief `bear_agent_margin`)
| Stack (one engine run each) | Value | vs base 4,258.5p | Rating |
|---|---|---|---|
| Engine bear (FY26 +2.0%, then 0.2%; WACC +1 pt to 7.50%) + JVs at bear Ke 8.164% (EUR 3,544.3m) + margin 16.2% + 25% Foods-cash tax (EUR 3,507m) | **3,051.0p** | -1,207.6p (-424.6p vs the engine bear) | SELL (-35.2%) |
| The same + HUL at market (EUR 15,507m; other minorities proportionate) | **2,694.9p** | -1,563.6p | SELL (-42.8%) |

14 Oct values, superseded: 2,817p and 2,437p. The tests interact through EV and minorities, so they do not simply add.

## Audit stress lines (15 Oct 2026; each one change vs the base, engine re-run)
| Stress | Value | Impact | Rating | Source |
|---|---|---|---|---|
| ERP 5.0% (Kroll), JVs consistent | 3,854.1p | -404.4p | **SELL** (-18.2%) | erp-evidence.md 2b (secondhand) |
| ERP 5.5% (Fernandez 2025, US), JVs consistent | 3,642.4p | -616.1p | **SELL** (-22.7%) | erp-evidence.md 2c (secondhand) |
| Bund 3.50% (9 Oct 2026), JVs consistent | 4,222.4p | -36.1p | **SELL** (-10.4%) | thetrading.tools (brief comment) |
| Credit spread 1.0% | 4,231.8p | -26.8p | **SELL** (-10.2%) | audit finding 8 |
| Foods cash part (EUR 14,026.6m) discounted to 30 Jun 2027 (0.71 years) at the pre-tax cost of debt 4.15%: EUR 398.9m | 4,242.9p | -15.7p | HOLD (-9.9%), 3.5p above the line | Valuation notes (a) |
| Whole Foods consideration (EUR 33,312.4m) discounted to 30 Jun 2027 at WACC 6.50%: EUR 1,456.7m (upper bound) | 4,201.3p | -57.2p | **SELL** (-10.8%) | Valuation notes (a) |
| McCormick dividends 2 quarters, not 3 (EUR 428.6m, not 642.9m; closing before the July 2027 ex-date) **(upside)** | 4,267.0p | +8.4p | HOLD (-9.4%) | apply_audit_fixes_2026-10-15.py FLAG |

**Which Foods discount is right.** Discounting the cash part at the cost of debt is the cleaner test. The McCormick shares are priced at market, and the missed dividends are already deducted; discounting the share part again at WACC would partly double-count. So the honest Foods-timing impact is **-15.7p, which alone leaves HOLD**. The upper bound of -57.2p gives SELL.

**Correction to valuation/notes.md:** it says the -16p cash discount "would make it SELL". The engine re-run gives 4,242.9p, HOLD by 3.5p. It is SELL only when combined with almost any other item.

## PM responses to the bear (14 Oct 2026, "accept all five"): do they still hold at the 15 Oct base?
The responses are from docs/phase5/ulvr-bear-responses.md, agreed as brief decision 13. I have not changed them; the last column is my assessment.

| Challenge | PM response (14 Oct 2026) | Still holds at 4,258.5p HOLD? |
|---|---|---|
| 1. Foods consideration worth less | Accepted as a risk, not a base-case change. Tax left out (39p per EUR 1bn shown); tax stress -138p and McCormick -1 s.d. -201p "both stay SELL"; a failed deal is "roughly neutral". | **No.** The policy (show the risk, do not deduct) is unchanged, but the conclusion has reversed. Tax -137.7p and McCormick -201.4p now each **turn HOLD into SELL**, and any tax above about EUR 0.49bn does so. A failed deal is no longer neutral: it is **+115p to +151p (HOLD)**. |
| 2. 17.7% margin is a peak | Keep 17.7%; "even at 16.2% the rating stays SELL". | **No.** 16.2% gives 3,932.2p, **SELL vs a HOLD base**: the rating now depends on the margin. The breakeven is 17.61%, only 0.09 points below the base. The argument for 17.7% over 16.2% stands, but the cushion behind it has gone. |
| 3. HUL minorities at market | Keep proportionate (the Diageo rule); market value "shown as the bear line and stays SELL". | **No.** The method choice is defensible, but it now decides the rating: HUL at market gives **SELL** (-171.4p to -261.2p) against the HOLD base. |
| 4. Growth and terminal value | Partly accepted; 1.6% at the top of 1.1-1.6%, TV 75.7% flagged; RONIC = WACC extreme, low bound 16.5% -20p; "both stay SELL". | **No.** TV is now 77.9% of EV. Terminal growth 1.1% gives **SELL** (-221.1p). Even the 16.5% RONIC low bound, which the response used to dismiss the point, now gives **SELL** (4,235.0p, -23.6p). |
| 5. Discount rate | Keep beta 0.8844 (latest Damodaran); 0.9998 is older evidence; "SELL either way"; the larger risk runs the other way (beta 0.748 reaches HOLD). | **No.** The evidence choice for 0.8844 still holds, but "SELL either way" does not. Beta 0.9998 and 0.91 both give **SELL** against the HOLD base, and the breakeven is 0.892. The upside risk is now BUY: beta 0.54 gives 5,486.2p (+16.5%) at WACC 5.29%, below the desk's 6-9% range. |
| Overall view | "Every sourced bear test stays SELL, so the bear case strengthens the call." | **No, reversed.** Every challenge now **moves the HOLD to SELL**. The bear case now argues against the HOLD instead of confirming a SELL. |

## Risks to the bear view (what argues for HOLD or better), each re-run through the engine
HOLD -> SELL breakevens from the Valuation notes, checked here by engine re-run. Each lands on the line (4,238.2-4,239.4p against 4,239.45p), which confirms the scratch method:
- beta 0.892: 4,238.2p
- margin 17.61%: 4,239.0p
- McCormick USD 43.55: 4,239.4p

| Risk to the bear | Value | Impact | Rating |
|---|---|---|---|
| **Beta 0.54** (own 5y weekly vs FTSE 100; JVs consistent; WACC 5.29%, below the 6-9% range) | **5,486.2p** | +1,227.7p | **BUY (+16.5%)**, was HOLD |
| Margin 18.8% (restructuring treated as one-off) | 4,497.9p | +239.3p | HOLD (-4.5%), was SELL |
| Margin 18.2% (18.8% less management's 0.6% guide) | 4,367.3p | +108.8p | HOLD (-7.3%), was SELL |
| McCormick back to the USD 57.84 deal reference (dividend deduction kept) | 4,490.0p | +231.4p | HOLD (-4.7%), was SELL |
| The deal fails (with the USD 420m fee) | 4,409.0p | +150.5p | HOLD (-6.4%), was SELL |
| McCormick dividends 2 quarters | 4,267.0p | +8.4p | HOLD |
| Foods' cash flows from 1 Jan 2026 to closing belong to Unilever (MISSING; Data agent indicator about EUR 2.9bn) | about +113p (indicator only, not run) | | HOLD |

Nothing sourced reaches BUY except Unilever's noisy own weekly beta (R-squared 0.08-0.30, risk/notes.md).

## Management track record: guidance vs outcome (unchanged from 14 Oct; still valid)
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
| FY26 | 4-6% range, "bottom end" (FY25 6-K 0001654954-26-001155); upgraded in July: H2 4-5% (H1 2026 6-K) | H1 USG 4.8%; HPC reported turnover +2.0% in euros (the base's FY26) | On track; the euro figure is H1 only |
| Restructuring | 2022 "around EUR 1.4bn", then "around 1% of turnover" (FY21 6-K) | FY23-25: 0.8%, 1.4%, 1.2% (average 1.1%); FY26 guide "around 1.0%" (H1 2026 6-K) | Roughly met at 1%. The **new 0.6% guide** (31 Mar 2026 call) has never been reached in ten years (lowest 0.8%) |

**Reading.** One-year guides are usually met, because they are qualitative or wide ranges. The **multi-year promises** are the weak spot:
- the 20% margin by 2020 was missed;
- the USG range was missed three years running (FY18-20);
- restructuring has never fallen below 0.8% of turnover.

The Foods deal and the HOLD both rest on that kind of promise: "no margin dilution" from EUR 400-500m of stranded costs, and synergies that "fully offset" an undisclosed tax. The HOLD now survives a margin miss of only 0.09 points.

---

**Strongest reason not to buy:** at 4,710.5p the HOLD survives by just 19.1p (0.4% of the price), and only at the lowest ERP we found (4.2%, seen secondhand). Each of the five bear challenges turns it into a SELL on its own: Foods tax -138p, McCormick volatility -201p, HUL at market -171p, the 16.2% margin -326p, terminal growth 1.1% -221p. So does each of Kroll's ERP, the 9 Oct Bund, a 1.0% spread and the bear's own RONIC low bound. The price still pays 14.7x EBITDA for the business that remains (peer median 11.9x).
