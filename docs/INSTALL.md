# Install

Load BUN once. Use it in every chat after.

## Claude on web or desktop

1. Get `bun.zip` from the latest release, or run `python3 scripts/build_zip.py`.
2. Open Claude. Go to Customize > Skills.
3. Click `+`. Pick Upload a skill. Choose `bun.zip`.
4. Switch BUN on.
5. New chat. Type: `Write a LinkedIn post`.

Works? BUN asks niche, audience, goal, and whether you have an idea.

## Zip rule

Zip must hold one folder named `bun`. Folder name = `name:` line in `SKILL.md`.

```
bun.zip
└── bun/
    ├── SKILL.md
    └── references/
```

Wrong folder name? Upload fails. Rename the folder. Zip again.

## Add from the repository

Customize > Plugins > Add > Add marketplace > Add from a repository. Paste `CoffeeIsAllYouNeed/bun`. Sync. Find BUN under Discover. Click Add.

## Claude Code

```
/plugin marketplace add CoffeeIsAllYouNeed/bun
/plugin install bun@bun
```

Or clone the repo and open it. The `.claude/skills/bun` symlink loads the skill. No install needed.

## Update

New `bun.zip`? Upload it the same way. Start a new chat.

## Remove

Customize > Skills. Switch BUN off, or delete it.

## Web search

Only the "search ideas for me" path needs it. Skip search? Pick "I have an idea" and give your own story.
