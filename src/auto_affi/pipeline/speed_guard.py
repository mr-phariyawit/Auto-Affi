"""Voice-over speed guard — pure logic, no I/O.

Checks each VO segment's speed factor (raw_audio_s / slot_s) against
the production principle thresholds:

  - > 1.08x → WARNING  (voice sounds slightly rushed)
  - > 1.15x → ERROR / REJECT  (voice is unacceptably rushed; rewrite line)

See docs/principles/2026-06-03-production-review-principle.md §6 for
the policy (preferred 1.0x, warn >1.08x, reject >1.15x).
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from pydantic import BaseModel, Field

# Threshold constants from the production principle
_WARN_THRESHOLD: float = 1.08
_REJECT_THRESHOLD: float = 1.15


# ---------------------------------------------------------------------------
# Input protocol — accepts any object with raw_audio_s + slot_s
# ---------------------------------------------------------------------------


@runtime_checkable
class VoSegment(Protocol):
    """Anything with a raw audio duration and a timeline slot duration."""

    raw_audio_s: float
    slot_s: float


# ---------------------------------------------------------------------------
# Report model
# ---------------------------------------------------------------------------


class SpeedGuardReport(BaseModel):
    """Result of :func:`check_speed`."""

    ok: bool
    warnings: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
    max_factor: float = 0.0


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def check_speed(segments: list[VoSegment]) -> SpeedGuardReport:
    """Evaluate each segment's speed factor and return a :class:`SpeedGuardReport`.

    Parameters
    ----------
    segments
        List of objects with ``raw_audio_s`` (natural speech duration) and
        ``slot_s`` (timeline slot available). Each factor is computed as
        ``raw_audio_s / slot_s``. A factor > 1 means the audio must be
        sped up to fit.

    Returns
    -------
    SpeedGuardReport
        ``ok=False`` if any segment exceeds the reject threshold (>1.15x).
        Warnings are collected separately for segments between 1.08-1.15x.
    """
    warnings: list[str] = []
    errors: list[str] = []
    max_factor: float = 0.0

    for idx, seg in enumerate(segments):
        if seg.slot_s <= 0:
            errors.append(f"segment[{idx}]: slot_s must be > 0, got {seg.slot_s}")
            continue

        factor = seg.raw_audio_s / seg.slot_s
        max_factor = max(max_factor, factor)

        label = f"segment[{idx}] factor={factor:.3f}x (raw={seg.raw_audio_s}s, slot={seg.slot_s}s)"

        if factor > _REJECT_THRESHOLD:
            errors.append(f"REJECT {label} — exceeds {_REJECT_THRESHOLD}x hard limit")
        elif factor > _WARN_THRESHOLD:
            warnings.append(f"WARN {label} — exceeds {_WARN_THRESHOLD}x warn threshold")

    return SpeedGuardReport(
        ok=len(errors) == 0,
        warnings=warnings,
        errors=errors,
        max_factor=max_factor,
    )
