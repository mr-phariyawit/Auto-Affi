"""Tests for the run_once CLI entrypoint (AFFI-T-039)."""

from __future__ import annotations

import pytest

from auto_affi.ops.run_once import RunOnceResult, run_once, _stub_product, _stub_brief


class TestRunOnce:
    """End-to-end pipeline run with stubs."""

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_full_pipeline_succeeds(self) -> None:
        result = await run_once(12345)
        assert result.success
        assert len(result.steps_completed) == 6
        assert result.steps_completed == [
            "scout", "strategist", "writers_room",
            "safety_gate", "publisher", "analytics",
        ]

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_brief_id_populated(self) -> None:
        result = await run_once(12345)
        assert result.brief_id != ""

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_storyboard_id_populated(self) -> None:
        result = await run_once(12345)
        assert result.storyboard_id != ""

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_safety_passes(self) -> None:
        result = await run_once(12345)
        assert result.safety_passed is True

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_publish_record_id_populated(self) -> None:
        result = await run_once(12345)
        assert result.publish_record_id != ""

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_outcome_label_populated(self) -> None:
        result = await run_once(12345)
        assert result.outcome_label != ""

    @pytest.mark.unit
    def test_stub_product(self) -> None:
        product = _stub_product(99999)
        assert product.item_id == 99999
        assert product.name != ""

    @pytest.mark.unit
    def test_stub_brief(self) -> None:
        product = _stub_product(12345)
        brief = _stub_brief(product)
        assert brief.product_id == 12345
        assert brief.persona.label != ""

    @pytest.mark.unit
    def test_run_once_result_success(self) -> None:
        result = RunOnceResult(product_id=1, safety_passed=True)
        assert result.success is True

    @pytest.mark.unit
    def test_run_once_result_failure(self) -> None:
        result = RunOnceResult(
            product_id=1, safety_passed=True, errors=["boom"]
        )
        assert result.success is False
