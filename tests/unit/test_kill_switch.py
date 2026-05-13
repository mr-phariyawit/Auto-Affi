"""Tests for kill switch registry + auto-kill (AFFI-T-031, T-032)."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from auto_affi.agents.kill_switch import (
    KillLevel,
    KillSwitchRegistry,
    SafetyViolationEvent,
    ViolationTracker,
)


# ------------------------------------------------------------------ #
# KillSwitchRegistry tests (T-031)                                     #
# ------------------------------------------------------------------ #


class TestKillSwitchRegistry:
    """Kill switch registry with scope cascade."""

    @pytest.mark.unit
    def test_activate_and_check_product(self) -> None:
        reg = KillSwitchRegistry()
        reg.activate(KillLevel.PRODUCT, "prod-123", reason="test")
        assert reg.is_killed(product_id="prod-123") is True
        assert reg.is_killed(product_id="prod-456") is False

    @pytest.mark.unit
    def test_activate_campaign_blocks_product(self) -> None:
        reg = KillSwitchRegistry()
        reg.activate(KillLevel.CAMPAIGN, "camp-001", reason="test")
        assert reg.is_killed(campaign_id="camp-001") is True
        assert reg.is_killed(campaign_id="camp-002") is False

    @pytest.mark.unit
    def test_activate_platform_blocks_campaign(self) -> None:
        reg = KillSwitchRegistry()
        reg.activate(KillLevel.PLATFORM, "ig", reason="test")
        assert reg.is_killed(platform="ig") is True
        assert reg.is_killed(platform="fb") is False

    @pytest.mark.unit
    def test_global_blocks_everything(self) -> None:
        reg = KillSwitchRegistry()
        reg.activate(KillLevel.GLOBAL, "global", reason="test")
        assert reg.is_killed(product_id="any") is True
        assert reg.is_killed(campaign_id="any") is True
        assert reg.is_killed(platform="any") is True
        assert reg.is_killed() is True

    @pytest.mark.unit
    def test_cascade_global_over_product(self) -> None:
        """Global kill overrides even when product is not killed."""
        reg = KillSwitchRegistry()
        reg.activate(KillLevel.GLOBAL, "global", reason="emergency")
        assert reg.is_killed(product_id="prod-123") is True

    @pytest.mark.unit
    def test_deactivate(self) -> None:
        reg = KillSwitchRegistry()
        reg.activate(KillLevel.PRODUCT, "prod-123", reason="test")
        assert reg.is_killed(product_id="prod-123") is True
        result = reg.deactivate(KillLevel.PRODUCT, "prod-123")
        assert result is not None
        assert reg.is_killed(product_id="prod-123") is False

    @pytest.mark.unit
    def test_deactivate_nonexistent_returns_none(self) -> None:
        reg = KillSwitchRegistry()
        assert reg.deactivate(KillLevel.PRODUCT, "nope") is None

    @pytest.mark.unit
    def test_audit_log(self) -> None:
        reg = KillSwitchRegistry()
        reg.activate(KillLevel.PRODUCT, "p1", activated_by="human", reason="r1")
        reg.deactivate(KillLevel.PRODUCT, "p1", deactivated_by="human", reason="r2")
        assert len(reg.audit_log) == 2
        assert reg.audit_log[0].activated is True
        assert reg.audit_log[1].activated is False

    @pytest.mark.unit
    def test_active_switches_list(self) -> None:
        reg = KillSwitchRegistry()
        reg.activate(KillLevel.PLATFORM, "ig", reason="r1")
        reg.activate(KillLevel.PRODUCT, "p1", reason="r2")
        assert len(reg.active_switches()) == 2
        reg.deactivate(KillLevel.PRODUCT, "p1")
        assert len(reg.active_switches()) == 1

    @pytest.mark.unit
    def test_no_active_by_default(self) -> None:
        reg = KillSwitchRegistry()
        assert reg.is_killed() is False
        assert reg.active_switches() == []

    @pytest.mark.unit
    def test_multiple_levels_independent(self) -> None:
        reg = KillSwitchRegistry()
        reg.activate(KillLevel.PLATFORM, "ig", reason="r1")
        reg.activate(KillLevel.PRODUCT, "p1", reason="r2")
        reg.deactivate(KillLevel.PLATFORM, "ig")
        # Product kill still active
        assert reg.is_killed(product_id="p1") is True
        # Platform kill removed
        assert reg.is_killed(platform="ig") is False


# ------------------------------------------------------------------ #
# ViolationTracker + Auto-kill tests (T-032)                           #
# ------------------------------------------------------------------ #


class TestViolationTracker:
    """Auto-kill trigger based on violation count."""

    @pytest.mark.unit
    def test_no_auto_kill_below_threshold(self) -> None:
        reg = KillSwitchRegistry()
        tracker = ViolationTracker(registry=reg, threshold=3)
        event = SafetyViolationEvent(
            violation_type="claim", scope_id="v1", details="test"
        )
        triggered = tracker.record_violation(event)
        assert triggered is False
        assert reg.is_killed() is False

    @pytest.mark.unit
    def test_auto_kill_at_threshold(self) -> None:
        reg = KillSwitchRegistry()
        tracker = ViolationTracker(registry=reg, threshold=3)
        now = datetime.now(UTC)
        for i in range(3):
            event = SafetyViolationEvent(
                violation_type="claim",
                scope_id=f"v{i}",
                details=f"violation {i}",
                ts=now + timedelta(minutes=i),
            )
            triggered = tracker.record_violation(event)

        assert triggered is True
        assert reg.is_killed() is True
        # Check that global was activated by auto-kill
        switches = reg.active_switches()
        assert any(s.activated_by == "auto-kill" for s in switches)

    @pytest.mark.unit
    def test_rolling_window_prunes_old(self) -> None:
        reg = KillSwitchRegistry()
        tracker = ViolationTracker(
            registry=reg, threshold=3, window=timedelta(hours=24)
        )
        old_time = datetime.now(UTC) - timedelta(hours=25)
        # Record 2 old violations (outside window)
        for i in range(2):
            tracker.record_violation(
                SafetyViolationEvent(
                    violation_type="claim",
                    scope_id=f"old-{i}",
                    details="old",
                    ts=old_time + timedelta(minutes=i),
                )
            )
        # Record 1 new violation (inside window)
        now = datetime.now(UTC)
        triggered = tracker.record_violation(
            SafetyViolationEvent(
                violation_type="claim",
                scope_id="new-0",
                details="new",
                ts=now,
            )
        )
        assert triggered is False
        assert tracker.violation_count(now=now) == 1

    @pytest.mark.unit
    def test_violation_count(self) -> None:
        reg = KillSwitchRegistry()
        tracker = ViolationTracker(registry=reg, threshold=5)
        now = datetime.now(UTC)
        for i in range(3):
            tracker.record_violation(
                SafetyViolationEvent(
                    violation_type="brand",
                    scope_id=f"v{i}",
                    details="test",
                    ts=now,
                )
            )
        assert tracker.violation_count(now=now) == 3

    @pytest.mark.unit
    def test_custom_threshold(self) -> None:
        reg = KillSwitchRegistry()
        tracker = ViolationTracker(registry=reg, threshold=1)
        triggered = tracker.record_violation(
            SafetyViolationEvent(
                violation_type="nsfw", scope_id="v1", details="test"
            )
        )
        assert triggered is True

    @pytest.mark.unit
    def test_auto_kill_reason_includes_details(self) -> None:
        reg = KillSwitchRegistry()
        tracker = ViolationTracker(registry=reg, threshold=1)
        tracker.record_violation(
            SafetyViolationEvent(
                violation_type="claim",
                scope_id="v1",
                details="health claim detected",
            )
        )
        switches = reg.active_switches()
        assert len(switches) == 1
        assert "health claim detected" in switches[0].reason
