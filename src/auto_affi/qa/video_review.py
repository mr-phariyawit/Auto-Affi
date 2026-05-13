"""Video review unit — quantifies how close each clip is to the storyboard intent.

Three signals, all derivable from the local clip + the storyboard JSON:

1. **Motion score** — mean absolute pixel-difference between the clip's
   first and last frame. 0 = identical (clip is a still). 1 = totally
   different (clip is animated). Threshold below which we flag STATIC.
2. **Duration mismatch** — actual clip length vs storyboard's
   ``duration_s``. Threshold above which we flag TIMING.
3. **Scene metadata cross-check** — the storyboard specifies a
   ``camera_movement`` like ``slow-dolly-in`` or ``push-in``. If the
   motion score is below a threshold AND the scene wasn't supposed to be
   static (``movement != "static"``), we flag MOTION_INTENT_MISSED.

The reviewer is intentionally LLM-free for now — pure ffmpeg + Pillow.
A vision-LLM tier can stack on top later (it would catch composition
drift and anatomy artifacts that survived into motion). The pure-pixel
motion check is enough to surface the "all clips are stills" failure
mode the human reported on run #4.
"""

from __future__ import annotations

import json
import subprocess
import tempfile
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from PIL import Image


# Threshold tuning — see docstring rationale below
MOTION_STATIC_THRESHOLD = 0.025  # mean abs pixel diff (RGB, normalised 0-1)
DURATION_MISMATCH_THRESHOLD_S = 1.0


@dataclass
class MotionScore:
    """Per-clip motion signal.

    ``mean_abs_diff`` is the average absolute difference between
    first-frame and last-frame pixels, normalised to [0, 1].

    Empirically on our test runs:
    - Ken-Burns'd stills (the failure mode the human reported) score
      0.005 – 0.020 (≈ 1–2% pixel-difference; only the slow parallax
      from i2v's micro-zoom registers).
    - Properly animated clips (Sora 2 / Seedance N→N+1) score
      0.080 – 0.200 (≈ 8–20% — actual character motion across the frame).
    - Pure cuts (e.g. wipe filters) can hit > 0.5.

    ``MOTION_STATIC_THRESHOLD = 0.025`` puts the line between
    "essentially a still" and "actual motion".
    """

    clip_path: Path
    duration_s: float
    mean_abs_diff: float
    is_static: bool
    threshold: float = MOTION_STATIC_THRESHOLD

    def to_dict(self) -> dict[str, Any]:
        return {
            "clip_path": str(self.clip_path),
            "duration_s": round(self.duration_s, 3),
            "mean_abs_diff": round(self.mean_abs_diff, 4),
            "is_static": self.is_static,
            "threshold": self.threshold,
        }


@dataclass
class SceneReview:
    """Per-scene review: motion + duration + intent cross-check + recommendation."""

    scene_idx: int
    expected_duration_s: float
    expected_movement: str
    motion: MotionScore
    issues: list[str] = field(default_factory=list)
    recommendation: str = ""

    @property
    def actual_duration_s(self) -> float:
        return self.motion.duration_s

    @property
    def duration_drift_s(self) -> float:
        return self.actual_duration_s - self.expected_duration_s

    def to_dict(self) -> dict[str, Any]:
        return {
            "scene_idx": self.scene_idx,
            "expected_duration_s": self.expected_duration_s,
            "actual_duration_s": round(self.actual_duration_s, 3),
            "duration_drift_s": round(self.duration_drift_s, 3),
            "expected_movement": self.expected_movement,
            "motion": self.motion.to_dict(),
            "issues": list(self.issues),
            "recommendation": self.recommendation,
        }


@dataclass
class VideoReviewReport:
    """Aggregated review across all scenes in a run."""

    run_id: str
    item_id: int
    order_no: int
    run_no: int
    reviews: list[SceneReview]
    overall_static_ratio: float
    overall_recommendation: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "item_id": self.item_id,
            "order_no": self.order_no,
            "run_no": self.run_no,
            "reviews": [r.to_dict() for r in self.reviews],
            "overall_static_ratio": round(self.overall_static_ratio, 3),
            "overall_recommendation": self.overall_recommendation,
        }


# ---- ffmpeg helpers ----------------------------------------------------- #


def _ffprobe_duration(path: Path) -> float:
    """Return clip duration in seconds via ffprobe."""
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        check=True, capture_output=True, text=True,
    )
    return float(r.stdout.strip())


