"""Tests for the calculator tool."""
from __future__ import annotations

import pytest

from app.tools.calculator import CalculatorInput, CalculatorTool
from app.tools.errors import ToolInputError


@pytest.mark.asyncio
async def test_calculator_basic_arithmetic() -> None:
    tool = CalculatorTool()
    out = await tool.run(CalculatorInput(expression="2 + 2"))
    assert out.result == 4.0


@pytest.mark.asyncio
async def test_calculator_precedence_and_parens() -> None:
    tool = CalculatorTool()
    out = await tool.run(CalculatorInput(expression="(3 + 4) * 2 - 5"))
    assert out.result == 9.0


@pytest.mark.asyncio
async def test_calculator_power_and_unary() -> None:
    tool = CalculatorTool()
    out = await tool.run(CalculatorInput(expression="-(2**3) + 1"))
    assert out.result == -7.0


@pytest.mark.asyncio
async def test_calculator_rejects_function_call() -> None:
    tool = CalculatorTool()
    with pytest.raises(ToolInputError):
        await tool.run(CalculatorInput(expression="__import__('os').system('ls')"))


@pytest.mark.asyncio
async def test_calculator_rejects_name_lookup() -> None:
    tool = CalculatorTool()
    with pytest.raises(ToolInputError):
        await tool.run(CalculatorInput(expression="open('x')"))


@pytest.mark.asyncio
async def test_calculator_rejects_division_by_zero() -> None:
    tool = CalculatorTool()
    with pytest.raises(ToolInputError):
        await tool.run(CalculatorInput(expression="1/0"))


@pytest.mark.asyncio
async def test_calculator_rejects_empty() -> None:
    tool = CalculatorTool()
    with pytest.raises(Exception):
        await tool.run(CalculatorInput(expression=""))


def test_calculator_validates_input_type() -> None:
    tool = CalculatorTool()
    payload = tool.validate_input({"expression": "5*5"})
    assert isinstance(payload, CalculatorInput)
    assert payload.expression == "5*5"
