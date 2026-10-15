# Unilever (ULVR): evidence audit of the 14 Oct 2026 run, done 15 Oct 2026

**Verdict: mostly yes, with one gap that matters.** Every number has a source, and I re-checked 38 of them against the primary documents with no errors found. The gap is the discount rate. The equity risk premium (ERP, 5.0%) has no source anywhere, and the risk-free rate (3.45%) can only be found on data-aggregator websites.
**The rating depends on the ERP.** The SELL (3,855p vs 4,710.5p, -18.2%) flips to HOLD at an ERP of 4.23%. A search result (not checked at the source) puts Damodaran's January 2026 market ERP at exactly 4.23%. Every other finding moves the value by less than 60p and leaves SELL in place.
**Findings: 18.** 9 change the value (1 of them can change the rating), 5 are misleading, 4 are cosmetic.
**My corrections taken together (FX, leverage, McCormick dividends, minorities, FY26 growth): 3,915p (+60p), still SELL.** The share price is 4,876p this morning (15 Oct, early trading), so upside is -20.9% and the rating is still SELL.
**Not verifiable from here:** the 3.45% Bund yield (the Bundesbank, ECB, Trading Economics and Damodaran sites are all blocked) and the 5.0% ERP. Nothing else was left unchecked that affects the value.

Scope: briefs/ULVR.yaml; runs/ULVR/2026-10-14/ (inputs.yaml, all agent notes, valuation.json, memo.md); docs/phase5/brief-unilever.md and ulvr-*.md; run-2026-10-14-ulvr/results.md; mistakes-log.md. Read-only: I changed no repo file. Every pence impact below comes from re-running the desk's own engine (`desk.valuation_run.build`, `desk.dcf`, `desk.rating`) in memory, with the JV value re-computed whenever the cost of equity moves. The harness reproduces the desk's own figures exactly: risk-free 3.18% gives 4,018p and 3.50% gives 3,827p, the same as the evidence audit. Pence (GBp) per share; money in EUR m unless labelled.

---

## 1. Findings, ranked (impact on value per share vs 3,855p)