def _extract_frame(clip_path: Path, *, t: float, out_path: Path) -> None:
    """Extract a single frame at time t (seconds) into out_path as JPG.

    Uses ``-ss`` before ``-i`` for fast seek; if that produces no frame
    (some H.264 streams won't decode the requested time without keyframe),
    falls back to ``-sseof`` (seek-from-end) for the "last frame" case.
    """
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t:.3f}",
         "-i", str(clip_path), "-frames:v", "1", "-q:v", "2", str(out_path)],
        check=True,
    )
    if out_path.exists() and out_path.stat().st_size > 0:
        return
    # Fallback — seek from end of file
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-sseof", "-0.3",
         "-i", str(clip_path), "-frames:v", "1", "-q:v", "2", str(out_path)],
        check=True,
    )


def _mean_abs_diff(img_a: Path, img_b: Path) -> float:
    """Mean absolute difference between two same-size RGB images, normalised to [0, 1].

    Reads raw RGB bytes via ``tobytes()`` — avoids Pillow 12's deprecated
    ``getdata()`` and keeps the implementation numpy-free.
    """
    a = Image.open(img_a).convert("RGB")
    b = Image.open(img_b).convert("RGB")
    if a.size != b.size:
        b = b.resize(a.size, Image.LANCZOS)
    ab = a.tobytes()
    bb = b.tobytes()
    n = len(ab)
    if n == 0:
        return 0.0
    total = sum(abs(ab[i] - bb[i]) for i in range(n))
    return total / (n * 255)


# ---- public API --------------------------------------------------------- #


def analyze_motion(clip_path: Path, *, workdir: Path | None = None) -> MotionScore:
    """Compute motion score for a single clip.

    Extracts first and last frames via ffmpeg, computes pixel-diff via Pillow,
    classifies as static if below threshold.
    """
    duration = _ffprobe_duration(clip_path)
    # Sample slightly inside the boundaries so first/last frames are stable
    t_first = 0.05
    t_last = max(t_first + 0.01, duration - 0.05)
    if workdir is None:
        workdir = Path(tempfile.mkdtemp(prefix="auto-affi-qa-"))
    workdir.mkdir(parents=True, exist_ok=True)
    fa = workdir / f"{clip_path.stem}-first.jpg"
    fb = workdir / f"{clip_path.stem}-last.jpg"
    _extract_frame(clip_path, t=t_first, out_path=fa)
    _extract_frame(clip_path, t=t_last, out_path=fb)
    mad = _mean_abs_diff(fa, fb)
    return MotionScore(
        clip_path=clip_path,
        duration_s=duration,
        mean_abs_diff=mad,
        is_static=mad < MOTION_STATIC_THRESHOLD,
    )


def analyze_scene(
    *,
    scene_idx: int,
    clip_path: Path,
    storyboard_frame: dict[str, Any],
    workdir: Path | None = None,
) -> SceneReview:
    """Combine motion + duration + intent cross-check for one scene."""
    motion = analyze_motion(clip_path, workdir=workdir)
    expected_duration = float(storyboard_frame.get("duration_s", 0.0))
    expected_movement = str(storyboard_frame.get("camera_movement", ""))

    issues: list[str] = []
    rec_parts: list[str] = []

    # Motion intent check
    intends_motion = bool(expected_movement) and "static" not in expected_movement.lower()
    if motion.is_static and intends_motion:
        issues.append("MOTION_INTENT_MISSED")
        rec_parts.append(
            f"Storyboard asks for `{expected_movement}` but clip is essentially still "
            f"(mean abs diff {motion.mean_abs_diff:.4f} < {MOTION_STATIC_THRESHOLD}). "
            f"Switch this scene to Seedance N→N+1 (two keyframes) or raise i2v motion strength."
        )
    elif motion.is_static and not intends_motion:
        # The storyboard agrees this should be still — accept
        rec_parts.append("Scene is intentionally still; motion score matches intent.")

    # Duration drift
    drift = abs(motion.duration_s - expected_duration)
    if drift > DURATION_MISMATCH_THRESHOLD_S:
        issues.append("DURATION_MISMATCH")
        rec_parts.append(
            f"Clip is {motion.duration_s:.2f}s, storyboard expected {expected_duration:.2f}s "
            f"(drift {drift:+.2f}s). Trim/extend in mux."
        )

    if not issues and not rec_parts:
        rec_parts.append("OK — within tolerance.")

    return SceneReview(
        scene_idx=scene_idx,
        expected_duration_s=expected_duration,
        expected_movement=expected_movement,
        motion=motion,
        issues=issues,
        recommendation=" ".join(rec_parts),
    )


