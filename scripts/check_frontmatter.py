#!/usr/bin/env python3
"""Parse every skills/*/SKILL.md frontmatter with a strict YAML loader.

A SKILL.md that looks fine can still fail to load: an unescaped quote inside
`description` ends the scalar early and the loader skips the skill in silence.
This checks what a strict loader sees, and that the folder name equals `name:`.

Usage: python3 scripts/check_frontmatter.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("PyYAML is missing. Run: python3 -m pip install -r requirements-dev.txt")

ROOT = Path(__file__).resolve().parents[1]
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)


def check(skill_md: Path) -> list[str]:
    problems: list[str] = []
    text = skill_md.read_text(encoding="utf-8")
    match = FRONTMATTER.match(text)
    if not match:
        return [f"{skill_md}: no frontmatter block"]
    try:
        data = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        return [f"{skill_md}: frontmatter does not parse: {exc}"]
    if not isinstance(data, dict):
        return [f"{skill_md}: frontmatter is not a mapping"]
    name, description = data.get("name"), data.get("description")
    if not name:
        problems.append(f"{skill_md}: missing name")
    elif name != skill_md.parent.name:
        problems.append(f"{skill_md}: name '{name}' does not match folder '{skill_md.parent.name}'")
    if not description:
        problems.append(f"{skill_md}: missing description")
    elif len(str(description)) > 400:
        problems.append(f"{skill_md}: description is {len(str(description))} chars, limit is 400")
    return problems


def main() -> int:
    skills = sorted((ROOT / "skills").glob("*/SKILL.md"))
    if not skills:
        print("no skills found under skills/")
        return 1
    problems = [p for s in skills for p in check(s)]
    for p in problems:
        print("FAIL", p)
    if not problems:
        print(f"ok: {len(skills)} skill(s) parse and match their folder name")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
