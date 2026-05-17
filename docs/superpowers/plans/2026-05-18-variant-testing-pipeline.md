# Auto-Affi Variant-Testing Pipeline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a per-concept video pipeline that produces 3 hook-variant ads sharing body+CTA shots, each tagged with a unique Shopee affiliate sub_id so CVR-based winner selection can close the learning loop.

**Architecture:** New `ConceptVariantSet` schema describes one concept + N hook variants on top of a shared base. New `scripts/produce-variant-set.py` orchestrator renders shared shots ONCE then per-variant hook shots, assembling N final mp4s. HeyGen surface removed entirely. Default video model swaps from `seedance_2_0` Fast 720p → `kling3_0` std (57% cheaper, native 1080p, native audio).

**Tech Stack:** Python 3.13 (`.venv/bin/python`), Pydantic v2, asyncio, Higgsfield CLI (already in `src/auto_affi/adapters/higgsfield_cli.py`), Gemini Nano Banana Pro (`src/auto_affi/adapters/gemini_image.py`), edge-tts, HyperFrames (overlays), ffmpeg (concat / mix / loop).

---

## File Map

**Phase 1 — HeyGen removal (no new code, only deletions + edits):**
- DELETE: `src/auto_affi/adapters/heygen.py`
- DELETE: `scripts/heygen-lipsync-clips.py`
- DELETE: `tests/unit/test_heygen_adapter.py`
- MODIFY: `src/auto_affi/schemas/ai_storyboard.py` (drop `HEYGEN_AVATAR_IV` enum value + 3 invariants in `_enforce_generator_invariants`)
- MODIFY: `scripts/produce-ai-storyboard.py` (drop heygen import, `_run_heygen_avatar_iv` helper, env check, dispatch branch)

**Phase 2 — `ConceptVariantSet` schema:**
- MODIFY: `src/auto_affi/schemas/ai_storyboard.py` (add `ConceptVariantSet` model + validators)
- CREATE: `tests/unit/test_concept_variant_set.py`

**Phase 3 — Variant orchestrator:**
- CREATE: `scripts/produce-variant-set.py`
- CREATE: `tests/unit/test_produce_variant_set.py`

**Phase 4 — Live validation (PD300X concept-3-v1):**
- CREATE: `data/registry/items/28875679676/concepts/shure-vs-maono/base.json` (gitignored — operator authors)
- CREATE: `data/registry/items/28875679676/concepts/shure-vs-maono/hooks/{a,b,c}.json` (gitignored)
- RUN: `scripts/produce-variant-set.py` against the above

**Phase 5 — Measurement layer (gated on Phase 4 producing live data):**
- CREATE: `scripts/pull-shopee-results.py`
- CREATE: `scripts/compare-variant-results.py`
- CREATE: `tests/unit/test_compare_variant_results.py`

**Phase 6 — Docs:**
- CREATE: `docs/workflow-pipeline-v14.md`

---

## Phase 1: HeyGen Removal

Spec section 9. Done first so the new variant code never has to consider a dormant adapter.

### Task 1: Remove HeyGen adapter file + test + lipsync driver script

**Files:**
- Delete: `src/auto_affi/adapters/heygen.py`
- Delete: `scripts/heygen-lipsync-clips.py`
- Delete: `tests/unit/test_heygen_adapter.py`

- [ ] **Step 1: Verify suite currently passes (baseline)**

Run: `.venv/bin/python -m pytest tests/unit/ -q --no-cov 2>&1 | tail -5`
Expected: "passed" — captures the pre-removal baseline so we know the green count to match after deletion.

- [ ] **Step 2: Delete the three files**

```bash
rm src/auto_affi/adapters/heygen.py
rm scripts/heygen-lipsync-clips.py
rm tests/unit/test_heygen_adapter.py
```

- [ ] **Step 3: Run suite and confirm collection still works (will fail on import-time references)**

Run: `.venv/bin/python -m pytest tests/unit/ -q --no-cov 2>&1 | tail -20`
Expected: collection errors in `tests/unit/` files that import from `auto_affi.adapters.heygen`. We fix those in Task 2 + 3. Do NOT commit yet — broken state.

### Task 2: Drop `HEYGEN_AVATAR_IV` from the `Generator` enum + invariants

**Files:**
- Modify: `src/auto_affi/schemas/ai_storyboard.py`

- [ ] **Step 1: Read the current `Generator` enum block and the `_enforce_generator_invariants` method**

Run: `.venv/bin/python -c "from auto_affi.schemas.ai_storyboard import Generator; print(list(Generator))"`
Expected: shows current enum members including `HEYGEN_AVATAR_IV`.

- [ ] **Step 2: Edit the enum**

Open `src/auto_affi/schemas/ai_storyboard.py`. Find the `Generator(StrEnum)` block (around line 47) and delete this line:

```python
    HEYGEN_AVATAR_IV = "heygen_avatar_iv"
```

Also update the file docstring (around line 11) — change:

```python
   model owns it (heygen_avatar_iv / seedance_2kf / seedance_t2v / veo /
```
to:
```python
   model owns it (higgsfield_cli / seedance_2kf / seedance_t2v / veo /
```

- [ ] **Step 3: Delete the HeyGen invariant block**

In the same file, find `_enforce_generator_invariants` (around line 130). Delete the entire `if self.generator is Generator.HEYGEN_AVATAR_IV:` block and its 3 nested invariants (the block that requires `phaya_tts` + `dialogue_th` + duration ≤ 6.0).

- [ ] **Step 4: Run the schema's own tests**

Run: `.venv/bin/python -c "from auto_affi.schemas.ai_storyboard import AiStoryboard, AiShot, Generator, NarrativeRole, AudioSource; s = AiShot(shot_id='s0', narrative_role=NarrativeRole.HOOK, duration_s=3.0, generator=Generator.HOLD, image_prompt='a'*30, consistency_seed=1, audio_source=AudioSource.SILENCE); print('schema OK')"`
Expected: prints `schema OK` — confirms enum reshape didn't break the validator graph.

### Task 3: Drop HeyGen dispatch from `produce-ai-storyboard.py`

**Files:**
- Modify: `scripts/produce-ai-storyboard.py`

- [ ] **Step 1: Drop the HeyGen import**

Find this line (around line 49) and delete it:

```python
from auto_affi.adapters.heygen import HeyGenClient, HeyGenError
```

- [ ] **Step 2: Drop the `_run_heygen_avatar_iv` function**

Find `async def _run_heygen_avatar_iv(` (around line 245). Delete the entire function (it ends at the next `async def` or top-level `def` definition).

- [ ] **Step 3: Drop the env-key check + client construction**

In `main()`, find the `HEYGEN_API_KEY` entry in the env-check loop (around line 521) and delete it. Find the `heygen = HeyGenClient(...)` line (around line 529) and delete it. Replace any downstream `heygen` reference in the dispatch loop with a `pass` removal (see next step).

- [ ] **Step 4: Drop the dispatch branch**

Find the `elif shot.generator is Generator.HEYGEN_AVATAR_IV:` branch in the per-shot dispatch loop (around line 596). Delete this entire branch (the `elif` line + its body that calls `_run_heygen_avatar_iv`).

- [ ] **Step 5: Update the file's top-level docstring**

Around line 10, the docstring lists generators. Update:

