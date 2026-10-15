"""Demo 5 — call the model gateway instead of the SDK directly.

This is the same request shape as Demo 1, but routed through
`app.model_gateway.complete` so we exercise the normalised path the rest
of the app uses.
"""
from __future__ import annotations

import asyncio
import os
import sys

from app.config import get_settings
from app.model_gateway import ModelGatewayError, complete
from app.schemas import ChatMessage


async def _run() -> str:
    return (
        await complete(
            [ChatMessage(role="user", content="Say hi in 5 words.")],
            settings=get_settings(),
        )
    ).content


def main() -> int:
    if not os.environ.get("GEMINI_API_KEY"):
        print("Set GEMINI_API_KEY before running.", file=sys.stderr)
        return 1
    try:
        print(asyncio.run(_run()))
    except ModelGatewayError as exc:
        print(f"gateway error: {exc.code}: {exc.message}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
