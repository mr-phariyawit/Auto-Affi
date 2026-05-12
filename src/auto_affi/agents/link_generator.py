"""Affiliate link generator — bridges SubIds taxonomy with publishing (FR-PB-03).

Composes a full 5-slot SubIds instance from publishing context:
  slot[0] = platform (ig, fb, yt, tk)
  slot[1] = account handle
  slot[2] = video_id (campaign-stamped UUID short)
  slot[3] = campaign_id (from CampaignBrief)
  slot[4] = variant (A/B test variant, default A)

Then calls :meth:`ShopeeClient.generate_short_link` to produce a
subId-tagged affiliate deep link for tracking attribution.
"""

from __future__ import annotations

import uuid

from auto_affi.adapters.shopee import ShopeeClient, ShopeeShortLink
from auto_affi.adapters.shopee_subids import Platform, SubIds
from auto_affi.schemas.tool_result import ToolResult


def compose_sub_ids(
    *,
    platform: Platform,
    account_handle: str,
    campaign_id: str,
    variant: str = "A",
    video_id: str | None = None,
) -> SubIds:
    """Build a SubIds instance from publishing context.

    If ``video_id`` is not provided, generates a short UUID.
    """
    vid = video_id or uuid.uuid4().hex[:12]
    return SubIds(
        platform=platform,
        account=account_handle,
        video_id=vid,
        campaign_id=campaign_id,
        variant=variant,
    )


async def generate_affiliate_link(
    client: ShopeeClient,
    *,
    item_id: int,
    shop_id: int,
    platform: Platform,
    account_handle: str,
    campaign_id: str,
    variant: str = "A",
    video_id: str | None = None,
) -> ToolResult[ShopeeShortLink]:
    """Generate a subId-tagged Shopee affiliate deep link.

    This is the single integration point between the SubIds taxonomy
    and the Shopee short-link API. Every published video should call
    this to get a trackable link.
    """
    sub_ids = compose_sub_ids(
        platform=platform,
        account_handle=account_handle,
        campaign_id=campaign_id,
        variant=variant,
        video_id=video_id,
    )
    return await client.generate_short_link(
        item_id=item_id,
        shop_id=shop_id,
        sub_ids=sub_ids,
    )
