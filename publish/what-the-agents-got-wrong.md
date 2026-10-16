# What the AI agents got wrong, and how we caught it

**AI Equity Research Desk · write-up of the mistakes log, 12 to 15 October 2026 · Amanda (portfolio manager)**

Six AI agents valued four companies (Diageo, Coca-Cola, Unilever and RELX) in four days. Every error we found was written down as it happened, in a mistakes log of 34 rows (docs/mistakes-log.md, with the row numbers used below). This note is what that log teaches. Per-share values are in pence (GBp) for the three London-listed companies and in US dollars (USD) for Coca-Cola.

## The short version

- **The AI never got a sum wrong in its head, because it was never allowed to do one.** All arithmetic lives in tested Python code (the desk/ folder). The errors were all of a different kind: an assumption with no source, a number that meant something else, two items measured on different dates or over different businesses, or a rule that was changed in one place but not another.
- **The dangerous errors looked reasonable.** A sales recovery to 3 to 4% (row 1), a 5.0% equity risk premium carried from company to company (row 27) and a beta copied from a rounded search snippet (row 33) were all plausible. None had a source. Plausibility is not evidence.
- **The checks that worked were the ones built into the process.** The rule "every number needs a source, or the agent stops" and a full evidence audit caught errors that an independent maths audit had passed.
- **One error changed a rating and another nearly did.** Diageo's first run said BUY at 2,475p on a beta and cost of debt that were mechanically correct but economically meaningless (row 7). Unilever crossed from SELL to HOLD only when, on top of the lower risk premium, its growth rate was measured on the same businesses as the forecast (row 32).

## Kinds of mistake

| Kind of mistake | Rows | Example |
|---|---|---|
| A plausible number with no source | 1, 27, 33 | The 5.0% equity risk premium was copied into all four companies as a "portfolio rule"; each 0.5 point moved Unilever by about 220p |
| Like-for-like: comparing different sets of businesses or assets | 14, 16, 23, 26, 32, 34 | Unilever's FY26 growth (+0.5%) included Foods, which the model had already removed; the businesses actually valued grew +2.0% |
| Dates: items measured at different points in time | 5, 12, 15, 17, 22, 24 | Unilever's share count was after a EUR 1,507m buyback but the cash was never deducted: about 59p too high |
| Labels and units: a number that meant something else | 3, 4, 6, 18, 25, 29 | Diageo's "Revenue" tag includes excise duty (about USD 28bn) rather than net sales (about USD 20bn) |
| A correct formula giving a meaningless answer | 7, 9, 20 | Unilever's euro cash flows were first discounted with a UK gilt yield (4.99%) rather than the German Bund (3.18%): about 1.8 points of WACC |
| A rule changed in one place but not everywhere | 2, 8, 10, 13, 28 | A retired script could have overwritten Diageo's beta and turned SELL into BUY (+694p) if anyone had re-run it |
| A disclosure that was missed | 11, 19, 21, 30 | Diageo's c.USD 850m of restructuring cash for FY27-29 appeared nowhere in the model (about -30p) |
| Process | 31 | An audit sub-agent sent the PM's email address to the SEC as its contact header |

Some rows fit two kinds; each is counted once, under its main cause.

## Who caught them

| Caught by | Rows | Count |
|---|---|---|
| The builder's own reviews and tie-outs to filings (Claude Code) | 3, 4, 5, 6, 8, 9, 11, 12, 13, 14, 15, 16, 17, 19, 20, 21 | 16 |
| Another agent on the desk, or the agent itself | 7, 18, 22, 23, 24, 25, 26, 31 | 8 |
| The evidence audit and source check the PM ordered on 15 Oct, and the check at source on 16 Oct | 27, 28, 29, 30, 32, 33, 34 | 7 |
| The PM refusing an unsupported assumption | 1 | 1 |
| An automated test | 2 | 1 |
| Codex, the independent maths auditor | 10 | 1 |
| **Total** | | **34** |

Two things stand out. First, the agents checked each other: the Bear case agent rejected a beta of 0.37 with an R-squared of 0.04 (row 7), the Data agent noticed that net debt and the share count were at different dates (row 22), and the Data agent stopped the RELX run rather than guess when its download failed (row 25). Second, the independent maths audit was useful but not enough. Codex found the retired beta script (row 10) and independently confirmed the terminal-value error (row 9), but it missed the minority-interest double count (row 14) and the missing restructuring cash (row 11). Code that computes the right formula can still be fed the wrong number. Only checking each input against its source finds that.

## The five mistakes that mattered most

