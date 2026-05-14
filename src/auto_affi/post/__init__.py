"""Post-processing module — overlays, mixing, finalization steps that run
after Seedance/Veo video generation but before the final mp4 ships.

Currently exposes the HyperFrames renderer that turns
``Storyboard.hyperframe_overlays`` entries into ProRes-with-alpha MOVs
ready for ffmpeg compositing.
"""

from auto_affi.post.hyperframes_renderer import (
    HyperframesRendererError,
    OverlayRender,
    render_storyboard_overlays,
)

__all__ = [
    "HyperframesRendererError",
    "OverlayRender",
    "render_storyboard_overlays",
]
