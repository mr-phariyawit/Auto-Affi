"""End-to-end integration test — full pipeline with in-process executor (AFFI-T-042).

Tests the complete chain: Discovery DAG + Campaign DAG using stub
transports and the InProcessExecutor. No live API calls.

This validates that all subsystems wire together correctly:
Scout -> Strategist -> Writers Room -> Safety -> Publisher -> Analytics -> Curator -> Wiki
"""

from __future__ import annotations

import pytest

from auto_affi.adapters.publisher import DryRunPublisher
from auto_affi.adapters.shopee import ShopeeProduct
from auto_affi.agents.analytics_collector import (
    AnalyticsCollector,
    DryRunMetricsTransport,
)
from auto_affi.agents.caption_builder import CaptionInput, Platform, build_caption
from auto_affi.agents.feedback_curator import FeedbackCurator, OutcomeRecord
from auto_affi.agents.safety_gate import safety_gate
from auto_affi.agents.writers_room import WritersRoom
from auto_affi.ops.run_once import run_once
from auto_affi.schemas.campaign_brief import CampaignBrief, CTA, Persona
from auto_affi.schemas.metrics import OutcomeLabel, PollSchedule
from auto_affi.wiki.review_queue import ReviewQueue
from auto_affi.wiki.store import WikiStore, promote_from_queue
from auto_affi.wiki.tier_promoter import TierPromoter
from auto_affi.workflows.budget import BudgetCircuitBreaker, BudgetDecision
from auto_affi.workflows.definitions import build_campaign_workflow
from auto_affi.workflows.executor import InProcessExecutor
from auto_affi.workflows.handlers import (
    build_learning_workflow,
    make_analytics_rollup_handler,
    make_curator_handler,
    make_tier_promotion_handler,
)


class TestFullPipelineE2E:
    """End-to-end pipeline with stub transports."""

    @pytest.mark.asyncio
    async def test_run_once_full_loop(self) -> None:
        """run_once chains all 6 stages successfully."""
        result = await run_once(12345)
        assert result.success
        assert len(result.steps_completed) == 6
        assert result.outcome_label in [
            "breakout", "hit", "neutral", "flop", "banned"
        ]

    @pytest.mark.asyncio
    async def test_writers_room_to_safety_to_publisher(self) -> None:
        """Writers Room output passes Safety and publishes."""
        brief = CampaignBrief(
            product_id=999,
            shop_id=100,
            persona=Persona(
                label="Thai women",
                age_range="18-30",
                pain_points=["oily skin"],
                daily_context="IG Reels user",
            ),
            angle="ควบคุมมันใน 1 ชม",
            hook_template_slug="before_after",
            cta=CTA(text_th="สั่งเลย!", placement="pinned_comment"),
            hypothesis="Before/after for oil control",
            expected_ctr=0.025,
            confidence=0.6,
        )
        room = WritersRoom()
        sb_result = await room.generate_storyboard(brief)
        assert sb_result.ok

        storyboard = sb_result.data
        assert storyboard is not None
        script = " ".join(
            s.dialogue.text_th for s in storyboard.scenes if s.dialogue
        )
        verdict = safety_gate(script_text_th=script, product_name="Oil Control Serum")
        assert verdict.passed

        caption = build_caption(
            CaptionInput(
                platform=Platform.IG,
                product_name="Oil Control Serum",
                hook_text_th="ไม่มันอีกต่อไป!",
                affiliate_link="https://shp.ee/test",
                hashtags=["skincare"],
            )
        )
        publisher = DryRunPublisher()
        pub = await publisher.publish(
            video_url="https://example.com/v.mp4",
            caption=caption.text,
        )
        assert pub.ok

    @pytest.mark.asyncio
    async def test_analytics_to_curator_to_wiki_loop(self) -> None:
        """Metrics -> Outcome -> Curator -> ReviewQueue -> Promote -> WikiStore."""
        # Collect metrics
        collector = AnalyticsCollector(
            transport=DryRunMetricsTransport(base_views=15000, base_ctr=0.03)
        )
        await collector.collect("pub-e2e", PollSchedule.DAY_7)
        outcome = collector.get_outcome("pub-e2e")
        assert outcome is OutcomeLabel.HIT

        # Build outcome records for curator
        outcomes = [
            OutcomeRecord(
                video_id=f"v{i}",
                publish_record_id=f"pub-{i}",
                outcome=OutcomeLabel.HIT,
                views=15000,
                hook_template_slug="curiosity_gap",
            )
            for i in range(5)
        ] + [
            OutcomeRecord(
                video_id=f"f{i}",
                publish_record_id=f"pub-f{i}",
                outcome=OutcomeLabel.FLOP,
                views=100,
                hook_template_slug="talking_head",
            )
            for i in range(5)
        ]

        # Curator extracts patterns
        queue = ReviewQueue()
        curator = FeedbackCurator(review_queue=queue)
        result = await curator.curate(outcomes)
        assert result.ok
        assert len(queue.pending()) >= 1

        # Promote to wiki store
        store = WikiStore()
        promoter = TierPromoter()
        promoted = promote_from_queue(queue, store, promoter)
        assert promoted >= 1
        assert store.entry_count >= 1

    @pytest.mark.asyncio
    async def test_budget_circuit_breaker_integration(self) -> None:
        """Budget breaker correctly blocks when daily cap exceeded."""
        breaker = BudgetCircuitBreaker(daily_cap=5.0)
        breaker.record_spend("video_gen", 4.0)
        breaker.record_spend("tts", 1.0)
        # At $5.0 spent, next $1.0 would be $6.0 > $5.5 (5.0 * 1.1)
        decision = breaker.check_budget("misc", 1.0)
        assert decision is BudgetDecision.DENY

    @pytest.mark.asyncio
    async def test_learning_workflow_e2e(self) -> None:
        """LearningWorkflow executes: rollup -> curator -> tier_promotion."""
        queue = ReviewQueue()
        curator = FeedbackCurator(review_queue=queue)
        promoter = TierPromoter()

        outcomes = [
            OutcomeRecord(
                video_id=f"v{i}",
                publish_record_id=f"p{i}",
                outcome=OutcomeLabel.HIT,
                views=20000,
                hook_template_slug="curiosity_gap",
            )
            for i in range(4)
        ] + [
            OutcomeRecord(
                video_id=f"f{i}",
                publish_record_id=f"pf{i}",
                outcome=OutcomeLabel.FLOP,
                views=50,
                hook_template_slug="talking_head",
            )
            for i in range(4)
        ]

        executor = InProcessExecutor()
        executor.register(
            "analytics_rollup_handler",
            make_analytics_rollup_handler(outcomes),
        )
        executor.register("curator_handler", make_curator_handler(curator))
        executor.register(
            "tier_promotion_handler",
            make_tier_promotion_handler(queue, promoter),
        )

        dag = build_learning_workflow(run_id="e2e-test")
        result = await executor.execute(dag)
        assert result.success
        assert result.steps_completed == 3
