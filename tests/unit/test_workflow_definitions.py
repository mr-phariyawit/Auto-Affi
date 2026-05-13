"""Tests for workflow definitions and executor (AFFI-T-034)."""

from __future__ import annotations

import pytest

from auto_affi.workflows.definitions import (
    ActivityStatus,
    ActivityStep,
    RetryPolicy,
    WorkflowDAG,
    build_campaign_workflow,
    build_discovery_workflow,
)
from auto_affi.workflows.executor import InProcessExecutor


# ------------------------------------------------------------------ #
# WorkflowDAG construction tests                                      #
# ------------------------------------------------------------------ #


class TestWorkflowDAG:
    """DAG construction and validation."""

    @pytest.mark.unit
    def test_valid_dag(self) -> None:
        dag = WorkflowDAG(
            name="test",
            steps=[
                ActivityStep(name="a", handler_name="h_a"),
                ActivityStep(name="b", handler_name="h_b", depends_on=["a"]),
            ],
        )
        assert len(dag.steps) == 2

    @pytest.mark.unit
    def test_rejects_duplicate_step_names(self) -> None:
        with pytest.raises(ValueError, match="Duplicate step names"):
            WorkflowDAG(
                name="bad",
                steps=[
                    ActivityStep(name="a", handler_name="h_a"),
                    ActivityStep(name="a", handler_name="h_b"),
                ],
            )

    @pytest.mark.unit
    def test_rejects_unknown_dependency(self) -> None:
        with pytest.raises(ValueError, match="unknown step"):
            WorkflowDAG(
                name="bad",
                steps=[
                    ActivityStep(name="a", handler_name="h_a", depends_on=["nonexistent"]),
                ],
            )

    @pytest.mark.unit
    def test_rejects_cycle(self) -> None:
        with pytest.raises(ValueError, match="Cycle detected"):
            WorkflowDAG(
                name="bad",
                steps=[
                    ActivityStep(name="a", handler_name="h_a", depends_on=["b"]),
                    ActivityStep(name="b", handler_name="h_b", depends_on=["a"]),
                ],
            )

    @pytest.mark.unit
    def test_execution_order_respects_deps(self) -> None:
        dag = WorkflowDAG(
            name="test",
            steps=[
                ActivityStep(name="c", handler_name="h_c", depends_on=["a", "b"]),
                ActivityStep(name="a", handler_name="h_a"),
                ActivityStep(name="b", handler_name="h_b", depends_on=["a"]),
            ],
        )
        order = [s.name for s in dag.execution_order()]
        assert order.index("a") < order.index("b")
        assert order.index("b") < order.index("c")

    @pytest.mark.unit
    def test_get_step(self) -> None:
        dag = WorkflowDAG(
            name="test",
            steps=[ActivityStep(name="a", handler_name="h_a")],
        )
        assert dag.get_step("a") is not None
        assert dag.get_step("nonexistent") is None

    @pytest.mark.unit
    def test_empty_dag_is_valid(self) -> None:
        dag = WorkflowDAG(name="empty", steps=[])
        assert dag.execution_order() == []


# ------------------------------------------------------------------ #
# Pre-built workflow tests                                             #
# ------------------------------------------------------------------ #


class TestPrebuiltWorkflows:
    """Factory functions for Discovery and Campaign workflows."""

    @pytest.mark.unit
    def test_discovery_workflow_structure(self) -> None:
        dag = build_discovery_workflow(run_id="test-001")
        assert dag.name == "DiscoveryWorkflow"
        assert len(dag.steps) == 3
        order = [s.name for s in dag.execution_order()]
        assert order == ["trend_analyst", "scout", "persist_candidates"]

    @pytest.mark.unit
    def test_campaign_workflow_structure(self) -> None:
        dag = build_campaign_workflow(brief_id="b-001", run_id="r-001")
        assert dag.name == "CampaignWorkflow"
        assert len(dag.steps) == 7
        order = [s.name for s in dag.execution_order()]
        assert order[0] == "strategist"
        assert order[-1] == "schedule_metrics"
        # Producer has 30min timeout for video gen
        producer = dag.get_step("producer")
        assert producer is not None
        assert producer.timeout_s == 1800.0

    @pytest.mark.unit
    def test_campaign_workflow_idempotency_keys(self) -> None:
        dag = build_campaign_workflow(brief_id="b-001", run_id="r-001")
        keys = [s.idempotency_key for s in dag.steps]
        assert all(k for k in keys)  # all non-empty
        assert len(set(keys)) == len(keys)  # all unique

    @pytest.mark.unit
    def test_discovery_workflow_metadata(self) -> None:
        dag = build_discovery_workflow(run_id="test-001")
        assert dag.metadata["cron"] == "0 */6 * * *"


# ------------------------------------------------------------------ #
# RetryPolicy tests                                                    #
# ------------------------------------------------------------------ #


