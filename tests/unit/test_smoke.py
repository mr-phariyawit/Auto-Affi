"""AFFI-S1-01 baseline: the rebuilt package imports and exposes a version."""

import pytest

import auto_affi


@pytest.mark.unit
def test_package_imports() -> None:
    assert auto_affi.__version__ == "0.1.0"
