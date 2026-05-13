"""Offline replay harness for wiki validation (FR-FB-04).

Re-runs the Strategist's brief-generation logic on historical data and
compares the output with actual ground-truth outcomes. If divergence
exceeds a threshold, the wiki may have rotted and needs review.

Phase 1: simple accuracy-based divergence scoring.
Phase 2+: KL divergence on CTR distributions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class ReplayCase:
    """A historical case for replay testing."""

    case_id: str
    brief_data: dict[str, Any]
    actual_outcome: str  # breakout | hit | neutral | flop | banned
    actual_ctr: float = 0.0


@dataclass(frozen=True, slots=True)
class ReplayResult:
    """Result of replaying a single case."""

    case_id: str
    predicted_ctr: float
    actual_ctr: float
    actual_outcome: str
    ctr_error: float  # abs(predicted - actual)


@dataclass
class DivergenceReport:
    """Summary of replay divergence across all cases."""

    total_cases: int
    mean_ctr_error: float
    max_ctr_error: float
    accuracy: float  # fraction where predicted direction matches actual
    divergence_alert: bool  # True if divergence exceeds threshold
    threshold: float
    results: list[ReplayResult] = field(default_factory=list)


@dataclass
class ReplayHarness:
    """Offline replay harness.

    Replays historical briefs through a scoring function and compares
    with ground-truth outcomes.
    """

    divergence_threshold: float = 0.15  # alert if mean CTR error > 15pp

    def replay(
        self,
        cases: list[ReplayCase],
        *,
        predict_fn: Any | None = None,
    ) -> DivergenceReport:
        """Run replay on a set of historical cases.

        Args:
            cases: Historical cases with known outcomes.
            predict_fn: Optional callable(brief_data) -> predicted_ctr.
                        If None, uses the brief's expected_ctr field.

        Returns:
            DivergenceReport with per-case results and aggregate metrics.
        """
        if not cases:
            return DivergenceReport(
                total_cases=0,
                mean_ctr_error=0.0,
                max_ctr_error=0.0,
                accuracy=1.0,
                divergence_alert=False,
                threshold=self.divergence_threshold,
            )

        results: list[ReplayResult] = []
        total_error = 0.0
        max_error = 0.0
        correct = 0

        for case in cases:
            if predict_fn is not None:
                predicted_ctr = predict_fn(case.brief_data)
            else:
                predicted_ctr = case.brief_data.get("expected_ctr", 0.0)

            error = abs(predicted_ctr - case.actual_ctr)
            total_error += error
            max_error = max(max_error, error)

            # "Correct" if the prediction direction matches the outcome
            # (high predicted CTR -> hit/breakout, low -> flop)
            predicted_good = predicted_ctr >= 0.02
            actual_good = case.actual_outcome in ("hit", "breakout")
            if predicted_good == actual_good:
                correct += 1

            results.append(
                ReplayResult(
                    case_id=case.case_id,
                    predicted_ctr=predicted_ctr,
                    actual_ctr=case.actual_ctr,
                    actual_outcome=case.actual_outcome,
                    ctr_error=error,
                )
            )

        mean_error = total_error / len(cases)
        accuracy = correct / len(cases)

        return DivergenceReport(
            total_cases=len(cases),
            mean_ctr_error=mean_error,
            max_ctr_error=max_error,
            accuracy=accuracy,
            divergence_alert=mean_error > self.divergence_threshold,
            threshold=self.divergence_threshold,
            results=results,
        )
