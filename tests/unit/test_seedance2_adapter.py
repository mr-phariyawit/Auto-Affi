"""Tests for the Seedance 2.0 (PiAPI) adapter. All HTTP mocked via
httpx.MockTransport — no network, no spend."""

from __future__ import annotations

import asyncio
from pathlib import Path

import httpx
import pytest
from pydantic import SecretStr

from auto_affi.adapters.seedance2 import (
    Seedance2Client,
    Seedance2Error,
    Seedance2Job,
    Seedance2Result,
)


def _client_with_transport(transport: httpx.MockTransport) -> Seedance2Client:
    """Build a Seedance2Client whose AsyncClient uses the given mock transport."""
    c = Seedance2Client(api_key=SecretStr("test-key"), timeout_s=2.0)
    original = httpx.AsyncClient

    class _Patched(httpx.AsyncClient):  # type: ignore[misc]
        def __init__(self, **kwargs):
            kwargs["transport"] = transport
            super().__init__(**kwargs)

    httpx.AsyncClient = _Patched  # type: ignore[misc]
    c._restore = lambda: setattr(httpx, "AsyncClient", original)
    return c


def _restore(c: Seedance2Client) -> None:
    fn = getattr(c, "_restore", None)
    if fn:
        fn()


def test_create_first_last_frames_builds_correct_body():
    captured: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        import json
        captured["url"] = str(request.url)
        captured["method"] = request.method
        captured["headers"] = dict(request.headers)
        captured["body"] = json.loads(request.content.decode())
        return httpx.Response(200, json={"data": {
            "task_id": "task_abc123", "status": "Pending",
        }})

    transport = httpx.MockTransport(handler)
    client = _client_with_transport(transport)
    try:
        job = asyncio.run(client.create_first_last_frames(
            first_frame_url="https://example.com/start.jpg",
            last_frame_url="https://example.com/end.jpg",
            prompt="slow push-in revealing the maono microphone",
            model="seedance-2-fast",
            duration_s=4,
            resolution="720p",
            aspect_ratio="9:16",
        ))
    finally:
        _restore(client)

    assert isinstance(job, Seedance2Job)
    assert job.task_id == "task_abc123"
    assert captured["method"] == "POST"
    assert captured["url"].endswith("/api/v1/task")
    assert captured["headers"]["x-api-key"] == "test-key"
    body = captured["body"]
    assert body["model"] == "seedance-2-fast"
    assert body["task_type"] == "first_last_frames"
    assert body["input"]["first_frame_url"] == "https://example.com/start.jpg"
    assert body["input"]["last_frame_url"] == "https://example.com/end.jpg"
    assert body["input"]["prompt"].startswith("slow push-in")
    assert body["input"]["duration"] == "4"
    assert body["input"]["aspect_ratio"] == "9:16"
    assert body["input"]["resolution"] == "720p"


def test_create_first_last_frames_supports_pro_variant():
    captured: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        import json
        captured["body"] = json.loads(request.content.decode())
        return httpx.Response(200, json={"data": {
            "task_id": "task_xyz", "status": "Pending",
        }})

    transport = httpx.MockTransport(handler)
    client = _client_with_transport(transport)
    try:
        asyncio.run(client.create_first_last_frames(
            first_frame_url="https://a", last_frame_url="https://b",
            prompt="x", model="seedance-2",
            duration_s=8, resolution="1080p",
        ))
    finally:
        _restore(client)
    assert captured["body"]["model"] == "seedance-2"
    assert captured["body"]["input"]["resolution"] == "1080p"


def test_create_first_last_frames_raises_on_http_error():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(402, json={
            "error": {"code": "insufficient_credits", "message": "Need top-up"}
        })

    transport = httpx.MockTransport(handler)
    client = _client_with_transport(transport)
    try:
        with pytest.raises(Seedance2Error, match="HTTP 402"):
            asyncio.run(client.create_first_last_frames(
                first_frame_url="a", last_frame_url="b", prompt="x",
            ))
    finally:
        _restore(client)


def test_wait_for_task_polls_until_completed():
    states = iter(["Pending", "Processing", "Completed"])

    def handler(request: httpx.Request) -> httpx.Response:
        s = next(states)
        body: dict[str, object] = {"data": {"status": s}}
        if s == "Completed":
            body["data"]["output"] = {  # type: ignore[index]
                "video_url": "https://piapi.example/out.mp4",
                "duration": 4.0,
            }
        return httpx.Response(200, json=body)

    transport = httpx.MockTransport(handler)
    client = _client_with_transport(transport)
    try:
        result = asyncio.run(client.wait_for_task(
            "task_abc", interval_s=0.01, timeout_s=5.0,
        ))
    finally:
        _restore(client)

    assert isinstance(result, Seedance2Result)
    assert result.video_url == "https://piapi.example/out.mp4"
    assert result.duration_s == 4.0


def test_wait_for_task_raises_on_failed():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={
            "data": {"status": "Failed", "error": "moderation rejected"}
        })

    transport = httpx.MockTransport(handler)
    client = _client_with_transport(transport)
    try:
        with pytest.raises(Seedance2Error, match="moderation rejected"):
            asyncio.run(client.wait_for_task(
                "task_abc", interval_s=0.01, timeout_s=2.0,
            ))
    finally:
        _restore(client)


def test_wait_for_task_times_out():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"data": {"status": "Processing"}})

    transport = httpx.MockTransport(handler)
    client = _client_with_transport(transport)
    try:
        with pytest.raises(Seedance2Error, match="timed out"):
            asyncio.run(client.wait_for_task(
                "task_abc", interval_s=0.01, timeout_s=0.1,
            ))
    finally:
        _restore(client)


def test_download_video_writes_to_disk(tmp_path):
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, content=b"fake-mp4")

    transport = httpx.MockTransport(handler)
    client = _client_with_transport(transport)
    dest = tmp_path / "out.mp4"
    try:
        result = asyncio.run(client.download_video(
            "https://piapi.example/out.mp4", dest,
        ))
    finally:
        _restore(client)
    assert result == dest
    assert dest.read_bytes() == b"fake-mp4"


def test_schema_accepts_seedance_2_fast_with_keyframes():
    """AiShot validator: seedance_2_fast / seedance_2_pro must require keyframes
    block — same invariant as legacy seedance_2kf."""
    from auto_affi.schemas.ai_storyboard import (
        AiShot, AudioSource, Generator, Keyframes, NarrativeRole,
    )
    # Missing keyframes → ValueError
    with pytest.raises(ValueError, match="keyframes"):
        AiShot(
            shot_id="s0",
            narrative_role=NarrativeRole.STORY,
            duration_s=4.0,
            generator=Generator.SEEDANCE_2_FAST,
            image_prompt="a" * 30,
            consistency_seed=1,
            audio_source=AudioSource.MUSIC_ONLY,
        )

    # With keyframes → accepted
    shot = AiShot(
        shot_id="s0",
        narrative_role=NarrativeRole.STORY,
        duration_s=4.0,
        generator=Generator.SEEDANCE_2_PRO,
        image_prompt="a" * 30,
        consistency_seed=1,
        audio_source=AudioSource.MUSIC_ONLY,
        keyframes=Keyframes(start_ref="s0.jpg", end_ref="s1.jpg",
                            motion_label="slow push-in"),
    )
    assert shot.generator is Generator.SEEDANCE_2_PRO
