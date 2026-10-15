# Evidence audit: Diageo (DGE), final memo HOLD 1,627p

Auditor: Claude (read-only audit, 15 Oct 2026). Nothing in the repo was changed. All pence figures are GBp per ordinary share; company money is USD m.

## Summary
1. **Verdict: the HOLD holds up.** Almost every number traces to a filing, a market data series or a recorded PM decision. About 30 inputs and memo numbers were checked against primary sources and matched (table A). No finding on its own moves the value from HOLD to SELL or BUY.
2. **Findings: 20 in total.** 9 change the value but not the rating. 4 are misleading. 7 are cosmetic. Separately, 6 known MISSING items are still open.
3. **Biggest gap: the equity risk premium (ERP) of 5.0% has no source.** The brief says "state the source", and none is given. Each 0.5 point of ERP moves the value by about 100-110p. SELL starts above 5.62% and BUY below 3.77%. Damodaran's Jan 2026 implied US ERP of 4.23% (secondhand) would give **1,803p (+176p, still HOLD)**.
4. **Next weakest: the long-run assumptions.** Growth of 3% in FY30-31 has no source, and the desk's own IWSR evidence argues against it (2% gives -27p). Terminal growth of 2% is a PM judgement (1.5% gives -56p). Disposal proceeds are gross, but the brief asks for net (about -3.5p per USD 100m of tax).
5. **Consistency is clean.** Memo = valuation.json = PDF = results.md (1,627.26p, HOLD, -2.7%). But the memo uses the 12 Oct price (1,673p) although it is dated 13 Oct (close 1,712.5p, so upside -5.0%, still HOLD). Since 15 Oct the shares trade without the 30c (22.6p) dividend.

Impacts below are one change at a time, computed with `desk.valuation_run.build` from the run's own inputs. They are not added together. Base 1,627.3p; SELL line 1,505.7p; BUY line 1,923.95p.

---

## A. Spot-checks against primary sources (value-sensitive inputs)

