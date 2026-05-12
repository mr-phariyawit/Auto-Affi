"""Smoke tests for the ToolResult schema."""

from __future__ import annotations

import pytest

from auto_affi.schemas.tool_result import ToolResult


@pytest.mark.unit
def test_ok_result_with_data() -> None:
    result: ToolResult[dict[str, int]] = ToolResult(
        ok=True,
        data={"score": 42},
        cost_usd=0.012,
        latency_ms=840,
        trace_id="trace-1",
    )
    assert result.ok is True
    assert result.data == {"score": 42}
    assert result.cost_usd == pytest.approx(0.012)


@pytest.mark.unit
def test_error_result_without_data() -> None:
    result: ToolResult[None] = ToolResult(ok=False, error="rate limited")
    assert result.ok is False
    assert result.data is None
    assert result.error == "rate limited"


@pytest.mark.unit
def test_negative_cost_rejected() -> None:
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        ToolResult(ok=True, cost_usd=-1.0)
