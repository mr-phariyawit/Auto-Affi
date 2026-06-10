"""Budget circuit-breaker for workflows (FR-OR-03).

Enforces per-node and daily cost caps from cost-model.md resonance:
- Per-node caps: each pipeline stage has a max cost
- Daily cap: auto-stop generation when daily cost > budget * 1.1
- Alert threshold: flag when cost/video > target * 1.5

Integrates into InProcessExecutor as a pre-step guard.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class BudgetDecision(StrEnum):
    """Result of a budget check."""

    ALLOW = "allow"
    DENY = "deny"
    ALERT = "alert"


@dataclass(frozen=True, slots=True)
class BudgetAlert:
    """Alert when a budget threshold is exceeded."""

    node: str
    spent: float
    cap: float
    decision: BudgetDecision
    message: str


# Per-node budget caps from cost-model.md (Phase 1)
DEFAULT_NODE_CAPS: dict[str, float] = {
    "scout_strategist_llm": 0.05,
    "writer_llm": 0.10,
    "editor_agent": 0.40,  # hard cap from SPEC 3.5.1
    "image_gen": 0.25,
    "video_gen": 1.80,
    "tts": 0.18,
    "asr": 0.02,
    "hyperframe": 0.05,
    "compose_storage": 0.05,
    "metrics_wiki": 0.07,
}

# Daily budget from settings (default: $50 Opus cap from NFR-CS-03)
DEFAULT_DAILY_CAP: float = 50.0

# Per-video target from cost-model.md
DEFAULT_PER_VIDEO_TARGET: float = 2.87

# Alert multiplier from SPEC 11.3
ALERT_MULTIPLIER: float = 1.5


@dataclass
class BudgetCircuitBreaker:
    """Enforces per-node and daily cost caps.

    Call :meth:`check_budget` before each workflow step to determine
    if the step should proceed, be denied, or trigger an alert.
    """

    node_caps: dict[str, float] = field(
        default_factory=lambda: dict(DEFAULT_NODE_CAPS)
    )
    daily_cap: float = DEFAULT_DAILY_CAP
    per_video_target: float = DEFAULT_PER_VIDEO_TARGET
    alert_multiplier: float = ALERT_MULTIPLIER

    # Running totals
    _node_spent: dict[str, float] = field(default_factory=dict, init=False)
    _daily_spent: float = field(default=0.0, init=False)
    _video_count: int = field(default=0, init=False)
    _alerts: list[BudgetAlert] = field(default_factory=list, init=False)

    def check_budget(self, node: str, estimated_cost: float) -> BudgetDecision:
        """Check if a workflow step should proceed.

        Returns ALLOW if under cap, DENY if over daily cap (auto-stop),
        or ALERT if per-video target is exceeded (continue but flag).
        """
        # Daily cap check (hard stop)
        projected_daily = self._daily_spent + estimated_cost
        if projected_daily > self.daily_cap * 1.1:
            alert = BudgetAlert(
                node=node,
                spent=self._daily_spent,
                cap=self.daily_cap,
                decision=BudgetDecision.DENY,
                message=(
                    f"Daily budget exceeded: ${self._daily_spent:.2f} + "
                    f"${estimated_cost:.2f} > ${self.daily_cap * 1.1:.2f} "
                    f"(cap * 1.1). Auto-stop."
                ),
            )
            self._alerts.append(alert)
            return BudgetDecision.DENY

        # Per-node cap check (hard stop for that node)
        node_cap = self.node_caps.get(node)
        if node_cap is not None:
            node_spent = self._node_spent.get(node, 0.0) + estimated_cost
            if node_spent > node_cap:
                alert = BudgetAlert(
                    node=node,
                    spent=self._node_spent.get(node, 0.0),
                    cap=node_cap,
                    decision=BudgetDecision.DENY,
                    message=(
                        f"Node '{node}' budget exceeded: "
                        f"${self._node_spent.get(node, 0.0):.2f} + "
                        f"${estimated_cost:.2f} > ${node_cap:.2f}"
                    ),
                )
                self._alerts.append(alert)
                return BudgetDecision.DENY

        return BudgetDecision.ALLOW

    def record_spend(self, node: str, cost: float) -> None:
        """Record actual cost after a step completes."""
        self._node_spent[node] = self._node_spent.get(node, 0.0) + cost
        self._daily_spent += cost

    def record_video_complete(self, total_cost: float) -> BudgetDecision:
        """Record a completed video and check per-video alert threshold."""
        self._video_count += 1

        if total_cost > self.per_video_target * self.alert_multiplier:
            alert = BudgetAlert(
                node="video_total",
                spent=total_cost,
                cap=self.per_video_target * self.alert_multiplier,
                decision=BudgetDecision.ALERT,
                message=(
                    f"Video #{self._video_count} cost ${total_cost:.2f} > "
                    f"${self.per_video_target * self.alert_multiplier:.2f} "
                    f"(target * {self.alert_multiplier})"
                ),
            )
            self._alerts.append(alert)
            return BudgetDecision.ALERT
        return BudgetDecision.ALLOW

    def reset_node(self, node: str) -> None:
        """Reset per-node spend (new video starts fresh per-node tracking)."""
        self._node_spent.pop(node, None)

    def reset_daily(self) -> None:
        """Reset daily spend (new day)."""
        self._daily_spent = 0.0
        self._video_count = 0

    @property
    def daily_spent(self) -> float:
        return self._daily_spent

    @property
    def video_count(self) -> int:
        return self._video_count

    @property
    def alerts(self) -> list[BudgetAlert]:
        return list(self._alerts)

    def node_spent(self, node: str) -> float:
        return self._node_spent.get(node, 0.0)
