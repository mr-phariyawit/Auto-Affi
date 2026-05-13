"""Unit tests for the Phaya.io adapter — auth, parsing, jobs polling.

Uses ``httpx.MockTransport`` so no network is touched. Response shapes
mirror live probes against api.phaya.io captured 2026-05-13.
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

_FAKE_KEY = SecretStr("pk_test_unit_only_xxxxxxxxxx")


def _client(handler: Callable[[httpx.Request], httpx.Response]) -> PhayaClient:
    transport = httpx.MockTransport(handler)
    http = httpx.AsyncClient(transport=transport)
    return PhayaClient(api_key=_FAKE_KEY, client=http, max_retries=2)


@pytest.mark.unit
def test_rejects_empty_api_key() -> None:
    with pytest.raises(AdapterError, match="api_key is empty"):
        PhayaClient(api_key=SecretStr(""))


@pytest.mark.unit
def test_rejects_unknown_prefix() -> None:
    with pytest.raises(AdapterError, match="must start with"):
        PhayaClient(api_key=SecretStr("nope-not-a-phaya-key"))


@pytest.mark.unit
def test_accepts_pk_prefix() -> None:
    PhayaClient(api_key=SecretStr("pk_test_abc12345"))


@pytest.mark.unit
def test_accepts_phaya_prefix() -> None:
    PhayaClient(api_key=SecretStr("phaya_live_abc12345"))


@pytest.mark.unit
async def test_get_credits_parses_balance_and_converts_to_usd() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert "/api/v1/user/profile" in str(request.url)
        assert request.headers["Authorization"].startswith("Bearer pk_test_")
        return httpx.Response(
            200,
            json={
                "success": True,
                "user_id": "uuid-test",
                "email": "test@example.com",
                "credits_balance": 150.0,
            },
        )

    client = _client(handler)
    result = await client.get_credits()
    assert result.ok is True
    assert result.data is not None
    assert result.data.balance_thb == 150.0
    # 150 THB * 0.028 USD/THB = 4.20 USD
    assert 4.15 < result.data.balance_usd < 4.25


@pytest.mark.unit
async def test_chat_parses_message_content_and_uses_credits_thb_as_cost() -> None:
    captured: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["url"] = str(request.url)
        captured["body"] = request.content.decode("utf-8")
        return httpx.Response(
            200,
            json={
                "success": True,
                "id": "gen-test",
                "model": "Phaya-GPT",
                "message": {"role": "assistant", "content": "สวัสดีครับ"},
                "usage": {"prompt_tokens": 11, "completion_tokens": 4, "total_tokens": 15},
                "credits_used": 0.000466,  # THB
                "finish_reason": "stop",
            },
        )

    client = _client(handler)
    result = await client.chat([{"role": "user", "content": "ทักทาย"}], max_tokens=30)

    assert result.ok is True
    assert result.data is not None
    assert result.data.content == "สวัสดีครับ"
    assert result.data.usage_in_tokens == 11
    assert result.data.usage_out_tokens == 4
    assert result.data.cost_thb == pytest.approx(0.000466, rel=1e-3)
    # USD = THB * 0.028, rounded to 6 decimals (micro-cents precision)
    assert result.data.cost_usd == round(0.000466 * 0.028, 6)
    assert "/api/v1/phaya-gpt/chat/completions" in str(captured["url"])


@pytest.mark.unit
async def test_embed_parses_data_embedding_4096_dim_shape() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert "/api/v1/embedding/create" in str(request.url)
        body_str = request.content.decode("utf-8")
        assert "เซรั่ม" in body_str
        return httpx.Response(
            200,
            json={
                "success": True,
                "id": "gen-emb-test",
                "model": "Phaya Text Embedding",
                "usage": {"prompt_tokens": 6, "total_tokens": 6},
                "credits_used": 1.68e-05,  # THB
                "data": [{"embedding": [0.1] * 4096}],
            },
        )

    client = _client(handler)
    result = await client.embed(["เซรั่ม"])

    assert result.ok is True
    assert result.data is not None
    assert len(result.data.vectors) == 1
    assert len(result.data.vectors[0]) == 4096  # confirms shape contract
    assert result.data.usage_tokens == 6
    assert result.data.cost_thb == pytest.approx(1.68e-05, rel=1e-3)


@pytest.mark.unit
async def test_create_sora2_uses_n_frames_and_aspect_ratio_9_16() -> None:
    captured: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["url"] = str(request.url)
        captured["body"] = request.content.decode("utf-8")
        return httpx.Response(
            200,
            json={"job_id": "sora-job-1", "state": "queued", "credits_used": 0.0},
        )

    client = _client(handler)
    result = await client.create_sora2_video(
        prompt="POV oily-skin Bangkok afternoon", n_frames=120
    )
    assert result.ok is True
    assert result.data is not None
    assert result.data.job_id == "sora-job-1"
    assert result.data.state is JobState.QUEUED
    assert "/api/v1/sora2-text-to-video/create" in str(captured["url"])
    body = str(captured["body"])
    assert '"n_frames":120' in body
    assert '"aspect_ratio":"9:16"' in body
    assert '"remove_watermark":true' in body


@pytest.mark.unit
async def test_get_sora2_status_completed_returns_result_url() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert "/api/v1/sora2-text-to-video/status/sora-job-1" in str(request.url)
        return httpx.Response(
            200,
            json={
                "state": "completed",
                "result_url": "https://cdn.phaya.io/sora/sora-job-1.mp4",
                "credits_used": 25.0,
            },
        )

    client = _client(handler)
    result = await client.get_sora2_status("sora-job-1")
    assert result.ok is True
    assert result.data is not None
    assert result.data.state is JobState.COMPLETED
    assert result.data.result_url == "https://cdn.phaya.io/sora/sora-job-1.mp4"
    assert result.data.cost_thb == 25.0


@pytest.mark.unit
async def test_wait_for_sora2_polls_until_completed() -> None:
    states = iter(["processing", "processing", "completed"])

    def handler(_request: httpx.Request) -> httpx.Response:
        state = next(states)
        body: dict[str, object] = {"state": state}
        if state == "completed":
            body["result_url"] = "https://cdn.phaya.io/out.mp4"
            body["credits_used"] = 25.0
        return httpx.Response(200, json=body)

    client = _client(handler)
    result = await client.wait_for_sora2(
        "sora-job-1", poll_interval_s=0.01, timeout_s=2.0
    )
    assert result.ok is True
    assert result.data is not None
    assert result.data.state is JobState.COMPLETED


@pytest.mark.unit
async def test_tts_submits_with_thai_voice_and_language() -> None:
    captured: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["url"] = str(request.url)
        captured["body"] = request.content.decode("utf-8")
        return httpx.Response(
            200, json={"job_id": "tts-1", "state": "queued"}
        )

    client = _client(handler)
    result = await client.create_tts(
        "แตะลิงก์ใต้คลิป", voice="Algenib", language="th"
    )
    assert result.ok is True
    assert result.data is not None
    assert result.data.job_id == "tts-1"
    assert "/api/v1/text-to-speech/generate" in str(captured["url"])
    body = str(captured["body"])
    assert "แตะลิงก์ใต้คลิป" in body
    assert '"voice":"Algenib"' in body
    assert '"language":"th"' in body


@pytest.mark.unit
async def test_4xx_surfaces_as_adapter_error_inside_tool_result() -> None:
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(401, text='{"error":"invalid_api_key"}')

    client = _client(handler)
    result = await client.chat([{"role": "user", "content": "hi"}])
    assert result.ok is False
    assert result.error is not None
    assert "HTTP 401" in result.error
