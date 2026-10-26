#!/usr/bin/env python3
"""Run every offline check. Run this before you push.

    python3 -m pip install -r requirements-dev.txt
    python3 scripts/selftest.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STEPS = [
    ("secrets", [sys.executable, "scripts/check_no_secrets.py"]),
    ("frontmatter", [sys.executable, "scripts/check_frontmatter.py"]),
    ("markdown references", [sys.executable, "scripts/check_markdown_references.py"]),
    ("tests", [sys.executable, "-m", "unittest", "discover", "-s", "tests"]),
]


def main() -> int:
    failed = []
    for name, cmd in STEPS:
        result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        status = "ok  " if result.returncode == 0 else "FAIL"
        print(f"{status} {name}")
        if result.returncode != 0:
            failed.append(name)
            print((result.stdout + result.stderr).strip())
    print("\nall checks passed" if not failed else f"\nfailed: {', '.join(failed)}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
