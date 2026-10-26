#!/usr/bin/env python3
"""Build dist/bun.zip, the file you upload in Claude (Customize > Skills).

The zip holds one folder named `bun`, which must equal `name:` in SKILL.md.

Usage: python3 scripts/build_zip.py
"""
from __future__ import annotations

import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "skills" / "bun"
OUT = ROOT / "dist" / "bun.zip"


def main() -> int:
    if not (SRC / "SKILL.md").is_file():
        print("skills/bun/SKILL.md not found")
        return 1
    OUT.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(SRC.rglob("*")):
            if path.is_file() and "__pycache__" not in path.parts:
                zf.write(path, Path("bun") / path.relative_to(SRC))
    print(f"ok: wrote {OUT.relative_to(ROOT)} ({len(zipfile.ZipFile(OUT).namelist())} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
