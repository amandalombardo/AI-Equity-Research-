# Paper portfolio: design choices for Amanda (15 Oct 2026)

Goal: turn the desk's four final calls into a paper portfolio and track it against the FTSE 100 and the S&P 500.
Student project, not investment advice. Each choice below has options, my recommendation, and why.

**Decision (Amanda, 15 Oct 2026 13:22 UTC): all recommended options.** They are set in `portfolio/portfolio.yaml`.

**Update (Amanda, 15 Oct 2026 13:45 UTC): Unilever re-rated SELL before the start** (choice 4, option C), because at 4,925.5p its 4,258.5p fair value is 13.5% below the price. Fair value unchanged; the memo still shows the published HOLD.

## The problem to solve first

The desk has **no BUY calls**: two HOLDs (Diageo, Unilever) and two SELLs (Coca-Cola, RELX).
A normal long-only portfolio can only own what you like, so it would hold two stocks you are neutral on and say nothing about the two SELLs, which are the desk's strongest views (-44% and -34% to fair value). The design has to test the SELLs.

## Prices today (Yahoo Finance closes, adjusted series checked 15 Oct 2026 13:20 UTC)

| Stock | Call | Fair value | Price in memo | Latest price | Upside at latest price | Band |
|---|---|---|---|---|---|---|
| Diageo | HOLD | 1,780.2p | 1,673p (12 Oct) | 1,740.0p (15 Oct) | +2.3% | HOLD |
| Unilever | HOLD (borderline) | 4,258.5p | 4,710.5p (13 Oct) | 4,925.5p (15 Oct) | **-13.5%** | **SELL territory** |
| RELX | SELL | 1,821p | 2,771p (13 Oct) | 2,849.0p (15 Oct) | -36.1% | SELL |
| Coca-Cola | SELL | USD 50.25 | USD 90.12 (13 Oct) | USD 91.78 (14 Oct) | -45.2% | SELL |

Source: query1.finance.yahoo.com chart data via `desk/data_sources.py`. London 15 Oct figures were intraday when pulled; the start prices will be the official 15 Oct closes.

**Challenge:** Unilever has risen 4.6% since the memo price. At today's price the desk rule (SELL at -10% or worse) would make it a SELL. See choice 4.

## Choice 1: how HOLD and SELL become positions

| Option | What it means | Good | Bad |
|---|---|---|---|
| A. Long-only, SELLs in cash | Put the money in the two HOLDs, nothing in KO or RELX | Anyone could do it for real; no shorting | Two-stock portfolio of HOLDs; never tests the SELLs; mostly a bet on consumer staples vs the index |
| **B. Benchmark plus active bets (recommended)** | Start with £100,000 in the benchmark. Each SELL is a paper short of £10,000 of the stock, with the £10,000 put into its home index. HOLDs get no active bet (they stay at roughly index weight) | Fund minus benchmark = exactly the value added by your calls. This is how a fund manager is judged (active return) | Needs paper shorting, which you can't easily do in a real ISA. Shorts lose without limit if the stock rallies; the update will report the loss honestly |
| C. Long the HOLDs, short the SELLs | £25,000 long each HOLD, £25,000 short each SELL | Uses all four calls | Treats HOLD as BUY, which your own rule says it is not |

Size of each SELL bet: **10% of the fund (recommended)** so the result is visible on £100,000; 5% is more typical for a real fund manager but the effect would be tiny.

Whatever you pick, the weekly update will also show a **scorecard**: each stock's return against its home index since the call (KO vs S&P 500, the other three vs FTSE 100). A SELL is right if the stock lags its index; a HOLD is right if it stays within the HOLD band.

## Choice 2: benchmark

| Option | Mix | Note |
|---|---|---|
| **A. 75% FTSE 100 / 25% S&P 500 (recommended)** | Matches where the calls are (3 UK, 1 US) | Fair comparison: you're not rewarded or punished for the UK vs US split |
| B. 50 / 50 | Equal | The fund's result would partly be a UK-vs-US bet you never made |
| C. Two separate lines, no blend | FTSE 100 and S&P 500 shown on their own | Always shown anyway, next to whichever blend you choose |

Total return, not price only, because all four stocks and both indices pay dividends, and a short seller has to pay the dividend on a shorted stock. Data: S&P 500 Total Return index (Yahoo ^SP500TR, USD) and, since Yahoo has no clean FTSE 100 total return index, the iShares Core FTSE 100 accumulating ETF (CUKX.L, GBp) as the proxy. Stocks use dividend-adjusted closes.

## Choice 3: start date and prices

| Option | Note |
|---|---|
| **A. 15 Oct 2026 closing prices (recommended)** | The day the calls were finalised and published. No hindsight. KO starts at the 15 Oct New York close |
| B. The memo price dates (12-13 Oct) | Matches the memos, but gives the desk 2-3 days it already knows the result of. A reviewer would mark this down |

## Choice 4: what happens when a price crosses a band (e.g. Unilever now)

| Option | Note |
|---|---|
| **A. Calls stay as published; the update flags any band crossing and you decide whether to re-run that company (recommended)** | Tests the memos you published. You stay in charge of rating changes. Unilever would be flagged in the first update |
| B. Re-rate mechanically from fair value vs current price at each update | Fair values never change but ratings flip with the price; the portfolio would trade on price moves, not research |
| C. Re-rate Unilever to SELL before starting | Defensible (desk rule at today's price) but changes a published call before the test begins |

## Choice 5: rebalancing

| Option | Note |
|---|---|
| **A. None; positions only change when a call changes (recommended)** | Simple to audit; real buy-and-hold test |
| B. Monthly back to target sizes | Keeps bets at 10%, but adds trades and a rule to explain |

## Defaults I'll use unless you say otherwise

- Fund currency: pounds (GBP). The KO short and its S&P 500 leg are both in US dollars, so the currency move mostly cancels; the result is converted to pounds at the Yahoo GBPUSD rate on each update date.
- Costs: none, disclosed. ETFs have no UK stamp duty; shorts are notional. A real short has a borrow fee (often small for large caps) which I can't source yet, so it is flagged as missing, not guessed.
- Horizon: 12 months to 15 Oct 2027, weekly update, with a monthly summary.
- Code goes on a branch with a pull request (new `portfolio/` folder plus tests); nothing merges without your approval.