**1. Correct maths, wrong answer (row 7, Diageo).** The first run calculated a cost of debt of 3.81%, below the 5.22% risk-free rate, and a five-year beta of 0.37 with an R-squared of 0.04. Both were arithmetically right and economically meaningless: no lender charges Diageo less than the US government, and a beta that explains 4% of the share's moves is noise. The result was BUY at 2,475p. The PM set the cost of debt to the risk-free rate plus 1% and asked for an evidence-based beta. Of seven estimates tested, she chose the industry bottom-up beta. The rating became SELL at 1,448p.

**2. A default is still an assumption (row 27, all four companies).** The 5.0% equity risk premium (the extra return investors demand for owning shares rather than government bonds) was set for Diageo and copied into every later brief. It had no source. The PM replaced it with Damodaran's implied premium of 4.2% (1 October 2026), because that measure is built from today's market prices, like the bond yields the desk uses. All four companies were re-run. This premium still decides close calls: at 5.5% Diageo becomes a SELL by 3p.

**3. Same businesses on both sides (rows 16 and 32).** For Coca-Cola, the proposed growth guidance already included the sale of the African bottler, which the model had also removed from the base year, so the disposal would have been counted twice. The same mistake then happened again for Unilever: growth included the Foods business being sold, while the model valued only the remaining businesses. Together with the lower risk premium, fixing it moved Unilever from SELL to HOLD (4,258.5p against 4,710.5p). The lesson was written down after the first time and still repeated, which is why it is now a check on every company.

**4. Every item in the bridge needs a date (rows 12, 17, 22 and 24).** Going from the value of the business to the value per share means adding and subtracting many items: debt, dividends, buybacks, stakes, legal liabilities. Each one is measured on some date. Twice an item was counted twice because of dates: Coca-Cola's 2026 tax charge (row 17), and listed stakes already priced on the run date but grown again (row 24). Once a cash outflow was missed: Unilever's buybacks (row 22). And once a dividend was nearly deducted although the share price still included it (row 12).

**5. Copy from the source, not from a summary (row 33).** Diageo's industry beta was typed as 0.73 from a rounded search result instead of 0.7250 from the Damodaran file itself. The value moved from 1,772.1p to 1,780.2p, with no change of rating. Small, but it is the clearest example of why the desk now treats a search result only as a pointer to the real source.

## How the rules changed

Each mistake became a rule in the desk's instructions, the code or the briefs:

- Every assumption has a source in the brief, or it is written as MISSING and the run stops.
- A decision by the PM lives in a field the agents read, never only in a comment (row 28).
- When the engine changes, every company it affects is re-run (row 28).
- Growth, margins, capex and depreciation must cover the same businesses and assets as the base year (rows 16, 23, 32).
- Every item in the equity bridge carries a date, and only items at the balance-sheet date are rolled forward (rows 22, 24).
- The discount rate follows the currency of the cash flows, not of the share price (row 20).
- Inputs are copied at full precision from the source file (row 33).
- Each change of method gets an automated test, including values exactly on a rating threshold (row 2).

## How the ratings moved

Diageo's very first run said BUY at 2,475p; the fixes in rows 7, 9, 14 and 15 took it to HOLD at 1,627.3p before the final audit. The table shows each company before and after the evidence audit of 15 October.

| Company | Before the audit | Final (15 Oct 2026) vs share price | What moved it |
|---|---|---|---|
| Diageo | HOLD 1,627.3p | HOLD 1,780.2p vs 1,673p | ERP 4.2%, diluted share count, FY30-31 growth 2.0%, exact beta (rows 27, 29, 33) |
| Coca-Cola | SELL USD 47.60 | SELL USD 50.25 vs USD 90.12 | ERP 4.2%, stakes not grown twice, bear margin (rows 27, 28) |
| Unilever | SELL 3,855.3p | HOLD 4,258.5p vs 4,710.5p (borderline) | ERP 4.2%, growth on the same businesses, pension deficit (rows 27, 30, 32) |
| RELX | SELL 1,621p | SELL 1,821p vs 2,771p | ERP 4.2% (row 27) |

## What is still not verified at source

Three inputs could only be seen second-hand, because the sites that publish them block automated access from the desk. They are disclosed in each memo: the UK gilt yield of 5.45% and the German Bund yield of 3.45% (aggregator websites), and EABL's sales (press reports). Everything else in the four memos traces to a filing, a data file or a database series. The 4.2% equity risk premium was also second-hand at first; on 16 Oct 2026, once the PM allowed the desk to reach Damodaran's site, it was confirmed at source (4.20% on 1 Oct 2026).

## What I would tell another analyst using AI

Use the AI for reading, drafting and challenging, and keep the arithmetic in code you can test. Treat every number it proposes as a claim that needs a source, especially the ones that sound reasonable. And make the agents check each other: between them, the Bear case and Data agents caught four errors, against one found first by the independent auditor.
