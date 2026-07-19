---
name: social-media
description: Drafts social-media content for multiple platforms from one idea when the user asks "draft a post for facebook", "write an instagram caption", "youtube title and description", "tweet this", "linkedin post", "gmail subject and body", "cross-post this idea", "content calendar", or "hashtag ideas". Use this skill whenever the user wants to draft or repurpose social-media content.
---

# Social Media Content Drafter

## When to Use
- User wants to draft a post/caption/title for one or more platforms.
- User has one idea and wants it adapted to FB, IG, YouTube, X, LinkedIn, and Gmail.
- User wants a content calendar entry.

## How to Use

1. **Get the idea + tone.** Accept the source idea from `$ARGUMENTS` or the user's message. If tone isn't specified, ask: `professional` / `casual` / `promotional` / `educational`.
2. **Read platform specs.** Consult `references/platform-specs.md` for each platform's character limits, conventions, and tone presets.
3. **Draft per platform:**
   - **Facebook** — 1–2 engaging sentences + 1–2 emoji. Conversational.
   - **Instagram** — caption ≤ 2200 chars (aim for 150–400 for engagement), ends with a CTA, then 10–15 hashtags. First line must hook (IG truncates after ~125 chars in feed).
   - **YouTube** — title ≤ 100 chars (front-load keywords, curiosity gap, no clickbait); description: 2–3 sentence summary + timestamps placeholder + links section + 8–12 comma-separated tags.
   - **X/Twitter** — tweet ≤ 280 chars. One idea per tweet. Optional thread if the idea is big.
   - **LinkedIn** — professional, hook line + 3–5 short paragraphs or a bulleted list, ends with a question to drive comments. No hashtags spam (3–5 max).
   - **Gmail** — subject ≤ 60 chars (front-load the value), body: greeting + 2–3 short paragraphs + CTA + signature placeholder.
4. **Generate hashtags** (IG + YouTube) — relevant, mix of broad (#ai) and niche (#sglang). Avoid banned/shadowbanned tags.
5. **Append to the content calendar.** Run `bash scripts/init-calendar.sh` (creates the file if missing), then append a row to `templates/content-calendar.md` with date, idea summary, platforms drafted, tone.
6. **Present all 6 drafts** in one fenced block per platform so the user can copy each individually.

## Rules
- **No auto-posting.** This skill drafts only. No OAuth, no API calls to Facebook/Instagram/YouTube/Gmail. Do not attempt to post on the user's behalf. See README.
- Don't fabricate stats, quotes, or testimonials in promotional content.
- Respect platform conventions (don't put 30 hashtags on IG; don't exceed tweet length).

## References
- `references/platform-specs.md` — char limits, tone presets (authoritative).
- `templates/content-calendar.md`
- `scripts/init-calendar.sh`
