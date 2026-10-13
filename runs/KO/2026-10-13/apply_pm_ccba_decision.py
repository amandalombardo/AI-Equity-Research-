"""PM decision 2026-10-13: remove CCBA from the base year using Coca-Cola HBC's published deal figures,
and value listed stakes at run-date market prices (brief rule). Rewrites five inputs; everything else untouched."""
import csv
import yaml
from pathlib import Path

p = Path(__file__).with_name("inputs.yaml")
inp = yaml.safe_load(p.read_text())
CCHBC = ("Coca-Cola HBC CCBA acquisition announcement, 21 Oct 2025 (factsheet https://www.coca-colahellenic.com/content/dam/cch/us/"
         "documents/investors-and-financial/2026-q1-trading-update/coca-cola-hbc-factsheet-ccba-acquisition-q1-2026.pdf.downloadasset.pdf"
         " and acquisition presentation): CCBA 2024 net sales revenue EUR 3,357m, EBIT EUR 246m; KO sells 41.5% for USD 1.3bn, keeps 25%;"
         " 100% equity value USD 3.4bn. Seen via web search; page not reachable from this environment, PM asked to verify")
EURUSD_2024 = 1.0819996  # FRED DEXUSEU, 2024 average of 251 daily values
ccba_sales = 3357 * EURUSD_2024  # FX conversion: EUR m x USD per EUR = USD m
ccba_ebit = 246 * EURUSD_2024
# base year ex-disposal: reported FY25 net operating revenues less the business being sold
base_sales = 47941 - ccba_sales
# comparable operating margin ex-CCBA = (comparable EBIT - CCBA EBIT) / (comparable revenue - CCBA revenue)
base_margin = (15013 - ccba_ebit) / (48062 - ccba_sales)
# listed stakes at run-date market value (Data agent roll-forward: price and FX change applied to 31 Dec 2025 fair values)
with open(Path(__file__).parent / "data" / "associates_rollforward_check.csv") as f:
    listed_run = sum(float(r["value_run_date_musd"]) for r in csv.DictReader(f))
retained_25 = 0.25 * 3400  # kept 25% of CCBA at the deal's equity value
inp["base_sales"] = {"value": round(base_sales, 1), "source": f"FY25 10-K net operating revenues 47,941 less CCBA {ccba_sales:.1f} (EUR 3,357m x {EURUSD_2024:.4f} USD/EUR, FRED DEXUSEU 2024 average). {CCHBC}. FLAG: CCBA figure is calendar 2024. PM decision 2026-10-13"}
inp["base_margin"] = {"value": round(base_margin, 5), "source": f"(comparable operating income 15,013 - CCBA EBIT {ccba_ebit:.1f}) / (comparable revenues 48,062 - CCBA {ccba_sales:.1f}); Q4 2025 8-K 0001628280-26-006642 + {CCHBC}. PM rule: held flat. PM decision 2026-10-13"}
inp["disposal_proceeds"] = {"value": 1300.0, "source": f"KO's 41.5% of CCBA sold for USD 1.3bn, not yet received (Q2 2026 10-Q: not closed). {CCHBC}. PM decision 2026-10-13"}
inp["associates"] = {"value": round(listed_run + 6236 + retained_25, 1), "source": f"Listed stakes at run-date market value {listed_run:.1f} (data/associates_rollforward_check.csv: 31 Dec 2025 fair values from FY25 10-K x price and FX change to 13 Oct 2026, Yahoo/FRED) + unlisted equity-method investments at book 6,236 (FY25 10-K: 20,235 - listed book 13,999) + retained 25% of CCBA at deal value {retained_25:.0f} (0.25 x USD 3.4bn, {CCHBC}). PM rule: listed stakes at run-date market value"}
inp["minority_interests"]["source"] += " FLAG (PM informed 2026-10-13): includes CCBA's outside shareholder (Gutsche 33.5%), not disclosed; full amount deducted (conservative, up to c.USD 1.1bn too much)."
p.write_text(yaml.safe_dump(inp, sort_keys=False, allow_unicode=True, width=200))
print(round(base_sales, 1), round(base_margin, 5), round(listed_run, 1), inp["associates"]["value"])
