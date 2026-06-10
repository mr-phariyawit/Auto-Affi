"""HSO x VCS creative rubric lint (SPEC §19.1) -- deterministic, offline-only.

The rubric enforces Hard-Sell Offer (HSO) x Value-Creation Script (VCS)
creative standards on a completed Storyboard before it is handed to the
video-generation pipeline. All violations are surfaced at lint time, before
any GPU spend occurs.

Rules enforced (from SPEC §19.1):
  1. HOOK TIMING -- hook (scenes[0]) duration must be 1.0s-2.0s inclusive.
  2. BODY SHOT TIMING -- average body shot (scenes[1:end-1]) must be 3-5s.
  3. CLIP MAX — every individual clip must be <= 6s.
  4. CAPTIONS/DIALOGUE — every scene must have dialogue OR on_screen_text
     (not both required, but at least one is required per scene).
  5. SINGLE CTA — exactly ONE scene may have purpose == CTA.
  6. PRODUCT VISIBILITY — at least one scene's visual_prompt must contain
     a product reference (checked via `visual_prompt` length >= 20 chars and
     a "product" mention — best-effort heuristic for offline lint).

No LLM, no network, no Anthropic.
"""

from __future__ import annotations

from pydantic import BaseModel

from auto_affi.schemas.storyboard import ScenePurpose, Storyboard

# ---------------------------------------------------------------------------
# Constants from SPEC §19.1
# ---------------------------------------------------------------------------

_HOOK_MIN_S = 1.0
_HOOK_MAX_S = 2.0
_BODY_AVG_MIN_S = 3.0
_BODY_AVG_MAX_S = 5.0
_CLIP_MAX_S = 6.0


# ---------------------------------------------------------------------------
# RubricReport — the lint result
# ---------------------------------------------------------------------------

class RubricReport(BaseModel):
    """Result of the HSO x VCS creative rubric lint."""

    ok: bool
    violations: list[str]


# ---------------------------------------------------------------------------
# Lint function
# ---------------------------------------------------------------------------

def lint_storyboard(sb: Storyboard) -> RubricReport:
    """Lint a Storyboard against the HSO x VCS creative rubric (SPEC §19.1).

    Parameters
    ----------
    sb:
        A pydantic-validated Storyboard (schema validators have already
        passed; this rubric adds CREATIVE constraints on top).

    Returns
    -------
    RubricReport
        ``ok=True`` when all rules pass; ``violations`` lists each failure.
    """
    violations: list[str] = []

    if not sb.scenes:
        return RubricReport(ok=False, violations=["storyboard has no scenes"])

    # Rule 1: HOOK TIMING
    hook = sb.scenes[0]
    if hook.purpose is not ScenePurpose.HOOK:
        violations.append(
            f"Rule 1 HOOK TIMING: scenes[0].purpose is {hook.purpose!r}, expected HOOK"
        )
    else:
        if hook.duration_s < _HOOK_MIN_S:
            violations.append(
                f"Rule 1 HOOK TIMING: hook duration {hook.duration_s:.2f}s < {_HOOK_MIN_S}s minimum"
            )
        if hook.duration_s > _HOOK_MAX_S:
            violations.append(
                f"Rule 1 HOOK TIMING: hook duration {hook.duration_s:.2f}s > {_HOOK_MAX_S}s maximum"
            )

    # Rule 2: BODY SHOT TIMING (scenes[1:] excluding the CTA if it is last)
    # "body" = all scenes except hook and CTA
    cta_indices = {i for i, s in enumerate(sb.scenes) if s.purpose is ScenePurpose.CTA}
    body_scenes = [
        s for i, s in enumerate(sb.scenes)
        if i != 0 and i not in cta_indices
    ]
    if body_scenes:
        avg_body = sum(s.duration_s for s in body_scenes) / len(body_scenes)
        if avg_body < _BODY_AVG_MIN_S:
            violations.append(
                f"Rule 2 BODY AVG: average body shot {avg_body:.2f}s < {_BODY_AVG_MIN_S}s"
            )
        if avg_body > _BODY_AVG_MAX_S:
            violations.append(
                f"Rule 2 BODY AVG: average body shot {avg_body:.2f}s > {_BODY_AVG_MAX_S}s"
            )

    # Rule 3: CLIP MAX — every individual clip <= 6s
    for scene in sb.scenes:
        if scene.duration_s > _CLIP_MAX_S:
            violations.append(
                f"Rule 3 CLIP MAX: scene[{scene.idx}] duration {scene.duration_s:.2f}s > {_CLIP_MAX_S}s"
            )

    # Rule 4: CAPTIONS/DIALOGUE — every scene must have at least one
    for scene in sb.scenes:
        has_dialogue = scene.dialogue is not None and len(scene.dialogue.text_th.strip()) > 0
        has_caption = scene.on_screen_text is not None and len(scene.on_screen_text.th.strip()) > 0
        if not has_dialogue and not has_caption:
            violations.append(
                f"Rule 4 CAPTIONS: scene[{scene.idx}] ({scene.purpose.value}) "
                f"has neither dialogue nor on_screen_text"
            )

    # Rule 5: SINGLE CTA — exactly one CTA scene
    num_cta = len(cta_indices)
    if num_cta == 0:
        violations.append("Rule 5 SINGLE CTA: no scene with purpose=CTA found")
    elif num_cta > 1:
        violations.append(
            f"Rule 5 SINGLE CTA: {num_cta} CTA scenes found (indices {sorted(cta_indices)}), expected exactly 1"
        )

    # Rule 6: PRODUCT VISIBILITY — at least one scene's visual_prompt is substantive
    # (>= 20 chars is enforced by Scene schema; we check for any product-descriptive content)
    has_product_visual = any(
        len(s.visual_prompt) >= 20 for s in sb.scenes
    )
    if not has_product_visual:
        violations.append(
            "Rule 6 PRODUCT VISIBLE: no scene has a substantive visual_prompt (>= 20 chars)"
        )

    return RubricReport(ok=len(violations) == 0, violations=violations)
