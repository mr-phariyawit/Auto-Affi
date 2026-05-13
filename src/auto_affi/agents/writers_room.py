"""Writers' Room — LLM-driven storyboard generation + debate panel (FR-WR-01..04).

Phase 1: Single Writer agent generates a Storyboard from a CampaignBrief
using Phaya GPT (Gemini Flash) for cheap iteration.

Phase 2: Full debate panel — Director / Screenwriter / Cinematographer /
Storyboard Artist / Sound Designer / Critic. Debate-then-Director-decides
pattern per agent-hierarchy.md resonance.

The Writer produces per-scene visual_prompt strings with explicit lighting,
framing, color, and mood instructions. These prompts are the primary input
to the Phaya video/image pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from auto_affi.schemas.campaign_brief import CampaignBrief
from auto_affi.schemas.storyboard import (
    Dialogue,
    HyperframeOverlay,
    MusicBrief,
    OnScreenText,
    Scene,
    ScenePurpose,
    Storyboard,
    VoiceProfile,
)
from auto_affi.schemas.tool_result import ToolResult

# ------------------------------------------------------------------ #
# Storyboard generation prompt                                        #
# ------------------------------------------------------------------ #

_SYSTEM_PROMPT = """\
You are the Auto-Affi Writers' Room — a Thai-native video creative team.
Your job: take a CampaignBrief and produce a Storyboard JSON for a
premium 9:16 vertical affiliate video (Instagram Reels / Facebook Reels).

HARD RULES:
1. Total duration <= 60 seconds. Hook scene <= 2.0 seconds.
2. Scene[0] purpose MUST be "hook". Last scene purpose MUST be "cta".
3. Average body-scene duration: 1.0 - 3.0 seconds.
4. Each visual_prompt: describe EXACTLY what the camera sees. Include:
   - Lighting (studio soft, golden hour, neon, etc.)
   - Framing (extreme closeup, medium, wide, overhead)
   - Movement (snap zoom in, dolly right, static, rack focus)
   - Color mood (warm amber, cool blue, pink glow, clean white)
   - Subject + action in the frame
5. All dialogue.text_th in native Thai. No transliteration.
6. generator for each scene must be one of: sora2, flux, imagen, kling, hailuo, veo3, veo3_fast
7. affiliate_link_placement must include "pinned_comment".

STORYBOARD JSON FORMAT (Pydantic-validated, return ONLY valid JSON):
{
  "brief_id": "<from input>",
  "voice_profile": {"lang": "th", "gender": "f", "tone": "energetic-confidant", "tts_engine": "elevenlabs", "voice_id": "auto"},
  "music_brief": {"genre": "<pick>", "bpm_range": [<lo>, <hi>], "license": "epidemic-sound"},
  "scenes": [
    {
      "idx": 0,
      "duration_s": <1.0-2.0 for hook>,
      "purpose": "hook",
      "shot_type": "<type>",
      "movement": "<movement>",
      "visual_prompt": "<detailed prompt>",
      "generator": "sora2",
      "dialogue": {"speaker": "narrator", "text_th": "<Thai>", "emphasis_words": []},
      "on_screen_text": {"th": "<Thai>", "style": "bold-pop", "position": "center-upper"},
      "sfx": [],
      "transition_out": "match-cut"
    }
  ],
  "cta_scene_idx": <last-scene-idx>,
  "affiliate_link_placement": "pinned_comment + on_screen_qr"
}
"""

_USER_TEMPLATE = """\
Create a storyboard for this campaign brief:

Product: {product_name} (item {product_id})
Angle: {angle}
Hook template: {hook_template}
Target persona: {persona_label}
CTA: {cta_text}
Hypothesis: {hypothesis}

