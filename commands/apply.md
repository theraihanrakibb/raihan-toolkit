---
description: Tailor a cover letter, resume tweaks, interview questions, skills-gap analysis, and 7-day prep plan from a job description.
argument-hint: <paste-JD-or-job-URL>
allowed-tools: ["Read", "Write", "Edit", "Bash", "WebFetch", "AskUserQuestion", "Skill"]
---

# /raihan-toolkit:apply

Activate the **job-application** skill for the JD provided.

**Input:** `$ARGUMENTS` is either a pasted JD or a job URL. If empty, ask the user to paste the JD or give a URL.

## Workflow

1. If `$ARGUMENTS` looks like a URL, fetch the JD via `WebFetch`. Otherwise treat it as pasted text.
2. Ask the user for their resume: paste text, or give a local file path. Read it via `Read` if a path.
3. Produce the five outputs in order (cover letter → resume tweaks → interview Qs → skills-gap → 7-day prep plan). Use `templates/cover-letter.md`.
4. Append a row to `templates/job-applications-log.md` (create if missing): date | company | role | JD source | status=`drafted`.
5. Present everything in one structured response.

**Rules:** Do not invent experience. Do not auto-submit anywhere.
