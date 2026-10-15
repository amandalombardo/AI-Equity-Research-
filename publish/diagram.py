"""Diagram of how the six agents work together, drawn with reportlab so it can be saved as SVG (for the README),
PNG and PDF (for the research pack). It contains no financial numbers.

Usage: python -m publish.diagram   (writes publish/agent-diagram.svg and .png)
"""
from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

from reportlab.graphics import renderPDF, renderSVG
from reportlab.graphics.shapes import Drawing, Line, PolyLine, Polygon, Rect, String
from reportlab.lib import colors

NAVY = colors.HexColor("#1F3864")
GREY = colors.HexColor("#4A4A4A")
AGENT_FILL = colors.HexColor("#E8EEF8")
ENGINE_FILL, ENGINE_LINE = colors.HexColor("#FFF4E0"), colors.HexColor("#B7791F")
CHECK_FILL, CHECK_LINE = colors.HexColor("#E8F5E9"), colors.HexColor("#2E7D32")
STOP_FILL, STOP_LINE = colors.HexColor("#FDECEA"), colors.HexColor("#C62828")

W, H = 493, 572

AGENTS = [  # (name, what it does, what it writes), in the order /run-desk runs them
    ("Data", "Downloads filings, prices, rates and FX", "inputs.yaml, financials.csv: a source on every number"),
    ("Risk", "Industry beta, volatility, drawdown, leverage", "risk.json; adds beta to inputs.yaml"),
    ("Fundamentals", "Growth, margins, ROIC, cash conversion", "ratios.csv, commentary.md"),
    ("Valuation", "DCF and comparables on the PM's assumptions", "valuation.json, dcf.xlsx (live formulas)"),
    ("Bear case", "Argues against; prices each challenge per share", "challenges.md"),
    ("Editor", "Writes the memo using only the agents' numbers", "memo.pdf, traced by memo_check"),
]
AGENT_X, AGENT_W, AGENT_H, AGENT_TOP, AGENT_GAP = 150, 193, 50, 96, 20


def _y(top: float) -> float:
    """reportlab measures y from the bottom; the layout below is written from the top."""
    return H - top


def _box(d: Drawing, x, top, w, h, fill, stroke, title, lines, title_colour=NAVY, text_colour=GREY, dash=None):
    d.add(Rect(x, _y(top + h), w, h, rx=4, ry=4, fillColor=fill, strokeColor=stroke, strokeWidth=0.9,
               strokeDashArray=dash))
    d.add(String(x + 7, _y(top + 14), title, fontName="Helvetica-Bold", fontSize=8.6, fillColor=title_colour))
    for k, ln in enumerate(lines):
        d.add(String(x + 7, _y(top + 26 + 10 * k), ln, fontName="Helvetica", fontSize=7, fillColor=text_colour))


def _arrow(d: Drawing, points: list[tuple[float, float]], colour=NAVY, dash=None):
    """Polyline through (x, top) points with an arrowhead at the last point."""
    pts = [(x, _y(t)) for x, t in points]
    d.add(PolyLine([c for p in pts for c in p], strokeColor=colour, strokeWidth=1, strokeDashArray=dash))
    (x0, y0), (x1, y1) = pts[-2], pts[-1]
    dx, dy = x1 - x0, y1 - y0
    n = (dx * dx + dy * dy) ** 0.5 or 1
    ux, uy = dx / n, dy / n
    s = 5
    d.add(Polygon([x1, y1, x1 - s * ux + s * 0.55 * uy, y1 - s * uy - s * 0.55 * ux,
                   x1 - s * ux - s * 0.55 * uy, y1 - s * uy + s * 0.55 * ux],
                  fillColor=colour, strokeColor=colour, strokeWidth=0.5))


def agent_top(i: int) -> float:
    return AGENT_TOP + i * (AGENT_H + AGENT_GAP)


