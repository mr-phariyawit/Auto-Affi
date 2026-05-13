"""Tests for workflow handlers + chain execution (AFFI-T-035)."""

from __future__ import annotations

import pytest

from auto_affi.agents.analytics_collector import (
    AnalyticsCollector,
    DryRunMetricsTransport,
)
from auto_affi.agents.feedback_curator import FeedbackCurator, OutcomeRecord
from auto_affi.schemas.metrics import OutcomeLabel, PollSchedule
from auto_affi.wiki.review_queue import ReviewQueue
from auto_affi.wiki.tier_promoter import TierPromoter
from auto_affi.workflows.executor import InProcessExecutor
from auto_affi.workflows.handlers import (
    build_learning_workflow,
    build_metrics_poll_workflow,
    make_analytics_rollup_handler,
    make_curator_handler,
    make_label_outcome_handler,
    make_poll_metrics_handler,
    make_tier_promotion_handler,
)


# ------------------------------------------------------------------ #
# MetricsPollWorkflow tests                                            #
# ------------------------------------------------------------------ #


class TestMetricsPollWorkflow:
    """MetricsPollWorkflow: poll -> label."""

    @pytest.mark.unit
    def test_dag_structure(self) -> None:
        dag = build_metrics_poll_workflow(
            publish_record_id="pub-001", run_id="r1"
        )
        assert dag.name == "MetricsPollWorkflow"
        assert len(dag.steps) == 2
        order = [s.name for s in dag.execution_order()]
        assert order == ["poll_metrics", "label_outcome"]

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_full_metrics_chain(self) -> None:
        transport = DryRunMetricsTransport(base_views=20_000, base_ctr=0.03)
        collector = AnalyticsCollector(transport=transport)

        executor = InProcessExecutor()
        executor.register(
            "poll_metrics_handler",
            make_poll_metrics_handler(collector, "pub-001", PollSchedule.DAY_7),
        )
        executor.register(
            "label_outcome_handler",
            make_label_outcome_handler(collector, "pub-001"),
        )

        dag = build_metrics_poll_workflow(
            publish_record_id="pub-001", run_id="test"
        )
        result = await executor.execute(dag)
        assert result.success
        assert result.step_results["label_outcome"]["outcome"] == "hit"


# ------------------------------------------------------------------ #
# LearningWorkflow tests                                               #
# ------------------------------------------------------------------ #


class TestLearningWorkflow:
    """LearningWorkflow: rollup -> curator -> tier promotion."""

    @pytest.mark.unit
    def test_dag_structure(self) -> None:
        dag = build_learning_workflow(run_id="r1")
        assert dag.name == "LearningWorkflow"
        assert len(dag.steps) == 3
        order = [s.name for s in dag.execution_order()]
        assert order == ["analytics_rollup", "curator", "tier_promotion"]

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_full_learning_chain(self) -> None:
        queue = ReviewQueue()
        curator = FeedbackCurator(review_queue=queue)
        promoter = TierPromoter()

        # Create enough outcomes for the curator to find patterns
        outcomes = [
            OutcomeRecord(
                video_id=f"v{i}",
                publish_record_id=f"pub-{i}",
                outcome=OutcomeLabel.HIT,
                views=15000,
                hook_template_slug="curiosity_gap",
            )
            for i in range(5)
        ] + [
            OutcomeRecord(
                video_id=f"f{i}",
                publish_record_id=f"pub-f{i}",
                outcome=OutcomeLabel.FLOP,
                views=100,
                hook_template_slug="talking_head",
            )
            for i in range(5)
        ]

        executor = InProcessExecutor()
        executor.register(
            "analytics_rollup_handler",
            make_analytics_rollup_handler(outcomes),
        )
        executor.register("curator_handler", make_curator_handler(curator))
        executor.register(
            "tier_promotion_handler",
            make_tier_promotion_handler(queue, promoter),
        )

        dag = build_learning_workflow(run_id="test")
        result = await executor.execute(dag)
        assert result.success
        assert result.step_results["analytics_rollup"]["count"] == 10
        assert result.step_results["curator"]["entries_created"] >= 1

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_learning_chain_empty_outcomes(self) -> None:
        queue = ReviewQueue()
        curator = FeedbackCurator(review_queue=queue)
        promoter = TierPromoter()

        executor = InProcessExecutor()
        executor.register(
            "analytics_rollup_handler",
            make_analytics_rollup_handler([]),
        )
        executor.register("curator_handler", make_curator_handler(curator))
        executor.register(
            "tier_promotion_handler",
            make_tier_promotion_handler(queue, promoter),
        )

        dag = build_learning_workflow(run_id="empty")
        result = await executor.execute(dag)
        assert result.success
        assert result.step_results["curator"]["entries_created"] == 0

    @pytest.mark.unit
    def test_learning_workflow_metadata(self) -> None:
        dag = build_learning_workflow(run_id="r1")
        assert dag.metadata["cron"] == "0 2 * * *"
