"""Tests for claim_auditor and safety_gate — adapted from 5602e53.

All tests are pure (no I/O, no ffmpeg). Covers:
  - audit() returns violations in reading order
  - is_blocked() convenience wrapper
  - has_disclosure() detection
  - safety_gate() orchestration (claim check, brand blocklist, NSFW)
  - Thai ห้าม-claims: กันน้ำ100%, กันลื่น100%, รับประกัน
  - Clean text passes
"""

from __future__ import annotations

import pytest

from auto_affi.agents.claim_auditor import (
    ClaimCategory,
    ClaimViolation,
    audit,
    has_disclosure,
    is_blocked,
)
from auto_affi.agents.safety_gate import (
    CheckResult,
    SafetyGateConfig,
    SafetyVerdict,
    check_brand_blocklist,
    check_claims,
    check_nsfw,
    safety_gate,
)

# ---------------------------------------------------------------------------
# audit() — violation detection
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_audit_clean_text_returns_empty() -> None:
    clean = "รองเท้ากันน้ำ สวมใส่สบาย คุ้มค่า ราคาถูก"
    # "กันน้ำ" alone (no 100%) is fine
    violations = audit(clean)
    assert violations == []


@pytest.mark.unit
def test_audit_waterproof_100pct_blocked() -> None:
    text = "กันน้ำ100% ดีมาก"
    violations = audit(text)
    cats = [v.category for v in violations]
    assert ClaimCategory.WATERPROOF in cats


@pytest.mark.unit
def test_audit_antislip_100pct_blocked() -> None:
    text = "กันลื่น100% ปลอดภัย"
    violations = audit(text)
    cats = [v.category for v in violations]
    assert ClaimCategory.SLIP in cats


@pytest.mark.unit
def test_audit_blanket_guarantee_blocked() -> None:
    text = "สินค้ารับประกันคุณภาพ"
    violations = audit(text)
    cats = [v.category for v in violations]
    assert ClaimCategory.GUARANTEE in cats


@pytest.mark.unit
def test_audit_medical_claim_blocked() -> None:
    text = "รักษาสิวหายภายใน 7 วัน"
    violations = audit(text)
    cats = [v.category for v in violations]
    assert ClaimCategory.MEDICAL in cats


@pytest.mark.unit
def test_audit_whitening_blocked() -> None:
    text = "ทำให้ผิวขาวขึ้นทันที"
    violations = audit(text)
    cats = [v.category for v in violations]
    assert ClaimCategory.WHITENING in cats


@pytest.mark.unit
def test_audit_financial_guarantee_blocked() -> None:
    text = "รับประกันผลตอบแทน 100% แน่นอน"
    violations = audit(text)
    cats = [v.category for v in violations]
    assert ClaimCategory.FINANCIAL in cats
    assert ClaimCategory.GUARANTEE in cats


@pytest.mark.unit
def test_audit_violations_in_reading_order() -> None:
    """violations must be sorted by span[0] (reading order)."""
    text = "ผิวขาวขึ้น และ กันน้ำ100%"
    violations = audit(text)
    spans = [v.span[0] for v in violations]
    assert spans == sorted(spans), f"violations not in reading order: {spans}"


@pytest.mark.unit
def test_audit_returns_claimviolation_instances() -> None:
    text = "กันน้ำ100%"
    violations = audit(text)
    for v in violations:
        assert isinstance(v, ClaimViolation)
        assert 1 <= v.severity <= 3
        assert len(v.matched_text) >= 1


@pytest.mark.unit
def test_audit_absolute_percent_severity() -> None:
    text = "100%"
    violations = audit(text)
    # absolute_percent pattern severity=2
    assert any(v.severity >= 2 for v in violations)


# ---------------------------------------------------------------------------
# is_blocked() convenience wrapper
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_is_blocked_true_for_forbidden_claim() -> None:
    assert is_blocked("กันน้ำ100% สุดยอด") is True


@pytest.mark.unit
def test_is_blocked_false_for_clean_text() -> None:
    assert is_blocked("รองเท้าคุณภาพดี ราคาสมเหตุสมผล") is False


@pytest.mark.unit
def test_is_blocked_respects_min_severity() -> None:
    # severity=1 claims should not block at default min_severity=2
    # we test with min_severity=4 (above max) — nothing blocks
    assert is_blocked("กันน้ำ100%", min_severity=4) is False


# ---------------------------------------------------------------------------
# has_disclosure()
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_has_disclosure_finds_thai_marker() -> None:
    assert has_disclosure("สินค้าโฆษณา ซื้อได้เลย") is True


