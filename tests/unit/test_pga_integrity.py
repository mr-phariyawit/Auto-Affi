"""PGA audit-integrity: bypass cannot override hard-compliance; approvals are
tamper-evident via the append-only event log.

Closes Audit Lead gap #6 + honesty holes H2/H5
(reports/2026-06-27_crew-review-findings.md).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from auto_affi.pipeline.prompt_audit import (
    GenerationBlocked,
    ReferenceManifest,
    StageApproval,
    assert_may_generate,
    audit,
    load_approvals,
    prompt_hash,
    record_approval,
    record_audit,
    record_bypass,
    save_approvals,
)

_IDENTITY = "JIAP02, lean athletic Southeast Asian male"


def _manifest(**overrides: object) -> ReferenceManifest:
    base: dict[str, object] = {
        "prompt": f"{_IDENTITY}. Product orbit, sunlit room.",
        "identity_string": _IDENTITY,
        "cast_sheet_approved": True,
        "objects_sheet_approved": True,
        "declared_objects": ["product"],
        "scene_objects": ["product"],
        "face_reference_count": 1,
        "negative_prompt": "different person, extra limbs, watermark",
        "aspect": "9:16",
        "resolution": "720p",
        "duration_s": 8.0,
        "soul_id": "soul-x",
    }
    base.update(overrides)
    return ReferenceManifest(**base)  # type: ignore[arg-type]


# --------------------- bypass vs hard-compliance (gap #6) ----------------- #


@pytest.mark.unit
def test_bypass_refused_on_banned_claims(tmp_path: Path) -> None:
    record_audit(tmp_path, "video", audit(_manifest(has_banned_claims=True)))
    with pytest.raises(GenerationBlocked, match="hard-compliance"):
        record_bypass(tmp_path, "video", reason="ship it anyway")


@pytest.mark.unit
def test_bypass_refused_on_restricted_category(tmp_path: Path) -> None:
    record_audit(tmp_path, "video", audit(_manifest(category_restricted=True)))
    with pytest.raises(GenerationBlocked, match="hard-compliance"):
        record_bypass(tmp_path, "video", reason="override")


@pytest.mark.unit
def test_bypass_refused_on_failed_economics(tmp_path: Path) -> None:
    record_audit(tmp_path, "video", audit(_manifest(economics_passed=False)))
    with pytest.raises(GenerationBlocked, match="hard-compliance"):
        record_bypass(tmp_path, "video", reason="override")


@pytest.mark.unit
def test_bypass_still_works_for_soft_failure(tmp_path: Path) -> None:
    # A structural/soft failure (wrong aspect) may still be bypassed.
    record_audit(tmp_path, "cast_sheet", audit(_manifest(aspect="16:9")))
    record_bypass(tmp_path, "cast_sheet", reason="hand-made sheet, trusted")
    assert_may_generate("cast_sheet", tmp_path)  # cleared


@pytest.mark.unit
def test_hard_compliance_blocks_even_if_bypassed_first(tmp_path: Path) -> None:
    # bypass BEFORE audit, then audit reveals a hard-compliance failure.
    record_bypass(tmp_path, "video", reason="pre-cleared")
    record_audit(tmp_path, "video", audit(_manifest(has_banned_claims=True)))
    with pytest.raises(GenerationBlocked, match="hard-compliance"):
        assert_may_generate("video", tmp_path)


@pytest.mark.unit
def test_hard_compliance_sticky_through_clean_same_hash_reaudit(tmp_path: Path) -> None:
    """Laundering attack: has_banned_claims is NOT in the prompt hash, so a clean
    re-audit at the SAME hash must NOT clear the latch (Audit Lead re-audit gap)."""
    banned = _manifest(has_banned_claims=True)
    clean = _manifest()  # identical prompt/refs -> identical hash, flag flipped
    assert prompt_hash(banned) == prompt_hash(clean)
    record_audit(tmp_path, "video", audit(banned))
    record_audit(tmp_path, "video", audit(clean))  # attempted launder
    with pytest.raises(GenerationBlocked, match="hard-compliance"):
        assert_may_generate("video", tmp_path)
    with pytest.raises(GenerationBlocked, match="hard-compliance"):
        record_bypass(tmp_path, "video", reason="launder")


@pytest.mark.unit
def test_stale_approve_event_replay_is_rejected(tmp_path: Path) -> None:
    """Replay attack: approve hash H1, re-audit to H2 (invalidates), then revert
    approvals.json to H1+approved. The old H1 approve event predates the H2 audit
    event in the append-only log, so the gate rejects it."""
    m1 = _manifest(prompt=f"{_IDENTITY}. Scene A.")
    record_audit(tmp_path, "cast_sheet", audit(m1))
    record_approval(tmp_path, "cast_sheet", approved_by="operator:alice")
    h1 = prompt_hash(m1)

    m2 = _manifest(prompt=f"{_IDENTITY}. Scene B.")
    record_audit(tmp_path, "cast_sheet", audit(m2))  # new hash invalidates approval

    # Attacker fully reverts approvals.json to the old approved H1 state.
    approvals = load_approvals(tmp_path)
    st = approvals["cast_sheet"]
    st.audited = True
    st.audit_pass = True
    st.approved = True
    st.approved_by = "human"
    st.prompt_hash = h1
    save_approvals(tmp_path, approvals)

    with pytest.raises(GenerationBlocked, match=r"tamper|superseded"):
        assert_may_generate("cast_sheet", tmp_path)


# --------------------- tamper-evident approvals (H2/H5) ------------------- #


@pytest.mark.unit
def test_legitimate_approval_passes(tmp_path: Path) -> None:
    record_audit(tmp_path, "cast_sheet", audit(_manifest()))
    record_approval(tmp_path, "cast_sheet", approved_by="operator:alice")
    assert_may_generate("cast_sheet", tmp_path)
    # an approve event is in the append-only log
    log = (tmp_path / "audit_events.jsonl").read_text()
    assert "approve" in log and "operator:alice" in log


@pytest.mark.unit
def test_forged_approval_without_event_is_rejected(tmp_path: Path) -> None:
    # Audit legitimately (so the audit event exists and audit_pass=true), then
    # forge approved=true in approvals.json with NO approve event — must be rejected.
    record_audit(tmp_path, "cast_sheet", audit(_manifest()))
    approvals = load_approvals(tmp_path)
    forged = approvals["cast_sheet"]
    forged.approved = True
    forged.approved_by = "human"  # the classic forge: just set the field
    save_approvals(tmp_path, approvals)
    with pytest.raises(GenerationBlocked, match=r"no matching .*event|tamper"):
        assert_may_generate("cast_sheet", tmp_path)


@pytest.mark.unit
def test_stale_bypass_event_replay_is_rejected(tmp_path: Path) -> None:
    """Bypass-path mirror of the replay attack: bypass a soft-fail at H1, re-audit
    to H2 (invalidates), revert approvals.json to bypassed=true — the old bypass
    event predates the H2 audit event, so it is rejected."""
    m1 = _manifest(prompt=f"{_IDENTITY}. Scene A.", aspect="16:9")  # soft fail -> bypassable
    record_audit(tmp_path, "cast_sheet", audit(m1))
    record_bypass(tmp_path, "cast_sheet", reason="trusted hand-made A")

    m2 = _manifest(prompt=f"{_IDENTITY}. Scene B.", aspect="16:9")
    record_audit(tmp_path, "cast_sheet", audit(m2))  # newer audit invalidates the bypass

    approvals = load_approvals(tmp_path)
    st = approvals["cast_sheet"]
    st.bypassed = True
    save_approvals(tmp_path, approvals)
    with pytest.raises(GenerationBlocked, match=r"tamper|superseded"):
        assert_may_generate("cast_sheet", tmp_path)


@pytest.mark.unit
def test_bypass_does_not_authorize_a_different_manifest(tmp_path: Path) -> None:
    """A bypass trusts ONE artifact, not any. Generating a different manifest on a
    bypassed stage is blocked by the bypass hash binding."""
    trusted = _manifest(prompt=f"{_IDENTITY}. Trusted scene.", aspect="16:9")
    record_audit(tmp_path, "cast_sheet", audit(trusted))
    record_bypass(tmp_path, "cast_sheet", reason="trust this one")
    # Same artifact is fine.
    assert_may_generate("cast_sheet", tmp_path, manifest=trusted)
    # A different artifact must NOT ride the bypass.
    evil = _manifest(prompt=f"{_IDENTITY}. Evil different scene.", aspect="16:9")
    with pytest.raises(GenerationBlocked, match="hash mismatch"):
        assert_may_generate("cast_sheet", tmp_path, manifest=evil)


@pytest.mark.unit
def test_json_forged_audit_pass_cannot_be_approved(tmp_path: Path) -> None:
    """GAP-F: audit-pass is derived from the append-only log, not approvals.json.
    Flipping audit_pass=true in the JSON on a soft-failed stage cannot launder it
    into an approval, and cannot clear the gate."""
    record_audit(tmp_path, "cast_sheet", audit(_manifest(aspect="16:9")))  # soft fail
    approvals = load_approvals(tmp_path)
    approvals["cast_sheet"].audit_pass = True  # forge the JSON field
    save_approvals(tmp_path, approvals)
    # record_approval reads the log -> refuses.
    with pytest.raises(GenerationBlocked, match="did not pass"):
        record_approval(tmp_path, "cast_sheet", approved_by="op")
    # And forcing approved=true directly still cannot clear the gate.
    approvals = load_approvals(tmp_path)
    approvals["cast_sheet"].approved = True
    save_approvals(tmp_path, approvals)
    with pytest.raises(GenerationBlocked):
        assert_may_generate("cast_sheet", tmp_path)


@pytest.mark.unit
def test_forged_prior_stage_approval_is_rejected(tmp_path: Path) -> None:
    """GAP-C: prior stages are log-authoritative too. Forging cast_sheet/objects
    approved=true in approvals.json (no events) must not let a later stage generate."""
    record_audit(tmp_path, "storyboard", audit(_manifest()))
    record_approval(tmp_path, "storyboard", approved_by="operator:alice")
    approvals = load_approvals(tmp_path)
    for prior in ("cast_sheet", "objects_sheet"):
        approvals[prior].approved = True  # forged: no approve event exists
        approvals[prior].audited = True
        approvals[prior].audit_pass = True
    save_approvals(tmp_path, approvals)
    with pytest.raises(GenerationBlocked, match="prior stage"):
        assert_may_generate("storyboard", tmp_path)


@pytest.mark.unit
def test_banned_prior_stage_blocks_downstream(tmp_path: Path) -> None:
    """GAP-D: a hard-compliance latch on an upstream stage blocks downstream
    generation even if approvals.json is forged to clear it."""
    record_audit(tmp_path, "cast_sheet", audit(_manifest(has_banned_claims=True)))
    approvals = load_approvals(tmp_path)
    approvals["cast_sheet"].approved = True  # forged clearance of a banned stage
    approvals["cast_sheet"].hard_block = False
    save_approvals(tmp_path, approvals)
    record_audit(tmp_path, "objects_sheet", audit(_manifest()))
    record_approval(tmp_path, "objects_sheet", approved_by="op")
    record_audit(tmp_path, "storyboard", audit(_manifest()))
    record_approval(tmp_path, "storyboard", approved_by="op")
    with pytest.raises(GenerationBlocked, match="hard-compliance"):
        assert_may_generate("storyboard", tmp_path)


@pytest.mark.unit
def test_forged_bypass_without_event_is_rejected(tmp_path: Path) -> None:
    approvals = {
        "cast_sheet": StageApproval(bypassed=True, bypass_reason="forged"),
    }
    full = load_approvals(tmp_path)
    full["cast_sheet"] = approvals["cast_sheet"]
    save_approvals(tmp_path, full)
    # no event log written
    with pytest.raises(GenerationBlocked, match=r"no matching .*event|tamper"):
        assert_may_generate("cast_sheet", tmp_path)
