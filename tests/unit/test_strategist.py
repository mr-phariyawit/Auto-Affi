"""Unit tests for the Strategist agent."""

from __future__ import annotations

from datetime import date

import pytest

from auto_affi.agents.strategist import is_mega_sale_window, _extract_json


@pytest.mark.unit
@pytest.mark.parametrize(
    ("today", "expected"),
    [
        # 10 days before 6.6 → inside window
        (date(2026, 5, 27), True),
        # 14 days before 6.6 → exactly at boundary
        (date(2026, 5, 23), True),
        # Day of 6.6 → inside window (delta=0)
        (date(2026, 6, 6), True),
        # 15 days before 6.6 → outside
        (date(2026, 5, 22), False),
        # 1 day after 6.6 → outside (we only look forward)
        (date(2026, 6, 7), False),
        # 10 days before 11.11
        (date(2026, 11, 1), True),
        # No mega-sale nearby (mid-July)
        (date(2026, 7, 15), False),
        # 3 days before 3.3
        (date(2026, 2, 28), True),
    ],
)
def test_mega_sale_window(today: date, expected: bool) -> None:
    assert is_mega_sale_window(today=today) is expected


@pytest.mark.unit
def test_extract_json_plain() -> None:
    text = '{"angle": "test", "hook_template_slug": "pov_self_identification"}'
    result = _extract_json(text)
    assert result["angle"] == "test"


@pytest.mark.unit
def test_extract_json_with_markdown_fence() -> None:
    text = '```json\n{"angle": "test"}\n```'
    result = _extract_json(text)
    assert result["angle"] == "test"


@pytest.mark.unit
def test_extract_json_with_plain_fence() -> None:
    text = '```\n{"angle": "test"}\n```'
    result = _extract_json(text)
    assert result["angle"] == "test"


@pytest.mark.unit
def test_extract_json_raises_on_invalid() -> None:
    with pytest.raises(Exception):
        _extract_json("not json at all")


@pytest.mark.unit
def test_extract_json_raises_on_array() -> None:
    with pytest.raises(TypeError, match="Expected JSON object"):
        _extract_json('[1, 2, 3]')
