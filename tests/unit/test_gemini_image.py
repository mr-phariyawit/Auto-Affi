"""Unit tests for the Gemini image adapter — HTTP mocked, no real API spend."""

from __future__ import annotations

import base64
from pathlib import Path

import httpx
import pytest
from pydantic import SecretStr

from auto_affi.adapters.gemini_image import (
    GEMINI_NANO_BANANA_PRO,
    GeminiImageClient,
    GeminiImageResult,
    write_image_to_path,
)


# Tiny 1×1 PNG bytes (valid file)
_TINY_PNG = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
    b"\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\rIDATx\x9cc\xfc\x0f"
    b"\x00\x00\x01\x01\x01\x00\x18\xdd\x8d\xb0\x00\x00\x00\x00IEND\xaeB`\x82"
)


def _make_client(handler) -> GeminiImageClient:
    transport = httpx.MockTransport(handler)
    return GeminiImageClient(
        api_key=SecretStr("test-key"),
        injected_client=httpx.AsyncClient(transport=transport),
    )


@pytest.mark.asyncio
async def test_create_image_success():
    img_b64 = base64.b64encode(_TINY_PNG).decode("ascii")

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={
            "candidates": [{
                "content": {
                    "parts": [
                        {"text": "Here's the image"},
                        {"inline_data": {"mime_type": "image/png", "data": img_b64}},
                    ]
                }
            }],
            "usageMetadata": {"promptTokenCount": 100, "candidatesTokenCount": 200},
        })

    client = _make_client(handler)
    r = await client.create_image("A studio portrait of a cat", aspect_ratio="9:16")
    assert r.ok
    assert r.data is not None
    assert r.data.image_bytes == _TINY_PNG
    assert r.data.mime_type == "image/png"
    assert r.data.model == GEMINI_NANO_BANANA_PRO
    assert r.data.text_commentary == "Here's the image"
    assert r.data.usage_input_tokens == 100
    assert r.data.usage_output_tokens == 200


@pytest.mark.asyncio
async def test_create_image_with_reference(tmp_path):
    ref_path = tmp_path / "ref.jpg"
    ref_path.write_bytes(_TINY_PNG)

    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        import json
        captured["body"] = json.loads(request.content)
        img_b64 = base64.b64encode(_TINY_PNG).decode("ascii")
        return httpx.Response(200, json={
            "candidates": [{"content": {"parts": [{"inline_data": {"mime_type": "image/png", "data": img_b64}}]}}]
        })

    client = _make_client(handler)
    r = await client.create_image(
        "Same character, different angle",
        aspect_ratio="9:16",
        reference_images=[ref_path],
    )
    assert r.ok
    parts = captured["body"]["contents"][0]["parts"]
    assert len(parts) == 2
    assert parts[0]["text"] == "Same character, different angle"
    assert "inline_data" in parts[1]
    assert parts[1]["inline_data"]["mime_type"] == "image/jpeg"


@pytest.mark.asyncio
async def test_create_image_bad_aspect():
    client = GeminiImageClient(api_key=SecretStr("test-key"))
    r = await client.create_image("anything", aspect_ratio="42:7")
    assert not r.ok
    assert "aspect_ratio" in r.error


@pytest.mark.asyncio
async def test_create_image_http_error():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(429, text='{"error":{"message":"prepayment credits depleted"}}')

    client = _make_client(handler)
    r = await client.create_image("anything", aspect_ratio="9:16")
    assert not r.ok
    assert "429" in r.error


@pytest.mark.asyncio
async def test_create_image_no_image_part():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={
            "candidates": [{"content": {"parts": [{"text": "I refuse"}]}}]
        })

    client = _make_client(handler)
    r = await client.create_image("anything", aspect_ratio="9:16")
    assert not r.ok
    assert "no image part" in r.error


def test_write_image_to_path(tmp_path):
    result = GeminiImageResult(
        image_bytes=_TINY_PNG, mime_type="image/png", model="test-model",
    )
    dest = tmp_path / "out" / "test.png"
    write_image_to_path(result, dest)
    assert dest.exists()
    assert dest.read_bytes() == _TINY_PNG
