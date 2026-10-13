"""Risk agent: the ONLY script that writes `beta` to inputs.yaml (Codex audit RISK-01).

PM rule (briefs/KO.yaml dcf.wacc.beta): bottom-up beta = Damodaran US 'Beverage (Soft)' unlevered beta
(Betas by Sector (US), January 2026 update), relevered at KO's market D/E with Hamada:
    levered beta = unlevered beta x (1 + (1 - tax) x D/E)
KO's own regressions vs the S&P 500 (risk.json) are cross-checks only and never written here.

The industry number must come from the source, never from memory. If the source cannot be reached,
beta is written as MISSING - STOP and the valuation must not run.
"""
import json
import re
from pathlib import Path

import requests
import yaml

RUN = Path(__file__).resolve().parents[1]
SOURCES = [
    "https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/Betas.html",
    "https://pages.stern.nyu.edu/~adamodar/pc/datasets/betas.xls",
    "http://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/Betas.html",
    "https://www.stern.nyu.edu/~adamodar/pc/datasets/betas.xls",
    "https://web.archive.org/web/2026/https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/Betas.html",
]
UNLEVERED_FROM_SOURCE = None   # fill ONLY by reading the downloaded source; cite the URL and table row

attempts = []
for url in SOURCES:
    try:
        r = requests.get(url, timeout=30)
        attempts.append({"url": url, "result": f"HTTP {r.status_code}, {len(r.content)} bytes"})
        if r.ok:
            raise SystemExit(f"Source reachable at {url}: read the 'Beverage (Soft)' row, set UNLEVERED_FROM_SOURCE, rerun.")
    except requests.RequestException as e:
        attempts.append({"url": url, "result": f"failed: {type(e).__name__}: {str(e)[:160]}"})

inp = yaml.safe_load((RUN / "inputs.yaml").read_text())
wd, tax = inp["debt_weight"]["value"], inp["tax_rate"]["value"]
de = wd / (1 - wd)                     # market debt-to-equity from the market debt weight: D/E = wD / (1 - wD)
relever_factor = 1 + (1 - tax) * de    # Hamada relevering multiplier

if UNLEVERED_FROM_SOURCE is None:
    beta_entry = {"value": None, "status": "MISSING - STOP",
                  "source": ("MISSING. PM rule needs Damodaran US 'Beverage (Soft)' unlevered beta (Betas by Sector (US), Jan 2026). "
                             "pages.stern.nyu.edu, www.stern.nyu.edu and web.archive.org are all refused by the network proxy "
                             "(HTTP CONNECT 403, organisation policy) on 2026-10-13; not taken from memory. When obtained: "
                             f"beta = unlevered x {relever_factor:.4f} (Hamada, KO market D/E {de:.4f}, tax {tax:.1%}). "
                             "Regressions vs S&P 500 are cross-checks only: see risk/risk.json and risk/beta_evidence.json.")}
    relevered = None
else:
    relevered = UNLEVERED_FROM_SOURCE * relever_factor
    beta_entry = {"value": round(relevered, 4),
                  "source": (f"Risk agent, bottom-up: Damodaran US Beverage (Soft) unlevered beta {UNLEVERED_FROM_SOURCE} "
                             f"(Jan 2026) relevered at KO D/E {de:.4f}, tax {tax:.1%}. See risk/beta_evidence.json")}

risk_json = json.loads((Path(__file__).parent / "risk.json").read_text())
out = {"rule": "bottom-up (briefs/KO.yaml dcf.wacc.beta)", "source_attempts": attempts,
       "industry_unlevered_beta": UNLEVERED_FROM_SOURCE, "ko_market_debt_to_equity": de, "tax_rate": tax,
       "hamada_relever_factor": relever_factor, "relevered_beta": relevered, "inputs_yaml_entry": beta_entry,
       "cross_checks_not_used": {k: {"beta": v["beta"], "std_error": v["std_error"], "r_squared": v["r_squared"],
                                     "observations": v["observations"]} for k, v in risk_json["own_regressions"].items()}
       | {"peer_median_5y_monthly_levered": risk_json["peer_median_beta_core"],
          "peer_median_5y_monthly_unlevered": risk_json["peer_median_unlevered_beta_core"]}}
(Path(__file__).parent / "beta_evidence.json").write_text(json.dumps(out, indent=2))

# Write ONLY the beta key: drop any old top-level beta block, append the new one; other keys untouched.
text = (RUN / "inputs.yaml").read_text()
text = re.sub(r"(?ms)^beta:\n(?:[ \t].*\n?)*", "", text).rstrip("\n") + "\n"
text += yaml.safe_dump({"beta": beta_entry}, sort_keys=False, width=1000)
new = yaml.safe_load(text)
assert {k: v for k, v in new.items() if k != "beta"} == {k: v for k, v in inp.items() if k != "beta"}
(RUN / "inputs.yaml").write_text(text)
print(json.dumps(out, indent=1))
