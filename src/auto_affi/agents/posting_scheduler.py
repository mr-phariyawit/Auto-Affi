"""Posting scheduler — Wiki-driven optimal posting time (FR-PB-05).

Reads platform_norm wiki entries to determine the best posting time for
each platform and niche.  Falls back to default schedule if no wiki data.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import time

from auto_affi.wiki.entry import WikiNamespace
from auto_affi.wiki.retriever import WikiRetriever

# Default posting times by platform (Thailand local, UTC+7)
# Derived from general IG/FB/YT best-practice for Thai audiences
DEFAULT_SCHEDULES: dict[str, list[time]] = {
    "ig": [time(11, 0), time(18, 0), time(20, 0)],  # 18:00, 01:00, 03:00 UTC
    "fb": [time(12, 0), time(19, 0)],
    "yt": [time(17, 0), time(21, 0)],
}


@dataclass
class PostingScheduler:
    """Suggests optimal posting times from wiki or defaults.

    Phase 1: returns defaults or wiki-matched times.
    Phase 2: learns from actual metrics via Feedback Curator patterns.
    """

    retriever: WikiRetriever | None = None
    default_schedules: dict[str, list[time]] = field(
        default_factory=lambda: dict(DEFAULT_SCHEDULES)
    )

    def suggest_post_times(
        self,
        platform: str,
        *,
        niche: str = "beauty",
    ) -> list[time]:
        """Suggest optimal posting times for a platform + niche.

        Tries wiki retrieval first; falls back to defaults.
        """
        if self.retriever is not None:
            result = self.retriever.retrieve(
                f"optimal posting time {platform} {niche}",
                namespaces=[WikiNamespace.PLATFORM_NORM],
                top_k=3,
            )
            if result.entries:
                # Extract time hints from wiki entry payloads
                times = self._extract_times_from_entries(result.entries)
                if times:
                    return times

        # Fallback to defaults
        return self.default_schedules.get(platform, [time(12, 0)])

    def _extract_times_from_entries(self, entries: list) -> list[time]:
        """Extract posting times from wiki entry payloads."""
        times: list[time] = []
        for entry in entries:
            payload_times = entry.payload.get("optimal_times", [])
            for t in payload_times:
                if isinstance(t, str) and ":" in t:
                    parts = t.split(":")
                    try:
                        times.append(time(int(parts[0]), int(parts[1])))
                    except (ValueError, IndexError):
                        continue
        return times
