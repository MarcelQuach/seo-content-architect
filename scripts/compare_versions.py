#!/usr/bin/env python3
"""Compare draft A and manually humanized version B without automatic API calls.

Usage: python scripts/compare_versions.py draft_a.txt draft_b.txt comparison.html
Produces a side-by-side-style inline HTML diff for editorial review.
This does NOT replace fact checking or SEO quality assurance.
"""
import difflib
import html
import sys
from pathlib import Path

def compare(a, b, destination):
    left = Path(a).read_text(encoding="utf-8")
    right = Path(b).read_text(encoding="utf-8")
    diff = difflib.HtmlDiff(wrapcolumn=72).make_file(
        left.splitlines(), right.splitlines(),
        fromdesc="Original approved draft A",
        todesc="Manually edited/humanized draft B",
        context=True, numlines=3, charset="utf-8")
    note = ("<p><strong>Manual QA B required:</strong> Validate factual claims, product specs, "
            "figures, missing expertise, keyword coverage, search intent, links and brand tone. "
            "Differences alone do not certify content quality.</p>")
    diff = diff.replace("<body>", "<body>" + note, 1)
    Path(destination).parent.mkdir(parents=True, exist_ok=True)
    Path(destination).write_text(diff, encoding="utf-8")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit("Usage: compare_versions.py draft_a.txt draft_b.txt diff.html")
    compare(*sys.argv[1:4])
    print(sys.argv[3])
