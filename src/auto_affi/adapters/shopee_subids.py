"""SubId taxonomy for Shopee affiliate deep links.

Shopee preserves up to 5 free-form ``subIds[0..4]`` slots through every
``generateShortLink`` call. We use them to attribute conversions back to
the exact creative variant, per execution-playbook §5.3:

    subId[0] = platform           (tk | ig | yt | fb)
    subId[1] = account_handle     (@handle or hash)
    subId[2] = video_id           (campaign-stamped UUID short)
    subId[3] = campaign_id        (UUID short)
    subId[4] = variant            (A | B | C | ...)
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator

Platform = Literal["tk", "ig", "yt", "fb"]

# Shopee subId slots are short — keep each value within a reasonable bound so
# the resulting deep link stays clean and tracking joins remain stable.
_MAX_SLOT_LEN = 64


class SubIds(BaseModel):
    """The 5-slot Shopee subId taxonomy."""

    platform: Platform
    account: str = Field(min_length=1, max_length=_MAX_SLOT_LEN)
    video_id: str = Field(min_length=1, max_length=_MAX_SLOT_LEN)
    campaign_id: str = Field(min_length=1, max_length=_MAX_SLOT_LEN)
    variant: str = Field(min_length=1, max_length=_MAX_SLOT_LEN, default="A")

    @field_validator("account", "video_id", "campaign_id", "variant")
    @classmethod
    def _no_pipe(cls, value: str) -> str:
        if "|" in value:
            raise ValueError("subId slot must not contain '|' (reserved separator)")
        return value

    def to_list(self) -> list[str]:
        """Return the 5 slots in canonical order for the Shopee API call."""
        return [self.platform, self.account, self.video_id, self.campaign_id, self.variant]

    @classmethod
    def from_list(cls, slots: list[str]) -> SubIds:
        """Inverse of ``to_list``; tolerant of trailing empties from the API."""
        padded = (slots + [""] * 5)[:5]
        platform, account, video_id, campaign_id, variant = padded
        return cls(
            platform=platform,  # type: ignore[arg-type]
            account=account,
            video_id=video_id,
            campaign_id=campaign_id,
            variant=variant or "A",
        )
