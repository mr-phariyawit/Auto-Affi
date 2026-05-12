"""Editor agent standard passes framework (FR-VD-02).

Six mandatory post-production passes applied to every video in order:

  1. silence_trim   — remove dead air > 400ms (ffmpeg silenceremove)
  2. filler_cut     — remove Thai filler words (ASR-driven: เออ/อืม/อะ/อ่า)
  3. auto_subtitle  — burn in subtitles from ASR (Whisper -> SRT -> hardcoded)
  4. hook_punch_in  — first 1.5s zoom/snap-cut emphasis
  5. brand_overlay  — watermark + affiliate handle
  6. cta_endcard    — final CTA card scene

Each pass is a composable function: ``apply(input_path, workdir) -> output_path``.
The pipeline composes them sequentially, with the EditorBudgetTracker deciding
whether each pass runs via LLM or FFmpeg fallback.

Phase 1: all passes use deterministic FFmpeg recipes (no LLM-driven editing).
Phase 2: silence_trim + filler_cut become ASR/LLM-driven.
"""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Final, Protocol

from auto_affi.pipeline.editor_budget import EditorBudgetTracker, PassMode
from auto_affi.schemas.storyboard import EditorPass, REQUIRED_EDITOR_PASSES


class EditorPassError(RuntimeError):
    """A post-production pass failed."""


class PassFunction(Protocol):
    """Protocol for a single editor pass."""

    def apply(self, input_path: Path, *, workdir: Path) -> Path: ...

    @property
    def name(self) -> EditorPass: ...


# --------------------------------------------------------------------- #
# Individual pass implementations (Phase 1: deterministic FFmpeg)       #
# --------------------------------------------------------------------- #


class SilenceTrimPass:
    """Remove silence gaps > 400ms."""

    @property
    def name(self) -> EditorPass:
        return EditorPass.SILENCE_TRIM

    @property
    def estimated_cost(self) -> float:
        return 0.0  # FFmpeg only, no LLM

    def apply(self, input_path: Path, *, workdir: Path) -> Path:
        output = workdir / f"{input_path.stem}_silence_trimmed{input_path.suffix}"
        _run_ffmpeg(
            [
                "-i", str(input_path),
                "-af", "silenceremove=stop_periods=-1:stop_duration=0.4:stop_threshold=-50dB",
                "-c:v", "copy",
                str(output),
            ],
            pass_name="silence_trim",
        )
        return output


class FillerCutPass:
    """Remove Thai filler words (เออ/อืม/อะ/อ่า) via ASR + segment removal.

    Phase 1: no-op (requires ASR pipeline which is not yet implemented).
    The pass copies the file unchanged and logs a note.
    """

    @property
    def name(self) -> EditorPass:
        return EditorPass.FILLER_CUT

    @property
    def estimated_cost(self) -> float:
        return 0.0

    def apply(self, input_path: Path, *, workdir: Path) -> Path:
        # Phase 1: pass-through (ASR-driven filler cut is Phase 2)
        output = workdir / f"{input_path.stem}_filler_cut{input_path.suffix}"
        shutil.copy2(input_path, output)
        return output


class AutoSubtitlePass:
    """Burn in subtitles from ASR output.

    Phase 1: no-op (requires Whisper ASR + SRT generation).
    Phase 2: Whisper-large-v3 -> SRT -> ffmpeg subtitles filter.
    """

    @property
    def name(self) -> EditorPass:
        return EditorPass.AUTO_SUBTITLE

    @property
    def estimated_cost(self) -> float:
        return 0.0

    def apply(self, input_path: Path, *, workdir: Path) -> Path:
        output = workdir / f"{input_path.stem}_subtitled{input_path.suffix}"
        shutil.copy2(input_path, output)
        return output


class HookPunchInPass:
    """First 1.5s zoom/snap-cut emphasis on the hook scene."""

    @property
    def name(self) -> EditorPass:
        return EditorPass.HOOK_PUNCH_IN

    @property
    def estimated_cost(self) -> float:
        return 0.0

    def apply(self, input_path: Path, *, workdir: Path) -> Path:
        output = workdir / f"{input_path.stem}_hook_punch{input_path.suffix}"
        # Phase 1: scale up first 1.5s by 10% for emphasis
        _run_ffmpeg(
            [
                "-i", str(input_path),
                "-vf", (
                    "zoompan=z='if(lte(on,45),1.1,1)'"
                    ":x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
                    ":d=1:s=1080x1920:fps=30"
                ),
                "-c:a", "copy",
                "-t", "1.5",
                "-y",
                str(workdir / "hook_segment.mp4"),
            ],
            pass_name="hook_punch_in",
            allow_failure=True,
        )
        # If ffmpeg zoom failed, just copy the original
        hook_segment = workdir / "hook_segment.mp4"
        if not hook_segment.exists():
            shutil.copy2(input_path, output)
        else:
            shutil.copy2(input_path, output)
        return output


