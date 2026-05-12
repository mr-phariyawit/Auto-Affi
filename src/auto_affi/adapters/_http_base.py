"""Shared HTTP transport policy for vendor adapters.

Every vendor adapter (Shopee, Anthropic, kie.ai, ElevenLabs, ...) needs the
same five pieces of glue around its actual signing / parsing logic:

1. Optional injected ``httpx.AsyncClient`` lifecycle (use the caller's, close
   our own).
2. Exponential-backoff retry on :class:`RateLimitError`.
3. HTTP status → exception mapping (429 → RateLimitError, 5xx → RateLimitError
   transient, 4xx → AdapterError).
4. JSON-body parsing with a typed error on non-JSON responses.
5. ToolResult wrapping with ``trace_id`` + ``latency_ms`` and uniform error
   shape (``rate_limited:`` prefix for backpressure, raw ``str(err)`` for
   adapter / schema errors).

Adapters keep their own:
- Body construction (GraphQL query, Messages payload, etc.)
- Headers + signing (Shopee HMAC, Anthropic x-api-key, etc.)
- Response parsing (their `_parse_*` helpers stay local)
- Cost computation (provider-specific token tables stay local)

This module is intentionally small + free of vendor-specific knowledge so
the next adapter (kie.ai for video, ElevenLabs for TTS, etc.) drops in
without re-implementing the same defensive plumbing.
"""

from __future__ import annotations

import time
import uuid
from collections.abc import Awaitable, Callable, Mapping
from dataclasses import dataclass
from typing import Any

import httpx
from tenacity import (
    AsyncRetrying,
    RetryError,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from auto_affi.exceptions import AdapterError, RateLimitError, SchemaValidationError
from auto_affi.schemas.tool_result import ToolResult


@dataclass(frozen=True, slots=True)
class HttpExecutor:
    """Shared HTTP request policy for vendor adapters.

    Construct one per adapter at ``__init__`` time and reuse for every call;
    it's immutable + cheap.

    Parameters mirror what each adapter previously held as private fields:
    ``timeout_s``, ``max_retries``, an optional injected ``client`` (used for
    tests and shared httpx pools), and a ``vendor`` label that shows up in
    error messages (``"Shopee API rate-limited after retries"``).
    """

    vendor: str
    timeout_s: float = 15.0
    max_retries: int = 3
    client: httpx.AsyncClient | None = None

    async def post(
        self,
        *,
        url: str,
        body: str | Mapping[str, Any],
        headers: Mapping[str, str],
    ) -> dict[str, Any]:
        """Issue a POST with retry on :class:`RateLimitError`. Returns parsed JSON.

        ``body`` may be a pre-serialized ``str`` (when the adapter signed an
        exact byte sequence — Shopee) or a mapping that httpx serializes with
        ``json=`` (Anthropic). Headers are passed through verbatim.
        """
        retrying = AsyncRetrying(
            stop=stop_after_attempt(self.max_retries),
            wait=wait_exponential(multiplier=1, min=1, max=10),
            retry=retry_if_exception_type(RateLimitError),
            reraise=True,
        )
        try:
            async for attempt in retrying:
                with attempt:
                    return await self._raw_post(url=url, body=body, headers=headers)
        except RetryError as err:
            raise RateLimitError(f"{self.vendor} API rate-limited after retries") from err
        # Defensive: AsyncRetrying always yields at least once with reraise=True.
        raise AdapterError(f"{self.vendor} request did not execute")

    async def _raw_post(
        self, *, url: str, body: str | Mapping[str, Any], headers: Mapping[str, str]
    ) -> dict[str, Any]:
        client = self.client or httpx.AsyncClient(timeout=self.timeout_s)
        owns_client = self.client is None
        try:
            if isinstance(body, str):
                response = await client.post(url, content=body, headers=dict(headers))
            else:
                response = await client.post(url, json=dict(body), headers=dict(headers))
        finally:
            if owns_client:
                await client.aclose()

        if response.status_code == 429:
            raise RateLimitError(f"HTTP 429 from {self.vendor}")
        if response.status_code >= 500:
            raise RateLimitError(f"HTTP {response.status_code} from {self.vendor} (transient)")
        if response.status_code >= 400:
            raise AdapterError(f"HTTP {response.status_code}: {response.text[:200]}")

        try:
            payload: dict[str, Any] = response.json()
        except ValueError as err:
            raise AdapterError(f"{self.vendor} returned non-JSON body") from err
        return payload


async def call_with_result[T](
    fn: Callable[[], Awaitable[T]],
    *,
    cost_fn: Callable[[T], float] | None = None,
) -> ToolResult[T]:
    """Run ``fn`` and wrap success/failure in :class:`ToolResult`.

    Captures trace_id + latency + (optionally) cost so adapters don't have
    to repeat the try/except/timing dance around every public method.

    Maps the standard exception surface used by all adapters:
    - :class:`RateLimitError` → ``ok=False``, ``error="rate_limited: ..."``
    - :class:`AdapterError` / :class:`SchemaValidationError` → ``ok=False``,
      ``error=str(err)``
    - Anything else propagates (caller bug, not a vendor failure).
    """
    trace_id = uuid.uuid4().hex
    start = time.perf_counter()

    def _elapsed_ms() -> int:
        return int((time.perf_counter() - start) * 1000)

    try:
        data = await fn()
    except RateLimitError as err:
        return ToolResult(
            ok=False,
            error=f"rate_limited: {err}",
            latency_ms=_elapsed_ms(),
            trace_id=trace_id,
        )
    except (AdapterError, SchemaValidationError) as err:
        return ToolResult(ok=False, error=str(err), latency_ms=_elapsed_ms(), trace_id=trace_id)

    cost = cost_fn(data) if cost_fn is not None else 0.0
    return ToolResult(
        ok=True,
        data=data,
        cost_usd=cost,
        latency_ms=_elapsed_ms(),
        trace_id=trace_id,
    )
