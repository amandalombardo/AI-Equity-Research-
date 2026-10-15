"""PM decision 15 Oct 2026 (evidence audit, docs/audit-2026-10-15/ULVR.md findings 4 and 6): deduct both items."""
import yaml
from pathlib import Path

p = Path(__file__).with_name("inputs.yaml")
inp = yaml.safe_load(p.read_text())
SRC_20F = "Unilever FY25 Form 20-F (SEC accession 0000217410-26-000007, filed 12 Mar 2026) p.131"
# Pension: plans in deficit are a debt-like claim; a surplus in one plan cannot normally pay an unfunded plan's deficit.
# After-tax deficit = gross deficit x (1 - tax rate), because pension contributions are tax-deductible
gross, tax = 944.0, 0.26
inp["pension_deficit"] = {"value": round(gross * (1 - tax), 1), "source": f"PM decision 15 Oct 2026 (evidence audit): plans in deficit 944 (funded in deficit 100 + unfunded 844, {SRC_20F}) x (1 - 26% tax, briefs/ULVR.yaml tax_rate) = {gross*(1-tax):.1f}. The net surplus (3,518) is not offset against them; surpluses are not added (brief rule)"}
# McCormick dividends before closing: the new McCormick shares are issued at closing (mid-2027), so they miss the
# quarterly dividends in between, which today's McCormick share price includes. Leakage = shares x dividend x quarters / FX
shares, dps, quarters, usd_per_eur = 499_691_175, 0.48, 3, 1.1193
leak = shares * dps * quarters / usd_per_eur / 1e6
for k in ("disposal_proceeds", "priced_at_valuation_date_meur"):
    old = inp[k]["value"]
    inp[k]["value"] = round(old - leak, 1)
    inp[k]["source"] += (f" LESS McCormick dividends the new shares miss before closing (PM decision 15 Oct 2026): 499,691,175 shares x USD 0.48 a quarter"
                         f" (McCormick 10-Q to 31 Aug 2026, accession 0000063754-26-000329) x 3 quarters (ex-dates Jan, Apr, Jul 2027; closing expected mid-2027,"
                         f" Form 425 0000217410-26-000027) / 1.1193 USD per EUR (FRED DEXUSEU 2026-10-09) = {leak:.1f}; {old} - {leak:.1f}. FLAG: if closing comes before the July ex-date, 2 quarters (+c.8p)")
p.write_text(yaml.safe_dump(inp, sort_keys=False, allow_unicode=True, width=200))
print(inp["pension_deficit"]["value"], round(leak, 1), inp["disposal_proceeds"]["value"], inp["priced_at_valuation_date_meur"]["value"])

# Joint ventures inside `associates` are valued as a growing perpetuity (Gordon growth) on FY25 JV dividends at the run's
# cost of equity (PM decision 10). The ERP change lowers the cost of equity, so the JV value is recomputed with the same rule.
# Cost of equity (CAPM) = risk-free + beta x ERP; JV value = dividend x (1 + g) / (Ke - g)
rf, beta, erp, g, jv_div = 0.0345, 0.8844, 0.042, 0.016, 229.0
ke_old = rf + beta * 0.050
ke_new = rf + beta * erp
jv_old = jv_div * (1 + g) / (ke_old - g)
jv_new = jv_div * (1 + g) / (ke_new - g)
a = inp["associates"]
if "JV value recomputed" not in a["source"]:
    a["value"] = round(a["value"] - jv_old + jv_new, 1)
    a["source"] += (f" JV value recomputed 15 Oct 2026 at the new cost of equity {ke_new:.4%} (ERP 4.2%): 229 x 1.016 / ({ke_new:.4%} - 1.6%)"
                    f" = {jv_new:.1f} (was {jv_old:.1f} at {ke_old:.4%})")
    p.write_text(yaml.safe_dump(inp, sort_keys=False, allow_unicode=True, width=200))
print(a["value"], round(jv_old, 1), round(jv_new, 1))
