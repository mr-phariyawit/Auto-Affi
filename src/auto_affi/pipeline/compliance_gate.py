"""Compliance gate — composed pre-publish verification pipeline.

Runs four sub-checks and surfaces a unified :class:`ComplianceReport`:

  1. **Cleanroom** — ffprobe stream/duration/resolution contract
  2. **Speed guard** — VO segment speed factor (warn >1.08x, reject >1.15x)
  3. **Caption sync** — every shot with dialogue must have a caption line;
     counts must match
  4. **Claim audit** — Thai OCPB/platform-ToS claim violations across all
     dialogue + captions; disclosure presence check

See docs/principles/2026-06-03-production-review-principle.md for policy.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from auto_affi.agents.claim_auditor import audit as claim_audit
from auto_affi.agents.claim_auditor import has_disclosure
from auto_affi.pipeline.cleanroom import CleanroomReport, verify_master
from auto_affi.pipeline.speed_guard import SpeedGuardReport, VoSegment, check_speed

# ---------------------------------------------------------------------------
# Caption sync sub-report
# ---------------------------------------------------------------------------


class CaptionSyncReport(BaseModel):
    """Result of the caption / VO alignment check."""

    ok: bool
    dialogue_shots: int = 0
    caption_lines: int = 0
    violations: list[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Claims sub-report
# ---------------------------------------------------------------------------


class ClaimsReport(BaseModel):
    """Result of the claim audit + disclosure check."""

    ok: bool
    violation_count: int = 0
    has_disclosure: bool = False
    violations: list[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Top-level report
# ---------------------------------------------------------------------------


class ComplianceReport(BaseModel):
    """Aggregated compliance gate result."""

    ok: bool
    cleanroom: CleanroomReport
    speed_guard: SpeedGuardReport
    claims: ClaimsReport
    caption_sync: CaptionSyncReport
    violations: list[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _extract_dialogue(storyboard: Any) -> list[str]:  # type: ignore[explicit-any]
    """Pull all non-empty dialogue_th strings from storyboard shots.

    Supports both ``AiStoryboard`` (with ``.shots``) and plain dicts.
    """
    texts: list[str] = []
    shots = _get_shots(storyboard)
    for shot in shots:
        if isinstance(shot, dict):
            d = shot.get("dialogue_th")
        else:
            d = getattr(shot, "dialogue_th", None)
        if d:
            texts.append(str(d))
    return texts


def _get_shots(storyboard: Any) -> list[Any]:  # type: ignore[explicit-any]
    """Return shots list from storyboard (object or dict)."""
    if isinstance(storyboard, dict):
        return storyboard.get("shots", [])  # type: ignore[no-any-return]
    return getattr(storyboard, "shots", [])  # type: ignore[no-any-return]


def _count_dialogue_shots(storyboard: Any) -> int:  # type: ignore[explicit-any]
    """Count shots that have non-empty dialogue_th."""
    count = 0
    for shot in _get_shots(storyboard):
        if isinstance(shot, dict):
            d = shot.get("dialogue_th")
        else:
            d = getattr(shot, "dialogue_th", None)
        if d:
            count += 1
    return count


# ---------------------------------------------------------------------------
# Caption sync check
# ---------------------------------------------------------------------------


def _check_caption_sync(
    storyboard: Any,  # type: ignore[explicit-any]
    caption_lines: list[str] | None,
) -> CaptionSyncReport:
    """Verify every shot with dialogue has a corresponding caption line."""
    violations: list[str] = []
    n_dialogue = _count_dialogue_shots(storyboard)
    n_captions = len(caption_lines) if caption_lines else 0

    if n_dialogue > 0 and caption_lines is None:
        violations.append(
            f"storyboard has {n_dialogue} dialogue shot(s) but no caption_lines provided"
        )
    elif n_dialogue != n_captions:
        violations.append(
            f"caption count mismatch: {n_dialogue} dialogue shot(s) "
            f"vs {n_captions} caption line(s)"
        )

    return CaptionSyncReport(
        ok=len(violations) == 0,
        dialogue_shots=n_dialogue,
        caption_lines=n_captions,
        violations=violations,
    )


# ---------------------------------------------------------------------------
# Claims check
# ---------------------------------------------------------------------------


def _check_claims(
    storyboard: Any,  # type: ignore[explicit-any]
    caption_lines: list[str] | None,
) -> ClaimsReport:
    """Run the claim auditor over all dialogue + captions."""
    # Gather all text to audit
    texts: list[str] = _extract_dialogue(storyboard)
    if caption_lines:
        texts.extend(caption_lines)

    combined = " ".join(texts)

    violations_raw = claim_audit(combined)
    blocking = [v for v in violations_raw if v.severity >= 2]

    violation_msgs: list[str] = [
        f"[{v.category}/{v.pattern_name}] severity={v.severity}: "
        f"'{v.matched_text}'"
        for v in blocking
    ]

    disclosure_present = has_disclosure(combined)

    # Lack of disclosure is advisory (severity=1 — warn, not block)
    if not disclosure_present:
        violation_msgs.append(
            "no disclosure marker found (โฆษณา / affiliate / #ad) — "
            "required before public publish"
        )

    # ok = no blocking claim violations (disclosure warning is advisory)
    ok = len(blocking) == 0

    return ClaimsReport(
        ok=ok,
        violation_count=len(blocking),
        has_disclosure=disclosure_present,
        violations=violation_msgs,
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def run_compliance(
    master_path: Path,
    storyboard: Any,  # type: ignore[explicit-any]
    *,
    source_clips: list[Path] | None = None,
    vo_segments: list[VoSegment] | None = None,
    caption_lines: list[str] | None = None,
    profile_s: float | None = None,
) -> ComplianceReport:
    """Run the full compliance gate and return a :class:`ComplianceReport`.

    Parameters
    ----------
    master_path
        Path to the final assembled mp4.
    storyboard
        An ``AiStoryboard`` instance or compatible dict with ``.shots``.
    source_clips
        Optional source clips — each must have 0 audio streams.
    vo_segments
        VO segments to check for speed (each must have ``raw_audio_s`` +
        ``slot_s``). Pass ``None`` or ``[]`` to skip.
    caption_lines
        Caption strings to align against dialogue shots and audit.
    profile_s
        Expected master duration in seconds (passed to cleanroom).

    Returns
    -------
    ComplianceReport
        ``ok=True`` only when all four sub-checks pass.
    """
    # 1. Cleanroom
    cleanroom_report = verify_master(
        master_path,
        source_clips=source_clips,
        profile_s=profile_s,
    )

    # 2. Speed guard
    speed_report = check_speed(vo_segments or [])

    # 3. Caption sync
    caption_report = _check_caption_sync(storyboard, caption_lines)

    # 4. Claims
    claims_report = _check_claims(storyboard, caption_lines)

    # Aggregate violations
    all_violations: list[str] = []
    all_violations.extend(cleanroom_report.violations)
    all_violations.extend(speed_report.errors)
    all_violations.extend(speed_report.warnings)
    all_violations.extend(caption_report.violations)
    all_violations.extend(claims_report.violations)

    ok = (
        cleanroom_report.ok
        and speed_report.ok
        and caption_report.ok
        and claims_report.ok
    )

    return ComplianceReport(
        ok=ok,
        cleanroom=cleanroom_report,
        speed_guard=speed_report,
        claims=claims_report,
        caption_sync=caption_report,
        violations=all_violations,
    )
