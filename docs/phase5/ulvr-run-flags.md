# Unilever: what the Data agent found (run 14 Oct 2026), and what needs the PM

The Data agent tied every FY25 figure to the filings (turnover, underlying operating profit, free cash flow and net debt all within 0.5%). It also found items the brief did not cover. Pence figures use €1 = £0.8461 (EUR 1.1819 per GBP, FRED, 9 Oct 2026) and 2,154.3m shares. Full detail: runs/ULVR/2026-10-14/data/notes.md.

## Fixed without a decision (a consistency error, not an assumption)
**1. The 2026 share buyback (about 59p a share too high).** Net debt is at 31 Dec 2025, before Unilever spent **€1,507m** buying back 30.7m shares in H1 2026 (H1 2026 6-K cash flow; Total Voting Rights 6-K, 1 Sep 2026). But the share count (2,154.3m) is after the buyback. Using one date for the debt and another for the shares overstated value by €1,507m. The desk now deducts buybacks in the roll-forward, exactly like dividends (code change on PR #6, tested). Mistakes log row 22.

## Four items for the PM (evidence and recommendation for each)

### A. Capex should include software (my error, mistakes log row 23)
The agreed capex of 2.8% counts only property, plant and equipment (€1,417m). But the agreed D&A of 2.6% (€1,310m) includes amortisation of software and other intangibles. Unilever also spent **€174m** on intangibles in FY25 (€233m in FY24) (20-F XBRL `PurchaseOfIntangibleAssetsClassifiedAsInvestingActivities`). Counting the amortisation but not the spending flatters cash flow.

| Option | Capex % of sales | Basis |
|---|---|---|
| **Recommended** | **3.15%** | FY25 (1,417 + 174) / 50,503. FY24 was 3.08% on the same basis |
| Keep | 2.8% | PP&E only (inconsistent with D&A) |

### B. Joint ventures: worth far more than book value
Unilever's share of joint-venture profit was **€245m** in FY25 (€250m FY24), and it received **€229m** of dividends from them (20-F income statement; note 11, p.158). Most comes from the Pepsi Lipton tea partnerships (50% US, 45.45% rest of world, 20-F related undertakings). Those partnerships stay with Unilever: Lipton Ready-to-Drink is outside the Foods sale (Form 425). The JV profit sits **below** operating profit, so the DCF does not include it, and the brief carries the JVs at book value: **€109m (c.4p)**.

| Option | Value | Basis |
|---|---|---|
| Book | €109m (c.4p) | Brief rule from KO (unlisted stakes at book). For KO the unlisted stakes were small; here book is about half of one year's dividends, so it fails the evidence test |
| **Recommended: cash-flow value** | €229m of dividends as a growing perpetuity at Unilever's cost of equity and the agreed 1.6% growth (Gordon growth). The Valuation agent computes it with the run's cost of equity | Uses the cash Unilever actually receives, valued with the same discount rate and growth as the rest of the company |
| Multiple | 10x profit = €2.45bn (c.96p) | Simple, but the multiple is a choice with no specific source |

### C. Other financial investments (about €0.9-1.3bn)
Non-current financial assets in the FY25 20-F (note 17A) include, beyond the Magnum stake and derivatives already in net debt: other equity investments at fair value **€561m**, assets at fair value through profit or loss **€341m**, and assets at amortised cost **€368m** (of which judicial deposits €175m). None of these is in net debt or the bridge, and their income is not in operating profit.

| Option | Added | Per share |
|---|---|---|
| **Recommended** | The two fair-value lines, **€902m** | c.35p |
| All | €1,270m | c.50p |
| None | 0 | 0 |

The amortised-cost assets are left out because judicial deposits are cash lodged with courts while legal cases run (not available to shareholders), and the filing does not describe the rest.

### D. Temporary balances with Magnum Ice Cream
Unilever still runs services for Magnum Ice Cream under a transition agreement that ends within two years of the demerger (Dec 2027 at the latest). At 31 Dec 2025, receivables include **€2.1bn due from** Magnum Ice Cream and payables **€1.6bn due to** it (20-F notes 13 and 14). The Data agent removed only the payable from working capital, which was one-sided.

| Option | Working capital % of sales | Bridge |
|---|---|---|
| **Recommended** | **-11.98%** (both balances removed) | add the net **€0.5bn** owed to Unilever as cash to come (c.20p) |
| Data agent's version | -7.82% (payable removed only) | nothing |
| Raw | -10.99% (both left in) | nothing |

## Left as agreed, stated in the memo
- **Deal timing:** the Foods payment arrives at closing (about 0.7 years away). Each 1 point of discount rate is about €239m (9p). Foods' cash flows until closing belong to Unilever but are not disclosed. These partly offset (decision 1 stands).
- **Tax on the Foods cash:** still not disclosed; each €1bn = 39p (decision 5 stands).
- **Price date:** every price is the 13 Oct 2026 close (the download script picked up an intraday London price on 14 Oct; to be fixed).
