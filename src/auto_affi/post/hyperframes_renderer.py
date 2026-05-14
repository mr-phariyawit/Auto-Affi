"""HyperFrames renderer — wire ``Storyboard.hyperframe_overlays`` to MOVs.

For each :class:`HyperframeOverlay` declared on a Storyboard, this module:

1. Resolves the overlay's ``template`` name to a HyperFrames project under
   ``hyperframes/<template>/``.
2. Invokes ``npx hyperframes render`` with the overlay's ``props`` passed
   via ``--variables`` (JSON-encoded).
3. Returns a list of :class:`OverlayRender` records giving the local MOV
   path + the absolute start/duration on the final video timeline, so a
   caller can compose them via ffmpeg ``overlay`` filters.

Convention for time positioning (until the schema grows explicit fields):
the overlay's start/duration on the final timeline live in ``props`` as
the keys ``start_s`` (absolute seconds) and ``duration_s``. Renderer
falls back to the composition's declared duration if ``duration_s`` is
missing.

Time placement IS NOT applied to the MOV — the MOV is the overlay's own
length only. Compositing onto the final timeline (with ``-itsoffset`` /
``overlay=enable``) is the caller's job; this module just produces the
asset + the metadata for that compositing.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from auto_affi.schemas.storyboard import HyperframeOverlay


class HyperframesRendererError(RuntimeError):
    """Raised when HyperFrames render fails or required tooling is missing."""


@dataclass(frozen=True)
class OverlayRender:
    """One rendered overlay ready for ffmpeg compositing."""

    template: str
    scene_idx: int
    mov_path: Path
    start_s: float
    duration_s: float
    props: dict[str, object] = field(default_factory=dict)


def _hyperframes_available() -> bool:
    """Quick check for ``npx``; full ``hyperframes`` availability comes
    from the first ``npx --yes hyperframes`` invocation."""
    return shutil.which("npx") is not None


def render_storyboard_overlays(
    *,
    overlays: list[HyperframeOverlay],
    projects_dir: Path,
    output_dir: Path,
    quality: str = "high",
    fps: int = 30,
    aspect: str = "9:16",
) -> list[OverlayRender]:
    """Render every overlay in ``overlays`` to a MOV (ProRes 4444, alpha).

    Args:
        overlays: HyperframeOverlay entries from a Storyboard.
        projects_dir: directory containing per-template HyperFrames
            projects. Each overlay's ``template`` resolves to
            ``projects_dir / <template>``.
        output_dir: where to write the MOVs and metadata sidecar.
        quality: HyperFrames ``--quality`` (draft / standard / high).
        fps: target frame rate.
        aspect: informational only — the HTML composition declares its
            own ``data-width`` / ``data-height``; we just track the value
            so the caller can check it matches the base video.

    Returns:
        One :class:`OverlayRender` per overlay (skipping any whose
        template directory is missing — failures are logged, not raised,
        so a single broken template doesn't sink the whole run).

    Raises:
        HyperframesRendererError: if ``npx`` is unavailable.
    """
    if not _hyperframes_available():
        raise HyperframesRendererError(
            "HyperFrames renderer requires `npx` on PATH (Node.js >= 22)."
        )
    output_dir.mkdir(parents=True, exist_ok=True)

    results: list[OverlayRender] = []
    for ov in overlays:
        template_dir = projects_dir / ov.template
        if not (template_dir / "index.html").exists():
            print(
                f"  ⚠️  overlay template missing: {template_dir} — skipping "
                f"(scene_idx={ov.scene_idx}, template={ov.template!r})"
            )
            continue

        start_s = float(ov.props.get("start_s", 0.0))
        duration_s = float(ov.props.get("duration_s", 0.0))

        mov_path = (output_dir / f"overlay-{ov.scene_idx}-{ov.template}.mov").resolve()

        # Build --variables JSON: pass ALL props through so the composition
        # can pick them up via window.__hyperframes.getVariables().
        # The renderer reads start_s/duration_s for its own positioning
        # bookkeeping but the composition author may also use them.
        variables_json = json.dumps({k: v for k, v in ov.props.items()}, ensure_ascii=False)

        cmd = [
            "npx", "--yes", "hyperframes", "render",
            str(template_dir),
            "--output", str(mov_path),
            "--format", "mov",
            "--quality", quality,
            "--fps", str(fps),
            "--variables", variables_json,
        ]
        print(f"  rendering overlay {ov.scene_idx}/{ov.template} → {mov_path.name}")
        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            stderr_tail = (e.stderr or "")[-400:]
            print(f"    ❌ render failed: {stderr_tail}")
            continue

        # If duration_s wasn't supplied via props, probe the MOV
        if duration_s <= 0:
            duration_s = _ffprobe_duration(mov_path)

        results.append(
            OverlayRender(
                template=ov.template,
                scene_idx=ov.scene_idx,
                mov_path=mov_path,
                start_s=start_s,
                duration_s=duration_s,
                props=dict(ov.props),
            )
        )

    # Persist a sidecar manifest so downstream tools (compositor / debug)
    # can re-read the result set without re-invoking the renderer.
    manifest_path = output_dir / "overlays-manifest.json"
    manifest_path.write_text(
        json.dumps(
            [
                {
                    "template": r.template,
                    "scene_idx": r.scene_idx,
                    "mov_path": str(r.mov_path),
                    "start_s": r.start_s,
                    "duration_s": r.duration_s,
                    "props": r.props,
                }
                for r in results
            ],
            indent=2, ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    return results


def _ffprobe_duration(path: Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        check=True, capture_output=True, text=True,
    )
    return float(r.stdout.strip())


def composite_overlays_with_ffmpeg(
    *,
    base_video: Path,
    overlays: list[OverlayRender],
    output: Path,
) -> Path:
    """Composite a list of OverlayRender records onto a base video.

    Each overlay is layered via ``-itsoffset <start_s>`` + an overlay
    filter limited to its window. Output is re-encoded (video re-encode
    is necessary for the overlay filter; audio is copied through).

    Returns the output path.
    """
    if not overlays:
        # No overlays — pass-through copy
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-i", str(base_video),
             "-c", "copy", str(output)],
            check=True,
        )
        return output

    args = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(base_video)]
    # Each overlay is a delayed input
    for ov in overlays:
        args += ["-itsoffset", f"{ov.start_s:.3f}", "-i", str(ov.mov_path)]

    # Build per-overlay overlay filters chained
    fc_parts: list[str] = []
    cur = "[0:v]"
    for i, ov in enumerate(overlays, start=1):
        out_label = f"[v{i}]"
        end_s = ov.start_s + ov.duration_s
        fc_parts.append(
            f"{cur}[{i}:v]overlay=enable='between(t,{ov.start_s:.3f},{end_s:.3f})':x=0:y=0:format=auto{out_label}"
        )
        cur = out_label

    args += [
        "-filter_complex", ";".join(fc_parts),
        "-map", cur, "-map", "0:a",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
        "-c:a", "copy",
        "-shortest",
        str(output),
    ]
    subprocess.run(args, check=True)
    return output
