"""In-process workflow executor (Phase 1, FR-OR-01/02).

Runs a :class:`WorkflowDAG` by executing each activity step in
topological order.  Supports retry with exponential backoff per step.

Phase 1: sequential in-process execution — no Temporal server required.
Phase 2+: swap to Temporal SDK with the same DAG shapes.
"""

from __future__ import annotations

import asyncio
import time
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from typing import Any

from auto_affi.workflows.definitions import (
    ActivityStatus,
    ActivityStep,
    WorkflowDAG,
)

# Handler registry type
HandlerFn = Callable[..., Awaitable[Any]]


@dataclass
class ExecutionResult:
    """Result of a complete workflow execution."""

    workflow_name: str
    success: bool
    steps_completed: int
    steps_failed: int
    steps_skipped: int
    total_duration_s: float
    step_results: dict[str, Any] = field(default_factory=dict)
    errors: dict[str, str] = field(default_factory=dict)


@dataclass
class InProcessExecutor:
    """Executes a WorkflowDAG in-process with retry support.

    Register handlers via :meth:`register`, then call :meth:`execute`
    with a DAG.  Unregistered handlers cause the step to fail (not skip).

    Idempotency: if a step's ``idempotency_key`` has been seen before
    (in the executor's lifetime), the step is skipped and its cached
    result is returned.  This fulfils FR-OR-02.
    """

    _handlers: dict[str, HandlerFn] = field(default_factory=dict)
    _idempotency_cache: dict[str, Any] = field(default_factory=dict)

    def register(self, handler_name: str, fn: HandlerFn) -> None:
        """Register a handler function for a step."""
        self._handlers[handler_name] = fn

    async def execute(
        self,
        dag: WorkflowDAG,
        *,
        context: dict[str, Any] | None = None,
    ) -> ExecutionResult:
        """Execute all steps in topological order."""
        start = time.perf_counter()
        ctx = dict(context or {})
        completed = 0
        failed = 0
        skipped = 0
        step_results: dict[str, Any] = {}
        errors: dict[str, str] = {}

        for step in dag.execution_order():
            # Check dependencies — skip if any dependency failed
            dep_failed = any(
                dag.get_step(dep) is not None
                and dag.get_step(dep).status is ActivityStatus.FAILED  # type: ignore[union-attr]
                for dep in step.depends_on
            )
            if dep_failed:
                step.status = ActivityStatus.SKIPPED
                skipped += 1
                continue

            # Idempotency check (FR-OR-02)
            if step.idempotency_key and step.idempotency_key in self._idempotency_cache:
                step.result = self._idempotency_cache[step.idempotency_key]
                step.status = ActivityStatus.COMPLETED
                step_results[step.name] = step.result
                completed += 1
                continue

            # Execute with retry
            success = await self._execute_step(step, ctx)
            if success:
                completed += 1
                step_results[step.name] = step.result
                ctx[step.name] = step.result  # pipe output to next step
                if step.idempotency_key:
                    self._idempotency_cache[step.idempotency_key] = step.result
            else:
                failed += 1
                errors[step.name] = step.error or "Unknown error"

        duration = time.perf_counter() - start
        return ExecutionResult(
            workflow_name=dag.name,
            success=failed == 0,
            steps_completed=completed,
            steps_failed=failed,
            steps_skipped=skipped,
            total_duration_s=duration,
            step_results=step_results,
            errors=errors,
        )

    async def _execute_step(
        self,
        step: ActivityStep,
        ctx: dict[str, Any],
    ) -> bool:
        """Execute a single step with retry policy."""
        handler = self._handlers.get(step.handler_name)
        if handler is None:
            step.status = ActivityStatus.FAILED
            step.error = f"No handler registered for '{step.handler_name}'"
            return False

        step.status = ActivityStatus.RUNNING
        policy = step.retry_policy
        interval = policy.initial_interval_s

        for attempt in range(1, policy.max_attempts + 1):
            try:
                step.result = await asyncio.wait_for(
                    handler(ctx),
                    timeout=step.timeout_s,
                )
                step.status = ActivityStatus.COMPLETED
                return True
            except Exception as err:
                step.error = f"Attempt {attempt}/{policy.max_attempts}: {err}"
                if attempt < policy.max_attempts:
                    await asyncio.sleep(interval)
                    interval = min(
                        interval * policy.backoff_multiplier,
                        policy.max_interval_s,
                    )

        step.status = ActivityStatus.FAILED
        return False
