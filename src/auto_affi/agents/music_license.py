"""Music license validation gate (FR-SF-02).

Every storyboard scene's music reference must be from a licensed library.
Unlicensed or unknown tracks are hard-blocked before publishing.

Integrates into the pre-publish safety gate (AFFI-T-029) as an
additional check alongside claim audit, brand blocklist, and NSFW.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from pydantic import BaseModel, Field

# ------------------------------------------------------------------ #
# Licensed track registry                                             #
# ------------------------------------------------------------------ #

class LicenseType(StrEnum):
    """Type of music license."""

    ROYALTY_FREE = "royalty_free"
    EPIDEMIC_SOUND = "epidemic_sound"
    ARTLIST = "artlist"
    CREATIVE_COMMONS = "creative_commons"
    ORIGINAL = "original"


class LicensedTrack(BaseModel):
    """A track in the licensed music library."""

    track_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    license_type: LicenseType
    source: str = Field(default="", description="Library or provider name")
    genre: str = ""
    bpm: int = Field(ge=0, default=0)


# Seed library — production would load from database or API
_SEED_LIBRARY: list[LicensedTrack] = [
    LicensedTrack(
        track_id="ES-001",
        title="Upbeat Pop Energy",
        license_type=LicenseType.EPIDEMIC_SOUND,
        source="Epidemic Sound",
        genre="pop",
        bpm=120,
    ),
    LicensedTrack(
        track_id="ES-002",
        title="Lofi Chill Vibes",
        license_type=LicenseType.EPIDEMIC_SOUND,
        source="Epidemic Sound",
        genre="lofi",
        bpm=85,
    ),
    LicensedTrack(
        track_id="RF-001",
        title="Corporate Motivational",
        license_type=LicenseType.ROYALTY_FREE,
        source="Pixabay Music",
        genre="corporate",
        bpm=110,
    ),
    LicensedTrack(
        track_id="RF-002",
        title="Beauty Tutorial Background",
        license_type=LicenseType.ROYALTY_FREE,
        source="Pixabay Music",
        genre="ambient",
        bpm=90,
    ),
    LicensedTrack(
        track_id="AL-001",
        title="Trendy Fashion Beat",
        license_type=LicenseType.ARTLIST,
        source="Artlist",
        genre="electronic",
        bpm=128,
    ),
]


class ValidationResult(BaseModel):
    """Result of music license validation for a storyboard."""

    passed: bool
    licensed_tracks: list[str] = Field(default_factory=list)
    unlicensed_tracks: list[str] = Field(default_factory=list)
    unknown_tracks: list[str] = Field(default_factory=list)
    violations: list[str] = Field(default_factory=list)


@dataclass
class MusicLicenseRegistry:
    """Registry of licensed music tracks.

    Validates that storyboard music references are from licensed sources.
    Unlicensed or unknown tracks result in a hard block.
    """

    _tracks: dict[str, LicensedTrack] = field(default_factory=dict)

    def __post_init__(self) -> None:
        # Load seed library
        for track in _SEED_LIBRARY:
            self._tracks[track.track_id] = track

    def register(self, track: LicensedTrack) -> None:
        """Register a licensed track."""
        self._tracks[track.track_id] = track

    def is_licensed(self, track_id: str) -> bool:
        """Check if a track ID is in the licensed registry."""
        return track_id in self._tracks

    def get_track(self, track_id: str) -> LicensedTrack | None:
        """Look up a track by ID."""
        return self._tracks.get(track_id)

    @property
    def track_count(self) -> int:
        return len(self._tracks)

    def validate_storyboard_music(
        self,
        music_refs: list[str],
    ) -> ValidationResult:
        """Validate all music references in a storyboard.

        Args:
            music_refs: List of track IDs referenced in storyboard scenes.

        Returns:
            ValidationResult with pass/fail and per-track details.
        """
        if not music_refs:
            # No music = no violation (some scenes may be silent)
            return ValidationResult(passed=True)

        licensed: list[str] = []
        unlicensed: list[str] = []
        unknown: list[str] = []
        violations: list[str] = []

        for ref in music_refs:
            if not ref:
                continue
            if self.is_licensed(ref):
                licensed.append(ref)
            else:
                unknown.append(ref)
                violations.append(
                    f"Track '{ref}' not found in licensed library — hard block"
                )

        passed = len(violations) == 0

        return ValidationResult(
            passed=passed,
            licensed_tracks=licensed,
            unlicensed_tracks=unlicensed,
            unknown_tracks=unknown,
            violations=violations,
        )
