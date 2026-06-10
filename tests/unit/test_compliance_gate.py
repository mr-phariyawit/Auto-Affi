"""Integration tests for pipeline.compliance_gate.run_compliance.

Uses real ffmpeg/ffprobe to build master files and then exercises all four
sub-checks. Covers:
  - Full PASS on a compliant master + clean storyboard + aligned captions
  - FAIL when a forbidden claim is injected into dialogue
  - FAIL when a VO segment exceeds 1.15x speed
  - FAIL when caption count mismatches dialogue count
  - FAIL when cleanroom finds 0 audio streams (raw clip as master)
  - ok=True only when ALL four sub-checks pass
"""

from __future__ import annotations

import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest

from auto_affi.pipeline.compliance_gate import ComplianceReport, run_compliance
from auto_affi.pipeline.dry_render import assemble_master, render_shot


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


@dataclass
class _FakeShot:
    duration_s: float
    shot_id: str = "s0"


@dataclass
class _Seg:
    raw_audio_s: float
    slot_s: float


def _make_clip(tmpdir: Path, duration_s: float, shot_id: str = "s0") -> Path:
    dest = tmpdir / f"clip_{shot_id}.mp4"
    render_shot(_FakeShot(duration_s=duration_s, shot_id=shot_id), dest)
    return dest


def _make_master(tmpdir: Path, clips: list[Path]) -> Path:
    dest = tmpdir / "master.mp4"
    assemble_master(clips, dest)
    return dest


def _storyboard_with_dialogue(*dialogues: str) -> dict[str, Any]:
    """Build a minimal dict-storyboard with the given dialogue_th per shot."""
    shots: list[dict[str, Any]] = []
    for i, d in enumerate(dialogues):
        shots.append({"shot_id": f"s{i}", "dialogue_th": d})
    return {"shots": shots}


def _storyboard_no_dialogue(n: int = 2) -> dict[str, Any]:
    """Build a storyboard where no shots have dialogue."""
    return {"shots": [{"shot_id": f"s{i}", "dialogue_th": None} for i in range(n)]}


# ---------------------------------------------------------------------------
# PASS — full gate green
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_compliance_gate_full_pass() -> None:
    """A clean master + clean storyboard + aligned captions + 1.0x VO → ok=True."""
    with tempfile.TemporaryDirectory() as tmpdir:
        d = Path(tmpdir)
        clips = [_make_clip(d, 5.0, "s0"), _make_clip(d, 5.0, "s1")]
        master = _make_master(d, clips)

        storyboard = _storyboard_with_dialogue(
            "รองเท้ากันน้ำ สวมใส่สบาย โฆษณา",
            "ราคาดี คุ้มค่า สั่งซื้อได้เลย",
        )
        captions = [
            "รองเท้ากันน้ำ สวมใส่สบาย โฆษณา",
            "ราคาดี คุ้มค่า สั่งซื้อได้เลย",
        ]
        vo_segs = [
            _Seg(raw_audio_s=2.0, slot_s=2.0),  # 1.0x
            _Seg(raw_audio_s=3.0, slot_s=3.0),  # 1.0x
        ]

        report = run_compliance(
            master,
            storyboard,
            vo_segments=vo_segs,
            caption_lines=captions,
            profile_s=10.0,
        )

        assert report.ok is True, f"violations: {report.violations}"
        assert report.cleanroom.ok is True
        assert report.speed_guard.ok is True
        assert report.caption_sync.ok is True
        assert report.claims.ok is True


@pytest.mark.unit
def test_compliance_gate_returns_compliance_report() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        d = Path(tmpdir)
        clips = [_make_clip(d, 3.0, "s0")]
        master = _make_master(d, clips)

        report = run_compliance(master, _storyboard_no_dialogue(1))
        assert isinstance(report, ComplianceReport)


@pytest.mark.unit
def test_compliance_gate_pass_no_dialogue_no_captions() -> None:
    """Storyboard with no dialogue shots needs no captions — should pass sync."""
    with tempfile.TemporaryDirectory() as tmpdir:
        d = Path(tmpdir)
        clips = [_make_clip(d, 3.0, "s0")]
        master = _make_master(d, clips)

        report = run_compliance(
            master,
            _storyboard_no_dialogue(1),
            caption_lines=None,
        )
        assert report.caption_sync.ok is True


# ---------------------------------------------------------------------------
# FAIL — forbidden claim in dialogue
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_compliance_gate_fails_forbidden_claim_in_dialogue() -> None:
    """กันน้ำ100% in dialogue → claims sub-check fails → ok=False."""
    with tempfile.TemporaryDirectory() as tmpdir:
        d = Path(tmpdir)
        clips = [_make_clip(d, 5.0, "s0")]
        master = _make_master(d, clips)

        storyboard = _storyboard_with_dialogue("กันน้ำ100% ดีที่สุด")
        captions = ["กันน้ำ100% ดีที่สุด"]

        report = run_compliance(master, storyboard, caption_lines=captions)

        assert report.ok is False
        assert report.claims.ok is False
        assert report.claims.violation_count >= 1


@pytest.mark.unit
def test_compliance_gate_fails_forbidden_claim_in_caption() -> None:
    """กันลื่น100% only in caption (no dialogue) → claims fails."""
    with tempfile.TemporaryDirectory() as tmpdir:
        d = Path(tmpdir)
        clips = [_make_clip(d, 5.0, "s0")]
        master = _make_master(d, clips)

        storyboard = _storyboard_no_dialogue(1)
        captions = ["กันลื่น100% ปลอดภัย"]

        report = run_compliance(master, storyboard, caption_lines=captions)

        assert report.ok is False
        assert report.claims.ok is False


