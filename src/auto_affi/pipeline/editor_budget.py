"""Editor budget cap with FFmpeg fallback (FR-VD-04).

Tracks accumulated cost for editor agent passes on a single video.
If total cost exceeds the per-video cap ($0.40), remaining passes
fall back to deterministic FFmpeg recipes instead of LLM-driven editing.

This prevents cost runaway on edge cases where the LLM needs many
retries or produces unexpectedly long tool-call chains.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Final

from pydantic import BaseModel, Field

_DEFAULT_BUDGET_USD: Final[float] = 0.40


class PassMode(StrEnum):
    """Whether a pass ran via LLM agent or deterministic FFmpeg."""

    LLM = "llm"
    FFMPEG_FALLBACK = "ffmpeg_fallback"
    SKIPPED = "skipped"


class PassCostEntry(BaseModel):
    """Cost record for a single editor pass."""

    pass_name: str
    cost_usd: float = Field(ge=0.0)
    mode: PassMode
    note: str = ""


class BudgetStatus(BaseModel):
    """Current budget state for one video's editing pipeline."""

    budget_usd: float
    spent_usd: float
    remaining_usd: float
    is_over_budget: bool
    entries: list[PassCostEntry]

    @property
    def pass_count(self) -> int:
        return len(self.entries)


@dataclass
class EditorBudgetTracker:
    """Tracks per-video editing costs and enforces the $0.40 cap.

    Usage::

        tracker = EditorBudgetTracker(budget_usd=0.40)

        if tracker.can_afford(estimated_cost=0.05):
            # Run LLM-driven pass
            tracker.record("silence_trim", cost_usd=0.05, mode=PassMode.LLM)
        else:
            # Fall back to FFmpeg recipe
            tracker.record("silence_trim", cost_usd=0.0, mode=PassMode.FFMPEG_FALLBACK)
    """

    budget_usd: float = _DEFAULT_BUDGET_USD
    _entries: list[PassCostEntry] = field(default_factory=list)

    @property
    def spent_usd(self) -> float:
        return sum(e.cost_usd for e in self._entries)

    @property
    def remaining_usd(self) -> float:
        return max(0.0, self.budget_usd - self.spent_usd)

    @property
    def is_over_budget(self) -> bool:
        return self.spent_usd >= self.budget_usd

    def can_afford(self, estimated_cost: float) -> bool:
        """Check if the estimated cost fits within the remaining budget."""
        return (self.spent_usd + estimated_cost) <= self.budget_usd

    def record(
        self,
        pass_name: str,
        *,
        cost_usd: float,
        mode: PassMode,
        note: str = "",
    ) -> PassCostEntry:
        """Record a completed pass and its cost."""
        entry = PassCostEntry(
            pass_name=pass_name,
            cost_usd=cost_usd,
            mode=mode,
            note=note,
        )
        self._entries.append(entry)
        return entry

    def status(self) -> BudgetStatus:
        """Return the current budget status snapshot."""
        return BudgetStatus(
            budget_usd=self.budget_usd,
            spent_usd=self.spent_usd,
            remaining_usd=self.remaining_usd,
            is_over_budget=self.is_over_budget,
            entries=list(self._entries),
        )

    def decide_mode(self, pass_name: str, *, llm_cost_estimate: float) -> PassMode:
        """Decide whether to use LLM or FFmpeg fallback for the next pass.

        If the LLM cost estimate would push us over budget, returns
        ``FFMPEG_FALLBACK``. Otherwise returns ``LLM``.
        """
        if self.can_afford(llm_cost_estimate):
            return PassMode.LLM
        return PassMode.FFMPEG_FALLBACK
