"""Tests for the music license validation gate (AFFI-T-030)."""

from __future__ import annotations

import pytest

from auto_affi.agents.music_license import (
    LicenseType,
    LicensedTrack,
    MusicLicenseRegistry,
)


# ------------------------------------------------------------------ #
# LicensedTrack schema tests                                          #
# ------------------------------------------------------------------ #


class TestLicensedTrack:
    """LicensedTrack schema validation."""

    @pytest.mark.unit
    def test_valid_track(self) -> None:
        track = LicensedTrack(
            track_id="T-001",
            title="Test Track",
            license_type=LicenseType.ROYALTY_FREE,
            source="Test Library",
        )
        assert track.track_id == "T-001"

    @pytest.mark.unit
    def test_rejects_empty_id(self) -> None:
        with pytest.raises(ValueError):
            LicensedTrack(
                track_id="",
                title="Test",
                license_type=LicenseType.ROYALTY_FREE,
            )

    @pytest.mark.unit
    def test_rejects_empty_title(self) -> None:
        with pytest.raises(ValueError):
            LicensedTrack(
                track_id="T-001",
                title="",
                license_type=LicenseType.ROYALTY_FREE,
            )

    @pytest.mark.unit
    def test_all_license_types(self) -> None:
        for lt in LicenseType:
            track = LicensedTrack(
                track_id=f"T-{lt.value}",
                title=f"Test {lt.value}",
                license_type=lt,
            )
            assert track.license_type == lt


# ------------------------------------------------------------------ #
# MusicLicenseRegistry tests                                          #
# ------------------------------------------------------------------ #


class TestMusicLicenseRegistry:
    """MusicLicenseRegistry validation logic."""

    @pytest.mark.unit
    def test_seed_library_loaded(self) -> None:
        registry = MusicLicenseRegistry()
        assert registry.track_count >= 5

    @pytest.mark.unit
    def test_is_licensed_known_track(self) -> None:
        registry = MusicLicenseRegistry()
        assert registry.is_licensed("ES-001") is True

    @pytest.mark.unit
    def test_is_licensed_unknown_track(self) -> None:
        registry = MusicLicenseRegistry()
        assert registry.is_licensed("PIRATE-001") is False

    @pytest.mark.unit
    def test_register_custom_track(self) -> None:
        registry = MusicLicenseRegistry()
        custom = LicensedTrack(
            track_id="CUSTOM-001",
            title="Custom Track",
            license_type=LicenseType.ORIGINAL,
        )
        registry.register(custom)
        assert registry.is_licensed("CUSTOM-001") is True
        assert registry.get_track("CUSTOM-001") is not None

    @pytest.mark.unit
    def test_get_track_returns_none_for_unknown(self) -> None:
        registry = MusicLicenseRegistry()
        assert registry.get_track("nonexistent") is None


# ------------------------------------------------------------------ #
# Storyboard music validation tests                                    #
# ------------------------------------------------------------------ #


class TestStoryboardMusicValidation:
    """validate_storyboard_music() gate logic."""

    @pytest.mark.unit
    def test_all_licensed_passes(self) -> None:
        registry = MusicLicenseRegistry()
        result = registry.validate_storyboard_music(["ES-001", "RF-001"])
        assert result.passed is True
        assert len(result.licensed_tracks) == 2
        assert len(result.violations) == 0

    @pytest.mark.unit
    def test_unlicensed_track_fails(self) -> None:
        registry = MusicLicenseRegistry()
        result = registry.validate_storyboard_music(["ES-001", "PIRATE-SONG"])
        assert result.passed is False
        assert "PIRATE-SONG" in result.unknown_tracks
        assert len(result.violations) == 1
        assert "hard block" in result.violations[0].lower()

    @pytest.mark.unit
    def test_all_unlicensed_fails(self) -> None:
        registry = MusicLicenseRegistry()
        result = registry.validate_storyboard_music(["BAD-1", "BAD-2"])
        assert result.passed is False
        assert len(result.violations) == 2

    @pytest.mark.unit
    def test_empty_refs_passes(self) -> None:
        """No music references = no violation (silent scenes OK)."""
        registry = MusicLicenseRegistry()
        result = registry.validate_storyboard_music([])
        assert result.passed is True

    @pytest.mark.unit
    def test_empty_string_refs_ignored(self) -> None:
        registry = MusicLicenseRegistry()
        result = registry.validate_storyboard_music(["", "ES-001", ""])
        assert result.passed is True
        assert len(result.licensed_tracks) == 1

    @pytest.mark.unit
    def test_mixed_licensed_and_unknown(self) -> None:
        registry = MusicLicenseRegistry()
        result = registry.validate_storyboard_music(
            ["ES-001", "ES-002", "UNKNOWN-X"]
        )
        assert result.passed is False
        assert len(result.licensed_tracks) == 2
        assert len(result.unknown_tracks) == 1

    @pytest.mark.unit
    def test_single_licensed_track(self) -> None:
        registry = MusicLicenseRegistry()
        result = registry.validate_storyboard_music(["AL-001"])
        assert result.passed is True
        assert result.licensed_tracks == ["AL-001"]
