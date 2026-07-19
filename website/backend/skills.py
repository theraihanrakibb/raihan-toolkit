"""Skill logic for the raihan-toolkit web backend.

Template-based generation (no LLM dependency) so the site works out of the box.
Each function mirrors the corresponding CodeBuddy skill's behavior.
"""
from __future__ import annotations

import os
import re
from typing import Any

import httpx

GITHUB_API = "https://api.github.com"

# Optional: set GITHUB_TOKEN to raise GitHub API rate limits (60 → 5000 req/hr).
_GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
_GITHUB_HEADERS = {"Accept": "application/vnd.github+json"}
if _GITHUB_TOKEN:
    _GITHUB_HEADERS["Authorization"] = f"Bearer {_GITHUB_TOKEN}"


# ---------------------------------------------------------------------------
# 1. Portfolio audit
# ---------------------------------------------------------------------------
async def audit_portfolio(username: str, max_repos: int = 5) -> dict[str, Any]:
    """Score a GitHub user's top repos against a 10-point quality bar."""
    async with httpx.AsyncClient(timeout=20, headers=_GITHUB_HEADERS) as client:
        r = await client.get(f"{GITHUB_API}/users/{username}/repos", params={"per_page": 100, "sort": "pushed"})
        if r.status_code != 200:
            return {"error": f"GitHub API {r.status_code}: {r.text[:200]}"}
        repos = r.json()

    # Pick top N by stargazers_count
    repos = sorted(repos, key=lambda x: x.get("stargazers_count", 0), reverse=True)[:max_repos]

    scored = []
    async with httpx.AsyncClient(timeout=20, headers=_GITHUB_HEADERS) as client:
        for repo in repos:
            full_name = repo["full_name"]
            readme_ok = (await client.get(f"{GITHUB_API}/repos/{full_name}/readme")).status_code == 200
            license_ok = bool(repo.get("license"))
            topics = repo.get("topics", []) or []
            description = repo.get("description") or ""
            has_pages = bool(repo.get("has_pages"))
            has_issues = bool(repo.get("has_issues"))
            archived = bool(repo.get("archived"))

            # Score 0..10
            score = 0
            score += 1 if readme_ok else 0
            score += 1 if license_ok else 0
            score += 1 if topics else 0
            score += 1 if description else 0
            score += 1 if has_pages else 0
            score += 1 if has_issues else 0
            score += 1 if repo.get("forks", 0) > 0 else 0
            score += 1 if repo.get("stargazers_count", 0) > 0 else 0
            score += 1 if not archived else 0
            score += 1 if repo.get("homepage") else 0

            scored.append({
                "name": full_name,
                "stars": repo.get("stargazers_count", 0),
                "forks": repo.get("forks", 0),
                "description": description,
                "topics": topics,
                "license": repo.get("license", {}).get("spdx_id") if repo.get("license") else None,
                "has_readme": readme_ok,
                "has_pages": has_pages,
                "score": score,
                "max_score": 10,
                "fix_plan": _fix_plan(readme_ok, license_ok, topics, description, has_pages),
            })

    return {"username": username, "repos": scored}


def _fix_plan(readme_ok: bool, license_ok: bool, topics: list, description: str, pages: bool) -> list[str]:
    plan = []
    if not readme_ok:
        plan.append("[easy] Add a README.md (use templates/readme-scaffold.md)")
    if not license_ok:
        plan.append("[easy] Add a LICENSE file (MIT recommended)")
    if not topics:
        plan.append("[easy] Add 3–5 topics via gh repo edit --add-topic")
    if not description:
        plan.append("[easy] Set a repo description: gh repo edit --description '...'")
    if not pages:
        plan.append("[medium] Enable GitHub Pages for a project site")
    if not plan:
        plan.append("[ok] All easy items satisfied — focus on tests + CI next.")
    return plan


