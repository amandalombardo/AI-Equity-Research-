# Equity risk premium (ERP): evidence pack

**For:** Amanda (PM) | **Date:** 15 Oct 2026 | **Scope:** `dcf.wacc.equity_risk_premium` in briefs/DGE.yaml, KO.yaml, ULVR.yaml and RELX.yaml (all 5.0%, no source)
**Repo:** nothing was changed. Values come from the desk's own engine (`desk.valuation_run.build`), run on the current briefs and run inputs. Only the ERP was changed.

---

## 1. The short version

- **The desk's 5.0% does match one real published figure: Kroll's recommended US ERP, 5.0%.** It was set on 2 Sep 2025 and reaffirmed through 2026. But Kroll pairs it with the **20-year** US Treasury (5.60% on 13 Oct 2026, FRED DGS20). The desk uses the 10-year (5.22%). So the 5.0% can be sourced, but it is not being used the way Kroll intends.
- **Damodaran's implied ERP has been about 4.2% all year.** It was 4.23% on 1 Jan 2026 and 4.20% on 1 Oct 2026, even though the US 10-year rose from 4.18% to 5.29% over that time. "Implied" means it is worked out from today's share prices and today's bond yield, so it is the natural partner for the spot yields the desk uses.
- **Survey and historical figures are higher, at about 5-5.5%.** Fernandez's 2025 survey of what analysts actually use gives US 5.5%, UK 5.4% and Germany 5.4%. The DMS/UBS long-run US premium over bonds is about 4.9%. But those survey answers were paired with lower risk-free rates (about 4.1% US and UK, 2.7% Germany) than the desk's current ones.
- **Rating impact.** The ERP changes the rating for **Unilever only**. ULVR moves from SELL to HOLD below an ERP of **4.19%**. Diageo stays HOLD anywhere between 3.77% and 5.62%. KO and RELX stay SELL at every plausible ERP.
- **Recommendation: one desk-wide ERP of 4.2%,** taken from Damodaran's implied US ERP. **Before you sign it off, open Damodaran's page and confirm the number yourself** (section 6). Alternatives: (A) keep 5.0% but cite Kroll, and ideally pair it with the 20-year yield; (B) per-market Damodaran figures.
- **Caveat on every outside source:** this sandbox blocks Damodaran's site (NYU), Kroll, SSRN, Tulane, BVResources, UBS, LBS, Ofwat and gov.uk. **Every outside ERP figure below was seen secondhand**, in search-engine summaries of those pages, not on the page itself. The one exception is FRED (US Treasury yields), which I read directly. FRED independently confirms the bond yields Damodaran's figures are built on (section 2a). Status labels below: **Secondhand** = seen only in a search summary; **Corroborated** = secondhand, but a figure that depends on it checks out against FRED.

---

## 2. Sourced ERP estimates

### 2a. Damodaran (NYU Stern): implied ERP on the S&P 500

How it works: he finds the expected return that makes the S&P 500's current price equal to its expected future cash payouts (dividends plus buybacks), then subtracts the US 10-year Treasury yield on the same day. It is updated monthly.

