"""Anthropic Messages API adapter.

Central LLM gateway used by every agent. Wraps the Claude Messages API
with:

  - prompt caching on system + tools + canonical-wiki blocks (per
    docs/llm-allocation.md §3), so repeated agent turns hit cache reads
    at ~10% of the normal input price
  - cost computation from usage tokens using a per-model price table
    (Opus 4.7 / Sonnet 4.6 / Haiku 4.5, May 2026 list prices)
  - uniform ToolResult[CompletionResult] return shape so the Feedback
    Curator can aggregate latency / cost / cache-hit-rate across agents
  - tenacity retry on 429 + 5xx with exponential backoff

This module only knows about the transport contract. Higher-level helpers
(building tool definitions, parsing tool_use blocks, etc.) belong with
the per-agent code in src/auto_affi/agents/.
"""

from __future__ import annotations

import time
import uuid
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Literal

import httpx
from pydantic import BaseModel, Field, SecretStr
from tenacity import (
    AsyncRetrying,
    RetryError,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from auto_affi.exceptions import AdapterError, RateLimitError, SchemaValidationError
from auto_affi.schemas.tool_result import ToolResult

# --------------------------------------------------------------------- #
# constants                                                             #
# --------------------------------------------------------------------- #

ANTHROPIC_BASE_URL = "https://api.anthropic.com"
MESSAGES_PATH = "/v1/messages"
DEFAULT_API_VERSION = "2023-06-01"

Model = Literal[
    "claude-opus-4-7",
    "claude-sonnet-4-6",
    "claude-haiku-4-5-20251001",
]


# USD per 1M tokens (May 2026 list prices). Cache reads are ~10% of input
# and cache writes are ~125% of input -- typical Anthropic pricing curve.
@dataclass(frozen=True)
class _Price:
    input_per_m: float
    output_per_m: float
    cache_write_per_m: float
    cache_read_per_m: float


_PRICES: dict[Model, _Price] = {
    "claude-opus-4-7": _Price(15.0, 75.0, 18.75, 1.50),
    "claude-sonnet-4-6": _Price(3.0, 15.0, 3.75, 0.30),
    "claude-haiku-4-5-20251001": _Price(0.80, 4.0, 1.00, 0.08),
}


# --------------------------------------------------------------------- #
# response types                                                        #
# --------------------------------------------------------------------- #


class Usage(BaseModel):
    """Token usage extracted from the Anthropic response."""

    input_tokens: int = Field(ge=0)
    output_tokens: int = Field(ge=0)
    cache_creation_input_tokens: int = Field(ge=0, default=0)
    cache_read_input_tokens: int = Field(ge=0, default=0)

    @property
    def total_tokens(self) -> int:
        return (
            self.input_tokens
            + self.output_tokens
            + self.cache_creation_input_tokens
            + self.cache_read_input_tokens
        )

    @property
    def cache_hit_ratio(self) -> float:
        """Fraction of input tokens served from cache (0.0..1.0)."""
        denom = self.input_tokens + self.cache_read_input_tokens
        if denom == 0:
            return 0.0
        return self.cache_read_input_tokens / denom


class CompletionResult(BaseModel):
    """The bits of the Messages API response higher layers actually need."""

    text: str
    stop_reason: str | None = None
    model: Model
    usage: Usage
    content_blocks: list[dict[str, Any]] = Field(default_factory=list)


def compute_cost_usd(model: Model, usage: Usage) -> float:
    """Return the USD cost of a single response from token usage."""
    price = _PRICES[model]
    return (
        usage.input_tokens * price.input_per_m
        + usage.output_tokens * price.output_per_m
        + usage.cache_creation_input_tokens * price.cache_write_per_m
        + usage.cache_read_input_tokens * price.cache_read_per_m
    ) / 1_000_000.0


# --------------------------------------------------------------------- #
# client                                                                #
# --------------------------------------------------------------------- #


class AnthropicClient:
    """Async Anthropic Messages API client with caching + retry built in."""

    def __init__(
        self,
        api_key: SecretStr,
        *,
        base_url: str = ANTHROPIC_BASE_URL,
        api_version: str = DEFAULT_API_VERSION,
        timeout_s: float = 60.0,
        max_retries: int = 3,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        if not api_key.get_secret_value():
            raise AdapterError("Anthropic api_key is required")
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._api_version = api_version
        self._timeout_s = timeout_s
        self._max_retries = max_retries
        self._client = client

    async def complete(
        self,
        *,
        model: Model,
        messages: list[Mapping[str, Any]],
        system: list[Mapping[str, Any]] | str | None = None,
        tools: list[Mapping[str, Any]] | None = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        extra_headers: Mapping[str, str] | None = None,
    ) -> ToolResult[CompletionResult]:
        """Issue one Messages request. Caching is implicit if the caller
        already placed ``cache_control`` markers on system / tools / message
        blocks; this helper does not mutate the caller's payload.
        """
        body: dict[str, Any] = {
            "model": model,
            "messages": list(messages),
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        if system is not None:
            body["system"] = system
        if tools:
            body["tools"] = list(tools)

        headers: dict[str, str] = {
            "content-type": "application/json",
            "x-api-key": self._api_key.get_secret_value(),
            "anthropic-version": self._api_version,
        }
        if extra_headers:
            headers.update(extra_headers)

        trace_id = uuid.uuid4().hex
        start = time.perf_counter()
        try:
            payload = await self._do_request(body=body, headers=headers)
            latency_ms = int((time.perf_counter() - start) * 1000)
            result = _parse_response(payload, model=model)
            cost_usd = compute_cost_usd(model, result.usage)
            return ToolResult(
                ok=True,
                data=result,
                cost_usd=cost_usd,
                latency_ms=latency_ms,
                trace_id=trace_id,
            )
        except RateLimitError as err:
            latency_ms = int((time.perf_counter() - start) * 1000)
            return ToolResult(
                ok=False,
                error=f"rate_limited: {err}",
                latency_ms=latency_ms,
                trace_id=trace_id,
            )
        except (AdapterError, SchemaValidationError) as err:
            latency_ms = int((time.perf_counter() - start) * 1000)
            return ToolResult(ok=False, error=str(err), latency_ms=latency_ms, trace_id=trace_id)

    # ------------------------------------------------------------------ #
    # transport                                                          #
    # ------------------------------------------------------------------ #

    async def _do_request(
        self, *, body: Mapping[str, Any], headers: dict[str, str]
    ) -> dict[str, Any]:
        retrying = AsyncRetrying(
            stop=stop_after_attempt(self._max_retries),
            wait=wait_exponential(multiplier=1, min=1, max=10),
            retry=retry_if_exception_type(RateLimitError),
            reraise=True,
        )
        try:
            async for attempt in retrying:
                with attempt:
                    return await self._raw_post(body=body, headers=headers)
        except RetryError as err:
            raise RateLimitError("Anthropic API rate-limited after retries") from err
        raise AdapterError("Anthropic request did not execute")

    async def _raw_post(
        self, *, body: Mapping[str, Any], headers: dict[str, str]
    ) -> dict[str, Any]:
        url = self._base_url + MESSAGES_PATH
        client = self._client or httpx.AsyncClient(timeout=self._timeout_s)
        owns_client = self._client is None
        try:
            response = await client.post(url, json=dict(body), headers=headers)
        finally:
            if owns_client:
                await client.aclose()

        if response.status_code == 429:
            raise RateLimitError("HTTP 429 from Anthropic")
        if response.status_code >= 500:
            raise RateLimitError(f"HTTP {response.status_code} from Anthropic (transient)")
        if response.status_code >= 400:
            raise AdapterError(f"HTTP {response.status_code}: {response.text[:200]}")

        try:
            payload: dict[str, Any] = response.json()
        except ValueError as err:
            raise AdapterError("Anthropic returned non-JSON body") from err
        return payload


# --------------------------------------------------------------------- #
# parsing                                                               #
# --------------------------------------------------------------------- #


def _parse_response(payload: dict[str, Any], *, model: Model) -> CompletionResult:
    try:
        content_blocks = payload["content"]
        usage_dict = payload["usage"]
    except (KeyError, TypeError) as err:
        raise SchemaValidationError("Unexpected Anthropic response shape") from err

    if not isinstance(content_blocks, list):
        raise SchemaValidationError("content must be a list of blocks")

    text_parts: list[str] = []
    for block in content_blocks:
        if isinstance(block, dict) and block.get("type") == "text":
            text = block.get("text")
            if isinstance(text, str):
                text_parts.append(text)

    try:
        usage = Usage(
            input_tokens=int(usage_dict.get("input_tokens", 0)),
            output_tokens=int(usage_dict.get("output_tokens", 0)),
            cache_creation_input_tokens=int(usage_dict.get("cache_creation_input_tokens", 0) or 0),
            cache_read_input_tokens=int(usage_dict.get("cache_read_input_tokens", 0) or 0),
        )
    except (TypeError, ValueError) as err:
        raise SchemaValidationError("Bad usage block") from err

    return CompletionResult(
        text="".join(text_parts),
        stop_reason=payload.get("stop_reason"),
        model=model,
        usage=usage,
        content_blocks=[b for b in content_blocks if isinstance(b, dict)],
    )


# --------------------------------------------------------------------- #
# helpers                                                               #
# --------------------------------------------------------------------- #


def cached_text_block(text: str, *, ttl: Literal["5m", "1h"] = "1h") -> dict[str, Any]:
    """Build a single text block tagged for prompt caching.

    Use as the trailing element of the ``system`` array (or any large
    cached chunk) so subsequent requests reuse it instead of paying full
    input price.
    """
    return {
        "type": "text",
        "text": text,
        "cache_control": {"type": "ephemeral", "ttl": ttl},
    }
