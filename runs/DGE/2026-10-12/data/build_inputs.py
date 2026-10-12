"""Data agent script: builds financials.csv, the tie-out and inputs.yaml from the downloaded data.
Every hand-entered number below is quoted from the source named next to it."""
import json
from datetime import date
from pathlib import Path

import pandas as pd
import yaml

RUN = Path(__file__).resolve().parents[1]
DATA = RUN / "data"
brief = yaml.safe_load(Path("briefs/DGE.yaml").read_text())
raw = pd.read_csv(DATA / "financials_raw.csv")
mkt = json.loads((DATA / "market_inputs.json").read_text())
F26 = "Diageo Form 20-F FY26 (SEC accession 0001628280-26-057529, filed 2026-08-18)"


def v(item, fy):
    return float(raw[(raw["item"] == item) & (raw["fiscal_year"] == fy)]["value_musd"].iloc[0])


# ---- financials.csv: XBRL line items plus figures quoted from the 20-F text
fin = raw.rename(columns={"source": "source"})[["item", "fiscal_year", "value_musd", "source"]].copy()
fin["source"] = fin["source"] + " | XBRL tag " + raw["tag"]
fin["value_musd"] = fin["value_musd"].round(1)
text_items = [
    ("free_cash_flow", 2026, 3211, F26 + ", Financial review 'Movements in net borrowings' table"),
    ("free_cash_flow", 2025, 2748, F26 + ", Financial review 'Movements in net borrowings' table"),
    ("tax_rate_bei", 2026, 0.243, F26 + " p.22: 'tax rate before exceptional items ... 24.3%'"),
    ("tax_rate_bei", 2025, 0.249, F26 + " p.22: 'tax rate before exceptional items ... 24.9%' (FY25)"),
    ("tax_rate_reported", 2026, 0.258, F26 + " p.22: 'reported tax rate ... 25.8%'"),
    ("eps_bei_cents", 2026, 165.3, F26 + " p.210: 'Basic earnings per share before exceptional items 165.3'"),
    ("eps_bei_cents", 2025, 164.2, F26 + " p.210"),
    ("organic_net_sales_growth", 2026, -0.020, F26 + " p.13: 'Organic net sales declined 2.0%'"),
    ("organic_operating_profit_growth", 2026, 0.020, F26 + " p.13: 'Organic operating profit increased by 2.0%'"),
    ("roic", 2026, 0.134, F26 + " p.211: 'Return on average invested capital 13.4%'"),
    ("roic", 2025, 0.137, F26 + " p.211"),
    ("average_net_borrowings", 2026, 21336, F26 + " p.211"),
    ("average_net_borrowings", 2025, 21182, F26 + " p.211"),
    ("adjusted_net_borrowings_to_ebitda", 2026, 3.1, F26 + " p.186"),
    ("adjusted_net_borrowings_to_ebitda", 2025, 3.4, F26 + " p.186"),
    ("associates_moet_hennessy_carrying", 2026, 5107, F26 + " p.~165 note 'Investments in associates' (a): Moet Hennessy at 30 June 2026"),
    ("associates_other_carrying", 2026, 177, F26 + " note 'Investments in associates' (a)"),
    ("nci_usl_book", 2026, 755, F26 + " p.189 note (e) Non-controlling interests: USL"),
    ("nci_other_book", 2026, 1328, F26 + " p.189 note (e) Non-controlling interests: Other"),
]
fin = pd.concat([fin, pd.DataFrame(text_items, columns=fin.columns)], ignore_index=True)
regions = [  # FY26 20-F regional performance tables (pp.27-31), reported net sales USD m and organic growth
    ("North America", 7249, -0.084), ("Europe", 5097, 0.034), ("Asia Pacific", 3333, -0.063),
    ("Latin America and Caribbean", 2160, 0.077), ("Africa", 1642, 0.133), ("Corporate", 162, None)]
for name, ns, org in regions:
    fin.loc[len(fin)] = [f"net_sales_{name}", 2026, ns, F26 + f", regional review '{name}' net sales table"]
    if org is not None:
        fin.loc[len(fin)] = [f"organic_growth_{name}", 2026, org, F26 + f", regional review '{name}' commentary"]
fin.sort_values(["item", "fiscal_year"]).to_csv(DATA / "financials.csv", index=False)

# ---- tie-out vs the brief (published FY26 figures)
pub = brief["checks"]["published_fy26"]
tol = brief["checks"]["data_tie_out_tolerance"]
ours = {"net_sales_musd": v("net_sales", 2026), "operating_profit_bei_musd": v("operating_profit_bei", 2026),
        "net_debt_musd": v("net_borrowings", 2026),
        "free_cash_flow_musd": v("operating_cash_flow", 2026) - v("capex", 2026) + v("proceeds_from_ppe_disposals", 2026),
        "eps_bei_cents": 165.3}
tie = [{"item": k, "brief": pub[k], "data_agent": round(ours[k], 1), "diff_pct": round(ours[k] / pub[k] - 1, 5),
        "flag": abs(ours[k] / pub[k] - 1) > tol} for k in pub]
pd.DataFrame(tie).to_csv(DATA / "tie_out.csv", index=False)

# ---- EABL carve-out (non-filing source, see notes.md)
kes_per_usd = 128.32  # Yahoo Finance KES=X, average daily close 1 Jul 2025 - 30 Jun 2026 (260 days)
eabl_sales = 145.96e3 / kes_per_usd  # EABL FY26 (to 30 Jun 2026) net revenue KES 145.96bn, EABL results 6 Aug 2026 as reported by press
eabl_ebit = 32.1e3 / kes_per_usd     # EABL FY26 EBIT KES 32.1bn, same source
base_sales = v("net_sales", 2026) - eabl_sales
base_margin = (v("operating_profit_bei", 2026) - eabl_ebit) / base_sales

