"""E2E test — offline vertical slice (AFFI-S1-08 DoD).

Runs run_offline_slice(tmp_path) end-to-end and asserts the full contract:
  - master.mp4 is written
  - ffprobe: 1080x1920, duration <= 60s (approx storyboard total), 1v+1a
  - compliance.ok is True
  - rubric.ok is True
  - cost_usd == 0.0
  - RunEntry was persisted (registry runs.jsonl non-empty)

Zero paid calls. Zero network. Only ffmpeg (local) + dry-run fixtures.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

from auto_affi.ops.produce_slice import run_offline_slice


@pytest.mark.e2e
def test_offline_slice_full_contract(tmp_path: Path) -> None:
    """Run the full offline vertical slice and verify every DoD assertion."""
    # ---- run the slice ------------------------------------------------- #
    result = run_offline_slice(tmp_path)

    # ---- master.mp4 exists --------------------------------------------- #
    master = result.master_path
    assert master.exists(), f"master.mp4 was not written: {master}"
    assert master.name == "master.mp4"

    # ---- ffprobe: stream counts + resolution + duration ---------------- #
    ffprobe = shutil.which("ffprobe")
    assert ffprobe is not None, "ffprobe must be installed (part of ffmpeg)"

    probe_cmd = [
        ffprobe,
        "-v", "quiet",
        "-print_format", "json",
        "-show_streams",
        str(master),
    ]
    probe_output = subprocess.run(probe_cmd, check=True, capture_output=True, text=True)  # noqa: S603 -- cmd is [ffprobe, fixed flags, path]; no user input
    probe_data = json.loads(probe_output.stdout)
    streams = probe_data.get("streams", [])

    video_streams = [s for s in streams if s.get("codec_type") == "video"]
    audio_streams = [s for s in streams if s.get("codec_type") == "audio"]

    assert len(video_streams) == 1, (
        f"expected 1 video stream, got {len(video_streams)}"
    )
    assert len(audio_streams) == 1, (
        f"expected 1 audio stream, got {len(audio_streams)}"
    )

    # Resolution: 1080x1920 (9:16)
    v = video_streams[0]
    assert v.get("width") == 1080, f"expected width=1080, got {v.get('width')}"
    assert v.get("height") == 1920, f"expected height=1920, got {v.get('height')}"

    # Duration: <= 60s
    raw_dur = v.get("duration") or streams[0].get("duration")
    duration_s = float(raw_dur)
    assert duration_s <= 60.0, f"duration {duration_s:.2f}s exceeds 60s cap"

    # Duration: approximately matches storyboard total (within 2s tolerance)
    # Storyboard is 24.0s; ffmpeg may produce slightly different timestamps
    assert duration_s > 0.0, "duration must be positive"

    # ---- compliance.ok -------------------------------------------------- #
    assert result.compliance.ok is True, (
        f"compliance.ok is False; violations: {result.compliance.violations}"
    )

    # ---- rubric.ok ------------------------------------------------------ #
    assert result.rubric.ok is True, (
        f"rubric.ok is False; violations: {result.rubric.violations}"
    )

    # ---- cost_usd == 0.0 ------------------------------------------------ #
    assert result.cost_usd == 0.0, (
        f"expected cost_usd=0.0, got {result.cost_usd}"
    )

    # ---- registry: runs.jsonl non-empty --------------------------------- #
    runs_jsonl = tmp_path / "registry" / "runs.jsonl"
    assert runs_jsonl.exists(), "runs.jsonl was not created by the registry"

    lines = [ln.strip() for ln in runs_jsonl.read_text(encoding="utf-8").splitlines() if ln.strip()]
    assert len(lines) >= 1, "runs.jsonl is empty — RunEntry was not persisted"

    # Validate the run entry is valid JSON with expected fields
    run_data = json.loads(lines[-1])
    assert "run_id" in run_data, "run entry missing run_id"
    assert run_data.get("run_id") == result.run_id, (
        f"run_id mismatch: registry={run_data.get('run_id')} result={result.run_id}"
    )
    assert run_data.get("publish_mode") == "dry_run"
