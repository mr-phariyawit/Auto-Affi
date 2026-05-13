"""Feedback Curator agent (FR-FB-01, FR-FB-03).

Runs nightly batch: compares win cohort (top 20%) vs fail cohort
(bottom 20%) from outcome labels, extracts structured patterns, and
writes WikiEntry objects to the review queue.

Implements bilateral wiki sync write path: agents write to the review
queue ONLY, never directly to canonical (see ADR-003).
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field

from auto_affi.schemas.metrics import OutcomeLabel
from auto_affi.schemas.tool_result import ToolResult
from auto_affi.wiki.entry import WikiEntry, WikiNamespace, WikiTier
from auto_affi.wiki.review_queue import ReviewQueue

# ------------------------------------------------------------------ #
# Outcome record — input to the Curator                               #
# ------------------------------------------------------------------ #

@dataclass(frozen=True, slots=True)
class OutcomeRecord:
    """A video's final outcome with its brief metadata for pattern mining."""

    video_id: str
    publish_record_id: str
    outcome: OutcomeLabel
    views: int = 0
    ctr: float = 0.0
    gmv_thb: float = 0.0
    hook_template_slug: str = ""
    product_category: str = ""
    angle: str = ""
    persona_label: str = ""
    posted_hour: int = 0  # 0-23 UTC


# ------------------------------------------------------------------ #
# Pattern extraction                                                  #
# ------------------------------------------------------------------ #

@dataclass(frozen=True, slots=True)
class ExtractedPattern:
    """A structured insight from win/fail cohort comparison."""

    slug: str
    namespace: WikiNamespace
    title: str
    summary: str
    evidence_ids: list[str]
    confidence: float  # 0.0 - 1.0


def split_cohorts(
    records: Sequence[OutcomeRecord],
    *,
    win_pct: float = 0.20,
    fail_pct: float = 0.20,
) -> tuple[list[OutcomeRecord], list[OutcomeRecord]]:
    """Split records into win (top N%) and fail (bottom N%) cohorts.

    Breakout/hit go to win cohort, flop/banned go to fail cohort.
    Neutral is excluded from both.  Within each cohort, we keep up to
    ``pct * total_records`` entries (minimum 2 when available, so
    pattern extraction has enough signal).
    """
    wins = [
        r for r in records
        if r.outcome in (OutcomeLabel.BREAKOUT, OutcomeLabel.HIT)
    ]
    fails = [
        r for r in records
        if r.outcome in (OutcomeLabel.FLOP, OutcomeLabel.BANNED)
    ]

    # Sort by views descending for wins, ascending for fails
    wins.sort(key=lambda r: r.views, reverse=True)
    fails.sort(key=lambda r: r.views)

    # Take top/bottom percentages, minimum 2 when available for pattern mining
    win_count = max(2, int(len(records) * win_pct)) if wins else 0
    fail_count = max(2, int(len(records) * fail_pct)) if fails else 0

    return wins[:win_count], fails[:fail_count]


