"""Canonical wiki store + promotion pipeline (FR-FB-03).

The WikiStore is the authoritative repository of wiki entries.
Entries reach canonical store ONLY via the promotion path
(ReviewQueue -> TierPromoter -> WikiStore).

No agent writes directly to the store — that's the bilateral
wiki sync invariant from ADR-003.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from auto_affi.wiki.entry import WikiEntry, WikiNamespace, WikiTier
from auto_affi.wiki.review_queue import ReviewQueue
from auto_affi.wiki.tier_promoter import TierPromoter


@dataclass(frozen=True, slots=True)
class PromotionRecord:
    """Audit record of a promotion/rejection decision."""

    slug: str
    action: str  # "promoted" | "rejected" | "auto-promoted"
    from_tier: WikiTier
    to_tier: WikiTier
    reviewer: str
    reason: str
    ts: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass
class WikiStore:
    """Canonical wiki entry store.

    Entries are indexed by slug. Only the promotion pipeline may add
    or update entries — direct writes are prohibited by design.
    """

    _entries: dict[str, WikiEntry] = field(default_factory=dict)
    _audit_log: list[PromotionRecord] = field(default_factory=list)

    def get(self, slug: str) -> WikiEntry | None:
        return self._entries.get(slug)

    def get_by_namespace(
        self, namespace: WikiNamespace
    ) -> list[WikiEntry]:
        return [
            e for e in self._entries.values()
            if e.namespace == namespace and e.is_active
        ]

    def get_active(self) -> list[WikiEntry]:
        return [e for e in self._entries.values() if e.is_active]

    @property
    def entry_count(self) -> int:
        return len(self._entries)

    @property
    def audit_log(self) -> list[PromotionRecord]:
        return list(self._audit_log)

    def _put(
        self,
        entry: WikiEntry,
        *,
        action: str,
        from_tier: WikiTier,
        reviewer: str,
        reason: str = "",
    ) -> None:
        """Internal: add/update an entry with audit logging."""
        self._entries[entry.slug] = entry
        self._audit_log.append(
            PromotionRecord(
                slug=entry.slug,
                action=action,
                from_tier=from_tier,
                to_tier=entry.tier,
                reviewer=reviewer,
                reason=reason,
            )
        )


def promote_from_queue(
    queue: ReviewQueue,
    store: WikiStore,
    promoter: TierPromoter,
    *,
    reviewer: str = "safety",
) -> int:
    """Process the review queue: evaluate, promote, and store.

    For each pending item:
    1. TierPromoter evaluates whether the entry's tier should change
    2. If tier changes, approve in queue and add to store
    3. If tier doesn't change, auto-approve at current (Hypothesis) tier

    Returns the count of entries added/updated in the store.
    """
    promoted = 0
    for item in list(queue.pending()):
        evaluated = promoter.evaluate(item.entry)
        from_tier = item.entry.tier

        # Approve in queue with the evaluated tier
        queue.approve(
            item.entry.slug,
            reviewer=reviewer,
            target_tier=evaluated.tier,
        )

        # Add to store
        store._put(
            evaluated,
            action="promoted" if evaluated.tier is not from_tier else "auto-promoted",
            from_tier=from_tier,
            reviewer=reviewer,
        )
        promoted += 1

    return promoted
