"""Tool registry and allowlist.

The registry is the single source of truth for which tools exist. The
executor only invokes tools that are present in the registry, so a model
that hallucinates a tool name cannot trigger code execution.
"""
from __future__ import annotations

from typing import Iterable

from .base import Tool
from .errors import ToolNotAllowedError, ToolNotFoundError


class ToolRegistry:
    """Holds a name -> Tool mapping and exposes a narrow public surface."""

    def __init__(self, tools: Iterable[Tool] | None = None) -> None:
        self._tools: dict[str, Tool] = {}
        if tools:
            for t in tools:
                self.register(t)

    def register(self, tool: Tool) -> None:
        if tool.name in self._tools:
            raise ValueError(f"Tool {tool.name!r} is already registered")
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool:
        if name not in self._tools:
            raise ToolNotFoundError(
                f"Tool {name!r} is not registered", code="tool_not_found"
            )
        return self._tools[name]

    def allowlist(self, names: Iterable[str] | None = None) -> set[str]:
        """Return the set of tool names the agent is allowed to use.

        If `names` is None, all registered tools are allowed. Otherwise only
        the listed names are allowed and any other tool call must be rejected.
        """
        if names is None:
            return set(self._tools)
        unknown = set(names) - set(self._tools)
        if unknown:
            raise ToolNotAllowedError(
                f"Allowlist references unknown tools: {sorted(unknown)}",
                code="tool_not_allowed",
            )
        return set(names)

    def list_tools(self) -> list[Tool]:
        return list(self._tools.values())

    def __contains__(self, name: str) -> bool:
        return name in self._tools
