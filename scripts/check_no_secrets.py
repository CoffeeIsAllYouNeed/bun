#!/usr/bin/env python3
"""Fail if a credential, or a file that holds one, is in the repository.

BUN needs no credentials. So any `.env` file or key-shaped string is a mistake.
`.gitignore` only stops untracked files: a rename can still commit a real `.env`.
This checks the files themselves.

Usage: python3 scripts/check_no_secrets.py
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BAD_NAMES = re.compile(r"(^|/)(\.env(\..*)?|.*\.pem|.*\.key|id_rsa|credentials\.json)$")
KEY_SHAPES = [
    re.compile(r"\bsk-[A-Za-z0-9_\-]{20,}"),
    re.compile(r"\bghp_[A-Za-z0-9]{30,}"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bxox[abp]-[A-Za-z0-9\-]{10,}"),
    re.compile(r"-----BEGIN (RSA |EC )?PRIVATE KEY-----"),
]
SKIP_DIRS = {".git", "__pycache__", "dist", "runs"}


def files() -> list[Path]:
    try:
        out = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True).stdout
        listed = [ROOT / line for line in out.splitlines() if line]
        if listed:
            return listed
    except (OSError, subprocess.CalledProcessError):
        pass
    return [p for p in ROOT.rglob("*") if p.is_file() and not (SKIP_DIRS & set(p.relative_to(ROOT).parts))]


def main() -> int:
    problems = []
    for path in files():
        rel = path.relative_to(ROOT).as_posix()
        if BAD_NAMES.search(rel) and rel != ".env.example":
            problems.append(f"{rel}: file name looks like a credential file")
            continue
        if path.suffix in {".png", ".zip", ".svg"} or not path.exists():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for shape in KEY_SHAPES:
            if shape.search(text):
                problems.append(f"{rel}: contains a key-shaped string")
                break
    for p in problems:
        print("FAIL", p)
    if not problems:
        print("ok: no credentials found")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
