"""Check that every number in the memo can be traced to an agent output file.

Usage: python -m desk.memo_check runs/DGE/<date>
Exits with an error listing any memo number not found in the other output files.
Numbers are compared after rounding, so 1,234.5 in the memo matches 1234.48 in a JSON file.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

NUMBER = re.compile(r"(?<![\w.])-?\d[\d,]*\.?\d*")
IGNORE = {str(y) for y in range(2015, 2036)} | {str(i) for i in range(0, 11)}  # years and small counters


def numbers_in(text: str) -> list[str]:
    return [m.group().replace(",", "").rstrip(".") for m in NUMBER.finditer(text)]


def matches(memo_num: str, source_nums: set[float]) -> bool:
    x = abs(float(memo_num))  # signs are compared loosely: memos often write "down 2%" or use a typographic minus
    decimals = len(memo_num.split(".")[1]) if "." in memo_num else 0
    tol = 0.5 * 10 ** -decimals
    candidates = (x, x / 100)  # percentages in the memo may be decimals in the outputs
    return any(abs(c - s) <= tol * (1 if c == x else 0.01) + 1e-12 for c in candidates for s in source_nums)


def check(run_dir: str) -> list[str]:
    run = Path(run_dir)
    memo = (run / "editor" / "memo.md").read_text()
    body = memo.split("## Sources")[0]  # the sources appendix contains page numbers, not analysis
    source_nums: set[float] = set()
    for f in run.rglob("*"):
        if f.is_file() and f.suffix in {".json", ".csv", ".md", ".yaml"} and f.parent.name != "editor":
            source_nums.update(abs(float(n)) for n in numbers_in(f.read_text(errors="ignore")) if n not in {"-", ""})
    return [n for n in numbers_in(body) if n not in IGNORE and not matches(n, source_nums)]


if __name__ == "__main__":
    unmatched = check(sys.argv[1])
    if unmatched:
        sys.exit(f"Memo numbers not found in any agent output: {sorted(set(unmatched))}")
    print("All memo numbers trace to agent outputs.")
