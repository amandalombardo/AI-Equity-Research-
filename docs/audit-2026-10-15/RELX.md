# RELX PLC (REL.L): evidence audit, 15 Oct 2026

**Verdict: yes, with two gaps. Almost every number is backed by evidence, and none of my findings changes the SELL (fair value 1,621p vs 2,771p, -41.5%).** I checked about 30 numbers myself against primary filings, Yahoo and FRED, and every one matched exactly.
**The two gaps are both in the discount rate, which is what the SELL rests on.** The 5.45% gilt has no primary source, and I could not verify it either. The 5.0% equity risk premium (ERP) has no source at all; it is described only as a "portfolio rule".
**Findings by severity:** 0 change the rating; 2 change the value but not the rating; 3 are misleading (a wrong statement or an important omission); 10 are cosmetic.
**What it would take to flip the rating:** HOLD needs a gilt of 3.11%, an ERP of 2.31% or a beta of 0.449. No sourced reading I found comes close to any of these.
**Method:** an independent re-check. I did not rely on docs/phase5/relx-evidence-audit.md. Every pence impact below comes from re-running `desk.valuation_run.build` with one input changed. The base re-runs to exactly 1,621.5p. Script: scratchpad `scen.py`. No repo file was changed.

Units: money in GBP m (RELX reports in pounds); per-share values and the price in pence (GBp). 1 RELX ADR = 1 ordinary share (not used).

---

## 1. Assumptions in briefs/RELX.yaml

