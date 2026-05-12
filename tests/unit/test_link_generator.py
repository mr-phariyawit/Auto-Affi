"""Unit tests for affiliate link generator (FR-PB-03 SubId injection)."""

from __future__ import annotations

import pytest

from auto_affi.agents.link_generator import compose_sub_ids
from auto_affi.adapters.shopee_subids import SubIds


@pytest.mark.unit
def test_compose_sub_ids_all_fields() -> None:
    sub_ids = compose_sub_ids(
        platform="ig",
        account_handle="@nattatips",
        campaign_id="camp-001",
        variant="B",
        video_id="vid-abc",
    )
    assert sub_ids.platform == "ig"
    assert sub_ids.account == "@nattatips"
    assert sub_ids.video_id == "vid-abc"
    assert sub_ids.campaign_id == "camp-001"
    assert sub_ids.variant == "B"


@pytest.mark.unit
def test_compose_sub_ids_auto_generates_video_id() -> None:
    sub_ids = compose_sub_ids(
        platform="fb",
        account_handle="@test",
        campaign_id="camp-002",
    )
    assert len(sub_ids.video_id) == 12  # UUID hex[:12]
    assert sub_ids.variant == "A"  # default


@pytest.mark.unit
def test_compose_sub_ids_to_list_order() -> None:
    sub_ids = compose_sub_ids(
        platform="yt",
        account_handle="@channel",
        campaign_id="camp-003",
        variant="C",
        video_id="v123",
    )
    slots = sub_ids.to_list()
    assert slots == ["yt", "@channel", "v123", "camp-003", "C"]
    assert len(slots) == 5


@pytest.mark.unit
def test_compose_sub_ids_roundtrip() -> None:
    original = compose_sub_ids(
        platform="tk",
        account_handle="@tiktok_user",
        campaign_id="camp-rt",
        variant="A",
        video_id="rt-vid",
    )
    from_list = SubIds.from_list(original.to_list())
    assert from_list.platform == original.platform
    assert from_list.account == original.account
    assert from_list.video_id == original.video_id
    assert from_list.campaign_id == original.campaign_id
    assert from_list.variant == original.variant


@pytest.mark.unit
@pytest.mark.parametrize("platform", ["ig", "fb", "yt", "tk"])
def test_compose_sub_ids_all_platforms(platform: str) -> None:
    sub_ids = compose_sub_ids(
        platform=platform,  # type: ignore[arg-type]
        account_handle="@test",
        campaign_id="c",
        video_id="v",
    )
    assert sub_ids.platform == platform
