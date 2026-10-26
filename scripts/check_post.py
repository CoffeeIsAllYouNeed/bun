#!/usr/bin/env python3
"""Check a finished post against BUN's hard rules. Offline, deterministic.

    python3 scripts/check_post.py post.txt
    python3 scripts/check_post.py post.txt --details "I reviewed 40 resumes..."

With --details, every number in the post must also appear in the details.
That catches invented facts. Exit code 0 = pass, 1 = at least one rule broken.

Checks facts a machine can check. It does not judge if a hook is good.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

BANNED = ["game-changer", "unlock", "delve", "leverage", "thrilled to announce", "here's the thing"]
BAD_BULLETS = re.compile(r"^\s*(?:[*+]|[✅✔✓→▶▪◆★]|[\U0001F300-\U0001FAFF])")
NUMBERED = re.compile(r"^\s*\d+[.)]\s")
HASHTAG = re.compile(r"(?<![\w&])#[A-Za-z]\w*")
URL = re.compile(r"https?://|www\.")
NUMBER = re.compile(r"\d[\d,.]*")


def numbers(text: str) -> set[str]:
    return {n.strip(",.") for n in NUMBER.findall(text)}


def check(post: str, details: str | None = None) -> list[str]:
    failures: list[str] = []
    text = post.strip()
    words = len(text.split())
    if not 200 <= words <= 400:
        failures.append(f"length: {words} words, rule is 200-400")
    if HASHTAG.search(text):
        failures.append("hashtag found")
    if any(NUMBERED.match(line) for line in text.splitlines()):
        failures.append("numbered list found, lists must be bullets")
    if any(BAD_BULLETS.match(line) for line in text.splitlines()):
        failures.append("emoji or symbol bullet found, use •, ➤ or -")
    if URL.search(text):
        failures.append("link in the body, links go in the first comment")
    lowered = text.lower().replace("’", "'")
    for word in BANNED:
        if word in lowered:
            failures.append(f"banned word: {word}")
    if "—" in text or "–" in text:
        failures.append("em or en dash found")
    paragraphs = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    if paragraphs and len(paragraphs[0].splitlines()) > 2:
        failures.append("hook is longer than 2 lines")
    last = text.splitlines()[-1].strip() if text else ""
    if last.endswith("?"):
        failures.append("post ends with a question, rule is a hard stop")
    if details is not None:
        invented = sorted(numbers(text) - numbers(details))
        if invented:
            failures.append(f"numbers not in the user's details: {invented}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("file", type=Path)
    parser.add_argument("--details", help="the real facts the user gave; numbers outside it fail")
    args = parser.parse_args()
    failures = check(args.file.read_text(encoding="utf-8"), args.details)
    for f in failures:
        print("FAIL", f)
    if not failures:
        print("ok: post follows BUN's hard rules")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