def extract_patterns(
    wins: Sequence[OutcomeRecord],
    fails: Sequence[OutcomeRecord],
) -> list[ExtractedPattern]:
    """Extract feature differences between win and fail cohorts.

    Phase 1 implementation: simple feature frequency comparison.
    Phase 2+: LLM-assisted counterfactual + chi-squared / lift analysis.
    """
    patterns: list[ExtractedPattern] = []

    # Pattern 1: Hook template distribution
    win_hooks = _frequency(r.hook_template_slug for r in wins if r.hook_template_slug)
    fail_hooks = _frequency(r.hook_template_slug for r in fails if r.hook_template_slug)

    for hook, count in win_hooks.items():
        fail_count = fail_hooks.get(hook, 0)
        if count > fail_count and count >= 2:
            patterns.append(
                ExtractedPattern(
                    slug=f"hook-win-{hook}",
                    namespace=WikiNamespace.HOOK_PATTERN,
                    title=f"Hook template '{hook}' correlates with wins",
                    summary=(
                        f"Hook '{hook}' appeared in {count} wins vs {fail_count} fails. "
                        f"Consider prioritizing this hook style."
                    ),
                    evidence_ids=[r.video_id for r in wins if r.hook_template_slug == hook],
                    confidence=min(0.9, count / max(len(wins), 1)),
                )
            )

    for hook, count in fail_hooks.items():
        win_count = win_hooks.get(hook, 0)
        if count > win_count and count >= 2:
            patterns.append(
                ExtractedPattern(
                    slug=f"hook-fail-{hook}",
                    namespace=WikiNamespace.ANTI_PATTERN,
                    title=f"Hook template '{hook}' correlates with fails",
                    summary=(
                        f"Hook '{hook}' appeared in {count} fails vs {win_count} wins. "
                        f"Consider avoiding or revising this hook style."
                    ),
                    evidence_ids=[r.video_id for r in fails if r.hook_template_slug == hook],
                    confidence=min(0.9, count / max(len(fails), 1)),
                )
            )

    # Pattern 2: Posting time distribution
    win_hours = _frequency(str(r.posted_hour) for r in wins)
    fail_hours = _frequency(str(r.posted_hour) for r in fails)

    for hour, count in win_hours.items():
        fail_count = fail_hours.get(hour, 0)
        if count > fail_count and count >= 2:
            patterns.append(
                ExtractedPattern(
                    slug=f"time-win-hour-{hour}",
                    namespace=WikiNamespace.PLATFORM_NORM,
                    title=f"Posting at hour {hour} UTC correlates with wins",
                    summary=(
                        f"Hour {hour} appeared in {count} wins vs {fail_count} fails."
                    ),
                    evidence_ids=[r.video_id for r in wins if str(r.posted_hour) == hour],
                    confidence=min(0.7, count / max(len(wins), 1)),
                )
            )

    # Pattern 3: Product category patterns
    win_cats = _frequency(r.product_category for r in wins if r.product_category)
    fail_cats = _frequency(r.product_category for r in fails if r.product_category)

    for cat, count in win_cats.items():
        fail_count = fail_cats.get(cat, 0)
        if count > fail_count and count >= 2:
            patterns.append(
                ExtractedPattern(
                    slug=f"product-win-{cat}",
                    namespace=WikiNamespace.PRODUCT_ARCHETYPE,
                    title=f"Category '{cat}' correlates with wins",
                    summary=(
                        f"Category '{cat}' appeared in {count} wins vs {fail_count} fails."
                    ),
                    evidence_ids=[r.video_id for r in wins if r.product_category == cat],
                    confidence=min(0.8, count / max(len(wins), 1)),
                )
            )

    return patterns


def _frequency(items: ...) -> dict[str, int]:
    """Count frequency of items."""
    counts: dict[str, int] = {}
    for item in items:
        counts[item] = counts.get(item, 0) + 1
    return counts


# ------------------------------------------------------------------ #
# Feedback Curator agent                                              #
# ------------------------------------------------------------------ #

@dataclass
class FeedbackCurator:
    """Feedback Curator — extracts patterns and writes to review queue.

    Call :meth:`curate` with a batch of outcome records (typically all
    videos from the past 7 days).  The curator:
      1. Splits into win/fail cohorts
      2. Extracts structural patterns
      3. Converts patterns to WikiEntry objects
      4. Submits to the ReviewQueue (bilateral sync write path)
    """

    review_queue: ReviewQueue = field(default_factory=ReviewQueue)

    async def curate(
        self,
        outcomes: Sequence[OutcomeRecord],
    ) -> ToolResult[list[WikiEntry]]:
        """Run the curation pipeline on a batch of outcomes.

        Returns the list of WikiEntry objects submitted to the review queue.
        """
        if len(outcomes) < 2:
            return ToolResult(
                ok=True,
                data=[],
                cost_usd=0.0,
            )

        wins, fails = split_cohorts(outcomes)

        if not wins and not fails:
            return ToolResult(ok=True, data=[], cost_usd=0.0)

        patterns = extract_patterns(wins, fails)

        entries: list[WikiEntry] = []
        for pattern in patterns:
            entry = WikiEntry(
                slug=pattern.slug,
                namespace=pattern.namespace,
                tier=WikiTier.HYPOTHESIS,  # always start as hypothesis
                title=pattern.title,
                summary=pattern.summary,
                evidence_ids=pattern.evidence_ids,
                tags=["auto-extracted", f"confidence-{pattern.confidence:.2f}"],
            )
            self.review_queue.submit(entry, submitted_by="feedback_curator")
            entries.append(entry)

        return ToolResult(
            ok=True,
            data=entries,
            cost_usd=0.0,  # Phase 1: no LLM call, pure statistical
        )
