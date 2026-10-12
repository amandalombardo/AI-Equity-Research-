# Bear agent notes
- Re-ran the engine with one change per challenge (`run_challenges.py`, `challenges.json`). Each challenge is a single change, except "Combined 1+2", which is labelled as such.
- I challenged every agent: Data (cost of debt, stale net debt, gross disposal proceeds), Risk (beta), Fundamentals (growth vs track record), Valuation (flow-through, terminal growth).
- FLAG: the rating flips with the discount rate alone. BUY at the base WACC (6.21%), HOLD with beta 1.0, SELL with beta 1.0 plus a market cost of debt.
- Confidence: high on the impacts (engine output). Medium on the IWSR evidence (secondhand).
