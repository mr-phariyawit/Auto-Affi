"""Pre-Generation Audit (PGA) + Approval Gate — machine-enforced.

Codifies SPEC §10.5 gates 10 (PGA), 11 (Reference-Sheet Lock), 12 (Generation
Lock) and ``docs/principles/2026-06-27-pre-generation-audit-and-approval-gate.md``.

Three laws:
  1. AUDIT ALWAYS  — :func:`audit` checks a prompt + reference manifest against the
     PGA checklist (sections A-D) before any image/video generation.
  2. DETERMINISTIC — :func:`prompt_hash` makes identical approved inputs reproduce
     one hash; a changed hash invalidates that stage's approval and all downstream.
  3. NO GEN WITHOUT APPROVAL — :func:`assert_may_generate` blocks generation unless
     the stage passed audit AND was human-approved (or explicitly bypassed), and
     enforces stage ordering.
"""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path

from pydantic import BaseModel, Field

# Ordered generation stages; a later stage may not run until every earlier stage
# is approved or explicitly bypassed.
STAGES: tuple[str, ...] = (
    "cast_sheet",
    "objects_sheet",
    "storyboard",
    "contact_sheet",
    "video",
)

ALLOWED_ASPECT: str = "9:16"
_APPROVALS_FILENAME: str = "approvals.json"
_EVENTS_FILENAME: str = "audit_events.jsonl"


class AuditCode(StrEnum):
    """Stable identifiers for each PGA checklist failure."""

    CAST_SHEET_NOT_APPROVED = "cast_sheet_not_approved"
    OBJECTS_SHEET_NOT_APPROVED = "objects_sheet_not_approved"
    IDENTITY_STRING_MISSING = "identity_string_missing"
    STRAY_OBJECT = "stray_object"
    FACE_REFERENCE_NOT_SINGLE = "face_reference_not_single"
    NEGATIVE_PROMPT_MISSING = "negative_prompt_missing"
    ASPECT_INVALID = "aspect_invalid"
    DURATION_INVALID = "duration_invalid"
    NO_DETERMINISTIC_ANCHOR = "no_deterministic_anchor"
    THAI_LIPSYNC_VIOLATION = "thai_lipsync_violation"
    BANNED_CLAIMS = "banned_claims"
    CATEGORY_RESTRICTED = "category_restricted"
    ECONOMICS_NOT_PASSED = "economics_not_passed"


class AuditFailure(BaseModel):
    """One failing checklist item."""

    code: AuditCode
    section: str  # "A".."D"
    detail: str


class ReferenceManifest(BaseModel):
    """Everything the PGA needs to audit one generation prompt."""

    prompt: str
    identity_string: str
    cast_sheet_approved: bool
    objects_sheet_approved: bool
    declared_objects: list[str] = Field(default_factory=list)
    scene_objects: list[str] = Field(default_factory=list)
    face_reference_count: int
    reference_uris: list[str] = Field(
        default_factory=list,
        description="Actual reference-image URIs/paths fed to the generator; hashed so swapping a "
        "reference invalidates approval (Audit Lead GAP-5).",
    )
    negative_prompt: str
    aspect: str
    resolution: str
    duration_s: float
    seed: int | None = None
    soul_id: str | None = None
    thai_no_lipsync: bool = True
    visibly_speaking_thai_mouth: bool = False
    has_banned_claims: bool = False
    category_restricted: bool = False
    economics_passed: bool = True
    max_duration_s: float = 10.0


class AuditResult(BaseModel):
    """Outcome of a PGA evaluation."""

    passed: bool
    failures: list[AuditFailure]
    prompt_hash: str


class StageApproval(BaseModel):
    """Per-stage approval state persisted to ``runs/<run>/approvals.json``."""

    audited: bool = False
    audit_pass: bool = False
    approved: bool = False
    approved_by: str | None = None
    approved_at: str | None = None
    bypassed: bool = False
    bypass_reason: str | None = None
    prompt_hash: str | None = None


class GenerationBlocked(RuntimeError):
    """Raised when a generation is attempted without a cleared gate."""

    def __init__(self, stage: str, reason: str) -> None:
        self.stage = stage
        self.reason = reason
        super().__init__(f"generation blocked at stage '{stage}': {reason}")


# --------------------------------------------------------------------------- #
# Determinism
# --------------------------------------------------------------------------- #


