"""Build the Phase 6 publication pack from the final runs.

Writes to publish/:
- agent-diagram.svg / .png: how the six agents work together
- what-the-agents-got-wrong.pdf: the mistakes write-up (from what-the-agents-got-wrong.md)
- research-pack.pdf: cover page with the four calls, the diagram, the four memos and the write-up

The cover adds no numbers of its own: each value is copied from the Editor's memo header line (memo.md), and the
build stops if that header disagrees with the Valuation agent's valuation.json (fair value, price, rating).
Merging PDFs needs poppler's pdfunite.

Usage: python -m publish.build_pack
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

from desk import memo_pdf
from publish import diagram

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "publish"
RUNS = [  # final run folder of each company, in the order they were covered
    ("DGE", "runs/DGE/2026-10-12"),
    ("KO", "runs/KO/2026-10-13"),
    ("ULVR", "runs/ULVR/2026-10-14"),
    ("RELX", "runs/RELX/2026-10-14"),
]


def _number(text: str) -> float:
    """First number in a label such as 'USD 90.12 (13 Oct 2026)' or '1,780.2p'."""
    return float(re.search(r"-?[\d,]+(?:\.\d+)?", text).group().replace(",", ""))


def memo_header(run: Path) -> dict:
    """Read the Editor's '**Rating: X | Fair value ... | Share price ... | Upside ... | Bear case ...**' line
    plus the company name (memo title) and the headline of its first thesis bullet."""
    md = (run / "editor" / "memo.md").read_text()
    lines = md.splitlines()
    title = next(ln[2:].strip() for ln in lines if ln.startswith("# "))
    rating_line = next(ln for ln in lines if ln.startswith("**Rating:"))
    parts = [p.strip() for p in rating_line.strip("* ").split("|")]
    out = {"company": title, "rating": parts[0].split(":", 1)[1].strip()}
    for key, prefix in (("fair_value", "Fair value"), ("share_price", "Share price"), ("upside", "Upside"),
                        ("bear_case", "Bear case")):
        out[key] = next(p[len(prefix):].strip() for p in parts if p.startswith(prefix))
    thesis = md.split("## Thesis", 1)[1]
    out["headline"] = re.search(r"\*\*(.+?)\*\*", thesis).group(1)
    return out


def check_against_valuation(header: dict, run: Path) -> None:
    """The memo header must agree with valuation.json: same rating, and fair value and price equal at the
    memo's rounding (the memo shows at most 2 decimals)."""
    base = json.loads((run / "valuation" / "valuation.json").read_text())["base"]["rating"]
    if header["rating"] != base["rating"]:
        raise ValueError(f"{run}: memo rating {header['rating']} but valuation.json says {base['rating']}")
    for key in ("fair_value", "share_price"):
        shown, engine = _number(header[key]), base[key]
        decimals = len(header[key].split(".")[1].rstrip("p").split()[0]) if "." in header[key].split("(")[0] else 0
        if abs(round(engine, decimals) - shown) > 1e-9:
            raise ValueError(f"{run}: memo {key} {header[key]} but valuation.json says {engine}")
    # upside = fair value / price - 1, shown to one decimal place
    if abs(round(base["upside"] * 100, 1) - _number(header["upside"])) > 1e-9:
        raise ValueError(f"{run}: memo upside {header['upside']} but valuation.json says {base['upside']}")


