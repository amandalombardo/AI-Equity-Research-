"""Phase 6 publication: the cover and README must show the same numbers as the final memos and valuation.json."""
from pathlib import Path

import pytest

from publish import build_pack, diagram

ROOT = Path(__file__).resolve().parent.parent


@pytest.mark.parametrize("ticker,folder", build_pack.RUNS)
def test_memo_header_agrees_with_valuation_json(ticker, folder):
    run = ROOT / folder
    header = build_pack.memo_header(run)
    build_pack.check_against_valuation(header, run)  # raises if the memo and the engine disagree
    assert header["rating"] in ("BUY", "HOLD", "SELL")


def test_check_catches_a_memo_that_disagrees(tmp_path):
    (tmp_path / "valuation").mkdir()
    (tmp_path / "valuation" / "valuation.json").write_text(
        '{"base": {"rating": {"rating": "HOLD", "fair_value": 1780.209, "share_price": 1673.0, "upside": 0.0641}}}')
    header = {"rating": "HOLD", "fair_value": "1,780.3p", "share_price": "1,673p (12 Oct 2026)", "upside": "+6.4%"}
    with pytest.raises(ValueError):
        build_pack.check_against_valuation(header, tmp_path)
    header["fair_value"] = "1,780.2p"
    build_pack.check_against_valuation(header, tmp_path)


def test_readme_table_matches_memos():
    readme = (ROOT / "README.md").read_text()
    for _, folder in build_pack.RUNS:
        h = build_pack.memo_header(ROOT / folder)
        row = next(ln for ln in readme.splitlines() if ln.startswith(f"| {h['company']} |"))
        price = h["share_price"].replace(" close", "")
        for value in (h["rating"], h["fair_value"], price, h["upside"]):
            assert value in row, (value, row)


def test_diagram_saves_svg(tmp_path):
    paths = diagram.save(tmp_path)
    assert paths["svg"].read_text().count("agent") >= 6
