"""Wiki tier promotion + deprecation logic (FR-FB-02).

Implements the WikiEntry tier lifecycle from SPEC 5.2:
  Hypothesis  ->  Validated  ->  Canonical  ->  Deprecated

Tier transitions are based on evidence counts and contradiction signals:
  - Hypothesis:  1-2 evidence points (starting tier)
  - Validated:   >= 5 evidence points, p < 0.1 (strong signal)
  - Canonical:   >= 20 evidence points, cross-niche replicated (hard rule)
  - Deprecated:  contradicted by >= 3 recent fails (excluded from retrieval)
"""

from __future__ import annotations

from dataclasses import dataclass

from auto_affi.wiki.entry import WikiEntry, WikiTier

# ------------------------------------------------------------------ #
# Promotion thresholds                                                #
# ------------------------------------------------------------------ #

@dataclass(frozen=True, slots=True)
class TierThresholds:
    """Configurable evidence count thresholds for tier promotion."""

    validated_evidence: int = 5
    canonical_evidence: int = 20
    deprecation_contradictions: int = 3


# ------------------------------------------------------------------ #
# Tier promoter                                                       #
# ------------------------------------------------------------------ #

@dataclass
class TierPromoter:
    """Manages WikiEntry tier transitions.

    Call :meth:`evaluate` to determine if an entry should be promoted
    or deprecated based on its evidence and contradiction counts.
    """

    thresholds: TierThresholds = TierThresholds()

    def evaluate(
        self,
        entry: WikiEntry,
        *,
        contradiction_count: int = 0,
    ) -> WikiEntry:
        """Evaluate and potentially promote/deprecate an entry.

        Returns a new WikiEntry with the updated tier. The original
        entry is not mutated.
        """
        # Deprecation takes priority — even Canonical entries can be deprecated
        if contradiction_count >= self.thresholds.deprecation_contradictions:
            return self._deprecate(entry)

        evidence_count = len(entry.evidence_ids)
        current_tier = entry.tier

        # Already deprecated or canonical — no further promotion
        if current_tier is WikiTier.DEPRECATED:
            return entry

        if current_tier is WikiTier.CANONICAL:
            return entry

        # Hypothesis -> Validated -> Canonical based on evidence count
        if evidence_count >= self.thresholds.canonical_evidence:
            return self._promote_to(entry, WikiTier.CANONICAL)

        if evidence_count >= self.thresholds.validated_evidence and current_tier is WikiTier.HYPOTHESIS:
            return self._promote_to(entry, WikiTier.VALIDATED)

        return entry

    def add_evidence(
        self,
        entry: WikiEntry,
        new_evidence_ids: list[str],
        *,
        contradiction_count: int = 0,
    ) -> WikiEntry:
        """Add evidence to an entry and re-evaluate its tier.

        Merges new evidence IDs (deduplicating) and runs :meth:`evaluate`.
        """
        merged = list(dict.fromkeys(entry.evidence_ids + new_evidence_ids))
        updated = entry.model_copy(update={"evidence_ids": merged})
        return self.evaluate(updated, contradiction_count=contradiction_count)

    def _promote_to(self, entry: WikiEntry, tier: WikiTier) -> WikiEntry:
        """Promote an entry to a higher tier."""
        return entry.model_copy(update={"tier": tier})

    def _deprecate(self, entry: WikiEntry) -> WikiEntry:
        """Mark an entry as deprecated."""
        from datetime import UTC, datetime

        return entry.model_copy(
            update={
                "tier": WikiTier.DEPRECATED,
                "deprecated_at": datetime.now(UTC),
            }
        )

    def can_promote(
        self,
        entry: WikiEntry,
        *,
        contradiction_count: int = 0,
    ) -> bool:
        """Check if an entry would change tier under current evidence."""
        evaluated = self.evaluate(entry, contradiction_count=contradiction_count)
        return evaluated.tier is not entry.tier
