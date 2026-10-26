# Project conventions - bun (Claude Code)

For Claude Code working on this repository. Read before making changes. These are mandatory unless the user says otherwise.

## Versioning

- `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` must match on name, version, author, license, homepage, and description.
- Default: bump the PATCH segment (`0.0.X`) for every shippable change. Bump MINOR or MAJOR only when the user asks.
- After a bump: tag the commit (`git tag -a vX.Y.Z -m "..."`), push the tag, then publish a GitHub Release. A tag alone does not update the release badge.

## Skill invariants

- Exactly 1 skill: `skills/bun/`. The folder name must equal `name:` in its `SKILL.md`. The upload zip depends on this.
- `description:` is 400 characters or fewer, has no em dash, and ends with a "Not for ..." sentence.
- `SKILL.md` stays short: 300 words or fewer. It holds the start question, the 5 stages, and 4 rules. Detail goes in `references/`.
- Each reference file is read once, at its stage: `IDEAS.md`, `HOOKS.md`, `BODY.md`, `HUMANIZER.md`, `TOKEN_SAVING.md`.
- Every file in `skills/bun/references/` is named in `SKILL.md`.

## Writing rules BUN enforces

Never weaken these without the user asking:

- 200-400 words per post.
- No hashtags.
- Lists are bullets, never numbers, unless the user asks.
- No links in the post body. Links go in the first comment.
- The post ends with a hard stop. No CTA. No question.
- No invented facts. A missing number becomes `[add number]` and a question.
- Banned words: "game-changer", "unlock", "delve", "leverage", "thrilled to announce", "Here's the thing".

## Counts

Counts in `README.md` must match the files. `tests/test_reference_counts.py` checks them: hook types, hook templates, idea shapes, core AI tells.

## .claude/skills mirror

`.claude/skills/bun` is a symlink to `skills/bun`. Claude Code finds the skill from a plain clone. Do not replace it with a copy.

## Validation before push

```bash
python3 scripts/selftest.py
```

It runs the secret check, the frontmatter check, the Markdown reference check, and the offline tests. Fix everything before pushing.

## Credits

Material adapted from other projects goes in `NOTICE.md` with its license. Keep it up to date.
