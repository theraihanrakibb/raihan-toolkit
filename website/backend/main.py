"""FastAPI app exposing the 5 raihan-toolkit skills as HTTP endpoints.

Run: uvicorn main:app --reload --port 8000
Docs: http://localhost:8000/docs
"""
from __future__ import annotations

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from skills import ai_infra_helper, apply, audit_portfolio, pr_draft, social

app = FastAPI(
    title="raihan-toolkit API",
    description="HTTP wrapper for the 5 CodeBuddy skills: audit-portfolio, apply, pr-draft, ai-infra-helper, social.",
    version="1.0.0",
)

# Allow origins from env var (comma-separated). Defaults to local dev origins.
# In production set ALLOWED_ORIGINS=https://your-app.vercel.app (or * for a public demo).
_DEFAULT_ORIGINS = "http://localhost:5173,http://127.0.0.1:5173,http://localhost:8000"
_allowed = [o.strip() for o in os.getenv("ALLOWED_ORIGINS", _DEFAULT_ORIGINS).split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AuditRequest(BaseModel):
    username: str
    max_repos: int = 5


class ApplyRequest(BaseModel):
    jd: str
    resume: str


class PrDraftRequest(BaseModel):
    diff: str


class AiInfraRequest(BaseModel):
    question: str


class SocialRequest(BaseModel):
    idea: str
    tone: str = "professional"


@app.get("/api/health")
def health():
    return {"status": "ok", "skills": ["audit-portfolio", "apply", "pr-draft", "ai-infra-helper", "social"]}


@app.post("/api/audit-portfolio")
async def audit_portfolio_endpoint(req: AuditRequest):
    """Score a GitHub user's top repos against the 10/10 quality bar."""
    return await audit_portfolio(req.username, req.max_repos)


@app.post("/api/apply")
def apply_endpoint(req: ApplyRequest):
    """Tailor a cover letter + interview Qs + skills-gap + prep plan from a JD."""
    return apply(req.jd, req.resume)


@app.post("/api/pr-draft")
def pr_draft_endpoint(req: PrDraftRequest):
    """Generate a Conventional Commit message + PR description from a git diff."""
    return pr_draft(req.diff)


@app.post("/api/ai-infra-helper")
def ai_infra_endpoint(req: AiInfraRequest):
    """Return navigation guidance for SGLang/vLLM-style repos."""
    return ai_infra_helper(req.question)


@app.post("/api/social")
def social_endpoint(req: SocialRequest):
    """Draft content for FB/IG/YouTube/X/LinkedIn/Gmail from one idea."""
    return social(req.idea, req.tone)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