| Date | Implied ERP | US 10-year used | Expected market return (ERP + yield) | Source | Status |
|---|---|---|---|---|---|
| 1 Jan 2026 | **4.23%** (trailing 12-month cash yield) | 4.18% | 8.41% | Damodaran "Data Update 2 for 2026" (blog, Jan 2026): "IRR for the S&P 500 was 8.41% on Jan 1; subtracting the 10-year treasury rate (4.18%) yields an ERP of 4.23%" (edwardconard.com summary). Also BVWire "Damodaran posts his first data update for 2026". Underlying data: pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/histimpl.html | **Corroborated:** FRED DGS10 on 31 Dec 2025 = 4.18% (read directly) |
| 1 Feb 2026 | 4.14% (trailing 12-month) | n/a | n/a | Search summary of a March 2026 Damodaran post | Secondhand |
| 1 May 2026 | 4.24% | n/a | n/a | Search summary (source not named) | Secondhand |
| 1 Jul 2026 | **4.42%** (S&P 500 at 7,499.36) | n/a | n/a | Damodaran, "Country Risk: Determinants, Measures and Implications, The 2026 Edition" (SSRN 7107638; blog post aswathdamodaran.blogspot.com/2026/07/...) | Secondhand |
| **1 Oct 2026 (latest)** | **4.20%** (trailing 12-month, adjusted payout: his headline). Other versions on the same line: 3.70% (trailing 12-month cash yield), 5.67% (average cash yield over 10 years), 3.61% (net cash yield), 3.30% (normalised earnings and payout) | **5.29%** | 9.49% | Damodaran home page pages.stern.nyu.edu/~adamodar/New_Home_Page/home.htm (search snippet) | **Corroborated:** FRED DGS10 on 30 Sep 2026 = 5.29% (read directly). The search tool said "check before relying", because 4.20% is also his July mature-market figure |

**Mature-market ERP (the base he adds country premiums to).** Moody's cut the US from Aaa to Aa1 in May 2025. Since then Damodaran no longer uses the US implied ERP as the mature-market ERP. He removes the US default spread first.

- **January 2026:** mature-market ERP **4.23%**, with a US default spread of 0.23% (Damodaran, "Data Update 4 for 2026: A Risk Journey around the World", Substack). This search summary is internally muddled about whether 4.23% is before or after the 0.23% adjustment. The ctryprem table (below) is consistent with 4.23% as the mature-market base. **Secondhand.**
- **July 2026:** implied ERP 4.42%, less the 0.22% Aa1 default spread, gives a mature-market ERP of **4.20%** (2026 Country Risk paper, SSRN 7107638; BVWire "Damodaran revises country risk framework after U.S. rating downgrade"). A third-party summary and his X post of 2 Jul 2026 mention **4.17%** instead. The difference is unresolved. **Secondhand.**
- **October 2026:** no mature-market figure seen. If the same 0.22% spread were deducted from the 4.20% implied ERP, it would be about 3.98%. That is my inference, not his published number.

**UK, Germany and Eurozone (Damodaran country table, ctryprem.html, "Last updated: January 5, 2026"):**

- **United Kingdom:** Moody's Aa3, total ERP **5.01%** (search snippet of the table). This equals the 4.23% mature-market base plus the UK country risk premium. **Secondhand.**
- **Germany:** Aaa, so no country premium. Total ERP = mature-market ERP, about **4.2%** (Visual Capitalist map "World's riskiest markets in 2026", undated). **Secondhand.**
- **A note on method:** Damodaran adds country premiums according to **where a company operates**, not where it is listed or which bond the desk uses. Applying the UK's 5.01% to RELX or Diageo just because they are listed in London would not be his method.

**Local files.** I checked /mnt/project-files/ (including the uploads folder) and the run folders. The Damodaran files there are `betaGlobal.xls` (5 Jan 2026), `damodaran_betas_us_jan2026.xls` and an uploaded US betas file (saved 12 Apr 2026). **None of them states an ERP.** They contain betas only. No ctryprem, histimpl or ERP spreadsheet has been uploaded.

### 2b. Kroll (formerly Duff & Phelps)