def review_video_run(
    *,
    storyboard_json_path: Path,
    workdir: Path,
    run_id: str = "",
    item_id: int = 0,
    order_no: int = 0,
    run_no: int = 0,
    qa_workdir: Path | None = None,
) -> VideoReviewReport:
    """Run motion + duration + intent review for every scene in a run.

    Looks for per-scene clips at ``workdir/s{idx}-clip.mp4``. The
    storyboard JSON drives the scene-by-scene intent.
    """
    storyboard = json.loads(storyboard_json_path.read_text(encoding="utf-8"))
    frames = storyboard.get("frames", [])
    qa_workdir = qa_workdir or (workdir / "qa")
    qa_workdir.mkdir(parents=True, exist_ok=True)

    reviews: list[SceneReview] = []
    for f in frames:
        idx = int(f["idx"])
        clip_path = workdir / f"s{idx}-clip.mp4"
        if not clip_path.exists():
            # Skip silently — caller can filter on missing
            continue
        reviews.append(
            analyze_scene(
                scene_idx=idx,
                clip_path=clip_path,
                storyboard_frame=f,
                workdir=qa_workdir,
            )
        )

    if not reviews:
        overall_recommendation = "No clips found; nothing to review."
        return VideoReviewReport(
            run_id=run_id, item_id=item_id, order_no=order_no, run_no=run_no,
            reviews=[], overall_static_ratio=0.0,
            overall_recommendation=overall_recommendation,
        )

    static_count = sum(1 for r in reviews if r.motion.is_static)
    static_ratio = static_count / len(reviews)

    # Roll up
    intent_misses = [r for r in reviews if "MOTION_INTENT_MISSED" in r.issues]
    if static_ratio >= 0.8 and intent_misses:
        overall_recommendation = (
            f"{static_ratio*100:.0f}% of scenes are essentially stills despite "
            "non-static intent in the storyboard. The single-image i2v engine "
            "is not honouring motion direction. Switch this run to Seedance 1.5 "
            "Pro with N→N+1 keyframes (two stills per clip) before next "
            "iteration. See per-scene recommendations below."
        )
    elif intent_misses:
        overall_recommendation = (
            f"{len(intent_misses)} of {len(reviews)} scenes missed motion "
            "intent. Regenerate those scenes only — keep the rest."
        )
    elif static_ratio == 1.0:
        overall_recommendation = (
            "All scenes are still. If this is intentional (slideshow), accept. "
            "Otherwise switch engine."
        )
    else:
        overall_recommendation = "Run is within tolerance — accept."

    return VideoReviewReport(
        run_id=run_id, item_id=item_id, order_no=order_no, run_no=run_no,
        reviews=reviews, overall_static_ratio=static_ratio,
        overall_recommendation=overall_recommendation,
    )


# ---- Markdown rendering for human review -------------------------------- #


def render_report_md(report: VideoReviewReport) -> str:
    """Render the review as a markdown document for human review."""
    lines: list[str] = []
    lines.append(f"# Video Review · run {report.run_no:04d}")
    lines.append("")
    lines.append(f"- **Run**: order {report.order_no:04d} / run {report.run_no:04d} · `{report.run_id}`")
    lines.append(f"- **Item**: {report.item_id}")
    lines.append(f"- **Scenes reviewed**: {len(report.reviews)}")
    lines.append(f"- **Static ratio**: {report.overall_static_ratio*100:.0f}% "
                 f"(clips below motion threshold {MOTION_STATIC_THRESHOLD})")
    lines.append("")
    lines.append("## Overall verdict")
    lines.append("")
    lines.append(f"> {report.overall_recommendation}")
    lines.append("")
    lines.append("## Per-scene findings")
    lines.append("")
    lines.append("| # | Expected motion | Expected dur | Actual dur | Drift | Pixel-diff | Static? | Issues |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for r in report.reviews:
        issues = ", ".join(r.issues) if r.issues else "—"
        static_flag = "**STATIC**" if r.motion.is_static else "ok"
        lines.append(
            f"| {r.scene_idx+1} | `{r.expected_movement or '—'}` | {r.expected_duration_s:.2f}s | "
            f"{r.motion.duration_s:.2f}s | {r.duration_drift_s:+.2f}s | "
            f"{r.motion.mean_abs_diff:.4f} | {static_flag} | {issues} |"
        )
    lines.append("")
    lines.append("## Per-scene recommendations")
    lines.append("")
    for r in report.reviews:
        lines.append(f"### Scene {r.scene_idx+1}  ·  expected motion: `{r.expected_movement or '—'}`")
        lines.append("")
        lines.append(f"- Motion score: **{r.motion.mean_abs_diff:.4f}** "
                     f"(threshold {MOTION_STATIC_THRESHOLD}; static = below)")
        lines.append(f"- Duration: expected {r.expected_duration_s:.2f}s, actual {r.motion.duration_s:.2f}s "
                     f"({r.duration_drift_s:+.2f}s drift)")
        lines.append(f"- Issues: {', '.join(r.issues) if r.issues else 'none'}")
        lines.append(f"- Recommendation: {r.recommendation}")
        lines.append("")
    return "\n".join(lines)
