"""Unit tests for the Shopee adapter — signing, parsing, retry behaviour.

We use ``httpx.MockTransport`` so no network is touched. Vendor cassettes
(VCR-based, real responses captured once) belong under ``tests/integration``
and gate on an env flag.
"""

from __future__ import annotations

import hashlib
import json
import time
from collections.abc import Callable

import httpx
import pytest
from pydantic import SecretStr

from auto_affi.adapters.shopee import ShopeeClient, ShopeeProduct
from auto_affi.adapters.shopee_subids import SubIds

_APP_ID = "app-test"
_SECRET = "shh"


def _make_client(handler: Callable[[httpx.Request], httpx.Response]) -> ShopeeClient:
    transport = httpx.MockTransport(handler)
    http = httpx.AsyncClient(transport=transport)
    return ShopeeClient(
        app_id=_APP_ID,
        secret=SecretStr(_SECRET),
        client=http,
        max_retries=3,
    )


def _expected_signature(body: str, timestamp: int) -> str:
    return hashlib.sha256(f"{_APP_ID}{timestamp}{body}{_SECRET}".encode()).hexdigest()


@pytest.mark.unit
async def test_search_products_signs_request_and_filters_by_commission() -> None:
    captured: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["url"] = str(request.url)
        captured["auth"] = request.headers["Authorization"]
        captured["body"] = request.content.decode("utf-8")
        return httpx.Response(
            200,
            json={
                "data": {
                    "productOfferV2": {
                        "nodes": [
                            _product_node(item_id=1, commission=0.08, sales=500),
                            _product_node(item_id=2, commission=0.02, sales=10),
                        ]
                    }
                }
            },
        )

    client = _make_client(handler)
    result = await client.search_products("เซรั่ม", min_commission_pct=3.0)

    assert result.ok is True
    assert result.data is not None
    assert [p.item_id for p in result.data] == [1]
    assert isinstance(result.data[0], ShopeeProduct)

    # Verify the signature matches the body & timestamp recorded by the server.
    body = str(captured["body"])
    auth = str(captured["auth"])
    timestamp = _parse_timestamp(auth)
    assert _parse_signature(auth) == _expected_signature(body, timestamp)
    assert abs(timestamp - int(time.time())) < 5
    assert result.trace_id is not None


@pytest.mark.unit
async def test_rate_limit_retries_then_succeeds() -> None:
    attempts = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            return httpx.Response(429, json={"error": "rate limited"})
        return httpx.Response(
            200,
            json={"data": {"productOfferV2": {"nodes": []}}},
        )

    client = _make_client(handler)
    result = await client.search_products("foo")

    assert result.ok is True
    assert attempts == 2


@pytest.mark.unit
async def test_persistent_rate_limit_surfaces_error() -> None:
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(429)

    client = _make_client(handler)
    result = await client.search_products("foo")

    assert result.ok is False
    assert result.error is not None
    assert "rate_limited" in result.error


@pytest.mark.unit
async def test_generate_short_link_sends_subids_in_order() -> None:
    captured: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["body"] = json.loads(request.content)
        return httpx.Response(
            200,
            json={"data": {"generateShortLink": {"shortLink": "https://s.shopee.co.th/x"}}},
        )

    client = _make_client(handler)
    sub_ids = SubIds(
        platform="tk",
        account="@nattatips",
        video_id="v1",
        campaign_id="c1",
        variant="A",
    )
    result = await client.generate_short_link(item_id=11, shop_id=22, sub_ids=sub_ids)

    assert result.ok is True
    assert result.data is not None
    assert result.data.short_link == "https://s.shopee.co.th/x"
    body_input = captured["body"]
    assert isinstance(body_input, dict)
    variables = body_input["variables"]["input"]
    assert variables["itemId"] == 11
    assert variables["shopId"] == 22
    assert variables["subIds"] == ["tk", "@nattatips", "v1", "c1", "A"]


@pytest.mark.unit
async def test_graphql_errors_become_adapter_error() -> None:
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"errors": [{"message": "boom"}]})

    client = _make_client(handler)
    result = await client.search_products("foo")

    assert result.ok is False
    assert result.error is not None
    assert "GraphQL errors" in result.error


@pytest.mark.unit
async def test_bad_node_schema_surfaces_validation_error() -> None:
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={"data": {"productOfferV2": {"nodes": [{"itemId": "not-a-number"}]}}},
        )

    client = _make_client(handler)
    result = await client.search_products("foo")

    assert result.ok is False
    assert result.error is not None
    assert "Bad product node" in result.error


# ---------------------------------------------------------------------- #
# helpers                                                                #
# ---------------------------------------------------------------------- #


def _product_node(*, item_id: int, commission: float, sales: int) -> dict[str, object]:
    return {
        "itemId": item_id,
        "shopId": 999,
        "productName": "เซรั่มทดสอบ",
        "priceMin": 199.0,
        "priceMax": 299.0,
        "commissionRate": commission,
        "ratingStar": 4.7,
        "sales": sales,
        "imageUrl": "https://cf.shopee.co.th/x.jpg",
    }


def _parse_timestamp(auth: str) -> int:
    for part in auth.split(","):
        part = part.strip()
        if part.startswith("Timestamp="):
            return int(part.removeprefix("Timestamp="))
    raise AssertionError(f"no Timestamp in {auth!r}")


def _parse_signature(auth: str) -> str:
    for part in auth.split(","):
        part = part.strip()
        if part.startswith("Signature="):
            return part.removeprefix("Signature=")
    raise AssertionError(f"no Signature in {auth!r}")
