"""The skill must load, and its parts must hang together. Offline."""
from __future__ import annotations

import re
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "skills" / "bun"
SKILL_MD = SKILL_DIR / "SKILL.md"
REFERENCES = SKILL_DIR / "references"
EXPECTED_REFERENCES = {"IDEAS.md", "HOOKS.md", "BODY.md", "HUMANIZER.md", "TOKEN_SAVING.md"}


def frontmatter() -> dict:
    match = re.match(r"\A---\n(.*?)\n---\n", SKILL_MD.read_text(encoding="utf-8"), re.S)
    assert match, "SKILL.md has no frontmatter"
    return yaml.safe_load(match.group(1))


class SkillStructure(unittest.TestCase):
    def test_name_matches_folder(self):
        self.assertEqual(frontmatter()["name"], SKILL_DIR.name)

    def test_description_is_short_and_disambiguated(self):
        description = frontmatter()["description"]
        self.assertLessEqual(len(description), 400)
        self.assertNotIn("—", description)
        self.assertIn("Not for", description)

    def test_skill_md_stays_short(self):
        text = SKILL_MD.read_text(encoding="utf-8")
        self.assertLessEqual(len(text.split()), 300, "SKILL.md grew past 300 words, move detail to references/")

    def test_reference_files_are_exactly_the_expected_five(self):
        self.assertEqual({p.name for p in REFERENCES.glob("*.md")}, EXPECTED_REFERENCES)

    def test_every_reference_is_named_in_skill_md(self):
        text = SKILL_MD.read_text(encoding="utf-8")
        for name in EXPECTED_REFERENCES:
            self.assertIn(f"references/{name}", text, f"SKILL.md never points to {name}")

    def test_plugin_manifests_agree(self):
        import json

        plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        market = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
        entry = market["plugins"][0]
        for key in ("name", "version", "license", "homepage", "description"):
            self.assertEqual(plugin[key], entry[key], f"plugin.json and marketplace.json differ on {key}")
        self.assertEqual(plugin["author"], entry["author"])
        self.assertEqual(plugin["name"], frontmatter()["name"])

    def test_claude_skills_mirror_points_at_the_skill(self):
        mirror = ROOT / ".claude" / "skills" / "bun"
        self.assertTrue(mirror.exists(), ".claude/skills/bun is missing or a broken symlink")
        self.assertEqual(mirror.resolve(), SKILL_DIR.resolve())


if __name__ == "__main__":
    unittest.main()
