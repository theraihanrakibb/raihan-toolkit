# raihan-toolkit API (FastAPI backend)

HTTP wrapper for the 5 CodeBuddy skills. Template-based generation — no LLM dependency, works out of the box.

## Run

```bash
cd website/backend
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

- API root: http://localhost:8000
- OpenAPI docs: http://localhost:8000/docs
- Health check: http://localhost:8000/api/health

## Endpoints

| Method | Path | Body | Returns |
|---|---|---|---|
| GET | `/api/health` | — | `{status, skills}` |
| POST | `/api/audit-portfolio` | `{username, max_repos?}` | Repo scores + fix-plan per repo |
| POST | `/api/apply` | `{jd, resume}` | Cover letter + interview Qs + skills-gap + prep plan |
| POST | `/api/pr-draft` | `{diff}` | Conventional Commit + PR description + changelog |
| POST | `/api/ai-infra-helper` | `{question}` | SGLang/vLLM layout + CI behavior |
| POST | `/api/social` | `{idea, tone?}` | 6 platform drafts + hashtags |

## Notes

- `audit-portfolio` uses the unauthenticated GitHub API (60 req/hr per IP). For heavy use, set `GITHUB_TOKEN` env var and the client will use it.
- All generation is template-based. To plug in a real LLM, replace the functions in `skills.py` with calls to an OpenAI-compatible endpoint.
