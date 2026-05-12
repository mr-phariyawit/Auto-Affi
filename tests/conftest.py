"""Shared pytest fixtures."""

from __future__ import annotations

import pytest

from auto_affi.config.settings import get_settings


@pytest.fixture(autouse=True)
def _isolate_settings_cache() -> None:
    """Clear lru_cache on Settings between tests so env mutations apply."""
    get_settings.cache_clear()
