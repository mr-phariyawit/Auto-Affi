"""Unit tests for the PGA gate CLI (out-of-pipeline routes such as the Higgsfield UI operator)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from auto_affi.ops import gate_cli
from auto_affi.pipeline.prompt_audit import STAGES

_IDENTITY = "JIAB01, Southeast Asian male host, medium-long wavy hair"


def _manifest(path: Path, **overrides: object) -> Path:
    base: dict[str, object] = {
        "prompt": f"{_IDENTITY}. @jiab lifts @serum to chest height.",
        "identity_string": _IDENTITY,
        "stage_kind": "character",
        "prompt_mode": "video_gen",
        "cast_sheet_approved": True,
        "objects_sheet_approved": True,
        "declared_objects": ["serum bottle"],
        "scene_objects": ["serum bottle"],
        "face_reference_count": 1,
        "reference_uris": ["higgsfield:element/@jiab", "higgsfield:element/@serum"],
        "negative_prompt": "different person, extra hands, garbled label, text, watermark",
        "aspect": "9:16",
        "resolution": "1080p",
        "duration_s": 15.0,
        "max_duration_s": 15.0,
        "soul_id": "@jiab",
    }
    base.update(overrides)
    path.write_text(json.dumps(base), encoding="utf-8")
    return path


def _run(*args: str) -> int:
    return gate_cli.main(list(args))


def _approve_chain(run: Path, manifest: Path, upto: str = "video") -> None:
    for stage in STAGES[: STAGES.index(upto) + 1]:
        assert _run("audit", "--run", str(run), "--stage", stage, "--manifest", str(manifest)) == 0
        assert _run("approve", "--run", str(run), "--stage", stage, "--by", "human:test") == 0


def test_audit_pass_and_fail(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    good = _manifest(tmp_path / "m.json")
    assert _run("audit", "--run", str(tmp_path), "--stage", "cast_sheet", "--manifest", str(good)) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["passed"] is True and len(out["prompt_hash"]) == 64
    bad = _manifest(tmp_path / "bad.json", aspect="16:9")
    assert _run("audit", "--run", str(tmp_path), "--stage", "cast_sheet", "--manifest", str(bad)) == 1
    assert "ASPECT" in capsys.readouterr().out.upper()


def test_check_blocked_until_whole_chain_approved(tmp_path: Path) -> None:
    m = _manifest(tmp_path / "m.json")
    assert _run("check", "--run", str(tmp_path), "--stage", "video", "--manifest", str(m)) == 3
    _approve_chain(tmp_path, m, upto="contact_sheet")
    assert _run("check", "--run", str(tmp_path), "--stage", "video", "--manifest", str(m)) == 3
    _approve_chain(tmp_path, m)
    assert _run("check", "--run", str(tmp_path), "--stage", "video", "--manifest", str(m)) == 0


def test_changed_prompt_after_approval_is_blocked(tmp_path: Path) -> None:
    m = _manifest(tmp_path / "m.json")
    _approve_chain(tmp_path, m)
    edited = _manifest(tmp_path / "edited.json", prompt=f"{_IDENTITY}. @jiab spins @serum.")
    assert _run("check", "--run", str(tmp_path), "--stage", "video", "--manifest", str(edited)) == 3


def test_approve_requires_passing_audit(tmp_path: Path) -> None:
    assert _run("approve", "--run", str(tmp_path), "--stage", "cast_sheet", "--by", "human:test") == 3


def test_bypass_needs_reason_and_is_recorded(tmp_path: Path) -> None:
    with pytest.raises(SystemExit):
        _run("bypass", "--run", str(tmp_path), "--stage", "cast_sheet")
    assert _run("bypass", "--run", str(tmp_path), "--stage", "cast_sheet", "--reason", "reuse locked sheet",
                "--by", "human:test") == 0
    events = (tmp_path / "audit_events.jsonl").read_text().splitlines()
    assert json.loads(events[-1])["event"] == "bypass"


def test_spend_is_fail_closed_without_budget(tmp_path: Path) -> None:
    assert _run("spend", "--run", str(tmp_path), "--credits", "10") == 4


def test_spend_cap_and_ledger(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert _run("budget", "--run", str(tmp_path), "--max-credits", "100", "--by", "human:test") == 0
    assert _run("spend", "--run", str(tmp_path), "--credits", "60") == 0
    assert _run("spend", "--run", str(tmp_path), "--credits", "60", "--commit", "--label", "shot01 take1",
                "--route", "ui", "--model", "seedance-2.0") == 0
    assert _run("spend", "--run", str(tmp_path), "--credits", "50") == 4
    budget = json.loads((tmp_path / "credits.json").read_text())
    assert budget["spent_credits"] == 60
    entry = json.loads((tmp_path / "ledger.jsonl").read_text().splitlines()[-1])
    assert entry["credits"] == 60 and entry["label"] == "shot01 take1" and entry["route"] == "ui"


def test_preflight_needs_gate_and_budget(tmp_path: Path) -> None:
    m = _manifest(tmp_path / "m.json")
    _approve_chain(tmp_path, m)
    args = ("preflight", "--run", str(tmp_path), "--stage", "video", "--manifest", str(m), "--credits", "40")
    assert _run(*args) == 4  # gate passes, no budget yet
    _run("budget", "--run", str(tmp_path), "--max-credits", "100", "--by", "human:test")
    assert _run(*args) == 0
    edited = _manifest(tmp_path / "e.json", resolution="4k")
    assert _run("preflight", "--run", str(tmp_path), "--stage", "video", "--manifest", str(edited),
                "--credits", "40") == 3


def test_status_summarises_run(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    m = _manifest(tmp_path / "m.json")
    _approve_chain(tmp_path, m, upto="cast_sheet")
    capsys.readouterr()
    assert _run("status", "--run", str(tmp_path)) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["stages"]["cast_sheet"]["approved"] is True
    assert out["stages"]["video"]["approved"] is False


def test_refund_returns_credits(tmp_path: Path) -> None:
    _run("budget", "--run", str(tmp_path), "--max-credits", "100", "--by", "human:test")
    _run("spend", "--run", str(tmp_path), "--credits", "80", "--commit", "--label", "take1")
    assert _run("spend", "--run", str(tmp_path), "--credits", "50") == 4
    assert _run("spend", "--run", str(tmp_path), "--credits", "80", "--refund", "--label", "take1 failed, refunded") == 0
    assert json.loads((tmp_path / "credits.json").read_text())["spent_credits"] == 0
    assert _run("spend", "--run", str(tmp_path), "--credits", "50") == 0
