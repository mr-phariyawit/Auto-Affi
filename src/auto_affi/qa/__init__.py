"""QA module — automated review of generated video output.

Provides a video-review unit that compares produced clips against the
storyboard intent (motion · duration · scene composition) and emits a
structured feedback report used to drive the next iteration.

This is the feedback loop's input side. The output side (auto-regenerate
flagged scenes) is wired by the orchestrator separately.
"""

from auto_affi.qa.video_review import (
    MotionScore,
    SceneReview,
    VideoReviewReport,
    analyze_motion,
    analyze_scene,
    review_video_run,
)

__all__ = [
    "MotionScore",
    "SceneReview",
    "VideoReviewReport",
    "analyze_motion",
    "analyze_scene",
    "review_video_run",
]
