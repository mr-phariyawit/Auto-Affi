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
    if shutil.which("ffmpeg") is None:
        raise RendererError("ffmpeg not on PATH; install ffmpeg")
    if enable_tts and shutil.which("espeak-ng") is None:
        raise RendererError("espeak-ng not on PATH; install espeak-ng or pass enable_tts=False")


def _pick_thai_font(size: int) -> ImageFont.FreeTypeFont:
    for path in _THAI_FONT_CANDIDATES:
        if Path(path).exists():
            return ImageFont.truetype(path, size=size)
    raise RendererError(
        f"no Thai-capable font found; install one of: {', '.join(_THAI_FONT_CANDIDATES)}"
    )


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
    pixels = image.load()
    if pixels is None:  # pragma: no cover - PIL guarantees this
        return
    height = image.size[1]
    for y in range(height):
        t = y / max(height - 1, 1)
        r = int(top[0] + (bottom[0] - top[0]) * t)
        g = int(top[1] + (bottom[1] - top[1]) * t)
        b = int(top[2] + (bottom[2] - top[2]) * t)
        for x in range(image.size[0]):
            pixels[x, y] = (r, g, b)


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


def build_demo_storyboard() -> Storyboard:
    """Return a hand-built canonical demo storyboard.

    Pure data, no agent calls. Used by ``ops/make_demo.py`` so the demo
    end-to-end runs without LLM tokens or vendor credentials.
    """
    from auto_affi.schemas.storyboard import (
        Dialogue,
        MusicBrief,
        OnScreenText,
        ScenePurpose,
        VoiceProfile,
    )
    from auto_affi.schemas.storyboard import (
        Scene as _Scene,
    )

    voice = VoiceProfile(
        lang="th",
        gender="f",
        tone="energetic-confidant",
        tts_engine="elevenlabs",
        voice_id="local-espeak",
    )
    music = MusicBrief(genre="lofi-hype", bpm_range=(90, 110), license="suno")

    scenes = [
        _Scene(
            idx=0,
            duration_s=1.5,
            purpose=ScenePurpose.HOOK,
            shot_type="extreme-closeup",
            movement="snap-zoom-in",
            visual_prompt="oily-skin POV opening shot",
            generator="veo3_fast",
            dialogue=Dialogue(speaker="narrator", text_th="POV คนผิวมัน หาครีมไม่เจอ"),
            on_screen_text=OnScreenText(
                th="POV: คนผิวมัน",
                style="bold-pop",
                position="center-upper",
            ),
        ),
        _Scene(
            idx=1,
            duration_s=2.0,
            purpose=ScenePurpose.AGITATE,
            shot_type="medium",
            visual_prompt="mid-day shine on forehead",
            generator="veo3_fast",
            dialogue=Dialogue(speaker="narrator", text_th="หน้ามันตอนบ่ายทุกวัน เซ็งมาก"),
            on_screen_text=OnScreenText(
                th="หน้ามันบ่าย ๆ",
                style="bold-pop",
                position="center",
            ),
        ),
        _Scene(
            idx=2,
            duration_s=2.0,
            purpose=ScenePurpose.DEMONSTRATE,
            shot_type="medium-closeup",
            visual_prompt="apply serum on forearm in soft daylight",
            generator="veo3_fast",
            dialogue=Dialogue(speaker="narrator", text_th="ลองตัวนี้ ใช้ก่อนแต่งหน้าเลย"),
            on_screen_text=OnScreenText(
                th="ลองตัวนี้",
                style="bold-pop",
                position="center",
            ),
        ),
        _Scene(
            idx=3,
            duration_s=2.0,
            purpose=ScenePurpose.RESOLVE,
            shot_type="medium",
            visual_prompt="matte finish after application",
            generator="veo3_fast",
            dialogue=Dialogue(speaker="narrator", text_th="หน้าเรียบ ไม่มันยาว ๆ"),
            on_screen_text=OnScreenText(
                th="หน้าไม่มัน",
                style="bold-pop",
                position="center",
            ),
        ),
        _Scene(
            idx=4,
            duration_s=2.0,
            purpose=ScenePurpose.CTA,
            shot_type="medium",
            visual_prompt="hand pointing to caption with QR overlay",
            generator="veo3_fast",
            dialogue=Dialogue(speaker="narrator", text_th="แตะลิงก์ใต้คลิป"),
            on_screen_text=OnScreenText(
                th="แตะลิงก์ใต้คลิป",
                style="bold-pop",
                position="center",
            ),
        ),
    ]

    return Storyboard(
        brief_id="demo-brief-001",
        voice_profile=voice,
        music_brief=music,
        scenes=scenes,
        cta_scene_idx=4,
        affiliate_link_placement="pinned_comment + on_screen_qr",
    )