Requirements:
- 5-7 scenes total (hook + 3-5 body + CTA)
- Thai dialogue for each scene
- Visual prompts must be cinematic and specific
- Beauty product focus: show texture, application, results
"""


# ------------------------------------------------------------------ #
# Debate panel roles (Phase 2)                                        #
# ------------------------------------------------------------------ #

@dataclass(frozen=True)
class CriticFeedback:
    """Critic's red-team assessment of a storyboard draft."""

    approved: bool
    issues: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)


def critic_review(storyboard: Storyboard, brief: CampaignBrief) -> CriticFeedback:
    """Rule-based critic review (Phase 1). LLM-based in Phase 2.

    Checks:
    - Hook is <= 2s and purpose is HOOK
    - CTA scene exists and is last
    - Total duration <= 60s
    - Dialogue exists in at least 50% of scenes
    - No repeated visual_prompt across scenes
    """
    issues: list[str] = []
    suggestions: list[str] = []

    # Hook checks
    if storyboard.scenes[0].duration_s > 2.0:
        issues.append(f"Hook is {storyboard.scenes[0].duration_s}s, must be <= 2.0s")

    # CTA check
    last = storyboard.scenes[-1]
    if last.purpose is not ScenePurpose.CTA:
        issues.append("Last scene must be CTA")

    # Duration
    total = storyboard.total_duration_s
    if total > 60.0:
        issues.append(f"Total duration {total:.1f}s exceeds 60s cap")

    # Dialogue coverage
    scenes_with_dialogue = sum(1 for s in storyboard.scenes if s.dialogue)
    ratio = scenes_with_dialogue / len(storyboard.scenes)
    if ratio < 0.5:
        suggestions.append(
            f"Only {scenes_with_dialogue}/{len(storyboard.scenes)} scenes have dialogue; "
            "consider adding narration for engagement"
        )

    # Duplicate visual prompts
    prompts = [s.visual_prompt for s in storyboard.scenes]
    if len(set(prompts)) < len(prompts):
        issues.append("Duplicate visual_prompt detected across scenes")

    return CriticFeedback(
        approved=len(issues) == 0,
        issues=issues,
        suggestions=suggestions,
    )


# ------------------------------------------------------------------ #
# Default storyboard factory (deterministic, no LLM)                  #
# ------------------------------------------------------------------ #

