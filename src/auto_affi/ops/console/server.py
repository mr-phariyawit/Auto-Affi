"""Ops Console FastAPI server — wires dashboard + production + inbox routes.

Closes the Sprint 9 wire-up gap: ``app.py`` (dashboard service),
``production_routes.py`` (ADR-007 production handler), and ``inbox.py``
(HTMX render functions) all exist but were never bound to an actual
ASGI application. This module is that application.

Launch:
    .venv/bin/python -m auto_affi.ops.console           # uvicorn on :8000
    .venv/bin/python -m auto_affi.ops.console --port 4321 --host 0.0.0.0

Routes:
    Dashboard (existing app.py):
        GET  /                                — HTMX dashboard HTML
        GET  /api/dashboard                   — DashboardData JSON
        GET  /api/dashboard/fragment          — HTMX fragment poll target

    Production workflow (ADR-007, Sprint 7 production_routes.py):
        GET  /api/production/runs?status=…    — list runs
        GET  /api/production/runs/{id}        — run detail
        GET  /api/production/runs/{id}/stages/{n}            — stage detail
        POST /api/production/runs/{id}/stages/{n}/decide     — apply verdict

    Inbox + stage review (Sprint 8 inbox.py — newly mounted):
        GET  /inbox                           — full HTMX inbox HTML
        GET  /api/inbox/fragment              — HTMX 10s-poll fragment
        GET  /production/runs/{id}/stages/{n}/review  — stage review HTML

Auth: single shared-secret header for Phase 1 (env
``AUTO_AFFI__OPS_CONSOLE_TOKEN``). When unset, all routes are open
(dev only; never deploy unset). Phase 2 hardens to OIDC.
"""

from __future__ import annotations

import argparse
import os
from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

from auto_affi.agents.production_director import ProductionDirector
from auto_affi.ops.console.app import (
    DashboardService,
    get_dashboard_html,
    render_dashboard_fragment,
)
from auto_affi.ops.console.inbox import (
    render_inbox_fragment,
    render_inbox_page,
    render_stage_review_page,
)
from auto_affi.ops.console.production_routes import ProductionRouteHandler
from auto_affi.schemas.production import ProductionRunStatus


# ────────────────────────────────────────────────────────────────────
# Request models for decide endpoint
# ────────────────────────────────────────────────────────────────────


class DecideRequest(BaseModel):
    verdict: str  # "approve" | "revise" | "reject"
    notes_th: str = ""
    decided_by: str = "board"


# ────────────────────────────────────────────────────────────────────
# Singletons
# ────────────────────────────────────────────────────────────────────


def _build_director() -> ProductionDirector:
    """Default director — reads/writes .aegis/brain/production/ from CWD."""
    return ProductionDirector()


def _build_dashboard_service() -> DashboardService:
    return DashboardService()


# ────────────────────────────────────────────────────────────────────
# App factory
# ────────────────────────────────────────────────────────────────────


