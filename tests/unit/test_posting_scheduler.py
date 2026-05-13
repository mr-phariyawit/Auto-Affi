"""Tests for posting scheduler (AFFI-T-018)."""

from __future__ import annotations

from datetime import time

import pytest

from auto_affi.agents.posting_scheduler import PostingScheduler
from auto_affi.wiki.entry import WikiEntry, WikiNamespace, WikiTier
from auto_affi.wiki.retriever import WikiRetriever


class TestPostingScheduler:
    """PostingScheduler with wiki and defaults."""

    @pytest.mark.unit
    def test_default_ig_schedule(self) -> None:
        scheduler = PostingScheduler()
        times = scheduler.suggest_post_times("ig")
        assert len(times) == 3
        assert time(18, 0) in times

    @pytest.mark.unit
    def test_default_fb_schedule(self) -> None:
        scheduler = PostingScheduler()
        times = scheduler.suggest_post_times("fb")
        assert len(times) == 2

    @pytest.mark.unit
    def test_default_yt_schedule(self) -> None:
        scheduler = PostingScheduler()
        times = scheduler.suggest_post_times("yt")
        assert len(times) == 2

    @pytest.mark.unit
    def test_unknown_platform_fallback(self) -> None:
        scheduler = PostingScheduler()
        times = scheduler.suggest_post_times("tiktok")
        assert len(times) == 1
        assert times[0] == time(12, 0)

    @pytest.mark.unit
    def test_wiki_driven_schedule(self) -> None:
        retriever = WikiRetriever()
        retriever.add(
            WikiEntry(
                slug="ig-optimal-time",
                namespace=WikiNamespace.PLATFORM_NORM,
                tier=WikiTier.VALIDATED,
                title="IG optimal posting time beauty",
                summary="Best times for beauty niche on IG",
                payload={"optimal_times": ["19:30", "21:00"]},
            )
        )
        scheduler = PostingScheduler(retriever=retriever)
        times = scheduler.suggest_post_times("ig", niche="beauty")
        assert time(19, 30) in times
        assert time(21, 0) in times

    @pytest.mark.unit
    def test_empty_wiki_falls_back(self) -> None:
        retriever = WikiRetriever()  # empty
        scheduler = PostingScheduler(retriever=retriever)
        times = scheduler.suggest_post_times("ig")
        assert len(times) == 3  # falls back to defaults
