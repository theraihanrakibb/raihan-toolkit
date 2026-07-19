---
description: Generate a Conventional Commit message, PR description, and changelog entry from staged or recent git changes.
argument-hint: [--from=<ref>] [--scope=<scope>]
allowed-tools: ["Read", "Write", "Edit", "Bash", "AskUserQuestion", "Skill"]
---

# /raihan-toolkit:pr-draft

Activate the **pr-draft** skill.

**Input:** `$ARGUMENTS` optional flags:
- `--from=<ref>` — base the diff on this ref instead of staged changes (e.g. `--from=HEAD~1`).
- `--scope=<scope>` — suggested Conventional Commit scope.

## Workflow

1. Run `bash ${CODEBUDDY_PLUGIN_ROOT}/scripts/git-diff-staged.sh` to fetch the diff.
   - If nothing is staged and `--from` is given, run `git diff <from>...HEAD` instead.
   - If neither, ask the user what to base the message on.
2. Generate the three outputs:
   - Conventional Commit message (`<type>(<scope>): <subject>` + body).
   - PR description from `templates/pr-description.md`.
   - Changelog entry (Keep a Changelog style).
3. Show all three to the user.
4. If the user approves the commit message, offer to run `git commit -m "<message>"` — only after explicit confirmation. Do NOT push.

**Rules:** Don't add AI trailers (`Generated with`, `Co-Authored-By:`) to the commit message — the `hooks/validate-commit.sh` hook will deny them. Don't push without confirmation.
