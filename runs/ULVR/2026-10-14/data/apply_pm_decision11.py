"""Data agent (ULVR, run 2026-10-14): PM decision 11 (14 Oct 2026) - risk_free = German 10-year Bund on the run date.

Writes only `risk_free` in ../inputs.yaml; then re-run apply_pm_decision10.py (the JV Gordon value uses the cost of equity).
Run from the repo root:  python runs/ULVR/2026-10-14/data/apply_pm_decision11.py
"""
from pathlib import Path

import yaml

INPUTS = Path(__file__).resolve().parent.parent / "inputs.yaml"
inp = yaml.safe_load(INPUTS.read_text())
old = inp["risk_free"]["value"]
inp["risk_free"] = {"value": 0.0345, "source":
    "PM decision 14 Oct 2026 (decision 11; briefs/ULVR.yaml wacc.risk_free comment; docs/phase5/ulvr-evidence-audit.md): German 10-year "
    "Bund yield on the run date, 3.45% on 14 Oct 2026 (Trading Economics https://tradingeconomics.com/germany/government-bond-yield; also "
    "Bloomberg rates page https://www.bloomberg.com/markets/rates-bonds); cross-check 3.50% on 9 Oct 2026 "
    "(https://www.thetrading.tools/germany-10-year-yield). Replaces FRED IRLTLT01DEM156N (OECD monthly average, latest Aug 2026 = 3.18%, "
    "two months old). FLAG: data aggregator, not a primary source; the Bundesbank and ECB daily series (and these aggregator pages) are "
    "blocked from the Data agent's environment, so the Data agent could not re-check the 3.45% figure itself (PM-supplied, from the evidence audit)."}
INPUTS.write_text(yaml.safe_dump(inp, sort_keys=False, width=160, allow_unicode=True))
print(f"risk_free {old} -> {inp['risk_free']['value']}")
