"""Unit tests for the Phaya.io adapter — auth, parsing, jobs polling.

Uses ``httpx.MockTransport`` so no network is touched. Mirrors the pattern
of ``test_shopee_adapter.py``. These tests run without ``PHAYA_API_KEY``
because the transport is faked; the live key only matters at runtime.
"""

from __future__ import annotations

from collections.abc import Callable

import httpx
import pytest
from pydantic import SecretStr

from auto_affi.adapters.phaya import (
    JobState,
    PhayaClient,
    PhayaModel,
)
from auto_affi.exceptions import AdapterError

_FAKE_KEY = SecretStr("phaya_live_unit_test_only")


def _client(handler: Callable[[httpx.Request], httpx.Response]) -> PhayaClient:
    transport = httpx.MockTransport(handler)
    http = httpx.AsyncClient(transport=transport)
    return PhayaClient(api_key=_FAKE_KEY, client=http, max_retries=2)


@pytest.mark.unit
def test_rejects_empty_api_key() -> None:
    with pytest.raises(AdapterError, match="api_key is empty"):
        PhayaClient(api_key=SecretStr(""))


@pytest.mark.unit
def test_rejects_non_phaya_api_key() -> None:
    with pytest.raises(AdapterError, match="must start with 'phaya_'"):
        PhayaClient(api_key=SecretStr("sk-not-a-phaya-key"))


@pytest.mark.unit
async def test_chat_completion_parses_response_and_tallies_cost() -> None:
    captured: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["url"] = str(request.url)
        captured["auth"] = request.headers["Authorization"]
        captured["body"] = request.content.decode("utf-8")
        return httpx.Response(
            200,
            json={
                "choices": [
                    {"message": {"role": "assistant", "content": "สวัสดีครับ"}}
                ],
                "model": str(PhayaModel.PHAYA_GPT),
                "usage": {"prompt_tokens": 100, "completion_tokens": 50},
            },
        )

    client = _client(handler)
    result = await client.chat([{"role": "user", "content": "hello"}])

    assert result.ok is True
    assert result.data is not None
    assert result.data.content == "สวัสดีครับ"
    assert result.data.usage_in_tokens == 100
    assert result.data.usage_out_tokens == 50
    # 100 in @ $0.30/M + 50 out @ $2.50/M ≈ 0.000155
    assert 0.00014 < result.data.cost_usd < 0.00017
    assert captured["auth"] == "Bearer phaya_live_unit_test_only"
    assert "phaya.io/api/v1/chat/completions" in str(captured["url"])


@pytest.mark.unit
async def test_embeddings_returns_vectors_with_token_cost() -> None:
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "data": [
                    {"embedding": [0.1, 0.2, 0.3]},
                    {"embedding": [0.4, 0.5, 0.6]},
                ],
                "model": str(PhayaModel.PHAYA_EMBEDDING),
                "usage": {"total_tokens": 42},
            },
        )

    client = _client(handler)
    result = await client.embed(["เซรั่ม", "ครีมกันแดด"])

    assert result.ok is True
    assert result.data is not None
    assert len(result.data.vectors) == 2
    assert result.data.vectors[0] == [0.1, 0.2, 0.3]
    assert result.data.usage_tokens == 42
    # 42 tok @ $0.08/M ≈ 3.36e-9
    assert 0 < result.data.cost_usd < 1e-5


@pytest.mark.unit
async def test_create_sora2_video_returns_queued_job_handle() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert "sora-2/create" in str(request.url)
        return httpx.Response(
            200, json={"job_id": "job-abc-123", "state": "queued"}
        )

    client = _client(handler)
    result = await client.create_sora2_video(
        prompt="POV oily skin Bangkok afternoon", duration_s=5
    )

    assert result.ok is True
    assert result.data is not None
    assert result.data.job_id == "job-abc-123"
    assert result.data.state is JobState.QUEUED
    # 8 credits * $0.014 = $0.112
    assert 0.10 < result.data.cost_usd < 0.13


@pytest.mark.unit
async def test_get_job_returns_completed_with_result_url() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert "/jobs/job-abc-123" in str(request.url)
        return httpx.Response(
            200,
            json={
                "state": "completed",
                "result_url": "https://cdn.phaya.io/jobs/job-abc-123.mp4",
            },
        )

    client = _client(handler)
    result = await client.get_job("job-abc-123")

    assert result.ok is True
    assert result.data is not None
    assert result.data.state is JobState.COMPLETED
    assert result.data.result_url == "https://cdn.phaya.io/jobs/job-abc-123.mp4"


@pytest.mark.unit
async def test_wait_for_job_polls_through_states_then_returns_completed() -> None:
    states = iter(["processing", "processing", "completed"])

    def handler(_request: httpx.Request) -> httpx.Response:
        state = next(states)
        body: dict[str, object] = {"state": state}
        if state == "completed":
            body["result_url"] = "https://cdn.phaya.io/out.mp4"
        return httpx.Response(200, json=body)

    client = _client(handler)
    # Tiny poll interval keeps the test fast.
    result = await client.wait_for_job("job-x", poll_interval_s=0.01, timeout_s=2.0)

    assert result.ok is True
    assert result.data is not None
    assert result.data.state is JobState.COMPLETED
    assert result.data.result_url == "https://cdn.phaya.io/out.mp4"


@pytest.mark.unit
async def test_tts_returns_audio_url_for_thai_text() -> None:
    captured: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["body"] = request.content.decode("utf-8")
        return httpx.Response(
            200,
            json={
                "audio_url": "https://cdn.phaya.io/tts/abc.mp3",
                "duration": 3.5,
            },
        )

    client = _client(handler)
    result = await client.tts(
        "แตะลิงก์ใต้คลิปได้เลยนะคะ", voice_id="th-female-energetic"
    )

    assert result.ok is True
    assert result.data is not None
    assert result.data.audio_url == "https://cdn.phaya.io/tts/abc.mp3"
    assert result.data.duration_s == 3.5
    assert "แตะลิงก์ใต้คลิป" in str(captured["body"])  # Thai round-tripped


@pytest.mark.unit
async def test_4xx_surfaces_as_adapter_error_inside_tool_result() -> None:
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(401, text='{"error":"invalid_api_key"}')

    client = _client(handler)
    result = await client.chat([{"role": "user", "content": "hi"}])

    assert result.ok is False
    assert result.error is not None
    assert "HTTP 401" in result.error