| Item | Figure | Date | Source | Status |
|---|---|---|---|---|
| Recommended **US ERP** | **5.0%** | Effective 2 Sep 2025 (lowered from 5.5%, which applied from 15 Apr 2025). Reaffirmed 30 Jan 2026, again around 1 Apr 2026, and in a September 2026 BVWire item | Kroll, "Cost of Capital Updates, January 2026: Executive Summary" (edge.sitecorecloud.io/.../kroll-cost-of-capital-updates-jan26-executive-summary.pdf); BVWire "Kroll reaffirms U.S. ERP at 5.0% and lowers eurozone"; BVWire "Kroll reaffirms 5.0% U.S. ERP, sticks with Treasury risk-free rate" | Secondhand (all Kroll and BVWire pages blocked) |
| Matching **risk-free rate** | **The higher of** a normalised 3.5% **or the spot 20-year US Treasury yield** on the valuation date | Same | Kroll page "Kroll increases U.S. normalized risk-free rate from 3.0% to 3.5%, but spot 20-year U.S. Treasury yield preferred when higher" | Secondhand |
| Spot 20-year today | **5.60%** (13 Oct 2026); 5.65% (9 Oct) | 13 Oct 2026 | FRED DGS20 (read directly) | **Primary** |
| Recommended **Eurozone ERP** | **5.0-5.5%**, down from 5.5-6.0%. Kroll adds: "an ERP towards the higher end of the range (i.e., closer to a 5.5% ERP) is still likely more appropriate, but this indication could be lowered later in 2026." It is from a German investor's point of view | From 30 Jan 2026; unchanged in the May 2026 update | Kroll Jan 2026 executive summary; "kroll-eurozone-erp-rf-table-2026.pdf"; "Cost of capital in the current environment, May 2026 update" | Secondhand |
| UK ERP | **Not found.** Kroll publishes a UK normalised risk-free rate (since 2014), but I found no UK ERP | n/a | kroll.com "normalized risk-free rate guidance: United Kingdom, Canada" | **MISSING** |

What this means in practice: the textbook Kroll cost of equity for an average-risk US stock today is 5.60% + 5.0% = 10.60%. The desk's version is 5.22% + 5.0% = 10.22%.

### 2c. Fernandez et al.: survey of the ERP analysts and companies actually use

- **2025 survey:** "Survey: Market Risk Premium and Risk-Free Rate used for 54 countries in 2025", by P. Fernandez, D. García de la Garza and L. Fernández Acín (SSRN 5260463; IESE/Tulane PDF "Rf and Rm-Rf 2025"). Method: an email survey in April 2025 to more than 14,000 finance and economics professors, analysts and company managers. A country is reported only if it got more than 6 answers. Figures are averages in local currency.