| Item | Value used | Source given | Status | Evidence (what I checked) | Impact |
|---|---|---|---|---|---|
| Net sales FY26 | USD 19,643m | 20-F FY26 | **verified** | 20-F FY26 (acc. 0001628280-26-057529) text: "Reported net sales ... $19,643 million" | none |
| Base sales ex-EABL | USD 18,505.5m | 20-F less EABL KES 145.96bn / 128.32 | **sourced-not-verified (EABL part)** | 19,643 verified. KES 128.32 = Yahoo KES=X FY26 average (recomputed: 128.32). EABL sales "KES 146.0bn" seen only via an aggregator (africanfinancials.com). The EABL annual report was not reachable | none found |
| Operating profit before exceptionals | USD 5,683m | 20-F | **verified** | 20-F ROIC table: 3,156 + 2,527 = 5,683 | none |
| Base margin ex-EABL | 29.358% | 5,683 less EABL EBIT KES 32.1bn | **sourced-not-verified (EABL part)** | Aggregator: EBIT "KES 32.1bn". Data notes cite 32.07bn from EABL's report | +0.1p for 32.07bn |
| Organic growth FY27-29 | 0 / 1.5 / 2.5% | CMD 6-K, 6 Aug 2026 | **verified** | 6-K 0001654954-26-007324: FY27 "broadly flat"; FY27-29 "low-single-digit ... accelerating" | none |
| Organic growth FY30-31 | 3.0% / 3.0% | brief 5a: "roughly the industry's long-run nominal growth" | **unsourced, and contradicted** | No source. The Data agent's own IWSR evidence (secondhand) shows spirits volumes falling about 2% by 2035 and "challenges, rather than supports, the 3%" | **2.0% in FY30-31: 1,600p (-27p)** |
| Savings schedule | USD 377.5 / 962.5 / 1,000m | CMD 6-K | **verified** (except one desk assumption) | 6-K: c.$850m (c.40% FY27, rest FY28) + c.$150m (c.25% FY27). The 75% supply-chain phasing in FY28 is the desk's own assumption, and the brief says so | tiny |
| Flow-through | 46% | Calibrated to the low end of FY27-29 "mid-single-digit" profit growth | **sourced (calibration)** | Guidance wording verified in the 6-K. Note: the 6-K credits "savings **and more favourable mix**", so 46% stands for savings and mix together | 50%: +13p |
| Tax rate | 24.3% | 20-F p.22 | **verified** | 20-F: "tax rate before exceptional items ... 24.3% compared with 24.9%". No forward guidance found in the 20-F or the CMD 6-K | FY25 24.9%: -14p |
| Risk-free | 5.22% (8 Oct) | FRED DGS10 | **verified, but a day old** | FRED: 8 Oct 5.22%, **9 Oct 5.24%**, 12 Oct blank (US holiday), 13 Oct 5.21% | 5.24%: -5.8p; 5.21%: +2.9p |
| Beta | 0.96 | Damodaran global alcoholic beverages, unlevered 0.73 (cash-corrected), relevered at D/E 0.416, tax 24.3% | **sourced-not-verified (site blocked)** | Web search snippet of Damodaran's Jan 2026 global page: 0.69 unlevered, 0.73 cash-corrected, 217 firms. Arithmetic recomputed: 0.9601. Damodaran's industry D/E uses gross debt; the desk relevered with **net** debt | Gross-debt D/E 0.451 gives beta 0.979: **-21p** |
| ERP | 5.0% | none ("within the usual 4.5-5.5% range. State the source.") | **unsourced** | No document or URL anywhere in the brief, inputs or evidence packs. Secondhand: Damodaran implied US ERP 4.23% (Jan 2026), 4.24% (May 2026) | 4.5%: +111p; 5.5%: -100p; 4.23%: **+176p**; SELL above 5.62% |
| Cost of debt | 6.22% (Rf + 1.0%) | PM rule; FRED OAS | **verified** | FRED 8 Oct: A 0.69%, BBB 1.02%, HY 3.15%. 20-F: leverage range "broadly consistent with an A-band credit rating". Historic 812 / 21,336 = 3.81% also verified (20-F net interest table and ROIC table) | 2% spread: -68p (Bear) |
| Debt weight | 29.4% | 20,482 / (20,482 + 2,222m x 1,673p x 1.3234) | **verified inputs** | Each part verified separately. Note: the FX date (2 Oct) differs from the price date (12 Oct) | <1p |
| Net debt | USD 20,482m incl. leases 685 | 20-F note 17 | **verified** | 20-F: borrowings 2,449 + 19,062 - derivatives 194 + leases 685 - cash 1,520 = 20,482 | none |
| Minorities (proportionate) | 2.566% x EV = USD 1,562m | 20-F p.210: NCI 227 less 35% x EABL EBIT 250.2 | **verified (method is a PM judgement)** | 20-F ROIC table: "Profit before exceptional operating items attributable to NCI (227)". Recomputed 2.5667%. Book NCI 2,083 = USL 755 + other 1,328 verified. The NCI note names USL, Shuijingfang and Ketel One but not EABL, so "1,328 includes EABL's 35%" is plausible but not shown | none |
| Associates | USD 5,284m | 20-F associates note | **verified** | 5,107 Moet Hennessy + 177 others = 5,284. The 20-F calls the Moet Hennessy test "sensitive" | none |
| Disposal proceeds | USD 3,318.3m (gross) | 20-F p.85 (EABL c.$2.3bn) + 57.21% x RCB $1.78bn | **verified gross, but brief says NET** | 20-F: "approximately $2.3 billion". Press: RCB INR 16,660 crore = c.$1.78bn (Gulf News, Outlook Business). The brief asks for "net proceeds", but tax and costs are not deducted. RCB's profits also stay in the forecast while its proceeds are added (small, not quantified) | -3.5p per USD 100m of tax; -10.5p at an illustrative USD 300m |
| Restructuring cash | USD 850m (pre-tax) | CMD 6-K | **verified** | 6-K: c.$800m + c.$50m exceptional cash in FY27; "c.$850 million exceptional cash costs" FY27-29. 20-F: $752m charged in FY26, cash out in FY27 | Tax relief at 24.3%: +7.2p (already disclosed) |
| Pension | 0 (net surplus 627) | 20-F XBRL | **verified (rule)** | Adjusted net borrowings table: deficit-plan liabilities 387 | none (brief rule) |
| Shares | 2,222m | 2,432 issued - 208 treasury - 2 trusts | **wrong (small)** | 20-F note 18(c): "Own shares" 208m at 30 June 2026, and the policy defines own shares as shares "held in treasury **or by employee share trusts**". So the 2m trust shares are already inside the 208m and were deducted twice. Cross-checks: weighted shares "excluding own shares" 2,224m. US holders: 270.6m = 12.15% of outstanding, which implies about 2,227m. Dilutive shares +7m are ignored | 2,224m: -1.5p; diluted 2,231m: -6.6p |
| FX | USD 1.3234 / GBP (2 Oct) | FRED DEXUSUK | **verified, 6 trading days old** | FRED 2 Oct 1.3234; 9 Oct 1.3229 (latest before the run) | 9 Oct rate: +0.6p |
| Share price | 1,673p (12 Oct close) | Yahoo DGE.L | **verified** | Yahoo DGE.L (GBp) 12 Oct 1,673.0; 13 Oct 1,712.5; ex-dividend 15 Oct (22.6455p) | 13 Oct price: upside -5.0%, HOLD |
| Dividend ex-date | 15 Oct 2026, 30c (USD 668m) | 20-F | **verified** | 20-F dividend note; Yahoo shows the dividend event on 15 Oct | none |
| Terminal RONIC | 13.4% | 20-F FY26 ROIC | **verified** (FY26, FY25 13.7%) | 20-F ROIC table. FY23 18.4% and FY24 15.8% are not in the FY26 20-F and were not checked | Bear: 10.8% gives -66p |
| Forecast capex | 7.11% of sales (5-year average) | 20-F FY22-26 | **verified arithmetic, but against guidance** | Recomputed 7,193 / 101,228 = 7.106%; FY22 interest and FY26 capex 1,197 checked in XBRL and the 20-F. The 20-F CEO letter says "$3.75 billion of capital expenditure" over 3 years, about 6.63% of the model's FY27-29 sales. The model spends about USD 270m more | 6.63%: +12.8p (conservative today) |
| D&A | 3.38% of sales | 20-F XBRL | **sourced-not-verified** | XBRL tag named; not re-pulled | - |
| Working capital | 37.58% of sales | 20-F balance sheet | **verified figures, mismatched base** | 10,529 + 3,277 - 6,425 verified. The numerator is ex-EABL (held for sale), but the denominator includes EABL's sales | ex-EABL denominator (39.9%): -1.2p |
| Mid-year evidence | H1 FCF 1,532 / 1,696 | interim 6-Ks | **verified** | 6-K 0001654954-26-001518: "Free cash flow $1,532m $(164)m" | none |
| Breakeven inflation | 2.35% (8 Oct) | FRED T10YIE | **verified** | FRED 8 Oct 2.35 | none |
| Leverage | 3.14x | 20-F p.186 | **verified** | 20,869 / 6,650 | none |
| Fundamentals in memo | NA -8.4%, LAC +7.7%, Africa +13.3%, FCF 3,211, EPS 165.3c, FY22 interest USD 469m | 20-F | **verified** | 20-F regional reviews; XBRL InterestRevenueExpense FY22 USD -469m (so 13.6x cover holds) | none |
| Bear inputs for USL at market | INR 1,362.5, INR 95.285 / USD "12 Oct" | Yahoo | **does not match** | Yahoo UNITDSPR.NS closes: 9 Oct 1,366.0, 12 Oct 1,349.7. 95.285 matches a later Yahoo FX bar | Only moves the bear figure 1,480p by a few pence |

