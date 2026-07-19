---
description: Audit your public GitHub repos against a 10/10 quality bar and output a prioritized fix-plan.
argument-hint: [repo-paths-or-github-username]
allowed-tools: ["Read", "Write", "Edit", "Bash", "Glob", "Grep", "WebFetch", "AskUserQuestion", "Skill"]
---

# /raihan-toolkit:audit-portfolio

Activate the **portfolio-audit** skill and run a full audit.

**Input:** `$ARGUMENTS` is either:
- A list of local repo paths separated by spaces, OR
- A GitHub username (single token starting with `@` or just a name), OR
- Empty — in which case ask the user what to audit.

## Workflow

1. Parse `$ARGUMENTS`. If empty, ask: "Audit local paths or a GitHub username?"
2. For each repo, run `bash ${CODEBUDDY_PLUGIN_ROOT}/scripts/audit-repo.sh <path>` to gather signals.
3. Score each repo 0–10 against `references/quality-bar.md`.
4. Output a markdown table: repo | score | top 3 missing items.
5. Below the table, list a prioritized fix-plan (easy items first).
6. Ask the user: "Auto-fix easy items? (add LICENSE, scaffold README, add .gitignore)". If yes, apply using `templates/readme-scaffold.md` — but only after explicit per-file confirmation.
7. Save the audit snapshot to `references/portfolio-snapshot.md`.

**Rules:** Confirm before writing any files (LICENSE, README, .gitignore) to the user's repos.
