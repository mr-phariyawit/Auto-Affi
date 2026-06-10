"""Unit tests for editor budget cap + FFmpeg fallback (FR-VD-04)."""

from __future__ import annotations

import pytest

from auto_affi.pipeline.editor_budget import (
    EditorBudgetTracker,
    PassMode,
)


@pytest.mark.unit
def test_fresh_tracker_has_full_budget() -> None:
    tracker = EditorBudgetTracker(budget_usd=0.40)
    assert tracker.spent_usd == 0.0
    assert tracker.remaining_usd == 0.40
    assert tracker.is_over_budget is False


@pytest.mark.unit
def test_can_afford_within_budget() -> None:
    tracker = EditorBudgetTracker(budget_usd=0.40)
    assert tracker.can_afford(0.10) is True
    assert tracker.can_afford(0.40) is True
    assert tracker.can_afford(0.41) is False


@pytest.mark.unit
def test_record_accumulates_cost() -> None:
    tracker = EditorBudgetTracker(budget_usd=0.40)
    tracker.record("silence_trim", cost_usd=0.05, mode=PassMode.LLM)
    tracker.record("filler_cut", cost_usd=0.10, mode=PassMode.LLM)
    assert tracker.spent_usd == pytest.approx(0.15)
    assert tracker.remaining_usd == pytest.approx(0.25)


@pytest.mark.unit
def test_over_budget_detected() -> None:
    tracker = EditorBudgetTracker(budget_usd=0.10)
    tracker.record("pass1", cost_usd=0.05, mode=PassMode.LLM)
    tracker.record("pass2", cost_usd=0.05, mode=PassMode.LLM)
    assert tracker.is_over_budget is True
    assert tracker.can_afford(0.01) is False


@pytest.mark.unit
def test_decide_mode_llm_when_affordable() -> None:
    tracker = EditorBudgetTracker(budget_usd=0.40)
    mode = tracker.decide_mode("silence_trim", llm_cost_estimate=0.05)
    assert mode is PassMode.LLM


@pytest.mark.unit
def test_decide_mode_fallback_when_over() -> None:
    tracker = EditorBudgetTracker(budget_usd=0.10)
    tracker.record("pass1", cost_usd=0.08, mode=PassMode.LLM)
    mode = tracker.decide_mode("pass2", llm_cost_estimate=0.05)
    assert mode is PassMode.FFMPEG_FALLBACK


@pytest.mark.unit
def test_ffmpeg_fallback_has_zero_cost() -> None:
    tracker = EditorBudgetTracker(budget_usd=0.40)
    tracker.record("silence_trim", cost_usd=0.0, mode=PassMode.FFMPEG_FALLBACK)
    assert tracker.spent_usd == 0.0


@pytest.mark.unit
def test_status_snapshot() -> None:
    tracker = EditorBudgetTracker(budget_usd=0.40)
    tracker.record("p1", cost_usd=0.12, mode=PassMode.LLM)
    tracker.record("p2", cost_usd=0.0, mode=PassMode.FFMPEG_FALLBACK, note="over budget")

    status = tracker.status()
    assert status.budget_usd == 0.40
    assert status.spent_usd == pytest.approx(0.12)
    assert status.remaining_usd == pytest.approx(0.28)
    assert status.is_over_budget is False
    assert status.pass_count == 2
    assert status.entries[1].mode is PassMode.FFMPEG_FALLBACK


@pytest.mark.unit
def test_mixed_llm_and_fallback_workflow() -> None:
    """Simulate a realistic editing session that hits the budget mid-way."""
    tracker = EditorBudgetTracker(budget_usd=0.20)

    # Passes 1-3: LLM-driven (affordable)
    for name, cost in [("silence_trim", 0.05), ("filler_cut", 0.08), ("auto_sub", 0.06)]:
        mode = tracker.decide_mode(name, llm_cost_estimate=cost)
        if mode is PassMode.LLM:
            tracker.record(name, cost_usd=cost, mode=PassMode.LLM)
        else:
            tracker.record(name, cost_usd=0.0, mode=PassMode.FFMPEG_FALLBACK)

    status = tracker.status()
    # First two passes fit (0.05 + 0.08 = 0.13), third might fallback
    # Depends on exact budget check: 0.13 + 0.06 = 0.19 <= 0.20, so pass 3 fits
    assert status.pass_count == 3

    # Now try pass 4: should definitely fallback
    mode = tracker.decide_mode("hook_punch", llm_cost_estimate=0.05)
    assert mode is PassMode.FFMPEG_FALLBACK


@pytest.mark.unit
def test_remaining_never_negative() -> None:
    tracker = EditorBudgetTracker(budget_usd=0.10)
    tracker.record("p1", cost_usd=0.15, mode=PassMode.LLM)  # Overspent
    assert tracker.remaining_usd == 0.0  # Clamped to 0, not negative
    assert tracker.is_over_budget is True


@pytest.mark.unit
def test_default_cap_is_040() -> None:
    """The hard cap must be exactly $0.40 per SPEC 3.5.1."""
    tracker = EditorBudgetTracker()
    assert tracker.budget_usd == pytest.approx(0.40)
