"""Tests for speed_guard.check_speed — pure logic, no I/O.

Covers:
  - 1.0x factor → ok=True, no warnings, no errors
  - 1.10x factor → ok=True, 1 warning, no errors
  - 1.20x factor → ok=False, no warnings, 1 error (REJECT)
  - mixed segments → ok depends on worst error
  - empty segments → ok=True, max_factor=0
  - zero slot_s → error (invalid input)
  - max_factor field populated correctly
"""

from __future__ import annotations

from dataclasses import dataclass

import pytest

from auto_affi.pipeline.speed_guard import SpeedGuardReport, check_speed


# ---------------------------------------------------------------------------
# Minimal segment helper
# ---------------------------------------------------------------------------


@dataclass
class _Seg:
    raw_audio_s: float
    slot_s: float


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_speed_guard_1x_passes_clean() -> None:
    report = check_speed([_Seg(raw_audio_s=5.0, slot_s=5.0)])
    assert report.ok is True
    assert report.warnings == []
    assert report.errors == []
    assert abs(report.max_factor - 1.0) < 0.001


@pytest.mark.unit
def test_speed_guard_below_warn_passes() -> None:
    # 1.05x — under 1.08x warn threshold
    report = check_speed([_Seg(raw_audio_s=5.25, slot_s=5.0)])
    assert report.ok is True
    assert report.warnings == []
    assert report.errors == []


@pytest.mark.unit
def test_speed_guard_at_warn_boundary_passes() -> None:
    # exactly 1.08x — at threshold, not over; should pass without warn
    report = check_speed([_Seg(raw_audio_s=1.08, slot_s=1.0)])
    assert report.ok is True
    assert report.warnings == []


@pytest.mark.unit
def test_speed_guard_1_10x_warns_not_rejects() -> None:
    """1.10x is between 1.08x and 1.15x — warning only, ok=True."""
    report = check_speed([_Seg(raw_audio_s=1.10, slot_s=1.0)])
    assert report.ok is True
    assert len(report.warnings) == 1
    assert report.errors == []
    assert "WARN" in report.warnings[0]


@pytest.mark.unit
def test_speed_guard_1_15x_boundary_warns_only() -> None:
    """Exactly 1.15x is at the reject threshold but not over — warn only."""
    report = check_speed([_Seg(raw_audio_s=1.15, slot_s=1.0)])
    assert report.ok is True
    assert len(report.warnings) == 1
    assert report.errors == []


@pytest.mark.unit
def test_speed_guard_1_20x_rejects() -> None:
    """1.20x exceeds 1.15x hard limit — ok=False, error emitted."""
    report = check_speed([_Seg(raw_audio_s=1.20, slot_s=1.0)])
    assert report.ok is False
    assert len(report.errors) == 1
    assert "REJECT" in report.errors[0]
    assert report.warnings == []


@pytest.mark.unit
def test_speed_guard_multiple_segments_all_clean() -> None:
    segs = [
        _Seg(raw_audio_s=3.0, slot_s=3.0),  # 1.0x
        _Seg(raw_audio_s=4.0, slot_s=4.5),  # ~0.89x
        _Seg(raw_audio_s=2.0, slot_s=2.0),  # 1.0x
    ]
    report = check_speed(segs)
    assert report.ok is True
    assert report.warnings == []
    assert report.errors == []


@pytest.mark.unit
def test_speed_guard_mixed_warn_and_reject() -> None:
    segs = [
        _Seg(raw_audio_s=1.10, slot_s=1.0),  # 1.10x → warn
        _Seg(raw_audio_s=1.20, slot_s=1.0),  # 1.20x → reject
    ]
    report = check_speed(segs)
    assert report.ok is False
    assert len(report.warnings) == 1
    assert len(report.errors) == 1


@pytest.mark.unit
def test_speed_guard_empty_segments_ok() -> None:
    report = check_speed([])
    assert report.ok is True
    assert report.max_factor == 0.0
    assert report.warnings == []
    assert report.errors == []


@pytest.mark.unit
def test_speed_guard_zero_slot_errors() -> None:
    report = check_speed([_Seg(raw_audio_s=2.0, slot_s=0.0)])
    assert report.ok is False
    assert len(report.errors) == 1


@pytest.mark.unit
def test_speed_guard_max_factor_correct() -> None:
    segs = [
        _Seg(raw_audio_s=1.0, slot_s=1.0),   # 1.0x
        _Seg(raw_audio_s=1.20, slot_s=1.0),  # 1.2x — max
        _Seg(raw_audio_s=0.9, slot_s=1.0),   # 0.9x
    ]
    report = check_speed(segs)
    assert abs(report.max_factor - 1.20) < 0.001


@pytest.mark.unit
def test_speed_guard_returns_speed_guard_report() -> None:
    report = check_speed([_Seg(raw_audio_s=1.0, slot_s=1.0)])
    assert isinstance(report, SpeedGuardReport)
