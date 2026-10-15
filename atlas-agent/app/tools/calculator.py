"""Calculator tool.

We deliberately do not use `eval` on the raw input. Instead we parse the
expression into an AST and only allow numeric literals, the four basic
arithmetic operators, parentheses, and unary minus. This makes the tool safe
to expose to a model that may produce adversarial input.
"""
from __future__ import annotations

import ast
import math
import operator
from typing import Any

from pydantic import BaseModel, Field

from .base import Tool
from .errors import ToolInputError, ToolExecutionError


class CalculatorInput(BaseModel):
    expression: str = Field(..., min_length=1, max_length=512, description="Arithmetic expression")


class CalculatorOutput(BaseModel):
    result: float
    expression: str


_BINARY_OPS: dict[type, Any] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
_UNARY_OPS: dict[type, Any] = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def _safe_eval(node: ast.AST) -> float:
    if isinstance(node, ast.Expression):
        return _safe_eval(node.body)
    if isinstance(node, ast.Constant):
        if not isinstance(node.value, (int, float)):
            raise ToolInputError(
                f"Only numeric literals are allowed, got {type(node.value).__name__}",
                code="tool_input_invalid",
            )
        return float(node.value)
    if isinstance(node, ast.BinOp) and type(node.op) in _BINARY_OPS:
        left = _safe_eval(node.left)
        right = _safe_eval(node.right)
        try:
            return _BINARY_OPS[type(node.op)](left, right)
        except ZeroDivisionError as exc:
            raise ToolInputError("Division by zero", code="tool_input_invalid") from exc
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPS:
        return _UNARY_OPS[type(node.op)](_safe_eval(node.operand))
    raise ToolInputError(
        f"Unsupported expression node: {type(node).__name__}",
        code="tool_input_invalid",
    )


class CalculatorTool(Tool[CalculatorInput, CalculatorOutput]):
    """Evaluate a simple arithmetic expression."""

    name = "calculator"
    description = (
        "Evaluate a basic arithmetic expression using +, -, *, /, //, %, ** "
        "and parentheses. Use this whenever the user asks for a numeric "
        "calculation that should not be guessed."
    )
    input_schema = CalculatorInput
    output_schema = CalculatorOutput

    async def run(self, payload: CalculatorInput) -> CalculatorOutput:
        try:
            tree = ast.parse(payload.expression, mode="eval")
            value = _safe_eval(tree)
        except ToolInputError:
            raise
        except (SyntaxError, ValueError) as exc:
            raise ToolInputError(
                f"Could not parse expression: {exc}", code="tool_input_invalid"
            ) from exc
        except Exception as exc:  # pragma: no cover - defensive
            raise ToolExecutionError(
                f"Calculator failed: {exc}", code="tool_execution_error"
            ) from exc

        if not math.isfinite(value):
            raise ToolInputError(
                "Expression produced a non-finite value", code="tool_input_invalid"
            )

        return CalculatorOutput(result=value, expression=payload.expression)
