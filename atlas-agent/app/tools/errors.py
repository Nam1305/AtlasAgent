"""Normalised tool errors.

The agent loop depends on a small set of error categories so it can decide
whether to retry, ask the user, or stop. Provider-specific exceptions should
never leak past this layer.
"""
from __future__ import annotations


class ToolError(Exception):
    """Base for all tool errors. Carries a stable `code` and a human message."""

    code: str = "tool_error"

    def __init__(self, message: str, *, code: str | None = None) -> None:
        super().__init__(message)
        if code is not None:
            self.code = code


class ToolInputError(ToolError):
    """The input the model produced did not match the tool's schema."""

    code = "tool_input_invalid"


class ToolNotAllowedError(ToolError):
    """The tool is not in the agent's allowlist."""

    code = "tool_not_allowed"


class ToolTimeoutError(ToolError):
    """The tool exceeded its timeout."""

    code = "tool_timeout"


class ToolExecutionError(ToolError):
    """The tool raised an unexpected exception while running."""

    code = "tool_execution_error"


class ToolNotFoundError(ToolError):
    """A tool name was requested that does not exist in the registry."""

    code = "tool_not_found"
