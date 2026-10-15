"""Tool executor with schema validation, allowlist enforcement, and timeout.

A model can request any tool name with any arguments. The executor is the
only place that decides:
  - whether the tool exists,
  - whether the agent is allowed to use it,
  - whether the arguments are valid,
  - and how long we will wait before giving up.
"""
from __future__ import annotations

import asyncio
import logging
import time
from dataclasses import dataclass
from typing import Any

from .base import Tool
from .errors import (
    ToolError,
    ToolExecutionError,
    ToolInputError,
    ToolNotAllowedError,
    ToolNotFoundError,
    ToolTimeoutError,
)
from .registry import ToolRegistry

logger = logging.getLogger(__name__)


@dataclass
class ToolCall:
    name: str
    arguments: dict[str, Any]


@dataclass
class ToolResult:
    name: str
    success: bool
    output: Any = None
    error_code: str | None = None
    error_message: str | None = None
    duration_ms: float = 0.0


class ToolExecutor:
    """Run tool calls safely with allowlist, validation, and timeout."""

    def __init__(self, registry: ToolRegistry, allowlist: set[str] | None = None) -> None:
        self.registry = registry
        self.allowlist = registry.allowlist(allowlist)

    async def execute(self, call: ToolCall) -> ToolResult:
        start = time.perf_counter()

        if call.name not in self.allowlist:
            logger.warning("tool_not_allowed name=%s", call.name)
            return ToolResult(
                name=call.name,
                success=False,
                error_code="tool_not_allowed",
                error_message=f"Tool {call.name!r} is not in the agent's allowlist",
            )
        if call.name not in self.registry:
            return ToolResult(
                name=call.name,
                success=False,
                error_code="tool_not_found",
                error_message=f"Tool {call.name!r} is not registered",
            )

        tool: Tool = self.registry.get(call.name)
        try:
            payload = tool.validate_input(call.arguments)
        except ToolInputError as exc:
            return ToolResult(
                name=call.name,
                success=False,
                error_code=exc.code,
                error_message=str(exc),
            )
        except Exception as exc:  # pydantic ValidationError, etc.
            return ToolResult(
                name=call.name,
                success=False,
                error_code="tool_input_invalid",
                error_message=str(exc),
            )

        try:
            output = await asyncio.wait_for(tool.run(payload), timeout=tool.timeout_seconds)
        except asyncio.TimeoutError as exc:
            elapsed = (time.perf_counter() - start) * 1000
            logger.warning("tool_timeout name=%s duration_ms=%.1f", call.name, elapsed)
            return ToolResult(
                name=call.name,
                success=False,
                error_code="tool_timeout",
                error_message=f"Tool {call.name!r} exceeded {tool.timeout_seconds}s",
            )
        except ToolError as exc:
            elapsed = (time.perf_counter() - start) * 1000
            logger.warning(
                "tool_error name=%s code=%s duration_ms=%.1f",
                call.name,
                exc.code,
                elapsed,
            )
            return ToolResult(
                name=call.name,
                success=False,
                error_code=exc.code,
                error_message=str(exc),
            )
        except Exception as exc:  # pragma: no cover - defensive
            elapsed = (time.perf_counter() - start) * 1000
            logger.exception("tool_unexpected name=%s", call.name)
            return ToolResult(
                name=call.name,
                success=False,
                error_code="tool_execution_error",
                error_message=str(exc),
            )

        elapsed = (time.perf_counter() - start) * 1000
        logger.info(
            "tool_ok name=%s duration_ms=%.1f", call.name, elapsed
        )
        return ToolResult(name=call.name, success=True, output=output, duration_ms=elapsed)


# Re-export error classes so callers can `from app.tools.executor import ...`
__all__ = [
    "ToolCall",
    "ToolResult",
    "ToolExecutor",
    "ToolError",
    "ToolExecutionError",
    "ToolInputError",
    "ToolNotAllowedError",
    "ToolNotFoundError",
    "ToolTimeoutError",
]