| Item | Value | Source given | Status | Evidence (my check) | Impact if wrong |
|---|---|---|---|---|---|
| Base revenue FY25 | GBP 9,590m | FY25 results 6-K p.26; AR25 p.186; XBRL | **verified** | FY25 results 6-K (0000929869-26-000008) says "Revenue £9,590m"; XBRL RevenueFromContractsWithCustomers is 9,590,000,000 | n/a |
| Adjusted operating profit FY25 / margin | GBP 3,342m / 34.8% | FY25 results | **verified** | Same release: "£3,342m ... margin to 34.8%" | n/a |
| Base margin (held flat) | 35.0% | H1 2026 ex print: (1,727-78)/(4,871-157) | **verified** | H1 2026 6-K (0000929869-26-000054): revenue £4,871m, adjusted operating profit £1,727m, print revenue £157m, print profit £78m. The result is 34.98%. Justified: it is the latest actual, and management guides margins higher | Using the FY25 margin including print (34.85%) instead: -9.8p |
| Growth FY26 | +3.0% (GBP) | H1 2026 GBP change | **verified, rounded** | 4,871 / 4,741 = +2.7%, rounded to 3% | At 2.7%: -5.9p (cosmetic) |
| Growth FY27-30 | 5.0% a year | Constant-currency average of FY24 (6%), FY25 (4%) and H1 2026 (5%) | FY25 and H1 26 **verified**; FY24 **sourced, not verified** | FY25 release: underlying +7%, disposals and print -3%, so +4% at constant currency. H1 26: +7%, less 2% for disposals and print, so +5% | Each 1 point a year in FY27-30 is worth about ±75p. Rating holds |
| Industry growth forecast | **MISSING** | none; every research site is blocked | **unsourced (disclosed in data notes only)** | Thomson Reuters' 8% organic outlook is a peer read-across, not an independent forecast | Not a model input. See finding M2 |
| Tax rate | 22.8% | H1 2026 note 7 | **verified** | "adjusted effective tax rate was 22.8%". Note 7 ("best estimate of the annual tax rate") is about the reported rate, which is also 22.8% | Using FY25's 22.5%: +8.2p |
| Capex % of sales | 7.10% | H1 26 p.10: (292 + 54) / 4,871 | **verified** | Quote: "Capital expenditure was £292m ... excludes pre-publication costs of £54m" | Using FY25 (6.54% / 4.87%): +9.7p |
| D&A % of sales | 5.07% | H1 26: 193 + 12 + 42 | **verified** | The D&A note lists 193 + 12 + 18 (leases) + 42 = 265 | see leases |
| NWC % of sales | -15.53% | AR25 p.141; XBRL | **verified** | XBRL: payables 4,268, receivables 2,468; release balance sheet: inventories 311 | Using the release's 4,260 payables: -0.1p. NWC at zero: -18.2p |
| Terminal growth | 2.0% | BoE and Fed 2% targets | **sourced, not verified** (no URL given; a well-known fact) | FRED T10YIE 2.35% is the cross-check | At 2.35%: +37.9p |
| Terminal RONIC | 15.4% | AR25 p.186; FY25R p.14 | **verified** | "post-tax return on average invested capital in the year was 15.4%" | Bear (RONIC = WACC): -140p |
| **Risk-free (gilt)** | **5.45%** | Investing.com 5.4542%, Trading Economics 5.44% (aggregators) | **sourced, not verified (weak)** | I could not reach the Bank of England, CNBC or MarketWatch (all return HTTP 403 here). Web search finds only BoE 5.12% (19 Aug) and press reports of about 5.30-5.35% (mid-Sep). FRED's August average is 4.99% (verified). The US 10-year on FRED is 5.21% on 13 Oct (verified). So 5.45% is plausible but rests only on aggregators | **V1**: 5.30%: +40p; 5.21%: +65p; 4.99%: +128p; 5.55%: -26p. All stay SELL |
| **Equity risk premium** | **5.0%** | "portfolio rule"; no document or URL anywhere in the brief or the evidence files | **unsourced** | No evidence file exists for it | **V2**: 4.33%: +165p; 4.50%: +121p; 5.50%: -108p. HOLD needs 2.31% |
| Beta | 0.9729 (card 0.974) | Damodaran betaGlobal.xls (5 Jan 2026), Information Services, 0.8737, relevered | **verified** | I opened the file: sheet "Industry Averages", 86 firms, "unlevered beta corrected for cash" 0.873736. Hamada relevering at 7,104 / 48,319.4 and 22.8% tax gives 0.97291. At 7,201 it gives 0.97426 | 0.974 vs 0.9729: -1.3p. Relevering on gross debt 7,267: -2.7p. Contested by RELX's own regressions (0.38-0.67), which the memo discloses. HOLD needs 0.449 |
| Credit spread | 0.70% (A); bear 1.03% (BBB) | FRED BAMLC0A3CA / BAMLC0A4CBBB, 13 Oct | **verified** | FRED on 13 Oct: 0.70 / 1.03. These are **US-dollar** corporate indices added to a sterling gilt (finding M3) | BBB: -9.2p |
| Ratings | A3 / A- / BBB+ | RELX Capital term sheet, 24 Mar 2025 | **verified, 19 months old** | SEC 0001193125-25-061449: "Moody's: A3; S&P: A-; Fitch: BBB+". Current outlooks not checked | none |
| Net debt (excluding leases) | GBP 7,104m | FY25R p.13 | **verified** | "net debt figure of £7,201m"; "lease liabilities of £97m". 7,201 - 97 = 7,104 | see leases |
| Leases | 0 (out of net debt; lease depreciation not added back) | brief | **consistent** | Lease depreciation is left inside operating profit, so lease cost already reduces cash flow. Leaving the lease debt out avoids counting it twice | The alternative consistent treatment (leases in net debt, lease depreciation added back, beta relevered at 7,201) gives +4.7p |
| Joint ventures | not added (book 164) | FY25R p.19, p.26; AR25 p.206 | **verified** | The release reconciliation reclassifies "tax in joint ventures" and "finance income in JVs" into adjusted operating profit. Post-tax JV result 44 + 14 - 1 = 57. XBRL equity-method investments 164 | If wrongly left out: +10.2p. I judge the treatment right |
| Other investments | +GBP 131m | AR25 p.167 | **verified** | Release balance sheet: "Other investments 92 / 131" (the same figure as cash, 131, by coincidence) | n/a |
| Minorities | -GBP 24m (book) | FY25R p.22; XBRL | **verified** | XBRL NoncontrollingInterests 24,000,000 | n/a |
| Pension | 0 (surplus 43 not added) | AR25 p.141; XBRL | **verified** | XBRL LiabilityAssetOfDefinedBenefitPlans -43 | Adding the surplus: about +2p |
| Dividends after 31 Dec | GBP 1,217m | 851 + 366 | 851 **verified**; 366 is **RELX's expected cost** | H1 26: "48.0p ... amounted to £851m"; "expected total cost of funding this dividend is £366m" | +5m actual: -0.3p |
| Buybacks after 31 Dec | GBP 2,056.2m | 1,750 + 100 + 150 + 56.2 | **verified** | H1 26: "Total consideration ... £1,750m"; "A further £100m has been completed since 1 July", so there is no double count. 7 Sep 6-K: "completion of a £150 million ... programme on 4 September". I summed 15 daily VWAPs x shares (2,225,133 shares) from 6-K 0000929869-26-000071 ex 99.3, 99.4 and 99.6: **GBP 56.18m** | Stamp duty: 0.0p |
| Shares | 1,743.754727m | 6-K 28 Sep 2026 | **verified** | "has 1,743,754,727 ordinary shares in issue (excluding treasury shares)". About 6m Employee Benefit Trust shares are still included | Excluding the EBT (~1,737.8m): +5.6p |
| Share price | 2,771p | Yahoo REL.L close 13 Oct 2026 | **verified** | Yahoo chart: 13 Oct close 2,771.0 GBp. 14 Oct has no row. 15 Oct intraday 2,809p | The rating is unchanged at 2,809p |
| Debt weight | 12.82% | 7,104 / (7,104 + 48,319.4) | **verified (arithmetic)** | Mixes 31 Dec net debt with the September share count and October price. Disclosed | Using June net debt 8,614 (15.13%) and relevering: +12.5p |
| Stub years | 0.78356 | 286 / 365 | **verified** | 31 Dec 2025 to 13 Oct 2026 is 286 days | n/a |
| Bear margin | 32.4% | AR25 note 1 p.145 | **sourced, not verified** (AR not fetched) | Mistakes log row 26 | Bear only |
| Bear acquisitions | 2.7% of revenue | SEC XBRL FY21-25 | **sourced, not verified** | Computed by the Bear agent | Bear only |