class TestRetryPolicy:
    """RetryPolicy defaults and custom values."""

    @pytest.mark.unit
    def test_defaults(self) -> None:
        policy = RetryPolicy()
        assert policy.max_attempts == 3
        assert policy.initial_interval_s == 1.0

    @pytest.mark.unit
    def test_custom_policy(self) -> None:
        policy = RetryPolicy(max_attempts=5, initial_interval_s=2.0)
        assert policy.max_attempts == 5


# ------------------------------------------------------------------ #
# InProcessExecutor tests                                              #
# ------------------------------------------------------------------ #


class TestInProcessExecutor:
    """InProcessExecutor with mock handlers."""

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_execute_simple_dag(self) -> None:
        executor = InProcessExecutor()

        async def handler_a(ctx: dict) -> str:
            return "result_a"

        async def handler_b(ctx: dict) -> str:
            return f"result_b+{ctx.get('a', '')}"

        executor.register("h_a", handler_a)
        executor.register("h_b", handler_b)

        dag = WorkflowDAG(
            name="test",
            steps=[
                ActivityStep(name="a", handler_name="h_a"),
                ActivityStep(name="b", handler_name="h_b", depends_on=["a"]),
            ],
        )
        result = await executor.execute(dag)
        assert result.success
        assert result.steps_completed == 2
        assert result.steps_failed == 0
        assert result.step_results["a"] == "result_a"
        assert result.step_results["b"] == "result_b+result_a"

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_unregistered_handler_fails(self) -> None:
        executor = InProcessExecutor()
        dag = WorkflowDAG(
            name="test",
            steps=[ActivityStep(name="a", handler_name="missing_handler")],
        )
        result = await executor.execute(dag)
        assert not result.success
        assert result.steps_failed == 1
        assert "No handler registered" in result.errors["a"]

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_failed_step_skips_dependents(self) -> None:
        executor = InProcessExecutor()

        async def fail_handler(ctx: dict) -> None:
            raise RuntimeError("boom")

        async def success_handler(ctx: dict) -> str:
            return "ok"

        executor.register("h_fail", fail_handler)
        executor.register("h_ok", success_handler)

        dag = WorkflowDAG(
            name="test",
            steps=[
                ActivityStep(
                    name="a",
                    handler_name="h_fail",
                    retry_policy=RetryPolicy(max_attempts=1),
                ),
                ActivityStep(name="b", handler_name="h_ok", depends_on=["a"]),
            ],
        )
        result = await executor.execute(dag)
        assert not result.success
        assert result.steps_failed == 1
        assert result.steps_skipped == 1
        step_b = dag.get_step("b")
        assert step_b is not None
        assert step_b.status is ActivityStatus.SKIPPED

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_idempotency_cache(self) -> None:
        """Same idempotency key should return cached result on re-execute."""
        executor = InProcessExecutor()
        call_count = 0

        async def counted_handler(ctx: dict) -> str:
            nonlocal call_count
            call_count += 1
            return f"result-{call_count}"

        executor.register("h_counted", counted_handler)

        dag = WorkflowDAG(
            name="test",
            steps=[
                ActivityStep(
                    name="a",
                    handler_name="h_counted",
                    idempotency_key="idem-001",
                ),
            ],
        )

        r1 = await executor.execute(dag)
        assert r1.success
        assert call_count == 1

        # Reset step status for re-execution
        dag.steps[0].status = ActivityStatus.PENDING
        r2 = await executor.execute(dag)
        assert r2.success
        assert call_count == 1  # handler NOT called again
        assert r2.step_results["a"] == "result-1"  # cached result

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_retry_on_failure(self) -> None:
        """Handler that fails once then succeeds should complete."""
        executor = InProcessExecutor()
        attempts = 0

        async def flaky_handler(ctx: dict) -> str:
            nonlocal attempts
            attempts += 1
            if attempts < 2:
                raise RuntimeError("transient error")
            return "ok"

        executor.register("h_flaky", flaky_handler)

        dag = WorkflowDAG(
            name="test",
            steps=[
                ActivityStep(
                    name="a",
                    handler_name="h_flaky",
                    retry_policy=RetryPolicy(
                        max_attempts=3, initial_interval_s=0.01
                    ),
                ),
            ],
        )
        result = await executor.execute(dag)
        assert result.success
        assert attempts == 2

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_context_piping(self) -> None:
        """Output of step A should be available in step B's context."""
        executor = InProcessExecutor()

        async def handler_a(ctx: dict) -> dict:
            return {"product_id": 123}

        async def handler_b(ctx: dict) -> str:
            pid = ctx.get("a", {}).get("product_id", 0)
            return f"brief-for-{pid}"

        executor.register("h_a", handler_a)
        executor.register("h_b", handler_b)

        dag = WorkflowDAG(
            name="test",
            steps=[
                ActivityStep(name="a", handler_name="h_a"),
                ActivityStep(name="b", handler_name="h_b", depends_on=["a"]),
            ],
        )
        result = await executor.execute(dag)
        assert result.success
        assert result.step_results["b"] == "brief-for-123"
