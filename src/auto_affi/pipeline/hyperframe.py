"""Hyperframe overlay — brand watermark + CTA motion graphics (E-004 tail).

Generates overlay specifications for compositing onto video scenes.
Phase 1: produces overlay metadata (template + props) that FFmpeg or
Remotion consumes. Phase 2: renders HTML templates to transparent MP4.

Overlays from SPEC 6.2:
- snap_title_v2: bold text pop on hook scene
- cta_pulse: animated CTA on last scene
- brand_watermark: subtle corner logo throughout
- lower_third: product name + price callout
"""

from __future__ import annotations

from dataclasses import dataclass, field

from pydantic import BaseModel, Field

from auto_affi.schemas.storyboard import Storyboard


class OverlaySpec(BaseModel):
    """Rendered overlay specification for compositing."""

    scene_idx: int = Field(ge=0)
    template: str
    props: dict[str, object] = Field(default_factory=dict)
    layer: str = "overlay"  # overlay | watermark | lower_third
    opacity: float = Field(ge=0.0, le=1.0, default=1.0)
    position: str = "center"  # center | top-right | bottom-left | etc.
    duration_s: float = Field(gt=0.0, default=2.0)


# Default brand watermark config
DEFAULT_WATERMARK = OverlaySpec(
    scene_idx=0,  # placeholder — applied to all scenes
    template="brand_watermark",
    props={"logo_url": "assets/brand/auto-affi-logo.png", "size": "48px"},
    layer="watermark",
    opacity=0.3,
    position="top-right",
    duration_s=999.0,  # full video
)


@dataclass
class HyperframeRenderer:
    """Generates overlay specs from a storyboard.

    Phase 1: metadata-only (no actual rendering).
    Phase 2: Remotion/HTML template rendering to transparent MP4.
    """

    brand_watermark: OverlaySpec = field(default_factory=lambda: DEFAULT_WATERMARK)
    _specs: list[OverlaySpec] = field(default_factory=list, init=False)

    def generate_overlays(self, storyboard: Storyboard) -> list[OverlaySpec]:
        """Generate overlay specs for all scenes in a storyboard.

        Includes:
        1. Storyboard-defined hyperframe_overlays
        2. Brand watermark on every scene
        """
        specs: list[OverlaySpec] = []

        # Convert storyboard overlays to OverlaySpec
        for overlay in storyboard.hyperframe_overlays:
            duration = float(overlay.props.get("duration_s", 2.0))
            specs.append(
                OverlaySpec(
                    scene_idx=overlay.scene_idx,
                    template=overlay.template,
                    props=dict(overlay.props),
                    duration_s=duration,
                )
            )

        # Add brand watermark for each scene
        for scene in storyboard.scenes:
            specs.append(
                OverlaySpec(
                    scene_idx=scene.idx,
                    template=self.brand_watermark.template,
                    props=dict(self.brand_watermark.props),
                    layer="watermark",
                    opacity=self.brand_watermark.opacity,
                    position=self.brand_watermark.position,
                    duration_s=scene.duration_s,
                )
            )

        self._specs = specs
        return specs

    @property
    def overlay_count(self) -> int:
        return len(self._specs)
