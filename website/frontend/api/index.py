"""Vercel Python serverless entrypoint for Toolkit Skills.

Exposes an ASGI `app` (required by the current Vercel Python runtime) that routes
POST /api (with {"action": ...} in the body) to the skill logic in skills.py.
Pure standard library - no pip dependencies.
"""

import json
import os
import sys

# Ensure the function directory is importable (Vercel's uv builder does not
# always add it to sys.path at runtime).
sys.path.insert(0, os.path.dirname(__file__))

from skills import dispatch


async def app(scope, receive, send):
    assert scope["type"] == "http"

    # Read the full request body.
    body = b""
    while True:
        message = await receive()
        body += message.get("body", b"")
        if not message.get("more_body", False):
            break

    try:
        data = json.loads(body.decode("utf-8")) if body else {}
    except Exception:  # noqa: BLE001
        data = {}
    if not isinstance(data, dict):
        data = {}

    try:
        result = dispatch(data.get("action"), data)
        status, payload = 200, json.dumps(result).encode("utf-8")
    except Exception as e:  # noqa: BLE001
        status, payload = 500, json.dumps({"error": str(e)}).encode("utf-8")

    await send({
        "type": "http.response.start",
        "status": status,
        "headers": [(b"content-type", b"application/json")],
    })
    await send({"type": "http.response.body", "body": payload})
