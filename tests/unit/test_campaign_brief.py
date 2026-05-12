"""Unit tests for CampaignBrief validation."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from auto_affi.schemas.campaign_brief import (
    CTA,
    BriefStatus,
    CampaignBrief,
    Persona,
)


def _persona() -> Persona:
    return Persona(
        label="oily-skin late-twenties",
        age_range="25-32",
        pain_points=["mid-day shine", "foundation slips"],
        daily_context="works in air-con office, scrolls TikTok at lunch",
    )


def _cta() -> CTA:
    return CTA(text_th="แตะลิงก์ใต้คลิป", placement="pinned_comment")


@pytest.mark.unit
def test_minimum_valid_brief_round_trips() -> None:
    brief = CampaignBrief(
        product_id=123,
        shop_id=999,
        persona=_persona(),
        angle="hero ingredient + 30-second demo",
        hook_template_slug="pov_self_identification",
        cta=_cta(),
        hypothesis="POV beauty hook beats demo-first by 35% completion",
        expected_ctr=0.025,
        confidence=0.72,
    )
    assert brief.status is BriefStatus.PROPOSED
    assert brief.brief_id  # auto-generated


@pytest.mark.unit
def test_implausible_ctr_rejected() -> None:
    with pytest.raises(ValidationError):
        CampaignBrief(
            product_id=1,
            shop_id=1,
            persona=_persona(),
            angle="x",
            hook_template_slug="pov_self_identification",
            cta=_cta(),
            hypothesis="y",
            expected_ctr=0.30,
            confidence=0.5,
        )


@pytest.mark.unit
def test_hook_slug_format_enforced() -> None:
    with pytest.raises(ValidationError):
        CampaignBrief(
            product_id=1,
            shop_id=1,
            persona=_persona(),
            angle="x",
            hook_template_slug="POV Self ID",  # whitespace + uppercase
            cta=_cta(),
            hypothesis="y",
            expected_ctr=0.05,
            confidence=0.5,
        )


@pytest.mark.unit
def test_persona_age_pattern() -> None:
    with pytest.raises(ValidationError):
        Persona(
            label="x",
            age_range="adult",  # not numeric range
            pain_points=["a"],
            daily_context="b",
        )
