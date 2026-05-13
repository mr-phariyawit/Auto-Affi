"""End-to-end run_once entrypoint — fire the entire loop once.

Usage:
    .venv/bin/python -m auto_affi.ops.run_once --product-id 12345

Chains: Scout(stub) -> Strategist -> Writers Room -> Safety Gate ->
        Publisher(dry-run) -> Analytics(dry-run).

All steps use dry-run / fixture transports. No live API credentials
required. This is the manual trigger that proves the loop is closed.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

from auto_affi.adapters.publisher import DryRunPublisher
from auto_affi.adapters.shopee import ShopeeProduct
from auto_affi.adapters.shopee_public import (
    fetch_or_fixture,
    find_fixture_by_item_id,
    parse_url_to_ids,
)
from auto_affi.agents.analytics_collector import (
    AnalyticsCollector,
    DryRunMetricsTransport,
)
from auto_affi.agents.caption_builder import CaptionInput, Platform, build_caption
from auto_affi.agents.safety_gate import safety_gate
from auto_affi.agents.writers_room import WritersRoom
from auto_affi.schemas.campaign_brief import (
    CTA,
    BriefStatus,
    CampaignBrief,
    Persona,
)
from auto_affi.schemas.metrics import PollSchedule


@dataclass
class RunOnceResult:
    """Result of a single end-to-end pipeline run."""

    product_id: int
    brief_id: str = ""
    storyboard_id: str = ""
    safety_passed: bool = False
    publish_record_id: str = ""
    outcome_label: str = ""
    steps_completed: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def success(self) -> bool:
        return len(self.errors) == 0 and self.safety_passed


def _stub_product(product_id: int) -> ShopeeProduct:
    """Create a stub product for testing without Shopee API."""
    return ShopeeProduct(
        item_id=product_id,
        shop_id=100,
        name="เซรั่มวิตามินซี ผิวใส",
        price_min=299,
        price_max=399,
        commission_rate=0.08,
        rating_star=4.8,
        sales=1500,
        image_url="https://example.com/product.jpg",
    )


def _stub_brief(product: ShopeeProduct) -> CampaignBrief:
    """Create a stub campaign brief (Beauty niche default)."""
    return CampaignBrief(
        product_id=product.item_id,
        shop_id=product.shop_id,
        persona=Persona(
            label="Thai women 18-30",
            age_range="18-30",
            pain_points=["dull skin", "acne scars"],
            daily_context="scrolls IG Reels and Shopee daily",
        ),
        angle="ผิวกระจ่างใสใน 7 วัน ด้วยวิตามินซีเข้มข้น",
        hook_template_slug="curiosity_gap",
        cta=CTA(text_th="แตะลิงก์ใต้คลิปเลย!", placement="pinned_comment"),
        hypothesis="Curiosity gap + before/after for skincare drives Thai CTR",
        expected_ctr=0.035,
        confidence=0.7,
        status=BriefStatus.APPROVED,
    )


_NICHE_BRIEFS: dict[str, dict[str, object]] = {
    "Electronics/hardware-tools": {
        "persona": {
            "label": "Thai DIY enthusiasts + home mechanics",
            "age_range": "25-50",
            "pain_points": [
                "wrenches slip off bolt heads",
                "wrong-size sockets for tight spaces",
                "no extension bar for recessed nuts",
            ],
            "daily_context": "weekend home repairs, motorcycle maintenance, scrolls TikTok DIY hacks",
        },
        "angle": "8-14มม. ครบในชุดเดียว ใช้กับสว่านไฟฟ้าได้เลย ไม่ต้องเปลี่ยนหัว",
        "hook_template_slug": "problem_solution",
        "cta_text": "ครบทุกขนาด ลิงก์ใต้คลิป",
        "hypothesis": "DIY tool kits with size completeness + drill-compat hook drive contractors CTR",
        "expected_ctr": 0.028,
    },
    "Beauty/skincare": {
        "persona": {
            "label": "Thai women 18-30",
            "age_range": "18-30",
            "pain_points": ["dull skin", "acne scars"],
            "daily_context": "scrolls IG Reels and Shopee daily",
        },
        "angle": "ผิวกระจ่างใสใน 7 วัน ด้วยวิตามินซีเข้มข้น",
        "hook_template_slug": "curiosity_gap",
        "cta_text": "แตะลิงก์ใต้คลิปเลย!",
        "hypothesis": "Curiosity gap + before/after for skincare drives Thai CTR",
        "expected_ctr": 0.035,
    },
}


def _niche_aware_brief(
    product: ShopeeProduct, niche_hints: dict[str, object] | None
) -> CampaignBrief:
    """Build a CampaignBrief whose persona+angle+CTA fit the product's niche.

    Reads ``niche_hints`` block from the fixture file if present; otherwise
    falls back to keyword detection on the product name, then to the
    Beauty/skincare default.
    """
    niche_key = "Beauty/skincare"
    if niche_hints:
        niche = str(niche_hints.get("niche") or "").strip()
        sub = str(niche_hints.get("sub_niche") or "").strip()
        if niche and sub:
            niche_key = f"{niche}/{sub}"
        elif niche:
            niche_key = niche
    else:
        # Fallback keyword detection on product name
        name_lower = product.name.lower()
        if any(k in name_lower for k in ("socket", "bolt", "nut driver", "bit", "ประแจ")):
            niche_key = "Electronics/hardware-tools"

    spec = _NICHE_BRIEFS.get(niche_key) or _NICHE_BRIEFS["Beauty/skincare"]
    persona_dict: dict[str, object] = dict(spec["persona"])  # type: ignore[arg-type]
    return CampaignBrief(
        product_id=product.item_id,
        shop_id=product.shop_id,
        persona=Persona(**persona_dict),  # type: ignore[arg-type]
        angle=str(spec["angle"]),
        hook_template_slug=str(spec["hook_template_slug"]),
        cta=CTA(text_th=str(spec["cta_text"]), placement="pinned_comment"),
        hypothesis=str(spec["hypothesis"]),
        expected_ctr=float(spec["expected_ctr"]),  # type: ignore[arg-type]
        confidence=0.7,
        status=BriefStatus.APPROVED,
    )


def _resolve_product(
    *,
    product_id: int | None,
    shopee_url: str | None,
    fixture_path: Path | None,
) -> tuple[ShopeeProduct, dict[str, object] | None]:
    """Resolve a product + niche_hints from CLI args.

    Priority:
      1. ``--fixture <path>`` — load that fixture (niche_hints from JSON)
      2. ``--shopee-url <url>`` — parse, try fixture by item_id, niche_hints if found
      3. ``--product-id`` — synthesize the legacy beauty stub (no niche_hints)
    """
    if fixture_path is not None:
        raw = json.loads(fixture_path.read_text(encoding="utf-8"))
        product = ShopeeProduct(**raw["product"])
        return product, raw.get("niche_hints")
    if shopee_url is not None:
        product = fetch_or_fixture(url=shopee_url)
        shop_id, item_id = parse_url_to_ids(shopee_url)
        fx = find_fixture_by_item_id(item_id)
        niche_hints: dict[str, object] | None = None
        if fx is not None:
            try:
                niche_hints = json.loads(fx.read_text(encoding="utf-8")).get("niche_hints")
            except Exception:
                pass
        return product, niche_hints
    if product_id is None:
        product_id = 12345
    return _stub_product(product_id), None


async def run_once(
    product_id: int | None = None,
    *,
    shopee_url: str | None = None,
    fixture_path: Path | None = None,
) -> RunOnceResult:
    """Execute the full pipeline once with stub/dry-run transports.

    Source-of-truth for the product is, in priority order:
      1. ``fixture_path`` — explicit JSON fixture file
      2. ``shopee_url`` — Shopee URL, parsed for shop/item ids, fixture-resolved
      3. ``product_id`` — legacy stub path (synthesizes a beauty product)
    """
    product, niche_hints = _resolve_product(
        product_id=product_id, shopee_url=shopee_url, fixture_path=fixture_path
    )
    result = RunOnceResult(product_id=product.item_id)

    # Step 1: Scout (real product if URL/fixture; stub otherwise)
    result.steps_completed.append("scout")

    # Step 2: Strategist — niche-aware brief
    brief = _niche_aware_brief(product, niche_hints)
    result.brief_id = brief.brief_id
    result.steps_completed.append("strategist")

    # Step 3: Writers' Room
    room = WritersRoom()
    sb_result = await room.generate_storyboard(brief)
    if not sb_result.ok or sb_result.data is None:
        result.errors.append(f"writers_room: {sb_result.error}")
        return result
    storyboard = sb_result.data
    result.storyboard_id = storyboard.storyboard_id
    result.steps_completed.append("writers_room")

    # Step 4: Safety gate
    script_text = " ".join(
        s.dialogue.text_th for s in storyboard.scenes if s.dialogue
    )
    verdict = safety_gate(
        script_text_th=script_text,
        product_name=product.name,
    )
    result.safety_passed = verdict.passed
    if not verdict.passed:
        result.errors.append(f"safety: {verdict.block_reason}")
        return result
    result.steps_completed.append("safety_gate")

    # Step 5: Publisher (dry-run)
    publisher = DryRunPublisher()
    caption_input = CaptionInput(
        platform=Platform.IG,
        product_name=product.name,
        hook_text_th="ผิวใสใน 7 วัน!",
        affiliate_link="https://shp.ee/example",
        hashtags=["skincare", "shopee"],
        cta_text_th=brief.cta.text_th,
    )
    caption = build_caption(caption_input)
    pub_result = await publisher.publish(
        video_url="https://storage.example.com/video.mp4",
        caption=caption.text,
        affiliate_link="https://shp.ee/example",
    )
    if pub_result.ok and pub_result.data:
        result.publish_record_id = pub_result.data.platform_post_id
    result.steps_completed.append("publisher")

    # Step 6: Analytics (dry-run)
    collector = AnalyticsCollector(transport=DryRunMetricsTransport())
    await collector.collect(result.publish_record_id, PollSchedule.DAY_7)
    outcome = collector.get_outcome(result.publish_record_id)
    result.outcome_label = outcome.value
    result.steps_completed.append("analytics")

    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Auto-Affi pipeline once")
    src = parser.add_mutually_exclusive_group()
    src.add_argument(
        "--product-id",
        type=int,
        help="Synthesize a Beauty stub product with this id (legacy path)",
    )
    src.add_argument(
        "--shopee-url",
        type=str,
        help="Real Shopee TH URL (i.<shop>.<item>); resolves via fixture",
    )
    src.add_argument(
        "--fixture",
        type=Path,
        help="Explicit ShopeeProduct fixture JSON (with optional niche_hints)",
    )
    args = parser.parse_args()

    result = asyncio.run(
        run_once(
            product_id=args.product_id,
            shopee_url=args.shopee_url,
            fixture_path=args.fixture,
        )
    )

    print(f"\n{'='*60}")
    print("Auto-Affi run_once complete")
    print(f"{'='*60}")
    print(f"Product ID: {result.product_id}")
    print(f"Brief ID:   {result.brief_id}")
    print(f"Storyboard: {result.storyboard_id}")
    print(f"Safety:     {'PASS' if result.safety_passed else 'FAIL'}")
    print(f"Published:  {result.publish_record_id}")
    print(f"Outcome:    {result.outcome_label}")
    print(f"Steps:      {' -> '.join(result.steps_completed)}")
    print(f"Success:    {result.success}")
    if result.errors:
        print(f"Errors:     {result.errors}")
    print(f"{'='*60}")

    sys.exit(0 if result.success else 1)


if __name__ == "__main__":
    main()
