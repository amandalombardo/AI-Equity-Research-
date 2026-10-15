"""Source check 15 Oct 2026 (mistakes log row 33): the industry beta was typed as 0.73 from a rounded search snippet.
Damodaran's own file (betaGlobal.xls, 5 Jan 2026, uploaded by the PM, sheet "Industry Averages", Beverage (Alcoholic),
217 firms) gives 0.725044 (unlevered, corrected for cash) and 0.688411 (before the cash correction). This relevers the
exact figure at Diageo's CURRENT market D/E (after the 15 Oct diluted share count) without re-downloading prices.
Run from repo root: python3 runs/DGE/2026-10-12/risk/fix_beta_2026-10-15.py
"""
import json
from pathlib import Path
import yaml

RUN = Path(__file__).resolve().parents[1]
UNLEVERED_CASH_CORRECTED = 0.725044343989413  # betaGlobal.xls, Beverage (Alcoholic), "Unlevered beta corrected for cash"
UNLEVERED = 0.688411077891109                 # same row, "Unlevered beta" before the cash correction

inp = yaml.safe_load((RUN / "inputs.yaml").read_text())
wd, tax = inp["debt_weight"]["value"], inp["tax_rate"]["value"]
de = wd / (1 - wd)  # market debt-to-equity = debt weight / equity weight
# Bottom-up beta (Hamada relevering): levered beta = unlevered beta x (1 + (1 - tax rate) x D/E)
beta = UNLEVERED_CASH_CORRECTED * (1 + (1 - tax) * de)

ev = json.loads((RUN / "risk" / "beta_evidence.json").read_text())
ev["bottom_up"].update({
    "industry_unlevered_beta_cash_corrected": UNLEVERED_CASH_CORRECTED, "industry_unlevered_beta": UNLEVERED,
    "diageo_market_debt_to_equity": de, "tax_rate": tax, "relevered_beta": beta,
    "relevered_beta_without_cash_correction": UNLEVERED * (1 + (1 - tax) * de),
    "source": ("Damodaran, Betas by Sector (Global), file betaGlobal.xls dated 5 Jan 2026 (uploaded by the PM 14 Oct 2026, "
               "/mnt/project-files/equity-desk/phase5/data/betaGlobal.xls), sheet Industry Averages, Beverage (Alcoholic), 217 firms. "
               "Source check 15 Oct 2026: was 0.73 / 0.69 rounded from a search snippet (mistakes log row 33)"),
    "previous_relevered_beta": 0.9601})
ev["recommended_beta"] = beta
(RUN / "risk" / "beta_evidence.json").write_text(json.dumps(ev, indent=2))

inp["beta"] = {"value": float(round(beta, 4)),
               "source": (f"Risk agent, bottom-up: Damodaran global alcoholic beverages unlevered beta corrected for cash 0.7250 "
                          f"(betaGlobal.xls, 5 Jan 2026, 217 firms) relevered at Diageo market D/E {de:.4f} (debt weight {wd}), "
                          f"tax {tax:.1%}. Source check 15 Oct 2026: was 0.9601 from a rounded 0.73 (mistakes log row 33). "
                          f"See risk/beta_evidence.json")}
(RUN / "inputs.yaml").write_text(yaml.safe_dump(inp, sort_keys=False, allow_unicode=True, width=200))
print("D/E", round(de, 4), "beta", round(beta, 4))