| Country | Average ERP used | Average risk-free rate used | Rf + ERP | Status |
|---|---|---|---|---|
| USA | **5.5%** | 4.1% | 9.6% | Secondhand (BVWire summary; B.A. Ødegaard lecture slides reproducing the paper's table, ba-odegaard.no, Nov 2025) |
| UK | **5.4%** | 4.1% | 9.5% | Secondhand (Ødegaard slides only) |
| Germany | **5.4%** | 2.7% | 8.1% | Secondhand (Ødegaard slides only) |

- **2026 survey:** "... used for 97 countries in 2026", by Fernandez, Habibian and Fdez. Acín (SSRN 6570342, April 2026). It has 3,637 answers, collected March-April 2026. **The country figures are MISSING.** The SSRN paper is blocked, and no summary I found gives the US, UK or German values. Ødegaard's 24 Sep 2026 slides probably have them, but they are blocked too.

### 2d. UBS Global Investment Returns Yearbook 2026 (Dimson, Marsh, Staunton; launched 3 Mar 2026)

- **US, 1900-2025:** real (after-inflation) returns of 6.6% a year on equities and 1.6% on bonds. Nominal: 9.8% on equities, 4.6% on bonds, 3.4% on bills. Source: UBS public summary edition (ubs.com/.../giry2026-summary-public.pdf) and press coverage. **Secondhand.** The implied US equity premium over bonds is 1.066 / 1.016 - 1 = **4.9% a year** (geometric). That is my arithmetic on the secondhand figures.
- **UK vs bonds and World vs bonds, 1900-2025:** **MISSING.** The full Yearbook (paid) and the public PDF are blocked, and no summary gives these numbers.
- **For context only:** the 2025 edition gives world equities, 2000-2024, a premium of 4.3% over cash (not bonds), so it is not comparable.

### 2e. UK regulators

- **Ofwat PR24 final determination (Dec 2024):** total market return (TMR) of **6.83% real (CPIH)**, the midpoint of a 6.68-6.98% range (Ofwat, "PR24 final determinations: Aligning risk and return, Allowed return appendix"). **Secondhand.** Regulators keep TMR roughly stable and treat ERP as TMR minus the risk-free rate, so their ERP shrinks when gilt yields rise.
  - **Illustration only:** if CPIH inflation is 2% (my assumption), 6.83% real is about 8.97% nominal. Less today's 5.45% gilt, that leaves an ERP of about **3.5%**.
- **CMA PR24 redeterminations (final report 10 Mar 2026, published 26 Mar 2026):** final TMR **MISSING**. The provisional determination's cost of equity midpoint was 5.60% real (CPIH), against Ofwat's 4.83%, with a 2.49% risk-free rate (CMA provisional determinations, vol. 4). **Secondhand.**

---

## 3. Spot rates, and which ERP goes with them (plain language)

The cost of equity is **risk-free rate + beta x ERP**. For an average-risk share (beta = 1), the first two terms add up to "what the stock market as a whole is expected to return". The test is whether that total makes sense today.

- **An implied ERP is measured against today's bond yield.** Damodaran takes today's share prices, works out the return they imply, and subtracts today's 10-year yield. "Spot yield + implied ERP" therefore adds back up to the return the market is actually pricing: 5.29% + 4.20% = 9.49% on 1 Oct 2026. If yields rise and share prices don't fall, the implied ERP shrinks automatically. So **an implied ERP is the like-for-like partner for a spot rate.** That is exactly what the desk uses (US 10-year about 5.2%, gilt 5.45%, Bund 3.45%).
- **A historical ERP is an average over about 125 years** (DMS: about 4.9% over US bonds), a period when bond yields were often much lower or much higher than now. Adding it to an unusually high spot yield assumes the market's required return rises one-for-one with bond yields. It may or may not do so. Survey numbers (Fernandez) have a similar problem: respondents paired 5.4-5.5% with risk-free rates of about 4.1%, not today's 5.2-5.45%.
- **What 2026 shows:** the US 10-year rose 1.1 points (4.18% to 5.29%) and Damodaran's implied ERP barely moved (4.23% to 4.20%). So far this year, the market has repriced to demand about 1 point more in total, and the premium has held steady. The desk's current 5.22% + 5.0% = **10.22%** asks about **0.7 points more** than the market is pricing (9.49%). That makes every company look about 0.7 points riskier than the average stock.
- **Kroll's 5.0% is a deliberately steady figure, designed to go with the 20-year yield.** Used Kroll's way, it gives 10.6% for the US market today. That is a defensible, more cautious view, but it is Kroll's own judgement, not a market reading.
- **The currency question for ULVR and RELX:** the ERP should be measured in the same currency as the risk-free rate. Damodaran's 4.2% is a US-dollar figure. For euros he would use a mature-market ERP of about 4.2% with no German premium. For sterling he would add a premium only for UK operations. RELX earns most of its revenue outside the UK, so the UK's 5.01% would overstate its risk.

---

## 4. Value impact (desk engine, current briefs and run inputs, ERP changed only)

The script is at /tmp/claude-0/-home-user-ai-equity-research-/fb969581-7a6b-51a1-bb6d-fc50a294e095/scratchpad/audit/erp_all.py. It reads the repo and writes nothing to it. At ERP 5.0% it reproduces each stored `valuation.json` exactly.

- **Rating rule:** BUY if upside is at least +15%; SELL if downside is at least 10%; otherwise HOLD.
- **ERP feeds through twice:** once into WACC, and once into the cost of equity used to roll the value forward from the balance-sheet date.

| ERP | **DGE** (pence, price 1,673.0p) | **KO** (USD, price USD 90.12) | **ULVR** (pence, price 4,710.5p) | **RELX** (pence, price 2,771.0p) |
|---|---|---|---|---|
| 4.00% | 1,862p, +11.3%, HOLD | USD 52.34, -41.9%, SELL | 4,344p, -7.8%, **HOLD** | 1,877p, -32.3%, SELL |
| 4.20% (Damodaran implied, 1 Oct 2026) | 1,811p, +8.2%, HOLD | USD 51.31, -43.1%, SELL | 4,234p, **-10.1%, SELL** (just) | 1,821p, -34.3%, SELL |
| 4.23% (Damodaran implied, 1 Jan 2026) | 1,803p, +7.8%, HOLD | USD 51.16, -43.2%, SELL | 4,219p, -10.4%, SELL | 1,813p, -34.6%, SELL |
| 4.50% | 1,738p, +3.9%, HOLD | USD 49.85, -44.7%, SELL | 4,082p, -13.3%, SELL | 1,742p, -37.1%, SELL |
| **5.00% (current; Kroll US)** | **1,627p, -2.7%, HOLD** | **USD 47.60, -47.2%, SELL** | **3,855p, -18.2%, SELL** | **1,621p, -41.5%, SELL** |
| 5.40% (Fernandez UK/Germany 2025) | 1,547p, -7.6%, HOLD | USD 45.95, -49.0%, SELL | 3,695p, -21.6%, SELL | 1,534p, -44.6%, SELL |
| 5.50% (Fernandez US 2025; top of Kroll eurozone) | 1,527p, -8.7%, HOLD | USD 45.56, -49.4%, SELL | 3,657p, -22.4%, SELL | 1,514p, -45.4%, SELL |

**Inputs held fixed:**

| | Risk-free | Beta | Debt weight | Run date |
|---|---|---|---|---|
| DGE | US 10-year 5.22% | 0.960 | 29.4% | 12 Oct 2026 |
| KO | US 10-year 5.22% | 0.609 | 7.1% | 13 Oct 2026 |
| ULVR | Bund 3.45% | 0.884 | 16.1% | 14 Oct 2026 |
| RELX | Gilt 5.45% | 0.973 | 12.8% | 14 Oct 2026 |

**Breakeven ERP (where the rating flips):**

| Company | BUY if ERP at or below | SELL if ERP at or above | Comment |
|---|---|---|---|
| DGE | 3.77% | 5.62% | HOLD across every sourced figure (4.20-5.50%) |
| KO | never (still below +15% at ERP 0%) | 0.50% | SELL on any plausible ERP |
| ULVR | 2.53% | **4.19%** | **The only company whose rating the ERP decides.** At Damodaran's 4.20% it is SELL by 0.11 points of upside; at 4.0% it is HOLD |
| RELX | 1.10% | 2.31% | SELL on any plausible ERP |

**FLAG on the ULVR audit:** the ULVR audit (audit-2026-10-15/ULVR.md) says "HOLD starts at an ERP of 4.23%". On the current run inputs, the flip is at **4.19%**, and 4.23% gives 4,219p, SELL (-10.4%). The audit figure looks slightly off. Use 4.19%.

---

## 5. Recommendation

**Recommended: one desk-wide ERP of 4.2%, citing Damodaran's implied US ERP.** It was 4.23% on 1 Jan 2026 and 4.20% on 1 Oct 2026.

**Why:**

1. It is the only figure built to go with a **spot** risk-free rate, which is what the desk uses for all four companies (decision 11).
2. It has been stable all year (4.14-4.42%) while rates moved, so 4.2% isn't the result of picking a convenient month.
3. It is the most widely cited single public source, and it fits the desk's existing use of Damodaran betas.
4. It keeps Diageo at HOLD (1,811p), KO at SELL (USD 51.31) and RELX at SELL (1,821p). It also keeps **ULVR at SELL (4,234p), but only by 0.01 points of ERP.** The memo should say so.

**Conditions before sign-off:**

- (a) **Open Damodaran's home page (pages.stern.nyu.edu/~adamodar) in a normal browser and confirm "Implied ERP on October 1, 2026 = 4.20%"**, plus the January histimpl figure (4.23%). I could only see them secondhand. FRED confirms the 4.18% and 5.29% Treasury yields they are built on, but not the ERPs themselves.
- (b) Record in each brief that the ERP is "Damodaran implied US ERP, [date], paired with the spot 10-year (or local equivalent)".
- (c) For ULVR and RELX, note that a US-market ERP is being applied to euro and sterling rates. Damodaran would use about the same mature-market figure for Germany. For the UK he would add a country premium only for UK-based operations.

**Alternative A: keep 5.0%, but cite Kroll's recommended US ERP (effective 2 Sep 2025, reaffirmed 2026).**

- This is a respected practitioner source, needs no change to the numbers, and is the more cautious choice.
- Weakness: Kroll pairs it with the **20-year** Treasury (5.60%), not the 10-year. Taking Kroll at its word would also raise the risk-free rate, which the desk has not done. The UK figure is missing. The eurozone figure is 5.0-5.5% (Kroll leans towards 5.5%).
- Fernandez's survey (US 5.5%, UK and Germany 5.4%) supports "about 5%+ is what practitioners use". Those respondents used lower risk-free rates, though.
- Ratings: unchanged from today.

**Alternative B: per-market Damodaran figures (January 2026 country table).**

- US 4.2% for DGE and KO (US-dollar cash flows). Germany (Aaa) about 4.2% for ULVR. UK total ERP 5.01% (Aa3) for RELX.
- Ratings are the same as the recommendation, except RELX (5.0% is the current value anyway: SELL).
- Weakness: it assigns country premiums by the risk-free currency, not by where the companies operate. That is not Damodaran's own method. The fully correct version (revenue-weighted country premiums, e.g. 62% of ULVR's remaining sales are in emerging markets) is a bigger piece of work and would push ULVR's ERP **up**.

