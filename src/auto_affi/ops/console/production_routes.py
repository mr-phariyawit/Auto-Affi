"""Production workflow routes for the Ops Console (ADR-007).

Routes:
  GET  /api/production/runs                      — list runs
  GET  /api/production/runs/{run_id}              — run detail
  GET  /api/production/runs/{run_id}/stages/{n}   — stage detail
  POST /api/production/runs/{run_id}/stages/{n}/decide — apply verdict
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from auto_affi.agents.production_director import (
    InvalidTransitionError,
    ProductionDirector,
)
from auto_affi.schemas.production import (
    ProductionRunStatus,
)


@dataclass
class ProductionRouteHandler:
    """Handles production workflow API requests.

    Wraps ProductionDirector for use by the Ops Console.
    Not a FastAPI router itself — the console app calls these methods
    and serializes the results. This keeps the handler testable without
    needing an ASGI server.
    """

    director: ProductionDirector

    def list_runs(
        self, *, status: str | None = None
    ) -> dict[str, Any]:
        """GET /api/production/runs"""
        status_filter = None
        if status:
            try:
                status_filter = ProductionRunStatus(status)
            except ValueError:
                return {"error": f"Unknown status: {status}", "runs": []}

        runs = self.director.list_runs(status_filter=status_filter)
        return {
            "runs": [r.model_dump(mode="json") for r in runs],
            "count": len(runs),
        }

    def get_run(self, run_id: str) -> dict[str, Any]:
        """GET /api/production/runs/{run_id}"""
        run = self.director.get_run(run_id)
        if run is None:
            return {"error": f"Run {run_id} not found"}
        return run.model_dump(mode="json")

    def get_stage(self, run_id: str, stage_id: int) -> dict[str, Any]:
        """GET /api/production/runs/{run_id}/stages/{n}"""
        run = self.director.get_run(run_id)
        if run is None:
            return {"error": f"Run {run_id} not found"}
        stage = run.get_stage(stage_id)
        if stage is None:
            return {"error": f"Stage {stage_id} not found"}
        return {
            "run_id": run_id,
            "stage": stage.model_dump(mode="json"),
            "run_status": run.status.value,
        }

    def decide(
        self,
        run_id: str,
        stage_id: int,
        verdict: str,
        notes_th: str = "",
        decided_by: str = "board",
    ) -> dict[str, Any]:
        """POST /api/production/runs/{run_id}/stages/{n}/decide"""
        if verdict not in ("approve", "revise", "reject"):
            return {"error": f"Unknown verdict: {verdict}"}

        try:
            run = self.director.decide(
                run_id, stage_id, verdict,
                notes_th=notes_th,
                decided_by=decided_by,
            )
        except InvalidTransitionError as e:
            return {"error": str(e)}

        if run is None:
            return {"error": f"Run {run_id} not found"}

        return {
            "ok": True,
            "run_id": run_id,
            "stage_id": stage_id,
            "verdict": verdict,
            "run_status": run.status.value,
            "stage_status": run.get_stage(stage_id).status.value if run.get_stage(stage_id) else "unknown",
        }
