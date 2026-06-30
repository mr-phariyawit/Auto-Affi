"""prompt_mode guard: an image_to_video prompt must not carry FLF2V language.

Hollywood-standards upgrade do-now #1 — closes the wasted-batch bug where FLF2V
("Animate the transition between the first and last frame ...") prompts were fired
as i2v (no last frame) and produced garbled motion in every clip.
"""

from __future__ import annotations

import pytest

from auto_affi.pipeline.prompt_audit import AuditCode, ReferenceManifest, audit, prompt_hash

_PROD = "black-exterior yellow-interior storm umbrella with waterproof sleeve"


def _m(**ov: object) -> ReferenceManifest:
    base: dict[str, object] = {
        "prompt": f"Slow push-in: Ton holds the {_PROD} as it drips to the floor.",
        "identity_string": "Ton",
        "stage_kind": "product",
        "prompt_mode": "image_to_video",
        "cast_sheet_approved": True,
        "objects_sheet_approved": True,
        "declared_objects": ["umbrella", "sleeve"],
        "scene_objects": ["umbrella", "sleeve"],
        "face_reference_count": 0,
        "negative_prompt": "different person, text, watermark",
        "aspect": "9:16",
        "resolution": "720p",
        "duration_s": 4.0,
        "soul_id": "umbrella-335",
    }
    base.update(ov)
    return ReferenceManifest(**base)  # type: ignore[arg-type]


@pytest.mark.unit
def test_i2v_prompt_with_flf2v_language_is_blocked() -> None:
    bad = _m(
        prompt=(
            "Animate the transition between the first and last frame. It opens on the "
            f"{_PROD} on a counter."
        )
    )
    codes = {f.code for f in audit(bad).failures}
    assert AuditCode.PROMPT_MODE_MISMATCH in codes


@pytest.mark.unit
@pytest.mark.parametrize("phrase", ["last frame", "interpolate the motion", "transition between"])
def test_i2v_blocks_each_flf2v_phrase(phrase: str) -> None:
    bad = _m(prompt=f"{phrase}: the {_PROD} on a wet counter, slow push-in.")
    assert AuditCode.PROMPT_MODE_MISMATCH in {f.code for f in audit(bad).failures}


@pytest.mark.unit
def test_clean_i2v_motion_prompt_passes() -> None:
    ok = _m()  # single-action motion prompt, no FLF2V words
    assert AuditCode.PROMPT_MODE_MISMATCH not in {f.code for f in audit(ok).failures}


@pytest.mark.unit
def test_flf2v_language_allowed_when_mode_is_first_last_frame() -> None:
    # The same words are legitimate for an actual FLF2V generator.
    flf2v = _m(
        prompt="Animate the transition between the first and last frame of the umbrella.",
        prompt_mode="first_last_frame",
    )
    assert AuditCode.PROMPT_MODE_MISMATCH not in {f.code for f in audit(flf2v).failures}


@pytest.mark.unit
def test_prompt_mode_is_part_of_the_hash() -> None:
    a = _m(prompt_mode="image_to_video")
    b = _m(prompt_mode="first_last_frame")
    assert prompt_hash(a) != prompt_hash(b)


# --------------------- anti-message / prove-the-negative (do-now #2) ---------- #


@pytest.mark.unit
@pytest.mark.parametrize(
    "phrase",
    ["not a single drop falls", "the paper stays dry", "no water comes out",
     "น้ำไม่หยดสักหยด", "ปลอกไม่เปียก", "แห้งสนิท"],
)
def test_i2v_blocks_prove_the_negative(phrase: str) -> None:
    bad = _m(prompt=f"Macro of the {_PROD}; {phrase}.")
    assert AuditCode.VEO_PROVE_NEGATIVE in {f.code for f in audit(bad).failures}


@pytest.mark.unit
def test_neutral_action_prompt_passes() -> None:
    ok = _m(prompt=f"Calm slow push-in: hands slide the {_PROD} into its sleeve and zip it.")
    assert AuditCode.VEO_PROVE_NEGATIVE not in {f.code for f in audit(ok).failures}


@pytest.mark.unit
def test_prove_negative_only_applies_to_i2v() -> None:
    # a still image proof beat may legitimately depict the dry result
    still = _m(prompt=f"Studio still: the {_PROD}, not a single drop on the dry paper.",
               prompt_mode="image")
    assert AuditCode.VEO_PROVE_NEGATIVE not in {f.code for f in audit(still).failures}
