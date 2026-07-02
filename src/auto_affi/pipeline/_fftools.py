"""Shared ffmpeg/ffprobe binary-presence checks (used by cleanroom + dry_render)."""

from __future__ import annotations

import shutil


def require_binary(name: str, hint: str) -> str:
    """Return the path to *name* on PATH, or raise RuntimeError with *hint* if absent."""
    binary = shutil.which(name)
    if binary is None:
        raise RuntimeError(f"{name} is not installed or not on PATH. {hint}")
    return binary
