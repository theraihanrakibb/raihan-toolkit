# raihan-toolkit

![CI](https://github.com/theraihanrakibb/raihan-toolkit/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![Node](https://img.shields.io/badge/node-20-green.svg)

A CodeBuddy Code plugin bundle: 5 skills + 5 slash commands + 1 git-commit guard. Tailored for job-hunt, AI-infra, public-repos, and content creation workflows. Ships with a full-stack web UI (FastAPI + React) that wraps every skill as an HTTP endpoint.

## Skills & Commands

| Skill | Slash command | What it does |
|---|---|---|
| Portfolio Audit | `/raihan-toolkit:audit-portfolio` | Score your public repos against a 10/10 quality bar; output a fix-plan; optionally auto-fix simple gaps. |
| Job Application | `/raihan-toolkit:apply <jd>` | Tailored cover letter, resume tweaks, likely interview Qs, skills-gap analysis, 7-day prep plan. |
| PR Draft | `/raihan-toolkit:pr-draft` | Conventional Commit message + PR description + changelog entry from staged diff. |
| AI-Infra Helper | `/raihan-toolkit:ai-infra-helper` | Navigate SGLang/vLLM-style repos; reminds fork-PR CI behavior; drafts PRs. |
| Social Media | `/raihan-toolkit:social <idea>` | One idea → 6 platform drafts (FB/IG/YouTube/X/LinkedIn/Gmail) + content calendar. Drafting only — no auto-posting. |

## Hard Rules (enforced)

1. **No AI-generation footers.** Never emit `Generated with CodeBuddy Code`, `Co-Authored-By: Claude`, or any AI trailer in commits, PRs, cover letters, or social posts.
   - Enforced in each `SKILL.md` AND in `hooks/validate-commit.sh` (denies `git commit` calls whose message contains AI-footer patterns).
2. **Social media is drafting-only.** No actual posting. Auto-posting would require per-platform OAuth (Facebook Graph API, Instagram Graph API, YouTube Data API, Gmail API) — out of scope for v1.

## Install

### Option A — Dev/test (quick)
```bash
cc --plugin-dir e:\CodingWorkplace\raihan-toolkit
```
Hooks load at session start. Run `/hooks` to verify.

### Option B — Persistent install
```bash
bash scripts/sync-to-cache.sh
```
Then add to `~/.codebuddy/installed_plugins.json`:
```json
"raihan-toolkit@local": [{
  "scope": "user",
  "installPath": "C:\\Users\\Raihan\\.codebuddy\\plugins\\cache\\local\\raihan-toolkit\\1.0.0",
  "version": "1.0.0",
  "installedAt": "<ISO date>",
  "lastUpdated": "<ISO date>"
}]
```
And in `~/.codebuddy/settings.json` → `enabledPlugins`:
```json
"raihan-toolkit@local": true
```
Restart `cc` to confirm auto-load.

### Editing workflow
Edit files in `e:\CodingWorkplace\raihan-toolkit\`, then re-run `scripts/sync-to-cache.sh` to push to the persistent cache. Restart `cc` for hook changes.

## File layout

```
raihan-toolkit/
├── .codebuddy-plugin/plugin.json
├── commands/          # 5 slash commands
├── skills/            # 5 SKILL.md (auto-activating)
├── hooks/             # PreToolUse Bash guard (no AI footers)
├── references/        # quality-bar, platform-specs, ai-infra-repos, no-ai-footer-rule
├── templates/         # cover-letter, pr-description, readme-scaffold, logs, calendar
└── scripts/           # git-diff-staged, audit-repo, init-calendar, sync-to-cache
```

## License
MIT.

## Website (FastAPI + React)

A full-stack web UI for the 5 skills lives in [`website/`](./website). See [`website/README.md`](./website/README.md) for run instructions.

```bash
# backend
cd website/backend && pip install -r requirements.txt && uvicorn main:app --reload --port 8000
# frontend (separate terminal)
cd website/frontend && npm install && npm run dev
```

App at http://localhost:5173, API at http://localhost:8000/docs.

## Docker (one-command full stack)

```bash
cd website
docker compose up --build
```

App at http://localhost:8080, API at http://localhost:8000. Backend runs as a non-root user on `python:3.11-slim`; frontend is a multi-stage `node:20-alpine` → `nginx:alpine` build.

## CI / Tests / Quality

- **CI:** `.github/workflows/ci.yml` — 3 jobs (backend `ruff`+`pytest`, frontend `npm run build`, plugin `shellcheck`+`bash -n`+JSON validate). Runs on push and PR to `main`.
- **Backend tests:** `website/backend/tests/test_skills.py` — 17 tests covering all 5 skills. Run with `pytest`.
- **Lint:** `ruff check .` (config in `website/backend/pyproject.toml`).
- **Type hints + docstrings** throughout `skills.py` and `main.py`.

## Deploy

Frontend → Vercel · Backend → Fly.io. Full step-by-step in [`website/DEPLOY.md`](./website/DEPLOY.md).

```bash
# Backend → Fly.io
cd website/backend && fly launch && fly secrets set ALLOWED_ORIGINS=<vercel-url> && fly deploy

# Frontend → Vercel
cd website/frontend && vercel env add FLY_BACKEND_URL production && vercel --prod
```

Vercel proxies `/api/*` to the Fly backend (`website/frontend/vercel.json`), so the frontend code stays unchanged. CORS on the backend is configured via the `ALLOWED_ORIGINS` env var.
