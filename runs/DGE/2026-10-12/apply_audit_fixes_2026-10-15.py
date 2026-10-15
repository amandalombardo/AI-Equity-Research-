"""Evidence audit 15 Oct 2026 (docs/audit-2026-10-15/DGE.md, finding 8): share count fix."""
import yaml
from pathlib import Path

p = Path(__file__).with_name("inputs.yaml")
inp = yaml.safe_load(p.read_text())
# Shares outstanding = issued less "own shares"; Diageo's own shares (208m) ALREADY include the employee trusts' 2m
# (20-F note 18(c) policy: own shares are held "in treasury or by employee share trusts"), so they are not deducted again
inp["shares_outstanding_m"] = {"value": 2224.0, "source": "Diageo Form 20-F FY26 (SEC accession 0001628280-26-057529, filed 2026-08-18) p.188 and XBRL: 2,432m issued - 208m own shares (treasury AND employee trusts, note 18(c)) = 2,224m ordinary shares (NOT ADRs); cross-check: weighted average shares excluding own shares 2,224m. Evidence audit 15 Oct 2026 (was 2,222m: trusts deducted twice). Basic count; dilutive options (+7m) not added, the desk's convention"}
# Debt weight (market values) = net debt / (net debt + market cap); market cap = shares x price (pence/100) x USD per GBP
mcap = 2224.0 * 1673.0 / 100 * 1.3234
inp["debt_weight"] = {"value": round(20482 / (20482 + mcap), 5), "source": f"net debt 20,482 / (net debt + market cap {mcap:,.0f} = 2,224m shares x 1673p x 1.3234 USD/GBP); shares corrected by the evidence audit 15 Oct 2026"}
p.write_text(yaml.safe_dump(inp, sort_keys=False, allow_unicode=True, width=200))
print(inp["shares_outstanding_m"]["value"], inp["debt_weight"]["value"])
