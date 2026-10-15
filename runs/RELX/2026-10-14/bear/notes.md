# Bear agent notes: RELX PLC (RELX / REL.L), run 2026-10-14

## Re-run 15 Oct 2026 (evidence audit)

**Why.** The evidence audit of 15 Oct 2026 (`docs/audit-2026-10-15/RELX.md`, finding V2) found the 5.0% equity risk premium had no source. The PM decided on **4.2%** (Damodaran implied ERP, 1 Oct 2026; `briefs/RELX.yaml`; evidence `docs/audit-2026-10-15/erp-evidence.md`). The brief's bear margin is now **32.4%** (`bear_agent_margin`, PM bear responses, decision 14, 15 Oct 2026). I did not edit the brief, `inputs.yaml` or `desk/`.

**What I did.**
1. Saved the 14 Oct results as `bear/scratch/bear_results_erp5_2026-10-14.json`.
2. Edited `run_bear.py` (run-local script only):
   - reads the bear margin from the brief (and asserts it equals FY23 ex print, 32.38% rounded); 33.1% kept as the "old label" test;
   - reads the market-implied WACC from `valuation/sanity_checks.json` (was hard-coded 6.95%);
   - adds the audit stress lines: ERP 5.0% (Kroll), ERP 5.5% (Fernandez 2025 survey), gilt 5.30% (press), gilt 5.21% (US 10y, FRED DGS10), ERP 5.0% + BBB spread, and the full bear stack at ERP 5.0% and 5.5%.
3. Re-ran it: `PYTHONPATH=. python runs/RELX/2026-10-14/bear/run_bear.py`. The control copy reproduces the Valuation agent's new base (1,821.3p) and engine bear (1,386.3p) exactly. **Cross-checks:** at ERP 5.0% the scratch run reproduces the old base 1,621.5p and the old full stack 901.7p exactly; the beta values (2,117p / 2,264p / 2,400p / 2,844p) match `valuation/notes.md`, so audit finding C5 is closed for the bear file.
4. Rewrote `challenges.md` with new values everywhere, a "14 Oct" column for comparison, the audit lines, and the PM's bear responses (decision 14) with a check of whether each still holds.

