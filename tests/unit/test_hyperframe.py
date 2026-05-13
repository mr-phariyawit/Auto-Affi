"""Tests for Hyperframe overlay generation (AFFI-T-041)."""

from __future__ import annotations

import pytest

from auto_affi.agents.writers_room import create_default_storyboard
from auto_affi.pipeline.hyperframe import HyperframeRenderer, OverlaySpec
from auto_affi.schemas.campaign_brief import CampaignBrief, CTA, Persona


def _make_brief() -> CampaignBrief:
    return CampaignBrief(
        product_id=12345,
        shop_id=100,
        persona=Persona(
            label="Young Thai women",
            age_range="18-25",
            pain_points=["dry skin"],
            daily_context="scrolls IG Reels",
        ),
        angle="test angle",
        hook_template_slug="curiosity_gap",
        cta=CTA(text_th="test CTA", placement="pinned_comment"),
        hypothesis="test hypothesis",
        expected_ctr=0.03,
        confidence=0.7,
    )


class TestHyperframeRenderer:
    """Hyperframe overlay generation."""

    @pytest.mark.unit
    def test_generates_overlays_from_storyboard(self) -> None:
        renderer = HyperframeRenderer()
        sb = create_default_storyboard(_make_brief())
        specs = renderer.generate_overlays(sb)
        assert len(specs) > 0
        assert renderer.overlay_count == len(specs)

    @pytest.mark.unit
    def test_includes_storyboard_overlays(self) -> None:
        renderer = HyperframeRenderer()
        sb = create_default_storyboard(_make_brief())
        specs = renderer.generate_overlays(sb)
        templates = [s.template for s in specs]
        assert "snap_title_v2" in templates
        assert "cta_pulse" in templates

    @pytest.mark.unit
    def test_includes_watermark_per_scene(self) -> None:
        renderer = HyperframeRenderer()
        sb = create_default_storyboard(_make_brief())
        specs = renderer.generate_overlays(sb)
        watermarks = [s for s in specs if s.layer == "watermark"]
        assert len(watermarks) == len(sb.scenes)

    @pytest.mark.unit
    def test_watermark_opacity(self) -> None:
        renderer = HyperframeRenderer()
        sb = create_default_storyboard(_make_brief())
        specs = renderer.generate_overlays(sb)
        watermarks = [s for s in specs if s.layer == "watermark"]
        assert all(w.opacity == 0.3 for w in watermarks)

    @pytest.mark.unit
    def test_overlay_spec_validation(self) -> None:
        spec = OverlaySpec(
            scene_idx=0,
            template="test",
            opacity=0.5,
            duration_s=2.0,
        )
        assert spec.opacity == 0.5

    @pytest.mark.unit
    def test_overlay_spec_rejects_invalid_opacity(self) -> None:
        with pytest.raises(ValueError):
            OverlaySpec(
                scene_idx=0,
                template="test",
                opacity=1.5,
            )
