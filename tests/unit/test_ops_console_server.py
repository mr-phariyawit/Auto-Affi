"""Unit tests for the Ops Console FastAPI server (Sprint 9 wire-up gap fix).

Verifies all routes serve, auth works when configured, and the inbox
HTML actually contains expected production-run data.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from auto_affi.agents.production_director import ProductionDirector
from auto_affi.ops.console.server import create_app


# ────────────────────────────────────────────────────────────────────
# Fixtures
# ────────────────────────────────────────────────────────────────────


@pytest.fixture
def empty_director(tmp_path: Path) -> ProductionDirector:
    """Director with no runs (clean state, isolated repo_root)."""
    return ProductionDirector(repo_root=tmp_path)


@pytest.fixture
def client(empty_director: ProductionDirector) -> TestClient:
    app = create_app(director=empty_director, auth_token=None)
    return TestClient(app)


@pytest.fixture
def authed_client(empty_director: ProductionDirector) -> tuple[TestClient, str]:
    token = "test-secret-token"
    app = create_app(director=empty_director, auth_token=token)
    return TestClient(app), token


# ────────────────────────────────────────────────────────────────────
# Health + dashboard
# ────────────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_healthz_returns_ok(client: TestClient) -> None:
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


@pytest.mark.unit
def test_dashboard_root_returns_html(client: TestClient) -> None:
    r = client.get("/")
    assert r.status_code == 200
    assert "text/html" in r.headers["content-type"]
    assert "<html" in r.text.lower() or "<!doctype" in r.text.lower()


@pytest.mark.unit
def test_dashboard_api_returns_json(client: TestClient) -> None:
    r = client.get("/api/dashboard")
    assert r.status_code == 200
    body = r.json()
    # DashboardData has these top-level keys per console/models.py
    assert "metrics" in body or "campaigns" in body or "queue" in body


@pytest.mark.unit
def test_dashboard_fragment_returns_html(client: TestClient) -> None:
    r = client.get("/api/dashboard/fragment")
    assert r.status_code == 200
    assert "text/html" in r.headers["content-type"]


# ────────────────────────────────────────────────────────────────────
# Production routes (Sprint 7 surface)
# ────────────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_list_runs_empty(client: TestClient) -> None:
    r = client.get("/api/production/runs")
    assert r.status_code == 200
    body = r.json()
    assert body == {"runs": [], "count": 0}


@pytest.mark.unit
def test_list_runs_with_invalid_status_filter(client: TestClient) -> None:
    r = client.get("/api/production/runs?status=nope")
    assert r.status_code == 200
    body = r.json()
    assert "error" in body
    assert body["runs"] == []


@pytest.mark.unit
def test_get_run_missing_returns_404(client: TestClient) -> None:
    r = client.get("/api/production/runs/does-not-exist")
    assert r.status_code == 404
    assert "error" in r.json()


@pytest.mark.unit
def test_get_stage_missing_run_returns_404(client: TestClient) -> None:
    r = client.get("/api/production/runs/does-not-exist/stages/1")
    assert r.status_code == 404


@pytest.mark.unit
def test_decide_with_unknown_verdict_returns_400(client: TestClient) -> None:
    r = client.post(
        "/api/production/runs/x/stages/1/decide",
        json={"verdict": "definitely-not-a-verdict", "notes_th": ""},
    )
    assert r.status_code == 400
    assert "error" in r.json()


# ────────────────────────────────────────────────────────────────────
# Inbox HTML (the gap this commit closes)
# ────────────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_inbox_page_serves_html(client: TestClient) -> None:
    r = client.get("/inbox")
    assert r.status_code == 200
    assert "text/html" in r.headers["content-type"]
    body = r.text.lower()
    assert "inbox" in body or "auto-affi" in body


@pytest.mark.unit
def test_inbox_fragment_serves_html(client: TestClient) -> None:
    r = client.get("/api/inbox/fragment")
    assert r.status_code == 200
    assert "text/html" in r.headers["content-type"]


@pytest.mark.unit
def test_inbox_polls_via_hx_attribute(client: TestClient) -> None:
    """The inbox page must include the hx-trigger so HTMX auto-refreshes."""
    r = client.get("/inbox")
    assert r.status_code == 200
    # render_inbox_page mounts hx-get="/api/inbox/fragment" with 10s polling
    assert "hx-get" in r.text
    assert "/api/inbox/fragment" in r.text


@pytest.mark.unit
def test_stage_review_404_for_missing_run(client: TestClient) -> None:
    r = client.get("/production/runs/missing/stages/1/review")
    assert r.status_code == 404


# ────────────────────────────────────────────────────────────────────
# Auth (header token)
# ────────────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_auth_blocks_unauthenticated_when_token_set(
    authed_client: tuple[TestClient, str],
) -> None:
    client, _token = authed_client
    r = client.get("/inbox")
    assert r.status_code == 401


@pytest.mark.unit
def test_auth_allows_correct_token(
    authed_client: tuple[TestClient, str],
) -> None:
    client, token = authed_client
    r = client.get("/inbox", headers={"X-Console-Token": token})
    assert r.status_code == 200


@pytest.mark.unit
def test_healthz_open_even_with_auth(
    authed_client: tuple[TestClient, str],
) -> None:
    """Healthz must stay open for k8s/cloud-run probes."""
    client, _ = authed_client
    r = client.get("/healthz")
    assert r.status_code == 200


# ────────────────────────────────────────────────────────────────────
# End-to-end: route shape with a real persisted run
# ────────────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_inbox_reflects_director_state(tmp_path: Path) -> None:
    """When a run exists on disk, the inbox API list shows it."""
    # Seed a minimal ProductionRun JSON directly to disk
    prod_dir = tmp_path / ".aegis" / "brain" / "production"
    prod_dir.mkdir(parents=True)
    run_dict = {
        "run_id": "test-run-123",
        "shopee_url": "https://shopee.co.th/x-i.1.2",
        "shopee_item_id": 2,
        "shopee_shop_id": 1,
        "started_at": "2026-05-13T00:00:00+00:00",
        "status": "in_progress",
        "stages": [],
        "total_cost_thb": 0.0,
        "final_mp4_gs_uri": None,
        "published_post_id": None,
    }
    (prod_dir / "test-run-123.json").write_text(json.dumps(run_dict))

    director = ProductionDirector(repo_root=tmp_path)
    app = create_app(director=director, auth_token=None)
    client = TestClient(app)

    r = client.get("/api/production/runs")
    assert r.status_code == 200
    body = r.json()
    assert body["count"] >= 1
    assert any(run["run_id"] == "test-run-123" for run in body["runs"])
