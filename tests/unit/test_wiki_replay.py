"""Tests for offline replay harness (AFFI-T-028)."""

from __future__ import annotations

import pytest

from auto_affi.wiki.replay import ReplayCase, ReplayHarness


class TestReplayHarness:
    """Offline replay for wiki validation."""

    @pytest.mark.unit
    def test_empty_cases(self) -> None:
        harness = ReplayHarness()
        report = harness.replay([])
        assert report.total_cases == 0
        assert report.divergence_alert is False
        assert report.accuracy == 1.0

    @pytest.mark.unit
    def test_perfect_predictions(self) -> None:
        cases = [
            ReplayCase(
                case_id="c1",
                brief_data={"expected_ctr": 0.05},
                actual_outcome="hit",
                actual_ctr=0.05,
            ),
            ReplayCase(
                case_id="c2",
                brief_data={"expected_ctr": 0.01},
                actual_outcome="flop",
                actual_ctr=0.01,
            ),
        ]
        harness = ReplayHarness()
        report = harness.replay(cases)
        assert report.total_cases == 2
        assert report.mean_ctr_error == pytest.approx(0.0)
        assert report.accuracy == 1.0
        assert report.divergence_alert is False

    @pytest.mark.unit
    def test_high_divergence_triggers_alert(self) -> None:
        cases = [
            ReplayCase(
                case_id="c1",
                brief_data={"expected_ctr": 0.10},
                actual_outcome="flop",
                actual_ctr=0.005,
            ),
            ReplayCase(
                case_id="c2",
                brief_data={"expected_ctr": 0.08},
                actual_outcome="flop",
                actual_ctr=0.003,
            ),
        ]
        harness = ReplayHarness(divergence_threshold=0.05)
        report = harness.replay(cases)
        assert report.divergence_alert is True
        assert report.mean_ctr_error > 0.05

    @pytest.mark.unit
    def test_custom_predict_fn(self) -> None:
        cases = [
            ReplayCase(
                case_id="c1",
                brief_data={"angle": "curiosity"},
                actual_outcome="hit",
                actual_ctr=0.04,
            ),
        ]

        def predict(brief_data: dict) -> float:
            return 0.04  # perfect prediction

        harness = ReplayHarness()
        report = harness.replay(cases, predict_fn=predict)
        assert report.mean_ctr_error == pytest.approx(0.0)

    @pytest.mark.unit
    def test_accuracy_calculation(self) -> None:
        cases = [
            ReplayCase(
                case_id="c1",
                brief_data={"expected_ctr": 0.05},
                actual_outcome="hit",
                actual_ctr=0.04,
            ),
            ReplayCase(
                case_id="c2",
                brief_data={"expected_ctr": 0.05},
                actual_outcome="flop",  # predicted good but actual bad
                actual_ctr=0.001,
            ),
        ]
        harness = ReplayHarness()
        report = harness.replay(cases)
        assert report.accuracy == 0.5  # 1 correct, 1 wrong

    @pytest.mark.unit
    def test_per_case_results(self) -> None:
        cases = [
            ReplayCase(
                case_id="c1",
                brief_data={"expected_ctr": 0.03},
                actual_outcome="neutral",
                actual_ctr=0.025,
            ),
        ]
        harness = ReplayHarness()
        report = harness.replay(cases)
        assert len(report.results) == 1
        assert report.results[0].case_id == "c1"
        assert report.results[0].ctr_error == pytest.approx(0.005)
