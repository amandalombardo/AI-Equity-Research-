"""Convert the Editor's memo.md into a polished A4 PDF.

Supports: a `# Title` banner, a `**Rating: X | ... | ...**` line (shown as a coloured rating strip),
`##` headings, paragraphs, bullets, simple tables, **bold**, and a valuation range chart written as

    ```football
    marker: Share price | 1673
    marker: DCF fair value | 1545
    DCF, WACC +/-0.5 pt | 1400 | 1714
    Bear scenario | 1108 | 1108
    ```

(bars are "label | low | high" in the price currency, pence or USD; markers are vertical lines). The chart draws only numbers written
in memo.md, so memo_check still traces every one of them. `## Sources` starts a new page (the appendix is
not counted in the two pages).

Usage: python -m desk.memo_pdf runs/DGE/<date>/editor/memo.md
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from reportlab.graphics.shapes import Drawing, Line, Rect, String
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (ListFlowable, ListItem, PageBreak, Paragraph, SimpleDocTemplate,
                                Spacer, Table, TableStyle)

NAVY = colors.HexColor("#1F3864")
GREY = colors.HexColor("#5A5A5A")
LIGHT = colors.HexColor("#F2F4F8")
RATING_COLOURS = {"BUY": colors.HexColor("#2E7D32"), "HOLD": colors.HexColor("#B7791F"), "SELL": colors.HexColor("#C62828")}
PAGE_W = A4[0] - 36 * mm


def inline(text: str) -> str:
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    return re.sub(r"(?<![\w*])_(.+?)_(?!\w)", r"<i>\1</i>", text)


def styles() -> dict:
    s = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=s["BodyText"], fontName="Helvetica", fontSize=8.8, leading=11.4, spaceAfter=2)
    return {
        "body": body,
        "small": ParagraphStyle("small", parent=body, fontSize=7.6, leading=9.6),
        "cell": ParagraphStyle("cell", parent=body, fontSize=8, leading=9.8, spaceAfter=0),
        "head_cell": ParagraphStyle("head_cell", parent=body, fontSize=8, leading=9.8, spaceAfter=0,
                                    textColor=colors.white, fontName="Helvetica-Bold"),
        "h2": ParagraphStyle("h2", parent=body, fontName="Helvetica-Bold", fontSize=10.5, leading=13,
                             textColor=NAVY, spaceBefore=6, spaceAfter=3),
        "h3": ParagraphStyle("h3", parent=body, fontName="Helvetica-Bold", fontSize=9.2, textColor=NAVY, spaceBefore=4),
        "title": ParagraphStyle("title", parent=body, fontName="Helvetica-Bold", fontSize=17, leading=20,
                                textColor=colors.white, alignment=TA_LEFT),
        "strip": ParagraphStyle("strip", parent=body, fontSize=8.6, leading=10.5, spaceAfter=0),
        "strip_big": ParagraphStyle("strip_big", parent=body, fontName="Helvetica-Bold", fontSize=15, leading=18,
                                    textColor=colors.white, alignment=1, spaceAfter=0),
    }


def banner(title: str, st: dict) -> Table:
    t = Table([[Paragraph(inline(title), st["title"])]], colWidths=[PAGE_W])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), NAVY), ("TOPPADDING", (0, 0), (-1, -1), 7),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 8), ("LEFTPADDING", (0, 0), (-1, -1), 8)]))
    return t


def rating_strip(line: str, st: dict) -> Table:
    """'**Rating: HOLD | Fair value 1,545p | ...**' -> coloured rating cell followed by the other items."""
    parts = [p.strip() for p in line.strip("* ").split("|")]
    rating = parts[0].split(":", 1)[-1].strip()
    colour = RATING_COLOURS.get(rating.upper(), NAVY)
    cells = [Paragraph(inline(rating), st["strip_big"])] + [Paragraph(inline(p), st["strip"]) for p in parts[1:]]
    first = 28 * mm
    widths = [first] + [(PAGE_W - first) / max(1, len(parts) - 1)] * (len(parts) - 1)
    t = Table([cells], colWidths=widths)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (0, 0), colour), ("BACKGROUND", (1, 0), (-1, 0), LIGHT),
                           ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LINEBELOW", (0, 0), (-1, -1), 1.2, colour),
                           ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    return t


def data_table(rows: list[list[str]], st: dict) -> Table:
    rows = [r for r in rows if not set("".join(r)) <= set("-: ")]
    numeric = re.compile(r"^[\s*~<>≈+\-−]*[\d,.]+\s*(%|p|x|m|bn)?\**$")
    out = []
    for i, r in enumerate(rows):
        out.append([Paragraph(inline(c), st["head_cell"] if i == 0 else st["cell"]) for c in r])
    t = Table(out, hAlign="LEFT", repeatRows=1)
    style = [("BACKGROUND", (0, 0), (-1, 0), NAVY), ("LINEBELOW", (0, 0), (-1, -1), 0.25, colors.HexColor("#C8CED9")),
             ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 2),
             ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]
    for i in range(1, len(rows)):
        if i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i), LIGHT))
    # right-align a column (header included) when every body cell in it is a number
    for j in range(1, len(rows[0]) if rows else 0):
        body = [r[j] for r in rows[1:] if j < len(r) and r[j]]
        if body and all(numeric.match(c) for c in body):
            for i in range(len(rows)):
                if j < len(out[i]):
                    out[i][j].style = ParagraphStyle(f"num{i > 0}", parent=out[i][j].style, alignment=2)
    t.setStyle(TableStyle(style))
    return t


def football(lines: list[str]) -> Drawing:
    """Horizontal range chart in the price currency: one bar per 'label | low | high', vertical lines for 'marker: label | value'."""
    bars, markers = [], []
    for ln in lines:
        if not ln.strip():
            continue
        if ln.lower().startswith("marker:"):
            label, val = [p.strip() for p in ln.split(":", 1)[1].split("|")]
            markers.append((label, float(val.replace(",", ""))))
        else:
            label, lo, hi = [p.strip() for p in ln.split("|")]
            bars.append((label, float(lo.replace(",", "")), float(hi.replace(",", ""))))
    values = [v for _, a, b in bars for v in (a, b)] + [v for _, v in markers]
    lo_axis = (min(values) // 250) * 250
    hi_axis = (max(values) // 250 + 1) * 250
    label_w, row_h, top = 46 * mm, 13, 22
    width = PAGE_W
    height = top + row_h * len(bars) + 16
    d = Drawing(width, height)
    plot_w = width - label_w - 10

    def x(v: float) -> float:
        return label_w + (v - lo_axis) / (hi_axis - lo_axis) * plot_w

    for k, (label, a, b) in enumerate(bars):
        y = height - top - row_h * (k + 1)
        d.add(String(0, y + 3, label, fontName="Helvetica", fontSize=7.6, fillColor=GREY))
        w = max(x(b) - x(a), 2.5)
        d.add(Rect(x(a), y + 1, w, row_h - 4, fillColor=colors.HexColor("#8EA9DB"), strokeColor=NAVY, strokeWidth=0.4))
        text = f"{a:,.0f}p" if a == b else f"{a:,.0f}p to {b:,.0f}p"
        d.add(String(x(a) + w + 3, y + 3, text, fontName="Helvetica", fontSize=7, fillColor=GREY))
    tick = lo_axis
    while tick <= hi_axis:
        d.add(Line(x(tick), 10, x(tick), 13, strokeColor=GREY, strokeWidth=0.4))
        d.add(String(x(tick) - 9, 1, f"{tick:,.0f}p", fontName="Helvetica", fontSize=6.5, fillColor=GREY))
        tick += 250
    d.add(Line(label_w, 13, width - 10, 13, strokeColor=GREY, strokeWidth=0.4))
    for k, (label, v) in enumerate(markers):
        colour = colors.HexColor("#C62828") if k == 0 else NAVY
        d.add(Line(x(v), 13, x(v), height - top + 6, strokeColor=colour, strokeWidth=1, strokeDashArray=[3, 2]))
        d.add(String(x(v) - 20, height - top + 9 + 8 * (k % 2), f"{label} {v:,.0f}p", fontName="Helvetica-Bold",
                     fontSize=7, fillColor=colour))
    return d


def build(md: str) -> list:
    st = styles()
    out, bullets, table, fence, fence_kind = [], [], [], None, None
    in_sources = False

    def body_style():
        return st["small"] if in_sources else st["body"]

    def flush():
        nonlocal bullets, table
        if bullets:
            out.append(ListFlowable([ListItem(Paragraph(inline(b), body_style()), leftIndent=10) for b in bullets],
                                    bulletType="bullet", start="•", leftIndent=10, bulletFontSize=7))
            bullets = []
        if table:
            out.extend([data_table(table, st), Spacer(1, 4)])
            table = []

    for line in md.splitlines():
        s = line.strip()
        if fence is not None:
            if s.startswith("```"):
                if fence_kind == "football":
                    out.extend([football(fence), Spacer(1, 2)])
                fence, fence_kind = None, None
            else:
                fence.append(s)
            continue
        if s.startswith("```"):
            flush()
            fence, fence_kind = [], s.strip("`").strip().lower()
            continue
        if s.startswith("|"):
            table.append([c.strip() for c in s.strip("|").split("|")])
            continue
        if s.startswith(("- ", "* ")):
            bullets.append(s[2:])
            continue
        flush()
        if not s:
            out.append(Spacer(1, 2))
        elif s.startswith("**Rating:"):
            out.extend([rating_strip(s, st), Spacer(1, 4)])
        elif s.startswith("#"):
            level = len(s) - len(s.lstrip("#"))
            text = s.lstrip("# ")
            if level == 1:
                out.append(banner(text, st))
            elif level == 2:
                if text.lower() == "sources":
                    in_sources = True
                    out.append(PageBreak())
                out.append(Paragraph(inline(text), st["h2"]))
            else:
                out.append(Paragraph(inline(text), st["h3"]))
        else:
            out.append(Paragraph(inline(s), body_style()))
    flush()
    return out


def _footer(title: str):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 6.8)
        canvas.setFillColor(GREY)
        canvas.drawString(18 * mm, 9 * mm, f"{title}  ·  AI Equity Research Desk  ·  "
                                           "Student portfolio project, not investment advice")
        canvas.drawRightString(A4[0] - 18 * mm, 9 * mm, f"Page {doc.page}")
        canvas.restoreState()
    return draw


def main(md_path: str) -> Path:
    src = Path(md_path)
    pdf = src.with_suffix(".pdf")
    md = src.read_text()
    title = next((ln.lstrip("# ").strip() for ln in md.splitlines() if ln.startswith("# ")), "Memo")
    doc = SimpleDocTemplate(str(pdf), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
                            topMargin=13 * mm, bottomMargin=15 * mm, title=title, author="AI Equity Research Desk")
    doc.build(build(md), onFirstPage=_footer(title), onLaterPages=_footer(title))
    print(pdf)
    return pdf


if __name__ == "__main__":
    main(sys.argv[1])
