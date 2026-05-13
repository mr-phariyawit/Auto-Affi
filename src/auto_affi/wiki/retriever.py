"""Wiki retriever for RAG integration (FR-ST-02).

Provides in-memory retrieval of WikiEntry objects by namespace and
text similarity.  Phase 1 uses simple keyword matching (no pgvector).
Phase 2+ swaps in pgvector-backed semantic retrieval.

The Strategist agent queries this before reasoning to inject canonical
rules, audience personas, and anti-patterns as context.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field

from auto_affi.wiki.entry import WikiEntry, WikiNamespace, WikiTier


@dataclass
class RetrievalResult:
    """Result of a wiki retrieval query."""

    entries: list[WikiEntry]
    query: str
    namespaces_searched: list[WikiNamespace]
    total_candidates: int


@dataclass
class WikiRetriever:
    """In-memory wiki retriever for Phase 1 RAG.

    Stores entries and retrieves by namespace + keyword overlap.
    Filters out Deprecated entries (SPEC 5.2).
    """

    _entries: list[WikiEntry] = field(default_factory=list)

    def add(self, entry: WikiEntry) -> None:
        """Add a wiki entry to the retriever's store."""
        self._entries.append(entry)

    def add_many(self, entries: Sequence[WikiEntry]) -> None:
        """Add multiple wiki entries at once."""
        self._entries.extend(entries)

    @property
    def entry_count(self) -> int:
        return len(self._entries)

    def retrieve(
        self,
        query: str,
        *,
        namespaces: Sequence[WikiNamespace] | None = None,
        top_k: int = 10,
        include_tiers: Sequence[WikiTier] | None = None,
    ) -> RetrievalResult:
        """Retrieve wiki entries matching the query.

        Args:
            query: Search text (matched against title + summary + tags).
            namespaces: Filter to these namespaces. None = all namespaces.
            top_k: Maximum entries to return.
            include_tiers: Only include these tiers. Default = all except
                           Deprecated (per SPEC 5.2).

        Returns:
            RetrievalResult with ranked entries.
        """
        tiers = set(include_tiers or [WikiTier.HYPOTHESIS, WikiTier.VALIDATED, WikiTier.CANONICAL])
        ns_filter = set(namespaces) if namespaces else set(WikiNamespace)

        candidates = [
            e for e in self._entries
            if e.namespace in ns_filter and e.tier in tiers
        ]
        total_candidates = len(candidates)

        # Phase 1: simple keyword overlap scoring
        query_tokens = set(query.lower().split())
        scored: list[tuple[float, WikiEntry]] = []
        for entry in candidates:
            score = self._score(entry, query_tokens)
            if score > 0:
                scored.append((score, entry))

        # Sort by score descending, then by tier priority (Canonical > Validated > Hypothesis)
        tier_priority = {
            WikiTier.CANONICAL: 3,
            WikiTier.VALIDATED: 2,
            WikiTier.HYPOTHESIS: 1,
        }
        scored.sort(
            key=lambda x: (x[0], tier_priority.get(x[1].tier, 0)),
            reverse=True,
        )

        # If no keyword matches, return all candidates sorted by tier
        if not scored and candidates:
            candidates.sort(
                key=lambda e: tier_priority.get(e.tier, 0),
                reverse=True,
            )
            return RetrievalResult(
                entries=candidates[:top_k],
                query=query,
                namespaces_searched=list(ns_filter),
                total_candidates=total_candidates,
            )

        return RetrievalResult(
            entries=[entry for _, entry in scored[:top_k]],
            query=query,
            namespaces_searched=list(ns_filter),
            total_candidates=total_candidates,
        )

    def _score(self, entry: WikiEntry, query_tokens: set[str]) -> float:
        """Score an entry against query tokens via keyword overlap."""
        entry_text = f"{entry.title} {entry.summary} {' '.join(entry.tags)}".lower()
        entry_tokens = set(entry_text.split())
        overlap = query_tokens & entry_tokens
        if not overlap:
            return 0.0
        return len(overlap) / max(len(query_tokens), 1)
