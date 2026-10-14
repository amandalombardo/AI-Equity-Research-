"""Data agent (ULVR, run 2026-10-14): add priced_at_valuation_date_meur to ../inputs.yaml (mistakes log row 24).

The part of the bridge already valued at RUN-DATE market prices, which the engine must not grow in the roll-forward:
the TMICC stake at the 13 Oct 2026 MICC.AS close (component 1 of `associates`) + the Foods consideration at the 13 Oct 2026
McCormick price (`disposal_proceeds`). JVs (Gordon on FY25 dividends), associates at book, fair-value investments (31 Dec 2025)
and the Magnum transition balance are balance-sheet-date values and are left out. Only this one key is written.
Run from the repo root:  python runs/ULVR/2026-10-14/data/add_priced_at_valuation_date.py
"""
import json
from pathlib import Path

import yaml

DATA = Path(__file__).resolve().parent
INPUTS = DATA.parent / "inputs.yaml"
inp = yaml.safe_load(INPUTS.read_text())
mkt = json.loads((DATA / "market_data.json").read_text())

tmicc = round(121_604_413 * mkt["MICC.AS"]["close"] / 1e6, 1)   # same calculation and rounding as associates component 1
assert f"= {tmicc:,.1f}" in inp["associates"]["source"], "TMICC component not found in the associates source"
disposal = inp["disposal_proceeds"]["value"]
priced = round(tmicc + disposal, 1)                               # bridge items marked to run-date market prices

before = {k: v for k, v in inp.items() if k != "priced_at_valuation_date_meur"}
inp["priced_at_valuation_date_meur"] = {"value": priced, "source":
    f"Bridge items already at run-date market prices (not grown in the roll-forward; mistakes log row 24): TMICC stake {tmicc:,.1f} "
    f"(inputs.yaml `associates` component (1): 121,604,413 shares x EUR {mkt['MICC.AS']['close']:.3f}, Yahoo MICC.AS close "
    f"{mkt['MICC.AS']['date']}) + Foods consideration {disposal:,.1f} (inputs.yaml `disposal_proceeds`: USD 15,700m cash + 499,691,175 "
    f"McCormick shares x USD {mkt['MKC']['close']:.2f}, Yahoo MKC close {mkt['MKC']['date']}, at FRED DEXUSEU) = {priced:,.1f}. "
    f"Excluded (balance-sheet-date values): JVs by Gordon growth on FY25 dividends, associates at book 15, fair-value investments 902 "
    f"(31 Dec 2025), Magnum transition balance 500."}
assert all(inp[k] == v for k, v in before.items())
INPUTS.write_text(yaml.safe_dump(inp, sort_keys=False, width=160, allow_unicode=True))
print("priced_at_valuation_date_meur =", priced, "(TMICC", tmicc, "+ disposal", disposal, ")")
