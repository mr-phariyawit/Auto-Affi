"""Registry models — pydantic shapes for products, runs, storyboard overrides."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


def _utcnow() -> datetime:
    return datetime.now(UTC)


class ProductEntry(BaseModel):
    """One row of the `products` tab.

    The full brief shape lives here so the strategist agent can build a
    `CampaignBrief` directly without consulting any hard-coded niche dict.
    """

    model_config = ConfigDict(frozen=False, extra="forbid")

    order_no: int = Field(..., ge=1, description="Monotonic 1-based order id")
    item_id: int
    shop_id: int
    url: str
    name: str
    niche: str
    sub_niche: str = ""
    persona_label: str
    persona_age_range: str = ""
    persona_pain_points: list[str] = Field(default_factory=list)
    persona_daily_context: str = ""
    angle: str
    hook_template: str = "curiosity_gap"
    cta_text: str = ""
    hypothesis: str = ""
    expected_ctr: float = 0.025
    voice_id: str = "Algenib"
    voice_tone: str = "confident-direct"
    music_genre: str = "lofi-ambient"
    music_bpm_min: int = 85
    music_bpm_max: int = 105
    price_min_thb: float = 0.0
    price_max_thb: float = 0.0
    commission_rate: float = 0.04
    status: Literal["ACTIVE", "PAUSED", "ARCHIVED"] = "ACTIVE"
    notes: str = ""
    created_at: datetime = Field(default_factory=_utcnow)


class RunEntry(BaseModel):
    """One row of the `runs` tab. Updated as the run progresses."""

    model_config = ConfigDict(frozen=False, extra="forbid")

    run_no: int = Field(..., ge=1, description="Monotonic 1-based run id within order")
    order_no: int = Field(..., ge=1)
    run_id: str = Field(..., description="Opaque uuid-like for tracing")
    started_at: datetime = Field(default_factory=_utcnow)
    ended_at: datetime | None = None
    status: Literal["IN_PROGRESS", "APPROVED", "REJECTED", "FAILED"] = "IN_PROGRESS"
    total_cost_thb: float = 0.0
    gcs_prefix: str = ""
    final_mp4_gs_uri: str = ""
    scene_count: int = 0
    last_decision: str = ""
    publish_mode: Literal["dry_run", "live"] = "dry_run"
    error: str = ""


class StoryboardSceneOverride(BaseModel):
    """One row of the `storyboards` tab — optional per-product scene override.

    If the operator wants to lock a specific scene's prompt (e.g. after one
    pattern proves out in the Wiki), the override goes here and the writers'
    room respects it before any LLM call.
    """

    model_config = ConfigDict(frozen=False, extra="forbid")

    order_no: int = Field(..., ge=1)
    scene_idx: int = Field(..., ge=0)
    purpose: str = "demonstrate"  # hook | demonstrate | agitate | social_proof | cta
    duration_s: float = 2.5
    visual_prompt: str
    dialogue_th: str = ""
    on_screen_text_th: str = ""
    shot_type: str = "medium-shot"
    movement: str = "static"
    transition_out: str = "cut"
