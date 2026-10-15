"""Demo 2 — system, user and assistant message roles."""
from __future__ import annotations

import os
import sys

import httpx

URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


def main() -> int:
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        print("Set GEMINI_API_KEY before running.", file=sys.stderr)
        return 1
    model = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
    body = {
        "systemInstruction": {"parts": [{"text": "You answer in one short sentence."}]},
        "contents": [{"role": "user", "parts": [{"text": "What is 2+2?"}]}],
    }
    url = URL.format(model=model) + f"?key={api_key}"
    resp = httpx.post(url, json=body, timeout=30.0)
    resp.raise_for_status()
    text = resp.json()["candidates"][0]["content"]["parts"][0]["text"]
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
