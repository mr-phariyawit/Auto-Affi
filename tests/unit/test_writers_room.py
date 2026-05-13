"""Tests for the Writers' Room agent (AFFI-T-037, T-038)."""

from __future__ import annotations

import pytest

from auto_affi.agents.writers_room import (
    WritersRoom,
    create_default_storyboard,
    critic_review,
    CriticFeedback,
)
from auto_affi.schemas.campaign_brief import (
    CampaignBrief,
    CTA,
    Persona,
)
from auto_affi.schemas.storyboard import ScenePurpose


# ------------------------------------------------------------------ #
# Helpers                                                             #
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
        angle="ผิวใสใน 7 วัน",
        hook_template_slug="curiosity_gap",
        cta=CTA(text_th="แตะลิงก์เลย!", placement="pinned_comment"),
        hypothesis="Curiosity gap + before/after drives CTR for skincare",
        expected_ctr=0.03,
        confidence=0.7,
    )


# ------------------------------------------------------------------ #
# Default storyboard tests (T-037)                                     #
# ------------------------------------------------------------------ #


class TestDefaultStoryboard:
    """create_default_storyboard() output validation."""

    @pytest.mark.unit
    def test_creates_valid_storyboard(self) -> None:
        brief = _make_brief()
        sb = create_default_storyboard(brief)
        assert sb.brief_id == brief.brief_id
        assert len(sb.scenes) >= 4

    @pytest.mark.unit
    def test_hook_scene_first(self) -> None:
        sb = create_default_storyboard(_make_brief())
        assert sb.scenes[0].purpose is ScenePurpose.HOOK
        assert sb.scenes[0].duration_s <= 2.0

    @pytest.mark.unit
    def test_cta_scene_last(self) -> None:
        sb = create_default_storyboard(_make_brief())
        assert sb.scenes[-1].purpose is ScenePurpose.CTA
        assert sb.cta_scene_idx == len(sb.scenes) - 1

    @pytest.mark.unit
    def test_total_duration_under_60s(self) -> None:
        sb = create_default_storyboard(_make_brief())
        assert sb.total_duration_s <= 60.0

    @pytest.mark.unit
    def test_visual_prompts_are_detailed(self) -> None:
        sb = create_default_storyboard(_make_brief())
        for scene in sb.scenes:
            # Each prompt should be at least 50 chars (detailed, not stub)
            assert len(scene.visual_prompt) >= 50

    @pytest.mark.unit
    def test_dialogue_is_thai(self) -> None:
        sb = create_default_storyboard(_make_brief())
        for scene in sb.scenes:
            if scene.dialogue:
                # Thai text contains Thai Unicode range
                assert any(
                    "฀" <= c <= "๿" for c in scene.dialogue.text_th
                )

    @pytest.mark.unit
    def test_hyperframe_overlays_present(self) -> None:
        sb = create_default_storyboard(_make_brief())
        assert len(sb.hyperframe_overlays) >= 2

    @pytest.mark.unit
    def test_voice_profile_thai(self) -> None:
        sb = create_default_storyboard(_make_brief())
        assert sb.voice_profile.lang == "th"

    @pytest.mark.unit
    def test_affiliate_link_placement(self) -> None:
        sb = create_default_storyboard(_make_brief())
        assert "pinned_comment" in sb.affiliate_link_placement

    @pytest.mark.unit
    def test_editor_passes_all_required(self) -> None:
        sb = create_default_storyboard(_make_brief())
        from auto_affi.schemas.storyboard import REQUIRED_EDITOR_PASSES
        for p in REQUIRED_EDITOR_PASSES:
            assert p in sb.editor_passes


# ------------------------------------------------------------------ #
# Critic review tests (T-038)                                         #
# ------------------------------------------------------------------ #


class TestCriticReview:
    """critic_review() rule-based validation."""

    @pytest.mark.unit
    def test_valid_storyboard_approved(self) -> None:
        brief = _make_brief()
        sb = create_default_storyboard(brief)
        feedback = critic_review(sb, brief)
        assert feedback.approved is True
        assert len(feedback.issues) == 0

    @pytest.mark.unit
    def test_detects_duplicate_prompts(self) -> None:
        brief = _make_brief()
        sb = create_default_storyboard(brief)
        # Force duplicate
        sb.scenes[1] = sb.scenes[1].model_copy(
            update={"visual_prompt": sb.scenes[0].visual_prompt}
        )
        feedback = critic_review(sb, brief)
        assert not feedback.approved
        assert any("Duplicate" in i for i in feedback.issues)


# ------------------------------------------------------------------ #
# WritersRoom agent tests                                              #
# ------------------------------------------------------------------ #


class TestWritersRoom:
    """WritersRoom end-to-end."""

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_generate_storyboard(self) -> None:
        room = WritersRoom()
        brief = _make_brief()
        result = await room.generate_storyboard(brief)
        assert result.ok
        assert result.data is not None
        assert result.data.brief_id == brief.brief_id

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_generate_cost_zero_phase1(self) -> None:
        room = WritersRoom()
        result = await room.generate_storyboard(_make_brief())
        assert result.cost_usd == 0.0

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_disable_critic(self) -> None:
        room = WritersRoom(enable_critic=False)
        result = await room.generate_storyboard(_make_brief())
        assert result.ok