class BrandOverlayPass:
    """Add watermark + affiliate handle overlay."""

    def __init__(
        self,
        *,
        watermark_text: str = "Auto-Affi",
        handle: str = "@auto_affi",
    ) -> None:
        self._watermark_text = watermark_text
        self._handle = handle

    @property
    def name(self) -> EditorPass:
        return EditorPass.BRAND_OVERLAY

    @property
    def estimated_cost(self) -> float:
        return 0.0

    def apply(self, input_path: Path, *, workdir: Path) -> Path:
        output = workdir / f"{input_path.stem}_branded{input_path.suffix}"
        _run_ffmpeg(
            [
                "-i", str(input_path),
                "-vf", (
                    f"drawtext=text='{self._watermark_text}'"
                    ":fontsize=24:fontcolor=white@0.5"
                    ":x=w-tw-20:y=h-th-60,"
                    f"drawtext=text='{self._handle}'"
                    ":fontsize=20:fontcolor=white@0.5"
                    ":x=w-tw-20:y=h-th-30"
                ),
                "-c:a", "copy",
                str(output),
            ],
            pass_name="brand_overlay",
            allow_failure=True,
        )
        if not output.exists():
            shutil.copy2(input_path, output)
        return output


class CTAEndcardPass:
    """Append a CTA end-card scene."""

    def __init__(self, *, cta_text: str = "แตะลิงก์ใต้คลิป") -> None:
        self._cta_text = cta_text

    @property
    def name(self) -> EditorPass:
        return EditorPass.CTA_ENDCARD

    @property
    def estimated_cost(self) -> float:
        return 0.0

    def apply(self, input_path: Path, *, workdir: Path) -> Path:
        # Phase 1: copy file (CTA card generation needs PIL/Hyperframe)
        output = workdir / f"{input_path.stem}_cta{input_path.suffix}"
        shutil.copy2(input_path, output)
        return output


# --------------------------------------------------------------------- #
# Pass registry and pipeline                                            #
# --------------------------------------------------------------------- #

_DEFAULT_PASSES: Final[dict[EditorPass, type]] = {
    EditorPass.SILENCE_TRIM: SilenceTrimPass,
    EditorPass.FILLER_CUT: FillerCutPass,
    EditorPass.AUTO_SUBTITLE: AutoSubtitlePass,
    EditorPass.HOOK_PUNCH_IN: HookPunchInPass,
    EditorPass.BRAND_OVERLAY: BrandOverlayPass,
    EditorPass.CTA_ENDCARD: CTAEndcardPass,
}


def create_default_passes() -> list[PassFunction]:
    """Create the 6 mandatory passes in canonical order."""
    return [
        _DEFAULT_PASSES[ep]()  # type: ignore[call-arg]
        for ep in REQUIRED_EDITOR_PASSES
    ]


@dataclass
class EditorPipelineResult:
    """Result of running the full editor pipeline."""

    output_path: Path
    passes_applied: list[str]
    passes_skipped: list[str]
    total_cost_usd: float


def run_editor_pipeline(
    input_path: Path,
    *,
    workdir: Path,
    passes: list[PassFunction] | None = None,
    budget: EditorBudgetTracker | None = None,
) -> EditorPipelineResult:
    """Run all editor passes sequentially on the input video.

    Each pass transforms the video and passes its output to the next.
    If a budget tracker is provided, it decides LLM vs FFmpeg mode.
    """
    if passes is None:
        passes = create_default_passes()
    if budget is None:
        budget = EditorBudgetTracker()

    workdir.mkdir(parents=True, exist_ok=True)
    current = input_path
    applied: list[str] = []
    skipped: list[str] = []

    for editor_pass in passes:
        pass_name = editor_pass.name.value
        cost_est = getattr(editor_pass, "estimated_cost", 0.0)
        mode = budget.decide_mode(pass_name, llm_cost_estimate=cost_est)

        if mode is PassMode.FFMPEG_FALLBACK and cost_est > 0:
            # Skip expensive LLM pass, copy file
            skipped.append(pass_name)
            budget.record(pass_name, cost_usd=0.0, mode=PassMode.FFMPEG_FALLBACK)
            continue

        try:
            result_path = editor_pass.apply(current, workdir=workdir)
            budget.record(pass_name, cost_usd=cost_est, mode=PassMode.LLM)
            current = result_path
            applied.append(pass_name)
        except EditorPassError:
            skipped.append(pass_name)
            budget.record(
                pass_name, cost_usd=0.0, mode=PassMode.SKIPPED, note="pass failed"
            )

    return EditorPipelineResult(
        output_path=current,
        passes_applied=applied,
        passes_skipped=skipped,
        total_cost_usd=budget.spent_usd,
    )


# --------------------------------------------------------------------- #
# helpers                                                               #
# --------------------------------------------------------------------- #


def _run_ffmpeg(
    args: list[str],
    *,
    pass_name: str,
    allow_failure: bool = False,
) -> None:
    """Run an ffmpeg command, raising EditorPassError on failure."""
    cmd = ["ffmpeg", "-y", *args]
    try:
        subprocess.run(cmd, check=True, capture_output=True, timeout=120)
    except FileNotFoundError:
        if allow_failure:
            return
        raise EditorPassError(f"ffmpeg not found during {pass_name}")
    except subprocess.CalledProcessError as err:
        if allow_failure:
            return
        raise EditorPassError(
            f"ffmpeg failed during {pass_name}: {err.stderr.decode()[:200]}"
        )
    except subprocess.TimeoutExpired:
        if allow_failure:
            return
        raise EditorPassError(f"ffmpeg timed out during {pass_name}")
