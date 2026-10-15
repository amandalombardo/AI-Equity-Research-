# Bear agent notes: RELX PLC (RELX / REL.L), run 2026-10-14

Money in GBP m; values per share in pence (GBp). RELX reports in pounds, so no exchange rate is used. Price 2,771p (13 Oct 2026 close). Base 1,621p, SELL; HOLD from 2,494p.

## What I did
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

## Key results (each one change from the base, engine re-run)
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

## FLAGs
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

## Confidence
- **High** on the mechanics: every value comes from an engine run that reproduces the base exactly.
- **Medium** on the AI case: it is a stress test, and RELX's reported numbers so far show AI as a tailwind.
- **High** that the SELL depends on the discount rate and not on the cash flows.