years = [2022, 2023, 2024, 2025, 2026]
ns = sum(v("net_sales", y) for y in years)
da_pct = sum(v("depreciation_amortisation", y) for y in years) / ns
capex_pct = sum(v("capex", y) for y in years) / ns
nwc = v("inventories", 2026) + v("trade_and_other_receivables", 2026) - v("trade_and_other_payables", 2026)
nwc_pct = nwc / v("net_sales", 2026)
kd = 812 / 21336  # FY26 net interest charge / average net borrowings (both FY26 20-F)
shares = v("shares_issued_m", 2026) - v("treasury_shares_m", 2026) - v("employee_trust_shares_m", 2026)
price, fx = mkt["share_price_gbp_pence"]["value"], mkt["fx_usd_per_gbp"]["value"]
mcap_musd = shares * price / 100 * fx
net_debt = v("net_borrowings", 2026)
run_date = date(2026, 10, 12)
stub = (run_date - date(2026, 7, 1)).days / 365

inputs = {
    "base_sales": {"value": round(base_sales, 1), "source": f"{F26} net sales 19,643 less EABL FY26 net revenue KES 145.96bn / 128.32 KES per USD = {eabl_sales:.1f} (EABL: non-filing source, press reports of EABL FY26 results 6 Aug 2026; FX: Yahoo KES=X FY26 average)"},
    "base_margin": {"value": round(base_margin, 5), "source": f"({F26} operating profit before exceptionals 5,683 less EABL EBIT KES 32.1bn / 128.32 = {eabl_ebit:.1f}) / ex-EABL net sales"},
    "tax_rate": {"value": 0.243, "source": F26 + " p.22, tax rate before exceptional items FY26"},
    "da_pct_sales": {"value": round(da_pct, 5), "source": "FY22-FY26 depreciation & amortisation (excl. impairment) / net sales, summed over 5 years; 20-F XBRL deo:DepreciationAndIntangibleAssetAmortisationExpense and deo:NetSales"},
    "capex_pct_sales": {"value": round(capex_pct, 5), "source": "FY22-FY26 purchase of PP&E and software / net sales, summed over 5 years; 20-F cash flow statements"},
    "nwc_pct_sales": {"value": round(nwc_pct, 5), "source": "FY26 (inventories incl. maturing 10,529 + trade & other receivables 3,277 - trade & other payables 6,425) / net sales 19,643; " + F26 + " balance sheet"},
    "risk_free": {"value": round(mkt["risk_free"]["value"], 4), "source": f"{mkt['risk_free']['source']}, {mkt['risk_free']['date']}"},
    "pre_tax_cost_of_debt": {"value": round(kd, 5), "source": F26 + " p.211: FY26 net interest charge 812 / average net borrowings 21,336 (historic cost; see notes.md FLAG)"},
    "debt_weight": {"value": round(net_debt / (net_debt + mcap_musd), 5), "source": f"net debt 20,482 / (net debt + market cap {mcap_musd:,.0f} = {shares:,.0f}m shares x {price:.0f}p x {fx} USD/GBP)"},
    "net_debt": {"value": net_debt, "source": F26 + " note 17 p.187: net borrowings 20,482 (INCLUDES lease liabilities 685; EABL/RCB loans of 272 sit in liabilities held for sale)"},
    "lease_liabilities": {"value": 0, "source": "0 because the 685 of lease liabilities is already inside net borrowings (20-F note 17 p.187)"},
    "minority_interests": {"value": v("non_controlling_interests", 2026), "source": F26 + " balance sheet, non-controlling interests at book value (USL 755, other 1,328: p.189)"},
    "pension_deficit": {"value": 0, "source": F26 + ": net post-employment SURPLUS 627 (XBRL LiabilityAssetOfDefinedBenefitPlans -627); brief rule: 0 if in surplus. Deficit plans alone: 387 (see FLAG)"},
    "associates": {"value": v("investments_in_associates", 2026), "source": F26 + " note 'Investments in associates': Moet Hennessy 34% at 5,107 (carrying value tested at fair value less costs of disposal, 'sensitive' = little headroom) + others 177"},
    "disposal_proceeds": {"value": round(2300 + 0.5721 * 1780, 1), "source": "EABL + Kenyan spirits sale to Asahi c.$2.3bn (20-F p.85) + Diageo's 57.21% of USL's RCB sale INR 166.6bn = c.$1.78bn (USL/press, 24 Mar 2026); both gross, before tax and costs, not in net debt at 30 June 2026"},
    "shares_outstanding_m": {"value": shares, "source": F26 + " p.188 and XBRL: 2,432m issued - 208m treasury - 2m employee trusts (ordinary shares, NOT ADRs)"},
    "fx_usd_per_gbp": {"value": fx, "source": f"{mkt['fx_usd_per_gbp']['source']}, {mkt['fx_usd_per_gbp']['date']}"},
    "share_price_gbp_pence": {"value": price, "source": f"{mkt['share_price_gbp_pence']['source']}, {mkt['share_price_gbp_pence']['date']}"},
    "stub_years": {"value": round(stub, 4), "source": f"{(run_date - date(2026, 7, 1)).days} days of FY27 (from 1 Jul 2026) elapsed at run date {run_date} / 365"},
}
(RUN / "inputs.yaml").write_text(yaml.safe_dump(inputs, sort_keys=False, width=1000))
print(json.dumps({k: x["value"] for k, x in inputs.items()}, indent=1))
print(pd.DataFrame(tie).to_string())
