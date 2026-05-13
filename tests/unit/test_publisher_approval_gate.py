"""Unit tests for HumanApprovalGatePublisher (QW-7, ADR-008 MANUAL mode).

Verifies that the approval gate:
- Blocks publish calls without prior approval
- Allows publish after explicit approval
- Consumes approval after use (one-shot)
- Passes through when requires_human_approval=False
- Supports revoke
"""

from __future__ import annotations

import pytest

from auto_affi.adapters.publisher import (
    DryRunPublisher,
    HumanApprovalGatePublisher,
    PublishNotApprovedError,
    PublishPlatform,
)


@pytest.fixture
def dry_publisher() -> DryRunPublisher:
    return DryRunPublisher(PublishPlatform.IG)


@pytest.fixture
def gated_publisher(dry_publisher: DryRunPublisher) -> HumanApprovalGatePublisher:
    return HumanApprovalGatePublisher(dry_publisher, requires_human_approval=True)


VIDEO_URL = "https://storage.example.com/video-001.mp4"
CAPTION = "Best product #Ad"
LINK = "https://shopee.co.th/product/123/456?subId=test"


class TestApprovalGateBlocking:
    """Gate blocks unapproved publishes."""

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_publish_without_approval_raises(
        self, gated_publisher: HumanApprovalGatePublisher
    ) -> None:
        with pytest.raises(PublishNotApprovedError, match="human approval required"):
            await gated_publisher.publish(
                video_url=VIDEO_URL, caption=CAPTION, affiliate_link=LINK
            )

    @pytest.mark.unit
    def test_is_approved_returns_false_initially(
        self, gated_publisher: HumanApprovalGatePublisher
    ) -> None:
        assert gated_publisher.is_approved(VIDEO_URL) is False

    @pytest.mark.unit
    def test_requires_human_approval_flag(
        self, gated_publisher: HumanApprovalGatePublisher
    ) -> None:
        assert gated_publisher.requires_human_approval is True


class TestApprovalGateApproved:
    """Gate allows approved publishes."""

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_publish_after_approval_succeeds(
        self, gated_publisher: HumanApprovalGatePublisher
    ) -> None:
        gated_publisher.approve(video_url=VIDEO_URL, approved_by="board")
        result = await gated_publisher.publish(
            video_url=VIDEO_URL, caption=CAPTION, affiliate_link=LINK
        )
        assert result.ok is True
        assert result.data is not None
        assert result.data.platform == PublishPlatform.IG

    @pytest.mark.unit
    def test_is_approved_returns_true_after_approve(
        self, gated_publisher: HumanApprovalGatePublisher
    ) -> None:
        gated_publisher.approve(video_url=VIDEO_URL, approved_by="board")
        assert gated_publisher.is_approved(VIDEO_URL) is True

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_approval_consumed_after_publish(
        self, gated_publisher: HumanApprovalGatePublisher
    ) -> None:
        """Approval is one-shot: consumed after first successful publish."""
        gated_publisher.approve(video_url=VIDEO_URL, approved_by="board")
        await gated_publisher.publish(
            video_url=VIDEO_URL, caption=CAPTION, affiliate_link=LINK
        )
        # Second publish should fail — approval was consumed
        with pytest.raises(PublishNotApprovedError):
            await gated_publisher.publish(
                video_url=VIDEO_URL, caption=CAPTION, affiliate_link=LINK
            )


class TestApprovalGateRevoke:
    """Gate supports revoking approvals."""

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_revoke_blocks_publish(
        self, gated_publisher: HumanApprovalGatePublisher
    ) -> None:
        gated_publisher.approve(video_url=VIDEO_URL, approved_by="board")
        gated_publisher.revoke(video_url=VIDEO_URL)
        with pytest.raises(PublishNotApprovedError):
            await gated_publisher.publish(
                video_url=VIDEO_URL, caption=CAPTION, affiliate_link=LINK
            )

    @pytest.mark.unit
    def test_revoke_nonexistent_is_noop(
        self, gated_publisher: HumanApprovalGatePublisher
    ) -> None:
        # Should not raise
        gated_publisher.revoke(video_url="https://no-such-url.mp4")


class TestApprovalGateDisabled:
    """Gate passes through when disabled."""

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_publish_without_approval_when_disabled(
        self, dry_publisher: DryRunPublisher
    ) -> None:
        gated = HumanApprovalGatePublisher(
            dry_publisher, requires_human_approval=False
        )
        result = await gated.publish(
            video_url=VIDEO_URL, caption=CAPTION, affiliate_link=LINK
        )
        assert result.ok is True

    @pytest.mark.unit
    def test_is_approved_always_true_when_disabled(
        self, dry_publisher: DryRunPublisher
    ) -> None:
        gated = HumanApprovalGatePublisher(
            dry_publisher, requires_human_approval=False
        )
        assert gated.is_approved(VIDEO_URL) is True


class TestApprovalGatePlatformPassthrough:
    """Gate correctly passes through platform from inner publisher."""

    @pytest.mark.unit
    def test_platform_from_inner(
        self, gated_publisher: HumanApprovalGatePublisher
    ) -> None:
        assert gated_publisher.platform == PublishPlatform.IG

    @pytest.mark.unit
    def test_platform_fb(self) -> None:
        inner = DryRunPublisher(PublishPlatform.FB)
        gated = HumanApprovalGatePublisher(inner)
        assert gated.platform == PublishPlatform.FB
