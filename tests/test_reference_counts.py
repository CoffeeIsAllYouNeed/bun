"""Numbers claimed in README.md must match the reference files. Offline."""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REFERENCES = ROOT / "skills" / "bun" / "references"


def read(name: str) -> str:
    return (REFERENCES / name).read_text(encoding="utf-8")


def hook_types_and_templates() -> tuple[int, int]:
    hooks = read("HOOKS.md")
    types = re.findall(r"^## (\d+)\. ", hooks, re.M)
    templates = 0
    for section in re.split(r"^## ", hooks, flags=re.M):
        if not re.match(r"\d+\. ", section):
            continue
        block = re.search(r"Templates:\n(.*?)\n\nRules:", section, re.S)
        templates += len(re.findall(r"^- ", block.group(1), re.M)) if block else 0
    return len(types), templates


def idea_shapes() -> int:
    ideas = read("IDEAS.md")
    shapes = ideas.split("## IDEA SHAPES", 1)[1].split("## MODE", 1)[0]
    return len(re.findall(r"^\d+\. ", shapes, re.M))


def core_tells() -> int:
    text = read("HUMANIZER.md")
    block = text.split("## Strong tells", 1)[1].split("## Share-post tells", 1)[0]
    return len(re.findall(r"^\d+\. ", block, re.M))


class ReferenceCounts(unittest.TestCase):
    def setUp(self):
        self.readme = (ROOT / "README.md").read_text(encoding="utf-8")

    def test_hook_types_and_templates(self):
        types, templates = hook_types_and_templates()
        self.assertIn(f"{types} hook types", self.readme)
        self.assertIn(f"{templates} hook templates", self.readme)

    def test_idea_shapes(self):
        self.assertIn(f"{idea_shapes()} idea shapes", self.readme)

    def test_core_tells(self):
        self.assertIn(f"{core_tells()} core AI tells", self.readme)

    def test_plugin_description_counts(self):
        import json

        types, templates = hook_types_and_templates()
        description = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))["description"]
        for phrase in (f"{types} hook types", f"{templates} hook templates", f"{idea_shapes()} idea shapes"):
            self.assertIn(phrase, description)

    def test_every_hook_type_has_templates_and_rules(self):
        hooks = read("HOOKS.md")
        for section in re.split(r"^## ", hooks, flags=re.M):
            if re.match(r"\d+\. ", section):
                self.assertIn("Templates:", section, section.splitlines()[0])
                self.assertIn("Rules:", section, section.splitlines()[0])


if __name__ == "__main__":
    unittest.main()
