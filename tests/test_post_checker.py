"""scripts/check_post.py must pass a good post and catch each broken rule. Offline."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import check_post  # noqa: E402

FIXTURES = ROOT / "tests" / "fixtures"
GOOD = (FIXTURES / "good_post.txt").read_text(encoding="utf-8")
DETAILS = (FIXTURES / "details.txt").read_text(encoding="utf-8")


def fails(post: str, details: str | None = None) -> str:
    return " | ".join(check_post.check(post, details))


class PostChecker(unittest.TestCase):
    def test_good_post_passes(self):
        self.assertEqual(check_post.check(GOOD, DETAILS), [])

    def test_bad_fixture_trips_every_rule(self):
        bad = (FIXTURES / "bad_post.txt").read_text(encoding="utf-8")
        report = fails(bad, DETAILS)
        for expected in ("length", "hashtag", "numbered list", "bullet", "link", "banned word", "dash", "numbers not in"):
            self.assertIn(expected, report)

    def test_too_short(self):
        self.assertIn("length", fails("Short post."))

    def test_hashtag(self):
        self.assertIn("hashtag", fails(GOOD + "\n#resume"))

    def test_link(self):
        self.assertIn("link", fails(GOOD + "\nhttps://example.com"))

    def test_invented_number(self):
        self.assertIn("numbers not in", fails(GOOD + " It lifted replies by 92%.", DETAILS))

    def test_question_ending(self):
        self.assertIn("question", fails(GOOD.rstrip() + "\nSound familiar?"))

    def test_em_dash(self):
        self.assertIn("dash", fails(GOOD.replace("Six lines or more.", "Six lines — or more.")))

    def test_long_hook(self):
        long_hook = "Line one.\nLine two.\nLine three.\n\n" + GOOD.split("\n\n", 1)[1]
        self.assertIn("hook", fails(long_hook))


if __name__ == "__main__":
    unittest.main()
