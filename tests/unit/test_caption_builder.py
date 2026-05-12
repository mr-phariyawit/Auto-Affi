"""Unit tests for the caption builder with ad disclosure enforcement."""

from __future__ import annotations

import pytest

from auto_affi.agents.caption_builder import (
    Caption,
    CaptionInput,
    DisclosureError,
    Platform,
    build_caption,
    validate_disclosure,
)


def _sample_input(platform: Platform = Platform.IG) -> CaptionInput:
    return CaptionInput(
        platform=platform,
        product_name="เซรั่มบำรุงผิว XYZ",
        hook_text_th="ผิวมันแก้ได้ ลองตัวนี้เลย",
        affiliate_link="https://s.shopee.co.th/abc123",
        hashtags=["skincare", "เซรั่ม", "Shopee"],
        cta_text_th="แตะลิงก์ใต้คลิปเลย",
    )


@pytest.mark.unit
@pytest.mark.parametrize("platform", list(Platform))
def test_all_platforms_produce_valid_caption(platform: Platform) -> None:
    inp = _sample_input(platform)
    caption = build_caption(inp)
    assert caption.platform == platform
    assert caption.has_disclosure is True
    assert len(caption.text) > 0
    assert caption.hashtag_count > 0


@pytest.mark.unit
def test_ig_caption_contains_disclosure() -> None:
    caption = build_caption(_sample_input(Platform.IG))
    assert "#โฆษณา" in caption.text
    assert "affiliate" in caption.text.lower()


@pytest.mark.unit
def test_yt_caption_contains_thai_disclosure() -> None:
    caption = build_caption(_sample_input(Platform.YT))
    assert "ได้รับค่าตอบแทน" in caption.text


@pytest.mark.unit
def test_tk_caption_contains_ad_and_ai_label() -> None:
    caption = build_caption(_sample_input(Platform.TK))
    assert "#โฆษณา" in caption.text
    assert "#AIสร้าง" in caption.text or "#AIGenerated" in caption.text
    assert caption.has_ai_label is True


@pytest.mark.unit
def test_all_platforms_have_ai_label() -> None:
    for platform in Platform:
        caption = build_caption(_sample_input(platform))
        assert caption.has_ai_label is True, f"{platform} missing AI label"


@pytest.mark.unit
def test_caption_contains_affiliate_link() -> None:
    caption = build_caption(_sample_input())
    assert "https://s.shopee.co.th/abc123" in caption.text


@pytest.mark.unit
def test_caption_contains_product_name() -> None:
    caption = build_caption(_sample_input())
    assert "เซรั่มบำรุงผิว XYZ" in caption.text


@pytest.mark.unit
def test_caption_contains_hashtags() -> None:
    caption = build_caption(_sample_input())
    assert "#skincare" in caption.text
    assert "#เซรั่ม" in caption.text
    assert "#Shopee" in caption.text


@pytest.mark.unit
def test_caption_contains_cta() -> None:
    caption = build_caption(_sample_input())
    assert "แตะลิงก์ใต้คลิปเลย" in caption.text


@pytest.mark.unit
def test_empty_hashtags_still_works() -> None:
    inp = CaptionInput(
        platform=Platform.IG,
        product_name="Test Product",
        hook_text_th="Hook text",
        affiliate_link="https://example.com",
        hashtags=[],
    )
    caption = build_caption(inp)
    assert caption.has_disclosure is True
    # Built-in template adds #โฆษณา regardless of user hashtags
    assert "#โฆษณา" in caption.text


@pytest.mark.unit
def test_validate_disclosure_positive() -> None:
    assert validate_disclosure("Check out this product #โฆษณา") is True
    assert validate_disclosure("Paid partnership with brand") is True
    assert validate_disclosure("ได้รับค่าตอบแทนจากลิงก์นี้") is True


@pytest.mark.unit
def test_validate_disclosure_negative() -> None:
    assert validate_disclosure("Just a normal post about skincare") is False
    assert validate_disclosure("ลองใช้เซรั่มตัวนี้ ดีมาก") is False


@pytest.mark.unit
def test_no_triple_newlines_in_output() -> None:
    caption = build_caption(_sample_input())
    assert "\n\n\n" not in caption.text


@pytest.mark.unit
def test_hashtags_with_leading_hash_not_doubled() -> None:
    inp = CaptionInput(
        platform=Platform.IG,
        product_name="Test",
        hook_text_th="Hook",
        affiliate_link="https://example.com",
        hashtags=["#already_hashed", "no_hash"],
    )
    caption = build_caption(inp)
    # Should not produce ##already_hashed
    assert "##" not in caption.text
    assert "#already_hashed" in caption.text
    assert "#no_hash" in caption.text
