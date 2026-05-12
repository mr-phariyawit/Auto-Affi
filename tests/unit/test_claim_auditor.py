"""Tests for the Thai compliance claim auditor."""

from __future__ import annotations

import pytest

from auto_affi.agents.claim_auditor import ClaimCategory, audit, is_blocked


@pytest.mark.unit
def test_clean_caption_passes() -> None:
    text = "เซรั่มสูตรนี้บำรุงผิวให้ดูสดใส ใช้ทุกเช้าก่อนแต่งหน้า"
    assert audit(text) == []
    assert is_blocked(text) is False


@pytest.mark.unit
@pytest.mark.parametrize(
    ("text", "category"),
    [
        ("รักษาสิวภายใน 7 วัน", ClaimCategory.MEDICAL),
        ("ใช้แล้วหายขาด", ClaimCategory.MEDICAL),
        ("ลดฝ้ากระเห็นผล", ClaimCategory.MEDICAL),
        ("ผิวขาวขึ้นใน 3 วัน", ClaimCategory.WHITENING),
        ("Skin whitening cream ของแท้", ClaimCategory.WHITENING),
        ("รับประกันผลตอบแทน 10%", ClaimCategory.FINANCIAL),
        ("รวยเร็วภายใน 30 วัน", ClaimCategory.FINANCIAL),
        ("ได้ผลแน่นอน ทุกคน", ClaimCategory.GUARANTEE),
        ("100% ปลอดภัย", ClaimCategory.GUARANTEE),
        ("คืนเงินเต็มจำนวน ถ้าไม่พอใจ", ClaimCategory.GUARANTEE),
    ],
)
def test_violation_categories_detected(text: str, category: ClaimCategory) -> None:
    hits = audit(text)
    assert hits, text
    assert any(hit.category is category for hit in hits)


@pytest.mark.unit
def test_violations_sorted_by_position() -> None:
    text = "100% ปลอดภัย รับประกันผลตอบแทน ทุกคน"
    hits = audit(text)
    spans = [hit.span[0] for hit in hits]
    assert spans == sorted(spans)


@pytest.mark.unit
def test_is_blocked_uses_min_severity() -> None:
    text = "ผลิตภัณฑ์นี้ปลอดภัย 100%"
    # severity-2 hit: should block at default threshold
    assert is_blocked(text) is True
    # raise threshold past hit severity: should pass
    assert is_blocked(text, min_severity=3) is False


@pytest.mark.unit
def test_matched_text_preserved() -> None:
    text = "ใช้แล้วผิวขาวขึ้นทันที"
    hits = audit(text)
    assert hits
    assert any("ผิวขาวขึ้น" in hit.matched_text for hit in hits)


@pytest.mark.unit
def test_no_false_positive_on_neutral_skin_words() -> None:
    text = "ผิวของลูกค้าทุกคนแตกต่างกัน ควรลองทาที่ท้องแขนก่อน"
    assert audit(text) == []
