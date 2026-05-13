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
import sys
from dataclasses import dataclass, field

from auto_affi.adapters.publisher import DryRunPublisher
from auto_affi.adapters.shopee import ShopeeProduct
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
    """Create a stub campaign brief."""
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


async def run_once(product_id: int) -> RunOnceResult:
    """Execute the full pipeline once with stub/dry-run transports."""
    result = RunOnceResult(product_id=product_id)

    # Step 1: Scout (stub)
    product = _stub_product(product_id)
    result.steps_completed.append("scout")

    # Step 2: Strategist (stub brief)
    brief = _stub_brief(product)
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
    parser.add_argument(
        "--product-id",
        type=int,
        default=12345,
        help="Shopee product ID (stub in Phase 1)",
    )
    args = parser.parse_args()

    result = asyncio.run(run_once(args.product_id))

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
