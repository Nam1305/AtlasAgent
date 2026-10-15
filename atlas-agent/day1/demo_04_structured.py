"""Demo 4 — ask for structured output and parse it.

The model is asked to return JSON; the code uses a Pydantic model to
parse and validate. If the model returns malformed JSON, parsing fails
loudly here rather than silently in production.
"""
from __future__ import annotations

import json
import os
import sys

import httpx
from pydantic import BaseModel

URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


class Answer(BaseModel):
    summary: str
    confidence: float


def main() -> int:
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        print("Set GEMINI_API_KEY before running.", file=sys.stderr)
        return 1
    model = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
    body = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": (
                            "Reply as JSON: {\"summary\": <one sentence>, "
                            "\"confidence\": <0..1>}. Topic: 2+2."
                        )
                    }
                ],
            }
        ],
        "generationConfig": {"responseMimeType": "application/json"},
    }
    url = URL.format(model=model) + f"?key={api_key}"
    resp = httpx.post(url, json=body, timeout=30.0)
    resp.raise_for_status()
    raw = resp.json()["candidates"][0]["content"]["parts"][0]["text"]
    parsed = Answer.model_validate(json.loads(raw))
    print(parsed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
