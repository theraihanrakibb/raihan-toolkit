# Deploying toolkit-skills

**Single-platform deploy (Vercel only).** The whole app — React frontend **and** the
FastAPI-style backend — runs on Vercel. No card required (Vercel free tier).

- Frontend: Vite build → static `dist`.
- Backend: a Vercel Python serverless function at `website/frontend/api/index.py`
  that exposes `POST /api` with `{"action": ...}` in the body (logic in `api/skills.py`).
- The frontend calls `POST /api` (see `src/api.js`), which Vercel routes straight to
  the function. No proxy, no separate host.

## Prerequisites

- A Vercel account → https://vercel.com/signup (GitHub login works).
- Vercel CLI: `npm install -g vercel` → `vercel --version`.
- Logged in: `vercel login` (browser OAuth).

## Deploy

```bash
# from the repo root
cd website/frontend
vercel --prod --yes
```

- First run creates the project (Vite framework auto-detected from `vercel.json`;
  the `api/` dir becomes a Python serverless function).
- Output: `https://toolkit-skills-<hash>.vercel.app` (production URL).

Set a GitHub token to raise the portfolio-audit rate limit (optional, 60→5000/hr):

```bash
vercel env add GITHUB_TOKEN production
# paste a GitHub PAT with public_repo scope
```

## Verify

Open the Vercel URL → **Social Media** tab → type an idea → Generate.
Or hit the API directly:

```bash
curl -X POST https://<your-app>.vercel.app/api \
  -H 'Content-Type: application/json' \
  -d '{"action":"social","idea":"shipped a CLI tool"}'

curl -X POST https://<your-app>.vercel.app/api \
  -H 'Content-Type: application/json' \
  -d '{"action":"audit-portfolio","username":"theraihanrakibb"}'
```

## Local dev (FastAPI backend)

The same `POST /api` interface is served locally by `website/backend/main.py`, so the
frontend works unchanged with the Vite dev proxy (`/api` → `localhost:8000`):

```bash
# terminal 1
cd website/backend && pip install -r requirements.txt && uvicorn main:app --reload --port 8000
# terminal 2
cd website/frontend && npm install && npm run dev
```

## Update after a change

```bash
cd website/frontend && vercel --prod --yes
```

Push to `main` does **not** auto-deploy (CI only runs tests/lint). Re-run the command above.

## Troubleshooting

- **`audit-portfolio` 403/429:** unauthenticated GitHub rate limit (60/hr). Set `GITHUB_TOKEN`.
- **Function errors:** check Vercel → Project → Functions logs. The handler returns `{"error": ...}` on failure.
- **Build fails:** ensure `website/frontend` has `package.json` + `vercel.json`; `npm ci` runs automatically.
