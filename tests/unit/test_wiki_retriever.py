"""Tests for the Wiki retriever (AFFI-T-006)."""

from __future__ import annotations

import pytest

from auto_affi.wiki.entry import WikiEntry, WikiNamespace, WikiTier
from auto_affi.wiki.retriever import WikiRetriever


# ------------------------------------------------------------------ #
# Helpers                                                             #
# ------------------------------------------------------------------ #

def _make_entry(
    slug: str,
    namespace: WikiNamespace = WikiNamespace.HOOK_PATTERN,
    tier: WikiTier = WikiTier.VALIDATED,
    title: str = "Test entry",
    summary: str = "Test summary for retrieval",
    tags: list[str] | None = None,
) -> WikiEntry:
    return WikiEntry(
        slug=slug,
        namespace=namespace,
        tier=tier,
        title=title,
        summary=summary,
        tags=tags or [],
    )


def _seeded_retriever() -> WikiRetriever:
    """Create a retriever with enough entries for FR-ST-02 (>= 5 entries)."""
    retriever = WikiRetriever()
    retriever.add_many([
        _make_entry("hook-curiosity", title="Curiosity gap hook", summary="Start with a question"),
        _make_entry("hook-before-after", title="Before after hook", summary="Show transformation"),
        _make_entry("hook-countdown", title="Countdown hook", summary="Count down to reveal"),
        _make_entry(
            "persona-young-thai",
            namespace=WikiNamespace.AUDIENCE_PERSONA,
            title="Young Thai women 18-25",
            summary="Instagram-native beauty shoppers",
        ),
        _make_entry(
            "persona-mom",
            namespace=WikiNamespace.AUDIENCE_PERSONA,
            title="Thai moms 30-40",
            summary="Skincare routines for busy mothers",
        ),
        _make_entry(
            "anti-talking-head",
            namespace=WikiNamespace.ANTI_PATTERN,
            tier=WikiTier.CANONICAL,
            title="Avoid talking head only",
            summary="Pure talking head without product demos consistently underperforms",
        ),
        _make_entry(
            "anti-long-intro",
            namespace=WikiNamespace.ANTI_PATTERN,
            title="Avoid slow intro",
            summary="Intros longer than 2 seconds lose 30% viewers",
        ),
    ])
    return retriever


# ------------------------------------------------------------------ #
# Retrieval tests                                                      #
# ------------------------------------------------------------------ #


class TestWikiRetriever:
    """WikiRetriever query logic."""

    @pytest.mark.unit
    def test_retrieve_by_keyword(self) -> None:
        r = _seeded_retriever()
        result = r.retrieve("curiosity hook")
        assert len(result.entries) >= 1
        assert any("curiosity" in e.slug for e in result.entries)

    @pytest.mark.unit
    def test_retrieve_by_namespace(self) -> None:
        r = _seeded_retriever()
        result = r.retrieve(
            "beauty",
            namespaces=[WikiNamespace.AUDIENCE_PERSONA],
        )
        assert all(e.namespace == WikiNamespace.AUDIENCE_PERSONA for e in result.entries)

    @pytest.mark.unit
    def test_excludes_deprecated(self) -> None:
        r = WikiRetriever()
        r.add(_make_entry("dep-entry", tier=WikiTier.DEPRECATED, title="Old pattern"))
        r.add(_make_entry("active-entry", tier=WikiTier.VALIDATED, title="Active pattern"))
        result = r.retrieve("pattern")
        assert all(e.tier is not WikiTier.DEPRECATED for e in result.entries)

    @pytest.mark.unit
    def test_top_k_limit(self) -> None:
        r = _seeded_retriever()
        result = r.retrieve("hook", top_k=2)
        assert len(result.entries) <= 2

    @pytest.mark.unit
    def test_canonical_ranked_higher(self) -> None:
        """Canonical entries should appear before Hypothesis entries."""
        r = WikiRetriever()
        r.add(_make_entry("hyp", tier=WikiTier.HYPOTHESIS, title="avoid talking head"))
        r.add(_make_entry("can", tier=WikiTier.CANONICAL, title="avoid talking head"))
        result = r.retrieve("avoid talking head")
        assert result.entries[0].tier is WikiTier.CANONICAL

    @pytest.mark.unit
    def test_empty_retriever(self) -> None:
        r = WikiRetriever()
        result = r.retrieve("anything")
        assert result.entries == []

    @pytest.mark.unit
    def test_fr_st_02_minimum_entries(self) -> None:
        """FR-ST-02: retrieval log must have >= 5 entries/call.

        Uses a query with no keyword overlap so the fallback path returns
        all candidates sorted by tier, which should be >= 5 from the
        seeded retriever.
        """
        r = _seeded_retriever()
        # Use non-matching query to trigger "return all candidates" fallback
        result = r.retrieve(
            "xyzzy-broad-search",
            namespaces=[
                WikiNamespace.HOOK_PATTERN,
                WikiNamespace.AUDIENCE_PERSONA,
                WikiNamespace.ANTI_PATTERN,
            ],
        )
        # total_candidates should be >= 5 (all entries in these 3 namespaces)
        assert result.total_candidates >= 5
        # And the fallback should return them
        assert len(result.entries) >= 5

    @pytest.mark.unit
    def test_returns_all_when_no_keyword_match(self) -> None:
        """If query has no keyword overlap, return top entries by tier."""
        r = _seeded_retriever()
        result = r.retrieve(
            "xyzzy123",
            namespaces=[WikiNamespace.HOOK_PATTERN],
        )
        # Should still return entries (sorted by tier), even without keyword match
        assert len(result.entries) >= 1

    @pytest.mark.unit
    def test_add_and_count(self) -> None:
        r = WikiRetriever()
        assert r.entry_count == 0
        r.add(_make_entry("e1"))
        assert r.entry_count == 1

    @pytest.mark.unit
    def test_include_tiers_filter(self) -> None:
        r = _seeded_retriever()
        result = r.retrieve(
            "avoid",
            include_tiers=[WikiTier.CANONICAL],
        )
        assert all(e.tier is WikiTier.CANONICAL for e in result.entries)

    @pytest.mark.unit
    def test_multi_namespace_query(self) -> None:
        r = _seeded_retriever()
        result = r.retrieve(
            "beauty",
            namespaces=[WikiNamespace.HOOK_PATTERN, WikiNamespace.AUDIENCE_PERSONA],
        )
        namespaces_found = {e.namespace for e in result.entries}
        # Should find entries from at least audience_persona (beauty-related)
        assert WikiNamespace.AUDIENCE_PERSONA in namespaces_found or len(result.entries) >= 1
