"""Tool interface and base classes.

A Tool is a typed, schema-validated capability an agent can invoke. The
contract is deliberately small so we can build a registry, an executor with
timeouts, and a ReAct loop on top without coupling them to a specific
framework.
"""
from __future__ import annotations

import abc
from dataclasses import dataclass, field
from typing import Any, Generic, TypeVar

InputT = TypeVar("InputT")
OutputT = TypeVar("OutputT")


@dataclass(frozen=True)
class ToolRisk:
    """Risk classification for a tool call.

    - read_only: no side effects, safe to run without approval.
    - reversible_write: modifies state but the change can be undone.
    - destructive: cannot be easily undone; requires human approval.
    """

    level: str = "read_only"  # one of: read_only, reversible_write, destructive


class Tool(abc.ABC, Generic[InputT, OutputT]):
    """Base class for all tools.

    Subclasses must define:
      - name: short, snake_case, unique
      - description: one sentence, used by the LLM to pick the right tool
      - input_schema: a Pydantic model describing the input
      - output_schema: a Pydantic model describing the output
      - run(): the actual implementation
    """

    name: str
    description: str
    input_schema: type
    output_schema: type
    risk: ToolRisk = ToolRisk()
    timeout_seconds: float = 10.0

    def __init__(
        self,
        *,
        risk: ToolRisk | None = None,
        timeout_seconds: float | None = None,
    ) -> None:
        if risk is not None:
            self.risk = risk
        if timeout_seconds is not None:
            self.timeout_seconds = timeout_seconds

    def validate_input(self, raw: Any) -> InputT:
        """Coerce `raw` (typically a dict from the model) into the input model."""
        if isinstance(raw, self.input_schema):
            return raw
        if isinstance(raw, dict):
            return self.input_schema.model_validate(raw)
        raise ValueError(
            f"Tool {self.name!r} expects dict or {self.input_schema.__name__}, "
            f"got {type(raw).__name__}"
        )

    @abc.abstractmethod
    async def run(self, payload: InputT) -> OutputT:
        """Execute the tool. Must be idempotent and side-effect aware per risk."""
        raise NotImplementedError
