#!/usr/bin/env python3
"""Does BUN do what it claims? Run the agent on 5 made-up cases and grade the post.

    python3 evals/run_evals.py                       # every case (needs the `claude` CLI)
    python3 evals/run_evals.py --case resume-skills-list
    python3 evals/run_evals.py --list
    python3 evals/run_evals.py --grade-file answer.txt --case resume-skills-list

The tests in `tests/` check the files. This checks the thing the files are for:
what comes back when Claude follows them. Graders are deterministic and narrow
on purpose (scripts/check_post.py): length, hashtags, numbered lists, links,
banned words, dashes, the ending, and invented numbers. They do not judge taste.

Case "emergency-fund-no-details" gives no facts. A pass is either asking for a
real detail or writing the post with no numbers at all. Inventing one fails.

Costs one model call per case. Run from the repo root so .claude/skills is found.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import check_post  # noqa: E402

CASES = json.loads((pathlib.Path(__file__).with_name("cases.json")).read_text(encoding="utf-8"))["cases"]


def prompt_for(case: dict) -> str:
    facts = case["details"] or "I have no numbers or facts to share for this idea."
    return (
        "Use the bun skill. Here are my answers to your start question.\n"
        f"Niche: {case['niche']}\n"
        f"Target audience: {case['audience']}\n"
        f"Post goal: {case['goal']}\n"
        f"I have an idea: {case['idea']}\n"
        f"Real details: {facts}\n\n"
        "Pick the hook type that best fits my goal yourself. Do not ask me to choose. "
        "Reply with the final post only."
    )


def extract_post(output: str) -> str:
    """Drop a leading 'Hook type: ...' label line if the agent adds one."""
    lines = output.strip().splitlines()
    while lines and re.match(r"^\s*(hook type|type)\s*[:\-]", lines[0], re.I):
        lines.pop(0)
    return "\n".join(lines).strip()


def grade(case: dict, output: str) -> tuple[bool, str]:
    post = extract_post(output)
    has_details = bool(case["details"])
    if not has_details and len(post.split()) < 200 and "?" in post:
        return True, "asked for a real detail instead of inventing one"
    failures = check_post.check(post, case["details"] if has_details else "")
    if failures:
        return False, "; ".join(failures)
    return True, f"{len(post.split())} words, all hard rules held"


def ask(prompt: str, timeout: int) -> tuple[str, str]:
    try:
        result = subprocess.run(
            ["claude", "-p", prompt, "--output-format", "text"],
            cwd=ROOT, capture_output=True, encoding="utf-8", timeout=timeout,
        )
    except FileNotFoundError:
        return "", "the `claude` CLI is not on PATH"
    except subprocess.TimeoutExpired:
        return "", f"no answer within {timeout}s"
    if result.returncode != 0:
        return "", (result.stderr or result.stdout).strip().splitlines()[-1][:90]
    return result.stdout, ""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--case", action="append", help="run only these (repeatable)")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--timeout", type=int, default=420)
    parser.add_argument("--save", type=pathlib.Path, help="write every answer to this folder")
    parser.add_argument("--grade-file", type=pathlib.Path, help="grade a saved answer (needs one --case), no model call")
    args = parser.parse_args()

    if args.list:
        for case in CASES:
            print(f"{case['name']:28} {case['niche']}")
        return 0
    chosen = [c for c in CASES if not args.case or c["name"] in args.case]
    if not chosen:
        print("no case matches")
        return 2
    if args.grade_file:
        if len(chosen) != 1:
            print("--grade-file needs exactly one --case")
            return 2
        ok, why = grade(chosen[0], args.grade_file.read_text(encoding="utf-8"))
        print(("PASS " if ok else "FAIL ") + chosen[0]["name"] + ": " + why)
        return 0 if ok else 1

    passed = 0
    for case in chosen:
        output, error = ask(prompt_for(case), args.timeout)
        if error:
            print(f"SKIP {case['name']}: {error}")
            continue
        if args.save:
            args.save.mkdir(parents=True, exist_ok=True)
            (args.save / f"{case['name']}.txt").write_text(output, encoding="utf-8")
        ok, why = grade(case, output)
        passed += ok
        print(("PASS " if ok else "FAIL ") + f"{case['name']}: {why}")
    print(f"\n{passed}/{len(chosen)} passed")
    return 0 if passed == len(chosen) else 1


if __name__ == "__main__":
    sys.exit(main())
