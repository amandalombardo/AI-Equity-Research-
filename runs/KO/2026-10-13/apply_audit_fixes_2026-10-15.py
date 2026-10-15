"""Evidence audit 15 Oct 2026 (docs/audit-2026-10-15/KO.md, finding 2): listed stakes are not grown twice."""
import yaml
from pathlib import Path

p = Path(__file__).with_name("inputs.yaml")
inp = yaml.safe_load(p.read_text())
# Roll-forward: the listed stakes are already at 13 Oct 2026 market prices, so growing them at the cost of equity from
# 31 Dec 2025 would count the time value twice (mistakes log row 24, the rule added for Unilever in PR #6)
inp["priced_at_valuation_date_musd"] = {"value": 39539.5, "source": "Listed equity stakes at run-date (13 Oct 2026) market value, the 39,539.5 inside 'associates' (data/associates_rollforward_check.csv, Yahoo/FRED). Added by the evidence audit 15 Oct 2026: KO was valued before the desk learned to keep run-date values out of the roll-forward (mistakes log row 24)"}
p.write_text(yaml.safe_dump(inp, sort_keys=False, allow_unicode=True, width=200))
print(inp["priced_at_valuation_date_musd"]["value"])