def cover_markdown(headers: list[dict]) -> str:
    rows = "\n".join(
        f"| {h['company']} | **{h['rating']}** | {h['fair_value']} | {h['share_price']} | {h['upside']} | "
        f"{h['bear_case']} |" for h in headers)
    lines = "\n".join(f"- **{h['company']}:** {h['headline']}" for h in headers)
    return f"""# AI Equity Research Desk: four company calls, October 2026

**Portfolio manager: Amanda.** Six AI agents (Data, Risk, Fundamentals, Valuation, Bear case and Editor) each produced a buy/hold/sell memo on a listed company. The PM set every assumption, with a source for each one, and ruled on every challenge from the Bear case agent. All calculations were done by tested Python code, never by the AI itself.

**Desk rule:** BUY at +15% or more upside to the DCF fair value, SELL at -10% or worse, HOLD in between, with no overrides. Per-share values are in pence (GBp) for London listings and US dollars (USD) for Coca-Cola.

| Company | Rating | Fair value | Share price | Upside | Bear case |
|---|---|---|---|---|---|
{rows}

## The calls in one line (from each memo's thesis)

{lines}

## What is in this pack

- **How the desk works:** a diagram of the six agents, the Python engine, the PM's review loop and the independent checks.
- **The four memos:** two pages each, plus a page of sources (SEC filings with page references, FRED series, data files).
- **What the agents got wrong:** the 33 mistakes logged during the project, how each was caught, and the rules that came out of them.

## Read with care

- This is a student portfolio project, not investment advice. Prices are the closes of 12 and 13 October 2026.
- Four inputs could only be seen second-hand and are disclosed in the memos: the 4.2% equity risk premium (Damodaran implied), the UK gilt and German Bund yields, and EABL's sales.
- Unilever is a borderline HOLD: it is 19.1p above the SELL line, and its memo shows the inputs that would flip it.

Code, agent outputs and evidence files: github.com/amandalombardo/ai-equity-research-desk
"""


def _doc(path: Path, title: str) -> SimpleDocTemplate:
    return SimpleDocTemplate(str(path), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=13 * mm,
                             bottomMargin=15 * mm, title=title, author="AI Equity Research Desk")


def front_pages(headers: list[dict], path: Path) -> Path:
    """Cover page, then the diagram page."""
    st = memo_pdf.styles()
    flow = memo_pdf.build(cover_markdown(headers))
    flow += [memo_pdf.PageBreak(), memo_pdf.banner("How the desk works", st), Spacer(1, 8)]
    d = diagram.drawing()
    scale = min(1.0, memo_pdf.PAGE_W / d.width)
    d.scale(scale, scale)
    d.width, d.height = d.width * scale, d.height * scale
    flow += [d, Spacer(1, 6), Paragraph(memo_pdf.inline(
        "The agents run in order (/run-desk TICKER). Each writes only to its own folder and ends with notes.md: what it "
        "did, its flags, anything missing and its confidence. The Editor may use only numbers that trace back to an "
        "agent's output, which memo_check verifies."), st["small"])]
    title = "Four company calls, October 2026"
    _doc(path, title).build(flow, onFirstPage=memo_pdf._footer(title), onLaterPages=memo_pdf._footer(title))
    return path


def writeup_pdf(md_path: Path, pdf_path: Path) -> Path:
    md = md_path.read_text()
    title = "What the AI agents got wrong"
    _doc(pdf_path, title).build(memo_pdf.build(md), onFirstPage=memo_pdf._footer(title),
                                onLaterPages=memo_pdf._footer(title))
    return pdf_path


def build(out: Path = OUT) -> dict[str, Path]:
    headers = []
    for _, folder in RUNS:
        run = ROOT / folder
        header = memo_header(run)
        check_against_valuation(header, run)
        headers.append(header)
    paths = diagram.save(out)
    paths["writeup"] = writeup_pdf(OUT / "what-the-agents-got-wrong.md", out / "what-the-agents-got-wrong.pdf")
    if not shutil.which("pdfunite"):
        raise RuntimeError("pdfunite (poppler-utils) is needed to merge the pack")
    with tempfile.TemporaryDirectory() as tmp:
        front = front_pages(headers, Path(tmp) / "front.pdf")
        memos = [str(ROOT / folder / "editor" / "memo.pdf") for _, folder in RUNS]
        paths["pack"] = out / "research-pack.pdf"
        subprocess.run(["pdfunite", str(front), *memos, str(paths["writeup"]), str(paths["pack"])], check=True)
    return paths


if __name__ == "__main__":
    for p in build().values():
        print(p)