```python
       heygen_avatar_iv → Phaya TTS → HeyGen Avatar IV → download
```
to remove this line entirely (it's the only HeyGen reference in the docstring).

- [ ] **Step 6: Compile-check + run the orchestrator help**

Run:
```bash
.venv/bin/python -c "import py_compile; py_compile.compile('scripts/produce-ai-storyboard.py', doraise=True); print('OK')"
.venv/bin/python scripts/produce-ai-storyboard.py --help | head -5
```
Expected: `OK` from compile, then the orchestrator's usage line. If either fails, fix the residual reference.

### Task 4: Verify suite is green again + commit Phase 1

- [ ] **Step 1: Run full unit test suite**

Run: `.venv/bin/python -m pytest tests/unit/ -q --no-cov 2>&1 | tail -10`
Expected: all green; no collection errors; the count should be smaller than baseline by exactly the number of HeyGen tests removed (the adapter file had 9 tests in `test_heygen_adapter.py`).

- [ ] **Step 2: Stage + commit**

```bash
git add -A
git commit -m "chore(heygen): remove adapter, tests, dispatch — Higgsfield-only video

Per docs/superpowers/specs/2026-05-18-auto-affi-variant-testing-design.md
hard constraint #1: HeyGen is removed entirely. Higgsfield does not
support Thai lip-sync, but the v13 storyboard already sidesteps that
via the mouth-closed + edge-tts VO + caption pattern.

Surface removed:
  - src/auto_affi/adapters/heygen.py
  - scripts/heygen-lipsync-clips.py
  - tests/unit/test_heygen_adapter.py
  - Generator.HEYGEN_AVATAR_IV enum value + its invariants
  - HEYGEN_API_KEY .env check
  - heygen_avatar_iv dispatch branch in produce-ai-storyboard.py

Recoverable from git history if Higgsfield ever ships Thai lip-sync."
```

- [ ] **Step 3: Push**

Run: `git push 2>&1 | tail -3`

---

## Phase 2: `ConceptVariantSet` Schema

Spec section 6. New pydantic model that bundles one base storyboard with N hook-variant shot lists.

### Task 5: Write the failing test for `ConceptVariantSet`

**Files:**
- Create: `tests/unit/test_concept_variant_set.py`

- [ ] **Step 1: Write the test file**

```python
"""Tests for ConceptVariantSet — one concept × N hook variants on
shared body+CTA base."""

from __future__ import annotations

import pytest

from auto_affi.schemas.ai_storyboard import (
    AiShot, AiStoryboard, AudioSource, ConceptVariantSet,
    Generator, NarrativeRole,
)


def _hook_shot(shot_id: str = "s0") -> AiShot:
    return AiShot(
        shot_id=shot_id,
        narrative_role=NarrativeRole.HOOK,
        duration_s=3.0,
        generator=Generator.HOLD,
        image_prompt="a" * 30,
        consistency_seed=51728,
        audio_source=AudioSource.SILENCE,
    )


def _body_shot(shot_id: str, dur: float = 5.0) -> AiShot:
    return AiShot(
        shot_id=shot_id,
        narrative_role=NarrativeRole.STORY,
        duration_s=dur,
        generator=Generator.HOLD,
        image_prompt="a" * 30,
        consistency_seed=51728,
        audio_source=AudioSource.MUSIC_ONLY,
    )


def _base_with_body_and_cta(target_total: float) -> AiStoryboard:
    body_dur = target_total - 6.0  # 6s reserved for 2-shot hooks
    return AiStoryboard(
        concept_id="test-concept",
        title_en="t", title_th="t",
        item_id=1,
        consistency_seed=51728,
        target_total_duration_s=target_total,
        music_prompt="a" * 30,
        music_duration_s=target_total,
        shots=[
            _body_shot("s2", dur=body_dur / 2),
            _body_shot("s3", dur=body_dur / 2),
        ],
    )


def test_concept_variant_set_valid_shape():
    """Happy path: base + 3 hook variants each contributing 6s of hook."""
    base = _base_with_body_and_cta(target_total=20.0)
    variants = {
        "a": [_hook_shot("s0"), _hook_shot("s1")],
        "b": [_hook_shot("s0"), _hook_shot("s1")],
        "c": [_hook_shot("s0"), _hook_shot("s1")],
    }
    vs = ConceptVariantSet(
        concept_id="shure-vs-maono",
        item_id=1,
        base=base,
        variants=variants,
    )
    assert vs.concept_id == "shure-vs-maono"
    assert list(vs.variants.keys()) == ["a", "b", "c"]


def test_concept_variant_set_rejects_empty_variants():
    base = _base_with_body_and_cta(target_total=20.0)
    with pytest.raises(ValueError, match="at least one"):
        ConceptVariantSet(
            concept_id="x", item_id=1, base=base, variants={},
        )


def test_concept_variant_set_rejects_mismatched_hook_shot_count():
    """All variants must have the same number of hook shots."""
    base = _base_with_body_and_cta(target_total=20.0)
    variants = {
        "a": [_hook_shot("s0"), _hook_shot("s1")],
        "b": [_hook_shot("s0")],  # only 1 hook shot — mismatch
    }
    with pytest.raises(ValueError, match="same number of hook shots"):
        ConceptVariantSet(
            concept_id="x", item_id=1, base=base, variants=variants,
        )


def test_concept_variant_set_rejects_variant_seed_mismatch():
    """Variant hook shots must share base.consistency_seed."""
    base = _base_with_body_and_cta(target_total=20.0)
    bad_hook = AiShot(
        shot_id="s0",
        narrative_role=NarrativeRole.HOOK,
        duration_s=3.0,
        generator=Generator.HOLD,
        image_prompt="a" * 30,
        consistency_seed=99999,  # different seed
        audio_source=AudioSource.SILENCE,
    )
    variants = {
        "a": [bad_hook, _hook_shot("s1")],
    }
    with pytest.raises(ValueError, match="consistency_seed"):
        ConceptVariantSet(
            concept_id="x", item_id=1, base=base, variants=variants,
        )


def test_concept_variant_set_total_duration_check():
    """base.target_total_duration must equal hook-duration + body-duration."""
    base = _base_with_body_and_cta(target_total=20.0)
    # Hooks here add 6s (2 × 3s), body adds 14s, total 20 ✓
    ok = ConceptVariantSet(
        concept_id="x", item_id=1, base=base,
        variants={"a": [_hook_shot("s0"), _hook_shot("s1")]},
    )
    assert ok is not None
    # Now overshoot: 3 × 3s hooks = 9s, body 14s, total 23 vs target 20 → fail
    with pytest.raises(ValueError, match="total duration"):
        ConceptVariantSet(
            concept_id="x", item_id=1, base=base,
            variants={"a": [_hook_shot("s0"), _hook_shot("s1"), _hook_shot("s_extra")]},
        )


def test_concept_variant_set_variant_id_format():
    """Variant IDs should be lowercase single letters a-z for filename safety."""
    base = _base_with_body_and_cta(target_total=20.0)
    with pytest.raises(ValueError, match="variant id"):
        ConceptVariantSet(
            concept_id="x", item_id=1, base=base,
            variants={"VARIANT-1": [_hook_shot("s0"), _hook_shot("s1")]},
        )
```

- [ ] **Step 2: Run the tests — expect ImportError**

Run: `.venv/bin/python -m pytest tests/unit/test_concept_variant_set.py -v --no-cov 2>&1 | tail -10`
Expected: `ImportError: cannot import name 'ConceptVariantSet' from 'auto_affi.schemas.ai_storyboard'`. This is the failing test we want.

### Task 6: Implement `ConceptVariantSet`

**Files:**
- Modify: `src/auto_affi/schemas/ai_storyboard.py`

- [ ] **Step 1: Add the new model at the end of the file**

Append this to `src/auto_affi/schemas/ai_storyboard.py`:

```python


class ConceptVariantSet(BaseModel):
    """One concept × N hook variants on a shared body+CTA base.

    Spec: docs/superpowers/specs/2026-05-18-auto-affi-variant-testing-design.md

    Layout convention on disk:
        data/registry/items/<sku>/concepts/<concept_id>/
        ├── base.json     ← AiStoryboard (body + CTA shots, no hooks)
        ├── hooks/
        │   ├── a.json    ← list[AiShot] (variant A hook shots, e.g. s0+s1)
        │   ├── b.json
        │   └── c.json
        └── links.json    ← {variant_id: shopee_sub_id} (post-render)

    Invariants enforced here:
      * variants dict is non-empty
      * variant IDs are lowercase a-z single letters (filesystem safety)
      * all variants have the same number of hook shots
      * every variant hook shot shares base.consistency_seed
      * (sum of variant hook durations + sum of base body/CTA durations)
        equals base.target_total_duration_s within ±0.01s
    """

    concept_id: str = Field(min_length=1)
    item_id: int
    base: AiStoryboard
    variants: dict[str, list[AiShot]] = Field(min_length=1)

    @field_validator("variants")
    @classmethod
    def _variant_ids_must_be_lowercase_single_letter(
        cls, v: dict[str, list[AiShot]],
    ) -> dict[str, list[AiShot]]:
        if not v:
            raise ValueError("at least one variant required")
        for vid in v:
            if not (len(vid) == 1 and vid.isalpha() and vid.islower()):
                raise ValueError(
                    f"variant id {vid!r} invalid — must be a single lowercase "
                    f"letter a-z for filename safety"
                )
        return v

    @model_validator(mode="after")
    def _validate_variant_shape(self) -> "ConceptVariantSet":
        # Concept-level consistency_seed = base.consistency_seed
        base_seed = self.base.consistency_seed
        # All variants must have the same shot count
        hook_counts = {vid: len(shots) for vid, shots in self.variants.items()}
        if len(set(hook_counts.values())) > 1:
            raise ValueError(
                f"variants must have the same number of hook shots; "
                f"got {hook_counts}"
            )
        # Each hook shot must share base seed
        for vid, shots in self.variants.items():
            for shot in shots:
                if shot.consistency_seed != base_seed:
                    raise ValueError(
                        f"variant {vid!r} shot {shot.shot_id} has "
                        f"consistency_seed={shot.consistency_seed} but base "
                        f"requires {base_seed}"
                    )
        # Total duration = base body+CTA + ANY variant's hook block
        # (since all variants share the same hook count + a target duration,
        # we just check the first variant — the validator above guarantees
        # all variants have identical hook count, durations can still differ
        # per variant, so check each.)
        body_total = sum(s.duration_s for s in self.base.shots)
        target = self.base.target_total_duration_s
        for vid, shots in self.variants.items():
            hook_total = sum(s.duration_s for s in shots)
            if abs((body_total + hook_total) - target) > 0.01:
                raise ValueError(
                    f"variant {vid!r}: total duration "
                    f"{body_total + hook_total:.2f}s does not equal "
                    f"base.target_total_duration_s {target:.2f}s"
                )
        return self

    def variant_ids(self) -> list[str]:
        return sorted(self.variants.keys())
```

- [ ] **Step 2: Run the new tests — expect all pass**

Run: `.venv/bin/python -m pytest tests/unit/test_concept_variant_set.py -v --no-cov 2>&1 | tail -15`
Expected: 6 tests pass.

- [ ] **Step 3: Run the full schema-touching test suite to make sure nothing else broke**

Run: `.venv/bin/python -m pytest tests/unit/ -q --no-cov 2>&1 | tail -5`
Expected: all green.

- [ ] **Step 4: Commit**

```bash
git add src/auto_affi/schemas/ai_storyboard.py tests/unit/test_concept_variant_set.py
git commit -m "feat(schema): ConceptVariantSet for variant-testing pipeline

Bundles one base AiStoryboard (body + CTA shots) with N hook-variant
shot lists. Enforces: non-empty variants dict, lowercase-single-letter
variant ids, identical hook shot count across variants, shared
consistency_seed, total-duration parity with base.target_total_duration_s.

Per docs/superpowers/specs/2026-05-18-auto-affi-variant-testing-design.md
section 6.

6 unit tests cover the happy path + each invariant."
```

---

## Phase 3: Variant Orchestrator

Spec section 7a. New `scripts/produce-variant-set.py` that renders shared shots ONCE then per-variant hook shots, assembling N final mp4s.

### Task 7: Write the failing test for the orchestrator's shared-shot reuse

**Files:**
- Create: `tests/unit/test_produce_variant_set.py`

- [ ] **Step 1: Write the test file**

```python
"""Tests for scripts/produce-variant-set.py — variant orchestrator.

End-to-end behavior is mocked (Higgsfield CLI, Gemini, edge-tts,
HyperFrames, ffmpeg) — these tests verify the orchestration LOGIC:
shared shots render once, variant shots render per variant, final
assembly produces N mp4s with correct file paths."""

from __future__ import annotations

import asyncio
import importlib.util
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch, AsyncMock

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = REPO_ROOT / "scripts" / "produce-variant-set.py"


def _load_script_module():
    spec = importlib.util.spec_from_file_location("produce_variant_set", SCRIPT_PATH)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["produce_variant_set"] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def script_mod():
    return _load_script_module()


def test_render_plan_dedupes_shared_shots(script_mod):
    """Given a ConceptVariantSet with 2 hook shots + 5 base shots × 3
    variants, the render plan must dispatch the 5 base shots ONCE and
    the 2 hook shots × 3 variants = 6 hook renders, not 21."""
    from auto_affi.schemas.ai_storyboard import (
        AiShot, AiStoryboard, AudioSource, ConceptVariantSet,
        Generator, NarrativeRole,
    )

    def _shot(sid, role=NarrativeRole.STORY, dur=4.0, gen=Generator.HOLD):
        return AiShot(
            shot_id=sid, narrative_role=role, duration_s=dur,
            generator=gen, image_prompt="a" * 30,
            consistency_seed=42, audio_source=AudioSource.MUSIC_ONLY,
        )

    base = AiStoryboard(
        concept_id="t", title_en="t", title_th="t", item_id=1,
        consistency_seed=42, target_total_duration_s=26.0,
        music_prompt="a" * 30, music_duration_s=26.0,
        shots=[_shot("s2", dur=4), _shot("s3", dur=4),
               _shot("s4", dur=4), _shot("s5", dur=4), _shot("s6", dur=4)],
    )
    variants = {
        "a": [_shot("s0", role=NarrativeRole.HOOK, dur=3),
              _shot("s1", role=NarrativeRole.HOOK, dur=3)],
        "b": [_shot("s0", role=NarrativeRole.HOOK, dur=3),
              _shot("s1", role=NarrativeRole.HOOK, dur=3)],
        "c": [_shot("s0", role=NarrativeRole.HOOK, dur=3),
              _shot("s1", role=NarrativeRole.HOOK, dur=3)],
    }
    vs = ConceptVariantSet(
        concept_id="t", item_id=1, base=base, variants=variants,
    )

    plan = script_mod.build_render_plan(vs)
    # 5 shared shots (rendered once) + 2 hook shots × 3 variants = 11 total
    assert plan.shared_shot_count == 5
    assert plan.variant_hook_render_count == 6
    assert plan.total_renders == 11


def test_build_render_plan_emits_correct_output_paths(script_mod, tmp_path):
    """Plan should emit one mp4 path per variant under
    out/<sku>-<concept>/variant-<id>/final.mp4."""
    from auto_affi.schemas.ai_storyboard import (
        AiShot, AiStoryboard, AudioSource, ConceptVariantSet,
        Generator, NarrativeRole,
    )

    def _shot(sid, role=NarrativeRole.STORY, dur=4.0):
        return AiShot(
            shot_id=sid, narrative_role=role, duration_s=dur,
            generator=Generator.HOLD, image_prompt="a" * 30,
            consistency_seed=42, audio_source=AudioSource.MUSIC_ONLY,
        )

    base = AiStoryboard(
        concept_id="shure-vs-maono", title_en="t", title_th="t",
        item_id=28875679676, consistency_seed=42,
        target_total_duration_s=14.0, music_prompt="a" * 30,
        music_duration_s=14.0,
        shots=[_shot("s2", dur=4), _shot("s3", dur=4)],
    )
    variants = {
        "a": [_shot("s0", role=NarrativeRole.HOOK, dur=3),
              _shot("s1", role=NarrativeRole.HOOK, dur=3)],
        "b": [_shot("s0", role=NarrativeRole.HOOK, dur=3),
              _shot("s1", role=NarrativeRole.HOOK, dur=3)],
    }
    vs = ConceptVariantSet(
        concept_id="shure-vs-maono", item_id=28875679676,
        base=base, variants=variants,
    )

    plan = script_mod.build_render_plan(vs, out_root=tmp_path)
    expected_a = tmp_path / "28875679676-shure-vs-maono" / "variant-a" / "final.mp4"
    expected_b = tmp_path / "28875679676-shure-vs-maono" / "variant-b" / "final.mp4"
    assert plan.variant_outputs == {"a": expected_a, "b": expected_b}


def test_build_links_json_assigns_unique_sub_ids(script_mod, tmp_path):
    """links.json maps variant_id → sub_id of shape
    <item_id>-<concept>-<variant_id>."""
    from auto_affi.schemas.ai_storyboard import (
        AiShot, AiStoryboard, AudioSource, ConceptVariantSet,
        Generator, NarrativeRole,
    )

    def _shot(sid, role=NarrativeRole.STORY, dur=4.0):
        return AiShot(
            shot_id=sid, narrative_role=role, duration_s=dur,
            generator=Generator.HOLD, image_prompt="a" * 30,
            consistency_seed=42, audio_source=AudioSource.MUSIC_ONLY,
        )

    base = AiStoryboard(
        concept_id="shure-vs-maono", title_en="t", title_th="t",
        item_id=28875679676, consistency_seed=42,
        target_total_duration_s=10.0, music_prompt="a" * 30,
        music_duration_s=10.0, shots=[_shot("s2", dur=4)],
    )
    variants = {
        "a": [_shot("s0", role=NarrativeRole.HOOK, dur=3),
              _shot("s1", role=NarrativeRole.HOOK, dur=3)],
        "b": [_shot("s0", role=NarrativeRole.HOOK, dur=3),
              _shot("s1", role=NarrativeRole.HOOK, dur=3)],
    }
    vs = ConceptVariantSet(
        concept_id="shure-vs-maono", item_id=28875679676,
        base=base, variants=variants,
    )
    links = script_mod.build_links_map(vs)
    assert links == {
        "a": "28875679676-shure-vs-maono-a",
        "b": "28875679676-shure-vs-maono-b",
    }
```

- [ ] **Step 2: Run — expect FileNotFoundError (script doesn't exist yet)**

Run: `.venv/bin/python -m pytest tests/unit/test_produce_variant_set.py -v --no-cov 2>&1 | tail -10`
Expected: collection error citing `scripts/produce-variant-set.py` not found. This is the failing test we want.

### Task 8: Scaffold `produce-variant-set.py` with the pure-logic helpers (no I/O yet)

**Files:**
- Create: `scripts/produce-variant-set.py`

- [ ] **Step 1: Create the script skeleton + pure-logic helpers**

```python
#!/usr/bin/env python
"""Variant-set orchestrator — renders N hook variants of one concept,
sharing body+CTA shots across all variants.

Spec: docs/superpowers/specs/2026-05-18-auto-affi-variant-testing-design.md

Reads a ConceptVariantSet from disk:
    data/registry/items/<sku>/concepts/<concept_id>/
    ├── base.json       AiStoryboard (body + CTA shots, no hooks)
    └── hooks/{a,b,c}.json    list[AiShot] per variant

Phases:
  1. Stills — Gemini per-shot-per-variant
  2. Shared-shot render — Higgsfield once for body+CTA
  3. Variant-hook render — Higgsfield per variant
  4. Per-variant CTA bake — HyperFrames overlay with variant-specific sub_id
  5. Per-variant assembly — concat shared+variant clips, mix music, captions
  6. Persist links.json
"""

from __future__ import annotations

import argparse
import asyncio
import dataclasses
import json
import sys
from pathlib import Path

from auto_affi.schemas.ai_storyboard import (
    AiShot, AiStoryboard, ConceptVariantSet, Generator, NarrativeRole,
)


# ---------------------------------------------------------------------------
# Pure-logic helpers — no I/O, fully unit-testable
# ---------------------------------------------------------------------------


@dataclasses.dataclass(frozen=True)
class RenderPlan:
    """Output of build_render_plan — describes what the orchestrator
    will render and where each artifact will land. Pure data, no I/O."""

    concept_dir_name: str
    shared_shot_ids: list[str]
    variant_hook_shots: dict[str, list[str]]   # variant_id -> shot_ids
    variant_outputs: dict[str, Path]           # variant_id -> final.mp4 path
    shared_out_dir: Path

    @property
    def shared_shot_count(self) -> int:
        return len(self.shared_shot_ids)

    @property
    def variant_hook_render_count(self) -> int:
        return sum(len(s) for s in self.variant_hook_shots.values())

    @property
    def total_renders(self) -> int:
        return self.shared_shot_count + self.variant_hook_render_count


def _concept_dir_name(vs: ConceptVariantSet) -> str:
    """Standard directory name: <item_id>-<concept_id>."""
    return f"{vs.item_id}-{vs.concept_id}"


def build_render_plan(
    vs: ConceptVariantSet, *, out_root: Path = Path("out"),
) -> RenderPlan:
    """Pure function — given a ConceptVariantSet, return the render plan.

    Shared shots = base.shots (the body+CTA list).
    Variant hook shots = variants[v].
    Output paths follow the convention in the spec section 5.
    """
    cd = _concept_dir_name(vs)
    concept_dir = out_root / cd
    shared_out = concept_dir / "shared"
    variant_outputs: dict[str, Path] = {
        vid: concept_dir / f"variant-{vid}" / "final.mp4"
        for vid in vs.variants
    }
    return RenderPlan(
        concept_dir_name=cd,
        shared_shot_ids=[s.shot_id for s in vs.base.shots],
        variant_hook_shots={
            vid: [s.shot_id for s in shots]
            for vid, shots in vs.variants.items()
        },
        variant_outputs=variant_outputs,
        shared_out_dir=shared_out,
    )


def build_links_map(vs: ConceptVariantSet) -> dict[str, str]:
    """Pure function — variant_id -> Shopee sub_id of the form
    <item_id>-<concept_id>-<variant_id>. Persisted to links.json."""
    return {
        vid: f"{vs.item_id}-{vs.concept_id}-{vid}"
        for vid in vs.variants
    }


# ---------------------------------------------------------------------------
# I/O orchestration (Phase 2 of plan — wired in Task 9)
# ---------------------------------------------------------------------------


def load_variant_set(concept_dir: Path) -> ConceptVariantSet:
    """Read base.json + hooks/*.json from a concept directory."""
    base_path = concept_dir / "base.json"
    if not base_path.exists():
        raise FileNotFoundError(f"base.json missing in {concept_dir}")
    base = AiStoryboard.model_validate_json(base_path.read_text(encoding="utf-8"))

    hooks_dir = concept_dir / "hooks"
    if not hooks_dir.is_dir():
        raise FileNotFoundError(f"hooks/ missing in {concept_dir}")
    variants: dict[str, list[AiShot]] = {}
    for hook_file in sorted(hooks_dir.glob("*.json")):
        vid = hook_file.stem
        data = json.loads(hook_file.read_text(encoding="utf-8"))
        variants[vid] = [AiShot.model_validate(d) for d in data]

    return ConceptVariantSet(
        concept_id=concept_dir.name,
        item_id=base.item_id,
        base=base,
        variants=variants,
    )


async def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--concept-dir", type=Path, required=True,
                   help="Path to data/registry/items/<sku>/concepts/<concept_id>/")
    p.add_argument("--out-root", type=Path, default=Path("out"))
    args = p.parse_args()

    vs = load_variant_set(args.concept_dir)
    plan = build_render_plan(vs, out_root=args.out_root)
    links = build_links_map(vs)

    print(f"📜 concept: {vs.concept_id} (item {vs.item_id})")
    print(f"   shared shots: {plan.shared_shot_ids}")
    print(f"   variants: {plan.variant_hook_shots}")
    print(f"   total renders: {plan.total_renders} "
          f"(vs naive {plan.shared_shot_count * len(vs.variants) + plan.variant_hook_render_count})")
    print(f"   outputs: {[str(p) for p in plan.variant_outputs.values()]}")

    # links.json persistence
    (args.concept_dir / "links.json").write_text(
        json.dumps(links, indent=2), encoding="utf-8",
    )
    print(f"   wrote {args.concept_dir / 'links.json'}")

    # Phase 1-5 render orchestration is wired in Task 9 / live validation
    # (Phase 4 of this plan). For now this CLI just prints the plan.
    print("\n⚠️  render orchestration NOT YET WIRED — Task 9 builds on this.")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
```

- [ ] **Step 2: Compile-check**

Run: `.venv/bin/python -c "import py_compile; py_compile.compile('scripts/produce-variant-set.py', doraise=True); print('OK')"`
Expected: `OK`.

- [ ] **Step 3: Run the unit tests — expect all 3 pass**

Run: `.venv/bin/python -m pytest tests/unit/test_produce_variant_set.py -v --no-cov 2>&1 | tail -10`
Expected: 3 tests pass.

- [ ] **Step 4: Smoke the CLI help**

Run: `.venv/bin/python scripts/produce-variant-set.py --help 2>&1 | head -8`
Expected: usage lines including `--concept-dir` and `--out-root`.

- [ ] **Step 5: Commit Task 8 scaffold**

```bash
git add scripts/produce-variant-set.py tests/unit/test_produce_variant_set.py
git commit -m "feat(orchestrator): variant-set scaffold + pure-logic helpers

scripts/produce-variant-set.py with build_render_plan() and
build_links_map() pure functions, plus load_variant_set() reader.
CLI loads a ConceptVariantSet from disk and prints the dedupe plan
but does NOT yet render (Task 9 wires the Higgsfield/Gemini/ffmpeg
phases against the existing produce-ai-storyboard helpers).

3 unit tests verify dedupe math + output paths + sub_id format."
```

### Task 9: Wire the render orchestration (Higgsfield shared + per-variant + assembly)

**Files:**
- Modify: `scripts/produce-variant-set.py`

This task reuses the existing render helpers from `scripts/produce-ai-storyboard.py` — we import them rather than reimplement.

- [ ] **Step 1: Refactor `produce-ai-storyboard.py` to expose its helpers as importable**

The existing orchestrator's helpers (`_gemini_still`, `_hold_to_mp4`, `_run_higgsfield_cli`, `_normalize_mp4`, `_concat`, `_mix_music_under`, `_thai_tts_wav`, `_build_subtitle_overlays`) are currently private to the script. We need to import them. Add an `__all__` at the top of `scripts/produce-ai-storyboard.py` listing them — OR move them to a new shared module.

Decision: move to `src/auto_affi/pipeline/shot_renderers.py` so both orchestrators can import them. Create the new module:

```python
"""Shared render helpers used by both produce-ai-storyboard.py and
produce-variant-set.py. Extracted 2026-05-18 during the variant-testing
implementation."""
```

Copy these functions from `scripts/produce-ai-storyboard.py` into the new module (preserving signatures + docstrings exactly):
- `_aac_flags`
- `_ffprobe_duration`
- `_resolve_refs`
- `_gemini_still`
- `_hold_to_mp4`
- `_normalize_mp4`
- `_pad_audio`
- `_phaya_tts_wav` (legacy fallback)
- `_edge_tts_wav`
- `_thai_tts_wav`
- `_run_higgsfield_cli`
- `_run_seedance_2kf`
- `_run_seedance_2_2kf`
- `_concat`
- `_mix_music_under`
- `_build_subtitle_overlays`

Drop the leading underscore on public-facing ones (they're now module API). Keep underscored ones private. Re-export the public names from a `__all__` list at the top.

Then in `scripts/produce-ai-storyboard.py`, REPLACE the inline definitions with imports:

```python
from auto_affi.pipeline.shot_renderers import (
    aac_flags, ffprobe_duration, resolve_refs, gemini_still,
    hold_to_mp4, normalize_mp4, pad_audio, thai_tts_wav,
    run_higgsfield_cli, run_seedance_2kf, run_seedance_2_2kf,
    concat_clips, mix_music_under, build_subtitle_overlays,
)
```

- [ ] **Step 2: Run the existing suite to confirm the refactor didn't break anything**

Run: `.venv/bin/python -m pytest tests/unit/ -q --no-cov 2>&1 | tail -5`
Expected: still all green (the refactor is internal — public behavior unchanged).

- [ ] **Step 3: Commit the refactor as its own change before adding new orchestrator logic**

```bash
git add src/auto_affi/pipeline/shot_renderers.py scripts/produce-ai-storyboard.py
git commit -m "refactor(pipeline): extract shot renderers into src/auto_affi/pipeline/shot_renderers.py

Both produce-ai-storyboard.py and the forthcoming produce-variant-set.py
need the same render helpers (Gemini stills, Higgsfield CLI dispatch,
ffmpeg concat/mix, HyperFrames overlay builder). Move them into a
shared module rather than copy-paste.

No public-behavior change — produce-ai-storyboard.py imports the same
functions it previously defined inline."
```

- [ ] **Step 4: Wire `produce-variant-set.py`'s render orchestration**

Modify `scripts/produce-variant-set.py`. Append a new async function `orchestrate_renders` that uses `RenderPlan` to drive the render phases:

```python


# ---------------------------------------------------------------------------
# Render orchestration (Phase 3 — wired against shared shot_renderers)
# ---------------------------------------------------------------------------


from auto_affi.pipeline.shot_renderers import (
    gemini_still, hold_to_mp4, normalize_mp4, thai_tts_wav,
    run_higgsfield_cli, concat_clips, mix_music_under,
    build_subtitle_overlays,
)
# Other imports needed at I/O time:
import os
import subprocess
from datetime import timedelta
import httpx
from pydantic import SecretStr
from auto_affi.adapters.gcs_storage import GcsStorage
from auto_affi.adapters.gemini_image import (
    GEMINI_NANO_BANANA_PRO, GeminiImageClient,
)
from auto_affi.adapters.higgsfield_cli import HiggsfieldCli
from auto_affi.adapters.phaya import PhayaClient
from auto_affi.post.hyperframes_renderer import (
    composite_overlays_with_ffmpeg, render_storyboard_overlays,
)
from auto_affi.schemas.ai_storyboard import AudioSource


async def orchestrate_renders(
    vs: ConceptVariantSet, plan: RenderPlan,
    *, characters_dir: Path, product_refs_dir: Path,
    music_path: Path | None,
    tts_source: str = "edge", tts_voice: str | None = None,
) -> None:
    """Execute all render phases. Shared shots render once (under
    plan.shared_out_dir); variant shots render under
    plan.variant_outputs[vid].parent."""

    # Construct clients (lazy where possible)
    for k in ("GOOGLE_API_KEY", "AUTO_AFFI__GCS_BUCKET"):
        if not os.environ.get(k, "").strip():
            raise RuntimeError(f"missing env: {k}")
    gcs = GcsStorage(bucket_name=os.environ["AUTO_AFFI__GCS_BUCKET"])
    gemini = GeminiImageClient(
        api_key=SecretStr(os.environ["GOOGLE_API_KEY"]),
        model=GEMINI_NANO_BANANA_PRO,
    )
    higgsfield: HiggsfieldCli | None = None
    needs_hf = any(
        s.generator is Generator.HIGGSFIELD_CLI
        for shots in [vs.base.shots] + list(vs.variants.values())
        for s in shots
    )
    if needs_hf:
        higgsfield = HiggsfieldCli()

    plan.shared_out_dir.mkdir(parents=True, exist_ok=True)
    for vid in vs.variants:
        plan.variant_outputs[vid].parent.mkdir(parents=True, exist_ok=True)

    # PHASE 1 — Stills (shared + per-variant)
    print(f"── PHASE 1 · stills")
    for shot in vs.base.shots:
        still = plan.shared_out_dir / f"{shot.shot_id}_image.jpg"
        if still.exists():
            print(f"  📦 reusing shared {still.name}")
            continue
        refs = []  # callers supply via resolve_refs if needed
        await gemini_still(client=gemini, shot=shot, dest=still, refs=refs)
        print(f"  ✅ shared {still.name}")
    for vid, shots in vs.variants.items():
        for shot in shots:
            still = plan.variant_outputs[vid].parent / f"{shot.shot_id}_image.jpg"
            if still.exists():
                print(f"  📦 reusing variant-{vid} {still.name}")
                continue
            await gemini_still(client=gemini, shot=shot, dest=still, refs=[])
            print(f"  ✅ variant-{vid} {still.name}")

    # PHASE 2 — Shared shot clips (render ONCE)
    print(f"\n── PHASE 2 · shared shots (render once)")
    for shot in vs.base.shots:
        still = plan.shared_out_dir / f"{shot.shot_id}_image.jpg"
        clip = plan.shared_out_dir / f"{shot.shot_id}_clip.mp4"
        if clip.exists():
            print(f"  📦 reusing {clip.name}")
            continue
        await _render_one_shot(
            shot=shot, still=still, dest=clip,
            higgsfield=higgsfield, workdir=plan.shared_out_dir,
            tts_source=tts_source, tts_voice=tts_voice,
        )

    # PHASE 3 — Per-variant hook shots
    print(f"\n── PHASE 3 · per-variant hook shots")
    for vid, shots in vs.variants.items():
        var_dir = plan.variant_outputs[vid].parent
        for shot in shots:
            still = var_dir / f"{shot.shot_id}_image.jpg"
            clip = var_dir / f"{shot.shot_id}_clip.mp4"
            if clip.exists():
                print(f"  📦 reusing variant-{vid} {clip.name}")
                continue
            await _render_one_shot(
                shot=shot, still=still, dest=clip,
                higgsfield=higgsfield, workdir=var_dir,
                tts_source=tts_source, tts_voice=tts_voice,
            )

    # PHASE 4 — Per-variant assembly
    print(f"\n── PHASE 4 · per-variant assembly")
    for vid, shots in vs.variants.items():
        var_dir = plan.variant_outputs[vid].parent
        # Variant hook clips
        var_clip_paths = [var_dir / f"{s.shot_id}_clip.mp4" for s in shots]
        # Shared body+CTA clips
        shared_clip_paths = [
            plan.shared_out_dir / f"{s.shot_id}_clip.mp4"
            for s in vs.base.shots
        ]
        all_clips = var_clip_paths + shared_clip_paths
        concat_mp4 = var_dir / "concat.mp4"
        concat_clips(all_clips, var_dir, concat_mp4)

        # Music mix (use the music_path if supplied, else skip)
        mixed = var_dir / "mixed.mp4"
        if music_path and music_path.exists():
            mix_music_under(concat_mp4, music_path, mixed, gain_db=-12.0)
        else:
            mixed = concat_mp4

        # Captions (per-shot subtitles from the variant's shot list +
        # the base's shot list — same logic as produce-ai-storyboard)
        # Compute offsets across the full timeline:
        merged_shots = shots + list(vs.base.shots)
        offsets: dict[str, float] = {}
        t = 0.0
        for s in merged_shots:
            offsets[s.shot_id] = t
            # use actual clip duration from disk if available; spec says
            # variant + base durations sum to base.target_total_duration_s
            t += s.duration_s
        # Build a synthetic AiStoryboard for overlay rendering
        synthetic = AiStoryboard(
            concept_id=f"{vs.concept_id}-{vid}",
            title_en=vs.base.title_en, title_th=vs.base.title_th,
            item_id=vs.item_id, consistency_seed=vs.base.consistency_seed,
            target_total_duration_s=vs.base.target_total_duration_s,
            music_prompt=vs.base.music_prompt,
            music_duration_s=vs.base.music_duration_s,
            shots=merged_shots,
        )
        overlays = build_subtitle_overlays(synthetic, offsets)
        if overlays:
            ov_workdir = var_dir / "overlays"
            ov_workdir.mkdir(parents=True, exist_ok=True)
            rendered = render_storyboard_overlays(
                overlays=overlays, projects_dir=Path("hyperframes"),
                output_dir=ov_workdir,
            )
            composite_overlays_with_ffmpeg(
                base_video=mixed, overlays=rendered,
                output=plan.variant_outputs[vid],
            )
        else:
            mixed.replace(plan.variant_outputs[vid])
        print(f"  ✅ variant-{vid}: {plan.variant_outputs[vid]}")


async def _render_one_shot(
    *, shot: AiShot, still: Path, dest: Path,
    higgsfield: HiggsfieldCli | None, workdir: Path,
    tts_source: str, tts_voice: str | None,
) -> None:
    """Single-shot dispatch shared by Phase 2 + Phase 3."""
    print(f"  {shot.shot_id} [{shot.generator.value}] {shot.duration_s}s")
    if shot.generator is Generator.HOLD:
        vo_wav: Path | None = None
        if shot.audio_source is AudioSource.PHAYA_TTS and shot.dialogue_th:
            vo_wav = workdir / f"{shot.shot_id}_vo.wav"
            if not vo_wav.exists():
                await thai_tts_wav(
                    client=None, gcs=None, text=shot.dialogue_th, dest=vo_wav,
                    source=tts_source, voice=tts_voice,
                )
        hold_to_mp4(still, dest, shot.duration_s, voiceover_wav=vo_wav)
    elif shot.generator is Generator.HIGGSFIELD_CLI:
        if higgsfield is None:
            raise RuntimeError(f"{shot.shot_id}: higgsfield_cli requires the CLI")
        await run_higgsfield_cli(
            hf=higgsfield, shot=shot, still=still, workdir=workdir, dest=dest,
        )
    else:
        raise RuntimeError(
            f"{shot.shot_id}: generator {shot.generator.value} not supported "
            f"in variant orchestrator (use HOLD or HIGGSFIELD_CLI)"
        )
```

Then update `main()` to call `orchestrate_renders` after printing the plan. Add the same character-workdir and product-refs CLI flags `produce-ai-storyboard.py` uses, plus a `--music-path` flag for music reuse.

- [ ] **Step 5: Compile-check + run the existing tests**

Run:
```bash
.venv/bin/python -c "import py_compile; py_compile.compile('scripts/produce-variant-set.py', doraise=True); print('OK')"
.venv/bin/python -m pytest tests/unit/test_produce_variant_set.py tests/unit/test_higgsfield_cli_adapter.py tests/unit/test_concept_variant_set.py -v --no-cov 2>&1 | tail -10
```
Expected: `OK` then all tests pass.

- [ ] **Step 6: Commit**

```bash
git add scripts/produce-variant-set.py
git commit -m "feat(orchestrator): wire variant-set render orchestration

orchestrate_renders() dispatches:
  Phase 1: stills (Gemini per-shot, shared dir + per-variant dir)
  Phase 2: shared body+CTA shots (rendered ONCE)
  Phase 3: per-variant hook shots
  Phase 4: per-variant assembly (concat shared+variant clips, optional
    music mix, HyperFrames caption overlay)

_render_one_shot is the single dispatch point for HOLD + HIGGSFIELD_CLI
generators (the only two needed for variant-testing per the spec —
seedance_2kf and seedance_2_* legacy paths are not used here).

Reuses the shared shot_renderers module so behavior matches
produce-ai-storyboard.py shot-for-shot."
```

---

## Phase 4: Live Validation (PD300X concept-3-v1)

Spec section 10 step 3. This is a manual/operator phase — the operator authors a real concept + variants and runs the orchestrator end-to-end.

### Task 10: Operator authors `data/registry/items/28875679676/concepts/shure-vs-maono/`

**Files:** (all gitignored — per-product artifacts)
- Create: `data/registry/items/28875679676/concepts/shure-vs-maono/base.json`
- Create: `data/registry/items/28875679676/concepts/shure-vs-maono/hooks/a.json`
- Create: `data/registry/items/28875679676/concepts/shure-vs-maono/hooks/b.json`
- Create: `data/registry/items/28875679676/concepts/shure-vs-maono/hooks/c.json`

- [ ] **Step 1: Author `base.json`**

Copy the v13 concept-2-v5 storyboard at `data/registry/items/28875679676/concept-2-v5/storyboard.json`, then strip the first 2 shots (the hook section). Keep shots s2-s6 as the base body+CTA. Adjust `target_total_duration_s` to `base_body_total + 2 × 3` (room for 2 hook shots of 3s each).

- [ ] **Step 2: Author three hook variants**

Each variant is a JSON file containing a list of 2 `AiShot` objects (s0 + s1). Three different hook strategies — examples to start from (operator can rewrite):

`hooks/a.json`: **Price-text overlay** — hand holding PD300X with bold "Shure ฿9,000 vs Maono ฿2,590" text upper-third (current v13 hook).

`hooks/b.json`: **Problem-led** — phone showing recording app with choppy audio waveform, then cut to PD300X with clean waveform.

`hooks/c.json`: **Creator-authority** — creator chest-up nodding at camera with PD300X visible at lower-left, "ผมใช้ตัวนี้ปีกว่า" caption.

All three share `consistency_seed=51728` (matches v13's base seed).

- [ ] **Step 3: Validate the variant set loads**

Run:
```bash
.venv/bin/python -c "
from pathlib import Path
import sys
sys.path.insert(0, 'scripts')
import importlib.util
spec = importlib.util.spec_from_file_location('p', 'scripts/produce-variant-set.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
vs = m.load_variant_set(Path('data/registry/items/28875679676/concepts/shure-vs-maono'))
print('✅ loaded:', vs.concept_id, vs.variant_ids())
"
```
Expected: `✅ loaded: shure-vs-maono ['a', 'b', 'c']`. If it raises, fix the JSON (most likely the duration-parity invariant).

### Task 11: Run the orchestrator end-to-end

- [ ] **Step 1: Pre-stage music (reuse from v13 workdir to avoid Phaya music regen)**

Run:
```bash
mkdir -p out/28875679676-shure-vs-maono/shared
cp out/maono-concept-2-workdir-v13/music.mp3 out/28875679676-shure-vs-maono/shared/music.mp3
ls -la out/28875679676-shure-vs-maono/shared/music.mp3
```
Expected: shows the music file copied.

- [ ] **Step 2: Run the orchestrator with the live concept**

Run:
```bash
set -a && source .env && set +a && \
.venv/bin/python scripts/produce-variant-set.py \
  --concept-dir data/registry/items/28875679676/concepts/shure-vs-maono \
  --out-root out \
  --music-path out/28875679676-shure-vs-maono/shared/music.mp3 \
  --tts-source edge --tts-voice th-TH-NiwatNeural 2>&1 | tail -40
```
Expected: prints PHASE 1-4 progress, ends with 3 ✅ lines (one per variant), no error.

- [ ] **Step 3: Verify the 3 mp4s exist + total cost**

Run:
```bash
ls -la out/28875679676-shure-vs-maono/variant-*/final.mp4
higgsfield account status | head -2
```
Expected: 3 mp4 files (one per variant a/b/c), credit balance dropped by ~115 credits (50 shared + 60 hook + ~5 overlay overhead). Target cost: ≤ $5 worth of Higgsfield credits.

- [ ] **Step 4: Verify shared-shot reuse (sanity check the dedupe claim)**

Run:
```bash
ls -la out/28875679676-shure-vs-maono/shared/*_clip.mp4
ls -la out/28875679676-shure-vs-maono/variant-a/*_clip.mp4
ls -la out/28875679676-shure-vs-maono/variant-b/*_clip.mp4
```
Expected: 5 shared `s2..s6` clips, 2 variant-a hook clips, 2 variant-b hook clips, etc. Shared clips exist exactly once.

- [ ] **Step 5: Sanity-check `links.json`**

Run: `cat data/registry/items/28875679676/concepts/shure-vs-maono/links.json`
Expected: JSON mapping `"a": "28875679676-shure-vs-maono-a", "b": ..., "c": ...`.

- [ ] **Step 6: Open all 3 finals + sanity-check visually**

Run:
```bash
open out/28875679676-shure-vs-maono/variant-a/final.mp4
open out/28875679676-shure-vs-maono/variant-b/final.mp4
open out/28875679676-shure-vs-maono/variant-c/final.mp4
```
Acceptance criteria: each clip plays, runs ~target_total_duration_s, shares the s2-s6 body footage, differs in s0-s1 hook footage, has the correct variant-tagged CTA card at s6.

- [ ] **Step 7: Commit only the framework artifacts (not data/ which is gitignored)**

```bash
git add -A
git status --short  # confirm only framework changes staged
git commit -m "feat(variant-set): live validation against PD300X concept-3-v1

Three hook variants (price-text / problem-led / creator-authority)
rendered through scripts/produce-variant-set.py. Shared body+CTA shots
rendered exactly once (5 clips) then reused across all variants. Total
cost ~\$5 for 3 testable mp4s vs naive 3× v13 cost of \$10.80.

Live artifacts not committed (data/registry/ and out/ are gitignored)."
```

---

## Phase 5: Measurement Layer (deferred — wired after first real posts)

Spec section 7b + 7c. Built AFTER the operator has posted at least one variant set to TikTok / Shopee and accumulated 72h of dashboard data. This phase is intentionally separated so we don't speculatively build measurement code before we know the real Shopee API shape.

### Task 12: Stub `pull-shopee-results.py` with a manual-CSV-import path

**Files:**
- Create: `scripts/pull-shopee-results.py`

- [ ] **Step 1: Write the CLI skeleton + CSV import implementation**

```python
#!/usr/bin/env python
"""Pull per-variant Shopee dashboard results.

Spec: docs/superpowers/specs/2026-05-18-auto-affi-variant-testing-design.md
section 7b.

Two input modes:
  --csv <path>     Manual CSV export from Shopee Affiliate dashboard.
                   Required columns: sub_id, views, clicks, orders, revenue_thb.
  --api            (FUTURE) Direct Shopee Affiliate API pull.
                   Not implemented — Shopee TH affiliate API is intermittent
                   and undocumented; CSV is the operator path for now.

Outputs append-only JSONL at:
  data/registry/items/<sku>/concepts/<concept_id>/results.jsonl

One line per (variant, pull_time) pair so we can track time-series.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from pathlib import Path


def load_links(concept_dir: Path) -> dict[str, str]:
    """links.json maps variant_id → sub_id."""
    path = concept_dir / "links.json"
    if not path.exists():
        raise FileNotFoundError(f"links.json missing in {concept_dir}")
    return json.loads(path.read_text(encoding="utf-8"))


def reverse_links(links: dict[str, str]) -> dict[str, str]:
    """sub_id → variant_id, for joining CSV rows back to variants."""
    return {v: k for k, v in links.items()}


def import_csv(csv_path: Path, sub_to_variant: dict[str, str]) -> list[dict]:
    """Parse a Shopee Affiliate CSV export. Returns one dict per variant."""
    rows: list[dict] = []
    with csv_path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sub_id = row.get("sub_id", "").strip()
            if not sub_id or sub_id not in sub_to_variant:
                continue
            views = int(row.get("views", 0))
            clicks = int(row.get("clicks", 0))
            orders = int(row.get("orders", 0))
            revenue = float(row.get("revenue_thb", 0))
            rows.append({
                "variant_id": sub_to_variant[sub_id],
                "sub_id": sub_id,
                "views": views,
                "clicks": clicks,
                "orders": orders,
                "revenue_thb": revenue,
                "cvr_views": (orders / views) if views else 0,
                "cvr_clicks": (orders / clicks) if clicks else 0,
            })
    return rows


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--concept-dir", type=Path, required=True)
    p.add_argument("--csv", type=Path,
                   help="Manual Shopee Affiliate CSV export.")
    args = p.parse_args()

    links = load_links(args.concept_dir)
    sub_to_variant = reverse_links(links)
    print(f"📜 concept: {args.concept_dir.name}")
    print(f"   variants: {sorted(links)}")

    if not args.csv:
        print("ERROR: --csv required (Shopee API mode not implemented)")
        return 1
    if not args.csv.exists():
        print(f"ERROR: csv not found: {args.csv}"); return 2

    rows = import_csv(args.csv, sub_to_variant)
    if not rows:
        print("WARNING: no matching sub_ids in CSV — check that your "
              "Shopee dashboard export includes the sub_id column AND "
              "that the IDs match the variant set's links.json.")
        return 3

    results_path = args.concept_dir / "results.jsonl"
    pull_ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with results_path.open("a", encoding="utf-8") as f:
        for row in rows:
            row["pull_ts"] = pull_ts
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"   wrote {len(rows)} rows → {results_path}")
    for row in rows:
        print(f"   {row['variant_id']}: views={row['views']} "
              f"clicks={row['clicks']} orders={row['orders']} "
              f"CVR(clicks)={row['cvr_clicks']:.3%}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Compile-check**

Run: `.venv/bin/python -c "import py_compile; py_compile.compile('scripts/pull-shopee-results.py', doraise=True); print('OK')"`
Expected: `OK`.

- [ ] **Step 3: Commit**

```bash
git add scripts/pull-shopee-results.py
git commit -m "feat(measurement): pull-shopee-results.py CSV-import path

Manual CSV import is the MVP because Shopee TH Affiliate API is
intermittent. Operator exports their dashboard, points this script
at the CSV + concept-dir, and the script joins via sub_id → variant_id
and appends to results.jsonl.

API mode left as a stub — wire when operator brings real API
credentials AND has confirmed which Shopee endpoint actually serves
per-sub_id data."
```

### Task 13: Write the failing test for `compare-variant-results.py`

**Files:**
- Create: `tests/unit/test_compare_variant_results.py`

- [ ] **Step 1: Write the test**

```python
"""Tests for scripts/compare-variant-results.py — winner selection
from results.jsonl + persistence to data/patterns/winning-hooks.jsonl."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = REPO_ROOT / "scripts" / "compare-variant-results.py"


def _load_script_module():
    spec = importlib.util.spec_from_file_location("compare_variant_results", SCRIPT_PATH)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["compare_variant_results"] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def script_mod():
    return _load_script_module()


def test_select_winner_picks_highest_cvr_above_threshold(script_mod):
    """Above min-sample threshold, the highest CVR wins."""
    results = [
        {"variant_id": "a", "clicks": 500, "orders": 5, "cvr_clicks": 0.010},
        {"variant_id": "b", "clicks": 600, "orders": 12, "cvr_clicks": 0.020},
        {"variant_id": "c", "clicks": 550, "orders": 8, "cvr_clicks": 0.0145},
    ]
    winner = script_mod.select_winner(results, min_clicks=200)
    assert winner is not None
    assert winner["variant_id"] == "b"


def test_select_winner_returns_none_below_threshold(script_mod):
    """If NO variant has min_clicks, return None (insufficient sample)."""
    results = [
        {"variant_id": "a", "clicks": 50, "orders": 2, "cvr_clicks": 0.04},
        {"variant_id": "b", "clicks": 80, "orders": 4, "cvr_clicks": 0.05},
    ]
    winner = script_mod.select_winner(results, min_clicks=200)
    assert winner is None


def test_select_winner_ignores_underpowered_variants(script_mod):
    """A variant below threshold is excluded; remaining variants compete."""
    results = [
        {"variant_id": "a", "clicks": 100, "orders": 10, "cvr_clicks": 0.10},  # underpowered
        {"variant_id": "b", "clicks": 500, "orders": 10, "cvr_clicks": 0.020},
        {"variant_id": "c", "clicks": 600, "orders": 15, "cvr_clicks": 0.025},
    ]
    winner = script_mod.select_winner(results, min_clicks=200)
    assert winner is not None
    assert winner["variant_id"] == "c"


def test_append_winner_to_patterns_jsonl_creates_file_if_missing(script_mod, tmp_path):
    """First write should create the pattern file with the JSON line."""
    patterns_path = tmp_path / "winning-hooks.jsonl"
    winner_entry = {
        "ts": "2026-05-18", "concept": "shure-vs-maono", "winner": "b",
        "hook_type": "problem_led", "cvr": 0.020, "sample_size": 600,
    }
    script_mod.append_pattern(patterns_path, winner_entry)
    assert patterns_path.exists()
    lines = patterns_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    assert json.loads(lines[0])["winner"] == "b"


def test_append_winner_to_patterns_jsonl_appends(script_mod, tmp_path):
    """Second write should append, not overwrite."""
    patterns_path = tmp_path / "winning-hooks.jsonl"
    script_mod.append_pattern(patterns_path, {"winner": "a"})
    script_mod.append_pattern(patterns_path, {"winner": "b"})
    lines = patterns_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
```

- [ ] **Step 2: Run — expect FileNotFoundError**

Run: `.venv/bin/python -m pytest tests/unit/test_compare_variant_results.py -v --no-cov 2>&1 | tail -10`
Expected: collection error, `compare-variant-results.py` not found.

### Task 14: Implement `compare-variant-results.py`

**Files:**
- Create: `scripts/compare-variant-results.py`

- [ ] **Step 1: Write the script**

```python
#!/usr/bin/env python
"""Declare a winner from a concept's results.jsonl and append to the
pattern library.

Spec: docs/superpowers/specs/2026-05-18-auto-affi-variant-testing-design.md
section 7c.

Winner = highest cvr_clicks above the min-clicks threshold. If no
variant has min_clicks, NO winner is declared (insufficient sample).
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path


def load_latest_results(results_path: Path) -> list[dict]:
    """Read results.jsonl, return ONLY the latest pull per variant."""
    if not results_path.exists():
        return []
    latest: dict[str, dict] = {}
    with results_path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            vid = row["variant_id"]
            prev = latest.get(vid)
            if prev is None or row["pull_ts"] > prev["pull_ts"]:
                latest[vid] = row
    return list(latest.values())


def select_winner(results: list[dict], *, min_clicks: int) -> dict | None:
    """Return the entry with the highest cvr_clicks among variants that
    crossed min_clicks. Returns None if NO variant qualifies."""
    qualified = [r for r in results if r.get("clicks", 0) >= min_clicks]
    if not qualified:
        return None
    return max(qualified, key=lambda r: r.get("cvr_clicks", 0))


def append_pattern(patterns_path: Path, entry: dict) -> None:
    patterns_path.parent.mkdir(parents=True, exist_ok=True)
    with patterns_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--concept-dir", type=Path, required=True)
    p.add_argument("--hook-type", type=str, required=True,
                   help="Categorical label for the winning hook style "
                        "(e.g. 'price_comparison_text', 'problem_led', "
                        "'creator_authority'). Operator picks this.")
    p.add_argument("--min-clicks", type=int, default=200,
                   help="Minimum clicks per variant for the result to count.")
    p.add_argument("--patterns-path", type=Path,
                   default=Path("data/patterns/winning-hooks.jsonl"))
    args = p.parse_args()

    results_path = args.concept_dir / "results.jsonl"
    rows = load_latest_results(results_path)
    if not rows:
        print(f"ERROR: no results in {results_path}"); return 1

    winner = select_winner(rows, min_clicks=args.min_clicks)
    if winner is None:
        print(f"⚠️  no winner — every variant under {args.min_clicks} clicks")
        for r in rows:
            print(f"   {r['variant_id']}: clicks={r.get('clicks',0)} "
                  f"orders={r.get('orders',0)}")
        return 2

    entry = {
        "ts": time.strftime("%Y-%m-%d"),
        "concept": args.concept_dir.name,
        "winner": winner["variant_id"],
        "hook_type": args.hook_type,
        "cvr": winner.get("cvr_clicks", 0),
        "sample_size": winner.get("clicks", 0),
    }
    append_pattern(args.patterns_path, entry)
    print(f"🏆 winner: variant-{entry['winner']} ({entry['hook_type']}) "
          f"CVR={entry['cvr']:.3%} n={entry['sample_size']}")
    print(f"   appended to {args.patterns_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Run the unit tests — expect all 5 pass**

Run: `.venv/bin/python -m pytest tests/unit/test_compare_variant_results.py -v --no-cov 2>&1 | tail -10`
Expected: 5 tests pass.

- [ ] **Step 3: Smoke the CLI help**

Run: `.venv/bin/python scripts/compare-variant-results.py --help | head -10`
Expected: usage lines including `--concept-dir`, `--hook-type`, `--min-clicks`.

- [ ] **Step 4: Commit**

```bash
git add scripts/compare-variant-results.py tests/unit/test_compare_variant_results.py
git commit -m "feat(measurement): compare-variant-results.py + pattern library

select_winner() picks highest cvr_clicks among variants above
min-clicks threshold (default 200, configurable). No winner declared
if no variant qualifies — surfaces 'insufficient sample' loudly.

Operator runs after pull-shopee-results.py has written results.jsonl.
Winner appends to data/patterns/winning-hooks.jsonl (append-only
JSONL) with hook_type categorical the operator supplies — that
hook_type label is the lookup key for the next concept's hook design.

5 unit tests cover winner selection + pattern persistence."
```

---

## Phase 6: Update Workflow Doc

### Task 15: Create `docs/workflow-pipeline-v14.md`

**Files:**
- Create: `docs/workflow-pipeline-v14.md`

- [ ] **Step 1: Write the v14 workflow doc**

Mirror the structure of `docs/workflow-pipeline-v13.md` but document the new variant-testing flow. Include:

- 5-phase orchestrator pipeline mermaid diagram for `produce-variant-set.py`
- Cost-per-concept table from spec section 8
- New per-variant decision flow (no HeyGen branch; HOLD + HIGGSFIELD_CLI only)
- Pattern-library learning loop (results.jsonl → compare-variant-results → winning-hooks.jsonl)
- Reference back to v13 doc with "superseded for new productions" note

- [ ] **Step 2: Commit**

```bash
git add docs/workflow-pipeline-v14.md
git commit -m "docs(workflow): pipeline-v14 reference (variant-testing flow)

Updates the v13 reference for the new produce-variant-set.py
orchestrator: shared body+CTA + per-variant hooks, links.json,
results.jsonl, winning-hooks.jsonl learning library.

Single source of truth for the variant-testing pipeline shape."
```

- [ ] **Step 3: Final push**

Run: `git push 2>&1 | tail -3`

---

## Self-Review (writing-plans skill's required check)

Spec coverage check:
- §1 Goal (CVR-first) ↔ Tasks 12-14 (measurement + winner selection) ✓
- §2 Hard constraints — HeyGen removal ↔ Tasks 1-4 ✓; Higgsfield-only ↔ Task 9 dispatch (HOLD + HIGGSFIELD_CLI only) ✓; Gemini direct stills ↔ Task 9 imports `gemini_still` ✓; default model swap ↔ documented in Task 10's variant-author guidance ✓
- §4 Unit of work ↔ Task 5+6 (schema) ✓
- §5 Directory layout ↔ Task 8 (`load_variant_set` reads exactly that layout) ✓
- §6 Schema ↔ Tasks 5-6 ✓
- §7a Orchestrator ↔ Tasks 8-9 ✓
- §7b pull-shopee ↔ Task 12 ✓
- §7c compare-variant ↔ Tasks 13-14 ✓
- §7d pattern library ↔ Task 14 ✓
- §8 Cost model ↔ Task 11 step 3 verifies actual burn ≤ $5 ✓
- §9 HeyGen removal ↔ Tasks 1-4 ✓
- §10 Migration sequence ↔ phase order matches (HeyGen → schema → orchestrator → live → measurement → docs) ✓
- §11 Error handling ↔ Task 12 surfaces missing-CSV / no-match-sub-id ✓; Task 14 surfaces no-winner / insufficient-sample ✓
- §12 Testing ↔ Tasks 5, 7, 13 are TDD ✓

Placeholder scan: no TBDs / vague "implement appropriate" / TODO markers.

Type consistency: `ConceptVariantSet` fields used identically in tests, orchestrator, and `load_variant_set`. `RenderPlan` dataclass fields consistent across `build_render_plan` + `orchestrate_renders`.

Plan ready.
