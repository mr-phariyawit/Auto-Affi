"""stage_kind adapts the PGA person-specific checks (character/product/scene).

Default is "character" — existing behaviour is unchanged (covered elsewhere).
"""

from __future__ import annotations

import pytest

from auto_affi.pipeline.prompt_audit import AuditCode, ReferenceManifest, audit, prompt_hash

_PERSON = "JIAP02, lean athletic Southeast Asian male, V-line jaw"
_PRODUCT = "black-exterior yellow-interior storm umbrella with waterproof sleeve"


def _base(**ov: object) -> dict[str, object]:
    d: dict[str, object] = {
        "prompt": "",
        "identity_string": "",
        "stage_kind": "character",
        "cast_sheet_approved": True,
        "objects_sheet_approved": True,
        "declared_objects": [],
        "scene_objects": [],
        "face_reference_count": 1,
        "negative_prompt": "different person, extra limbs, text, watermark",
        "aspect": "9:16",
        "resolution": "720p",
        "duration_s": 8.0,
        "soul_id": "lock-x",
    }
    d.update(ov)
    return d


def _m(**ov: object) -> ReferenceManifest:
    return ReferenceManifest(**_base(**ov))  # type: ignore[arg-type]


# --------------------------- character (default) ------------------------- #


@pytest.mark.unit
def test_character_default_requires_identity_and_one_face() -> None:
    # passes with identity in prompt + 1 face
    ok = _m(prompt=f"{_PERSON} holding a product", identity_string=_PERSON)
    assert audit(ok).passed
    # missing identity -> fail
    no_id = _m(prompt="someone holding a product", identity_string=_PERSON)
    assert AuditCode.IDENTITY_STRING_MISSING in {f.code for f in audit(no_id).failures}
    # wrong face count -> fail
    two = _m(prompt=f"{_PERSON} ...", identity_string=_PERSON, face_reference_count=2)
    assert AuditCode.FACE_REFERENCE_NOT_SINGLE in {f.code for f in audit(two).failures}
    zero = _m(prompt=f"{_PERSON} ...", identity_string=_PERSON, face_reference_count=0)
    assert AuditCode.FACE_REFERENCE_NOT_SINGLE in {f.code for f in audit(zero).failures}


# --------------------------- product ------------------------------------- #


@pytest.mark.unit
def test_product_passes_with_no_face_and_product_identity() -> None:
    m = _m(
        stage_kind="product",
        prompt=f"Studio product photo of a {_PRODUCT}, white background, no people.",
        identity_string=_PRODUCT,
        face_reference_count=0,  # no human face — N/A for product
        declared_objects=["storm umbrella", "waterproof sleeve"],
        scene_objects=["storm umbrella", "waterproof sleeve"],
    )
    result = audit(m)
    assert result.passed, [f.code for f in result.failures]


@pytest.mark.unit
def test_product_still_requires_product_identity_in_prompt() -> None:
    m = _m(
        stage_kind="product",
        prompt="a generic umbrella photo",  # product descriptor absent
        identity_string=_PRODUCT,
        face_reference_count=0,
    )
    assert AuditCode.IDENTITY_STRING_MISSING in {f.code for f in audit(m).failures}


@pytest.mark.unit
def test_product_still_enforces_stray_object_and_compliance() -> None:
    m = _m(
        stage_kind="product",
        prompt=f"Studio product photo of a {_PRODUCT}",
        identity_string=_PRODUCT,
        face_reference_count=0,
        declared_objects=["storm umbrella"],
        scene_objects=["storm umbrella", "foam roller"],  # stray
        has_banned_claims=True,
    )
    codes = {f.code for f in audit(m).failures}
    assert AuditCode.STRAY_OBJECT in codes
    assert AuditCode.BANNED_CLAIMS in codes


# --------------------------- scene --------------------------------------- #


@pytest.mark.unit
def test_scene_needs_no_identity_or_face() -> None:
    m = _m(
        stage_kind="scene",
        prompt="rain falling on a city street, B-roll, no people",
        identity_string="",  # no subject required
        face_reference_count=0,
    )
    result = audit(m)
    assert result.passed, [f.code for f in result.failures]


@pytest.mark.unit
def test_scene_still_enforces_aspect_and_negative() -> None:
    m = _m(
        stage_kind="scene",
        prompt="rain falling, B-roll",
        identity_string="",
        face_reference_count=0,
        aspect="16:9",  # invalid
        negative_prompt="   ",  # empty
    )
    codes = {f.code for f in audit(m).failures}
    assert AuditCode.ASPECT_INVALID in codes
    assert AuditCode.NEGATIVE_PROMPT_MISSING in codes


# --------------------------- determinism --------------------------------- #


@pytest.mark.unit
def test_stage_kind_is_part_of_the_hash() -> None:
    char = _m(prompt=f"{_PERSON} ...", identity_string=_PERSON, stage_kind="character")
    prod = _m(prompt=f"{_PERSON} ...", identity_string=_PERSON, stage_kind="product")
    assert prompt_hash(char) != prompt_hash(prod)
