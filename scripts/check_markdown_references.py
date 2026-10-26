#!/usr/bin/env python3
"""Check that Markdown references resolve.

Covers two things:
  1. Relative Markdown links in README.md, docs/, NOTICE.md, SECURITY.md.
  2. `references/X.md` mentions in skills/bun/SKILL.md and its reference files.

Usage: python3 scripts/check_markdown_references.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"\]\(([^)\s]+)\)")
SKILL_REF = re.compile(r"references/([A-Za-z0-9_\-]+\.md)")


def link_problems(doc: Path) -> list[str]:
    problems = []
    for target in LINK.findall(doc.read_text(encoding="utf-8")):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        path = target.split("#", 1)[0]
        if path and not (doc.parent / path).exists():
            problems.append(f"{doc.relative_to(ROOT)}: broken link '{target}'")
    return problems


def main() -> int:
    problems: list[str] = []
    docs = [ROOT / n for n in ("README.md", "NOTICE.md", "SECURITY.md") if (ROOT / n).exists()]
    docs += sorted((ROOT / "docs").glob("*.md"))
    for doc in docs:
        problems += link_problems(doc)
    skill_dir = ROOT / "skills" / "bun"
    for doc in [skill_dir / "SKILL.md", *sorted((skill_dir / "references").glob("*.md"))]:
        for name in SKILL_REF.findall(doc.read_text(encoding="utf-8")):
            if not (skill_dir / "references" / name).exists():
                problems.append(f"{doc.relative_to(ROOT)}: references/{name} does not exist")
    for p in problems:
        print("FAIL", p)
    if not problems:
        print("ok: every Markdown reference resolves")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
