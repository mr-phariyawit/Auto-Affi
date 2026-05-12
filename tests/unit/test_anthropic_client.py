"""Unit tests for the Anthropic Messages API adapter."""

from __future__ import annotations

import json
from collections.abc import Callable

import httpx
import pytest
from pydantic import SecretStr

from auto_affi.adapters.anthropic_client import (
    AnthropicClient,
    Usage,
    cached_text_block,
    compute_cost_usd,
)


def _make_client(handler: Callable[[httpx.Request], httpx.Response]) -> AnthropicClient:
    transport = httpx.MockTransport(handler)
    http = httpx.AsyncClient(transport=transport)
    return AnthropicClient(api_key=SecretStr("test-key"), client=http, max_retries=3)


def _ok_response(*, text: str = "hello", usage: dict[str, int] | None = None) -> dict[str, object]:
    return {
        "id": "msg_x",
        "type": "message",
        "role": "assistant",
        "model": "claude-opus-4-7",
        "content": [{"type": "text", "text": text}],
        "stop_reason": "end_turn",
        "usage": usage
        or {
            "input_tokens": 1_000,
            "output_tokens": 500,
            "cache_creation_input_tokens": 0,
            "cache_read_input_tokens": 0,
        },
    }


@pytest.mark.unit
async def test_complete_returns_text_usage_and_cost() -> None:
    captured: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["headers"] = dict(request.headers)
        captured["body"] = json.loads(request.content)
        return httpx.Response(200, json=_ok_response(text="สวัสดี"))

    client = _make_client(handler)
    result = await client.complete(
        model="claude-opus-4-7",
        messages=[{"role": "user", "content": "hi"}],
        system="you are helpful",
    )

    assert result.ok is True
    assert result.data is not None
    assert result.data.text == "สวัสดี"
    assert result.data.usage.input_tokens == 1_000
    # 1000 * 15 + 500 * 75 = 15,000 + 37,500 = 52,500 per 1M -> $0.0525
    assert result.cost_usd == pytest.approx(0.0525)

    headers = captured["headers"]
    assert isinstance(headers, dict)
    assert headers["x-api-key"] == "test-key"
    assert headers["anthropic-version"]


@pytest.mark.unit
async def test_cache_read_tokens_drive_cost_down() -> None:
    cached_usage = {
        "input_tokens": 100,
        "output_tokens": 200,
        "cache_creation_input_tokens": 0,
        "cache_read_input_tokens": 5_000,
    }
    full_usage = {
        "input_tokens": 5_100,
        "output_tokens": 200,
        "cache_creation_input_tokens": 0,
        "cache_read_input_tokens": 0,
    }
    cached_cost = compute_cost_usd("claude-opus-4-7", Usage(**cached_usage))
    full_cost = compute_cost_usd("claude-opus-4-7", Usage(**full_usage))
    # Cache reads at 10% of input price should land well below uncached.
    assert cached_cost < full_cost * 0.5


@pytest.mark.unit
async def test_cache_hit_ratio_calculation() -> None:
    usage = Usage(input_tokens=200, output_tokens=50, cache_read_input_tokens=800)
    assert usage.cache_hit_ratio == pytest.approx(0.8)
    empty = Usage(input_tokens=0, output_tokens=0)
    assert empty.cache_hit_ratio == 0.0


@pytest.mark.unit
async def test_rate_limit_retries_then_succeeds() -> None:
    attempts = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            return httpx.Response(429, json={"error": "rate"})
        return httpx.Response(200, json=_ok_response())

    client = _make_client(handler)
    result = await client.complete(
        model="claude-sonnet-4-6",
        messages=[{"role": "user", "content": "hi"}],
    )
    assert result.ok is True
    assert attempts == 2


@pytest.mark.unit
async def test_persistent_rate_limit_surfaces_error() -> None:
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(429)

    client = _make_client(handler)
    result = await client.complete(
        model="claude-haiku-4-5-20251001",
        messages=[{"role": "user", "content": "hi"}],
    )
    assert result.ok is False
    assert result.error is not None
    assert "rate_limited" in result.error


@pytest.mark.unit
async def test_http_400_becomes_adapter_error() -> None:
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(400, text="invalid model")

    client = _make_client(handler)
    result = await client.complete(
        model="claude-opus-4-7",
        messages=[{"role": "user", "content": "hi"}],
    )
    assert result.ok is False
    assert result.error is not None
    assert "HTTP 400" in result.error


@pytest.mark.unit
async def test_malformed_response_surfaces_schema_error() -> None:
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"not": "anthropic"})

    client = _make_client(handler)
    result = await client.complete(
        model="claude-opus-4-7",
        messages=[{"role": "user", "content": "hi"}],
    )
    assert result.ok is False
    assert result.error is not None
    assert "Unexpected" in result.error


@pytest.mark.unit
def test_cached_text_block_carries_cache_control() -> None:
    block = cached_text_block("canonical wiki dump", ttl="1h")
    assert block["type"] == "text"
    assert block["text"] == "canonical wiki dump"
    assert block["cache_control"] == {"type": "ephemeral", "ttl": "1h"}
