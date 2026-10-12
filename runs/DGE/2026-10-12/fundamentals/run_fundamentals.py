"""Fundamentals agent script: every ratio comes from desk/fundamentals.py."""
from pathlib import Path

import pandas as pd

from desk import fundamentals as f

RUN = Path(__file__).resolve().parents[1]
fin = pd.read_csv(RUN / "data" / "financials.csv")


def v(item, fy):
    s = fin[(fin["item"] == item) & (fin["fiscal_year"] == fy)]["value_musd"]
    return float(s.iloc[0]) if len(s) else None


# organic growth as published (20-F KPI tables: FY23 20-F p.KPIs, FY24, FY25, FY26 20-F p.13)
organic = {2023: (0.065, 0.070), 2024: (-0.006, -0.048), 2025: (0.017, -0.007), 2026: (-0.020, 0.020)}
tax_bei = {2025: 0.249, 2026: 0.243}
rows = []


def add(item, year, value, formula, inputs):
    rows.append({"item": item, "year": year, "value": None if value is None else round(value, 4),
                 "formula": formula, "inputs": inputs})


for y in range(2022, 2027):
    ns, opb, opr = v("net_sales", y), v("operating_profit_bei", y), v("operating_profit_reported", y)
    gp, da = v("gross_profit", y), v("depreciation_amortisation", y)
    fcf = v("operating_cash_flow", y) - v("capex", y) + v("proceeds_from_ppe_disposals", y)
    npo, nd = v("net_profit_to_owners", y), v("net_borrowings", y)
    ebitda = v("adjusted_ebitda", y)
    ni = -v("net_interest", y)
    if y > 2022:
        add("reported_net_sales_growth", y, f.growth(ns, v("net_sales", y - 1)), "net sales / prior net sales - 1", f"{ns}, {v('net_sales', y - 1)}")
    if y in organic:
        add("organic_net_sales_growth", y, organic[y][0], "as published by Diageo", "20-F KPI table")
        add("organic_operating_profit_growth", y, organic[y][1], "as published by Diageo", "20-F KPI table")
    add("gross_margin", y, f.margin(gp, ns), "gross profit / net sales", f"{gp}, {ns}")
    add("operating_margin_bei", y, f.margin(opb, ns), "operating profit before exceptionals / net sales", f"{opb}, {ns}")
    add("operating_margin_reported", y, f.margin(opr, ns), "reported operating profit / net sales", f"{opr}, {ns}")
    add("free_cash_flow_musd", y, fcf, "operating cash flow - capex + PP&E disposal proceeds (Diageo definition)",
        f"{v('operating_cash_flow', y)}, {v('capex', y)}, {v('proceeds_from_ppe_disposals', y)}")
    add("cash_conversion", y, f.cash_conversion(fcf, npo), "free cash flow / net profit to shareholders (reported)", f"{fcf}, {npo}")
    add("net_debt_to_ebitda", y, f.leverage(v("adjusted_net_borrowings", y), ebitda), "adjusted net borrowings / adjusted EBITDA (Diageo definition)",
        f"{v('adjusted_net_borrowings', y)}, {ebitda}")
    add("interest_cover", y, f.interest_cover(opb, ni), "operating profit before exceptionals / net interest charge", f"{opb}, {ni}")
    if y in tax_bei:
        add("roic_published", y, {2025: 0.137, 2026: 0.134}[y], "as published by Diageo (20-F p.211)", "Diageo calculation")
pd.DataFrame(rows).to_csv(Path(__file__).parent / "ratios.csv", index=False)
print(pd.DataFrame(rows).pivot(index="item", columns="year", values="value").to_string())
