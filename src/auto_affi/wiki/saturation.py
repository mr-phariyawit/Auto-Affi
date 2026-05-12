"""Wiki saturation checker for Scout dedup (FR-SC-04).

Before promoting a product candidate, the Scout queries the wiki to check
if the product (or its category niche) is already saturated with recent
affiliate content. The goal: reduce the candidate list by >= 30% compared
to the raw (pre-saturation-filtered) list.

Phase 1 implementation: in-memory tracking of recently promoted products.
Phase 2: pgvector similarity search + LLM Wiki query.

The saturation score is a simple counter-based signal:
  - How many times has this product been promoted in the last 7 days?
  - How many videos in this category niche were published in the last 7 days?

If the combined saturation score exceeds the threshold, the product is
flagged as "saturated" and should be deprioritized or skipped.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from typing import Final

_DEFAULT_WINDOW_DAYS: Final[int] = 7
_DEFAULT_PRODUCT_THRESHOLD: Final[int] = 3
_DEFAULT_CATEGORY_THRESHOLD: Final[int] = 10


@dataclass(frozen=True)
class SaturationResult:
    """Result of a saturation check for one product candidate."""

    product_id: int
    is_saturated: bool
    product_count_7d: int
    category_count_7d: int
    reason: str | None = None


@dataclass
class PromotionRecord:
    """Record of a product being promoted (used to track saturation)."""

    product_id: int
    category: str
    promoted_at: datetime = field(default_factory=lambda: datetime.now(UTC))


class SaturationChecker:
    """In-memory saturation tracker for Phase 1.

    Tracks recently promoted products and their categories to detect
    saturation. Production Phase 2 replaces this with pgvector queries
    against the wiki's ``product_archetype`` namespace.

    Parameters
    ----------
    product_threshold
        Max times a single product can be promoted in the window before
        it's considered saturated.
    category_threshold
        Max total promotions in a category within the window.
    window_days
        Rolling window for saturation counting.
    """

    def __init__(
        self,
        *,
        product_threshold: int = _DEFAULT_PRODUCT_THRESHOLD,
        category_threshold: int = _DEFAULT_CATEGORY_THRESHOLD,
        window_days: int = _DEFAULT_WINDOW_DAYS,
    ) -> None:
        self._product_threshold = product_threshold
        self._category_threshold = category_threshold
        self._window = timedelta(days=window_days)
        self._records: list[PromotionRecord] = []

    def record_promotion(self, product_id: int, category: str) -> None:
        """Log that a product was promoted (selected for video production)."""
        self._records.append(PromotionRecord(product_id=product_id, category=category))

    def check(
        self,
        product_id: int,
        category: str,
        *,
        now: datetime | None = None,
    ) -> SaturationResult:
        """Check if a product is saturated based on recent promotion history.

        Returns a :class:`SaturationResult` indicating whether the product
        should be deprioritized.
        """
        cutoff = (now or datetime.now(UTC)) - self._window
        recent = [r for r in self._records if r.promoted_at >= cutoff]

        product_count = sum(1 for r in recent if r.product_id == product_id)
        category_count = sum(1 for r in recent if r.category == category)

        if product_count >= self._product_threshold:
            return SaturationResult(
                product_id=product_id,
                is_saturated=True,
                product_count_7d=product_count,
                category_count_7d=category_count,
                reason=f"Product promoted {product_count}x in {self._window.days}d "
                f"(threshold: {self._product_threshold})",
            )

        if category_count >= self._category_threshold:
            return SaturationResult(
                product_id=product_id,
                is_saturated=True,
                product_count_7d=product_count,
                category_count_7d=category_count,
                reason=f"Category '{category}' has {category_count} promotions in "
                f"{self._window.days}d (threshold: {self._category_threshold})",
            )

        return SaturationResult(
            product_id=product_id,
            is_saturated=False,
            product_count_7d=product_count,
            category_count_7d=category_count,
        )

    def filter_candidates(
        self,
        candidates: list[tuple[int, str]],
        *,
        now: datetime | None = None,
    ) -> tuple[list[tuple[int, str]], list[SaturationResult]]:
        """Filter a list of (product_id, category) candidates.

        Returns:
          - accepted: candidates that are NOT saturated
          - saturated: SaturationResult for each rejected candidate

        FR-SC-04 requires the filtered list to be >= 30% smaller than the
        raw list. The caller should verify this.
        """
        accepted: list[tuple[int, str]] = []
        saturated: list[SaturationResult] = []

        for product_id, category in candidates:
            result = self.check(product_id, category, now=now)
            if result.is_saturated:
                saturated.append(result)
            else:
                accepted.append((product_id, category))

        return accepted, saturated

    def prune_old(self, *, now: datetime | None = None) -> int:
        """Remove records older than the window. Returns count removed."""
        cutoff = (now or datetime.now(UTC)) - self._window
        before = len(self._records)
        self._records = [r for r in self._records if r.promoted_at >= cutoff]
        return before - len(self._records)
