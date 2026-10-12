# Bear agent notes
- Re-ran the engine with one change per challenge (`run_challenges.py`, `challenges.json`). Each challenge is a single change.
- I challenged every agent: Data (stale net debt, gross disposal proceeds), Risk (beta), Fundamentals (growth vs track record), Valuation (flow-through, terminal growth, credit spread).
- Re-run after the PM set cost of debt = risk-free + 1%. FLAG: beta 1.0 alone turns the BUY into a SELL (1,407p); 0% savings flow-through turns it into a HOLD (1,893p).
- Confidence: high on the impacts (engine output). Medium on the IWSR evidence (secondhand).
