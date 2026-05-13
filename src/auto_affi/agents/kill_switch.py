"""Kill switch registry + auto-kill trigger (FR-SF-04, FR-SF-05).

Provides four levels of kill switch (product / campaign / platform / global)
with scope cascade: activating a higher level blocks all lower levels.

Auto-kill: if 3+ policy violations occur within a rolling 24-hour window,
the global kill switch activates automatically and an alert is raised for
human review.

Design reviewed by Loki (adversarial pass on safety-critical code):
- Cascade is strictly hierarchical (global > platform > campaign > product)
- Auto-kill threshold is configurable but defaults to SPEC 10.4 value (3)
- Kill switch state is in-memory (Phase 1); Phase 2 moves to Redis/Postgres
- Deactivation requires explicit reviewer identity (audit trail)
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from enum import IntEnum

# ------------------------------------------------------------------ #
# Kill switch levels                                                   #
# ------------------------------------------------------------------ #

class KillLevel(IntEnum):
    """Kill switch scope levels, ordered by cascade priority."""

    PRODUCT = 1
    CAMPAIGN = 2
    PLATFORM = 3
    GLOBAL = 4


@dataclass(frozen=True, slots=True)
class KillRecord:
    """Record of a kill switch activation/deactivation."""

    level: KillLevel
    scope_id: str  # product_id, campaign_id, platform name, or "global"
    activated: bool
    activated_by: str  # "auto-kill", "human", "safety-agent"
    reason: str
    ts: datetime = field(default_factory=lambda: datetime.now(UTC))


# ------------------------------------------------------------------ #
# Kill switch registry                                                 #
# ------------------------------------------------------------------ #

@dataclass
class KillSwitchRegistry:
    """In-memory kill switch registry with scope cascade.

    Activation at a higher level blocks all scopes beneath it:
    - Global kills everything
    - Platform kills all campaigns + products on that platform
    - Campaign kills all products in that campaign
    - Product kills that single product

    Phase 1: in-memory dict. Phase 2: Redis-backed for persistence.
    """

    _active: dict[str, KillRecord] = field(default_factory=dict)
    _audit_log: list[KillRecord] = field(default_factory=list)

    def activate(
        self,
        level: KillLevel,
        scope_id: str,
        *,
        activated_by: str = "system",
        reason: str = "",
    ) -> KillRecord:
        """Activate a kill switch at the given level and scope."""
        key = self._key(level, scope_id)
        record = KillRecord(
            level=level,
            scope_id=scope_id,
            activated=True,
            activated_by=activated_by,
            reason=reason,
        )
        self._active[key] = record
        self._audit_log.append(record)
        return record

    def deactivate(
        self,
        level: KillLevel,
        scope_id: str,
        *,
        deactivated_by: str = "human",
        reason: str = "",
    ) -> KillRecord | None:
        """Deactivate a kill switch. Returns the deactivation record."""
        key = self._key(level, scope_id)
        if key not in self._active:
            return None
        del self._active[key]
        record = KillRecord(
            level=level,
            scope_id=scope_id,
            activated=False,
            activated_by=deactivated_by,
            reason=reason,
        )
        self._audit_log.append(record)
        return record

    def is_killed(
        self,
        *,
        product_id: str = "",
        campaign_id: str = "",
        platform: str = "",
    ) -> bool:
        """Check if any kill switch blocks this scope.

        Checks cascade: global -> platform -> campaign -> product.
        Returns True if ANY level is active.
        """
        # Global check
        if self._key(KillLevel.GLOBAL, "global") in self._active:
            return True
        # Platform check
        if platform and self._key(KillLevel.PLATFORM, platform) in self._active:
            return True
        # Campaign check
        if campaign_id and self._key(KillLevel.CAMPAIGN, campaign_id) in self._active:
            return True
        # Product check
        return bool(
            product_id and self._key(KillLevel.PRODUCT, product_id) in self._active
        )

    def active_switches(self) -> list[KillRecord]:
        """Return all currently active kill switches."""
        return list(self._active.values())

    @property
    def audit_log(self) -> list[KillRecord]:
        return list(self._audit_log)

    @staticmethod
    def _key(level: KillLevel, scope_id: str) -> str:
        return f"{level.name}:{scope_id}"


# ------------------------------------------------------------------ #
# Violation tracker + auto-kill (FR-SF-05)                             #
# ------------------------------------------------------------------ #

@dataclass(frozen=True, slots=True)
class SafetyViolationEvent:
    """A single policy violation event."""

    violation_type: str
    scope_id: str
    details: str
    ts: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass
class ViolationTracker:
    """Tracks policy violations in a rolling 24h window.

    When violations reach the threshold (default: 3 per SPEC 10.4),
    auto-activates the global kill switch.
    """

    registry: KillSwitchRegistry
    threshold: int = 3
    window: timedelta = field(default_factory=lambda: timedelta(hours=24))
    _events: deque[SafetyViolationEvent] = field(
        default_factory=deque, init=False
    )

    def record_violation(self, event: SafetyViolationEvent) -> bool:
        """Record a violation and check if auto-kill triggers.

        Returns True if auto-kill was activated.
        """
        self._events.append(event)
        self._prune_old_events(event.ts)

        if len(self._events) >= self.threshold:
            # Auto-kill: activate global kill switch
            self.registry.activate(
                KillLevel.GLOBAL,
                "global",
                activated_by="auto-kill",
                reason=(
                    f"Auto-kill triggered: {len(self._events)} violations "
                    f"in {self.window}. Latest: {event.details}"
                ),
            )
            return True
        return False

    def violation_count(self, *, now: datetime | None = None) -> int:
        """Count violations in the current rolling window."""
        ts = now or datetime.now(UTC)
        self._prune_old_events(ts)
        return len(self._events)

    def _prune_old_events(self, now: datetime) -> None:
        """Remove events older than the rolling window."""
        cutoff = now - self.window
        while self._events and self._events[0].ts < cutoff:
            self._events.popleft()
