"""KlingProvider + RoutedGenProvider — kie.ai i2v behind the shared PGA gate.

The live ``_video_api`` is patched so no network is touched; the uploader is injected as a
fake. Mirrors test_gemini_provider.py's gate/verify-before-spend coverage for the Kling path.
"""

from __future__ import annotations

import asyncio
from pathlib import Path
from unittest.mock import patch

import pytest

from auto_affi.adapters.gen_provider import GenAsset, ProviderSpendError
from auto_affi.adapters.kling_provider import (
    KlingGenerationError,
    KlingProvider,
    _kling_duration,
    _kling_video_url,
    build_kling_body,
)
from auto_affi.adapters.routing_provider import RoutedGenProvider, build_default_provider
from auto_affi.pipeline.prompt_audit import (
    STAGES,
    GenerationBlocked,
    ReferenceManifest,
    audit,
    record_approval,
    record_audit,
    record_bypass,
)
from auto_affi.workflows.budget import BudgetCircuitBreaker

_IDENTITY = "JIAP02 lean athletic Southeast Asian male"


def _m(prompt: str = f"{_IDENTITY}, product orbit") -> ReferenceManifest:
    return ReferenceManifest(
        prompt=prompt, identity_string="JIAP02",
        cast_sheet_approved=True, objects_sheet_approved=True,
        declared_objects=["product"], scene_objects=["product"],
        face_reference_count=1, negative_prompt="different person, extra limbs",
        aspect="9:16", resolution="720p", duration_s=4.0, soul_id="soul-x",
    )


def _clear(run_dir: Path, stage: str, manifest: ReferenceManifest) -> None:
    for prior in STAGES[: STAGES.index(stage)]:
        record_bypass(run_dir, prior, reason="prior")
    record_audit(run_dir, stage, audit(manifest))
    record_approval(run_dir, stage, approved_by="op")


# --------------------------- pure builders / parsers --------------------- #


@pytest.mark.unit
def test_build_kling_body_shape() -> None:
    body = build_kling_body("kling-2.6/image-to-video", "a shot", "https://cdn/x.jpg", "5")
    assert body["model"] == "kling-2.6/image-to-video"
    inp = body["input"]
    assert inp["image_urls"] == ["https://cdn/x.jpg"]  # single public URL, list form
    assert inp["duration"] == "5"  # STRING, not int
    assert inp["sound"] is False  # silent — Thai VO muxed separately (no-lipsync)
    assert inp["prompt"] == "a shot"


@pytest.mark.unit
@pytest.mark.parametrize(("secs", "expected"), [(3, "5"), (4, "5"), (5, "5"), (7, "5"), (8, "10"), (10, "10")])
def test_kling_duration_maps_to_allowed_set(secs: int, expected: str) -> None:
    assert _kling_duration(secs) == expected


@pytest.mark.unit
def test_kling_video_url_parses_resultjson_string() -> None:
    data = {"state": "success", "resultJson": '{"resultUrls": ["https://tempfile/x.mp4"]}'}
    assert _kling_video_url(data) == "https://tempfile/x.mp4"


@pytest.mark.unit
def test_kling_video_url_missing_raises() -> None:
    with pytest.raises(KlingGenerationError, match="no video url"):
        _kling_video_url({"state": "success", "resultJson": '{"resultUrls": []}'})


# --------------------------- construction / key -------------------------- #


@pytest.mark.unit
def test_dry_run_does_not_require_key() -> None:
    KlingProvider(dry_run=True)  # offline, no key needed


@pytest.mark.unit
def test_live_provider_requires_key() -> None:
    with pytest.raises(ProviderSpendError, match="KIE_API_KEY"):
        KlingProvider(dry_run=False, api_key=None)


@pytest.mark.unit
def test_generate_image_is_rejected_video_only() -> None:
    p = KlingProvider(dry_run=True)
    with pytest.raises(ProviderSpendError, match="video-only"):
        asyncio.run(p.generate_image(stage="cast_sheet", prompt="x"))