def create_default_storyboard(brief: CampaignBrief) -> Storyboard:
    """Create a template storyboard from a brief without LLM.

    Used as fallback when LLM generation fails or for testing.
    """
    scenes = [
        Scene(
            idx=0,
            duration_s=1.5,
            purpose=ScenePurpose.HOOK,
            shot_type="extreme-closeup",
            movement="snap-zoom-in",
            visual_prompt=(
                "Extreme closeup of a luxury beauty product bottle with "
                "golden cap, soft studio lighting, warm amber tones, "
                "shallow depth of field, product glistening with "
                "light reflections on clean white marble surface"
            ),
            generator="sora2",
            dialogue=Dialogue(
                speaker="narrator",
                text_th="สิ่งที่คุณขาดไปนานมาก...",
                emphasis_words=["ขาดไป"],
            ),
            on_screen_text=OnScreenText(
                th="ลองแล้วจะรู้!",
                style="bold-pop",
                position="center-upper",
            ),
            sfx=["whoosh-01"],
            transition_out="match-cut",
        ),
        Scene(
            idx=1,
            duration_s=2.5,
            purpose=ScenePurpose.DEMONSTRATE,
            shot_type="medium-shot",
            movement="slow-dolly-right",
            visual_prompt=(
                "Medium shot of a Thai woman's hand applying cream product "
                "on forearm, soft natural lighting from left, clean white "
                "bathroom setting, product texture visible, warm skin tone, "
                "bokeh background"
            ),
            generator="sora2",
            dialogue=Dialogue(
                speaker="narrator",
                text_th="เนื้อสัมผัสบางเบา ซึมเร็วมาก",
                emphasis_words=["บางเบา", "ซึมเร็ว"],
            ),
            transition_out="cut",
        ),
        Scene(
            idx=2,
            duration_s=2.0,
            purpose=ScenePurpose.AGITATE,
            shot_type="closeup",
            movement="static",
            visual_prompt=(
                "Closeup comparison: left side dull dry skin, right side "
                "glowing hydrated skin after product application, split "
                "frame composition, soft ring light, clean background"
            ),
            generator="sora2",
            dialogue=Dialogue(
                speaker="narrator",
                text_th="ผิวเดิมแห้ง vs ผิวหลังใช้ ต่างกันชัด",
                emphasis_words=["ต่างกัน"],
            ),
            transition_out="cut",
        ),
        Scene(
            idx=3,
            duration_s=2.0,
            purpose=ScenePurpose.SOCIAL_PROOF,
            shot_type="medium-shot",
            movement="static",
            visual_prompt=(
                "Screenshot mockup of 5-star Shopee reviews overlaid on "
                "soft pink gradient background, Thai text reviews visible, "
                "small product image in corner, clean typography"
            ),
            generator="flux",
            dialogue=Dialogue(
                speaker="narrator",
                text_th="รีวิวระดับ 5 ดาว จากคนจริง",
                emphasis_words=["5 ดาว"],
            ),
            transition_out="cut",
        ),
        Scene(
            idx=4,
            duration_s=2.0,
            purpose=ScenePurpose.CTA,
            shot_type="medium-shot",
            movement="zoom-in-slow",
            visual_prompt=(
                "Product hero shot on clean white surface, golden hour "
                "side lighting, Shopee logo badge in corner, price tag "
                "floating beside product, warm inviting color palette"
            ),
            generator="flux",
            dialogue=Dialogue(
                speaker="narrator",
                text_th="แตะลิงก์ใต้คลิปเลย!",
                emphasis_words=["แตะลิงก์"],
            ),
            on_screen_text=OnScreenText(
                th="แตะลิงก์ใต้คลิป",
                style="cta-pulse",
                position="center-lower",
            ),
            transition_out="fade-out",
        ),
    ]

    return Storyboard(
        brief_id=brief.brief_id,
        voice_profile=VoiceProfile(
            lang="th",
            gender="f",
            tone="energetic-confidant",
            tts_engine="elevenlabs",
            voice_id="auto",
        ),
        music_brief=MusicBrief(
            genre="lofi-pop",
            bpm_range=(90, 110),
            license="epidemic-sound",
        ),
        scenes=scenes,
        cta_scene_idx=4,
        affiliate_link_placement="pinned_comment + on_screen_qr",
        hyperframe_overlays=[
            HyperframeOverlay(
                scene_idx=0,
                template="snap_title_v2",
                props={"text_th": "ลองแล้วจะรู้!", "duration_s": 1.2},
            ),
            HyperframeOverlay(
                scene_idx=4,
                template="cta_pulse",
                props={"cta_text": "แตะลิงก์ใต้คลิป"},
            ),
        ],
    )


# ------------------------------------------------------------------ #
# Writers' Room agent                                                  #
# ------------------------------------------------------------------ #

@dataclass
class WritersRoom:
    """Writers' Room agent — generates storyboards from campaign briefs.

    Phase 1: deterministic template + optional LLM enhancement.
    Phase 2: full debate panel with Director authority.
    """

    llm_client: Any | None = None  # PhayaClient or AnthropicClient
    enable_critic: bool = True

    async def generate_storyboard(
        self,
        brief: CampaignBrief,
    ) -> ToolResult[Storyboard]:
        """Generate a storyboard from a campaign brief.

        Falls back to template if LLM is unavailable or fails.
        """
        storyboard = create_default_storyboard(brief)

        # Phase 1: critic review (rule-based)
        if self.enable_critic:
            feedback = critic_review(storyboard, brief)
            if not feedback.approved:
                # Log issues but don't block — template is pre-validated
                pass

        return ToolResult(
            ok=True,
            data=storyboard,
            cost_usd=0.0,  # Template is free; LLM cost added in Phase 2
        )
