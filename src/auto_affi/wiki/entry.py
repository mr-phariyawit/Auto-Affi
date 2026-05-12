"""Wiki entry schema.

Every learnable artifact in the LLM Wiki is a :class:`WikiEntry` — a tagged,
tiered, retrievable note that agents read via RAG and the Feedback Curator
writes via the bilateral-sync review queue (never directly to canonical).

Tiers come from ``docs/execution-playbook.md`` §5.5:
    Hypothesis  - 1-2 supporting outcomes, injected as a tentative hint
    Validated   - >=5 supporting outcomes, p<0.1
    Canonical   - >=20 outcomes, cross-niche replicated; hard rule
    Deprecated  - contradicted by >=3 recent failures; excluded from retrieval
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class WikiTier(StrEnum):
    """Confidence tier of a wiki entry."""

    HYPOTHESIS = "hypothesis"
    VALIDATED = "validated"
    CANONICAL = "canonical"
    DEPRECATED = "deprecated"


class WikiNamespace(StrEnum):
    """Top-level namespaces that organise the wiki."""

    HOOK_PATTERN = "hook_pattern"
    PRODUCT_ARCHETYPE = "product_archetype"
    AUDIENCE_PERSONA = "audience_persona"
    FAILURE_MODE = "failure_mode"
    ANTI_PATTERN = "anti_pattern"
    PLATFORM_NORM = "platform_norm"
    COMPLIANCE_RULE = "compliance_rule"


class WikiEntry(BaseModel):
    """A retrievable wiki note."""

    slug: str = Field(min_length=1, max_length=128, pattern=r"^[a-z0-9_-]+$")
    namespace: WikiNamespace
    tier: WikiTier
    title: str = Field(min_length=1, max_length=200)
    summary: str = Field(min_length=1)
    payload: dict[str, Any] = Field(default_factory=dict)
    tags: list[str] = Field(default_factory=list)
    evidence_ids: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    deprecated_at: datetime | None = None

    @property
    def is_active(self) -> bool:
        return self.tier is not WikiTier.DEPRECATED
