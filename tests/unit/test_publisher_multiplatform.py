"""Tests for FB Reels + YT Shorts publisher production paths (AFFI-T-048, T-049)."""

from __future__ import annotations

import pytest

from auto_affi.adapters.publisher import (
    FBReelsPublisher,
    PublishPlatform,
    YTShortsPublisher,
)


class TestFBReelsPublisher:
    """FB Reels publisher (dry-run mode for Phase 1)."""

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_publish_dry_run(self) -> None:
        pub = FBReelsPublisher()
        result = await pub.publish(
            video_url="https://example.com/v.mp4",
            caption="test caption",
            affiliate_link="https://shp.ee/test",
        )
        assert result.ok
        assert result.data is not None
        assert result.data.platform == PublishPlatform.FB

    @pytest.mark.unit
    def test_platform_is_fb(self) -> None:
        pub = FBReelsPublisher()
        assert pub.platform == PublishPlatform.FB

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_multiple_publishes(self) -> None:
        pub = FBReelsPublisher()
        r1 = await pub.publish(video_url="v1", caption="c1", affiliate_link="l1")
        r2 = await pub.publish(video_url="v2", caption="c2", affiliate_link="l2")
        assert r1.ok and r2.ok
        assert r1.data.platform_post_id != r2.data.platform_post_id


class TestYTShortsPublisher:
    """YT Shorts publisher (dry-run mode for Phase 1)."""

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_publish_dry_run(self) -> None:
        pub = YTShortsPublisher()
        result = await pub.publish(
            video_url="https://example.com/v.mp4",
            caption="test caption",
            affiliate_link="https://shp.ee/test",
        )
        assert result.ok
        assert result.data is not None
        assert result.data.platform == PublishPlatform.YT

    @pytest.mark.unit
    def test_platform_is_yt(self) -> None:
        pub = YTShortsPublisher()
        assert pub.platform == PublishPlatform.YT

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_yt_no_credentials_uses_dry_run(self) -> None:
        pub = YTShortsPublisher()
        result = await pub.publish(
            video_url="v.mp4", caption="test", affiliate_link="link",
        )
        assert result.ok
        assert "dry-run" in result.data.platform_post_id

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_yt_with_credentials_still_works(self) -> None:
        """Even with credentials, Phase 1 uses dry-run path."""
        pub = YTShortsPublisher(api_key="key", refresh_token="token")
        result = await pub.publish(
            video_url="v.mp4", caption="test", affiliate_link="link",
        )
        assert result.ok
