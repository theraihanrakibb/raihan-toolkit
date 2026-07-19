---
name: portfolio-audit
description: Audits the user's public GitHub repositories against a 10/10 quality bar when they ask to "audit my portfolio", "score my repos", "check repo quality", "which repos need improvement", or want a fix-plan for missing README/LICENSE/CI/tests. Use this skill whenever the user wants to evaluate or raise the quality of their public repos.
---

# Portfolio Quality Audit

## When to Use
- User asks to audit, score, or quality-check their public repos.
- User wants a fix-plan for missing README, LICENSE, CI, tests, examples, etc.
- User is preparing repos for a job hunt and wants them at 10/10 quality.

## How to Use

1. **Identify repos to audit.** Ask the user (or accept as input) for either:
   - A list of local repo paths (e.g. `e:\CodingWorkplace\sglang-fork`), OR
   - Their GitHub username (fetch the public repo list via `gh repo list <user> --public --limit 100`).
2. **For each repo**, run `scripts/audit-repo.sh <path>` to gather signals, then score against the criteria in `references/quality-bar.md`.
3. **Score each repo 0–10** with a per-criterion breakdown. The criteria are:
   - README quality (exists, has install/run/usage, has examples or screenshots)
   - LICENSE present
   - CI present (`.github/workflows/`)
   - Tests present (`tests/`, `test/`, `*_test.py`, `*.test.js`, etc.)
   - Examples directory
   - CONTRIBUTING.md
   - CODE_OF_CONDUCT.md
   - .gitignore appropriate for the language
   - Repo description + topics set on GitHub
   - Releases / tags (for libraries)
4. **Output a prioritized fix-plan** as markdown: rank repos by lowest score, list specific missing items per repo, mark each as `[easy]` / `[medium]` / `[hard]`.
5. **Offer to auto-fix easy items** (add LICENSE, scaffold README, add .gitignore) — only after explicit user confirmation. Use the templates in `templates/readme-scaffold.md`.
6. **Save a snapshot** to `references/portfolio-snapshot.md` with date, scores, and fix-plan so progress is trackable over time.

## Rules
- Do not push or commit anything without explicit user confirmation.
- When auditing remote GitHub repos, prefer `gh` CLI. If unavailable, ask the user to clone locally first.

## References
- `references/quality-bar.md` — the 10/10 criteria (authoritative).
- `templates/readme-scaffold.md` — README template for auto-fixes.
- `scripts/audit-repo.sh` — repo signal gatherer.