def prompt_hash(manifest: ReferenceManifest) -> str:
    """SHA-256 over the generation-determining fields of a manifest.

    Identical approved inputs reproduce the same hash; any change to a field that
    affects the output changes the hash (and therefore invalidates approval).
    """
    payload = {
        "prompt": manifest.prompt,
        "identity_string": manifest.identity_string,
        "declared_objects": sorted(manifest.declared_objects),
        "scene_objects": sorted(manifest.scene_objects),
        "negative_prompt": manifest.negative_prompt,
        "aspect": manifest.aspect,
        "resolution": manifest.resolution,
        "duration_s": manifest.duration_s,
        "seed": manifest.seed,
        "soul_id": manifest.soul_id,
        "face_reference_count": manifest.face_reference_count,
        "reference_uris": sorted(manifest.reference_uris),
    }
    canonical = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


# --------------------------------------------------------------------------- #
# Audit (gate 10)
# --------------------------------------------------------------------------- #


def audit(manifest: ReferenceManifest) -> AuditResult:
    """Evaluate the PGA checklist (sections A-D). Any failure => not passed."""
    failures: list[AuditFailure] = []

    def fail(code: AuditCode, section: str, detail: str) -> None:
        failures.append(AuditFailure(code=code, section=section, detail=detail))

    # --- A. Reference lock --------------------------------------------- #
    if not manifest.cast_sheet_approved:
        fail(AuditCode.CAST_SHEET_NOT_APPROVED, "A", "cast/character sheet not approved")
    if not manifest.objects_sheet_approved:
        fail(AuditCode.OBJECTS_SHEET_NOT_APPROVED, "A", "objects/props sheet not approved")
    if not manifest.identity_string or manifest.identity_string not in manifest.prompt:
        fail(
            AuditCode.IDENTITY_STRING_MISSING,
            "A",
            "canonical identity string not injected verbatim into the prompt",
        )

    # --- B. Prompt standard -------------------------------------------- #
    stray = sorted(set(manifest.scene_objects) - set(manifest.declared_objects))
    if stray:
        fail(AuditCode.STRAY_OBJECT, "B", f"objects not on the approved objects sheet: {stray}")
    if manifest.face_reference_count != 1:
        fail(
            AuditCode.FACE_REFERENCE_NOT_SINGLE,
            "B",
            f"exactly one face reference required, got {manifest.face_reference_count}",
        )
    if not manifest.negative_prompt.strip():
        fail(AuditCode.NEGATIVE_PROMPT_MISSING, "B", "negative prompt is empty")
    if manifest.aspect != ALLOWED_ASPECT:
        fail(AuditCode.ASPECT_INVALID, "B", f"aspect must be {ALLOWED_ASPECT}, got {manifest.aspect}")
    if not 0.0 < manifest.duration_s <= manifest.max_duration_s:
        fail(
            AuditCode.DURATION_INVALID,
            "B",
            f"duration {manifest.duration_s}s out of (0, {manifest.max_duration_s}]",
        )
    if manifest.seed is None and not manifest.soul_id:
        fail(
            AuditCode.NO_DETERMINISTIC_ANCHOR,
            "B",
            "no seed or soul_id locked for cross-shot determinism",
        )
    if manifest.thai_no_lipsync and manifest.visibly_speaking_thai_mouth:
        fail(
            AuditCode.THAI_LIPSYNC_VIOLATION,
            "B",
            "visibly-speaking Thai mouth violates the VO-over-B-roll constraint",
        )

    # --- C. Compliance -------------------------------------------------- #
    if manifest.has_banned_claims:
        fail(AuditCode.BANNED_CLAIMS, "C", "prompt carries banned (medical/financial/guaranteed) claims")
    if manifest.category_restricted:
        fail(AuditCode.CATEGORY_RESTRICTED, "C", "product category is restricted")
    if not manifest.economics_passed:
        fail(AuditCode.ECONOMICS_NOT_PASSED, "C", "product did not pass the Scout economics gate")

    return AuditResult(passed=not failures, failures=failures, prompt_hash=prompt_hash(manifest))


# --------------------------------------------------------------------------- #
# Approval state (gates 11 & 12)
# --------------------------------------------------------------------------- #


def _approvals_path(run_dir: Path) -> Path:
    return Path(run_dir) / _APPROVALS_FILENAME


def load_approvals(run_dir: Path) -> dict[str, StageApproval]:
    """Load per-stage approvals, defaulting any missing stage to a fresh state."""
    path = _approvals_path(run_dir)
    raw: dict[str, object] = {}
    if path.exists():
        loaded = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(loaded, dict):
            raw = loaded
    return {stage: StageApproval.model_validate(raw.get(stage, {})) for stage in STAGES}


