"""Workflow activity handlers (FR-OR-01).

Bridges workflow DAG steps to actual agent calls. Each handler receives
a context dict (piped from prior steps) and returns a result that feeds
the next step.

Phase 1: in-process calls to existing agent classes.
Phase 2+: Temporal activity implementations.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from auto_affi.agents.analytics_collector import (
    AnalyticsCollector,
)
from auto_affi.agents.feedback_curator import FeedbackCurator, OutcomeRecord
from auto_affi.schemas.metrics import PollSchedule
from auto_affi.wiki.review_queue import ReviewQueue
from auto_affi.wiki.tier_promoter import TierPromoter
from auto_affi.workflows.definitions import (
    ActivityStep,
    WorkflowDAG,
)

# ------------------------------------------------------------------ #
# Metrics + Learning workflow DAG factories                            #
# ------------------------------------------------------------------ #

def build_metrics_poll_workflow(
    *,
    publish_record_id: str = "",
    run_id: str = "",
) -> WorkflowDAG:
    """Build MetricsPollWorkflow DAG.

    Polls metrics at all 5 schedule intervals for a published video.
    Runs: 1h after publish, then 6h, 24h, 7d, 30d.
    """
    return WorkflowDAG(
        name="MetricsPollWorkflow",
        steps=[
            ActivityStep(
                name="poll_metrics",
                handler_name="poll_metrics_handler",
                timeout_s=60.0,
                idempotency_key=f"poll-{publish_record_id}-{run_id}",
            ),
            ActivityStep(
                name="label_outcome",
                handler_name="label_outcome_handler",
                timeout_s=30.0,
                idempotency_key=f"label-{publish_record_id}-{run_id}",
                depends_on=["poll_metrics"],
            ),
        ],
        metadata={
            "publish_record_id": publish_record_id,
            "run_id": run_id,
        },
    )


def build_learning_workflow(*, run_id: str = "") -> WorkflowDAG:
    """Build LearningWorkflow DAG.

    Pipeline: analytics rollup -> curator -> tier promotion.
    Cron: nightly.
    """
    return WorkflowDAG(
        name="LearningWorkflow",
        steps=[
            ActivityStep(
                name="analytics_rollup",
                handler_name="analytics_rollup_handler",
                timeout_s=120.0,
                idempotency_key=f"rollup-{run_id}",
            ),
            ActivityStep(
                name="curator",
                handler_name="curator_handler",
                timeout_s=300.0,
                idempotency_key=f"curator-{run_id}",
                depends_on=["analytics_rollup"],
            ),
            ActivityStep(
                name="tier_promotion",
                handler_name="tier_promotion_handler",
                timeout_s=60.0,
                idempotency_key=f"tier-{run_id}",
                depends_on=["curator"],
            ),
        ],
        metadata={"cron": "0 2 * * *", "run_id": run_id},
    )


# ------------------------------------------------------------------ #
# Handler implementations                                             #
# ------------------------------------------------------------------ #

def make_poll_metrics_handler(
    collector: AnalyticsCollector,
    publish_record_id: str,
    schedule: PollSchedule = PollSchedule.DAY_7,
) -> Any:
    """Create a poll_metrics handler bound to a specific collector."""

    async def handler(ctx: dict[str, Any]) -> dict[str, Any]:
        result = await collector.collect(publish_record_id, schedule)
        if not result.ok:
            raise RuntimeError(f"Metrics poll failed: {result.error}")
        return {
            "publish_record_id": publish_record_id,
            "snapshot": result.data,
        }

    return handler


def make_label_outcome_handler(
    collector: AnalyticsCollector,
    publish_record_id: str,
) -> Any:
    """Create a label_outcome handler that reads collector history."""

    async def handler(ctx: dict[str, Any]) -> dict[str, Any]:
        outcome = collector.get_outcome(publish_record_id)
        return {
            "publish_record_id": publish_record_id,
            "outcome": outcome.value,
        }

    return handler


def make_curator_handler(curator: FeedbackCurator) -> Any:
    """Create a curator handler that runs pattern extraction."""

    async def handler(ctx: dict[str, Any]) -> dict[str, Any]:
        outcomes: Sequence[OutcomeRecord] = ctx.get("analytics_rollup", {}).get(
            "outcomes", []
        )
        result = await curator.curate(outcomes)
        if not result.ok:
            raise RuntimeError(f"Curator failed: {result.error}")
        return {
            "entries_created": len(result.data or []),
            "cost_usd": result.cost_usd,
        }

    return handler


def make_tier_promotion_handler(
    review_queue: ReviewQueue,
    promoter: TierPromoter,
) -> Any:
    """Create a tier promotion handler that processes the review queue."""

    async def handler(ctx: dict[str, Any]) -> dict[str, Any]:
        pending = review_queue.pending()
        promoted = 0
        for item in pending:
            evaluated = promoter.evaluate(item.entry)
            if evaluated.tier is not item.entry.tier:
                review_queue.approve(
                    item.entry.slug,
                    reviewer="auto-promoter",
                    target_tier=evaluated.tier,
                )
                promoted += 1
        return {"pending_reviewed": len(pending), "promoted": promoted}

    return handler


def make_analytics_rollup_handler(
    outcomes: Sequence[OutcomeRecord],
) -> Any:
    """Create a rollup handler that passes outcomes to the curator step."""

    async def handler(ctx: dict[str, Any]) -> dict[str, Any]:
        return {"outcomes": list(outcomes), "count": len(outcomes)}

    return handler
