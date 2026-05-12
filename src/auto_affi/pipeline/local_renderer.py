"""Local 9:16 video renderer for the Claude Code demo path.

Produces a real ``.mp4`` from a :class:`Storyboard` without any vendor
credentials. Quality is intentionally placeholder-grade (PIL panels +
espeak-ng Thai TTS) so the rest of the pipeline -- agents, schemas,
publisher, analytics -- can run end-to-end inside this sandbox while we
wait for kie.ai / ElevenLabs / Shopee credentials.

Once those credentials exist, the production renderer (Veo + Hyperframe +
ElevenLabs) drops into ``pipeline/renderer.py`` and this module becomes a
fallback / CI fixture.

External tools required (already on the dev image):
  - ffmpeg
  - espeak-ng (with Thai voice "th")
  - Pillow + a Thai-capable font (Loma is fine, NotoSansThai if available)
"""

from __future__ import annotations

import functools
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Final

from PIL import Image, ImageDraw, ImageFont

from auto_affi.schemas.storyboard import Scene, Storyboard

# 9:16 master resolution per SPEC.md §3.5 / SRS FR-VD-01.
WIDTH: Final[int] = 1080
HEIGHT: Final[int] = 1920
FPS: Final[int] = 30
SAMPLE_RATE: Final[int] = 44_100

# Fonts shipped with tlwg-fonts / fonts-tlwg-loma on Debian-family images.
_THAI_FONT_CANDIDATES: Final[tuple[str, ...]] = (
    "/usr/share/fonts/opentype/tlwg/Loma-Bold.otf",
    "/usr/share/fonts/truetype/tlwg/Loma-Bold.ttf",
    "/usr/share/fonts/opentype/tlwg/Loma.otf",
    "/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf",
)


@dataclass(frozen=True)
class RenderResult:
    """Outcome of a render. ``mp4_path`` is the only thing callers need."""

    mp4_path: Path
    duration_s: float
    scene_count: int


class RendererError(RuntimeError):
    """Raised when ffmpeg or espeak-ng fails inside the local pipeline."""


# --------------------------------------------------------------------- #
# public surface                                                        #
# --------------------------------------------------------------------- #


def render_storyboard(
    storyboard: Storyboard,
    *,
    workdir: Path,
    output_path: Path,
    enable_tts: bool = True,
) -> RenderResult:
    """Render ``storyboard`` to a 9:16 mp4 at ``output_path``.

    ``workdir`` is wiped before use; callers should pass a tmp dir.
    """
    _check_tools(enable_tts=enable_tts)
    workdir.mkdir(parents=True, exist_ok=True)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    scene_clips: list[Path] = []
    for scene in storyboard.scenes:
        image_path = _render_scene_panel(scene, workdir)
        audio_path = _render_scene_audio(scene, workdir) if enable_tts else None
        clip_path = _compose_scene_clip(
            scene=scene,
            image_path=image_path,
            audio_path=audio_path,
            workdir=workdir,
        )
        scene_clips.append(clip_path)

    final_path = _concat_clips(scene_clips, output_path=output_path, workdir=workdir)
    return RenderResult(
        mp4_path=final_path,
        duration_s=storyboard.total_duration_s,
        scene_count=len(storyboard.scenes),
    )


# --------------------------------------------------------------------- #
# implementation                                                        #
# --------------------------------------------------------------------- #


def _check_tools(*, enable_tts: bool) -> None:
    required: tuple[tuple[str, str], ...] = (("ffmpeg", "install ffmpeg"),)
    if enable_tts:
        required = (*required, ("espeak-ng", "install espeak-ng or pass enable_tts=False"))
    missing = [(name, hint) for name, hint in required if shutil.which(name) is None]
    if missing:
        first_name, first_hint = missing[0]
        raise RendererError(f"{first_name} not on PATH; {first_hint}")


