"""Shopee Affiliate Open API adapter.

Talks to the Shopee Affiliate GraphQL endpoint
(``https://open-api.affiliate.shopee.co.th/graphql``) using the documented
SHA256-HMAC signature scheme:

    payload   = "<app_id><timestamp><body><secret>"
    signature = sha256(payload).hexdigest()
    Authorization: SHA256 Credential=<app_id>, Timestamp=<ts>, Signature=<sig>

Phase 1 scope:
- ``search_products`` — keyword + category + commission filter
- ``generate_short_link`` — affiliate deep link with full 5-slot subId taxonomy

The adapter wraps every call in :class:`ToolResult` for uniform cost / latency
tracking and retries transient failures with exponential backoff.
"""

from __future__ import annotations

import hashlib
import json
import time
import uuid
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any, ClassVar

import httpx
from pydantic import BaseModel, Field, SecretStr
from tenacity import (
    AsyncRetrying,
    RetryError,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from auto_affi.adapters.shopee_subids import SubIds
from auto_affi.exceptions import AdapterError, RateLimitError, SchemaValidationError
from auto_affi.schemas.tool_result import ToolResult


class ShopeeProduct(BaseModel):
    """A trimmed Shopee product offer used by the Scout agent."""

    item_id: int
    shop_id: int
    name: str
    price_min: float = Field(ge=0)
    price_max: float = Field(ge=0)
    commission_rate: float = Field(ge=0, le=1, description="0.0-1.0 fraction")
    rating_star: float = Field(ge=0, le=5)
    sales: int = Field(ge=0)
    image_url: str | None = None


class ShopeeShortLink(BaseModel):
    """The output of ``generate_short_link``."""

    short_link: str
    sub_ids: list[str]


@dataclass(frozen=True)
class _Endpoint:
    base_url: str
    path: str = "/graphql"

    @property
    def url(self) -> str:
        return self.base_url.rstrip("/") + self.path


TH_ENDPOINT = _Endpoint(base_url="https://open-api.affiliate.shopee.co.th")


_PRODUCT_QUERY = """\
query ProductOfferV2($keyword: String!, $page: Int!, $limit: Int!, \
$sortType: Int, $listType: Int) {
  productOfferV2(keyword: $keyword, page: $page, limit: $limit, \
sortType: $sortType, listType: $listType) {
    nodes {
      itemId
      shopId
      productName
      priceMin
      priceMax
      commissionRate
      ratingStar
      sales
      imageUrl
    }
  }
}
"""

_SHORTLINK_MUTATION = """\
mutation GenerateShortLink($input: ShortLinkInput!) {
  generateShortLink(input: $input) {
    shortLink
  }
}
"""


class ShopeeClient:
    """Async Shopee Affiliate Open API client."""

    _SIG_ALGO: ClassVar[str] = "SHA256"

    def __init__(
        self,
        app_id: str,
        secret: SecretStr,
        *,
        endpoint: _Endpoint = TH_ENDPOINT,
        timeout_s: float = 15.0,
        client: httpx.AsyncClient | None = None,
        max_retries: int = 3,
    ) -> None:
        if not app_id:
            raise AdapterError("Shopee app_id is required")
        self._app_id = app_id
        self._secret = secret
        self._endpoint = endpoint
        self._timeout_s = timeout_s
        self._client = client
        self._max_retries = max_retries

    # ------------------------------------------------------------------ #
    # public surface                                                     #
    # ------------------------------------------------------------------ #

    async def search_products(
        self,
        keyword: str,
        *,
        page: int = 1,
        limit: int = 20,
        min_commission_pct: float = 3.0,
    ) -> ToolResult[list[ShopeeProduct]]:
        """Search the TH Shopee affiliate catalog by keyword."""
        body = {
            "query": _PRODUCT_QUERY,
            "variables": {
                "keyword": keyword,
                "page": page,
                "limit": limit,
                "sortType": 2,
                "listType": 0,
            },
        }
        return await self._call(
            body=body,
            parser=lambda data: _parse_products(data, min_commission_pct=min_commission_pct),
        )

    async def generate_short_link(
        self,
        *,
        item_id: int,
        shop_id: int,
        sub_ids: SubIds,
    ) -> ToolResult[ShopeeShortLink]:
        """Create an affiliate deep link with the full 5-slot subId taxonomy."""
        body = {
            "query": _SHORTLINK_MUTATION,
            "variables": {
                "input": {
                    "itemId": item_id,
                    "shopId": shop_id,
                    "subIds": sub_ids.to_list(),
                }
            },
        }
        return await self._call(
            body=body,
            parser=lambda data: _parse_short_link(data, sub_ids=sub_ids),
        )

    # ------------------------------------------------------------------ #
    # transport                                                          #
    # ------------------------------------------------------------------ #

    async def _call[T](
        self,
        *,
        body: Mapping[str, Any],
        parser: Callable[[dict[str, Any]], T],
    ) -> ToolResult[T]:
        body_str = json.dumps(body, separators=(",", ":"))
        timestamp = int(time.time())
        signature = self._sign(body=body_str, timestamp=timestamp)
        headers = {
            "Content-Type": "application/json",
            "Authorization": (
                f"{self._SIG_ALGO} Credential={self._app_id}, "
                f"Timestamp={timestamp}, Signature={signature}"
            ),
        }
        trace_id = uuid.uuid4().hex
        start = time.perf_counter()
        try:
            payload = await self._do_request(body_str=body_str, headers=headers)
            latency_ms = int((time.perf_counter() - start) * 1000)
            data = parser(payload)
            return ToolResult(ok=True, data=data, latency_ms=latency_ms, trace_id=trace_id)
        except RateLimitError as err:
            latency_ms = int((time.perf_counter() - start) * 1000)
            return ToolResult(
                ok=False, error=f"rate_limited: {err}", latency_ms=latency_ms, trace_id=trace_id
            )
        except (AdapterError, SchemaValidationError) as err:
            latency_ms = int((time.perf_counter() - start) * 1000)
            return ToolResult(ok=False, error=str(err), latency_ms=latency_ms, trace_id=trace_id)

    async def _do_request(self, *, body_str: str, headers: dict[str, str]) -> dict[str, Any]:
        retrying = AsyncRetrying(
            stop=stop_after_attempt(self._max_retries),
            wait=wait_exponential(multiplier=1, min=1, max=10),
            retry=retry_if_exception_type(RateLimitError),
            reraise=True,
        )
        try:
            async for attempt in retrying:
                with attempt:
                    return await self._raw_post(body_str=body_str, headers=headers)
        except RetryError as err:
            raise RateLimitError("Shopee API rate-limited after retries") from err
        # Defensive: AsyncRetrying always yields at least once with reraise=True.
        raise AdapterError("Shopee request did not execute")

    async def _raw_post(self, *, body_str: str, headers: dict[str, str]) -> dict[str, Any]:
        client = self._client or httpx.AsyncClient(timeout=self._timeout_s)
        owns_client = self._client is None
        try:
            response = await client.post(self._endpoint.url, content=body_str, headers=headers)
        finally:
            if owns_client:
                await client.aclose()

        if response.status_code == 429:
            raise RateLimitError("HTTP 429 from Shopee")
        if response.status_code >= 500:
            raise RateLimitError(f"HTTP {response.status_code} from Shopee (transient)")
        if response.status_code >= 400:
            raise AdapterError(f"HTTP {response.status_code}: {response.text[:200]}")

        try:
            payload: dict[str, Any] = response.json()
        except json.JSONDecodeError as err:
            raise AdapterError("Shopee returned non-JSON body") from err

        if payload.get("errors"):
            raise AdapterError(f"GraphQL errors: {payload['errors']}")
        return payload

    def _sign(self, *, body: str, timestamp: int) -> str:
        payload = f"{self._app_id}{timestamp}{body}{self._secret.get_secret_value()}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------- #
# parsers                                                                #
# ---------------------------------------------------------------------- #


def _parse_products(payload: dict[str, Any], *, min_commission_pct: float) -> list[ShopeeProduct]:
    try:
        nodes = payload["data"]["productOfferV2"]["nodes"]
    except (KeyError, TypeError) as err:
        raise SchemaValidationError("Unexpected Shopee product payload") from err

    threshold = min_commission_pct / 100.0
    products: list[ShopeeProduct] = []
    for node in nodes:
        try:
            product = ShopeeProduct(
                item_id=int(node["itemId"]),
                shop_id=int(node["shopId"]),
                name=str(node["productName"]),
                price_min=float(node["priceMin"]),
                price_max=float(node["priceMax"]),
                commission_rate=float(node["commissionRate"]),
                rating_star=float(node["ratingStar"]),
                sales=int(node["sales"]),
                image_url=node.get("imageUrl"),
            )
        except (KeyError, TypeError, ValueError) as err:
            raise SchemaValidationError(f"Bad product node: {node!r}") from err
        if product.commission_rate >= threshold:
            products.append(product)
    return products


def _parse_short_link(payload: dict[str, Any], *, sub_ids: SubIds) -> ShopeeShortLink:
    try:
        short = payload["data"]["generateShortLink"]["shortLink"]
    except (KeyError, TypeError) as err:
        raise SchemaValidationError("Unexpected shortlink payload") from err
    return ShopeeShortLink(short_link=str(short), sub_ids=sub_ids.to_list())