## B. Brief assumptions (briefs/DGE.yaml and brief-diageo.md): source and justification

| Assumption | Source cited? | Justification? | Status |
|---|---|---|---|
| ADR ratio 4, CIK, USD reporting, June year end | yes (20-F) | yes | verified (20-F: "one ADR is equivalent to four ordinary shares") |
| Base year 19,643 / 5,683 | prelims URL (in brief md) | yes | verified |
| Growth FY27-29 | CMD 6-K, track record | yes | verified |
| **Growth FY30-31 3%** | **none** | "industry long-run nominal growth" | **unsourced; desk evidence contradicts it** |
| Savings and phasing | CMD 6-K | yes | verified; FY28 supply chain 75% is the desk's own assumption (disclosed) |
| Flow-through 46% | CMD 6-K + evidence file | yes | sourced. **But brief-diageo.md still says 50% "AGREED" (sections 5 and 7, decision 3)**, so the two brief files contradict each other |
| **Terminal growth 2%** | none directly; breakeven 2.35% added later in the bear responses | "below nominal GDP" | **weak** (PM judgement) |
| Terminal RONIC 13.4% | 20-F ROIC | yes | verified. **The yaml comment "if returns fall to c.10.8% ... -> SELL" is stale**: 10.8% now gives 1,562p, a HOLD; SELL is below 9.26% |
| Mid-year convention | interim 6-Ks | yes | verified |
| Valuation basis (30 June, roll forward) | method decision (Codex BRIDGE-01) | yes | fine |
| **ERP 5.0%** | **none** | "usual 4.5-5.5% range" | **unsourced; the most rating-sensitive gap** |
| Beta rule (bottom-up) | Damodaran + own regressions | yes | sourced; relevering basis debatable (net vs gross debt, -21p) |
| Credit spread 1.0% | FRED OAS (added in Phase 4) | yes | verified |
| Minorities method | 20-F + evidence audit | yes | sourced (judgement) |
| Bear scenario (0% growth, 25% flow-through, WACC +1 pt) | brief 5b | partly | 25% has no source (it is a stress test, so acceptable) |
| Peers, multiples | brief | yes | data weak (2 of 4 peers press-sourced, no EV/EBITDA) |
| Rating thresholds +15% / -10% | PM policy | n/a | fine |
| tax_rate note "c.23%" | brief proposal | n/a | superseded by verified 24.3%; the brief md still says c.23% |
| disposal_proceeds "**net** proceeds" | brief | yes | **the input is gross**, which contradicts the brief |
| Brief version | "Any change needs PM approval and a version bump" | - | **brief-diageo.md is still v1.0** after Phase 3/4 changes (46%, RONIC, minorities, restructuring cash) |

