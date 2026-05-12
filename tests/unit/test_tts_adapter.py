"""Unit tests for TTS adapter whitelist and ElevenLabs config."""

from __future__ import annotations

import pytest
from pydantic import SecretStr

from auto_affi.adapters.tts import (
    ElevenLabsConfig,
    ElevenLabsTTS,
    TTSProvider,
    validate_provider,
)
from auto_affi.exceptions import AdapterError


@pytest.mark.unit
@pytest.mark.parametrize(
    ("provider_str", "expected"),
    [
        ("elevenlabs", TTSProvider.ELEVENLABS),
        ("ElevenLabs", TTSProvider.ELEVENLABS),
        ("botnoi", TTSProvider.BOTNOI),
        ("azure", TTSProvider.AZURE),
        ("espeak", TTSProvider.ESPEAK),
    ],
)
def test_validate_provider_approved(provider_str: str, expected: TTSProvider) -> None:
    assert validate_provider(provider_str) is expected


@pytest.mark.unit
@pytest.mark.parametrize("banned", ["openai", "openai_tts", "OpenAI"])
def test_validate_provider_banned(banned: str) -> None:
    with pytest.raises(AdapterError, match="BANNED"):
        validate_provider(banned)


@pytest.mark.unit
def test_validate_provider_unknown() -> None:
    with pytest.raises(AdapterError, match="Unknown TTS provider"):
        validate_provider("google_wavenet")


@pytest.mark.unit
def test_elevenlabs_config_defaults() -> None:
    config = ElevenLabsConfig(api_key=SecretStr("test-key"))
    assert config.model_id == "eleven_multilingual_v2"
    assert 0.0 <= config.stability <= 1.0
    assert 0.0 <= config.similarity_boost <= 1.0


@pytest.mark.unit
def test_elevenlabs_config_custom() -> None:
    config = ElevenLabsConfig(
        api_key=SecretStr("key"),
        voice_id="custom-voice",
        model_id="eleven_turbo_v2_5",
        stability=0.8,
        similarity_boost=0.9,
    )
    assert config.voice_id == "custom-voice"
    assert config.model_id == "eleven_turbo_v2_5"


@pytest.mark.unit
def test_elevenlabs_requires_api_key() -> None:
    config = ElevenLabsConfig(api_key=SecretStr(""))
    with pytest.raises(AdapterError, match="api_key is required"):
        ElevenLabsTTS(config)


@pytest.mark.unit
def test_elevenlabs_provider_property() -> None:
    config = ElevenLabsConfig(api_key=SecretStr("test"))
    tts = ElevenLabsTTS(config)
    assert tts.provider is TTSProvider.ELEVENLABS


@pytest.mark.unit
def test_provider_enum_values() -> None:
    assert TTSProvider.ELEVENLABS == "elevenlabs"
    assert TTSProvider.BOTNOI == "botnoi"
    assert TTSProvider.AZURE == "azure"
    assert TTSProvider.ESPEAK == "espeak"
