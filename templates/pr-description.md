# PR Description Template

> Filled in by the `pr-draft` skill.

---

## Summary

[1–2 sentences: what this PR does and why. Lead with the user-facing or system-level impact, not the implementation.]

## Changes

- [Change 1 — what + why]
- [Change 2]
- [Change 3]

## Why

[2–4 sentences: motivation, alternatives considered, why this approach. Reference an issue if applicable: `Closes #123` or `Refs #123`.]

## Testing

- [ ] `pre-commit run --all-files` is green (or `./.format.sh` for vLLM)
- [ ] Targeted test: `pytest test/srt/test_<area>.py -k <name> -x`
- [ ] Manual: [one specific manual check — e.g. "started server, sent 3 requests, observed expected KV cache reuse"]

## Screenshots / Logs (optional)

<!-- Paste before/after screenshots, flame graphs, or log snippets if relevant. Delete this section if not. -->

## Notes for Reviewers

<!-- Anything non-obvious? Areas you'd like extra eyes on? Delete if not needed. -->

---

## Fill-in checklist (for the skill)
- [ ] Summary leads with impact, not implementation.
- [ ] Changes are bulleted, each one says WHY not just WHAT.
- [ ] Linked issue referenced (`Closes #NNN`).
- [ ] Testing section lists at least one specific command + one manual check.
