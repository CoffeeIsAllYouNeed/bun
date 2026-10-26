"""BUN's own files must not break BUN's own rules. Offline."""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REFERENCES = ROOT / "skills" / "bun" / "references"
BANNED = ["game-changer", "unlock", "delve", "leverage", "thrilled to announce", "here's the thing"]


class RulesInFiles(unittest.TestCase):
    def test_hook_templates_avoid_banned_words(self):
        hooks = (REFERENCES / "HOOKS.md").read_text(encoding="utf-8").lower()
        for section in re.split(r"^## ", hooks, flags=re.M):
            block = re.search(r"templates:\n(.*?)\n\nrules:", section, re.S)
            if not block:
                continue
            for word in BANNED:
                self.assertNotIn(word, block.group(1), f"a hook template uses banned word '{word}'")

    def test_skill_md_lists_all_banned_words(self):
        skill = (ROOT / "skills" / "bun" / "SKILL.md").read_text(encoding="utf-8").lower()
        for word in BANNED:
            self.assertIn(word, skill)

    def test_skill_states_the_hard_rules(self):
        skill = (ROOT / "skills" / "bun" / "SKILL.md").read_text(encoding="utf-8")
        for rule in ("200-400 words", "No hashtags", "bullets, never numbers"):
            self.assertIn(rule, skill)

    def test_body_rules_present(self):
        body = (REFERENCES / "BODY.md").read_text(encoding="utf-8")
        for phrase in ("Never in the body", "No CTA", "[add number]"):
            self.assertIn(phrase, body)

    def test_no_stale_pointers_to_removed_files(self):
        for path in [ROOT / "skills" / "bun" / "SKILL.md", *REFERENCES.glob("*.md")]:
            text = path.read_text(encoding="utf-8")
            for gone in ("REPURPOSE.md", "EXTRACT.md", "CREDITS.md"):
                self.assertNotIn(gone, text, f"{path.name} points to removed file {gone}")


if __name__ == "__main__":
    unittest.main()
