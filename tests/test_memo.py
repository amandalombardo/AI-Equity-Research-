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


def test_memo_pdf_draws_rating_strip_chart_and_sources_page(tmp_path):
    # the Sources appendix starts its own page, so it is not counted in the two-page memo
    from pypdf import PdfReader
    md = tmp_path / "memo.md"
    md.write_text("# Diageo\n**Rating: SELL | Fair value 1,400p | Price 1,673p**\n\n```football\n"
                  "marker: Share price | 1673\nDCF range | 1300 | 1500\nBear | 1100 | 1100\n```\n\n"
                  "Short memo.\n\n## Sources\n- 20-F p.22\n")
    pdf = memo_pdf.main(str(md))
    pages = PdfReader(str(pdf)).pages
    assert len(pages) == 2 and "Sources" in pages[1].extract_text() and "Sources" not in pages[0].extract_text()