def create_app(
    *,
    director: ProductionDirector | None = None,
    dashboard: DashboardService | None = None,
    auth_token: str | None = None,
) -> FastAPI:
    """Build a FastAPI app with the production workflow + dashboard routes.

    Tests inject lightweight director / dashboard fixtures; production
    boots them from defaults. ``auth_token`` defaults to the env var
    ``AUTO_AFFI__OPS_CONSOLE_TOKEN``; when None/empty, auth is bypassed
    (dev only).
    """
    director = director or _build_director()
    dashboard = dashboard or _build_dashboard_service()
    handler = ProductionRouteHandler(director=director)
    if auth_token is None:
        auth_token = os.environ.get("AUTO_AFFI__OPS_CONSOLE_TOKEN", "") or None

    app = FastAPI(
        title="Auto-Affi Ops Console",
        version="1.0.0",
        description="Studio workflow + dashboard for Phase 1 supervisor ops",
    )

    # ── Auth dependency (no-op when token unset) ─────────────────────
    def _require_token(
        x_console_token: Annotated[str | None, Header(alias="X-Console-Token")] = None,
    ) -> None:
        if auth_token is None:
            return
        if x_console_token != auth_token:
            raise HTTPException(status_code=401, detail="invalid console token")

    auth = Depends(_require_token)

    # ── Dashboard routes (existing surface) ──────────────────────────

    @app.get("/", response_class=HTMLResponse, dependencies=[auth])
    def dashboard_page() -> str:
        return get_dashboard_html()

    @app.get("/api/dashboard", dependencies=[auth])
    def dashboard_data() -> JSONResponse:
        return JSONResponse(dashboard.get_dashboard().model_dump(mode="json"))

    @app.get("/api/dashboard/fragment", response_class=HTMLResponse, dependencies=[auth])
    def dashboard_fragment() -> str:
        return render_dashboard_fragment(dashboard.get_dashboard())

    # ── Production workflow routes (Sprint 7) ────────────────────────

    @app.get("/api/production/runs", dependencies=[auth])
    def list_runs(
        status: Annotated[str | None, Query(description="Filter by run status")] = None,
    ) -> JSONResponse:
        return JSONResponse(handler.list_runs(status=status))

    @app.get("/api/production/runs/{run_id}", dependencies=[auth])
    def get_run(run_id: str) -> JSONResponse:
        result = handler.get_run(run_id)
        status = 404 if "error" in result else 200
        return JSONResponse(result, status_code=status)

    @app.get("/api/production/runs/{run_id}/stages/{stage_id}", dependencies=[auth])
    def get_stage(run_id: str, stage_id: int) -> JSONResponse:
        result = handler.get_stage(run_id, stage_id)
        status = 404 if "error" in result else 200
        return JSONResponse(result, status_code=status)

    @app.post(
        "/api/production/runs/{run_id}/stages/{stage_id}/decide",
        dependencies=[auth],
    )
    def decide(run_id: str, stage_id: int, body: DecideRequest) -> JSONResponse:
        result = handler.decide(
            run_id=run_id,
            stage_id=stage_id,
            verdict=body.verdict,
            notes_th=body.notes_th,
            decided_by=body.decided_by,
        )
        status = 400 if "error" in result else 200
        return JSONResponse(result, status_code=status)

    # ── Inbox + stage review HTML (Sprint 8 — finally mounted) ───────

    @app.get("/inbox", response_class=HTMLResponse, dependencies=[auth])
    def inbox_page() -> str:
        in_review_runs = director.list_runs(
            status_filter=ProductionRunStatus.IN_PROGRESS
        )
        return render_inbox_page(in_review_runs)

    @app.get("/api/inbox/fragment", response_class=HTMLResponse, dependencies=[auth])
    def inbox_fragment() -> str:
        in_review_runs = director.list_runs(
            status_filter=ProductionRunStatus.IN_PROGRESS
        )
        return render_inbox_fragment(in_review_runs)

    @app.get(
        "/production/runs/{run_id}/stages/{stage_id}/review",
        response_class=HTMLResponse,
        dependencies=[auth],
    )
    def stage_review_page(run_id: str, stage_id: int) -> str:
        run = director.get_run(run_id)
        if run is None:
            raise HTTPException(status_code=404, detail=f"run {run_id} not found")
        stage = run.get_stage(stage_id)
        if stage is None:
            raise HTTPException(
                status_code=404, detail=f"stage {stage_id} not found in run {run_id}"
            )
        return render_stage_review_page(run, stage)

    # ── Healthcheck (always open) ────────────────────────────────────

    @app.get("/healthz")
    def healthz() -> dict[str, str]:
        return {"status": "ok"}

    return app


# ────────────────────────────────────────────────────────────────────
# Default app for `uvicorn auto_affi.ops.console.server:app`
# ────────────────────────────────────────────────────────────────────

app = create_app()


# ────────────────────────────────────────────────────────────────────
# CLI launcher for `python -m auto_affi.ops.console`
# ────────────────────────────────────────────────────────────────────


def main() -> None:
    parser = argparse.ArgumentParser(description="Auto-Affi Ops Console server")
    parser.add_argument("--host", default="127.0.0.1", help="bind address")
    parser.add_argument("--port", type=int, default=8000, help="bind port")
    parser.add_argument(
        "--reload",
        action="store_true",
        help="enable auto-reload (dev only)",
    )
    args = parser.parse_args()

    import uvicorn

    uvicorn.run(
        "auto_affi.ops.console.server:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
    )


if __name__ == "__main__":
    main()