## 2. Can every number in the final memo be traced?
- `python -m desk.memo_check runs/RELX/2026-10-14` passes. It also passes when I remove `bear/scratch`.
- **memo_check is weak.** It matches a number found anywhere in the run folder, so it can confirm a number exists but not that it means the same thing. I therefore traced the headline numbers by hand:
  - **Matched to valuation.json:** fair value 1,621p (1,621.48), upside -41.5%, WACC 9.60%, cost of equity 10.31%, EV 36,209.2, equity 28,274.7, bear 1,244p (1,243.9), sensitivity grid, terminal value 69.3% of EV, exit multiple 7.9x.
  - **HOLD and BUY thresholds:** 2,494p and 3,187p are correct (2,771 x 0.90 and x 1.15).
- When I check against the structured outputs alone (JSON, CSV, inputs.yaml), 6 memo numbers are found only in agent notes, not in any data file: margins 31.4%, 33.9%, 33.4%; print margin 46.4%; 95 (the regression range); -146p. All six are in fundamentals or bear notes.
  - I verified FY24 33.9% and FY25 34.8% myself in the FY25 release.
- **No untraced numbers.** The one inconsistency is in the beta scenarios (finding C5).

## 3. Findings

### Changes value, not the rating
- **V1. Risk-free 5.45% has no primary source.**
  - It comes from aggregators. The Bank of England and DMO sites are blocked, and I could not verify it either.
  - The nearest checkable readings are BoE 5.12% (19 Aug), about 5.30-5.35% in mid-September (press), and the US 10-year at 5.21% (FRED, 13 Oct).
  - This is the most value-sensitive input in the model: each 1 point is worth -233p / +300p. A plausible error range of 5.21-5.55% moves value between +65p and -26p. All stay SELL.
  - Disclosed in the memo as a FLAG. **Fix:** get the BoE IUDMNZC series for 13 Oct from a network that can reach it.
- **V2. ERP 5.0% has no source anywhere.**
  - Not in the brief yaml, brief-relx.md or any evidence file. It is labelled only a "portfolio rule".
  - That falls short of CLAUDE.md rule 3 ("every number needs a source").
  - Each 1 point is worth -205p / +256p. A Damodaran-style implied ERP of 4.3-4.5% (not verified here) would give +121p to +165p. Still SELL.
  - **Fix:** write a short ERP evidence card (source, date, and why 5.0% was chosen over an implied ERP).

