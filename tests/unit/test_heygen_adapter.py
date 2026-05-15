"""Tests for the HeyGen Avatar IV adapter. All HTTP calls mocked via
httpx.MockTransport — no network, no spend."""

from __future__ import annotations

import asyncio
from pathlib import Path

import httpx
import pytest
from pydantic import SecretStr

from auto_affi.adapters.heygen import (
    CompletedVideo,
    HeyGenClient,
    HeyGenError,
    UploadedAsset,
    VideoJob,
)


def _client_with_transport(transport: httpx.MockTransport) -> HeyGenClient:
    """Build a HeyGenClient whose AsyncClient uses the given mock transport."""
    c = HeyGenClient(api_key=SecretStr("test-key"), timeout_s=2.0)
    # Monkey-patch httpx.AsyncClient to use our transport. The client
    # constructs a fresh AsyncClient per call, so we patch the class.
    original = httpx.AsyncClient

    class _PatchedClient(httpx.AsyncClient):  # type: ignore[misc]
        def __init__(self, **kwargs):
            kwargs["transport"] = transport
            super().__init__(**kwargs)

    httpx.AsyncClient = _PatchedClient  # type: ignore[misc]
    c._restore_async_client = lambda: setattr(httpx, "AsyncClient", original)
    return c


def _restore(client: HeyGenClient) -> None:
    fn = getattr(client, "_restore_async_client", None)
    if fn:
        fn()


def test_upload_asset_posts_multipart_and_returns_asset_id(tmp_path):
    f = tmp_path / "headshot.png"
    f.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)

    captured: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["url"] = str(request.url)
        captured["method"] = request.method
        captured["headers"] = dict(request.headers)
        captured["content_type"] = request.headers.get("content-type", "")
        return httpx.Response(200, json={"data": {
            "asset_id": "asset_abc123",
            "url": "https://files.heygen.ai/assets/asset_abc123.png",
            "mime_type": "image/png",
            "size_bytes": 108,
        }})

    transport = httpx.MockTransport(handler)
    client = _client_with_transport(transport)
    try:
        asset = asyncio.run(client.upload_asset(f))
    finally:
        _restore(client)

    assert isinstance(asset, UploadedAsset)
    assert asset.asset_id == "asset_abc123"
    assert asset.mime_type == "image/png"
    assert captured["method"] == "POST"
    assert captured["url"].endswith("/v3/assets")
    assert captured["headers"]["x-api-key"] == "test-key"
    assert "multipart/form-data" in captured["content_type"]


def test_upload_asset_missing_file_raises(tmp_path):
    client = HeyGenClient(api_key=SecretStr("k"))
    with pytest.raises(HeyGenError, match="not found"):
        asyncio.run(client.upload_asset(tmp_path / "nope.png"))


def test_upload_asset_http_error_raises(tmp_path):
    f = tmp_path / "x.png"
    f.write_bytes(b"\x00")

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(401, json={
            "error": {"code": "authentication_failed", "message": "bad key"}
        })

    transport = httpx.MockTransport(handler)
    client = _client_with_transport(transport)
    try:
        with pytest.raises(HeyGenError, match="HTTP 401"):
            asyncio.run(client.upload_asset(f))
    finally:
        _restore(client)


def test_create_video_from_image_with_audio_asset_id_builds_body():
    captured: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        import json
        captured["url"] = str(request.url)
        captured["body"] = json.loads(request.content.decode())
        return httpx.Response(200, json={"data": {
            "video_id": "v_xyz",
            "status": "waiting",
            "output_format": "mp4",
        }})

    transport = httpx.MockTransport(handler)
    client = _client_with_transport(transport)
    try:
        job = asyncio.run(client.create_video_from_image(
            image_asset_id="img_1",
            audio_asset_id="aud_1",
            aspect_ratio="9:16",
            resolution="720p",
            motion_prompt="subtle reading",
            expressiveness="medium",
        ))
    finally:
        _restore(client)

    assert isinstance(job, VideoJob)
    assert job.video_id == "v_xyz"
    assert captured["url"].endswith("/v3/videos")
    body = captured["body"]
    assert body["type"] == "image"
    assert body["image"] == {"type": "asset_id", "asset_id": "img_1"}
    assert body["audio_asset_id"] == "aud_1"
    assert body["aspect_ratio"] == "9:16"
    assert body["resolution"] == "720p"
    assert body["motion_prompt"] == "subtle reading"
    assert body["expressiveness"] == "medium"
    assert "audio_url" not in body
    assert "script" not in body


def test_create_video_from_image_with_audio_url_builds_body():
    captured: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        import json
        captured["body"] = json.loads(request.content.decode())
        return httpx.Response(200, json={"data": {
            "video_id": "v_2", "status": "waiting", "output_format": "mp4",
        }})

    transport = httpx.MockTransport(handler)
    client = _client_with_transport(transport)
    try:
        asyncio.run(client.create_video_from_image(
            image_asset_id="img_1",
            audio_url="https://example.com/a.mp3",
        ))
    finally:
        _restore(client)

    assert captured["body"]["audio_url"] == "https://example.com/a.mp3"
    assert "audio_asset_id" not in captured["body"]


def test_create_video_from_image_requires_exactly_one_audio_source():
    client = HeyGenClient(api_key=SecretStr("k"))
    with pytest.raises(HeyGenError, match="exactly one"):
        asyncio.run(client.create_video_from_image(image_asset_id="img_1"))
    with pytest.raises(HeyGenError, match="exactly one"):
        asyncio.run(client.create_video_from_image(
            image_asset_id="img_1",
            audio_asset_id="a", audio_url="https://x",
        ))


def test_wait_for_video_polls_until_completed():
    statuses = iter(["waiting", "processing", "completed"])

    def handler(request: httpx.Request) -> httpx.Response:
        status = next(statuses)
        body: dict[str, object] = {"data": {"status": status}}
        if status == "completed":
            body["data"]["video_url"] = "https://heygen.example/out.mp4"  # type: ignore[index]
            body["data"]["duration"] = 8.06  # type: ignore[index]
        return httpx.Response(200, json=body)

    transport = httpx.MockTransport(handler)
    client = _client_with_transport(transport)
    try:
        completed = asyncio.run(client.wait_for_video(
            "v_abc", interval_s=0.01, timeout_s=5.0,
        ))
    finally:
        _restore(client)

    assert isinstance(completed, CompletedVideo)
    assert completed.video_url == "https://heygen.example/out.mp4"
    assert completed.duration_s == 8.06


def test_wait_for_video_raises_on_failure():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={
            "data": {"status": "failed", "error": "render error"}
        })

    transport = httpx.MockTransport(handler)
    client = _client_with_transport(transport)
    try:
        with pytest.raises(HeyGenError, match="failed"):
            asyncio.run(client.wait_for_video(
                "v_abc", interval_s=0.01, timeout_s=2.0,
            ))
    finally:
        _restore(client)


def test_download_video_writes_to_disk(tmp_path):
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, content=b"fake-mp4-bytes")

    transport = httpx.MockTransport(handler)
    client = _client_with_transport(transport)
    dest = tmp_path / "out.mp4"
    try:
        result = asyncio.run(client.download_video(
            "https://heygen.example/out.mp4", dest,
        ))
    finally:
        _restore(client)

    assert result == dest
    assert dest.read_bytes() == b"fake-mp4-bytes"
