"""Bilateral wiki sync — review queue (FR-FB-03).

Agents write to the review queue ONLY.  Safety agent or human supervisor
promotes entries from the review queue to the canonical wiki store.
No agent ever writes directly to canonical tier.

This isolation prevents a single hallucinated pattern from corrupting
the shared knowledge base (see ADR-003).
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from datetime import UTC, datetime

from auto_affi.wiki.entry import WikiEntry, WikiTier


@dataclass
class ReviewItem:
    """An entry waiting for review + promotion decision."""

    entry: WikiEntry
    submitted_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    submitted_by: str = "feedback_curator"
    status: str = "pending"  # pending | approved | rejected
    reviewer: str | None = None
    reviewed_at: datetime | None = None
    rejection_reason: str | None = None


@dataclass
class ReviewQueue:
    """Write-only queue for wiki entries awaiting promotion.

    Guarantees bilateral sync: agents call :meth:`submit` (write path),
    only :meth:`approve` / :meth:`reject` (promote path) moves entries
    toward canonical status.
    """

    _items: list[ReviewItem] = field(default_factory=list)

    def submit(
        self,
        entry: WikiEntry,
        *,
        submitted_by: str = "feedback_curator",
    ) -> ReviewItem:
        """Submit a wiki entry for review.

        Entries start as Hypothesis tier regardless of what the submitter
        requests — the promote path decides the final tier.
        """
        # Force Hypothesis tier on submission (bilateral sync rule)
        safe_entry = entry.model_copy(update={"tier": WikiTier.HYPOTHESIS})
        item = ReviewItem(entry=safe_entry, submitted_by=submitted_by)
        self._items.append(item)
        return item

    def approve(
        self,
        slug: str,
        *,
        reviewer: str = "safety",
        target_tier: WikiTier = WikiTier.VALIDATED,
    ) -> ReviewItem | None:
        """Approve a pending entry and set its target tier.

        Only Safety agent or human supervisor should call this.
        """
        item = self._find_pending(slug)
        if item is None:
            return None

        item.status = "approved"
        item.reviewer = reviewer
        item.reviewed_at = datetime.now(UTC)
        item.entry = item.entry.model_copy(update={"tier": target_tier})
        return item

    def reject(
        self,
        slug: str,
        *,
        reviewer: str = "safety",
        reason: str = "",
    ) -> ReviewItem | None:
        """Reject a pending entry with optional reason."""
        item = self._find_pending(slug)
        if item is None:
            return None

        item.status = "rejected"
        item.reviewer = reviewer
        item.reviewed_at = datetime.now(UTC)
        item.rejection_reason = reason
        return item

    def pending(self) -> list[ReviewItem]:
        """Return all items awaiting review."""
        return [i for i in self._items if i.status == "pending"]

    def approved(self) -> list[ReviewItem]:
        """Return all approved items (ready for canonical store)."""
        return [i for i in self._items if i.status == "approved"]

    def all_items(self) -> Sequence[ReviewItem]:
        """Return all items in the queue."""
        return list(self._items)

    def _find_pending(self, slug: str) -> ReviewItem | None:
        for item in self._items:
            if item.entry.slug == slug and item.status == "pending":
                return item
        return None
