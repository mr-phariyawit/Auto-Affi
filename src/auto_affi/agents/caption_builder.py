"""Caption builder with mandatory ad disclosure enforcement.

Generates platform-specific captions for published affiliate videos.
Every caption MUST include:

  1. Ad disclosure markers per Thai OCPB rules (FR-PB-04)
  2. AI-generated content label per TikTok 2025 rule
  3. Affiliate link (subId-tagged Shopee deep link)
  4. Relevant hashtags from the CampaignBrief

Platform-specific rules:
  - IG Reels: #Ad + Thai disclosure in caption body
  - FB Reels: same as IG (shared Meta policy)
  - YT Shorts: paid promotion checkbox + caption disclosure
  - TikTok: AI label + #Ad (pending app approval)

The builder validates disclosure presence before returning. If a caption
is constructed without disclosure, it raises :class:`DisclosureError`
rather than silently shipping a non-compliant caption.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Final

from pydantic import BaseModel, Field, model_validator


class Platform(StrEnum):
    """Supported publishing platforms."""

    IG = "ig"
    FB = "fb"
    YT = "yt"
    TK = "tk"


# Thai disclosure markers — at least one MUST appear in every caption.
# These come from OCPB guidelines + Shopee affiliate ToS.
THAI_DISCLOSURE_MARKERS: Final[frozenset[str]] = frozenset(
    {
        "#โฆษณา",
        "#ad",
        "#affiliate",
        "โฆษณา",
        "ได้รับค่าตอบแทน",
        "มีค่าคอมมิชชั่น",
        "paid partnership",
        "sponsored",
    }
)

# AI-generated content labels per TikTok 2025 mandatory rule.
AI_LABELS: Final[frozenset[str]] = frozenset(
    {
        "#AIGenerated",
        "#AIสร้าง",
        "สร้างด้วย AI",
    }
)


class DisclosureError(ValueError):
    """Raised when a caption lacks mandatory ad disclosure."""


class CaptionInput(BaseModel):
    """Everything needed to build a caption for one platform."""

    platform: Platform
    product_name: str = Field(min_length=1, max_length=200)
    hook_text_th: str = Field(min_length=1, max_length=300)
    affiliate_link: str = Field(min_length=1)
    hashtags: list[str] = Field(default_factory=list, max_length=15)
    cta_text_th: str = Field(default="แตะลิงก์ใต้คลิปเลย")


class Caption(BaseModel):
    """Built caption ready for publishing."""

    platform: Platform
    text: str = Field(min_length=1)
    has_disclosure: bool
    has_ai_label: bool
    hashtag_count: int = Field(ge=0)

    @model_validator(mode="after")
    def _must_have_disclosure(self) -> Caption:
        if not self.has_disclosure:
            raise DisclosureError(
                f"Caption for {self.platform} missing ad disclosure. "
                "Every caption MUST include at least one disclosure marker."
            )
        return self


# Platform-specific disclosure templates.
_PLATFORM_TEMPLATES: dict[Platform, str] = {
    Platform.IG: (
        "{hook}\n\n"
        "{product_name}\n"
        "{cta}\n"
        "{link}\n\n"
        "{hashtags}\n"
        "#โฆษณา #affiliate #AIGenerated"
    ),
    Platform.FB: (
        "{hook}\n\n"
        "{product_name}\n"
        "{cta}\n"
        "{link}\n\n"
        "{hashtags}\n"
        "#โฆษณา #affiliate #AIGenerated"
    ),
    Platform.YT: (
        "{hook}\n\n"
        "{product_name}\n"
        "{cta}\n"
        "{link}\n\n"
        "ได้รับค่าตอบแทนจากลิงก์ affiliate\n"
        "{hashtags} #Shorts #AIGenerated"
    ),
    Platform.TK: (
        "{hook}\n\n"
        "{product_name}\n"
        "{cta}\n"
        "{link}\n\n"
        "{hashtags}\n"
        "#โฆษณา #ad #AIสร้าง #AIGenerated"
    ),
}


def build_caption(inp: CaptionInput) -> Caption:
    """Build a platform-specific caption with mandatory disclosure.

    Raises :class:`DisclosureError` if the result somehow lacks disclosure
    (should never happen with the built-in templates, but the validator
    catches custom overrides or template bugs).
    """
    # Format hashtags.
    formatted_tags = " ".join(
        f"#{tag.lstrip('#')}" for tag in inp.hashtags if tag.strip()
    )

    template = _PLATFORM_TEMPLATES[inp.platform]
    text = template.format(
        hook=inp.hook_text_th,
        product_name=inp.product_name,
        cta=inp.cta_text_th,
        link=inp.affiliate_link,
        hashtags=formatted_tags,
    )

    # Clean up multiple blank lines.
    while "\n\n\n" in text:
        text = text.replace("\n\n\n", "\n\n")
    text = text.strip()

    # Validate disclosure presence.
    text_lower = text.lower()
    has_disclosure = any(
        marker.lower() in text_lower for marker in THAI_DISCLOSURE_MARKERS
    )
    has_ai_label = any(
        label.lower() in text_lower for label in AI_LABELS
    )

    return Caption(
        platform=inp.platform,
        text=text,
        has_disclosure=has_disclosure,
        has_ai_label=has_ai_label,
        hashtag_count=text.count("#"),
    )


def validate_disclosure(text: str) -> bool:
    """Check if arbitrary text contains at least one disclosure marker.

    Convenience function for the Safety gate to validate captions
    produced by non-standard flows.
    """
    text_lower = text.lower()
    return any(
        marker.lower() in text_lower for marker in THAI_DISCLOSURE_MARKERS
    )
