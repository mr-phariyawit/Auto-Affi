"""Tests for budget circuit-breaker (AFFI-T-036)."""

from __future__ import annotations

import pytest

from auto_affi.workflows.budget import (
    DEFAULT_DAILY_CAP,
    DEFAULT_PER_VIDEO_TARGET,
    BudgetCircuitBreaker,
    BudgetDecision,
)


class TestBudgetCircuitBreaker:
    """Budget circuit-breaker for workflow cost control."""

    @pytest.mark.unit
    def test_allow_under_caps(self) -> None:
        breaker = BudgetCircuitBreaker()
        decision = breaker.check_budget("scout_strategist_llm", 0.03)
        assert decision is BudgetDecision.ALLOW

    @pytest.mark.unit
    def test_deny_over_node_cap(self) -> None:
        breaker = BudgetCircuitBreaker()
        # editor_agent cap is $0.40
        breaker.record_spend("editor_agent", 0.35)
        decision = breaker.check_budget("editor_agent", 0.10)
        assert decision is BudgetDecision.DENY

    @pytest.mark.unit
    def test_deny_over_daily_cap(self) -> None:
        breaker = BudgetCircuitBreaker(daily_cap=10.0)
        breaker.record_spend("video_gen", 10.5)
        decision = breaker.check_budget("video_gen", 1.0)
        assert decision is BudgetDecision.DENY

    @pytest.mark.unit
    def test_daily_cap_with_11_multiplier(self) -> None:
        """Daily cap triggers at budget * 1.1, not exactly at budget."""
        breaker = BudgetCircuitBreaker(daily_cap=10.0)
        # Use an unknown node (no per-node cap) to test daily cap only
        breaker.record_spend("misc_ops", 10.0)
        # 10.0 + 0.5 = 10.5, which is < 11.0 (10 * 1.1)
        decision = breaker.check_budget("misc_ops", 0.5)
        assert decision is BudgetDecision.ALLOW
        # 10.0 + 0.5 already spent, now spend 0.5 more → 10.5
        # then check 2.0 → 10.5 + 2.0 = 12.5 > 11.0 → DENY
        breaker.record_spend("misc_ops", 0.5)
        decision = breaker.check_budget("misc_ops", 2.0)
        assert decision is BudgetDecision.DENY

    @pytest.mark.unit
    def test_record_video_complete_under_target(self) -> None:
        breaker = BudgetCircuitBreaker()
        decision = breaker.record_video_complete(2.50)
        assert decision is BudgetDecision.ALLOW
        assert breaker.video_count == 1

    @pytest.mark.unit
    def test_record_video_complete_over_alert_threshold(self) -> None:
        breaker = BudgetCircuitBreaker(per_video_target=2.87, alert_multiplier=1.5)
        # 2.87 * 1.5 = 4.305
        decision = breaker.record_video_complete(5.00)
        assert decision is BudgetDecision.ALERT
        assert len(breaker.alerts) == 1

    @pytest.mark.unit
    def test_unknown_node_no_cap(self) -> None:
        """Unknown nodes have no per-node cap, only daily cap applies."""
        breaker = BudgetCircuitBreaker()
        decision = breaker.check_budget("unknown_node", 0.50)
        assert decision is BudgetDecision.ALLOW

    @pytest.mark.unit
    def test_reset_node(self) -> None:
        breaker = BudgetCircuitBreaker()
        breaker.record_spend("editor_agent", 0.30)
        assert breaker.node_spent("editor_agent") == pytest.approx(0.30)
        breaker.reset_node("editor_agent")
        assert breaker.node_spent("editor_agent") == 0.0

    @pytest.mark.unit
    def test_reset_daily(self) -> None:
        breaker = BudgetCircuitBreaker()
        breaker.record_spend("video_gen", 5.0)
        breaker.record_video_complete(3.0)
        breaker.reset_daily()
        assert breaker.daily_spent == 0.0
        assert breaker.video_count == 0

    @pytest.mark.unit
    def test_default_node_caps_from_cost_model(self) -> None:
        """Default caps must match cost-model.md values exactly."""
        breaker = BudgetCircuitBreaker()
        assert breaker.node_caps["editor_agent"] == pytest.approx(0.40)
        assert breaker.node_caps["video_gen"] == pytest.approx(1.80)
        assert breaker.node_caps["tts"] == pytest.approx(0.18)
        assert breaker.node_caps["scout_strategist_llm"] == pytest.approx(0.05)

    @pytest.mark.unit
    def test_cumulative_spending(self) -> None:
        breaker = BudgetCircuitBreaker()
        breaker.record_spend("scout_strategist_llm", 0.02)
        breaker.record_spend("writer_llm", 0.05)
        breaker.record_spend("video_gen", 1.50)
        assert breaker.daily_spent == pytest.approx(1.57)

    @pytest.mark.unit
    def test_alerts_accumulate(self) -> None:
        breaker = BudgetCircuitBreaker(daily_cap=1.0)
        breaker.record_spend("video_gen", 1.0)
        breaker.check_budget("video_gen", 0.50)  # deny
        breaker.check_budget("tts", 0.50)  # deny
        assert len(breaker.alerts) == 2

    @pytest.mark.unit
    def test_default_daily_cap_is_50(self) -> None:
        """Daily cap must be exactly $50.0 per NFR-CS-03."""
        assert pytest.approx(50.0) == DEFAULT_DAILY_CAP
        breaker = BudgetCircuitBreaker()
        assert breaker.daily_cap == pytest.approx(50.0)

    @pytest.mark.unit
    def test_default_per_video_target_is_287(self) -> None:
        """Per-video target must be $2.87 per cost-model.md."""
        assert pytest.approx(2.87) == DEFAULT_PER_VIDEO_TARGET
        breaker = BudgetCircuitBreaker()
        assert breaker.per_video_target == pytest.approx(2.87)

    @pytest.mark.unit
    def test_projected_daily_deny_at_boundary(self) -> None:
        """Exactly at daily_cap * 1.1 boundary: > triggers DENY, = does not."""
        breaker = BudgetCircuitBreaker(daily_cap=10.0)
        # Spend exactly 10.0; check 1.0 → 11.0 which is NOT > 11.0 → ALLOW
        breaker.record_spend("misc_ops", 10.0)
        decision = breaker.check_budget("misc_ops", 1.0)
        assert decision is BudgetDecision.ALLOW
        # check 1.01 → 11.01 which IS > 11.0 → DENY
        decision = breaker.check_budget("misc_ops", 1.01)
        assert decision is BudgetDecision.DENY
