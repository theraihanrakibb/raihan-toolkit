"""Tests for the raihan-toolkit skill functions."""
from unittest.mock import AsyncMock, patch

import pytest

from skills import (
    _extract_company,
    _extract_keywords,
    _extract_role,
    _fix_plan,
    ai_infra_helper,
    apply,
    audit_portfolio,
    pr_draft,
    social,
)


# ---------------------------------------------------------------------------
# apply
# ---------------------------------------------------------------------------
def test_apply_returns_all_fields():
    out = apply(
        jd="We're hiring a Senior Engineer at Acme Corp to work on Python and CUDA.",
        resume="I have 5 years of Python experience and worked on CUDA kernels.",
    )
    for key in ("cover_letter", "interview_questions", "skills_gap", "prep_plan", "matched_keywords", "missing_keywords"):
        assert key in out, f"missing key: {key}"
    assert "Acme Corp" in out["company"]
    assert len(out["prep_plan"]) == 7


def test_extract_keywords_returns_tokens():
    kws = _extract_keywords("We need Python, CUDA, and FastAPI skills.")
    assert "Python" in kws
    assert "CUDA" in kws


def test_extract_company_finds_at_pattern():
    assert _extract_company("Join us at Acme Corp today") == "Acme Corp"
    assert _extract_company("no company mentioned here") is None


def test_extract_role_finds_engineer():
    assert _extract_role("Software Engineer II on the infra team") is not None


# ---------------------------------------------------------------------------
# pr_draft
# ---------------------------------------------------------------------------
def test_pr_draft_detects_docs_type():
    diff = "diff --git a/README.md b/README.md\n+++ b/README.md\n+new line"
    out = pr_draft(diff)
    assert out["commit_message"].startswith("docs(")
    assert "README.md" in out["files"]


def test_pr_draft_detects_ci_type():
    diff = "diff --git a/.github/workflows/ci.yml b/.github/workflows/ci.yml\n+++ b/.github/workflows/ci.yml\n+on: push"
    out = pr_draft(diff)
    assert out["commit_message"].startswith("ci(")


def test_pr_draft_defaults_to_feat():
    diff = "diff --git a/src/app.py b/src/app.py\n+++ b/src/app.py\n+def foo(): pass"
    out = pr_draft(diff)
    assert out["commit_message"].startswith("feat(")
    assert out["additions"] >= 1
    assert out["deletions"] >= 0
    assert "No AI-generation footer" in out["commit_message"]


def test_pr_draft_empty_diff():
    out = pr_draft("")
    assert out["commit_message"].startswith("feat")
    assert out["files"] == []


# ---------------------------------------------------------------------------
# social
# ---------------------------------------------------------------------------
def test_social_returns_all_platforms():
    out = social("I shipped a new feature", tone="professional")
    platforms = out["platforms"]
    for key in ("facebook", "instagram", "youtube_title", "youtube_description",
                "youtube_tags", "twitter", "linkedin", "gmail_subject", "gmail_body"):
        assert key in platforms, f"missing platform: {key}"
    assert len(out["hashtags"]) > 0


def test_social_tweet_under_280():
    out = social("x" * 400, tone="casual")
    assert len(out["platforms"]["twitter"]) <= 280


def test_social_youtube_title_under_100():
    out = social("y" * 200, tone="promotional")
    assert len(out["platforms"]["youtube_title"]) <= 100


# ---------------------------------------------------------------------------
# ai_infra_helper
# ---------------------------------------------------------------------------
def test_ai_infra_sglang_question():
    out = ai_infra_helper("where do I add a model in sglang?")
    assert out["repo"] == "sglang"
    assert "models" in out["layout"]
    assert "lint" in out["ci_behavior"]


def test_ai_infra_vllm_question():
    out = ai_infra_helper("how is vllm structured?")
    assert out["repo"] == "vllm"
    assert "models" in out["layout"]


def test_ai_infra_generic_question():
    out = ai_infra_helper("what's the weather?")
    assert out["repo"] == "generic"


# ---------------------------------------------------------------------------
# audit_portfolio helpers
# ---------------------------------------------------------------------------
def test_fix_plan_lists_easy_items_when_everything_missing():
    plan = _fix_plan(readme_ok=False, license_ok=False, topics=[], description="", pages=False)
    assert any("README" in p for p in plan)
    assert any("LICENSE" in p for p in plan)
    assert any("topics" in p for p in plan)


def test_fix_plan_ok_when_everything_present():
    plan = _fix_plan(readme_ok=True, license_ok=True, topics=["ai"], description="ok", pages=True)
    assert any("[ok]" in p for p in plan)


@pytest.mark.asyncio
async def test_audit_portfolio_handles_api_error():
    """When GitHub returns a non-200, audit_portfolio returns an error dict, not an exception."""
    fake_response = AsyncMock()
    fake_response.status_code = 404
    fake_response.json.return_value = []
    fake_response.text = "not found"

    fake_client = AsyncMock()
    fake_client.__aenter__.return_value = fake_client
    fake_client.get.return_value = fake_response

    with patch("skills.httpx.AsyncClient", return_value=fake_client):
        out = await audit_portfolio("nonexistent-user-xyz-12345")
    assert "error" in out
    assert "404" in out["error"]
