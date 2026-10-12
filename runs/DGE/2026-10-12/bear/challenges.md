# Bear case: Diageo (DGE), run 2026-10-12 (latest re-run: debt at risk-free + 1%, beta 0.96 bottom-up)

Base case: **1,448p (-13.5% vs 1,673p, SELL)** at a WACC of 8.46%. The engine's bear scenario (no growth, 25% flow-through, WACC +1 point) gives 1,071p (-36.0%).
The base case is now itself bearish, so this file does two jobs. It shows what could make it worse (challenges 3-6). It also shows, as a check on our own pessimism, the strongest case **against selling** (challenge 1).
For each challenge, I re-ran `desk.valuation_run` with one change (`run_challenges.py`, results in `challenges.json`).

## 1. Against our SELL: the beta may be too high (challenges the Risk agent): **+290p**
**Claim:** Diageo's own best regression beta is 0.72 (5y weekly vs FTSE 100, standard error 0.11). The bottom-up 0.96 sits just above its 95% range. At 0.72, WACC is 7.61% and the value is 1,738p: **HOLD, +3.9%.** The market is pricing a WACC of about 7.8%. For reference, the rejected 0.48 gives 2,141p (BUY).
**Evidence:** `risk/beta_evidence.json`.

## 2. A 1% credit spread may be too tight (challenges the PM's debt rule): **-64p**
Leverage of 3.1x is above the range Diageo calls "broadly consistent with an A-band credit rating" (20-F p.186). A 2.0% spread gives 1,384p (-64p).

## 3. Savings flow-through: management says the savings will be reinvested (challenges the Valuation assumptions): **-91p to -181p**
Diageo says "these savings will allow us to invest without reducing operating profit" (20-F p.21). 25% flow-through gives 1,357p (-91p). 0% gives 1,266p (-181p).

## 4. Terminal growth of 2% vs a shrinking spirits market (challenges the Data agent's industry check): **-110p**
IWSR reports that spirits volumes fell 3% in 2025, and it sees volumes down about 2% by 2035 (secondhand). Terminal growth of 1.5% gives 1,338p (-110p).

## 5. Management's track record (challenges the Fundamentals agent): **-49p**
Every 2023-26 incentive target was missed: organic sales CAGR -0.3% vs a 4.0% threshold, organic profit CAGR -3.4% vs 4.5% (20-F p.110). Zero growth gives 1,398p (-49p).

## 6. Net debt is stale (challenges the Data agent): **-23p**
The 30c final dividend (about 667) is paid after the run date. Deducting it gives 1,425p (-23p).

## Not quantified
- Minorities at book value (2,083); USL's listed minority is worth more. Disposal proceeds are gross and not yet received.

**Strongest reason not to buy: on any beta the evidence supports (0.60 or above), the stock is at best fairly valued, and at the industry beta it is worth 1,448p, 13.5% below the price.**