# ---------------------------------------------------------------------------
# 2. Job application
# ---------------------------------------------------------------------------
def apply(jd: str, resume: str) -> dict[str, Any]:
    """Template-based cover letter, interview Qs, skills-gap, prep plan."""
    jd_keywords = _extract_keywords(jd)
    resume_keywords = _extract_keywords(resume)

    matched = [k for k in jd_keywords if k.lower() in {r.lower() for r in resume_keywords}]
    missing = [k for k in jd_keywords if k.lower() not in {r.lower() for r in resume_keywords}][:8]

    company = _extract_company(jd) or "your company"
    role = _extract_role(jd) or "the role"

    cover_letter = f"""Dear Hiring Team at {company},

I'm writing to apply for {role}. The job description emphasizes {', '.join(jd_keywords[:3])}, which aligns directly with my background.

In my recent work, I have focused on {', '.join(matched[:3]) or 'building production systems'}, with attention to reliability and measurable impact. I'm confident I can contribute to {company}'s goals from day one.

I'm especially drawn to {company} because of its engineering culture and the problems the team is solving. I'd welcome the chance to discuss how my experience maps to your needs.

Thank you for your time and consideration.

Best regards,
[Your Name]
"""

    interview_questions = [
        *[f"Walk me through a project where you used {k}." for k in matched[:3]],
        "Tell me about a time you debugged a hard issue under pressure.",
        "How do you approach writing tests for a new feature?",
        "Describe a system you designed end-to-end.",
        "What's a trade-off you made recently, and why?",
        *[f"How would you ramp up on {k} if you haven't used it?" for k in missing[:3]],
    ]

    skills_gap = [
        {"skill": k, "status": "learnable-quickly" if len(k) < 12 else "stretch"}
        for k in missing
    ]

    prep_plan = [
        "Day 1: Re-read the JD; map each requirement to a resume bullet or a project you'll lean on.",
        "Day 2: Practice a 90-second intro (who you are, what you've built, why this role).",
        "Day 3: Drill 3 technical questions on the matched skills.",
        "Day 4: Prepare 2 stories using STAR (one challenge, one collaboration).",
        "Day 5: Study one missing skill — enough to talk about it for 2 minutes.",
        "Day 6: Mock interview (with a friend or in front of a camera).",
        "Day 7: Rest, prepare questions for them, confirm logistics.",
    ]

    return {
        "company": company,
        "role": role,
        "matched_keywords": matched,
        "missing_keywords": missing,
        "cover_letter": cover_letter,
        "interview_questions": interview_questions,
        "skills_gap": skills_gap,
        "prep_plan": prep_plan,
    }


def _extract_keywords(text: str) -> list[str]:
    # Crude: pick capitalized words and known tech tokens.
    stopwords = {"the", "and", "for", "with", "you", "our", "will", "this", "that", "from", "have", "are"}
    tokens = re.findall(r"[A-Za-z][A-Za-z0-9+#.]{2,}", text)
    seen, out = set(), []
    for t in tokens:
        low = t.lower()
        if low in stopwords:
            continue
        if low in seen:
            continue
        seen.add(low)
        out.append(t)
    return out[:12]


def _extract_company(jd: str) -> str | None:
    # Match "at <Capitalized Words>" or "join <Capitalized Words>" — each word must start uppercase.
    m = re.search(r"\b(?:at|join)\s+([A-Z][A-Za-z0-9&]+(?:\s+[A-Z][A-Za-z0-9&]+)*)", jd)
    return m.group(1).strip() if m else None


def _extract_role(jd: str) -> str | None:
    m = re.search(r"\b(Engineer|Developer|Intern|Lead|Architect|Scientist)[A-Za-z ]{0,30}", jd)
    return m.group(0).strip() if m else None


# ---------------------------------------------------------------------------
# 3. PR draft
# ---------------------------------------------------------------------------
def pr_draft(diff: str) -> dict[str, Any]:
    """Generate a Conventional Commit message + PR description from a diff."""
    files = re.findall(r"^\+\+\+ b/(.+)$", diff, flags=re.MULTILINE)
    additions = diff.count("\n+")
    deletions = diff.count("\n-")

    # Guess type from file paths
    joined = " ".join(files).lower()
    if any(k in joined for k in ["readme", "doc", "license", ".md"]):
        ctype = "docs"
    elif any(k in joined for k in ["test", "spec"]):
        ctype = "test"
    elif any(k in joined for k in [".yml", ".yaml", "github/workflows", "dockerfile"]):
        ctype = "ci"
    elif any(k in joined for k in ["refactor", "rename"]):
        ctype = "refactor"
    else:
        ctype = "feat"

    scope = files[0].split("/")[0] if files else "core"
    subject = f"update {scope}" if files else "update project"

    commit_message = f"{ctype}({scope}): {subject}\n\nUpdates {len(files)} file(s). +{additions} -{deletions}.\n\nNo AI-generation footer."

    pr_description = f"""## Summary
Updates {len(files)} file(s) across `{scope}`.

## Changes
""" + "\n".join(f"- `{f}`" for f in files) + f"""

## Why
[Explain the motivation here.]

## Testing
- [ ] `pre-commit run --all-files` is green
- [ ] Targeted test passes locally

## Stats
+{additions} additions / -{deletions} deletions across {len(files)} file(s).
"""

    changelog = f"- [{ctype}] {scope}: {subject}"

    return {
        "commit_message": commit_message,
        "pr_description": pr_description,
        "changelog_entry": changelog,
        "files": files,
        "additions": additions,
        "deletions": deletions,
    }


