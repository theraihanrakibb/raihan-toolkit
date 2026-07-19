---
name: job-application
description: Accelerates job applications when the user pastes a job description (JD) or asks "tailor my resume for this job", "write a cover letter for this JD", "what interview questions should I expect", "skills gap analysis", or "prep plan for this role". Use this skill whenever the user is applying to a job and wants cover letter, resume tweaks, interview prep, or a prep plan.
---

# Job Application Accelerator

## When to Use
- User pastes a JD or shares a job URL.
- User asks for a cover letter, resume tailoring, interview prep, or skills-gap analysis.

## How to Use

1. **Gather inputs.**
   - JD: accept pasted text or a URL (fetch via `WebFetch` if URL).
   - Resume: accept pasted text or a local file path (read via `Read`).
2. **Produce five outputs** in this order:
   1. **Tailored cover letter** — 250–350 words, references the company/role, highlights 2–3 resume points that match the JD. Use `templates/cover-letter.md`.
   2. **Resume bullet tweaks** — for each existing bullet that maps to a JD requirement, suggest a sharper rewrite that front-loads the JD keyword. Don't invent experience.
   3. **Likely interview questions** — 6 technical + 4 behavioral, derived from JD responsibilities. Include a one-line "what they're really checking" hint per question.
   4. **Skills-gap analysis** — list JD requirements the resume does NOT cover; mark each as `[learnable-quickly]` / `[stretch]` / `[blocking]`.
   5. **7-day prep plan** — day-by-day: topics to study, a mock interview question to practice, one resume tweak to make.
3. **Log the application** — append a row to `templates/job-applications-log.md` with date, company, role, JD source, and status `drafted`.

## Rules
- Never invent experience, employers, or metrics. Only rephrase what the user actually has.
- If the JD asks for something the user clearly can't do, say so in the skills-gap section rather than faking it.
- Don't auto-submit applications anywhere. Output is drafts only.

## References
- `templates/cover-letter.md`
- `templates/job-applications-log.md`
