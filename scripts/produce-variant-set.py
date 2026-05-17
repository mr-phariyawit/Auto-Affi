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
