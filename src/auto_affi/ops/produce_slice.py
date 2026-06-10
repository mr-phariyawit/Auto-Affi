"""Offline vertical slice orchestrator — AFFI-S1-08 DoD.

Chains every built component into a single end-to-end run:
  DryRunShopeeSource → scout score → strategist → writers' room →
  HSO x VCS rubric lint → dry render (6 shots) → assemble master →
  compliance gate → registry → budget check.

Zero paid calls. Zero network. Only ffmpeg (local) + dry-run fixtures.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from auto_affi.adapters.shopee import DryRunShopeeSource, ShopeeProduct, get_fixture_products
from auto_affi.agents.scout_scoring import ScoutInput
from auto_affi.agents.scout_scoring import score as scout_score
from auto_affi.agents.strategist import build_brief
from auto_affi.agents.writers_room import build_storyboard
from auto_affi.pipeline.compliance_gate import ComplianceReport, run_compliance
from auto_affi.pipeline.dry_render import assemble_master, render_shot
from auto_affi.pipeline.editor_budget import EditorBudgetTracker, PassMode
from auto_affi.pipeline.hso_vcs_rubric import RubricReport, lint_storyboard
from auto_affi.registry.local_jsonl import LocalJsonlRegistry
from auto_affi.schemas.storyboard import Storyboard
from auto_affi.workflows.budget import BudgetCircuitBreaker, BudgetDecision

# ---------------------------------------------------------------------------
# Result model
# ---------------------------------------------------------------------------


class SliceResult(BaseModel):
    """Result of a single offline vertical-slice run."""

    product_title: str
    master_path: Path
    compliance: ComplianceReport
    rubric: RubricReport
    cost_usd: float
    run_id: str


# ---------------------------------------------------------------------------
# Adapters for compliance gate
# ---------------------------------------------------------------------------


@dataclass
class _VoSegmentImpl:
    """Minimal VoSegment — satisfies the VoSegment Protocol (raw_audio_s + slot_s)."""

    raw_audio_s: float
    slot_s: float


class _SceneProxy:
    """Proxy that exposes ``dialogue_th`` for one scene, as the compliance gate expects."""

    def __init__(self, dialogue_th: str | None) -> None:
        self.dialogue_th = dialogue_th


class _StoryboardComplianceAdapter:
    """Wrap a v1 Storyboard so the compliance gate can read ``.shots``.

    The compliance gate looks for:
      - `storyboard.shots` (list) where each element has ``.dialogue_th``

    The v1 Storyboard uses ``.scenes`` where each scene has ``.dialogue.text_th``.
    This adapter bridges the two shapes without touching either module.
    """

    def __init__(self, storyboard: Storyboard) -> None:
        self._sb = storyboard
        self.shots: list[Any] = [
            _SceneProxy(
                dialogue_th=(
                    scene.dialogue.text_th
                    if scene.dialogue and scene.dialogue.text_th.strip()
                    else None
                )
            )
            for scene in storyboard.scenes
        ]


# ---------------------------------------------------------------------------
# Scout-input helper — derive from ShopeeProduct using sensible defaults
# ---------------------------------------------------------------------------


def _product_to_scout_input(product: ShopeeProduct) -> ScoutInput:
    """Map a ShopeeProduct to a ScoutInput using sensible Phase-1 defaults.

    Fields not present on ShopeeProduct default to neutral values so the
    scoring formula runs without hard-filtering on missing data.
    """
    # Derive AOV from mid-point of price band
    aov = (product.price_min + product.price_max) / 2.0

    # Map product name keywords to a category string for the scoring rubric.
    name = product.name
    if any(kw in name for kw in ("ครีม", "SPF", "กันแดด", "สกิน", "ผิว")):
        category = "beauty_skincare"
    elif any(kw in name for kw in ("ร่ม", "กันฝน")):
        category = "mom_baby"
    elif any(kw in name for kw in ("ซอง", "กระเป๋า", "กันน้ำ", "2-in-1")):
        category = "gadgets_accessories"
    else:
        category = "home"

    return ScoutInput(
        category=category,
        commission_rate=product.commission_rate,
        aov_thb=aov,
        shop_rating=product.rating_star,
        review_count=product.sales,         # proxy: sales ≈ review count floor
        sales_velocity_7d=min(product.sales // 52, 300),  # rough weekly velocity
        tiktok_mention_growth_7d=0.0,
        saturation_count_7d=0,
        shop_catalog_size=50,
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def run_offline_slice(out_dir: Path, *, product: ShopeeProduct | None = None) -> SliceResult:
    """Run the full offline vertical slice and return a SliceResult.

    Steps
    -----
    1. Pick a fixture product (or use the supplied one).
    2. Scout-score the product (deterministic).
    3. Build a CampaignBrief (strategist, deterministic).
    4. Build a Storyboard (writers' room, deterministic).
    5. Lint with HSO x VCS rubric (raise on failure).
    6. Render 6 shots into out_dir/clips/ using ffmpeg lavfi.
    7. Assemble master → out_dir/master.mp4.
    8. Build VO segments + caption lines (dry-run: speed_factor == 1.0).
    9. Run compliance gate.
    10. Register a RunEntry via LocalJsonlRegistry.
    11. Check budget via BudgetCircuitBreaker (all costs == 0.0).

    Parameters
    ----------
    out_dir
        Directory where clips/ and master.mp4 are written.
    product
        Optional override fixture product. Defaults to the highest-scoring
        fixture (first non-rejected hit from get_fixture_products()).

    Returns
    -------
    SliceResult
        Fully-populated result; callers should check result.compliance.ok.
    """
    out_dir = Path(out_dir)
    clips_dir = out_dir / "clips"
    clips_dir.mkdir(parents=True, exist_ok=True)

    # --- 1. Pick product ------------------------------------------------ #
    if product is None:
        source = DryRunShopeeSource(dry_run=True)
        candidates = source.fetch_products()
        if not candidates:
            candidates = get_fixture_products()

        # Score each candidate; pick highest scorer (first non-rejected)
        best: ShopeeProduct | None = None
        best_score: float = -1.0
        for p in candidates:
            si = _product_to_scout_input(p)
            s = scout_score(si)
            if not s.rejected and s.score > best_score:
                best_score = s.score
                best = p

        if best is None:
            # Fallback: use first fixture regardless of score
            best = candidates[0]
        product = best

    # --- 2. Scout score ------------------------------------------------- #
    scout_input = _product_to_scout_input(product)
    s_result = scout_score(scout_input)
    numeric_score: float = s_result.score if not s_result.rejected else 0.0

    # --- 3. Campaign brief ---------------------------------------------- #
    brief = build_brief(product, scout_score=numeric_score)

    # --- 4. Storyboard -------------------------------------------------- #
    storyboard: Storyboard = build_storyboard(brief, product)

    # --- 5. Rubric lint ------------------------------------------------- #
    rubric = lint_storyboard(storyboard)
    if not rubric.ok:
        raise RuntimeError(
            f"Rubric lint failed for '{product.name}': {rubric.violations}"
        )

    # --- 6. Render shots ------------------------------------------------ #
    clips: list[Path] = []
    for scene in storyboard.scenes:
        clip_path = clips_dir / f"shot_{scene.idx:02d}.mp4"
        render_shot(scene, clip_path)
        clips.append(clip_path)

    # --- 7. Assemble master --------------------------------------------- #
    master_path = out_dir / "master.mp4"
    assemble_master(clips, master_path)

    # --- 8. VO segments + captions -------------------------------------- #
    # Dry-run: raw_audio_s == slot_s (speed_factor == 1.0 exactly)
    # One segment per scene that has dialogue text.
    vo_segments: list[_VoSegmentImpl] = []
    caption_lines: list[str] = []

    for scene in storyboard.scenes:
        if scene.dialogue and scene.dialogue.text_th.strip():
            vo_segments.append(
                _VoSegmentImpl(
                    raw_audio_s=scene.duration_s,
                    slot_s=scene.duration_s,
                )
            )
            # Caption line mirrors the dialogue text
            caption_lines.append(scene.dialogue.text_th)

    # Wrap storyboard so compliance gate can read .shots
    sb_adapter = _StoryboardComplianceAdapter(storyboard)

    # --- 9. Compliance gate --------------------------------------------- #
    compliance = run_compliance(
        master_path,
        sb_adapter,
        source_clips=clips,
        vo_segments=vo_segments,  # type: ignore[arg-type]
        caption_lines=caption_lines,
        profile_s=storyboard.total_duration_s,
    )

    # --- 10. Registry --------------------------------------------------- #
    run_id = uuid.uuid4().hex[:16]
    registry = LocalJsonlRegistry(out_dir / "registry")

    # Register the product (idempotent)
    product_entry = registry.register_product(
        item_id=product.item_id,
        shop_id=product.shop_id,
        url=product.shopee_url or f"https://shopee.co.th/i.{product.shop_id}.{product.item_id}",
        name=product.name,
        niche="offline_fixture",
        persona_label=brief.persona.label,
        persona_pain_points=brief.persona.pain_points,
        angle=brief.angle,
        hook_template=brief.hook_template_slug,
        cta_text=brief.cta.text_th,
        hypothesis=brief.hypothesis,
        expected_ctr=brief.expected_ctr,
        price_min_thb=product.price_min,
        price_max_thb=product.price_max,
        commission_rate=product.commission_rate,
    )

    # Start + finalize run
    run_entry = registry.start_run(
        order_no=product_entry.order_no,
        run_id=run_id,
        publish_mode="dry_run",
    )
    registry.finalize_run(
        run_no=run_entry.run_no,
        order_no=product_entry.order_no,
        status="APPROVED" if compliance.ok else "REJECTED",
        total_cost_thb=0.0,
        final_mp4_gs_uri=str(master_path.resolve()),
        scene_count=len(storyboard.scenes),
        last_decision="offline_slice_run",
    )

    # --- 11. Budget check ----------------------------------------------- #
    budget = BudgetCircuitBreaker()
    # All costs are 0.0 in dry-run — record each node at 0.0
    for node in ["scout_strategist_llm", "writer_llm", "editor_agent", "video_gen", "tts"]:
        decision = budget.check_budget(node, 0.0)
        assert decision in (BudgetDecision.ALLOW, BudgetDecision.ALERT), (
            f"Budget circuit breaker DENIED node={node} unexpectedly"
        )
        budget.record_spend(node, 0.0)

    # Editor budget (also 0.0 — all ffmpeg fallback in dry-run)
    editor_tracker = EditorBudgetTracker(budget_usd=0.40)
    editor_tracker.record("offline_dry_run", cost_usd=0.0, mode=PassMode.FFMPEG_FALLBACK)
    total_cost_usd = editor_tracker.spent_usd  # 0.0

    return SliceResult(
        product_title=product.name,
        master_path=master_path,
        compliance=compliance,
        rubric=rubric,
        cost_usd=total_cost_usd,
        run_id=run_id,
    )


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def main() -> int:
    """Run the offline slice into out/slice/ and print a summary.

    Exits 0 if compliance.ok, else 1.
    """

    out_dir = Path("out") / "slice"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Running offline vertical slice → {out_dir.resolve()}")
    result = run_offline_slice(out_dir)

    print()
    print(f"  product  : {result.product_title}")
    print(f"  master   : {result.master_path}")
    print(f"  run_id   : {result.run_id}")
    print(f"  cost_usd : {result.cost_usd}")
    print(f"  rubric   : ok={result.rubric.ok}  violations={result.rubric.violations}")
    print(f"  compliance: ok={result.compliance.ok}")
    if not result.compliance.ok:
        for v in result.compliance.violations:
            print(f"    VIOLATION: {v}")

    if result.compliance.ok:
        print()
        print("PASS — compliance OK, cost $0.00")
        return 0
    else:
        print()
        print("FAIL — compliance not OK")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
