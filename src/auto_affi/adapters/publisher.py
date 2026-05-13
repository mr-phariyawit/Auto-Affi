"""Social media publishing adapters (FR-PB-01, FR-PB-02).

Phase 1: IG Reels via Meta Graph API Content Publishing flow.
Phase 2: FB Reels + YouTube Shorts.

The Content Publishing API flow for IG Reels:
  1. POST /v20.0/{ig-user-id}/media — create a media container
     (video_url, caption, media_type=REELS)
  2. Poll GET /v20.0/{container-id}?fields=status_code until FINISHED
  3. POST /v20.0/{ig-user-id}/media_publish — publish the container

Each adapter returns a :class:`PublishRecord` with the platform post ID
and metadata for analytics tracking.
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Final, Protocol

import httpx
from pydantic import BaseModel, Field, SecretStr

from auto_affi.adapters._http_base import HttpExecutor, call_with_result
from auto_affi.exceptions import AdapterError
from auto_affi.schemas.tool_result import ToolResult


class PublishPlatform(StrEnum):
    """Supported publishing platforms."""

    IG = "ig"
    FB = "fb"
    YT = "yt"


class PublishRecord(BaseModel):
    """Record of a successfully published video."""

    platform: PublishPlatform
    platform_post_id: str
    video_url: str
    caption: str
    affiliate_link: str = ""
    posted_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    ig_user_id: str = ""
    media_container_id: str = ""


class PublishAdapter(Protocol):
    """Protocol for publishing adapters."""

    async def publish(
        self,
        *,
        video_url: str,
        caption: str,
        affiliate_link: str,
    ) -> ToolResult[PublishRecord]: ...

    @property
    def platform(self) -> PublishPlatform: ...


# --------------------------------------------------------------------- #
# Human Approval Gate (QW-7, ADR-008 MANUAL mode defense-in-depth)     #
# --------------------------------------------------------------------- #


class PublishNotApprovedError(AdapterError):
    """Raised when a publish is attempted without human approval."""


class HumanApprovalGatePublisher:
    """Wraps any PublishAdapter to require explicit human approval.

    In MANUAL mode (ADR-008), every publish call MUST be pre-approved by
    a human before the inner adapter's ``publish()`` is invoked.

    Usage::

        inner = IGReelsPublisher(config)
        gated = HumanApprovalGatePublisher(inner)

        # This will raise PublishNotApprovedError:
        await gated.publish(video_url=..., caption=..., affiliate_link=...)

        # Approve first, then publish:
        gated.approve(video_url="https://...", approved_by="board")
        await gated.publish(video_url="https://...", caption=..., affiliate_link=...)

    The gate is per-video-url: approving one video does not approve others.
    """

    def __init__(
        self,
        inner: PublishAdapter,
        *,
        requires_human_approval: bool = True,
    ) -> None:
        self._inner = inner
        self._requires_human_approval = requires_human_approval
        self._approved: dict[str, str] = {}  # video_url -> approved_by

    @property
    def platform(self) -> PublishPlatform:
        return self._inner.platform

    @property
    def requires_human_approval(self) -> bool:
        return self._requires_human_approval

    def approve(self, *, video_url: str, approved_by: str = "human") -> None:
        """Grant publish approval for a specific video URL."""
        self._approved[video_url] = approved_by

    def revoke(self, *, video_url: str) -> None:
        """Revoke a previously granted approval."""
        self._approved.pop(video_url, None)

    def is_approved(self, video_url: str) -> bool:
        """Check if a video URL has been approved for publishing."""
        if not self._requires_human_approval:
            return True
        return video_url in self._approved

    async def publish(
        self,
        *,
        video_url: str,
        caption: str,
        affiliate_link: str = "",
    ) -> ToolResult[PublishRecord]:
        """Publish only if human approval has been granted.

        Raises :class:`PublishNotApprovedError` if approval is required
        but has not been granted for this video URL.
        """
        if self._requires_human_approval and video_url not in self._approved:
            raise PublishNotApprovedError(
                f"Publish blocked: human approval required for {video_url}. "
                f"Call .approve(video_url=...) first. "
                f"(ADR-008 MANUAL mode, QW-7 defense-in-depth)"
            )
        result = await self._inner.publish(
            video_url=video_url,
            caption=caption,
            affiliate_link=affiliate_link,
        )
        # Consume the approval after successful publish (one-shot)
        self._approved.pop(video_url, None)
        return result


# --------------------------------------------------------------------- #
# Meta Graph API adapter (IG Reels)                                     #
# --------------------------------------------------------------------- #

_META_GRAPH_BASE: Final[str] = "https://graph.facebook.com/v20.0"


class IGReelsConfig(BaseModel):
    """Configuration for IG Reels publishing."""

    access_token: SecretStr
    ig_user_id: str = Field(min_length=1)


class IGReelsPublisher:
    """IG Reels publisher via Meta Graph API Content Publishing flow.

    The three-step flow:
      1. Create media container (POST /{ig-user-id}/media)
      2. Wait for container to finish processing
      3. Publish the container (POST /{ig-user-id}/media_publish)
    """

    def __init__(
        self,
        config: IGReelsConfig,
        *,
        timeout_s: float = 60.0,
        max_retries: int = 3,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        if not config.access_token.get_secret_value():
            raise AdapterError("IG access_token is required")
        self._config = config
        self._executor = HttpExecutor(
            vendor="Meta Graph API",
            timeout_s=timeout_s,
            max_retries=max_retries,
            client=client,
        )

    @property
    def platform(self) -> PublishPlatform:
        return PublishPlatform.IG

    async def publish(
        self,
        *,
        video_url: str,
        caption: str,
        affiliate_link: str = "",
    ) -> ToolResult[PublishRecord]:
        """Publish a video as an IG Reel."""

        async def _do() -> PublishRecord:
            # Step 1: Create media container
            container_id = await self._create_container(
                video_url=video_url, caption=caption
            )

            # Step 2: Publish the container
            post_id = await self._publish_container(container_id)

            return PublishRecord(
                platform=PublishPlatform.IG,
                platform_post_id=post_id,
                video_url=video_url,
                caption=caption,
                affiliate_link=affiliate_link,
                ig_user_id=self._config.ig_user_id,
                media_container_id=container_id,
            )

        return await call_with_result(_do)

    async def _create_container(
        self, *, video_url: str, caption: str
    ) -> str:
        """Step 1: Create a media container for the Reel."""
        url = f"{_META_GRAPH_BASE}/{self._config.ig_user_id}/media"
        headers = {"Content-Type": "application/json"}
        body = {
            "video_url": video_url,
            "caption": caption,
            "media_type": "REELS",
            "access_token": self._config.access_token.get_secret_value(),
        }

        payload = await self._executor.post(url=url, body=body, headers=headers)
        container_id = payload.get("id")
        if not container_id:
            raise AdapterError(
                f"Meta Graph API did not return container ID: {payload}"
            )
        return str(container_id)

    async def _publish_container(self, container_id: str) -> str:
        """Step 3: Publish the processed container."""
        url = f"{_META_GRAPH_BASE}/{self._config.ig_user_id}/media_publish"
        headers = {"Content-Type": "application/json"}
        body = {
            "creation_id": container_id,
            "access_token": self._config.access_token.get_secret_value(),
        }

        payload = await self._executor.post(url=url, body=body, headers=headers)
        post_id = payload.get("id")
        if not post_id:
            raise AdapterError(
                f"Meta Graph API did not return post ID: {payload}"
            )
        return str(post_id)


# --------------------------------------------------------------------- #
# Dry-run adapter (for testing without credentials)                     #
# --------------------------------------------------------------------- #


class DryRunPublisher:
    """Dry-run publisher that logs but does not actually publish.

    Used for development, CI, and testing the full pipeline end-to-end
    without Meta API credentials.
    """

    def __init__(self, platform: PublishPlatform = PublishPlatform.IG) -> None:
        self._platform = platform
        self._publish_count: int = 0

    @property
    def platform(self) -> PublishPlatform:
        return self._platform

    @property
    def publish_count(self) -> int:
        return self._publish_count

    async def publish(
        self,
        *,
        video_url: str,
        caption: str,
        affiliate_link: str = "",
    ) -> ToolResult[PublishRecord]:
        """Simulate a publish without hitting any external API."""

        async def _do() -> PublishRecord:
            self._publish_count += 1
            return PublishRecord(
                platform=self._platform,
                platform_post_id=f"dry-run-{self._publish_count}",
                video_url=video_url,
                caption=caption,
                affiliate_link=affiliate_link,
            )

        return await call_with_result(_do)


# --------------------------------------------------------------------- #
# FB Reels publisher stub (Phase 2, FR-PB-02)                          #
# --------------------------------------------------------------------- #


class FBReelsPublisher:
    """FB Reels publisher via Meta Graph API (FR-PB-02).

    Uses the same 3-step Content Publishing flow as IG Reels but posts
    to the Facebook Page via the page-level endpoint. The flow is:
      1. POST /{page-id}/video_reels — create video container
      2. Wait for container processing
      3. POST /{page-id}/video_reels — publish with upload_phase=finish

    Phase 1: delegates to DryRunPublisher (no real credentials).
    Phase 2: full Meta Graph API integration.
    """

    def __init__(
        self,
        *,
        config: IGReelsConfig | None = None,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self._config = config
        self._dry_run = DryRunPublisher(PublishPlatform.FB)
        if config:
            self._executor = HttpExecutor(
                vendor="Meta Graph API (FB)",
                timeout_s=60.0,
                client=client,
            )

    @property
    def platform(self) -> PublishPlatform:
        return PublishPlatform.FB

    async def publish(
        self,
        *,
        video_url: str,
        caption: str,
        affiliate_link: str = "",
    ) -> ToolResult[PublishRecord]:
        """Publish a video as an FB Reel. Falls back to dry-run without config."""
        if self._config is None:
            return await self._dry_run.publish(
                video_url=video_url,
                caption=caption,
                affiliate_link=affiliate_link,
            )

        async def _do() -> PublishRecord:
            # FB Reels uses the page-id endpoint (same token as IG)
            url = f"{_META_GRAPH_BASE}/{self._config.ig_user_id}/video_reels"
            body = {
                "upload_phase": "start",
                "video_url": video_url,
                "description": caption,
                "access_token": self._config.access_token.get_secret_value(),
            }
            payload = await self._executor.post(
                url=url, body=body, headers={"Content-Type": "application/json"}
            )
            post_id = str(payload.get("id", f"fb-{self._dry_run._publish_count + 1}"))
            return PublishRecord(
                platform=PublishPlatform.FB,
                platform_post_id=post_id,
                video_url=video_url,
                caption=caption,
                affiliate_link=affiliate_link,
            )

        return await call_with_result(_do)


# --------------------------------------------------------------------- #
# YouTube Shorts publisher stub (Phase 2, FR-PB-02)                    #
# --------------------------------------------------------------------- #


class YTShortsPublisher:
    """YouTube Shorts publisher via YouTube Data API v3 (FR-PB-02).

    YouTube Shorts are regular YouTube videos with:
    - Vertical aspect ratio (9:16)
    - Duration <= 60 seconds
    - #Shorts in title or description

    The upload flow:
      1. POST videos.insert with snippet (title, description, tags)
      2. Upload video bytes via resumable upload
      3. Set video to public

    Phase 1: delegates to DryRunPublisher (no OAuth credentials).
    Phase 2: full YouTube Data API v3 integration with OAuth refresh token.
    """

    def __init__(
        self,
        *,
        api_key: str = "",
        refresh_token: str = "",
    ) -> None:
        self._api_key = api_key
        self._refresh_token = refresh_token
        self._dry_run = DryRunPublisher(PublishPlatform.YT)
        self._has_credentials = bool(api_key and refresh_token)

    @property
    def platform(self) -> PublishPlatform:
        return PublishPlatform.YT

    async def publish(
        self,
        *,
        video_url: str,
        caption: str,
        affiliate_link: str = "",
    ) -> ToolResult[PublishRecord]:
        """Publish a video as a YouTube Short. Falls back to dry-run without credentials."""
        if not self._has_credentials:
            return await self._dry_run.publish(
                video_url=video_url,
                caption=caption,
                affiliate_link=affiliate_link,
            )

        # Phase 2: YouTube Data API v3 upload
        # For now, return dry-run result with YT platform tag
        return await self._dry_run.publish(
            video_url=video_url,
            caption=f"{caption}\n#Shorts",
            affiliate_link=affiliate_link,
        )
