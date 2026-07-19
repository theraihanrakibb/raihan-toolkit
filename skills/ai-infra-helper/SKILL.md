---
name: ai-infra-helper
description: Helps the user contribute to AI-inference open-source repos (SGLang, vLLM, TensorRT-LLM, etc.) when they ask "how is sglang structured", "where do I add a model in sglang", "what tests do I run before pushing", "draft a PR for this sglang change", or "why is my fork PR CI failing". Use this skill whenever the user is working inside an AI-inference repo and needs navigation help, test/lint commands, or PR drafting.
---

# AI-Infra Contributor Coach

## When to Use
- User is working inside an AI-inference repo (SGLang, vLLM, TensorRT-LLM, lmdeploy, etc.) and asks about structure, tests, lint, or PR prep.
- User's fork-PR CI is failing and they want to know which checks actually gate their code.

## How to Use

1. **Identify the repo.** If unclear, ask which repo (SGLang fork? vLLM? other). Read `references/ai-infra-repos.md` for the repo's layout cheat-sheet.
2. **For "where do I make change X" questions**, use the layout cheat-sheet to point at the likely file(s), then verify with `Grep` / `Glob` before answering.
3. **For "what tests do I run"**, give the **minimal** lint+test command from the reference doc — usually `pre-commit` + the targeted test path, NOT the full suite. Remind the user:
   > **Fork-PR CI behavior (important!)** For SGLang: fork PRs fail `pr-gate` / `pr-test-*` by design — those checks need repo secrets the fork doesn't have. **Only `lint` actually gates your code.** Don't waste cycles trying to make `pr-test-*` green; just make `lint` green.
4. **For "draft a PR"**, follow the `pr-draft` skill workflow — Conventional Commit message + PR description from `templates/pr-description.md`, with the no-AI-footer rule.

## Rules
- Don't push to upstream — only to the user's fork.
- Don't run the full SGLang test suite locally just to "make CI green" — it's slow and most failures are fork-only.

## References
- `references/ai-infra-repos.md` — SGLang/vLLM layout + CI behavior (authoritative).
- `templates/pr-description.md`
- The `pr-draft` skill (for PR drafting workflow).