def save_approvals(run_dir: Path, approvals: dict[str, StageApproval]) -> None:
    Path(run_dir).mkdir(parents=True, exist_ok=True)
    data = {stage: approvals[stage].model_dump() for stage in STAGES}
    _approvals_path(run_dir).write_text(
        json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def _log_event(run_dir: Path, event: dict[str, str]) -> None:
    Path(run_dir).mkdir(parents=True, exist_ok=True)
    line = json.dumps(event, ensure_ascii=False)
    with (Path(run_dir) / _EVENTS_FILENAME).open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def _invalidate_from(approvals: dict[str, StageApproval], stage: str) -> None:
    """Reset the given stage and every downstream stage to a fresh state."""
    for downstream in STAGES[STAGES.index(stage) :]:
        approvals[downstream] = StageApproval()


def record_audit(run_dir: Path, stage: str, result: AuditResult) -> dict[str, StageApproval]:
    """Record an audit. If the prompt hash changed for an already-recorded stage,
    invalidate its (and all downstream) approvals first (determinism / gate 11).
    """
    if stage not in STAGES:
        raise ValueError(f"unknown stage: {stage!r}")
    approvals = load_approvals(run_dir)
    existing = approvals[stage]
    if existing.prompt_hash is not None and existing.prompt_hash != result.prompt_hash:
        _invalidate_from(approvals, stage)
    st = approvals[stage]
    st.audited = True
    st.audit_pass = result.passed
    st.prompt_hash = result.prompt_hash
    save_approvals(run_dir, approvals)
    return approvals


def record_approval(run_dir: Path, stage: str, approved_by: str = "human") -> dict[str, StageApproval]:
    """Mark a stage human-approved. Refuses to approve an un-audited/failed stage."""
    if stage not in STAGES:
        raise ValueError(f"unknown stage: {stage!r}")
    approvals = load_approvals(run_dir)
    st = approvals[stage]
    if not st.audited or not st.audit_pass:
        raise GenerationBlocked(stage, "cannot approve a stage that has not passed audit")
    st.approved = True
    st.approved_by = approved_by
    st.approved_at = _now_iso()
    save_approvals(run_dir, approvals)
    return approvals


def record_bypass(
    run_dir: Path, stage: str, reason: str, by: str = "human"
) -> dict[str, StageApproval]:
    """Explicit human override for one stage. Logged to ``audit_events.jsonl``."""
    if stage not in STAGES:
        raise ValueError(f"unknown stage: {stage!r}")
    approvals = load_approvals(run_dir)
    st = approvals[stage]
    st.bypassed = True
    st.bypass_reason = reason
    st.approved_by = by
    st.approved_at = _now_iso()
    save_approvals(run_dir, approvals)
    _log_event(
        run_dir,
        {"event": "bypass", "stage": stage, "reason": reason, "by": by, "at": _now_iso()},
    )
    return approvals


def assert_may_generate(
    stage: str, run_dir: Path, *, manifest: ReferenceManifest | None = None
) -> None:
    """Block generation unless the stage is cleared and stage ordering holds.

    Cleared = ``bypassed`` OR (``audit_pass`` AND ``approved``). Every earlier
    stage must itself be approved or bypassed.

    When ``manifest`` is supplied, the gate BINDS the approval to the exact
    content being generated: it recomputes the prompt hash and rejects unless it
    equals the approved hash. Without this binding the audit is decoupled from the
    generation (Audit Lead GAP-1) — approving a clean manifest then generating
    something else would otherwise pass.
    """
    if stage not in STAGES:
        raise ValueError(f"unknown stage: {stage!r}")
    approvals = load_approvals(run_dir)
    idx = STAGES.index(stage)

    for prior in STAGES[:idx]:
        prev = approvals[prior]
        if not (prev.approved or prev.bypassed):
            raise GenerationBlocked(stage, f"prior stage '{prior}' not approved/bypassed")

    st = approvals[stage]
    if st.bypassed:
        return
    if not st.audited or not st.audit_pass:
        raise GenerationBlocked(stage, "stage not audited or audit failed")
    if not st.approved:
        raise GenerationBlocked(stage, "stage not approved by human")
    if manifest is not None and prompt_hash(manifest) != st.prompt_hash:
        raise GenerationBlocked(
            stage,
            "prompt/reference changed since approval (hash mismatch) — re-audit and re-approve",
        )
