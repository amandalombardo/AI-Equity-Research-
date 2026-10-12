from desk import memo_check, memo_pdf


def test_memo_check_flags_untraceable_numbers(tmp_path):
    (tmp_path / "valuation").mkdir()
    (tmp_path / "editor").mkdir()
    (tmp_path / "valuation" / "valuation.json").write_text('{"value_pence": 2185.21, "wacc": 0.0712}')
    (tmp_path / "editor" / "memo.md").write_text("Fair value 2,185.2p, WACC 7.12%, invented 999.9\n## Sources\np. 142")
    assert memo_check.check(str(tmp_path)) == ["999.9"]


def test_memo_pdf_builds(tmp_path):
    md = tmp_path / "memo.md"
    md.write_text("# Diageo\n**Rating: HOLD**\n\n- point one\n\n| a | b |\n|---|---|\n| 1 | 2 |\n")
    assert memo_pdf.main(str(md)).exists()
