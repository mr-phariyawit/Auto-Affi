"""Shared pytest fixtures."""

from __future__ import annotations

import pytest


@pytest.fixture(autouse=True)
def _isolate_settings_cache() -> None:
    """Clear lru_cache on Settings between tests so env mutations apply."""
    from auto_affi.config.settings import get_settings

    get_settings.cache_clear()
