"""Write the base-case DCF to Excel with live formulas, so the PM can audit it and
compare it line by line with her own model. A 'Python check' column shows the value
the code calculated; if the Excel formula and the Python value disagree, one is wrong."""
from __future__ import annotations

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter

BOLD = Font(bold=True)
INPUT_FILL = PatternFill("solid", fgColor="FFF2CC")  # yellow = input


def write_dcf_workbook(path, brief: dict, v: dict, sources: dict, base: dict) -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "Inputs"
    d = brief["dcf"]
    inputs = [
        ("base_sales", "Base-year net sales ex-EABL (USD m)", v["base_sales"]),
        ("base_margin", "Base operating margin before exceptionals", v["base_margin"]),
        ("tax_rate", "Tax rate", v["tax_rate"]),
        ("da_pct", "D&A % of sales", v["da_pct_sales"]),
        ("capex_pct", "Capex % of sales", v["capex_pct_sales"]),
        ("nwc_pct", "Net working capital % of sales", v["nwc_pct_sales"]),
        ("flow_through", "Savings flow-through", d["savings"]["flow_through"]),
        ("rf", "Risk-free rate (US 10y)", v["risk_free"]),
        ("erp", "Equity risk premium", d["wacc"]["equity_risk_premium"]),
        ("beta", "Beta", v["beta"]),
        ("kd", "Pre-tax cost of debt", v["pre_tax_cost_of_debt"]),
        ("wd", "Debt weight D/(D+E)", v["debt_weight"]),
        ("g", "Terminal growth", d["terminal_growth"]),
        ("stub", "Fraction of FY27 elapsed at valuation date", v["stub_years"]),
        ("net_debt", "Net debt (USD m)", v["net_debt"]),
        ("leases", "Lease liabilities not in net debt (USD m)", v["lease_liabilities"]),
        ("minorities", "Minority interests (USD m)", v["minority_interests"]),
        ("pension", "Pension deficit (USD m)", v["pension_deficit"]),
        ("associates", "Associates incl. Moet Hennessy (USD m)", v["associates"]),
        ("disposals", "Disposal proceeds not in net debt (USD m)", v["disposal_proceeds"]),
        ("shares", "Ordinary shares (m)", v["shares_outstanding_m"]),
        ("fx", "USD per GBP", v["fx_usd_per_gbp"]),
        ("price", "Share price (pence)", v["share_price_gbp_pence"]),
    ]
    ws.append(["Input", "Value", "Source"])
    for c in ws[1]:
        c.font = BOLD
    ref = {}
    source_key = {"da_pct": "da_pct_sales", "capex_pct": "capex_pct_sales", "nwc_pct": "nwc_pct_sales", "rf": "risk_free",
                  "kd": "pre_tax_cost_of_debt", "wd": "debt_weight", "stub": "stub_years", "leases": "lease_liabilities",
                  "minorities": "minority_interests", "pension": "pension_deficit", "disposals": "disposal_proceeds",
                  "shares": "shares_outstanding_m", "fx": "fx_usd_per_gbp", "price": "share_price_gbp_pence"}
    for i, (key, label, val) in enumerate(inputs, start=2):
        src = sources.get(source_key.get(key, key)) or "PM assumption (briefs/DGE.yaml)"
        ws.append([label, val, src])
        ws.cell(row=i, column=2).fill = INPUT_FILL
        ref[key] = f"Inputs!$B${i}"
    ws.column_dimensions["A"].width = 46
    ws.column_dimensions["C"].width = 70

    s = wb.create_sheet("DCF")
    rows = base["dcf"]["rows"]
    n = len(rows)
    cols = [get_column_letter(3 + i) for i in range(n)]  # C.. for forecast years; B = base year
    s.append(["USD m", "FY26 base"] + [f"FY{r['year'] % 100}" for r in rows] + ["", "Python check (final year)"])
    labels = ["Growth", "Net sales", "Savings kept", "EBIT", "Tax", "NOPAT", "D&A", "Capex", "Increase in NWC",
              "Unlevered FCF", "Cash flow counted", "Discount period", "Discount factor", "PV of FCF"]
    for lab in labels:
        s.append([lab])
    R = {lab: i + 2 for i, lab in enumerate(labels)}
    s[f"B{R['Net sales']}"] = f"={ref['base_sales']}"
    for i, c in enumerate(cols):
        prev = "B" if i == 0 else cols[i - 1]
        s[f"{c}{R['Growth']}"] = rows[i]["growth"]
        s[f"{c}{R['Growth']}"].fill = INPUT_FILL
        s[f"{c}{R['Net sales']}"] = f"={prev}{R['Net sales']}*(1+{c}{R['Growth']})"
        s[f"{c}{R['Savings kept']}"] = f"={d['savings']['cumulative_musd'][i]}*{ref['flow_through']}"
        s[f"{c}{R['EBIT']}"] = f"={c}{R['Net sales']}*{ref['base_margin']}+{c}{R['Savings kept']}"
        s[f"{c}{R['Tax']}"] = f"={c}{R['EBIT']}*{ref['tax_rate']}"
        s[f"{c}{R['NOPAT']}"] = f"={c}{R['EBIT']}-{c}{R['Tax']}"
        s[f"{c}{R['D&A']}"] = f"={c}{R['Net sales']}*{ref['da_pct']}"
        s[f"{c}{R['Capex']}"] = f"={c}{R['Net sales']}*{ref['capex_pct']}"
        s[f"{c}{R['Increase in NWC']}"] = f"=({c}{R['Net sales']}-{prev}{R['Net sales']})*{ref['nwc_pct']}"
        s[f"{c}{R['Unlevered FCF']}"] = (f"={c}{R['NOPAT']}+{c}{R['D&A']}-{c}{R['Capex']}-{c}{R['Increase in NWC']}")
        factor = f"(1-{ref['stub']})" if i == 0 else "1"
        s[f"{c}{R['Cash flow counted']}"] = f"={c}{R['Unlevered FCF']}*{factor}"
        if d["mid_year_convention"]:
            start = "0" if i == 0 else f"({i}-{ref['stub']})"
            s[f"{c}{R['Discount period']}"] = f"=({start}+({i + 1}-{ref['stub']}))/2"
        else:
            s[f"{c}{R['Discount period']}"] = f"={i + 1}-{ref['stub']}"
        s[f"{c}{R['Discount factor']}"] = f"=1/(1+WACC)^{c}{R['Discount period']}"
        s[f"{c}{R['PV of FCF']}"] = f"={c}{R['Cash flow counted']}*{c}{R['Discount factor']}"
    chk = get_column_letter(3 + n + 1)
    last = rows[-1]
    for lab, key in [("Net sales", "sales"), ("EBIT", "ebit"), ("Unlevered FCF", "ufcf"), ("PV of FCF", "pv")]:
        s[f"{chk}{R[lab]}"] = last[key]

    lc = cols[-1]
    r0 = len(labels) + 3
    w = base["wacc"]
    eq = base["equity"]
    summary = [
        ("Cost of equity = Rf + beta x ERP", f"={ref['rf']}+{ref['beta']}*{ref['erp']}", w["cost_of_equity"]),
        ("After-tax cost of debt", f"={ref['kd']}*(1-{ref['tax_rate']})", w["after_tax_cost_of_debt"]),
        ("WACC", f"=(1-{ref['wd']})*B{r0}+{ref['wd']}*B{r0 + 1}", w["wacc_used"]),
        ("Sum of PV of FCF", f"=SUM(C{R['PV of FCF']}:{lc}{R['PV of FCF']})", base["dcf"]["pv_forecast"]),
        ("Terminal value (Gordon growth)", f"={lc}{R['Unlevered FCF']}*(1+{ref['g']})/(WACC-{ref['g']})", base["dcf"]["terminal_value"]),
        ("PV of terminal value", f"=B{r0 + 4}/(1+WACC)^({n}-{ref['stub']})", base["dcf"]["pv_terminal_value"]),
        ("Enterprise value", f"=B{r0 + 3}+B{r0 + 5}", base["dcf"]["enterprise_value"]),
        ("Equity value", (f"=B{r0 + 6}-{ref['net_debt']}-{ref['leases']}-{ref['minorities']}-{ref['pension']}"
                          f"+{ref['associates']}+{ref['disposals']}"), eq["equity_value"]),
        ("Value per share (USD)", f"=B{r0 + 7}/{ref['shares']}", eq["per_share_usd"]),
        ("Value per share (pence)", f"=B{r0 + 8}/{ref['fx']}*100", eq["per_share_gbp_pence"]),
        ("Upside vs share price", f"=B{r0 + 9}/{ref['price']}-1", base["rating"]["upside"]),
    ]
    s[f"A{r0 - 1}"] = "Valuation"
    s[f"A{r0 - 1}"].font = BOLD
    s[f"C{r0 - 1}"] = "Python check"
    s[f"C{r0 - 1}"].font = BOLD
    for i, (lab, formula, py) in enumerate(summary):
        s[f"A{r0 + i}"] = lab
        s[f"B{r0 + i}"] = formula
        s[f"C{r0 + i}"] = py
    from openpyxl.workbook.defined_name import DefinedName
    wb.defined_names["WACC"] = DefinedName("WACC", attr_text=f"DCF!$B${r0 + 2}")
    s.column_dimensions["A"].width = 36
    for row in s.iter_rows(min_row=2):
        for c in row[1:]:
            if isinstance(c.value, (int, float)) or (isinstance(c.value, str) and c.value.startswith("=")):
                c.number_format = "#,##0.0000" if c.row in (R["Growth"], R["Discount factor"], R["Discount period"]) else "#,##0.0"
    for i in (0, 1, 2, 10):
        s[f"B{r0 + i}"].number_format = s[f"C{r0 + i}"].number_format = "0.00%"
    wb.save(path)
