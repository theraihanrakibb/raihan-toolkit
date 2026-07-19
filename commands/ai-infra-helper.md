---
description: Navigate SGLang/vLLM-style repos, get test/lint commands, understand fork-PR CI behavior, draft PRs.
argument-hint: [question-or-repo-path]
allowed-tools: ["Read", "Write", "Edit", "Bash", "Glob", "Grep", "AskUserQuestion", "Skill"]
---

# /raihan-toolkit:ai-infra-helper

Activate the **ai-infra-helper** skill.

**Input:** `$ARGUMENTS` is the user's question, optionally prefixed with a repo path. If empty, ask what they need.

## Workflow

1. Identify the repo (ask if unclear). Load `references/ai-infra-repos.md` for the layout cheat-sheet.
2. If the question is about structure → point at the likely file(s) using the cheat-sheet, then verify with `Grep` / `Glob`.
3. If the question is about tests/lint → give the minimal command from the reference doc. Remind the user of the fork-PR CI behavior:
   > For SGLang: fork PRs fail `pr-gate` / `pr-test-*` by design. **Only `lint` actually gates your code.**
4. If the user wants a PR drafted → switch to the `pr-draft` workflow.
5. If they want to push → remind them to push to their fork, not upstream. Confirm before any push.

**Rules:** Don't run the full test suite just to make fork-only CI green.
