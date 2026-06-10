"""Standard tool result wrapper used by every MCP-style agent tool.

Every agent tool returns this shape so the Feedback Curator can track cost,
latency, and failure rate at the tool level.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class ToolResult[T](BaseModel):
    """Uniform return shape for all agent tools."""

    ok: bool
    data: T | None = None
    error: str | None = None
    cost_usd: float = Field(ge=0.0, default=0.0)
    latency_ms: int = Field(ge=0, default=0)
    trace_id: str | None = None