### Old vs new (values per share in pence, GBp; price 2,771p; HOLD from 2,494p)
| Item | 14 Oct (ERP 5.0%) | 15 Oct (ERP 4.2%) |
|---|---|---|
| Base (Valuation agent), WACC | 1,621p SELL (-41.5%), 9.60% | **1,821p SELL (-34.3%), 8.92%** |
| Engine bear (growth 3%, WACC +1 pt) | 1,244p (-378p) | **1,386p (-435p)**, -50.0% |
| Margin 32.4% (brief bear margin) | 1,451p (-170p) | **1,636p (-185p)** |
| Margin 33.1% (old label) | 1,498p (-124p) | 1,687p (-134p) |
| Growth 3.0% | 1,476p (-146p) | 1,661p (-160p) |
| Terminal growth 1.5% | 1,573p (-49p) | 1,756p (-65p) |
| RONIC = WACC | 1,481p (-140p) | 1,632p (-189p) |
| Acquisitions 2.7% | 1,549p (-73p) | 1,748p (-73p) |
| Tax 25.0% | 1,561p (-60p) | 1,757p (-65p) |
| BBB spread 1.03% | 1,612p (-9p) | 1,810p (-11p) |
| Beta 1.195 (Damodaran 5y average) | 1,390p (-231p) | 1,586p (-235p) |
| June 2026 leverage | 1,634p (+12.5p) | 1,835p (+13p) |
| **AI case** (growth 3%, margin 32.4%, g 1.5%) | 1,274p (-347p) | **1,432p (-389p)**, -48.3% |
| **Full bear stack** (margin 32.4%) | 902p (-720p), WACC 10.62% | **1,002p (-819p)**, -63.8%, WACC 9.94% |
| Full bear stack, margin 33.1% | 938p | 1,040p |
| **NEW audit line: ERP 5.0% (Kroll)** | (the base) | **1,621p (-200p), SELL** |
| **NEW audit line: ERP 5.5% (Fernandez)** | n/a | **1,514p (-308p), SELL** |
| NEW: ERP 5.0% + BBB spread | n/a | 1,612p (-209p), SELL |
| NEW: full bear stack at ERP 5.0% / 5.5% | 902p / n/a | 902p / 845p |
| **NEW audit line: gilt 5.30% (press)** | (audit +40p) | **1,870p (+48p), SELL** |
| **NEW audit line: gilt 5.21% (US 10y)** | (audit +65p) | **1,900p (+78p), SELL** |
| Market-implied WACC / beta needed | 6.95% / 0.365 | 6.93% / **0.429** |
| Beta 0.75 / 0.66 / 0.58 / 0.38 | 1,918 / 2,067 / 2,207 / 2,673p HOLD | 2,117 / 2,264 / 2,400 / **2,844p HOLD (+2.6%)** |
| Fisher fixes (g 2.33% / 2.50% / gilt 4.94%) | +36p / +55p / +144p | +48p / +75p / +174p |
| Generous stack, gilt 4.99% (stale), beta 0.75 | 2,548p HOLD | 2,840p HOLD |
| **Generous stack, gilt 5.45%, beta 0.75, growth 7%** | 2,336p SELL | **2,586p HOLD** (flips) |
| Generous stack, gilt 5.45%, beta 0.75, growth 5% | 2,142p SELL | 2,374p SELL |
| **Generous stack, gilt 5.45%, beta 0.66, growth 5%** | 2,315p SELL | **2,546p HOLD** (flips) |
| Generous stack, beta kept at 0.973 | 2,127p SELL | 2,409p SELL |

### What flips the rating now
- **No single sourced bear or audit line changes the rating** (all SELL), and no sourced ERP or gilt reading reaches HOLD (ERP 4.2-5.5% gives 1,821p to 1,514p; gilt 5.21-5.45% gives 1,900p to 1,821p).
- **Single inputs to HOLD (Valuation agent):** WACC 7.38%, beta 0.535, gilt 3.80%, ERP 2.31%. Only one sourced input crosses: own 5y monthly beta 0.3783 (2,844p; R-squared 0.04).
- **What is new:** on 14 Oct a generous stack reached HOLD only with the stale August gilt. **At ERP 4.2% two generous stacks reach HOLD with the run-date 5.45% gilt**, but only with a lower beta (0.66 or 0.75): 2,586p and 2,546p. With the bottom-up beta (0.973) every stack is SELL.
- **Bear reading:** the lower ERP makes the bear lines bigger in pence (cash flows far out are worth more, so losing them costs more), while the beta cushion before HOLD has shrunk (0.97 vs 0.535, was 0.97 vs 0.45).

### FLAGs (re-run)
1. **The 4.2% ERP is the lowest of the sourced premiums** (Kroll 5.0%, Fernandez 5.5% US / 5.4% UK). All three were seen only in search summaries (audit). Kroll pairs its 5.0% with the 20-year Treasury (5.60%, FRED DGS20); a UK 20-year gilt yield is **MISSING**, so the "Kroll as intended" case was not run.
2. **The credit spreads are US-dollar indices** (audit M3); the BBB line (-11p) uses the same index.
3. **The gilt 5.30% press figure is secondhand** (audit V1); 5.21% is a US yield used only as a proxy.
4. **The PM's bear responses quote 14 Oct values** (902p, 6.95%, beta 0.365, gilt 3.11%, +36p to +144p, and others). I kept the PM's wording and added the new values next to it in `challenges.md`. The decision text in `docs/phase5/relx-bear-responses.md` is not mine to change.
5. **pytest not run;** no change in `desk/`. The only code change is the run-local `run_bear.py`.