# --------------------------- dry-run (offline/free) ---------------------- #


@pytest.mark.unit
def test_dry_run_video_is_free_stub_after_gate(tmp_path: Path) -> None:
    m = _m()
    _clear(tmp_path, "video", m)
    p = KlingProvider(dry_run=True)
    a = asyncio.run(p.generate_video(stage="video", prompt=m.prompt, run_dir=tmp_path, manifest=m, duration=4))
    assert isinstance(a, GenAsset) and a.kind == "video" and a.cost_usd == 0.0
    assert "kling" in a.raw and "5s" in a.raw  # 4s request -> Kling min 5s


@pytest.mark.unit
def test_video_blocked_without_approval(tmp_path: Path) -> None:
    p = KlingProvider(dry_run=True)
    with pytest.raises(GenerationBlocked):
        asyncio.run(p.generate_video(stage="video", prompt="x", run_dir=tmp_path, manifest=_m()))


# --------------------------- gate / verify-before-spend ------------------ #


def _patch_video(tmp_path: Path):
    async def fake_video(self, model, prompt, kdur, run_dir, stage, seed):
        return (run_dir or tmp_path) / f"{stage}.mp4"

    return patch.object(KlingProvider, "_video_api", fake_video)


@pytest.mark.unit
def test_live_requires_budget(tmp_path: Path) -> None:
    m = _m()
    _clear(tmp_path, "video", m)
    with _patch_video(tmp_path):
        p = KlingProvider(dry_run=False, api_key="k")
        with pytest.raises(ProviderSpendError, match="requires a BudgetCircuitBreaker"):
            asyncio.run(p.generate_video(stage="video", prompt=m.prompt, run_dir=tmp_path,
                                         manifest=m, reference_images=("https://cdn/s.jpg",)))


@pytest.mark.unit
def test_live_requires_seed_image(tmp_path: Path) -> None:
    m = _m()
    _clear(tmp_path, "video", m)
    with _patch_video(tmp_path):
        p = KlingProvider(dry_run=False, api_key="k")
        with pytest.raises(ProviderSpendError, match="requires a seed image"):
            asyncio.run(p.generate_video(stage="video", prompt=m.prompt, run_dir=tmp_path,
                                         manifest=m, budget=BudgetCircuitBreaker()))


@pytest.mark.unit
def test_live_video_short_clip_proceeds_and_spends(tmp_path: Path) -> None:
    m = _m()
    _clear(tmp_path, "video", m)
    breaker = BudgetCircuitBreaker()
    with _patch_video(tmp_path):
        p = KlingProvider(dry_run=False, api_key="k")
        a = asyncio.run(p.generate_video(stage="video", prompt=m.prompt, duration=5, run_dir=tmp_path,
                                         manifest=m, budget=breaker, reference_images=("https://cdn/s.jpg",)))
    assert a.kind == "video" and a.cost_usd == pytest.approx(0.275) and a.cost_estimated
    assert breaker.node_spent("video_gen") == pytest.approx(0.275)  # well under Veo's cost


# --------------------------- seed hosting (_to_url) ---------------------- #


@pytest.mark.unit
def test_to_url_passes_through_http() -> None:
    p = KlingProvider(dry_run=True)
    assert asyncio.run(p._to_url("https://cdn/x.jpg")) == "https://cdn/x.jpg"


@pytest.mark.unit
def test_to_url_local_without_uploader_raises() -> None:
    p = KlingProvider(dry_run=True)
    with pytest.raises(ProviderSpendError, match="no upload_image"):
        asyncio.run(p._to_url("seed.png"))


@pytest.mark.unit
def test_to_url_local_uses_injected_uploader() -> None:
    async def fake_upload(path: Path) -> str:
        return f"https://cdn/hosted/{path.name}"

    p = KlingProvider(dry_run=True, upload_image=fake_upload)
    assert asyncio.run(p._to_url("seed.png")) == "https://cdn/hosted/seed.png"


# --------------------------- RoutedGenProvider --------------------------- #


