"""Tests for multi-niche configuration (AFFI-T-050)."""

from __future__ import annotations

import pytest

from auto_affi.agents.niche_config import (
    Niche,
    NicheConfig,
    get_niche_config,
    NICHE_CONFIGS,
)


class TestNicheConfig:
    """Multi-niche expansion configuration."""

    @pytest.mark.unit
    def test_all_niches_defined(self) -> None:
        for niche in Niche:
            assert niche in NICHE_CONFIGS

    @pytest.mark.unit
    def test_beauty_config(self) -> None:
        cfg = get_niche_config(Niche.BEAUTY)
        assert cfg.niche == Niche.BEAUTY
        assert cfg.display_name_th == "ความงาม"
        assert "beauty_skincare" in cfg.shopee_categories

    @pytest.mark.unit
    def test_electronics_config(self) -> None:
        cfg = get_niche_config(Niche.ELECTRONICS)
        assert cfg.niche == Niche.ELECTRONICS
        assert "cool blue" in cfg.visual_style.color_palette
        assert cfg.demo_duration_hint_s == 3.0

    @pytest.mark.unit
    def test_fashion_config(self) -> None:
        cfg = get_niche_config(Niche.FASHION)
        assert cfg.niche == Niche.FASHION
        assert "full-body" in cfg.visual_style.primary_shot_types

    @pytest.mark.unit
    def test_get_by_string(self) -> None:
        cfg = get_niche_config("electronics")
        assert cfg.niche == Niche.ELECTRONICS

    @pytest.mark.unit
    def test_unknown_niche_falls_back_to_beauty(self) -> None:
        cfg = get_niche_config("unknown_niche")
        assert cfg.niche == Niche.BEAUTY

    @pytest.mark.unit
    def test_commission_ranges_valid(self) -> None:
        for niche, cfg in NICHE_CONFIGS.items():
            lo, hi = cfg.typical_commission_range
            assert 0 < lo < hi <= 1.0, f"{niche}: invalid commission range"

    @pytest.mark.unit
    def test_price_bands_valid(self) -> None:
        for niche, cfg in NICHE_CONFIGS.items():
            lo, hi = cfg.typical_price_band_thb
            assert 0 < lo < hi, f"{niche}: invalid price band"

    @pytest.mark.unit
    def test_each_niche_has_hook_preferences(self) -> None:
        for niche, cfg in NICHE_CONFIGS.items():
            assert len(cfg.hook_preferences) >= 2, f"{niche}: needs at least 2 hook prefs"

    @pytest.mark.unit
    def test_each_niche_has_visual_style(self) -> None:
        for niche, cfg in NICHE_CONFIGS.items():
            assert cfg.visual_style.lighting != ""
            assert cfg.visual_style.color_palette != ""
            assert len(cfg.visual_style.primary_shot_types) >= 2
