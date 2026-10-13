# Coca-Cola (KO): fundamentals commentary, FY21-FY25 (USD)

Sources: `ratios.csv` and `segments.csv` in this folder (all from `runs/KO/2026-10-13/data/` and the SEC filings cited there).

**Growth.** Organic revenue growth (non-GAAP, as published) slowed from 16% (FY21, FY22) to 12% (FY23, FY24) and 5% (FY25). Reported USD growth was much lower in FY22-FY24: 11.3%, 6.4% and 2.9%. The gap is currency (minus 7, 4 and 5 points, ko-growth-evidence.md), mainly Argentina, where inflation-driven pricing lifted organic growth while the peso fell. Bottler sales took a further 4 points off FY24. In FY25 reported growth was 1.9% against 5% organic. By segment (FY25), Latin America grew 10% organic but fell 2% reported. North America grew 4% on both measures.

**Margins.** Gross margin rose from 58.1% (FY22) to 61.6% (FY25). Comparable operating margin rose every year from FY22: 28.7%, 29.1%, 30.0%, 31.2%. Reported operating margin is noisier: 21.2% in FY24, then 28.7% in FY25. The comparable rise partly reflects shrinking low-margin Bottling Investments: revenue down 8% reported in FY25, at a 7.4% comparable margin, against 30-60% for the concentrate segments.

**Returns.** ROIC on comparable operating income at the DCF tax rate of 23.7% was 25.0%, 27.5%, 27.9% and 27.0% (FY22-FY25). Excluding the $6.0bn IRS deposit from capital, FY25 is 31.4%.

**Cash.** Reported cash conversion fell from 115% (FY21) to 45% (FY24) and 40% (FY25). Excluding the IRS deposit ($6,041m) and the fairlife payment ($6,069m), it was 101% and 87%. That is close to the FY22-FY23 levels (100%, 91%).

**Leverage.** Net debt was steady at $27.5-30.1bn. Net debt / comparable EBITDA fell from 2.4x to 1.8x. Net interest cover (reported) was 15.9x in FY25. On a comparable gross basis it was 8.9x.

## Flags
1. **FY24 reported margin dip is an exceptional item, not trading.** The reported operating margin was 21.2% against 30.0% comparable. The gap is $3,118m of transaction losses (of which the fairlife contingent-consideration remeasurement was $3,109m) plus $886m of asset impairments (North America $760m, Latin America $126m). Source: Q4 2025 8-K 0001628280-26-006642 p.28. So the FY25 reported operating income jump of +38% is mostly the absence of that charge. FY25 still carries $1,045m of impairments (North America $960m).
2. **Cash conversion denominators are distorted.** FY24 net profit is depressed by the non-cash fairlife charge, which is why FY24 ex-one-off conversion is above 100%. FY25 net profit ($13,107m) includes other income (net) of $1,073m (10-K p.117). Comparable cash conversion was not computed.
3. **Interest cover in FY21-FY22 swings on non-comparable interest.** Reported interest expense was $1,597m (FY21) and $882m (FY22), against comparable interest expense of $776m and $906m (Q4 2022 8-K 0000021344-23-000005). Net reported cover of 25.2x in FY22 is an outlier. Use the comparable gross cover (8.4x to 14.3x).
4. **FY25 net debt excludes CCBA.** The $1,435m of CCBA debt and $178m of cash sit in held-for-sale. Including them, net debt is $30,943m, or 1.93x comparable EBITDA.
5. **Segments do not match the template regions.** Coca-Cola has no separate Europe or Africa segment. Africa sits inside EMEA (concentrate) and Bottling Investments (CCBA). Global Ventures (Costa) was folded into EMEA on 1 Jan 2025 (10-K Item 1), so pre-FY24 segment history is not comparable. The 10-K does not publish organic growth by segment; it comes from the Q4 2025 8-K. Segment margins use total segment revenue, including intersegment sales.
6. **Organic growth is published only to the whole percent.** There are no decimals, so the organic vs reported gaps are approximate.
7. **ROIC FY21 is MISSING.** It needs FY20 invested capital, which is not in the data folder.
8. **Desk code comment.** The docstring on `desk/fundamentals.py` `leverage()` says "the company's own target range is 2.5 to 3.0x". That is Diageo's range, not Coca-Cola's. No Coca-Cola leverage target was sourced. I have not changed the code (not my folder).
9. **The margin trend includes a mix effect.** Part of the FY23-FY25 comparable margin rise comes from selling low-margin bottlers. This is consistent with the brief's choice not to extrapolate it.
