"""PM decision 2026-10-13 (evidence audit, docs/phase5/ko-evidence-audit.md): two input fixes."""
import yaml
from pathlib import Path

p = Path(__file__).with_name("inputs.yaml")
inp = yaml.safe_load(p.read_text())
# Contingent liability at the 31 Dec 2025 balance sheet date only: the H1 2026 accrual is 2026 tax that the
# 23.7% tax rate already charges (mistakes log row 17)
inp["contingent_liabilities"] = {"value": 14000.0, "source": "Potential IRS tax and interest 2010-2025 at 31 Dec 2025, KO FY25 10-K (accession 0001628280-26-010047; XBRL ko:IncrementalTaxAndInterestLiability = 14,000m). PM decision 2026-10-13: assume KO loses; H1 2026 accrual (USD 900m, Q2 2026 10-Q) excluded because the 23.7% tax rate already charges 2026 onwards (mistakes log row 17)"}
# Capex intensity = FY25 purchases of PP&E / net operating revenues (latest actual, in line with FY26 guidance c.$2.2bn)
inp["capex_pct_sales"] = {"value": round(2112 / 47941, 5), "source": "FY25 purchases of property, plant and equipment 2,112 / net operating revenues 47,941, KO FY25 10-K (accession 0001628280-26-010047; XBRL us-gaap:PaymentsToAcquirePropertyPlantAndEquipment, us-gaap:Revenues). PM decision 2026-10-13 (evidence audit): latest actual instead of the 5-year average (3.99%), which included Covid-era 2021; FY26 guidance capex c.$2.2bn (Q2 2026 8-K 0001628280-26-049922)"}
p.write_text(yaml.safe_dump(inp, sort_keys=False, allow_unicode=True, width=200))
print(inp["contingent_liabilities"]["value"], inp["capex_pct_sales"]["value"])
