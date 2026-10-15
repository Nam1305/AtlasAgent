"""Demo 3 — token usage metadata.

The provider returns prompt / completion / total counts when you ask
for `usageMetadata`. We surface it so you can see how cost grows with
context size.
"""
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
    body = {"contents": [{"role": "user", "parts": [{"text": "Count to 10."}]}]}
    url = URL.format(model=model) + f"?key={api_key}"
    resp = httpx.post(url, json=body, timeout=30.0)
    resp.raise_for_status()
    data = resp.json()
    usage = data.get("usageMetadata", {})
    text = data["candidates"][0]["content"]["parts"][0]["text"]
    print(text)
    print("---")
    print(f"prompt={usage.get('promptTokenCount')} completion={usage.get('candidatesTokenCount')} total={usage.get('totalTokenCount')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
