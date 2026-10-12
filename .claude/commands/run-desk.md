---
description: Run the full six-agent equity research desk on one company, e.g. /run-desk DGE
argument-hint: <TICKER>
---
Run the equity research desk for **$ARGUMENTS**. Set RUN_DATE to today's date (YYYY-MM-DD) and create `runs/$ARGUMENTS/<RUN_DATE>/`.

Run the agents **in this order**, waiting for each to finish, and pass them the ticker and run folder:
1. `data` agent
2. `risk` agent (it needs the prices and adds beta to inputs.yaml)
3. `fundamentals` agent
4. `valuation` agent
5. `bear` agent
6. `editor` agent

After each agent, read its `notes.md`. If it reports a STOP, halt the run and tell the PM exactly what is missing. Do not work around it.

At the end, give the PM:
- a **key numbers table** to check against her Excel model: base sales, margin, tax rate, WACC (and its parts), each year's FCF, terminal value, EV, equity value, value per share (USD and pence), share price, upside, and rating
- every FLAG raised by any agent
- the paths to `memo.pdf` and `dcf.xlsx`
- suggested entries for the mistakes log (anything an agent got wrong and how it was caught).
