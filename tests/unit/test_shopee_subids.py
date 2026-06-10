"""Unit tests for the SubId taxonomy."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from auto_affi.adapters.shopee_subids import SubIds


@pytest.mark.unit
def test_canonical_order() -> None:
    sub_ids = SubIds(
        platform="tk",
        account="@nattatips",
        video_id="vid-001",
        campaign_id="cmp-42",
        variant="B",
    )
    assert sub_ids.to_list() == ["tk", "@nattatips", "vid-001", "cmp-42", "B"]


@pytest.mark.unit
def test_default_variant_is_a() -> None:
    sub_ids = SubIds(platform="ig", account="acct", video_id="v", campaign_id="c")
    assert sub_ids.variant == "A"


@pytest.mark.unit
def test_round_trip() -> None:
    original = SubIds(
        platform="yt",
        account="ch-beauty",
        video_id="v-77",
        campaign_id="c-9",
        variant="C",
    )
    restored = SubIds.from_list(original.to_list())
    assert restored == original


@pytest.mark.unit
def test_from_list_pads_missing_slots() -> None:
    sub_ids = SubIds.from_list(["fb", "acct", "vid", "cmp"])
    assert sub_ids.variant == "A"


@pytest.mark.unit
def test_pipe_is_reserved() -> None:
    with pytest.raises(ValidationError):
        SubIds(
            platform="tk",
            account="bad|name",
            video_id="v",
            campaign_id="c",
        )


@pytest.mark.unit
def test_platform_constrained() -> None:
    with pytest.raises(ValidationError):
        SubIds(
            platform="tiktok",  # type: ignore[arg-type]
            account="acct",
            video_id="v",
            campaign_id="c",
        )
