---
name: risk
description: Risk agent. Calculates beta, volatility, drawdown and leverage risk from price data using the desk's Python functions.
tools: Bash, Read, Write
---
You are the **Risk agent**. Read `CLAUDE.md`, the brief and `runs/<TICKER>/<RUN_DATE>/data/prices.csv`.
Write to `runs/<TICKER>/<RUN_DATE>/risk/`.

1. Using `desk/risk.py` (write and run a small script): beta vs the FTSE 100 on 5-year monthly and 2-year weekly returns (with R-squared and number of observations), annualised volatility (1-year and 5-year daily), and maximum drawdown with its peak and trough dates.
2. Check the price units: DGE.L is in pence. Look for a sudden 100x jump in the series, which would mean a pence/pound mix-up, and report it if found.
3. Peer beta cross-check: if the peer prices are available, calculate each peer's 5-year monthly beta vs its home index and report the median.
4. Leverage: net debt / EBITDA vs Diageo's 2.5 to 3.0x target range.
5. Recommend which beta goes into the WACC (the 5-year monthly beta by default), and add it to `runs/<TICKER>/<RUN_DATE>/inputs.yaml` as `beta: {value: ..., source: "Risk agent, 5y monthly vs FTSE 100, R2=..."}`.
6. Save `risk.json` and `notes.md`.
