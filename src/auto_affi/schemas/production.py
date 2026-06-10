"""Production run schemas — studio-grade approval workflow (ADR-007).

Models the 10-stage production pipeline with per-stage state machine:
DRAFT -> IN_REVIEW -> APPROVED / REVISION_PENDING / REJECTED.

A ProductionRun persists as JSON at `.aegis/brain/production/<run_id>.json`
and is indexable via the Ops Console API.
"""

from __future__ import annotations

import json
import uuid
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator

# ------------------------------------------------------------------ #
# Status enums                                                        #
# ------------------------------------------------------------------ #

class ProductionRunStatus(StrEnum):
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"


class ProductionStageStatus(StrEnum):
    DRAFT = "draft"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    REVISION_PENDING = "revision_pending"
    REJECTED = "rejected"


# ------------------------------------------------------------------ #
# Decision + Revision                                                  #
# ------------------------------------------------------------------ #

class Decision(BaseModel):
    """A board decision on a stage deliverable."""

    decided_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    verdict: Literal["approve", "revise", "reject"]
    decided_by: str = "board"
    notes_th: str | None = None


class Revision(BaseModel):
    """One iteration of a stage's deliverable."""

    revision_idx: int = Field(ge=0)
    produced_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    cost_thb: float = Field(ge=0.0, default=0.0)
    artifact: dict[str, Any] = Field(default_factory=dict)
    artifact_gs_uris: list[str] = Field(default_factory=list)
    decision: Decision | None = None


# ------------------------------------------------------------------ #
# Stage                                                                #
# ------------------------------------------------------------------ #

# Stage name constants
STAGE_NAMES: dict[int, str] = {
    1: "brief_and_concept",
    2: "script",
    3: "storyboard",
    4: "visual_references",
    5: "animatics",
    6: "voice_over",
    7: "music_and_sfx",
    8: "final_cut",
    9: "compliance",
    10: "publish",
}

STAGE_DISPLAY: dict[int, str] = {
    1: "Brief & Concept",
    2: "Script",
    3: "Storyboard",
    4: "Visual References",
    5: "Animatics (motion)",
    6: "Voice-over",
    7: "Music & SFX",
    8: "Final Cut",
    9: "Compliance",
    10: "Publish",
}

MAX_REVISIONS_PER_STAGE = 3
DEFAULT_SLA_HOURS = 24


class ProductionStage(BaseModel):
    """One of the 10 pipeline stages."""

    stage_id: int = Field(ge=1, le=10)
    name: str
    status: ProductionStageStatus = ProductionStageStatus.DRAFT
    revisions: list[Revision] = Field(default_factory=list)
    sla_deadline: datetime = Field(
        default_factory=lambda: datetime.now(UTC) + timedelta(hours=DEFAULT_SLA_HOURS)
    )

    @property
    def current_revision(self) -> Revision | None:
        return self.revisions[-1] if self.revisions else None

    @property
    def revision_count(self) -> int:
        return len(self.revisions)

    @property
    def is_past_sla(self) -> bool:
        return datetime.now(UTC) > self.sla_deadline

    @property
    def display_name(self) -> str:
        return STAGE_DISPLAY.get(self.stage_id, self.name)


# ------------------------------------------------------------------ #
# Production Run                                                       #
# ------------------------------------------------------------------ #

class ProductionRun(BaseModel):
    """A complete production run through all 10 stages."""

    run_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12])
    shopee_url: str = ""
    shopee_item_id: int = 0
    shopee_shop_id: int = 0
    started_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    status: ProductionRunStatus = ProductionRunStatus.DRAFT
    stages: list[ProductionStage] = Field(default_factory=list)
    total_cost_thb: float = Field(ge=0.0, default=0.0)
    final_mp4_gs_uri: str | None = None
    published_post_id: str | None = None

    @model_validator(mode="after")
    def _ensure_stages(self) -> ProductionRun:
        """Initialize 10 stages if empty."""
        if not self.stages:
            object.__setattr__(self, "stages", [
                ProductionStage(
                    stage_id=i,
                    name=STAGE_NAMES[i],
                )
                for i in range(1, 11)
            ])
        return self

    def get_stage(self, stage_id: int) -> ProductionStage | None:
        for s in self.stages:
            if s.stage_id == stage_id:
                return s
        return None

    @property
    def current_stage_id(self) -> int:
        """The lowest-numbered stage that is not yet APPROVED."""
        for s in self.stages:
            if s.status != ProductionStageStatus.APPROVED:
                return s.stage_id
        return 10  # all approved

    @property
    def in_review_stages(self) -> list[ProductionStage]:
        return [s for s in self.stages if s.status == ProductionStageStatus.IN_REVIEW]


# ------------------------------------------------------------------ #
# Persistence helpers                                                  #
# ------------------------------------------------------------------ #

_PRODUCTION_DIR = ".aegis/brain/production"


def _production_dir(repo_root: Path | None = None) -> Path:
    root = repo_root or Path(".")
    d = root / _PRODUCTION_DIR
    d.mkdir(parents=True, exist_ok=True)
    return d


def to_json_path(run: ProductionRun, *, repo_root: Path | None = None) -> Path:
    """Persist a ProductionRun to JSON. Returns the file path.

    Uses atomic write (write to temp + rename) to prevent corruption
    on crash mid-write (Loki review REVISE #4).
    """
    d = _production_dir(repo_root)
    path = d / f"{run.run_id}.json"
    tmp_path = d / f".{run.run_id}.json.tmp"
    tmp_path.write_text(run.model_dump_json(indent=2), encoding="utf-8")
    tmp_path.rename(path)
    return path


def from_json_path(path: Path) -> ProductionRun:
    """Load a ProductionRun from a JSON file."""
    data = json.loads(path.read_text(encoding="utf-8"))
    return ProductionRun.model_validate(data)


def list_runs(
    *,
    repo_root: Path | None = None,
    status_filter: ProductionRunStatus | None = None,
) -> list[ProductionRun]:
    """List all persisted production runs, optionally filtered by status."""
    d = _production_dir(repo_root)
    runs: list[ProductionRun] = []
    for f in sorted(d.glob("*.json")):
        try:
            run = from_json_path(f)
            if status_filter is None or run.status == status_filter:
                runs.append(run)
        except (json.JSONDecodeError, ValueError):
            continue
    return runs
