# Phase 5 shortlist: which companies the desk covers next

Drafted 2026-10-13 for Amanda (PM). Nothing has been run yet; you choose first.

## What I looked for
1. **Tests the desk.** Each pick should break a different Diageo-only habit: a new reporting currency, US accounting (10-K instead of 20-F), a different year-end, a different business model.
2. **Fits a DCF.** Steady, cash-generative businesses. Banks, insurers, miners and oil majors are left out: their value is driven by capital rules or commodity prices, so the desk's DCF would mislead.
3. **Free, checkable data.** Every pick files annual accounts with the US SEC, so the Data agent can use the same source as Diageo (EDGAR) and cite every number.
4. **Supports the Phase 6 comparison.** At least one S&P 500 name alongside the FTSE 100 names.

Filing facts below were checked on SEC EDGAR today (data.sec.gov submissions API).

## Recommended three

| Company | Index | Sector | Reports in | Year-end | Latest annual filing | What it tests |
|---|---|---|---|---|---|---|
| **Unilever** (ULVR.L / UL) | FTSE 100 | Consumer staples | EUR | 31 Dec | 20-F, filed 12 Mar 2026 (FY25) | A third currency (EUR results, GBp share price); a close "branded staples" cousin of Diageo, so the comps can be reused and checked |
| **RELX** (REL.L / RELX) | FTSE 100 | Information & analytics | GBP | 31 Dec | 20-F, filed 19 Feb 2026 (FY25) | A different business: asset-light, very high returns, little inventory. Tests whether the capex, working capital and RONIC rules still make sense |
| **Coca-Cola** (KO) | S&P 500 | Beverages | USD | 31 Dec | 10-K, filed 20 Feb 2026 (FY25) | US accounting (US GAAP tags), a US share price in dollars, the S&P 500 as benchmark, no ADR. The anchor for the US side of the portfolio |

## Alternatives
- **Procter & Gamble** (PG, S&P 500): 10-K filed 4 Aug 2026, June year-end. Fresher data than Coca-Cola, but the same year-end as Diageo, so it tests less.
- **British American Tobacco** (BATS.L / BTI, FTSE 100): 20-F filed 13 Feb 2026, reports in GBP. Heavily indebted, structurally declining volumes: a strong test for the Bear agent, but a harder terminal-growth call.
- **Constellation Brands** (STZ) or **Brown-Forman** (BF-B), S&P 500 drinks peers (10-Ks filed Apr and Jun 2026). Same sector as Diageo, so they test the desk least. Better used as comps than as new coverage.

## What changes in the desk (plain language)
- The Data agent currently looks for Diageo's own labels in the SEC data (for example Diageo's "net sales"). Each new company needs its own list of labels, and Coca-Cola needs the US accounting labels. This is a code change on a branch with a PR, as usual.
- Each company gets its own brief (`briefs/<TICKER>.yaml`) with your assumptions, signed off by you before anything runs, same as Diageo.
- Currency handling grows from USD to EUR and GBP, and from London pence to US dollar prices.

## Suggested order
One company at a time, start to finish (brief, run, your checks, memo), before the next. I would start with **Coca-Cola**: it tests the most new plumbing (US accounting, dollar prices, S&P 500) and its data is simplest to verify.
