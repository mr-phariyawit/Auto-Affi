"""Workflow DAG definitions for Auto-Affi (FR-OR-01, FR-OR-02).

Defines the two core workflow DAGs as typed Python dataclasses:
  - DiscoveryWorkflow: Scout -> persist candidates (cron 4x/day)
  - CampaignWorkflow: Strategist -> WritersRoom -> SafetyPreCheck ->
    Producer -> SafetyPostCheck -> Publisher -> schedule MetricsPoll

Phase 1 uses :class:`InProcessExecutor` — no Temporal server required.
Phase 2+ migrates to Temporal SDK with the same DAG shapes.

Each activity step is typed, idempotent (via ``idempotency_key``),
and configurable with retry policy and timeout.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

# ------------------------------------------------------------------ #
# Retry policy                                                        #
# ------------------------------------------------------------------ #

@dataclass(frozen=True, slots=True)
class RetryPolicy:
    """Retry behaviour for a workflow activity."""

    max_attempts: int = 3
    initial_interval_s: float = 1.0
    max_interval_s: float = 60.0
    backoff_multiplier: float = 2.0


# ------------------------------------------------------------------ #
# Activity step                                                       #
# ------------------------------------------------------------------ #

class ActivityStatus(StrEnum):
    """Execution status of an activity step."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class ActivityStep:
    """A single typed step in a workflow DAG.

    Each step has a unique ``name``, a ``handler_name`` (which the
    executor resolves to a callable), and configurable retry + timeout.
    ``idempotency_key`` ensures re-execution produces no duplicates
    (FR-OR-02).
    """

    name: str
    handler_name: str
    retry_policy: RetryPolicy = field(default_factory=RetryPolicy)
    timeout_s: float = 300.0
    idempotency_key: str = ""
    status: ActivityStatus = ActivityStatus.PENDING
    result: Any = None
    error: str | None = None
    depends_on: list[str] = field(default_factory=list)


# ------------------------------------------------------------------ #
# Workflow DAG                                                        #
# ------------------------------------------------------------------ #

@dataclass
class WorkflowDAG:
    """A directed acyclic graph of activity steps.

    Steps are executed in topological order respecting ``depends_on``
    edges.  The DAG enforces that:
      - Step names are unique
      - Dependencies reference existing steps
      - No cycles exist (enforced at construction time)
    """

    name: str
    steps: list[ActivityStep] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        names = {s.name for s in self.steps}
        if len(names) != len(self.steps):
            raise ValueError("Duplicate step names in workflow DAG")
        for step in self.steps:
            for dep in step.depends_on:
                if dep not in names:
                    raise ValueError(
                        f"Step '{step.name}' depends on unknown step '{dep}'"
                    )
        # Simple cycle detection via topological sort
        self._toposort()

    def _toposort(self) -> list[str]:
        """Kahn's algorithm for topological ordering."""
        in_degree: dict[str, int] = {s.name: 0 for s in self.steps}
        adj: dict[str, list[str]] = {s.name: [] for s in self.steps}
        for step in self.steps:
            for dep in step.depends_on:
                adj[dep].append(step.name)
                in_degree[step.name] += 1

        queue = [n for n, d in in_degree.items() if d == 0]
        order: list[str] = []
        while queue:
            node = queue.pop(0)
            order.append(node)
            for neighbor in adj[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(order) != len(self.steps):
            raise ValueError(f"Cycle detected in workflow DAG '{self.name}'")
        return order

    def execution_order(self) -> list[ActivityStep]:
        """Return steps in topological execution order."""
        order = self._toposort()
        step_map = {s.name: s for s in self.steps}
        return [step_map[name] for name in order]

    def get_step(self, name: str) -> ActivityStep | None:
        """Look up a step by name."""
        for step in self.steps:
            if step.name == name:
                return step
        return None


# ------------------------------------------------------------------ #
# Pre-built workflow factories (FR-OR-01)                             #
# ------------------------------------------------------------------ #

def build_discovery_workflow(*, run_id: str = "") -> WorkflowDAG:
    """Build the DiscoveryWorkflow DAG.

    Pipeline: TrendAnalyst -> Scout -> persist candidates.
    Cron: 4x/day (every 6 hours).
    """
    return WorkflowDAG(
        name="DiscoveryWorkflow",
        steps=[
            ActivityStep(
                name="trend_analyst",
                handler_name="trend_analyst_activity",
                timeout_s=120.0,
                idempotency_key=f"trend-{run_id}",
            ),
            ActivityStep(
                name="scout",
                handler_name="scout_activity",
                timeout_s=180.0,
                idempotency_key=f"scout-{run_id}",
                depends_on=["trend_analyst"],
            ),
            ActivityStep(
                name="persist_candidates",
                handler_name="persist_candidates_activity",
                timeout_s=30.0,
                idempotency_key=f"persist-{run_id}",
                depends_on=["scout"],
            ),
        ],
        metadata={"cron": "0 */6 * * *", "run_id": run_id},
    )


def build_campaign_workflow(
    *,
    brief_id: str = "",
    run_id: str = "",
) -> WorkflowDAG:
    """Build the CampaignWorkflow DAG.

    Pipeline: Strategist -> WritersRoom -> SafetyPreCheck -> Producer ->
              SafetyPostCheck -> Publisher -> schedule MetricsPoll.
    Triggered: per accepted product candidate.
    """
    return WorkflowDAG(
        name="CampaignWorkflow",
        steps=[
            ActivityStep(
                name="strategist",
                handler_name="strategist_activity",
                timeout_s=120.0,
                idempotency_key=f"strat-{brief_id}-{run_id}",
            ),
            ActivityStep(
                name="writers_room",
                handler_name="writers_room_activity",
                timeout_s=300.0,
                idempotency_key=f"writers-{brief_id}-{run_id}",
                depends_on=["strategist"],
            ),
            ActivityStep(
                name="safety_pre_check",
                handler_name="safety_pre_check_activity",
                timeout_s=60.0,
                idempotency_key=f"safety-pre-{brief_id}-{run_id}",
                depends_on=["writers_room"],
            ),
            ActivityStep(
                name="producer",
                handler_name="producer_activity",
                timeout_s=1800.0,  # 30 min for video gen
                retry_policy=RetryPolicy(max_attempts=2, initial_interval_s=30.0),
                idempotency_key=f"prod-{brief_id}-{run_id}",
                depends_on=["safety_pre_check"],
            ),
            ActivityStep(
                name="safety_post_check",
                handler_name="safety_post_check_activity",
                timeout_s=60.0,
                idempotency_key=f"safety-post-{brief_id}-{run_id}",
                depends_on=["producer"],
            ),
            ActivityStep(
                name="publisher",
                handler_name="publisher_activity",
                timeout_s=120.0,
                idempotency_key=f"pub-{brief_id}-{run_id}",
                depends_on=["safety_post_check"],
            ),
            ActivityStep(
                name="schedule_metrics",
                handler_name="schedule_metrics_activity",
                timeout_s=30.0,
                idempotency_key=f"metrics-{brief_id}-{run_id}",
                depends_on=["publisher"],
            ),
        ],
        metadata={"brief_id": brief_id, "run_id": run_id},
    )