| # | Item | Value used | Source given | Status | Evidence (what I found) | Impact | Severity |
|---|---|---|---|---|---|---|---|
| 1 | **Equity risk premium** | 5.0% | None. "Agreed at sign-off" (brief item I, decision 8). The Diageo brief said "State the source"; it never was, for any company | **unsourced** | No document or justification in the yaml, the brief or the evidence packs. A web search result (not checked at the source; Damodaran's site is blocked) gives Damodaran's Jan 2026 implied US ERP as **4.23%**. A higher ERP could be argued because 62% of the remaining company's sales are in emerging markets (Form 425, slide 17), but nobody has made that argument | ERP 4.5%: 4,094p (+239p). 5.5%: 3,647p (-209p). 6.0%: 3,463p (-393p). **HOLD starts at an ERP of 4.23%.** | **Changes value; can change the rating** |
| 2 | Risk-free (German 10-year Bund on the run date) | 3.45% | Trading Economics / Bloomberg page (aggregator); cross-check 3.50% on 9 Oct (thetrading.tools). Flagged by the PM (decision 11) | sourced, not verified | My web search and fetch attempts failed (sites blocked). FRED's OECD monthly series is rising (Jun 2.96%, Jul 3.07%, Aug 3.18%), so 3.45% in October is plausible. Disclosed in the memo | 3.18%: 4,018p (+163p). 3.50%: 3,827p (-28p). Stays SELL | Changes value (disclosed) |
| 3 | FY26 revenue growth | +0.5% | H1 2026 6-K: Group turnover +0.5% | sourced, verified, **but the wrong perimeter** | The +0.5% is the **whole Group, including Foods, which fell 4.0%**. The DCF excludes Foods. The three HPC business groups grew **+2.0% reported in euros** in H1 2026 (B&W +0.3% to EUR 6.5bn, Personal Care +4.2% to EUR 6.8bn, Home Care +1.5% to EUR 6.0bn; H1 2026 6-K key figures). This is the same mismatch between growth and base year as mistakes-log row 16 | FY26 at +2.0%: 3,909p (**+54p**). Stays SELL | Changes value |
| 4 | McCormick dividends before closing | listed as MISSING | n/a | quantifiable from a filing | McCormick pays **USD 0.48 a quarter** (10-Q to 31 Aug 2026, income statement). The new McCormick shares are issued only at closing (mid-2027), so today's MKC price includes 2-3 dividends that Unilever and its holders will not receive | Two dividends: EUR 429m, **-17p**. Three: **-25p** | Changes value |
| 5 | Tax on the USD 15.7bn Foods cash | not deducted | PM decision 5. CFO: "premature to start making estimates" (Form 425, call transcript) | MISSING (disclosed) | Correctly stated as missing in the memo, at 39.3p per EUR 1bn | 25% stress: -138p (bear agent). Stays SELL | Changes value (disclosed) |
| 6 | Pension | 0 (net surplus EUR 3,518m) | 20-F note 4B; brief rule "0 if surplus" | verified figure; **the rule is weak** | The surplus is netted against **EUR 944m of plans in deficit (unfunded 844 + funded deficit 100, 20-F p.131)**. A surplus in one plan cannot normally pay the deficit of an unfunded plan. The memo does not mention this | Deduct 944 after 26% tax relief: **-29p**. Before tax: -39p | Changes value |
| 7 | Minorities' share of value | 10.684% (FY24 profit share) | Fundamentals agent; 20-F p.128/42/43, note 15B | sourced; partly verified | NCI profit 609 (XBRL) and underlying profit 6,816 (20-F) match. FY24 was chosen as "most cautious"; FY25 gives 10.39%, H1 2026 gives 9.46%. The agent itself says the method slightly overstates the share | FY25: +11p. H1 2026: +47p. Stays SELL | Changes value (judgement, disclosed) |
| 8 | Credit spread on the cost of debt | 0.70% | FRED BAMLC0A3CA, 12 Oct 2026 | verified (0.70% on 12 and 13 Oct) | This is the **US-dollar** single-A spread, added to a **euro** Bund yield. The currency rule (mistakes row 20) is not applied to the spread. No euro single-A series was reachable | Spread 1.0%: **-21p** | Changes value (small) |
| 9 | Leverage date in beta and WACC | net debt EUR 23,076m (31 Dec 2025) vs market cap at 13 Oct | Risk agent | verified; disclosed (Risk FLAG 2) | 30 Jun 2026 net debt is EUR 26.0bn (H1 2026 6-K, verified). That gives beta 0.8981 and a debt weight of 17.79% | **+13p** | Changes value (small) |
| 10 | Margin history in the memo | "18.4%, 16.1%, 17.6%, 19.4%, 20.0%" | ratios.csv | verified, **bases mixed** | FY21-22 are the Group including Ice Cream; FY23-25 are without Ice Cream (FY22 16.1% verified in the FY22 6-K). The memo does not say so, so the series appears to show a smoother recovery than like-for-like figures would | none | Misleading |
| 11 | Memo bear table, challenge 5 | "3,191p (-21p)" | bear/notes.md | traced | The table heading says "impact vs 3,855p", but -21p is measured against the bear case (3,212p) | none | Misleading |
| 12 | docs/phase5/brief-unilever.md | McCormick USD 44.44, EUR 33.8bn, c.1,327p, "28% of the price"; Bund 3.18% in the item I table | brief draft 13 Oct | **wrong (stale)** | The run uses **USD 44.64** (Yahoo close 13 Oct, verified), EUR 33,955m and 1,334p. The Bund was changed to 3.45% by decision 11 | none on the value | Misleading |
| 13 | Superseded tables left in agent files | data/notes.md section 4 (capex 2.8%, risk-free 3.18%, associates 2,044, working capital -7.82%); risk/notes.md body (cost of equity 7.60%); beta_evidence.json | agent notes | stale | Headers say they are superseded, but the tables still show old inputs. A reader checking one table gets the wrong number | none | Misleading |
| 14 | memo_check | "All memo numbers trace" | desk/memo_check.py | passes, but weak | I re-ran it and it passes. However, it matches a number found **anywhere** in the run folder, as the editor's FLAG 4 says. I traced the key numbers by hand (section 3) | none | Misleading (as a control) |
| 15 | EUR per GBP and EUR per USD | 1.18190; 1.1193 | FRED, 9 Oct 2026 | verified | Prices are 13 Oct closes but FX is 9 Oct. Yahoo on 13 Oct: 1.18373 EUR per GBP and 1.1160 USD per EUR. Disclosed | Both FX rates at 13 Oct: **-2p** | Cosmetic |
| 16 | Date label on the Yahoo FX check | "EURGBP=X 2026-10-12" (inputs.yaml) vs "13 Oct" (data notes) | Yahoo | verified | Yahoo stamps the 13 Oct London session at 12 Oct 23:00 UTC. Both labels refer to the same rate | none | Cosmetic |
| 17 | Editor notes | "PM review pending", "PM to respond" | editor/notes.md | stale | The memo and results.md say "PM confirmed SELL 14 Oct" and contain the PM view (decisions 12 and 13). The notes were not updated | none | Cosmetic |
| 18 | Tax justification wording | "FY25's 25.7% was helped by one-off settlements" | brief yaml | partly contradicted | The FY25 6-K says FY25 had *lower* settlement benefits than FY24. The H1 2026 6-K says the 2026 rate rose because of *lower* benefits than in 2025. The 26.0% itself is verified (H1 2026 actual and "remains around 26%") | none | Cosmetic |

**Stale data since the run (information, not an error):** ULVR is 4,876p on 15 Oct (early trading), +3.5% on the 4,710.5p used. MICC.AS is EUR 16.53 (+EUR 75m, about +3p) and MKC USD 44.80 (about +3p). At 4,876p the upside is -20.9% and the rating is still SELL; HOLD would start at 4,388p.

---

## 2. Every assumption in briefs/ULVR.yaml: source and justification

| Assumption | Value | Source cited | Justification stated | Audit status |
|---|---|---|---|---|
| Base sales ex-perimeter | EUR 39,803m | FY25 6-K 50,503 less Form 425 slide 25 EUR 10.7bn | Decision 1 | **verified** (both figures). The perimeter is rounded to EUR 0.1bn |
| Ex-perimeter UOP / margin | EUR 7,484m / 18.8% | 6-K 10,084 less Form 425 EUR 2.6bn | Decision 1 | **verified**. Management's own pro forma is ">19%" on a slightly different perimeter (Foods excluding India Foods), consistent |
| Growth FY26 | +0.5% | H1 2026 6-K | Decision 2 | verified figure, **wrong perimeter** (finding 3) |
| Growth FY27-30 | 1.6% | 4% low end of USG range less 2.4-pt FY17-25 currency drag; ulvr-growth-evidence.md | Decision 2 | sourced; a cautious judgement. The deal deck guides "mid-single digit" USG for the HPC company. The currency drag is a Group average including Foods |
| Savings | none | n/a | Margin held flat instead | OK (stated) |
| Margin | 17.7% | 18.8% less FY23-25 restructuring 1.12% (XBRL 425/710/599 on 51,680/52,479/50,503) | Decision 3; 0.6% guide never achieved | **verified** (XBRL). H1 2026 guides FY26 restructuring "around 1.0% of turnover" (verified) |
| Tax | 26.0% | H1 2026 ETR 26.0%; "around 26%" guide | Decision 9 | **verified** (wording, finding 18) |
| Capex | 3.15% | XBRL PP&E 1,417 + intangibles 174 / 50,503 | Decision 10 | **verified** |
| D&A | 2.6% | XBRL 1,310 / 50,503 | Sign-off | **verified** |
| Working capital | -11.98% | XBRL inventories 4,043, receivables 7,346, payables 16,939; notes 13-14 (2.1bn / 1.6bn) | Decision 10, item D | **verified** (all five figures, including the note wording) |
| Terminal growth | 1.6% | Matches FY27-30 | Decision 6 | sourced judgement; at the top of the Data agent's 1.1-1.6% range |
| Terminal RONIC | 17.8% | FY25 6-K ROIC: (10,084-599) x 0.74 / 39,502 | Sign-off; ex-Foods ROIC MISSING (flagged) | **verified** (39,502 and the formula) |
| Mid-year / valuation basis | mid-year; 31 Dec 2025 rolled forward | H1 FCF 19% of the year | Sign-off | sourced |
| Risk-free | 3.45% | Aggregator | Decision 11 | sourced, **not verified** (finding 2) |
| **ERP** | **5.0%** | **none** | **none** | **unsourced** (finding 1) |
| Beta | 0.8844 | Damodaran betaGlobal.xls, Household Products 0.774144 (588 firms, 5 Jan 2026), relevered at D/E 0.1924, tax 26% | PM rule | **verified** (I read the file myself; the Hamada relevering checks) |
| Credit spread | 0.70% | FRED BAMLC0A3CA | A+/A1 rating | verified figure; the 20-F says "strong single A", but I did not find the exact A+/A1 wording; USD index (finding 8) |
| Debt weight | 16.13% | Dec net debt / market cap on 13 Oct | Market values | verified inputs; mixed dates (finding 9) |
| Net debt | EUR 23,076m, leases 1,326 inside | FY25 6-K reconciliation; 20-F note 15C | Brief | **verified** (both) |
| Minorities | proportionate 10.684% | 20-F p.128/42/43, note 15B | Decision 4 | partly verified (finding 7) |
| Pension | 0 | Net surplus 3,518 (note 4B) | Brief rule | figure **verified**; rule weak (finding 6) |
| TMICC stake | 121,604,413 x EUR 15.914 = EUR 1,935m | TMICC 424(b)(4); Yahoo MICC.AS 13 Oct | Item E | **verified** (both) |
| JVs | 229 x 1.016 / (Ke - 1.6%) = EUR 3,710m | 20-F note 11 | Decision 10, item B | **verified** (229 in note 11). Valuing dividends as a growing perpetuity is a judgement |
| Other investments | EUR 902m | 20-F note 17A (561 + 341) | Item C | sourced, not verified line by line |
| Magnum net balance | EUR 500m | 20-F notes 13-14 | Item D | **verified** |
| Foods consideration | EUR 33,955m | USD 15.7bn + 269,064,479 x 65/35 MKC shares x USD 44.64 / 1.1193 | Decision 1 | **verified**: share count, 55.1%/9.9%, USD 15.7bn, MKC close and FRED FX. Diluted MKC shares add only 0.1m (immaterial). The MKC dividend leakage is unsized (finding 4) |
| Stranded-cost restructuring | EUR 500m | Form 425 slide 19 | Decision 3 | **verified** |
| Buyback deducted | EUR 1,507m | H1 2026 6-K | Mistakes row 22 | **verified** ("€1.5 billion share buyback ... completed" in June) |
| Dividends deducted | EUR 3,038.8m | H1 equity statement 2,034 + Q2 EUR 0.4664 x shares | Roll-forward | **verified** (2,034 and 0.4664) |
| Shares | 2,154,327,621 | TVR 6-K 1 Sep 2026 | Latest | **verified**. EDGAR still shows no later TVR on 15 Oct. The July-August count was flat, so no buyback is missing |
| Share price | 4,710.5p | Yahoo ULVR.L 13 Oct | Last close | **verified** |
| Bear: growth 0.2%, margin 16.2%, WACC +1 pt | | Growth evidence (FY17-25 excluding FY22); 2023 c.17.3% less 1.1% | Decisions 2, 3 | sourced; 17.3% is the desk's own inference from "+170bps" (Form 425, verified) |
| Rating rule | +15% / -10% | Portfolio rule | Policy | OK |
| Comps peers | 7 HPC peers | SEC XBRL (3) and Yahoo (4) | Flagged | sourced; cross-check only |

**No assumption has a contradictory source.** One has no source at all (ERP). One cannot be checked against a primary source (risk-free). One uses a figure for the wrong perimeter (FY26 growth). One relies on a rule that nets a surplus against unfunded deficits (pension).

---

## 3. Memo numbers traced (memo → agent file → source)

| Memo number | Agent file | Primary source | Status |
|---|---|---|---|
| SELL, 3,855p, -18.2%, bear 3,212p | valuation.json (3,855.29; -0.18155; 3,211.93) | engine | **match** |
| HOLD at 4,239p, BUY at 5,417p | 4,710.5 x 0.90 / x 1.15 | brief rating rule | match |
| EV 91,140; minorities 9,737; equity 98,844 / 98,163; EUR 45.57 | valuation.json | engine | match |
| WACC 7.10%, Ke 7.872%, Kd 4.15%, debt weight 16.13%, beta 0.8844 | valuation.json | as above | match |
| Sensitivity grid and football ranges | valuation.json grid | engine | match |
| Foods 1,334p, net debt -962p, minorities -406p | valuation/notes.md (d) | 33,955 / 2,154.3m / 1.1819 | match |
| McCormick USD 44.64, USD 57.84, -23% | inputs.yaml; brief | Yahoo (verified); 57.84 is the deal reference in the brief, not a filing I checked | match (57.84 sourced, not verified) |
| 14.7x, 11.9x, 10.9x, comps 3,166 / 3,911 / 6,541p | comps.json, valuation notes | SEC XBRL + Yahoo | traced; peer data not re-checked |
| USG 4.5 / 9.0 / 7.0 / 4.2 / 3.5% | growth evidence pack | results 6-Ks (FY25 3.5% verified) | traced |
| Margins 18.4 / 16.1 / 17.6 / 19.4 / 20.0% | ratios.csv | FY22 16.1% and FY24-25 verified | traced; bases mixed (finding 10) |
| Segment margins 22.6 / 19.2 / 14.9%; perimeter 24.3%; remaining 18.8% | segments.csv | FY25 6-K note 2 (2,973/13,161 etc.) | match |
| 62% emerging markets | brief | Form 425 slide 17 | **verified** |
| Leverage 2.03x / 2.27x; A+/A1 | risk/notes.md | 6-K "2.3x" verified | match |
| Volatility 22.4% / 19.2% / 30.5%; drawdown -25.5% | risk.json, bear notes | Yahoo prices | traced, not re-computed |
| Own betas 0.43 / 0.54 / 0.91 | risk.json | Yahoo regressions | traced |
| Bear tests (-138p, -201p, -290p, -224p / -301p, -166p, -383p, -267p, 2,817p, 2,437p) | bear_results.json, challenges.md | engine re-runs | traced; "-21p" mislabelled (finding 11) |
| -86.5p engine fix, 16p to 70p timing, 113p interim cash | valuation/notes.md, data notes | engine / Data agent's own indicator (labelled) | traced |

**Untraced numbers: none.** Every memo figure appears in an agent output with a source behind it.

**Consistency checks:**
- **Memo vs valuation.json:** value and rating agree.
- **Currency labels:** present on every number checked.
- **Open FLAGs and MISSING items:**
  - Foods tax, Foods interim cash flows and a primary Bund source are all shown in the memo.
  - McCormick dividends and ex-Foods ROIC are listed as missing in agent notes. The McCormick dividends can be sized from the 10-Q (finding 4).
  - The terminal value is 75.7% of EV, just over the 75% flag (disclosed).
- **Stale data not disclosed:** none in the memo itself. The stale files are the brief document and agent notes (findings 12, 13, 17).

---

## 4. What I verified against primary sources (38 checks, 0 wrong)

- **SEC EDGAR, Unilever FY25 20-F XBRL:**
  - Revenue 51,680 / 52,479 / 50,503 and restructuring 425 / 710 / 599
  - Capex: PP&E 1,417, intangibles 174 (FY24 1,381 / 233)
  - D&A 1,310; inventories 4,043; receivables 7,346; payables 16,939
  - Minorities: NCI book 2,057; NCI continuing profit FY24 609
- **SEC EDGAR, Unilever FY25 20-F text:**
  - Note 11: JV dividends 229
  - Notes 13-14: EUR 2.1bn due from TMICC and EUR 1.6bn due to it
  - Note 15C: lease liabilities 1,326 inside 28,278
  - Pension surplus 3,518; HUL 61.90%
  - Underlying profit 6,816; "strong single A" rating
- **SEC EDGAR, FY25 results 6-K:**
  - Turnover 50,503; UOP 10,084; net debt 23,076
  - Average invested capital 39,502; underlying ETR 25.7%; USG 3.5%
- **SEC EDGAR, H1 2026 6-K:**
  - Turnover +0.5% and business-group turnover; underlying ETR 26.0%; "remains around 26%"
  - Restructuring "around 1.0%"; buyback 1,507 (completed June)
  - Dividends 2,034 and EUR 0.4664; net debt EUR 26.0bn
- **SEC EDGAR, other filings:**
  - Form 425: EUR 10.7bn / EUR 2.6bn / 24%; EUR 500m restructuring 2027-29; USD 15.7bn; 55.1% / 9.9%; 62% EM; "€39bn ... UOM >19%"
  - McCormick 10-Q: 14,522,864 + 254,541,615 shares; 55.1 / 35.0 / 9.9%; USD 15.7bn; USD 420m termination fee; USD 0.48 quarterly dividend
  - TMICC 424(b)(4): 121,604,413 shares
  - TVR 6-K: 2,154,327,621 shares
  - FY22 6-K: underlying margin 16.1%
- **Yahoo Finance (13 Oct closes):** ULVR.L 4,710.5p; MKC USD 44.64; MICC.AS EUR 15.914; HINDUNILVR.NS INR 1,875.5; EURGBP 0.84479; EURUSD 1.1160.
- **FRED:**
  - DEXUSUK 1.3229 and DEXUSEU 1.1193 (9 Oct), giving EUR 1.18190 per GBP
  - BAMLC0A3CA 0.70% (12 and 13 Oct)
  - IRLTLT01DEM156N 3.18% (Aug 2026)
- **Damodaran file (PM upload):** Household Products, 588 firms, unlevered beta corrected for cash 0.774144, dated 5 Jan 2026.

**Could not verify:**
- the Bund at 3.45% (all daily sources blocked)
- the ERP (Damodaran site blocked; search snippet only)
- note 17A's 561 + 341 line by line
- the exact "A+/A1" wording
- the USD 57.84 deal reference price
- Yahoo-sourced peer data and HUL's share count (bear line only)

## 5. Recommendations for the PM (nothing changed)
1. Set the ERP with a cited source and a stated reason (for example, Damodaran's mature-market ERP plus or minus a country-risk adjustment for 62% emerging-market sales). It is the only input that, on its own and from a citable source, can move ULVR from SELL to HOLD. The same unsourced 5.0% is used for Diageo, KO and RELX.
2. Re-base FY26 growth on the remaining HPC business (+2.0% reported in H1 2026) rather than the Group's +0.5% (+54p).
3. Size the McCormick dividend leakage (-17p to -25p) and decide on unfunded pension plans (-29p after tax) instead of leaving them as "missing" or netted.
4. Clean up the stale tables (brief-unilever.md section 3 and item A, data notes section 4, risk notes, editor notes) and label the bases in the memo's margin history.