@pytest.mark.unit
def test_has_disclosure_finds_english_marker() -> None:
    assert has_disclosure("Great product #ad") is True
    assert has_disclosure("This is a sponsored post") is True
    assert has_disclosure("affiliate link below") is True


@pytest.mark.unit
def test_has_disclosure_false_for_no_marker() -> None:
    assert has_disclosure("สินค้าดี ราคาดี") is False


# ---------------------------------------------------------------------------
# check_claims() (safety_gate wrapper)
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_check_claims_passes_clean_text() -> None:
    result = check_claims("สินค้าดีมาก ราคาถูก")
    assert result.passed is True
    assert result.violations == []


@pytest.mark.unit
def test_check_claims_fails_forbidden_claim() -> None:
    result = check_claims("กันน้ำ100% ทุกสภาพอากาศ")
    assert result.passed is False
    assert len(result.violations) >= 1


@pytest.mark.unit
def test_check_claims_severity_threshold() -> None:
    # severity=2 absolute_percent at min_severity=3 should NOT block
    result = check_claims("100% ดี", min_severity=3)
    # absolute_percent is severity=2 — should pass at threshold 3
    assert result.passed is True


# ---------------------------------------------------------------------------
# check_brand_blocklist()
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_brand_blocklist_blocks_chanel() -> None:
    result = check_brand_blocklist("ซื้อ chanel มาลอง", product_name="")
    assert result.passed is False
    assert any("chanel" in v for v in result.violations)


@pytest.mark.unit
def test_brand_blocklist_passes_unknown_brand() -> None:
    result = check_brand_blocklist("รองเท้าคุณภาพดี", product_name="Shoe Brand XYZ")
    assert result.passed is True


@pytest.mark.unit
def test_brand_blocklist_matches_product_name() -> None:
    result = check_brand_blocklist("สินค้าดี", product_name="Apple Watch Series 10")
    assert result.passed is False


@pytest.mark.unit
def test_brand_blocklist_case_insensitive() -> None:
    result = check_brand_blocklist("GUCCI bag review", product_name="")
    assert result.passed is False


# ---------------------------------------------------------------------------
# check_nsfw()
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_nsfw_disabled_always_passes() -> None:
    result = check_nsfw(enabled=False)
    assert result.passed is True


@pytest.mark.unit
def test_nsfw_enabled_passes_placeholder() -> None:
    result = check_nsfw(enabled=True)
    assert result.passed is True


# ---------------------------------------------------------------------------
# safety_gate() orchestration
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_safety_gate_passes_clean_compliant_text() -> None:
    verdict = safety_gate(
        script_text_th="รองเท้ากันน้ำ สวมใส่สบาย ใส่ทำงานได้ทั้งวัน ราคาดี",
        product_name="XYZ Shoe",
    )
    assert verdict.passed is True
    assert verdict.block_reason is None


@pytest.mark.unit
def test_safety_gate_blocks_forbidden_claim() -> None:
    verdict = safety_gate(
        script_text_th="กันน้ำ100% ดีที่สุด",
        product_name="Shoe",
    )
    assert verdict.passed is False
    assert verdict.block_reason is not None


@pytest.mark.unit
def test_safety_gate_blocks_blocked_brand() -> None:
    verdict = safety_gate(
        script_text_th="ลองใส่ gucci รองเท้าแบบนี้",
        product_name="",
    )
    assert verdict.passed is False


@pytest.mark.unit
def test_safety_gate_returns_safety_verdict_instance() -> None:
    verdict = safety_gate(script_text_th="ดี", product_name="")
    assert isinstance(verdict, SafetyVerdict)


@pytest.mark.unit
def test_safety_gate_failed_checks_property() -> None:
    verdict = safety_gate(
        script_text_th="กันน้ำ100%",
        product_name="",
    )
    assert len(verdict.failed_checks) >= 1
    for fc in verdict.failed_checks:
        assert isinstance(fc, CheckResult)
        assert fc.passed is False


@pytest.mark.unit
def test_safety_gate_config_custom_blocklist() -> None:
    cfg = SafetyGateConfig(brand_blocklist=frozenset({"nike"}))
    verdict = safety_gate(
        script_text_th="สินค้า nike ดีมาก",
        product_name="",
        config=cfg,
    )
    assert verdict.passed is False


@pytest.mark.unit
def test_safety_gate_all_checks_present() -> None:
    verdict = safety_gate(script_text_th="ดี", product_name="")
    check_names = [c.check for c in verdict.checks]
    assert "claim_audit" in check_names
    assert "brand_blocklist" in check_names
    assert "nsfw_check" in check_names
