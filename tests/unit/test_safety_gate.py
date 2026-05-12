"""Unit tests for the pre-publish safety gate (FR-SF-01)."""

from __future__ import annotations

import pytest

from auto_affi.agents.safety_gate import (
    DEFAULT_BRAND_BLOCKLIST,
    SafetyCheckName,
    SafetyGateConfig,
    check_brand_blocklist,
    check_claims,
    check_nsfw,
    safety_gate,
)


# ------------------------------------------------------------------ #
# claim_audit check                                                   #
# ------------------------------------------------------------------ #


@pytest.mark.unit
def test_clean_thai_text_passes_claim_check() -> None:
    result = check_claims("เซรั่มบำรุงผิว สารสกัดจากธรรมชาติ")
    assert result.passed is True
    assert result.check == SafetyCheckName.CLAIM_AUDIT


@pytest.mark.unit
def test_medical_claim_fails_claim_check() -> None:
    result = check_claims("รักษาสิวภายใน 7 วัน")
    assert result.passed is False
    assert len(result.violations) > 0
    assert "medical" in result.violations[0].lower() or "claim" in result.violations[0].lower()


@pytest.mark.unit
def test_claim_check_respects_min_severity() -> None:
    # "100%" is severity 2
    text = "ผลิตภัณฑ์นี้ปลอดภัย 100%"
    # At min_severity=2 it should block
    result_block = check_claims(text, min_severity=2)
    assert result_block.passed is False

    # At min_severity=3 it should pass
    result_pass = check_claims(text, min_severity=3)
    assert result_pass.passed is True


# ------------------------------------------------------------------ #
# brand_blocklist check                                               #
# ------------------------------------------------------------------ #


@pytest.mark.unit
def test_no_brand_mention_passes() -> None:
    result = check_brand_blocklist(
        "เซรั่มยี่ห้อไทย ดีมาก",
        product_name="Thai Serum Plus",
    )
    assert result.passed is True


@pytest.mark.unit
def test_blocked_brand_in_text_fails() -> None:
    result = check_brand_blocklist(
        "ครีมคล้าย Chanel แต่ราคาถูกกว่า",
        product_name="Generic Cream",
    )
    assert result.passed is False
    assert any("chanel" in v.lower() for v in result.violations)


@pytest.mark.unit
def test_blocked_brand_in_product_name_fails() -> None:
    result = check_brand_blocklist(
        "ครีมบำรุงผิวดีมาก",
        product_name="Louis Vuitton Inspired Case",
    )
    assert result.passed is False
    assert any("louis vuitton" in v.lower() for v in result.violations)


@pytest.mark.unit
def test_custom_blocklist() -> None:
    custom = frozenset({"mybrand"})
    result = check_brand_blocklist(
        "MyBrand is great",
        blocklist=custom,
    )
    assert result.passed is False


# ------------------------------------------------------------------ #
# nsfw check                                                          #
# ------------------------------------------------------------------ #


@pytest.mark.unit
def test_nsfw_disabled_always_passes() -> None:
    result = check_nsfw(enabled=False)
    assert result.passed is True
    assert result.check == SafetyCheckName.NSFW_CHECK


@pytest.mark.unit
def test_nsfw_enabled_passes_placeholder() -> None:
    # Phase 1 placeholder — always passes even when enabled
    result = check_nsfw(enabled=True)
    assert result.passed is True


# ------------------------------------------------------------------ #
# composed safety_gate                                                #
# ------------------------------------------------------------------ #


@pytest.mark.unit
def test_clean_content_passes_full_gate() -> None:
    verdict = safety_gate(
        script_text_th="เซรั่มบำรุงผิว สูตรอ่อนโยน ใช้ได้ทุกวัน",
        product_name="Thai Beauty Serum",
    )
    assert verdict.passed is True
    assert len(verdict.checks) == 3
    assert verdict.block_reason is None
    assert len(verdict.failed_checks) == 0


@pytest.mark.unit
def test_medical_claim_blocks_gate() -> None:
    verdict = safety_gate(
        script_text_th="รักษาสิวหายขาดภายใน 3 วัน",
        product_name="Acne Cure",
    )
    assert verdict.passed is False
    assert verdict.block_reason is not None
    assert any(c.check == SafetyCheckName.CLAIM_AUDIT for c in verdict.failed_checks)


@pytest.mark.unit
def test_brand_mention_blocks_gate() -> None:
    verdict = safety_gate(
        script_text_th="ผลิตภัณฑ์คุณภาพดี ราคาไม่แพง",
        product_name="Gucci Style Bag",
    )
    assert verdict.passed is False
    assert any(c.check == SafetyCheckName.BRAND_BLOCKLIST for c in verdict.failed_checks)


@pytest.mark.unit
def test_multiple_failures_all_reported() -> None:
    verdict = safety_gate(
        script_text_th="รักษาสิวหายขาด Chanel style",
        product_name="Luxury Cream",
    )
    assert verdict.passed is False
    # Both claim and brand should fail
    failed_names = {c.check for c in verdict.failed_checks}
    assert SafetyCheckName.CLAIM_AUDIT in failed_names
    assert SafetyCheckName.BRAND_BLOCKLIST in failed_names


@pytest.mark.unit
def test_custom_config_raises_severity_threshold() -> None:
    # "100%" is severity 2 — with min_severity=3, it should pass
    config = SafetyGateConfig(claim_min_severity=3)
    verdict = safety_gate(
        script_text_th="ผลิตภัณฑ์นี้ปลอดภัย 100%",
        product_name="Safe Product",
        config=config,
    )
    assert verdict.passed is True
