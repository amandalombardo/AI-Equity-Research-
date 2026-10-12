import json
import shutil
import subprocess
from pathlib import Path

import pytest
from openpyxl import load_workbook

from desk import valuation_run

ROOT = Path(__file__).resolve().parents[1]
BRIEF = ROOT / "briefs" / "DGE.yaml"
FIXTURE = ROOT / "tests" / "fixtures" / "sample_inputs.yaml"


def test_run_refuses_missing_or_unsourced_inputs(tmp_path):
    bad = tmp_path / "inputs.yaml"
    bad.write_text("tax_rate: {value: 0.23}\n")
    with pytest.raises(SystemExit):
        valuation_run.main(str(BRIEF), str(bad), str(tmp_path / "out"))


def test_full_run_writes_outputs(tmp_path):
    valuation_run.main(str(BRIEF), str(FIXTURE), str(tmp_path))
    result = json.loads((tmp_path / "valuation.json").read_text())
    assert result["base"]["rating"]["rating"] in {"BUY", "HOLD", "SELL"}
    # bear case (no growth, lower flow-through, higher WACC) must be worth less than the base case
    assert result["bear"]["equity"]["per_share_gbp_pence"] < result["base"]["equity"]["per_share_gbp_pence"]
    assert (tmp_path / "dcf.xlsx").exists()


@pytest.mark.skipif(not shutil.which("soffice"), reason="LibreOffice not installed")
def test_excel_formulas_match_python(tmp_path):
    valuation_run.main(str(BRIEF), str(FIXTURE), str(tmp_path))
    subprocess.run(["soffice", "--headless", "--convert-to", "xlsx", "--outdir", str(tmp_path / "recalc"),
                    str(tmp_path / "dcf.xlsx")], check=True, capture_output=True, timeout=120)
    ws = load_workbook(tmp_path / "recalc" / "dcf.xlsx", data_only=True)["DCF"]
    rows = list(ws.iter_rows(values_only=True))
    start = next(i for i, r in enumerate(rows) if r[0] == "Valuation")
    checked = 0
    for r in rows[start + 1:]:  # valuation section: column B = Excel formula, column C = Python value
        if r[0]:
            assert r[1] == pytest.approx(r[2], rel=1e-9), r[0]
            checked += 1
    assert checked == 11
    # forecast block: final-year Excel formulas vs the Python check column
    for r in rows[1:start]:
        if r[0] and isinstance(r[-1], (int, float)):
            assert r[-3] == pytest.approx(r[-1], rel=1e-9), r[0]
            checked += 1
    assert checked == 15


def test_credit_spread_rule_sets_cost_of_debt():
    brief = {"dcf": {"wacc": {"credit_spread": 0.01}}}
    v = {"risk_free": 0.05, "pre_tax_cost_of_debt": 0.035}
    sources = {"pre_tax_cost_of_debt": "historic"}
    valuation_run.apply_brief_rules(brief, v, sources)
    assert v["pre_tax_cost_of_debt"] == pytest.approx(0.06)
    assert v["pre_tax_cost_of_debt_historic"] == pytest.approx(0.035)


def test_no_credit_spread_keeps_agent_input():
    v = {"risk_free": 0.05, "pre_tax_cost_of_debt": 0.035}
    valuation_run.apply_brief_rules({"dcf": {"wacc": {}}}, v, {})
    assert v["pre_tax_cost_of_debt"] == pytest.approx(0.035)
