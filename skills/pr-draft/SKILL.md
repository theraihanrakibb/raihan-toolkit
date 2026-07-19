---
name: pr-draft
description: Generates a clean Conventional Commit message, PR description, and changelog entry from staged or recent git changes when the user asks "write a commit message", "draft a PR", "what should my commit message be", "summarize my diff", or "make a PR description". Use this skill whenever the user wants to turn git changes into well-structured commit/PR text.
---

# Clean Commit / PR Writer

## When to Use
- User asks for a commit message, PR description, or changelog entry.
- User has staged changes and wants to summarize them.
- User is about to push and wants a clean message.

## How to Use

1. **Get the diff.** Run `bash scripts/git-diff-staged.sh` from the plugin root to fetch the staged diff. If nothing is staged, fall back to `git diff HEAD~1` (last commit) or ask the user what to base the message on.
2. **Generate three outputs:**
   1. **Conventional Commit message** — `<type>(<scope>): <subject>` then a body. Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`, `build`, `ci`. Subject ≤ 72 chars, imperative mood, lowercase first word, no period.
   2. **PR description** — use `templates/pr-description.md`. Sections: Summary, Changes (bulleted), Why, Testing, Screenshots (placeholder).
   3. **Changelog entry** — one-line `Keep a Changelog` style entry under the right section (Added / Changed / Fixed / Removed).
3. **Present the message** to the user. If they approve, you may run `git commit -m "<message>"` for them — but only after explicit confirmation.

## Rules
- Don't push without explicit confirmation.
- Don't amend published commits.

## References
- `templates/pr-description.md`
- `scripts/git-diff-staged.sh`
- `hooks/validate-commit.sh` (the enforcing hook)
