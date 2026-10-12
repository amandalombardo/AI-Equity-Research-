# Equity research desk: rules for every agent and for Claude Code

The PM is Amanda. She does not write code. Explain anything technical to her in plain language.

1. **The maths lives in `desk/`.** Agents call these functions and never do valuation or ratio arithmetic in their heads.
2. **Assumptions live in `briefs/<TICKER>.yaml`** and are set by the PM. Agents never change them. If an agent disagrees with one, it says so in its `notes.md`.
3. **Every number needs a source** (document + page, or URL). If a number can't be found, write that it is missing and STOP. Never estimate silently.
4. **Units:** Diageo reports in USD; London prices are in pence (GBp); 1 DEO ADR = 4 ordinary shares. Label the currency on every number.
5. Each agent writes only to its own folder in `runs/<TICKER>/<RUN_DATE>/<agent>/` and finishes with a `notes.md` (what it did, FLAGs, what's missing, confidence).
6. Code changes go on a branch with a pull request. Nothing is merged without Amanda's approval. All tests (`python -m pytest`) must pass.
7. Each formula has a short comment naming the finance concept, so a finance reader can follow it.