def drawing() -> Drawing:
    d = Drawing(W, H)
    d.add(Rect(0, 0, W, H, fillColor=colors.white, strokeColor=None))  # white background, readable in dark mode

    # top row: public sources and the PM
    _box(d, 4, 12, 122, 58, colors.white, GREY, "Public sources",
         ["SEC filings (20-F, 10-K, 6-K)", "Yahoo Finance prices", "FRED rates and FX"])
    d.add(Rect(AGENT_X, _y(12 + 58), AGENT_W, 58, rx=4, ry=4, fillColor=NAVY, strokeColor=NAVY))
    d.add(String(AGENT_X + 7, _y(26), "Portfolio manager (Amanda)", fontName="Helvetica-Bold", fontSize=8.6,
                 fillColor=colors.white))
    for k, ln in enumerate(["Sets every assumption in briefs/<TICKER>.yaml,", "each with its source. Rules on bear",
                            "challenges. Approves every change."]):
        d.add(String(AGENT_X + 7, _y(38 + 10 * k), ln, fontName="Helvetica", fontSize=7, fillColor=colors.white))

    # the six agents, in run order
    for i, (name, job, output) in enumerate(AGENTS):
        _box(d, AGENT_X, agent_top(i), AGENT_W, AGENT_H, AGENT_FILL, NAVY, f"{i + 1}  {name} agent", [job, output])
        if i:
            _arrow(d, [(AGENT_X + AGENT_W / 2, agent_top(i) - AGENT_GAP), (AGENT_X + AGENT_W / 2, agent_top(i))])
    _arrow(d, [(AGENT_X + AGENT_W / 2, 70), (AGENT_X + AGENT_W / 2, agent_top(0))])
    _arrow(d, [(65, 70), (65, agent_top(0) + AGENT_H / 2), (AGENT_X, agent_top(0) + AGENT_H / 2)])

    # left: the Python engine every calculating agent calls
    eng_top, eng_h = agent_top(1) - 6, agent_top(4) + AGENT_H - agent_top(1) + 12
    _box(d, 4, eng_top, 122, eng_h, ENGINE_FILL, ENGINE_LINE, "desk/ Python engine",
         ["DCF, WACC, terminal value", "EV-to-equity bridge", "beta, volatility, ratios", "", "Agents call these",
          "functions and never do", "arithmetic in their heads.", "", "Each formula is tested", "against a hand",
          "calculation (pytest)."], title_colour=ENGINE_LINE)
    for i in (1, 2, 3, 4):
        mid = agent_top(i) + AGENT_H / 2
        _arrow(d, [(AGENT_X, mid), (126, mid)], colour=ENGINE_LINE)

    # right: the STOP rule and the PM's review loop
    _box(d, 372, agent_top(0), 117, 70, STOP_FILL, STOP_LINE, "STOP rule",
         ["A number with no source is", "written as MISSING and the", "run stops. The PM decides", "what happens next."],
         title_colour=STOP_LINE)
    loop_x = 357
    bear_mid = agent_top(4) + AGENT_H / 2
    _arrow(d, [(AGENT_X + AGENT_W, bear_mid), (loop_x, bear_mid), (loop_x, 41), (AGENT_X + AGENT_W, 41)], dash=[3, 2])
    _box(d, 372, agent_top(3) + 10, 117, 82, colors.white, NAVY, "Review loop",
         ["The PM accepts or rejects", "each bear challenge. A", "change goes into the brief,", "then the desk re-runs.",
          "Every company re-runs when", "the engine changes."], dash=[3, 2])

    # bottom: outputs and the independent checks
    out_top = agent_top(5) + AGENT_H + AGENT_GAP
    _box(d, AGENT_X, out_top, AGENT_W, 46, colors.white, NAVY, "Published output",
         ["Memo: two pages plus a sources page", "DCF in Excel with live formulas"])
    _arrow(d, [(AGENT_X + AGENT_W / 2, out_top - AGENT_GAP), (AGENT_X + AGENT_W / 2, out_top)])
    _box(d, 372, out_top - 40, 117, 86, CHECK_FILL, CHECK_LINE, "Independent checks",
         ["Automated tests", "Codex blind maths audit", "PM's own Excel model", "Evidence audit of every",
          "input against its source"], title_colour=CHECK_LINE)
    _arrow(d, [(372, out_top + 23), (AGENT_X + AGENT_W, out_top + 23)], colour=CHECK_LINE)
    return d


def save(out_dir: Path) -> dict[str, Path]:
    """Write agent-diagram.svg and agent-diagram.png (PNG needs poppler's pdftoppm; skipped if absent)."""
    out_dir.mkdir(parents=True, exist_ok=True)
    d = drawing()
    paths = {"svg": out_dir / "agent-diagram.svg"}
    renderSVG.drawToFile(d, str(paths["svg"]))
    if shutil.which("pdftoppm"):
        with tempfile.TemporaryDirectory() as tmp:
            pdf = Path(tmp) / "diagram.pdf"
            renderPDF.drawToFile(d, str(pdf))
            subprocess.run(["pdftoppm", "-png", "-r", "200", "-singlefile", str(pdf), str(out_dir / "agent-diagram")],
                           check=True)
        paths["png"] = out_dir / "agent-diagram.png"
    return paths


if __name__ == "__main__":
    for p in save(Path(__file__).parent).values():
        print(p)