**Missing (new):** UK 20-year gilt yield (for Kroll's pairing); Fernandez 2026 country figures; Kroll UK ERP. Earlier missing items below still apply.

**Confidence.** High on the mechanics (control and both ERP 5.0% cross-checks reproduce exactly). High that the SELL survives every sourced ERP and gilt. Medium that it survives a beta challenge: the beta needed for HOLD is now 0.535, close to the Blume 0.58.

---

*Everything below is the 14 Oct 2026 first run (ERP 5.0%, bear margin label 33.1%). Values are superseded by the section above.*

Money in GBP m; values per share in pence (GBp). RELX reports in pounds, so no exchange rate is used. Price 2,771p (13 Oct 2026 close). Base 1,621p, SELL; HOLD from 2,494p.

## What I did (14 Oct 2026)
1. Read the brief, `inputs.yaml`, every agent's notes (data, fundamentals, risk, valuation), `valuation.json`, `sanity_checks.json`, `risk.json`, and all `docs/phase5/relx-*.md` and `brief-relx.md`.
2. Wrote `run_bear.py`. It runs every test through `desk.valuation_run` on scratch copies in `bear/scratch/<test>/`.
   - An unchanged copy reproduces 1,621.5p and 1,243.9p exactly; the script asserts this.
   - The brief, `inputs.yaml` and `desk/` were not changed.
   - Re-run from the repo root: `PYTHONPATH=. python runs/RELX/2026-10-14/bear/run_bear.py`.
   - Results are in `bear_results.json`.
3. Fetched new evidence (kept as small extracts in `bear/scratch/downloads/`):
   - SEC XBRL acquisition cash flows FY21-25 (`acquisitions_xbrl.json`);
   - the FY21-FY25 results releases and H1 2026 release, as text, for outlook statements and AI risk wording;
   - FRED DGS10, T10YIE, DFII10, BAMLC0A3CA and BAMLC0A4CBBB for 13 Oct 2026.
4. Wrote `challenges.md`:
   - Part A: the case against buying, 5 challenges plus a stack.
   - Part B: 8 challenges against the SELL plus a generous stack.
   - Management track record, and the closing line.

## Key results (each one change from the base, engine re-run) (superseded 15 Oct 2026: ERP 5.0%; see the re-run section at the top)
| Bear line | Impact | | Against the SELL | Impact |
|---|---|---|---|---|
| Growth 3.0% | -146p | | Beta 0.75 (peer median) | +296p |
| Margin 33.1% (brief label) | -124p | | Beta 0.66 (own 5y weekly) | +445p |
| Margin 32.4% (FY23 ex print, like-for-like) | -170p | | Beta 0.58 (Blume) | +585p |
| Tax 25.0% | -60p | | **Beta 0.38 (own 5y monthly): 2,673p HOLD** | +1,051p |
| Terminal growth 1.5% | -49p | | Terminal growth 2.33% (US breakeven) | +36p |
| RONIC = WACC | -140p | | Terminal growth 2.50% (Fisher, gilt-implied) | +55p |
| Acquisitions 2.7% | -73p | | Gilt 4.94% (Fisher, US real + 2%) | +144p |
| BBB spread 1.03% | -9p | | Gilt 4.99% (FRED Aug, stale) | +128p |
| Beta 1.195 (Damodaran 5y average) | -231p | | RONIC 25.1% (book) | +90p |
| Engine bear (growth 3%, WACC +1) | -378p | | Margin 35.5% | +33p |
| AI case (growth 3%, margin 32.4%, g 1.5%) | -347p | | Growth 7% FY27-30 | +154p |
| **Stacked bear (32.4%)** | **902p (-720p)** | | **Generous stack, beta 0.75 + stale gilt** | **2,548p HOLD** |
| Stacked bear (33.1%) | 938p | | Generous stack, gilt kept at 5.45% | 2,336p SELL |

- **Does anything reach HOLD?**
  - **One single sourced input does:** beta 0.38, which has an R-squared of 0.04.
  - **The stacked generous case reaches HOLD only with a lower beta (0.66-0.75) AND the stale August gilt (4.99%).** With the run-date 5.45% gilt it is SELL (2,336p). With the base beta it is SELL (2,127p).
  - The comps median (2,990p) is also in HOLD territory.
- **Price risk (not a DCF value):** 1-year volatility is 36.0%. A 1-standard-deviation fall would take the price to 1,774p; a repeat of the -51.3% drawdown to 1,349p.

## FLAGs (14 Oct 2026; FLAG 1 resolved by PM decision 14, the other values superseded by the re-run section)
1. **Bear margin label (confirms Fundamentals FLAG 1, mistakes log row 26).** 33.1% is the FY23 group margin including print. Like-for-like (ex print) it is 32.38% = (3,030 - 253) / (9,161 - 586) (AR25 p.145, p.186). The difference is worth 47p. I suggest the PM switches the bear margin to 32.4%.
2. **Acquisitions 2.7% is confirmed.** SEC XBRL FY21-25 gives 254, 394, 124, 170 and 260 on revenue of 44,002 = **2.73% pooled** (2.80% simple average). I charge it in FY26-30 only. Terminal reinvestment comes from RONIC, and RELX's 15.4% ROIC already counts acquisitions at cost, so adding them in the terminal year would double count. FY25 acquisitions added only £14m of revenue (AR25 p.199).
3. **More leverage does not lower the value in this engine.** June 2026 leverage (beta 0.994, debt weight 15.1%) gives **+12.5p**: more weight on cheap after-tax debt beats the higher beta. Leverage is a memo risk (downgrade, refinancing), not a value line.
4. **The Fisher inconsistency is real but small in value.** A 5.45% gilt with 2.0% perpetual inflation implies a 3.38% real rate, against a 2.88% US TIPS real yield (FRED DFII10). The fix is worth +36p to +144p, and no version reaches HOLD.
   - **The UK breakeven is MISSING:** the Bank of England and DMO sites are blocked (proxy 403), and FRED has no UK series.
   - "UK real = US real" is an assumption, labelled as such.
   - The US breakeven was 2.33% on 13 Oct (the price date) and 2.35% on 14 Oct (the figure in the evidence file). I used 13 Oct.
5. **The margin "trend" test (38.6%) is a judgement, not a source.** It applies +0.9 point a year for four years from FY26, so it overstates the value. It is shown only to bound the margin argument.
6. **The AI case uses only the brief's AI-labelled lines** (growth 3%, terminal 1.5%) plus the like-for-like FY23 margin. I found no sourced estimate of the size of an AI price cut, so I did not invent one. The segment check confirms the brief's 3%: halving STM and Legal underlying growth costs 1.87 points, giving 3.1%. **Counter-evidence:** Legal growth is accelerating (+10% in H1 2026).
7. **Engine limit:** the engine cannot hold a rising margin or an exit multiple. The tests show both indirectly (flat higher margin; the terminal growth needed for 11.1x).
8. **pytest** was not run as part of this task; I changed no code in `desk/`.

## Management track record
- Qualitative outlooks were met every year from FY22 to FY25, and H1 2026 is on track.
- After 2023 the wording dropped from "above historical trends" to "strong", and underlying profit growth slowed from +15% to +9%.
- The 2025 buyback was done at an average 3,797p, 27% above today's price.

## What is missing
- UK breakeven inflation (blocked sources).
- Any sourced estimate of AI-driven price cuts in Legal or STM.
- Relevered peer betas (peer D/E not collected; the 0.75 is raw).
- A primary daily gilt (Data FLAG 2).

## Confidence (14 Oct 2026)
- **High** on the mechanics: every value comes from an engine run that reproduces the base exactly.
- **Medium** on the AI case: it is a stress test, and RELX's reported numbers so far show AI as a tailwind.
- **High** that the SELL depends on the discount rate and not on the cash flows.