## C. Memo numbers: tracing

- `desk.memo_check` passes. I also mapped each memo number to the files that contain it. Every number in the body appears in at least one agent output. Valuation figures (1,627, 60,870, 1,562, 46,579, 47,851, the grid, 1,506 / 1,924, 1.078, 9.1%) come from `valuation/valuation.json` and `sanity_checks.json`. Bear figures come from `bear/challenges.json`. Each of those files traces back to the sourced `inputs.yaml`.
- Weak traces (narrative files only, no data file): ROIC FY23 18.4% (only `bear/challenges.md` and a brief comment; not in the FY26 20-F and not verified by me). Interest cover 13.6x (`fundamentals/commentary.md`; I verified it from ratios.csv and XBRL).
- The checker is loose: it accepts a number found anywhere in the run folder, so it cannot confirm context. The editor flags this too.
- Untraced numbers: **none** found.

## D. Consistency and staleness

| Check | Result |
|---|---|
| Memo vs valuation.json | Match: 1,627.26p, HOLD, upside -2.734%, bear 1,179.9p, EV 60,870, sensitivity grid identical |
| PDF vs repo | `run-2026-10-13-phase4/diageo-memo-phase4.pdf` is byte-identical to `runs/DGE/2026-10-12/editor/memo.pdf` |
| Currency labels | Good overall (pence, USD m). Small gap: the FX rate and risk-free rate appear in the body **without dates**; the dates are only in the Sources appendix (brief trap 1 asks for "a stated FX rate with its date") |
| Stale market data | Risk-free 8 Oct (9 Oct 5.24% existed); FX 2 Oct (10 days before the price date). Neither is stated in the body. Combined effect about -5p |
| Memo date vs price | Memo dated 13 Oct; price 12 Oct (labelled). 13 Oct close 1,712.5p means upside -5.0%. From 15 Oct the shares are ex-dividend (22.6p), so any reuse must compare against an ex-dividend price **and** deduct the dividend in the roll-forward |
| Leverage wording | The memo says "about 2.6x after the disposal proceeds, before tax on them". The Phase 4 evidence pack said to add "and before EABL's EBITDA leaves, so somewhat higher". **That caveat was dropped** |
| Old numbers in notes | Valuation notes still carry Phase 3 text ("market-implied WACC about 8.1%", "SELL if beta above 0.997", 1,545p) below the Phase 4 section. The memo uses the current numbers |
| Open FLAG / MISSING | Still open: peer EV/EBITDA and FCF yield; Constellation EPS; calendarised peers; Moet Hennessy fair value; USL net cash; split of the USD 1,328m other minorities; EABL completion not confirmed in a filing; tax on disposals; IWSR only secondhand. Valuation notes say `python -m pytest` could not run in that session (CLAUDE.md rule 6) |

## E. Findings ranked by severity