# ---------------------------------------------------------------------------
# 4. AI-infra helper
# ---------------------------------------------------------------------------
def ai_infra_helper(question: str) -> dict[str, Any]:
    """Return guidance for navigating SGLang/vLLM-style repos."""
    q = question.lower()
    if "sglang" in q or "model" in q and "add" in q:
        return {
            "repo": "sglang",
            "layout": {
                "models": "python/sglang/srt/models/<arch>.py",
                "scheduler": "python/sglang/srt/managers/scheduler.py",
                "server": "python/sglang/srt/entrypoints/",
                "frontend": "python/sglang/lang/",
                "tests": "test/srt/",
            },
            "commands": [
                "pre-commit install && pre-commit run --all-files",
                "pytest test/srt/test_<area>.py -k <name> -x",
            ],
            "ci_behavior": "Fork PRs fail pr-gate / pr-test-* by design (need repo secrets). Only `lint` actually gates your code. Make lint green; don't chase pr-test-*.",
            "answer": f"For '{question}': see SGLang layout above. Likely file: python/sglang/srt/models/<arch>.py",
        }
    if "vllm" in q:
        return {
            "repo": "vllm",
            "layout": {
                "models": "vllm/model_executor/models/",
                "engine": "vllm/engine/",
                "entrypoints": "vllm/entrypoints/",
                "tests": "tests/",
            },
            "commands": ["./.format.sh", "pytest tests/<area>/test_x.py -k <name> -x"],
            "ci_behavior": "Similar to SGLang: fork PRs can't access GPU CI. Make ruff + black green.",
            "answer": f"For '{question}': see vLLM layout above.",
        }
    return {
        "repo": "generic",
        "answer": f"Question '{question}' doesn't match SGLang or vLLM. Try asking about 'sglang', 'vllm', 'where to add a model', or 'what tests to run'.",
    }


# ---------------------------------------------------------------------------
# 5. Social media
# ---------------------------------------------------------------------------
def social(idea: str, tone: str = "professional") -> dict[str, Any]:
    """Draft content for 6 platforms from one idea."""
    hook = idea[:120]

    facebook = f"{hook}\n\nWhat do you think? Drop a comment below. 👇"

    instagram_caption = (
        f"{hook}\n\n"
        f"Save this for later 🔖 and share with someone who needs to see it.\n\n"
        f"#ai #buildinpublic #developer #tech #programming"
    )

    youtube_title = idea[:90]
    youtube_description = (
        f"{hook}\n\n"
        f"In this video we break down the idea, walk through the implementation, and "
        f"show concrete results.\n\n"
        f"0:00 Intro\n0:30 Context\n1:15 Demo\n3:00 Takeaways\n\n"
        f"Links: [placeholder]\n\n"
        f"Tags: ai, programming, buildinpublic, developer, tech, tutorial, howto"
    )

    tweet = idea[:277] + ("…" if len(idea) > 277 else "")

    linkedin = (
        f"{hook}\n\n"
        f"I've been thinking about this, and here's my take:\n\n"
        f"- It's easy to overlook the small things.\n"
        f"- The compounding effect is real.\n"
        f"- Sharing what you learn helps everyone.\n\n"
        f"What's your experience with this? Curious to hear from the network."
    )

    gmail_subject = idea[:55]
    gmail_body = (
        f"Hi [Name],\n\n"
        f"{hook}\n\n"
        f"I thought this might be relevant given what you're working on. "
        f"Happy to share more detail if useful.\n\n"
        f"Best,\n[Your Name]"
    )

    hashtags = ["#ai", "#buildinpublic", "#developer", "#tech", "#programming", "#coding"]
    youtube_tags = ["ai", "programming", "buildinpublic", "developer", "tech", "tutorial", "howto"]

    return {
        "idea": idea,
        "tone": tone,
        "platforms": {
            "facebook": facebook,
            "instagram": instagram_caption,
            "youtube_title": youtube_title,
            "youtube_description": youtube_description,
            "youtube_tags": youtube_tags,
            "twitter": tweet,
            "linkedin": linkedin,
            "gmail_subject": gmail_subject,
            "gmail_body": gmail_body,
        },
        "hashtags": hashtags,
    }