class _StubProvider:
    """Records which method fired; optionally raises a chosen error on video."""

    def __init__(self, tag: str, video_error: Exception | None = None) -> None:
        self.tag, self.video_error, self.calls = tag, video_error, []

    async def generate_image(self, **kw) -> GenAsset:
        self.calls.append("image")
        return GenAsset(kind="image", raw=self.tag)

    async def generate_video(self, **kw) -> GenAsset:
        self.calls.append("video")
        if self.video_error is not None:
            raise self.video_error
        return GenAsset(kind="video", raw=self.tag)


@pytest.mark.unit
def test_router_sends_images_to_image_provider() -> None:
    img, vid = _StubProvider("gemini"), _StubProvider("kling")
    r = RoutedGenProvider(image_provider=img, video_provider=vid)
    a = asyncio.run(r.generate_image(stage="cast_sheet", prompt="x"))
    assert a.raw == "gemini" and img.calls == ["image"] and vid.calls == []


@pytest.mark.unit
def test_router_sends_video_to_video_provider() -> None:
    img, vid = _StubProvider("gemini"), _StubProvider("kling")
    r = RoutedGenProvider(image_provider=img, video_provider=vid)
    a = asyncio.run(r.generate_video(stage="video", prompt="x"))
    assert a.raw == "kling" and vid.calls == ["video"]


@pytest.mark.unit
def test_router_falls_back_to_veo_on_kling_generation_error() -> None:
    vid = _StubProvider("kling", video_error=KlingGenerationError("boom"))
    fb = _StubProvider("veo-fallback")
    r = RoutedGenProvider(image_provider=_StubProvider("gemini"), video_provider=vid, video_fallback=fb)
    a = asyncio.run(r.generate_video(stage="video", prompt="x"))
    assert a.raw == "veo-fallback" and vid.calls == ["video"] and fb.calls == ["video"]


@pytest.mark.unit
def test_router_does_not_fall_back_on_spend_stop() -> None:
    # A budget/gate DENY must propagate — never "recovered" by spending on the pricier model.
    vid = _StubProvider("kling", video_error=ProviderSpendError("budget breaker DENY"))
    fb = _StubProvider("veo-fallback")
    r = RoutedGenProvider(image_provider=_StubProvider("gemini"), video_provider=vid, video_fallback=fb)
    with pytest.raises(ProviderSpendError, match="DENY"):
        asyncio.run(r.generate_video(stage="video", prompt="x"))
    assert fb.calls == []  # fallback NOT invoked


@pytest.mark.unit
def test_router_reraises_kling_error_when_no_fallback() -> None:
    vid = _StubProvider("kling", video_error=KlingGenerationError("boom"))
    r = RoutedGenProvider(image_provider=_StubProvider("gemini"), video_provider=vid)
    with pytest.raises(KlingGenerationError):
        asyncio.run(r.generate_video(stage="video", prompt="x"))


# --------------------------- factory wiring ------------------------------ #


@pytest.mark.unit
def test_factory_default_routes_video_to_kling_no_autofallback(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("AUTO_AFFI_VIDEO_MODEL", raising=False)
    prov = build_default_provider(dry_run=True)
    assert isinstance(prov, RoutedGenProvider)
    assert type(prov.video_provider).__name__ == "KlingProvider"
    assert type(prov.image_provider).__name__ == "GeminiProvider"
    assert prov.video_fallback is None  # model-lock gate: no silent fallback by default


@pytest.mark.unit
def test_factory_opt_in_veo_fallback(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("AUTO_AFFI_VIDEO_MODEL", raising=False)
    prov = build_default_provider(dry_run=True, allow_veo_fallback=True)
    assert isinstance(prov, RoutedGenProvider)
    assert type(prov.video_fallback).__name__ == "GeminiProvider"  # explicit override only


@pytest.mark.unit
def test_factory_veo_mode_returns_gemini_only(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AUTO_AFFI_VIDEO_MODEL", "veo")
    prov = build_default_provider(dry_run=True)
    assert type(prov).__name__ == "GeminiProvider"
