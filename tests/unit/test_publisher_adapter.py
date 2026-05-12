"""Unit tests for publishing adapters (FR-PB-01)."""

from __future__ import annotations

import json

import httpx
import pytest
from pydantic import SecretStr

from auto_affi.adapters.publisher import (
    DryRunPublisher,
    IGReelsConfig,
    IGReelsPublisher,
    PublishPlatform,
    PublishRecord,
)
from auto_affi.exceptions import AdapterError


_TOKEN = "test-token"
_USER_ID = "17841400000000001"


def _make_ig_publisher(
    handler: object,
) -> IGReelsPublisher:
    transport = httpx.MockTransport(handler)  # type: ignore[arg-type]
    http = httpx.AsyncClient(transport=transport)
    config = IGReelsConfig(
        access_token=SecretStr(_TOKEN),
        ig_user_id=_USER_ID,
    )
    return IGReelsPublisher(config, client=http)


@pytest.mark.unit
def test_ig_config_requires_token() -> None:
    config = IGReelsConfig(access_token=SecretStr(""), ig_user_id="123")
    with pytest.raises(AdapterError, match="access_token is required"):
        IGReelsPublisher(config)


@pytest.mark.unit
def test_ig_platform_property() -> None:
    config = IGReelsConfig(access_token=SecretStr("tok"), ig_user_id="123")
    pub = IGReelsPublisher(config)
    assert pub.platform is PublishPlatform.IG


@pytest.mark.unit
async def test_ig_publish_success() -> None:
    call_count = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal call_count
        call_count += 1
        url = str(request.url)

        if "/media_publish" in url:
            return httpx.Response(200, json={"id": "post-789"})
        if "/media" in url:
            return httpx.Response(200, json={"id": "container-456"})
        return httpx.Response(404, json={"error": "not found"})

    pub = _make_ig_publisher(handler)
    result = await pub.publish(
        video_url="https://cdn.example.com/video.mp4",
        caption="Test caption #โฆษณา",
        affiliate_link="https://s.shopee.co.th/x",
    )

    assert result.ok is True
    assert result.data is not None
    assert result.data.platform is PublishPlatform.IG
    assert result.data.platform_post_id == "post-789"
    assert result.data.media_container_id == "container-456"
    assert result.data.ig_user_id == _USER_ID
    assert call_count == 2  # create_container + publish_container


@pytest.mark.unit
async def test_ig_publish_container_failure() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"error": "something went wrong"})

    pub = _make_ig_publisher(handler)
    result = await pub.publish(
        video_url="https://cdn.example.com/video.mp4",
        caption="Test",
    )

    assert result.ok is False
    assert result.error is not None
    assert "container ID" in result.error


@pytest.mark.unit
async def test_ig_publish_api_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(400, json={"error": {"message": "Invalid token"}})

    pub = _make_ig_publisher(handler)
    result = await pub.publish(
        video_url="https://cdn.example.com/video.mp4",
        caption="Test",
    )

    assert result.ok is False
    assert result.error is not None


# --------------------------------------------------------------------- #
# dry-run publisher                                                     #
# --------------------------------------------------------------------- #


@pytest.mark.unit
async def test_dry_run_publisher_success() -> None:
    pub = DryRunPublisher()
    result = await pub.publish(
        video_url="local://test.mp4",
        caption="Test caption",
        affiliate_link="https://example.com",
    )

    assert result.ok is True
    assert result.data is not None
    assert result.data.platform is PublishPlatform.IG
    assert result.data.platform_post_id == "dry-run-1"
    assert pub.publish_count == 1


@pytest.mark.unit
async def test_dry_run_publisher_counts() -> None:
    pub = DryRunPublisher()
    for _ in range(3):
        await pub.publish(video_url="v", caption="c")

    assert pub.publish_count == 3


@pytest.mark.unit
async def test_dry_run_custom_platform() -> None:
    pub = DryRunPublisher(platform=PublishPlatform.YT)
    result = await pub.publish(video_url="v", caption="c")
    assert result.data is not None
    assert result.data.platform is PublishPlatform.YT


@pytest.mark.unit
def test_publish_record_defaults() -> None:
    record = PublishRecord(
        platform=PublishPlatform.IG,
        platform_post_id="123",
        video_url="https://example.com/v.mp4",
        caption="Test",
    )
    assert record.affiliate_link == ""
    assert record.ig_user_id == ""
    assert record.posted_at is not None
