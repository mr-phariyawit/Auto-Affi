"""Unit tests for the Pre-Generation Audit + Approval Gate (SPEC §10.5 g10-12)."""

from __future__ import annotations

from pathlib import Path

import pytest

from auto_affi.pipeline.prompt_audit import (
    STAGES,
    AuditCode,
    GenerationBlocked,
    ReferenceManifest,
    assert_may_generate,
    audit,
    load_approvals,
    prompt_hash,
    record_approval,
    record_audit,
    record_bypass,
)

_IDENTITY = "JIAP02, lean athletic Southeast Asian male, V-line jaw"


def _clean_manifest(**overrides: object) -> ReferenceManifest:
    base: dict[str, object] = {
        "prompt": f"{_IDENTITY}. He holds a purple hula hoop in a sunlit room.",
        "identity_string": _IDENTITY,
        "cast_sheet_approved": True,
        "objects_sheet_approved": True,
        "declared_objects": ["purple hula hoop"],
        "scene_objects": ["purple hula hoop"],
        "face_reference_count": 1,
        "negative_prompt": "different person, wrong face, extra limbs, text, watermark",
        "aspect": "9:16",
        "resolution": "720p",
        "duration_s": 8.0,
        "soul_id": "soul-jiap02",
        "thai_no_lipsync": True,
        "visibly_speaking_thai_mouth": False,
        "has_banned_claims": False,
        "category_restricted": False,
        "economics_passed": True,
    }
    base.update(overrides)
    return ReferenceManifest(**base)  # type: ignore[arg-type]


# --------------------------- audit checklist ----------------------------- #


@pytest.mark.unit
def test_audit_passes_on_clean_manifest() -> None:
    result = audit(_clean_manifest())
    assert result.passed is True
    assert result.failures == []
    assert len(result.prompt_hash) == 64  # sha256 hex


@pytest.mark.unit
def test_audit_fails_when_identity_string_absent_from_prompt() -> None:
    result = audit(_clean_manifest(prompt="He holds a hula hoop in a room."))
    assert result.passed is False
    assert AuditCode.IDENTITY_STRING_MISSING in {f.code for f in result.failures}


@pytest.mark.unit
def test_audit_fails_on_stray_object_not_on_objects_sheet() -> None:
    result = audit(_clean_manifest(scene_objects=["purple hula hoop", "foam roller"]))
    codes = {f.code for f in result.failures}
    assert AuditCode.STRAY_OBJECT in codes


@pytest.mark.unit
def test_audit_fails_on_second_face_reference() -> None:
    result = audit(_clean_manifest(face_reference_count=2))
    assert AuditCode.FACE_REFERENCE_NOT_SINGLE in {f.code for f in result.failures}


@pytest.mark.unit
def test_audit_fails_on_missing_negative_prompt() -> None:
    result = audit(_clean_manifest(negative_prompt="   "))
    assert AuditCode.NEGATIVE_PROMPT_MISSING in {f.code for f in result.failures}


@pytest.mark.unit
def test_audit_fails_on_wrong_aspect() -> None:
    result = audit(_clean_manifest(aspect="16:9"))
    assert AuditCode.ASPECT_INVALID in {f.code for f in result.failures}


@pytest.mark.unit
def test_audit_fails_without_deterministic_anchor() -> None:
    result = audit(_clean_manifest(soul_id=None, seed=None))
    assert AuditCode.NO_DETERMINISTIC_ANCHOR in {f.code for f in result.failures}


@pytest.mark.unit
def test_audit_fails_on_thai_lipsync_violation() -> None:
    result = audit(_clean_manifest(visibly_speaking_thai_mouth=True))
    assert AuditCode.THAI_LIPSYNC_VIOLATION in {f.code for f in result.failures}


@pytest.mark.unit
def test_audit_fails_on_compliance_flags() -> None:
    result = audit(
        _clean_manifest(
            has_banned_claims=True,
            category_restricted=True,
            economics_passed=False,
        )
    )
    codes = {f.code for f in result.failures}
    assert {
        AuditCode.BANNED_CLAIMS,
        AuditCode.CATEGORY_RESTRICTED,
        AuditCode.ECONOMICS_NOT_PASSED,
    } <= codes


# --------------------------- determinism --------------------------------- #


@pytest.mark.unit
def test_prompt_hash_is_deterministic_and_input_sensitive() -> None:
    m = _clean_manifest()
    assert prompt_hash(m) == prompt_hash(_clean_manifest())  # same inputs -> same hash
    assert prompt_hash(m) != prompt_hash(_clean_manifest(prompt=m.prompt + " extra"))


# --------------------- approval gate state machine ----------------------- #


@pytest.mark.unit
def test_generation_blocked_without_approval(tmp_path: Path) -> None:
    record_audit(tmp_path, "cast_sheet", audit(_clean_manifest()))
    with pytest.raises(GenerationBlocked):
        assert_may_generate("cast_sheet", tmp_path)


@pytest.mark.unit
def test_generation_allowed_after_audit_and_approval(tmp_path: Path) -> None:
    record_audit(tmp_path, "cast_sheet", audit(_clean_manifest()))
    record_approval(tmp_path, "cast_sheet", approved_by="human")
    assert_may_generate("cast_sheet", tmp_path)  # does not raise


@pytest.mark.unit
def test_cannot_approve_a_failed_audit(tmp_path: Path) -> None:
    record_audit(tmp_path, "cast_sheet", audit(_clean_manifest(aspect="16:9")))
    with pytest.raises(GenerationBlocked):
        record_approval(tmp_path, "cast_sheet")


@pytest.mark.unit
def test_stage_ordering_enforced(tmp_path: Path) -> None:
    # video cannot generate until earlier stages are approved/bypassed.
    record_audit(tmp_path, "video", audit(_clean_manifest()))
    record_approval(tmp_path, "video")
    with pytest.raises(GenerationBlocked, match="prior stage"):
        assert_may_generate("video", tmp_path)


@pytest.mark.unit
def test_explicit_bypass_overrides_and_is_logged(tmp_path: Path) -> None:
    record_bypass(tmp_path, "cast_sheet", reason="hand-made sheet, trusted", by="human")
    # bypass clears the gate even with no audit/approval recorded.
    assert_may_generate("cast_sheet", tmp_path)
    approvals = load_approvals(tmp_path)
    assert approvals["cast_sheet"].bypassed is True
    assert approvals["cast_sheet"].bypass_reason == "hand-made sheet, trusted"
    log = (tmp_path / "audit_events.jsonl").read_text()
    assert "bypass" in log and "cast_sheet" in log


@pytest.mark.unit
def test_input_change_invalidates_downstream_approvals(tmp_path: Path) -> None:
    # Approve cast_sheet, then re-audit it with a changed prompt -> approval void.
    record_audit(tmp_path, "cast_sheet", audit(_clean_manifest()))
    record_approval(tmp_path, "cast_sheet")
    assert load_approvals(tmp_path)["cast_sheet"].approved is True

    changed = audit(_clean_manifest(prompt="totally different scene " + _IDENTITY))
    record_audit(tmp_path, "cast_sheet", changed)
    assert load_approvals(tmp_path)["cast_sheet"].approved is False
    with pytest.raises(GenerationBlocked):
        assert_may_generate("cast_sheet", tmp_path)


@pytest.mark.unit
def test_stages_constant_order() -> None:
    assert STAGES == (
        "cast_sheet",
        "objects_sheet",
        "storyboard",
        "contact_sheet",
        "video",
    )