| # | Severity | Finding | Impact (one at a time) |
|---|---|---|---|
| 1 | Changes value | ERP 5.0% has no source, although the brief requires one | ±100-111p per 0.5 pt; 4.23% gives 1,803p; SELL > 5.62%, BUY < 3.77% |
| 2 | Changes value | FY30-31 growth 3% is unsourced, and the desk's IWSR evidence contradicts it | 2%: -27p |
| 3 | Changes value | Terminal growth 2% is a PM judgement with only indirect evidence | 1.5%: -56p |
| 4 | Changes value | Beta relevered with net-debt D/E against Damodaran's gross-debt industry basis | -21p |
| 5 | Changes value | Disposal proceeds are gross; the brief asks for net. RCB profit is kept and RCB proceeds are added | -3.5p per USD 100m of tax |
| 6 | Changes value | Tax 24.3% is FY26 actual; no forward rate checked (the mistake-log lesson from row 21) | 24.9%: -14p |
| 7 | Changes value | Forecast capex 7.11% is above the CEO's $3.75bn FY27-29 plan (conservative) | +13p |
| 8 | Changes value | Share count double-deducts 2m trust shares; dilution ignored | -1.5p / -6.6p diluted |
| 9 | Changes value | Risk-free taken from 8 Oct, not 9 Oct | -5.8p |
| 10 | Misleading | brief-diageo.md (v1.0) still says 50% flow-through and tax c.23%; no version bump | none |
| 11 | Misleading | Stale yaml comment: RONIC 10.8% "-> SELL" (it is now HOLD) | none |
| 12 | Misleading | Memo leverage of 2.6x drops the "before EABL's EBITDA leaves" caveat | none |
| 13 | Misleading | Memo dated 13 Oct uses the 12 Oct price; the shares go ex-dividend 15 Oct | upside -2.7% -> -5.0% at 13 Oct close |
| 14 | Cosmetic | FX and risk-free dates missing in the memo body | +0.6p (FX) |
| 15 | Cosmetic | Working capital % uses an ex-EABL numerator over sales that include EABL | -1.2p |
| 16 | Cosmetic | Bear USL price and INR rate don't match the Yahoo closes for the stated date | a few p on the 1,480p bear case |
| 17 | Cosmetic | Drawdown peak 4,098p is dividend-adjusted (actual close 4,103.5p), and the memo does not say so | none |
| 18 | Cosmetic | memo_check matches numbers anywhere; ROIC 18.4% traces only to narrative files | none |
| 19 | Cosmetic | Notes files mix superseded Phase 3 numbers with current ones | none |
| 20 | Cosmetic | FY28 supply-chain phasing (75%) is a desk assumption (disclosed) | under 1p |

Known and already disclosed by the desk: restructuring tax relief +7.2p; EABL EBIT 32.07bn +0.1p.

Together, the small sourced corrections (diluted shares 2,231m, risk-free 5.24%, illustrative USD 300m tax on disposals) give **1,604.5p (-23p), still HOLD**.

## What I could not verify
- Damodaran pages (blocked): the beta 0.73 and the ERP were seen only in search snippets.
- EABL's own annual report (only an aggregator was reachable); IWSR; peer P/Es (Pernod, Campari, Remy); USL share count 727.35m.
- ROIC FY23 18.4% and FY24 15.8% (earlier 20-Fs not pulled).
- Diageo's actual credit rating (the 20-F says only "broadly consistent with an A-band credit rating").
- I did not re-run the beta regressions or the volatility figures (they were computed by desk/risk.py and were already reproduced by the Codex audit).

Sources used: SEC EDGAR 20-F FY26 (0001628280-26-057529), CMD 6-K (0001654954-26-007324), H1 FY26 6-K (0001654954-26-001518), EDGAR companyfacts XBRL; FRED DGS10, DEXUSUK, T10YIE, BAMLC0A3CA, BAMLC0A4CBBB; Yahoo Finance DGE.L, GBPUSD=X, KES=X, INR=X, UNITDSPR.NS; web search: [Damodaran Betas Global](https://pages.stern.nyu.edu/adamodar/New_Home_Page/datafile/BetasGlobal.html), [BV Wire on Damodaran 2026 ERP](https://bvresources.com/articles/bvwire/damodaran-posts-his-first-data-update-for-2026), [africanfinancials EABL 2026](https://africanfinancials.com/document/ke-eabl-2026-ab-00/), [Outlook Business RCB sale](https://www.outlookbusiness.com/corporate/usl-to-sell-rcb-in-16660-cr-deal-to-consortium-of-aditya-birla-gr-times-bolt-blackstone), [Gulf News RCB](https://gulfnews.com/sport/cricket/ipl/royal-challengers-bengaluru-sold-for-178-billion-1.500485300). Scripts: scratchpad `audit/sens.py`, `audit/erp.py` (call desk.valuation_run.build only).
