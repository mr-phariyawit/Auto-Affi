"""Multi-niche configuration (Phase 2 expansion).

Parameterizes the Writers' Room, Scout scoring, and Strategist by niche.
Phase 1: Beauty only. Phase 2: Electronics + Fashion.

Each niche defines:
- Visual style preferences (lighting, color palette, shot types)
- Product demo conventions (how to show the product)
- Thai audience language conventions
- Typical commission ranges and price bands
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class Niche(StrEnum):
    """Supported product niches."""

    BEAUTY = "beauty"
    ELECTRONICS = "electronics"
    FASHION = "fashion"


@dataclass(frozen=True)
class NicheVisualStyle:
    """Visual conventions for a niche."""

    lighting: str
    color_palette: str
    primary_shot_types: list[str]
    demo_convention: str


@dataclass(frozen=True)
class NicheConfig:
    """Complete configuration for a product niche."""

    niche: Niche
    display_name_th: str
    display_name_en: str
    visual_style: NicheVisualStyle
    typical_commission_range: tuple[float, float]  # e.g. (0.05, 0.15)
    typical_price_band_thb: tuple[int, int]  # e.g. (200, 2000)
    shopee_categories: list[str]
    hook_preferences: list[str]  # preferred hook template slugs
    cta_style: str
    demo_duration_hint_s: float = 2.5  # typical demo scene duration


# ------------------------------------------------------------------ #
# Niche registry                                                       #
# ------------------------------------------------------------------ #

NICHE_CONFIGS: dict[Niche, NicheConfig] = {
    Niche.BEAUTY: NicheConfig(
        niche=Niche.BEAUTY,
        display_name_th="ความงาม",
        display_name_en="Beauty & Skincare",
        visual_style=NicheVisualStyle(
            lighting="soft studio, golden hour, ring light",
            color_palette="warm amber, pink glow, clean white",
            primary_shot_types=["extreme-closeup", "medium-shot", "overhead"],
            demo_convention=(
                "Show product texture, application on skin, before/after comparison. "
                "Focus on glow, absorption speed, packaging details."
            ),
        ),
        typical_commission_range=(0.05, 0.15),
        typical_price_band_thb=(200, 2000),
        shopee_categories=["beauty_skincare", "beauty_makeup", "beauty_haircare"],
        hook_preferences=["curiosity_gap", "before_after", "secret_reveal"],
        cta_style="pinned_comment + on_screen_qr",
    ),
    Niche.ELECTRONICS: NicheConfig(
        niche=Niche.ELECTRONICS,
        display_name_th="อิเล็กทรอนิกส์",
        display_name_en="Electronics & Gadgets",
        visual_style=NicheVisualStyle(
            lighting="cool blue LED, clean white studio, dramatic side light",
            color_palette="cool blue, dark slate, neon accent, clean white",
            primary_shot_types=["product-hero", "overhead-flat-lay", "in-use-medium"],
            demo_convention=(
                "Show unboxing, feature highlights with on-screen text callouts, "
                "size comparison with hand/everyday object, screen quality demo."
            ),
        ),
        typical_commission_range=(0.03, 0.08),
        typical_price_band_thb=(500, 15000),
        shopee_categories=["electronics", "mobile_accessories", "computers"],
        hook_preferences=["unboxing_reveal", "comparison", "countdown"],
        cta_style="pinned_comment + end_screen_link",
        demo_duration_hint_s=3.0,
    ),
    Niche.FASHION: NicheConfig(
        niche=Niche.FASHION,
        display_name_th="แฟชั่น",
        display_name_en="Fashion & Apparel",
        visual_style=NicheVisualStyle(
            lighting="natural daylight, street photography, warm golden",
            color_palette="earth tones, pastel, street-style contrast",
            primary_shot_types=["full-body", "medium-shot", "detail-closeup"],
            demo_convention=(
                "Show outfit styling, fabric texture, fit on body, "
                "mix-and-match combinations, street-style context."
            ),
        ),
        typical_commission_range=(0.05, 0.12),
        typical_price_band_thb=(300, 3000),
        shopee_categories=["fashion_women", "fashion_men", "fashion_accessories"],
        hook_preferences=["transformation", "outfit_check", "before_after"],
        cta_style="pinned_comment + swipe_up",
        demo_duration_hint_s=2.0,
    ),
}


def get_niche_config(niche: Niche | str) -> NicheConfig:
    """Get configuration for a niche. Defaults to Beauty if unknown."""
    if isinstance(niche, str):
        try:
            niche = Niche(niche)
        except ValueError:
            return NICHE_CONFIGS[Niche.BEAUTY]
    return NICHE_CONFIGS.get(niche, NICHE_CONFIGS[Niche.BEAUTY])
