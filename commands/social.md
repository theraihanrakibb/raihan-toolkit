---
description: Draft social-media content for FB/IG/YouTube/X/LinkedIn/Gmail from one idea. Drafting only — no auto-posting.
argument-hint: <your-content-idea> [--tone=professional|casual|promotional|educational]
allowed-tools: ["Read", "Write", "Edit", "Bash", "AskUserQuestion", "Skill"]
---

# /raihan-toolkit:social

Activate the **social-media** skill.

**Input:** `$ARGUMENTS` is the content idea, optionally with `--tone=<preset>`. If tone is missing, ask: `professional` / `casual` / `promotional` / `educational`.

## Workflow

1. Parse the idea and tone from `$ARGUMENTS`.
2. Read `references/platform-specs.md` for char limits and tone presets.
3. Draft for all 6 platforms in one run: Facebook, Instagram, YouTube (title+desc+tags), X/Twitter, LinkedIn, Gmail (subject+body).
4. Generate 10–15 hashtags for IG and 8–12 tags for YouTube.
5. Run `bash ${CODEBUDDY_PLUGIN_ROOT}/scripts/init-calendar.sh` (creates `templates/content-calendar.md` if missing).
6. Append a row to the calendar: date | idea | platforms | tone.
7. Present each platform's draft in its own fenced block so the user can copy individually.

**Rules:**
- **Drafting only.** No auto-posting, no OAuth, no API calls.
- Don't fabricate stats, quotes, or testimonials.
