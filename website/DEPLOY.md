# Deploying raihan-toolkit

Two deployments:
- **Backend** (FastAPI) → **Fly.io** → `https://raihan-toolkit-backend.fly.dev`
- **Frontend** (React + Vite) → **Vercel** → `https://raihan-toolkit.<your-handle>.vercel.app`

Vercel proxies `/api/*` to the Fly backend (configured in `website/frontend/vercel.json`), so the frontend code stays unchanged.

## Prerequisites

- A Fly.io account → https://fly.io/app/sign-up
- A Vercel account → https://vercel.com/signup (GitHub login works)
- Both CLIs installed (see steps below)

---

## Step 1 — Deploy backend to Fly.io

### 1.1 Install `flyctl`

**Windows (PowerShell):**
```powershell
iwr https://get.fly.dev | iex
```
**macOS / Linux:**
```bash
curl -L https://fly.io/install.sh | sh
```
Verify: `fly version`

### 1.2 Log in
```bash
fly auth login
```
Browser opens → complete sign-in.

### 1.3 Launch the app (uses `website/backend/fly.toml`)
```bash
cd e:/CodingWorkplace/raihan-toolkit/website/backend
fly launch --no-deploy
```
- When prompted "Would you like to copy the configuration to the new app?", answer **Yes** (uses the committed `fly.toml`).
- If the app name `raihan-toolkit-backend` is taken, Fly will suggest an alternative — accept it and **update `fly.toml`'s `app` field** to match, then commit.
- Pick the same region as `fly.toml` (`nrt` — Tokyo) or choose a closer one.

### 1.4 Set secrets
```bash
fly secrets set ALLOWED_ORIGINS="https://raihan-toolkit.vercel.app"
fly secrets set GITHUB_TOKEN="<your-github-pat-with-public-repo-scope>"   # optional, raises GitHub API rate limit
```
Note: `ALLOWED_ORIGINS` will be finalized in step 2.4 once you know the Vercel URL. For now, set it to your best guess; you can re-run `fly secrets set ALLOWED_ORIGINS=...` later.

### 1.5 Deploy
```bash
fly deploy
```
First deploy takes ~2–3 minutes. When it finishes, you'll get the URL:
```
https://raihan-toolkit-backend.fly.dev
```

### 1.6 Verify
```bash
curl https://raihan-toolkit-backend.fly.dev/api/health
# → {"status":"ok","skills":[...]}
```

---

## Step 2 — Deploy frontend to Vercel

### 2.1 Install the Vercel CLI
```bash
npm install -g vercel
```
Verify: `vercel --version`

### 2.2 Log in
```bash
vercel login
```
Browser opens → complete sign-in.

### 2.3 Set the backend URL env var
From the project root:
```bash
cd website/frontend
vercel env add FLY_BACKEND_URL production
# Paste: https://raihan-toolkit-backend.fly.dev
```
(Or set it via the Vercel dashboard → Project → Settings → Environment Variables.)

### 2.4 Deploy
```bash
vercel --prod
```
- First run links the project; accept defaults (Vite framework auto-detected from `vercel.json`).
- Output: `https://raihan-toolkit.<hash>.vercel.app` (production URL).

### 2.5 Finalize CORS on the backend
Once you have the Vercel URL, re-set the backend's allowed origins:
```bash
cd website/backend
fly secrets set ALLOWED_ORIGINS="https://raihan-toolkit.<hash>.vercel.app"
```
(For multiple origins, comma-separate: `https://a.vercel.app,https://b.vercel.app`. For a public demo with no credentials, you can also set `ALLOWED_ORIGINS=*`.)

### 2.6 Verify
Open the Vercel URL → the Social Media tab → type an idea → "Draft for all 6 platforms". You should get drafts back, proxied through to the Fly backend.

---

## Alternative: connect via GitHub (no CLI)

If you'd rather not use the CLIs:

- **Vercel:** Dashboard → New Project → Import `theraihanrakibb/raihan-toolkit` → set Root Directory to `website/frontend` → add `FLY_BACKEND_URL` env var → Deploy.
- **Fly.io:** Dashboard → Launch → connect repo → set Dockerfile path to `website/backend/Dockerfile` → set `ALLOWED_ORIGINS` + `GITHUB_TOKEN` secrets → Deploy.

---

## Update after a code change

```bash
# Backend
cd website/backend && fly deploy

# Frontend
cd website/frontend && vercel --prod
```

Or push to GitHub `main` and re-run the manual deploy commands. (CI on GitHub Actions does NOT auto-deploy — add a deploy step to `.github/workflows/ci.yml` if you want CD.)

---

## Troubleshooting

- **CORS error in browser console:** the Vercel URL isn't in `ALLOWED_ORIGINS`. Re-run `fly secrets set ALLOWED_ORIGINS=<your-vercel-url>` and wait ~30s.
- **`audit-portfolio` returns a 403/429:** you hit GitHub's unauthenticated rate limit (60/hr). Set `GITHUB_TOKEN`.
- **Vercel rewrite not working:** confirm `FLY_BACKEND_URL` env var is set in the **Production** environment (not just Preview).
- **Fly app name taken:** pick a different name, update `fly.toml`'s `app` field, commit, re-run `fly launch`.
