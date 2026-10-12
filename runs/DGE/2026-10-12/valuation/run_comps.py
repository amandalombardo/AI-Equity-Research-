"""Valuation agent comps script: desk/comps.py and desk/units.py only."""
import json
from pathlib import Path

import pandas as pd
import yaml

from desk import comps, units

RUN = Path(__file__).resolve().parents[1]
peers = pd.read_csv(RUN / "data" / "peers.csv")
inp = yaml.safe_load((RUN / "inputs.yaml").read_text())
fx = inp["fx_usd_per_gbp"]["value"]
price = inp["share_price_gbp_pence"]["value"]
eps_usd = 1.653  # Diageo FY26 EPS before exceptionals, 165.3 cents (20-F p.210). Group EPS incl. EABL.

core = peers[~peers["name"].str.contains("Constellation")]
pe = core["pe_ltm"].dropna().tolist()
res = comps.implied_values(pe, eps_usd)
out = {"method": "P/E, last reported fiscal year (LTM). Pernod Ricard: June FY26, no calendarisation needed. "
                 "Brown-Forman: April FY26 (2-month gap), Remy Cointreau: March FY26 (3-month gap), Campari: December 2025 "
                 "(6-month gap); the next fiscal years are not yet reported (or H1 not found), so they cannot be calendarised to June.",
       "peers_used": core.dropna(subset=["pe_ltm"])["name"].tolist(), "multiples": pe,
       "median_pe": res["median_multiple"],
       "implied_value_per_share_pence": {k: units.usd_to_pence(res[k], fx) for k in ("low", "implied_value", "high")},
       "diageo_pe_at_current_price": units.pence_to_pounds(price) * fx / eps_usd,
       "missing": core[core["pe_ltm"].isna()]["name"].tolist() + ["Constellation Brands (shown separately; data missing)"],
       "warning": ("4 of 4 core peers now have a P/E (Phase 3), but Campari and Remy come from press reports, not filings, "
                   "and Remy's earnings are depressed by the cognac downturn (25x). The median is more robust than the range. "
                   "EV/EBITDA is still unavailable. Treat the comps value as a cross-check, not a valuation.")}
(Path(__file__).parent / "comps.json").write_text(json.dumps(out, indent=2))
pd.DataFrame({"peer": out["peers_used"], "pe_ltm": pe}).to_csv(Path(__file__).parent / "comps.csv", index=False)
print(json.dumps(out, indent=1))
