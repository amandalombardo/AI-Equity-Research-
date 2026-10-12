"""Convert the Editor's memo.md into a clean A4 PDF (headings, paragraphs, bullets, simple tables, **bold**).

Usage: python -m desk.memo_pdf runs/DGE/<date>/editor/memo.md
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import ListFlowable, ListItem, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def inline(text: str) -> str:
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)


def build(md: str) -> list:
    styles = getSampleStyleSheet()
    body = styles["BodyText"]
    body.fontSize, body.leading = 9.5, 12.5
    out, bullets, table = [], [], []

    def flush():
        nonlocal bullets, table
        if bullets:
            out.append(ListFlowable([ListItem(Paragraph(inline(b), body)) for b in bullets], bulletType="bullet"))
            bullets = []
        if table:
            rows = [[Paragraph(inline(c), body) for c in r] for r in table if not set("".join(r)) <= set("-: ")]
            t = Table(rows, hAlign="LEFT")
            t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                                   ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EEEEEE"))]))
            out.extend([t, Spacer(1, 4)])
            table = []

    for line in md.splitlines():
        s = line.strip()
        if s.startswith("|"):
            table.append([c.strip() for c in s.strip("|").split("|")])
            continue
        if s.startswith(("- ", "* ")):
            bullets.append(s[2:])
            continue
        flush()
        if not s:
            out.append(Spacer(1, 4))
        elif s.startswith("#"):
            level = len(s) - len(s.lstrip("#"))
            out.append(Paragraph(inline(s.lstrip("# ")), styles["Title" if level == 1 else "Heading2" if level == 2 else "Heading3"]))
        else:
            out.append(Paragraph(inline(s), body))
    flush()
    return out


def main(md_path: str) -> Path:
    src = Path(md_path)
    pdf = src.with_suffix(".pdf")
    doc = SimpleDocTemplate(str(pdf), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
                            topMargin=15 * mm, bottomMargin=15 * mm)
    doc.build(build(src.read_text()))
    print(pdf)
    return pdf


if __name__ == "__main__":
    main(sys.argv[1])
