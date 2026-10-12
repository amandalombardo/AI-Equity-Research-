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
                 "Brown-Forman: April FY26; FY27 not yet reported, so it cannot be calendarised to June (2-month gap).",
       "peers_used": core.dropna(subset=["pe_ltm"])["name"].tolist(), "multiples": pe,
       "median_pe": res["median_multiple"],
       "implied_value_per_share_pence": {k: units.usd_to_pence(res[k], fx) for k in ("low", "implied_value", "high")},
       "diageo_pe_at_current_price": units.pence_to_pounds(price) * fx / eps_usd,
       "missing": core[core["pe_ltm"].isna()]["name"].tolist() + ["Constellation Brands (shown separately; data missing)"],
       "warning": "Only 2 of 4 core peers have usable data. Treat the comps value as indicative only."}
(Path(__file__).parent / "comps.json").write_text(json.dumps(out, indent=2))
pd.DataFrame({"peer": out["peers_used"], "pe_ltm": pe}).to_csv(Path(__file__).parent / "comps.csv", index=False)
print(json.dumps(out, indent=1))
