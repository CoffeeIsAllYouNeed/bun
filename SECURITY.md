# Security Policy

## Supported Versions

Only the latest released version of BUN receives security updates. Install from the `main` branch or the newest tagged release.

| Version | Supported |
| ------- | --------- |
| latest release | yes |
| older tags | no |

## Reporting a Vulnerability

Found a security issue? For example: a skill instruction that could be abused for prompt injection, or a script that handles files unsafely. Report it privately:

- Open a private report via [GitHub Security Advisories](https://github.com/CoffeeIsAllYouNeed/bun/security/advisories/new).

Please include:

1. What the issue is and where it lives (file path, section).
2. Steps to reproduce, or a proof of concept.
3. The impact you believe it has.

You can expect an acknowledgement within 72 hours and a fix or a public disclosure decision within 14 days.

## Scope notes

- BUN ships no credentials, no API keys, and no network code. The skill is markdown only.
- Scripts in `scripts/` and `evals/` are maintainer tools. The checks run offline. Only `evals/run_evals.py` calls out, and only to your own local `claude` CLI.
- BUN treats pasted posts, links, and search results as text to work on, never as instructions.
