"""Hand-built demo storyboard used by the credential-free local renderer.

Pure data, no agent calls or vendor I/O. Consumed by:

  - ``auto_affi.ops.make_demo`` — CLI entrypoint for ``demo.mp4``
  - ``tests.unit.test_local_renderer_helpers`` — schema-level sanity
  - ``tests.integration.test_local_renderer`` — end-to-end mp4 render

Kept separate from ``pipeline.local_renderer`` so the renderer module stays
focused on the FFmpeg/PIL pipeline and demo data stays grep-able as a single
canonical fixture.
"""

from __future__ import annotations

from auto_affi.schemas.storyboard import (
    Dialogue,
    MusicBrief,
    OnScreenText,
    Scene,
    ScenePurpose,
    Storyboard,
    VoiceProfile,
)


def build_demo_storyboard() -> Storyboard:
    """Return the canonical demo storyboard for the credential-free pipeline."""
    voice = VoiceProfile(
        lang="th",
        gender="f",
        tone="energetic-confidant",
        tts_engine="elevenlabs",
        voice_id="local-espeak",
    )
    music = MusicBrief(genre="lofi-hype", bpm_range=(90, 110), license="suno")

    scenes = [
        Scene(
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
        Scene(
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
        Scene(
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
        Scene(
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
        Scene(
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
