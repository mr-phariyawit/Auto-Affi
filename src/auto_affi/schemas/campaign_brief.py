"""CampaignBrief — Strategist output, Writers' Room input.

The brief is the single hand-off between the Strategist agent and the
Writers' Room. Every field is required so the room never has to invent
context. Schema is intentionally strict; the Strategist's prompt is
gated on producing a valid JSON instance of this model.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator


class Persona(BaseModel):
    """Target audience description used by Screenwriter + Cinematographer."""

    label: str = Field(min_length=1, max_length=80)
    age_range: str = Field(pattern=r"^\d{1,2}-\d{1,2}$")
    pain_points: list[str] = Field(min_length=1, max_length=5)
    daily_context: str = Field(min_length=1, max_length=200)


class CTA(BaseModel):
    """Single call to action. Brief enforces exactly one CTA in the video."""

    text_th: str = Field(min_length=1, max_length=80)
    placement: str = Field(min_length=1, max_length=40)


class BriefStatus(StrEnum):
    """Lifecycle state of the brief."""

    PROPOSED = "proposed"
    APPROVED = "approved"
    REJECTED = "rejected"
    PRODUCED = "produced"


class CampaignBrief(BaseModel):
    """Strategist output — the contract for the Writers' Room."""

    brief_id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    product_id: int
    shop_id: int
    persona: Persona
    angle: str = Field(min_length=1, max_length=200)
    hook_template_slug: str = Field(pattern=r"^[a-z0-9_-]+$")
    cta: CTA
    hypothesis: str = Field(min_length=1, max_length=300)
    expected_ctr: float = Field(ge=0.0, le=1.0)
    confidence: float = Field(ge=0.0, le=1.0)
    priority_boost: bool = Field(
        default=False,
        description="True when within 14 days of a Shopee mega-sale per playbook §5.4.",
    )
    wiki_evidence_slugs: list[str] = Field(default_factory=list)
    status: BriefStatus = BriefStatus.PROPOSED
    created_by_agent: str = Field(default="strategist")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @field_validator("expected_ctr")
    @classmethod
    def _ctr_must_be_realistic(cls, value: float) -> float:
        # Anything above 15% CTR almost certainly means the Strategist made up
        # an outcome from the wiki — flag at validation time rather than later.
        if value > 0.15:
            raise ValueError("expected_ctr > 15% is implausible; recheck Strategist evidence")
        return value