@functools.cache
def _resolve_thai_font_path() -> str:
    """Resolve a Thai-capable font path once per process.

    Returns the first hit from the hardcoded candidate list, then falls back
    to fontconfig (``fc-match :lang=th``) for distros where Thai fonts live
    under a path we did not predict. Cached because resolution does a
    ``stat`` per candidate plus an optional subprocess.
    """
    for path in _THAI_FONT_CANDIDATES:
        if Path(path).exists():
            return path
    via_fc = _font_path_via_fc_match()
    if via_fc is not None:
        return via_fc
    raise RendererError(
        "no Thai-capable font found; install fonts-tlwg or fonts-thai-tlwg "
        "or any font listing 'lang=th' to fontconfig"
    )


@functools.cache
def _pick_thai_font(size: int) -> ImageFont.FreeTypeFont:
    """Return a cached :class:`ImageFont.FreeTypeFont` at the requested size.

    Caching matters because ``render_storyboard`` calls this twice per scene
    (headline + badge) at fixed sizes; without the cache each call walks the
    candidate list and reopens the truetype file.
    """
    return ImageFont.truetype(_resolve_thai_font_path(), size=size)


def _font_path_via_fc_match() -> str | None:
    """Resolve a Thai-capable font via fontconfig. Returns ``None`` if absent."""
    fc_match = shutil.which("fc-match")
    if fc_match is None:
        return None
    proc = subprocess.run(  # noqa: S603 -- fc_match is absolute, args are static
        [fc_match, "-f", "%{file}", ":lang=th"],
        check=False,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        return None
    path = proc.stdout.strip()
    return path if path and Path(path).exists() else None


def _render_scene_panel(scene: Scene, workdir: Path) -> Path:
    """Render one 1080x1920 PNG for a scene.

    Visual is a vertical gradient + headline (on_screen_text or scene purpose)
    + a scene-purpose badge. Real production uses Veo / Imagen; this gets us
    a usable visual without GPU spend.
    """
    image = Image.new("RGB", (WIDTH, HEIGHT))
    _fill_gradient(image, top=(20, 24, 48), bottom=(80, 50, 120))

    draw = ImageDraw.Draw(image)
    headline = _scene_headline(scene)
    font = _pick_thai_font(size=92)
    _draw_centered(draw, headline, font, y=HEIGHT // 2 - 80, max_width=WIDTH - 160)

    badge_font = _pick_thai_font(size=44)
    badge = scene.purpose.value.upper()
    draw.rectangle((60, 60, 60 + 300, 60 + 80), fill=(255, 255, 255, 220))
    draw.text((75, 70), badge, fill=(20, 24, 48), font=badge_font)

    out = workdir / f"scene_{scene.idx:02d}.png"
    image.save(out, "PNG")
    return out


def _scene_headline(scene: Scene) -> str:
    if scene.on_screen_text is not None:
        return scene.on_screen_text.th
    if scene.dialogue is not None:
        return scene.dialogue.text_th
    return scene.visual_prompt[:80]


def _fill_gradient(
    image: Image.Image, *, top: tuple[int, int, int], bottom: tuple[int, int, int]
) -> None:
    """Paint a vertical top→bottom gradient onto ``image`` in place.

    Builds a 1-pixel-wide gradient column (one ``putpixel`` per row) and
    resizes it to image width with ``Image.NEAREST``. This is ~100x faster
    than the previous per-pixel Python loop (avoids ``WIDTH * HEIGHT``
    Python attribute accesses) and the visual output is identical because
    the gradient varies only along Y.
    """
    width, height = image.size
    if height == 0 or width == 0:  # pragma: no cover - defensive
        return
    column = Image.new("RGB", (1, height))
    column_pixels = column.load()
    if column_pixels is None:  # pragma: no cover - PIL guarantees this
        return
    denom = max(height - 1, 1)
    for y in range(height):
        t = y / denom
        column_pixels[0, y] = (
            int(top[0] + (bottom[0] - top[0]) * t),
            int(top[1] + (bottom[1] - top[1]) * t),
            int(top[2] + (bottom[2] - top[2]) * t),
        )
    image.paste(column.resize((width, height), Image.Resampling.NEAREST))


def _draw_centered(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.FreeTypeFont,
    *,
    y: int,
    max_width: int,
) -> None:
    lines = _wrap(text, font, max_width=max_width)
    line_height = font.size + 12
    total_height = line_height * len(lines)
    start_y = y - total_height // 2
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        line_width = bbox[2] - bbox[0]
        draw.text(
            ((WIDTH - line_width) // 2, start_y + i * line_height),
            line,
            fill=(255, 255, 255),
            font=font,
            stroke_width=3,
            stroke_fill=(0, 0, 0),
        )


def _wrap(text: str, font: ImageFont.FreeTypeFont, *, max_width: int) -> list[str]:
    """Wrap text without spaces (Thai) by character; ASCII falls back to word wrap."""
    if " " in text and any(ch.isascii() for ch in text):
        words = text.split()
        lines: list[str] = []
        current = ""
        for word in words:
            probe = f"{current} {word}".strip()
            if font.getlength(probe) > max_width and current:
                lines.append(current)
                current = word
            else:
                current = probe
        if current:
            lines.append(current)
        return lines

    # Thai has no inter-word spaces -- wrap by character.
    lines = []
    current = ""
    for ch in text:
        if font.getlength(current + ch) > max_width and current:
            lines.append(current)
            current = ch
        else:
            current += ch
    if current:
        lines.append(current)
    return lines


def _render_scene_audio(scene: Scene, workdir: Path) -> Path | None:
    if scene.dialogue is None or not scene.dialogue.text_th.strip():
        return None
    out_wav = workdir / f"scene_{scene.idx:02d}.wav"
    cmd = [
        "espeak-ng",
        "-v",
        "th",
        "-s",
        "165",
        "-w",
        str(out_wav),
        scene.dialogue.text_th,
    ]
    _run(cmd, error="espeak-ng failed")
    return out_wav


def _compose_scene_clip(
    *,
    scene: Scene,
    image_path: Path,
    audio_path: Path | None,
    workdir: Path,
) -> Path:
    out = workdir / f"scene_{scene.idx:02d}.mp4"
    cmd: list[str] = [
        "ffmpeg",
        "-y",
        "-loop",
        "1",
        "-t",
        f"{scene.duration_s:.3f}",
        "-i",
        str(image_path),
    ]
    if audio_path is not None:
        cmd += ["-i", str(audio_path), "-shortest"]
    else:
        cmd += [
            "-f",
            "lavfi",
            "-t",
            f"{scene.duration_s:.3f}",
            "-i",
            f"anullsrc=channel_layout=stereo:sample_rate={SAMPLE_RATE}",
        ]
    cmd += [
        "-vf",
        f"scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=increase,crop={WIDTH}:{HEIGHT}",
        "-r",
        str(FPS),
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-ar",
        str(SAMPLE_RATE),
        "-b:a",
        "128k",
        "-movflags",
        "+faststart",
        str(out),
    ]
    _run(cmd, error=f"ffmpeg compose failed for scene {scene.idx}")
    return out


def _concat_clips(clips: list[Path], *, output_path: Path, workdir: Path) -> Path:
    if not clips:
        raise RendererError("no scene clips to concatenate")
    list_path = workdir / "concat.txt"
    list_path.write_text("\n".join(f"file '{clip.resolve()}'" for clip in clips), encoding="utf-8")
    cmd = [
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(list_path),
        "-c",
        "copy",
        str(output_path),
    ]
    _run(cmd, error="ffmpeg concat failed")
    return output_path


def _run(cmd: list[str], *, error: str) -> None:
    proc = subprocess.run(  # noqa: S603 -- args are controlled, not shell-evaluated
        cmd,
        check=False,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise RendererError(
            f"{error}: exit {proc.returncode}\ncmd: {' '.join(cmd)}\nstderr: {proc.stderr[-500:]}"
        )