### Misleading (a wrong statement or an important omission, no value change)
- **M1. relx-capex-evidence.md contradicts the bridge on leases.** It says lease depreciation is left out "because lease liabilities are already in net debt". The agreed bridge takes leases **out** of net debt, for the opposite reason: lease cost already reduces cash flow. The model itself is consistent (the alternative consistent treatment is +4.7p). Only the wording in the evidence file is wrong.
- **M2. The missing industry growth forecast is not in the memo.**
  - The Data agent marked it MISSING and used the Thomson Reuters outlook as a substitute (low confidence).
  - The memo's Sources and Risks sections do not say that no independent market forecast exists. The 5.0% rests only on RELX's own history.
  - Rule 3 says "STOP". The agent did not stop, which is arguably fine because this number is not a model input. Either way, the memo should say it is missing.
- **M3. The credit spread is a US-dollar index added to a sterling gilt.**
  - ICE BofA US Corporate A (BAMLC0A3CA) is a USD index. RELX borrows mostly in USD and EUR.
  - This mismatch is not stated. The impact is small: the BBB alternative is -9.2p, and debt is only 12.8% of capital.

### Cosmetic
- **C1. The beta comment in the brief is stale.** briefs/RELX.yaml and brief-relx.md decision 6 say 0.974, but the run uses 0.9729 (the lease consistency fix). Explained in the risk and valuation notes. -1.3p.
- **C2. Disclosures left out of the memo.** The memo does not mention three items:
  - Employee Benefit Trust shares are still in the count (+5.6p if excluded).
  - The interim dividend of GBP 366m is RELX's *expected* cost, not actual cash.
  - Buybacks from 26 Sep to 13 Oct are not filed. Cash and shares are both left out, which is consistent.
- **C3. Editor notes are out of date.** editor/notes.md says "PM to respond" in every bear cell and "PM review pending". The memo now carries the PM's responses and "PM confirmed 15 Oct 2026".
- **C4. Tax quote belongs to a different rate.** The tax quote ("best estimate of the annual tax rate") belongs to the reported rate, while the input is the adjusted rate. Both are 22.8%, so the impact is 0p.
- **C5. Beta scenario values differ between files.** The Bear agent and the memo give beta 0.38 = 2,673p, 0.75 = 1,918p, 0.58 = 2,207p. valuation/notes.md gives 2,668p, 1,920p, 2,213p. This is beta rounding; the rating is the same.
- **C6. Beta relevered on net debt, not gross debt.** Damodaran unlevers on gross debt, so relevering on gross debt (7,267) would be more consistent. -2.7p.
- **C7. FY26 growth is rounded.** The brief uses +3.0%; the H1 actual is +2.7%. -5.9p.
- **C8. Credit ratings are 19 months old.** The source is the March 2025 term sheet; current outlooks were not re-checked.
- **C9. Terminal-growth sources have no link.** The BoE and Fed 2% targets are cited without a URL.
- **C10. memo_check is weak.** It accepts a number found anywhere in the run, including scratch copies. The Editor's own FLAG 2 already says so. A fix belongs on a branch for Amanda's approval.

## 4. Consistency and stale data
- **Rating and value:** the memo matches valuation.json (SELL, 1,621.48p, -41.48%). results.md and brief-relx.md decision 13 match.
- **Currency labels:** correct throughout (GBP m and GBp). No exchange rate is used, correctly. The ADR ratio of 1:1 is not used.
- **Open FLAGs still unresolved:**
  - gilt from aggregators (V1);
  - WACC 9.60% above the desk's 6-9% range (disclosed);
  - implied exit multiple 7.9x below every peer (disclosed);
  - comps: four peers are Yahoo-only, and NTM EBITDA and RELX forward EPS are MISSING (disclosed).
- **Stale data:**
  - The price is the 13 Oct close. REL.L had risen from 2,496p (30 Sep) to 2,771p (13 Oct) and was 2,809p intraday on 15 Oct, which does not change the rating.
  - The latest company data is H1 2026 (23 Jul). The Q3 trading update is expected around 23 Oct; it is mentioned in the data notes, not the memo.
  - The FRED August gilt average is correctly rejected as stale.

## 5. Not verified by me
- **The gilt reading of 5.45%:** blocked; see V1.
- **The Annual Report 2025 pages:** p.141, 145, 167, 179, 186, 199 and 206 were not fetched. Where I could, I covered them with XBRL and the FY25 results release.
- **Earlier history:** FY24 constant-currency growth (6%) and the FY21-23 margins and tax rates.
- **Market data recomputed by agents:** RELX's own regression betas and the peer betas (Yahoo), and the peer multiples.
- **Industry growth:** no independent industry forecast is reachable.
