"""Tests for LLM-driven storyboard generation (QW-8a, AFFI-T-055).

Tests the new code paths:
- _extract_json_from_text (JSON extraction from LLM responses)
- _build_user_prompt (user template formatting)
- parse_llm_storyboard (full JSON -> Storyboard parsing)
- WritersRoom.generate_storyboard with mock LLM client
- Fallback to template on LLM failure
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

import pytest

from auto_affi.agents.writers_room import (
    WritersRoom,
    _build_user_prompt,
    _extract_json_from_text,
    parse_llm_storyboard,
)
from auto_affi.schemas.campaign_brief import (
    CTA,
    CampaignBrief,
    Persona,
)
from auto_affi.schemas.storyboard import ScenePurpose
from auto_affi.schemas.tool_result import ToolResult


# ------------------------------------------------------------------ #
# Fixtures                                                            #
# ------------------------------------------------------------------ #


def _make_brief() -> CampaignBrief:
    return CampaignBrief(
        product_id=12345,
        shop_id=100,
        persona=Persona(
            label="Young Thai women",
            age_range="18-25",
            pain_points=["dry skin"],
            daily_context="scrolls IG Reels after work",
        ),
        angle="Beauty serum review",
        hook_template_slug="curiosity_gap",
        cta=CTA(text_th="แตะลิงก์เลย!", placement="pinned_comment"),
        hypothesis="Curiosity gap + before/after drives CTR for skincare",
        expected_ctr=0.03,
        confidence=0.7,
    )


def _valid_storyboard_json(brief_id: str = "test-brief-001") -> dict[str, Any]:
    """Return a valid storyboard dict that passes Pydantic validation."""
    return {
        "brief_id": brief_id,
        "voice_profile": {
            "lang": "th",
            "gender": "f",
            "tone": "energetic-confidant",
            "tts_engine": "elevenlabs",
            "voice_id": "auto",
        },
        "music_brief": {
            "genre": "lofi-pop",
            "bpm_range": [90, 110],
            "license": "epidemic-sound",
        },
        "scenes": [
            {
                "idx": 0,
                "duration_s": 1.5,
                "purpose": "hook",
                "shot_type": "extreme-closeup",
                "movement": "snap-zoom-in",
                "visual_prompt": (
                    "Extreme closeup of a glass serum bottle with golden liquid, "
                    "soft diffused studio lighting from above, warm amber tones, "
                    "shallow depth of field with bokeh, droplets on clean marble"
                ),
                "generator": "sora2",
                "dialogue": {
                    "speaker": "narrator",
                    "text_th": "สิ่งที่คุณขาดไปนานมาก...",
                    "emphasis_words": ["ขาดไป"],
                },
                "on_screen_text": {
                    "th": "ลองแล้วจะรู้!",
                    "style": "bold-pop",
                    "position": "center-upper",
                },
                "sfx": ["whoosh-01"],
                "transition_out": "match-cut",
            },
            {
                "idx": 1,
                "duration_s": 2.5,
                "purpose": "demonstrate",
                "shot_type": "medium-shot",
                "movement": "slow-dolly-right",
                "visual_prompt": (
                    "Medium shot of Thai woman applying serum on cheek, "
                    "golden hour window light from left, clean bathroom, "
                    "product texture visible on fingertips, warm skin tone"
                ),
                "generator": "sora2",
                "dialogue": {
                    "speaker": "narrator",
                    "text_th": "เนื้อเซรั่มบางเบา ซึมเร็วมาก",
                    "emphasis_words": ["บางเบา"],
                },
                "transition_out": "cut",
            },
            {
                "idx": 2,
                "duration_s": 2.0,
                "purpose": "social_proof",
                "shot_type": "medium-shot",
                "movement": "static",
                "visual_prompt": (
                    "Screenshot mockup of 5-star Shopee reviews on pink "
                    "gradient background, Thai text visible, product thumb"
                ),
                "generator": "flux",
                "dialogue": {
                    "speaker": "narrator",
                    "text_th": "รีวิว 5 ดาวจากคนจริง",
                    "emphasis_words": ["5 ดาว"],
                },
                "transition_out": "cut",
            },
            {
                "idx": 3,
                "duration_s": 2.0,
                "purpose": "cta",
                "shot_type": "medium-shot",
                "movement": "zoom-in-slow",
                "visual_prompt": (
                    "Product hero shot on white surface with golden hour side "
                    "lighting, Shopee logo badge in corner, floating price tag"
                ),
                "generator": "flux",
                "dialogue": {
                    "speaker": "narrator",
                    "text_th": "แตะลิงก์ใต้คลิปเลย!",
                    "emphasis_words": ["แตะลิงก์"],
                },
                "on_screen_text": {
                    "th": "แตะลิงก์ใต้คลิป",
                    "style": "cta-pulse",
                    "position": "center-lower",
                },
                "transition_out": "fade-out",
            },
        ],
        "cta_scene_idx": 3,
        "affiliate_link_placement": "pinned_comment + on_screen_qr",
    }


# ------------------------------------------------------------------ #
# Mock LLM client                                                     #
# ------------------------------------------------------------------ #


@dataclass
class MockChatResponse:
    content: str
    model: str = "phaya-gpt"
    usage_in_tokens: int = 100
    usage_out_tokens: int = 500
    cost_thb: float = 0.5

    @property
    def cost_usd(self) -> float:
        return self.cost_thb * 0.028


class MockPhayaClient:
    """Mock PhayaClient that returns a predetermined storyboard JSON."""

    def __init__(self, response_json: dict[str, Any] | None = None, *, fail: bool = False) -> None:
        self._response_json = response_json or _valid_storyboard_json()
        self._fail = fail
        self.call_count = 0

    async def chat(
        self,
        messages: list[dict[str, str]],
        *,
        model: str = "phaya-gpt",
        max_tokens: int | None = None,
        temperature: float | None = None,
    ) -> ToolResult[MockChatResponse]:
        self.call_count += 1
        if self._fail:
            return ToolResult(ok=False, error="Mock LLM failure")
        content = json.dumps(self._response_json, ensure_ascii=False)
        return ToolResult(
            ok=True,
            data=MockChatResponse(content=content),
            cost_usd=0.014,
        )


class MockPhayaClientBadJson:
    """Mock that returns invalid JSON."""

    async def chat(self, messages: Any, **kwargs: Any) -> ToolResult[MockChatResponse]:
        return ToolResult(
            ok=True,
            data=MockChatResponse(content="Sure! Here's your storyboard: {invalid json}"),
            cost_usd=0.01,
        )


class MockPhayaClientMarkdown:
    """Mock that returns JSON wrapped in markdown code fence."""

    def __init__(self, response_json: dict[str, Any]) -> None:
        self._response_json = response_json

    async def chat(self, messages: Any, **kwargs: Any) -> ToolResult[MockChatResponse]:
        content = f"Here's the storyboard:\n\n```json\n{json.dumps(self._response_json, ensure_ascii=False)}\n```\n\nLet me know if you need changes!"
        return ToolResult(
            ok=True,
            data=MockChatResponse(content=content),
            cost_usd=0.014,
        )


# ------------------------------------------------------------------ #
# _extract_json_from_text tests                                       #
# ------------------------------------------------------------------ #


class TestExtractJson:
    @pytest.mark.unit
    def test_bare_json(self) -> None:
        text = '{"key": "value"}'
        assert json.loads(_extract_json_from_text(text)) == {"key": "value"}

    @pytest.mark.unit
    def test_markdown_code_fence(self) -> None:
        text = 'Here is the result:\n\n```json\n{"scenes": []}\n```\n'
        assert json.loads(_extract_json_from_text(text)) == {"scenes": []}

    @pytest.mark.unit
    def test_json_with_preamble(self) -> None:
        text = 'I created a storyboard for you:\n\n{"brief_id": "x"}'
        assert json.loads(_extract_json_from_text(text)) == {"brief_id": "x"}

    @pytest.mark.unit
    def test_nested_braces(self) -> None:
        text = '{"outer": {"inner": 1}}'
        result = json.loads(_extract_json_from_text(text))
        assert result["outer"]["inner"] == 1

    @pytest.mark.unit
    def test_no_json_raises(self) -> None:
        with pytest.raises(ValueError, match="No JSON object"):
            _extract_json_from_text("No json here at all")

    @pytest.mark.unit
    def test_unbalanced_braces_raises(self) -> None:
        with pytest.raises(ValueError, match="Unbalanced braces"):
            _extract_json_from_text('{"key": "value"')


# ------------------------------------------------------------------ #
# _build_user_prompt tests                                            #
# ------------------------------------------------------------------ #


class TestBuildUserPrompt:
    @pytest.mark.unit
    def test_contains_brief_fields(self) -> None:
        brief = _make_brief()
        prompt = _build_user_prompt(brief)
        assert "12345" in prompt  # product_id
        assert "Beauty serum review" in prompt  # angle
        assert "curiosity_gap" in prompt  # hook_template
        assert "Young Thai women" in prompt  # persona label
        assert "แตะลิงก์เลย!" in prompt  # CTA text


# ------------------------------------------------------------------ #
# parse_llm_storyboard tests                                         #
# ------------------------------------------------------------------ #


class TestParseLlmStoryboard:
    @pytest.mark.unit
    def test_valid_json_parses(self) -> None:
        data = _valid_storyboard_json()
        raw = json.dumps(data, ensure_ascii=False)
        storyboard = parse_llm_storyboard(raw, brief_id="test-brief")
        assert storyboard.brief_id == "test-brief"
        assert len(storyboard.scenes) == 4
        assert storyboard.scenes[0].purpose == ScenePurpose.HOOK
        assert storyboard.scenes[-1].purpose == ScenePurpose.CTA

    @pytest.mark.unit
    def test_brief_id_overridden(self) -> None:
        data = _valid_storyboard_json(brief_id="llm-said-this")
        raw = json.dumps(data, ensure_ascii=False)
        storyboard = parse_llm_storyboard(raw, brief_id="real-brief-id")
        assert storyboard.brief_id == "real-brief-id"

    @pytest.mark.unit
    def test_markdown_wrapped_json(self) -> None:
        data = _valid_storyboard_json()
        raw = f"```json\n{json.dumps(data, ensure_ascii=False)}\n```"
        storyboard = parse_llm_storyboard(raw, brief_id="test")
        assert len(storyboard.scenes) >= 2

    @pytest.mark.unit
    def test_invalid_json_raises(self) -> None:
        with pytest.raises((ValueError, json.JSONDecodeError)):
            parse_llm_storyboard("not json at all", brief_id="test")


# ------------------------------------------------------------------ #
# WritersRoom with mock LLM tests                                     #
# ------------------------------------------------------------------ #


class TestWritersRoomLlm:
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_llm_path_generates_storyboard(self) -> None:
        mock = MockPhayaClient()
        room = WritersRoom(llm_client=mock, enable_critic=True)
        brief = _make_brief()
        result = await room.generate_storyboard(brief)
        assert result.ok is True
        assert result.data is not None
        assert len(result.data.scenes) >= 2
        assert result.data.scenes[0].purpose == ScenePurpose.HOOK
        assert mock.call_count == 1

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_llm_failure_falls_back_to_template(self) -> None:
        mock = MockPhayaClient(fail=True)
        room = WritersRoom(llm_client=mock, enable_critic=True)
        brief = _make_brief()
        result = await room.generate_storyboard(brief)
        assert result.ok is True
        assert result.data is not None
        # Template always produces 5 scenes for beauty
        assert len(result.data.scenes) == 5
        assert result.cost_usd == 0.0

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_bad_json_falls_back_to_template(self) -> None:
        mock = MockPhayaClientBadJson()
        room = WritersRoom(llm_client=mock, enable_critic=True)
        brief = _make_brief()
        result = await room.generate_storyboard(brief)
        assert result.ok is True
        assert result.data is not None
        assert len(result.data.scenes) == 5  # template

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_markdown_wrapped_response(self) -> None:
        data = _valid_storyboard_json()
        mock = MockPhayaClientMarkdown(data)
        room = WritersRoom(llm_client=mock, enable_critic=True)
        brief = _make_brief()
        result = await room.generate_storyboard(brief)
        assert result.ok is True
        assert result.data is not None
        assert len(result.data.scenes) == 4

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_no_llm_uses_template(self) -> None:
        room = WritersRoom(llm_client=None, enable_critic=True)
        brief = _make_brief()
        result = await room.generate_storyboard(brief)
        assert result.ok is True
        assert result.data is not None
        assert len(result.data.scenes) == 5  # template
        assert result.cost_usd == 0.0

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_llm_cost_propagated(self) -> None:
        mock = MockPhayaClient()
        room = WritersRoom(llm_client=mock, enable_critic=True)
        brief = _make_brief()
        result = await room.generate_storyboard(brief)
        assert result.cost_usd > 0.0

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_visual_prompts_are_detailed(self) -> None:
        """LLM-generated storyboard has detailed per-scene visual prompts."""
        mock = MockPhayaClient()
        room = WritersRoom(llm_client=mock, enable_critic=True)
        brief = _make_brief()
        result = await room.generate_storyboard(brief)
        assert result.data is not None
        for scene in result.data.scenes:
            # Each visual_prompt should be substantial (>50 chars)
            assert len(scene.visual_prompt) > 50, (
                f"Scene {scene.idx} visual_prompt too short: {scene.visual_prompt!r}"
            )