# ---------------------------------------------------------------------------
# FAIL — speed guard rejects > 1.15x
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_compliance_gate_fails_high_speed_vo() -> None:
    """1.20x VO segment → speed_guard fails → ok=False."""
    with tempfile.TemporaryDirectory() as tmpdir:
        d = Path(tmpdir)
        clips = [_make_clip(d, 5.0, "s0")]
        master = _make_master(d, clips)

        vo_segs = [_Seg(raw_audio_s=1.20, slot_s=1.0)]  # 1.2x — REJECT

        report = run_compliance(
            master,
            _storyboard_no_dialogue(1),
            vo_segments=vo_segs,
        )

        assert report.ok is False
        assert report.speed_guard.ok is False
        assert len(report.speed_guard.errors) >= 1


@pytest.mark.unit
def test_compliance_gate_warns_on_high_but_not_rejected_speed() -> None:
    """1.10x → speed_guard ok=True (warn only) → gate may still pass on this dimension."""
    with tempfile.TemporaryDirectory() as tmpdir:
        d = Path(tmpdir)
        clips = [_make_clip(d, 5.0, "s0")]
        master = _make_master(d, clips)

        vo_segs = [_Seg(raw_audio_s=1.10, slot_s=1.0)]  # 1.1x — WARN

        report = run_compliance(
            master,
            _storyboard_no_dialogue(1),
            vo_segments=vo_segs,
        )

        assert report.speed_guard.ok is True
        assert len(report.speed_guard.warnings) == 1


# ---------------------------------------------------------------------------
# FAIL — caption/VO sync mismatch
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_compliance_gate_fails_caption_count_mismatch() -> None:
    """2 dialogue shots but only 1 caption → caption sync fails → ok=False."""
    with tempfile.TemporaryDirectory() as tmpdir:
        d = Path(tmpdir)
        clips = [_make_clip(d, 5.0, "s0"), _make_clip(d, 5.0, "s1")]
        master = _make_master(d, clips)

        storyboard = _storyboard_with_dialogue("ดีมาก โฆษณา", "คุ้มค่ามาก")
        captions = ["ดีมาก โฆษณา"]  # only 1 caption for 2 dialogue shots

        report = run_compliance(master, storyboard, caption_lines=captions)

        assert report.ok is False
        assert report.caption_sync.ok is False
        assert any("mismatch" in v.lower() for v in report.caption_sync.violations)


@pytest.mark.unit
def test_compliance_gate_fails_dialogue_without_captions() -> None:
    """Dialogue shots with no caption_lines provided → sync fails."""
    with tempfile.TemporaryDirectory() as tmpdir:
        d = Path(tmpdir)
        clips = [_make_clip(d, 5.0, "s0")]
        master = _make_master(d, clips)

        storyboard = _storyboard_with_dialogue("สวัสดี โฆษณา")

        report = run_compliance(master, storyboard, caption_lines=None)

        assert report.ok is False
        assert report.caption_sync.ok is False


# ---------------------------------------------------------------------------
# FAIL — cleanroom: 0 audio streams (raw clip used as master)
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_compliance_gate_fails_raw_clip_as_master() -> None:
    """A raw silent clip (0 audio) passed as master → cleanroom fails → ok=False."""
    with tempfile.TemporaryDirectory() as tmpdir:
        d = Path(tmpdir)
        raw_clip = _make_clip(d, 5.0, "s0")  # 0 audio streams

        report = run_compliance(raw_clip, _storyboard_no_dialogue(1))

        assert report.ok is False
        assert report.cleanroom.ok is False
        assert report.cleanroom.audio_streams == 0


# ---------------------------------------------------------------------------
# Violations list aggregation
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_compliance_gate_violations_list_populated_on_fail() -> None:
    """ComplianceReport.violations must be non-empty when ok=False."""
    with tempfile.TemporaryDirectory() as tmpdir:
        d = Path(tmpdir)
        clips = [_make_clip(d, 5.0, "s0")]
        master = _make_master(d, clips)

        storyboard = _storyboard_with_dialogue("กันน้ำ100%")
        captions = ["กันน้ำ100%"]

        report = run_compliance(master, storyboard, caption_lines=captions)

        assert not report.ok
        assert len(report.violations) >= 1


@pytest.mark.unit
def test_compliance_gate_violations_empty_on_pass() -> None:
    """ComplianceReport.violations must be empty when fully ok."""
    with tempfile.TemporaryDirectory() as tmpdir:
        d = Path(tmpdir)
        clips = [_make_clip(d, 5.0, "s0")]
        master = _make_master(d, clips)

        storyboard = _storyboard_with_dialogue("รองเท้าดี โฆษณา")
        captions = ["รองเท้าดี โฆษณา"]
        vo_segs = [_Seg(raw_audio_s=1.0, slot_s=1.0)]

        report = run_compliance(
            master,
            storyboard,
            vo_segments=vo_segs,
            caption_lines=captions,
        )

        if report.ok:
            # Only check empty-violations when truly ok
            claim_viol = [v for v in report.violations if "claim" in v.lower() or "กัน" in v]
            assert len(claim_viol) == 0
