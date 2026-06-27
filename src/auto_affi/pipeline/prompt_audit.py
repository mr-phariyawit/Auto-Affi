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


# Failures that a human `bypass` may NEVER override — bypass is for trusting a
# hand-made artifact, not for waving through banned claims / restricted goods /
# unviable economics (Audit Lead gap #6).
HARD_COMPLIANCE_CODES: frozenset[AuditCode] = frozenset(
    {AuditCode.BANNED_CLAIMS, AuditCode.CATEGORY_RESTRICTED, AuditCode.ECONOMICS_NOT_PASSED}
)


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
    audit_failure_codes: list[str] = Field(default_factory=list)
    hard_block: bool = False


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


def _read_events(run_dir: Path) -> list[dict[str, str]]:
    path = Path(run_dir) / _EVENTS_FILENAME
    if not path.exists():
        return []
    events: list[dict[str, str]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        parsed = json.loads(line)
        if isinstance(parsed, dict):
            events.append(parsed)
    return events


def _latest_event_index(events: list[dict[str, str]], *, event: str, stage: str) -> int | None:
    found: int | None = None
    for i, ev in enumerate(events):
        if ev.get("event") == event and ev.get("stage") == stage:
            found = i
    return found


def _hard_blocked(run_dir: Path, stage: str) -> bool:
    """True if the LATEST audit event for the stage latched a hard-compliance block.

    Reads the append-only log (not the forgeable approvals.json) so editing
    approvals.json cannot launder a banned/restricted/unviable stage. The latch
    is sticky across same-hash re-audits and only resets when the prompt hash
    changes (a genuinely different artifact), which records a fresh audit event.
    """
    events = _read_events(run_dir)
    idx = _latest_event_index(events, event="audit", stage=stage)
    return idx is not None and events[idx].get("hard_block") == "true"


def _latest_event(run_dir: Path, *, event: str, stage: str) -> dict[str, str] | None:
    events = _read_events(run_dir)
    idx = _latest_event_index(events, event=event, stage=stage)
    return events[idx] if idx is not None else None


def _bypass_is_current(run_dir: Path, stage: str) -> bool:
    """True only if a bypass event post-dates the latest audit event for the stage.

    Mirrors :func:`_approval_is_current` for the bypass path — defeats stale
    bypass-event replay after a hash-invalidating re-audit.
    """
    events = _read_events(run_dir)
    last_audit = _latest_event_index(events, event="audit", stage=stage)
    last_bypass = _latest_event_index(events, event="bypass", stage=stage)
    if last_bypass is None:
        return False
    return last_audit is None or last_bypass > last_audit


def _approval_is_current(run_dir: Path, stage: str, prompt_hash: str | None) -> bool:
    """True only if an approve event for this exact hash POST-DATES the latest
    audit event for the stage.

    Defeats stale-event replay: reverting to a previously-approved hash fails
    because a newer audit event sits after the old approve event in the
    append-only log. (Limit: appending a forged approve event still passes —
    that needs cryptographic signing; documented in the threat model.)
    """
    events = _read_events(run_dir)
    last_audit = _latest_event_index(events, event="audit", stage=stage)
    approve_idx: int | None = None
    for i, ev in enumerate(events):
        if ev.get("event") == "approve" and ev.get("stage") == stage and ev.get("prompt_hash") == prompt_hash:
            approve_idx = i
    if approve_idx is None:
        return False
    return last_audit is None or approve_idx > last_audit


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
    st.audit_failure_codes = [f.code.value for f in result.failures]
    # Sticky hard-compliance latch: once banned/restricted/unviable is seen for
    # this artifact, a clean same-hash re-audit cannot launder it (gap #6). The
    # latch only resets when the hash changed above (genuinely different content).
    new_hard = any(code in HARD_COMPLIANCE_CODES for code in st.audit_failure_codes)
    st.hard_block = st.hard_block or new_hard
    save_approvals(run_dir, approvals)
    # The append-only log is the gate's source of truth (not the mutable JSON).
    _log_event(
        run_dir,
        {
            "event": "audit",
            "stage": stage,
            "prompt_hash": result.prompt_hash,
            "audit_pass": "true" if result.passed else "false",
            "hard_block": "true" if st.hard_block else "false",
            "at": _now_iso(),
        },
    )
    return approvals


def record_approval(
    run_dir: Path, stage: str, approved_by: str = "human", *, approval_token: str | None = None
) -> dict[str, StageApproval]:
    """Mark a stage human-approved. Refuses to approve an un-audited/failed stage.

    Writes a matching ``approve`` event to the append-only log so the approval is
    tamper-evident (a JSON-only forge has no event). ``approved_by`` SHOULD name a
    real approver source (e.g. ``operator:alice``); ``approval_token`` carries an
    out-of-band token when an approval channel issues one.
    """
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
    _log_event(
        run_dir,
        {
            "event": "approve",
            "stage": stage,
            "prompt_hash": st.prompt_hash or "",
            "by": approved_by,
            "token": approval_token or "",
            "at": _now_iso(),
        },
    )
    return approvals


def record_bypass(
    run_dir: Path, stage: str, reason: str, by: str = "human"
) -> dict[str, StageApproval]:
    """Explicit human override for one stage. Logged to ``audit_events.jsonl``.

    A bypass may NOT override a hard-compliance audit failure (banned claims /
    restricted category / failed economics) — those raise (Audit Lead gap #6).
    """
    if stage not in STAGES:
        raise ValueError(f"unknown stage: {stage!r}")
    approvals = load_approvals(run_dir)
    st = approvals[stage]
    if _hard_blocked(run_dir, stage):
        raise GenerationBlocked(
            stage,
            f"cannot bypass a hard-compliance audit failure: {st.audit_failure_codes}",
        )
    st.bypassed = True
    st.bypass_reason = reason
    st.approved_by = by
    st.approved_at = _now_iso()
    save_approvals(run_dir, approvals)
    _log_event(
        run_dir,
        {
            "event": "bypass",
            "stage": stage,
            "reason": reason,
            "by": by,
            "prompt_hash": st.prompt_hash or "",
            "at": _now_iso(),
        },
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
    st = approvals[stage]

    # A hard-compliance latch on this stage can NEVER be cleared — not by
    # approval, not by bypass, regardless of prior stages. Read from the
    # append-only log so editing approvals.json cannot launder it (gap #6).
    if _hard_blocked(run_dir, stage):
        raise GenerationBlocked(
            stage, "hard-compliance audit failure cannot be cleared (see audit log)"
        )

    # Prior stages must be VALIDLY cleared too — using the same log-authoritative
    # checks as the target (Audit Lead GAP-C/GAP-D). Reading raw approvals.json
    # booleans here would let a forged JSON launder upstream stages and leak a
    # banned/restricted upstream artifact into downstream generation.
    for prior in STAGES[:idx]:
        if _hard_blocked(run_dir, prior):
            raise GenerationBlocked(
                stage, f"prior stage '{prior}' has an un-cleared hard-compliance failure"
            )
        prev = approvals[prior]
        prior_cleared = (prev.bypassed and _bypass_is_current(run_dir, prior)) or (
            prev.approved and _approval_is_current(run_dir, prior, prev.prompt_hash)
        )
        if not prior_cleared:
            raise GenerationBlocked(stage, f"prior stage '{prior}' not validly approved/bypassed")

    if st.bypassed:
        # Tamper-evidence: the bypass event must post-date the latest audit event
        # (defeats stale bypass-event replay), and — when a manifest is supplied —
        # must be bound to the exact content (a bypass trusts ONE artifact, not any).
        if not _bypass_is_current(run_dir, stage):
            raise GenerationBlocked(
                stage, "no matching current bypass event in the audit log (tamper / superseded)"
            )
        if manifest is not None:
            ev = _latest_event(run_dir, event="bypass", stage=stage)
            if (ev or {}).get("prompt_hash", "") != prompt_hash(manifest):
                raise GenerationBlocked(
                    stage, "prompt/reference changed since bypass (hash mismatch)"
                )
        return
    if not st.audited or not st.audit_pass:
        raise GenerationBlocked(stage, "stage not audited or audit failed")
    if not st.approved:
        raise GenerationBlocked(stage, "stage not approved by human")
    # Tamper-evidence: an approve event for this exact hash must POST-DATE the
    # latest audit event — defeats both the JSON-only forge and stale-event
    # replay after a hash revert (H2/H5).
    if not _approval_is_current(run_dir, stage, st.prompt_hash):
        raise GenerationBlocked(
            stage,
            "no matching current approve event in the audit log "
            "(tamper / forged or superseded approval)",
        )
    if manifest is not None and prompt_hash(manifest) != st.prompt_hash:
        raise GenerationBlocked(
            stage,
            "prompt/reference changed since approval (hash mismatch) — re-audit and re-approve",
        )