**Not recommended:** the regulator-implied ERP of about 3.5% (Ofwat TMR less today's gilt). It is a UK utility framework, the CMA's final figure is missing, and it depends on my 2% inflation assumption.

---

## 6. Missing / could not verify

- **Every Damodaran, Kroll, Fernandez, UBS/DMS and Ofwat/CMA figure is secondhand** (search summaries). The network blocks all of those sites. Only FRED was read directly.
- Damodaran **mature-market ERP for October 2026:** not published in anything I could see (about 3.98% by inference). July is 4.20% vs 4.17%, unresolved.
- **Fernandez 2026** country figures (US, UK, Germany): missing.
- **DMS 2026 UK and World** premium over bonds: missing.
- **Kroll UK ERP:** missing. **CMA PR24 final TMR:** missing.
- **Confidence:** medium-high on the direction and range (4.2% implied vs 5.0-5.5% Kroll/survey). Medium on each exact figure until it is checked at the source. High on the value table, which comes from the desk engine and reproduces stored results exactly.

## Sources

- Damodaran: [home page](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/home.htm), [histimpl](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/histimpl.html), [ctryprem (5 Jan 2026)](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/ctryprem.html), [Data Update 2 summary (EdwardConard)](https://www.edwardconard.com/macro-roundup/using-nominal-cash-flow-projections-the-irr-for-the-sp-500-was-8-41-on-jan-1-subtracting-the-10-year-treasury-rate-4-18-yields-an-erp-of-4-23-damodaran-notes-the-current-erp-is-alm/), [BVWire Jan 2026](https://www.bvresources.com/articles/bvwire/damodaran-posts-his-first-data-update-for-2026), [Data Update 4 for 2026](https://aswathdamodaran.substack.com/p/data-update-4-for-2026-a-risk-journey), [Country Risk 2026 (SSRN 7107638)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7107638), [blog July 2026](https://aswathdamodaran.blogspot.com/2026/07/country-risk-drivers-measures-and.html), [BVWire country-risk revision](https://www.bvresources.com/articles/bvwire/global-damodaran-revises-country-risk-framework-after-us-rating-downgrade), [X post July 2026](https://x.com/AswathDamodaran/status/2072791192388178322), [Visual Capitalist 2026 map](https://www.visualcapitalist.com/mapped-the-worlds-riskiest-markets-in-2026/)
- Kroll: [Jan 2026 executive summary](https://edge.sitecorecloud.io/krollllc17bf0-kroll6fee-proda464-0e9b/media/Cost-of-Capital/kroll-cost-of-capital-updates-jan26-executive-summary.pdf), [Eurozone ERP table 2026](https://edge.sitecorecloud.io/krollllc17bf0-kroll6fee-proda464-0e9b/media/Cost-of-Capital/kroll-eurozone-erp-rf-table-2026.pdf), [May 2026 update](https://edge.sitecorecloud.io/krollllc17bf0-kroll6fee-proda464-0e9b/media/Kroll-Images/PDFs/cost-of-capital-in-the-current-environment-may-2026-update.pdf), [normalised Rf 3.5% / spot 20-year](https://www.kroll.com/en/reports/cost-of-capital/kroll-increases-us-risk-free-rate-but-spot-treasury-yield-preferred), [BVWire reaffirms 5.0% / eurozone](https://www.bvresources.com/articles/bvwire/kroll-reaffirms-us-erp-at-50-and-lowers-eurozone), [BVWire reaffirms 5.0% (Treasury Rf)](https://www.bvresources.com/articles/bvwire/kroll-reaffirms-50-us-erp-sticks-with-treasury-risk-free-rate), [BVWire lowered to 5.0%](https://www.bvresources.com/articles/bvwire/kroll-lowers-recommended-us-erp-to-50)
- Fernandez: [2025 survey SSRN 5260463](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5260463), [Tulane PDF](https://breesept.tulane.edu/wp-content/uploads/sites/18/2026/03/Rf-and-Rm-Rf-2025.pdf), [BVWire 2025](https://www.bvresources.com/articles/bvwire/global-fernandezs-survey-of-2025-risk-premiums-and-risk-free-rates), [Ødegaard slides Nov 2025](https://ba-odegaard.no/teach/msb311_2025/lectures/worldwide_risk_premium_survey/lectures_wordwide_risk_premium_survey.pdf), [2026 survey SSRN 6570342](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6570342)
- DMS/UBS: [GIRY 2026 public summary](https://www.ubs.com/content/dam/assets/wm/static/cio/documents/giry2026-summary-public.pdf), [UBS press release 3 Mar 2026](https://www.ubs.com/global/en/media/display-page-ndp/en-20260303-global-investment-returns-yearbook-2026.html)
- Regulators: [Ofwat PR24 FD allowed return appendix](https://www.ofwat.gov.uk/wp-content/uploads/2024/12/PR24-final-determinations-Aligning-risk-and-return-Allowed-return-Appendix.pdf), [CMA PR24 provisional vol. 4](https://assets.publishing.service.gov.uk/media/68e7c1621c8b2a3b506907dc/PR24_PD_vol_4_-_chapter_7_to_10.pdf), [CMA PR24 final vol. 1](https://assets.publishing.service.gov.uk/media/69c5136793cc6e8b87a6f71c/Final_decision_summary_and_volume_1.pdf)
- FRED (read directly): [DGS10](https://fred.stlouisfed.org/series/DGS10) 31 Dec 2025 4.18%, 30 Sep 2026 5.29%, 13 Oct 2026 5.21%; [DGS20](https://fred.stlouisfed.org/series/DGS20) 9 Oct 2026 5.65%, 13 Oct 2026 5.60%
