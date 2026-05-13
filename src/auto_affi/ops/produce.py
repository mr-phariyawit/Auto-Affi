"""Studio production CLI — gated workflow from Shopee URL to finished clip.

Usage:
    .venv/bin/python -m auto_affi.ops.produce start --shopee-url URL
    .venv/bin/python -m auto_affi.ops.produce status
    .venv/bin/python -m auto_affi.ops.produce approve <run_id> --stage N
    .venv/bin/python -m auto_affi.ops.produce revise <run_id> --stage N --notes "..."
    .venv/bin/python -m auto_affi.ops.produce reject <run_id> --stage N --reason "..."
    .venv/bin/python -m auto_affi.ops.produce next

See ADR-007 for the full workflow specification.

Exit codes:
    0 — success
    1 — not found
    2 — invalid state transition
"""

from __future__ import annotations

import argparse
import contextlib
import json
import sys
from pathlib import Path

from auto_affi.agents.production_director import (
    InvalidTransitionError,
    ProductionDirector,
)
from auto_affi.schemas.production import (
    STAGE_DISPLAY,
    ProductionRunStatus,
    ProductionStageStatus,
)


def _director() -> ProductionDirector:
    return ProductionDirector(repo_root=Path("."))


# ADR-007: stages 9 (Compliance) and 10 (Publish) cannot be auto-approved.
# "Stage 9 is automated and cannot be skipped via --auto-approve; legal-grade backstop"
UNSKIPPABLE_STAGES: frozenset[int] = frozenset({9, 10})


def cmd_start(args: argparse.Namespace) -> int:
    """Start a new production run."""
    director = _director()
    run = director.start_run(args.shopee_url)

    # Auto-approve specified stages (except UNSKIPPABLE per ADR-007)
    if args.auto_approve:
        stage_names = [s.strip() for s in args.auto_approve.split(",")]
        name_to_id = {
            "brief": 1, "brief_and_concept": 1,
            "script": 2,
            "storyboard": 3,
            "visual_references": 4, "visuals": 4,
            "animatics": 5,
            "voice_over": 6, "vo": 6,
            "music": 7, "music_and_sfx": 7,
            "final_cut": 8,
            # compliance and publish intentionally excluded
        }
        for name in stage_names:
            sid = name_to_id.get(name)
            if sid and sid not in UNSKIPPABLE_STAGES:
                stage = run.get_stage(sid)
                if stage and stage.status == ProductionStageStatus.IN_REVIEW:
                    with contextlib.suppress(InvalidTransitionError):
                        run = director.decide(run.run_id, sid, "approve")

    _print_run_summary(run)
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    """List runs with IN_REVIEW stages."""
    director = _director()
    runs = director.list_runs()
    if not runs:
        print("No production runs found.")
        return 0

    print(f"{'Run ID':<14} {'Status':<14} {'Stage':<25} {'SLA'}")
    print("-" * 70)
    for run in runs:
        for stage in run.in_review_stages:
            sla = stage.sla_deadline.strftime("%H:%M %b %d")
            print(
                f"{run.run_id:<14} {run.status.value:<14} "
                f"{stage.display_name:<25} {sla}"
            )
        if not run.in_review_stages:
            print(f"{run.run_id:<14} {run.status.value:<14} {'(none in review)':<25}")

    if args.json:
        data = [r.model_dump(mode="json") for r in runs]
        print(json.dumps(data, indent=2, ensure_ascii=False))
    return 0


def cmd_approve(args: argparse.Namespace) -> int:
    """Approve a stage."""
    director = _director()
    try:
        run = director.decide(args.run_id, args.stage, "approve")
    except InvalidTransitionError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    if run is None:
        print(f"Run {args.run_id} not found.", file=sys.stderr)
        return 1
    _print_run_summary(run)
    return 0


def cmd_revise(args: argparse.Namespace) -> int:
    """Request revision on a stage."""
    director = _director()
    try:
        run = director.decide(args.run_id, args.stage, "revise", notes_th=args.notes)
    except InvalidTransitionError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    if run is None:
        print(f"Run {args.run_id} not found.", file=sys.stderr)
        return 1
    _print_run_summary(run)
    return 0


def cmd_reject(args: argparse.Namespace) -> int:
    """Reject a stage and halt the run."""
    director = _director()
    try:
        run = director.decide(
            args.run_id, args.stage, "reject", notes_th=args.reason
        )
    except InvalidTransitionError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    if run is None:
        print(f"Run {args.run_id} not found.", file=sys.stderr)
        return 1
    _print_run_summary(run)
    return 0


def cmd_next(args: argparse.Namespace) -> int:
    """Show the next stage awaiting review."""
    director = _director()
    runs = director.list_runs(status_filter=ProductionRunStatus.IN_PROGRESS)
    for run in runs:
        for stage in run.in_review_stages:
            print(f"Run: {run.run_id}")
            print(f"Stage: {stage.stage_id} — {stage.display_name}")
            print(f"Status: {stage.status.value}")
            if stage.current_revision and stage.current_revision.artifact:
                print("Deliverable preview:")
                print(json.dumps(stage.current_revision.artifact, indent=2, ensure_ascii=False))
            print(f"\nOps Console: http://localhost:8000/api/production/runs/{run.run_id}/stages/{stage.stage_id}")
            return 0
    print("No stages awaiting review.")
    return 0


def _print_run_summary(run) -> None:
    """Print a compact summary of a production run."""
    print(f"\n{'='*60}")
    print(f"Production Run: {run.run_id}")
    print(f"{'='*60}")
    print(f"Shopee URL:  {run.shopee_url}")
    print(f"Item ID:     {run.shopee_item_id}")
    print(f"Status:      {run.status.value}")
    print(f"Cost (THB):  {run.total_cost_thb:.3f}")
    print()
    for stage in run.stages:
        icon = {
            "draft": "  ",
            "in_review": "->",
            "approved": "OK",
            "revision_pending": "~~",
            "rejected": "XX",
        }.get(stage.status.value, "??")
        revs = f"(rev {stage.revision_count})" if stage.revision_count > 0 else ""
        name = STAGE_DISPLAY.get(stage.stage_id, stage.name)
        print(f"  [{icon}] {stage.stage_id:>2}. {name:<25} {stage.status.value:<20} {revs}")
    print(f"{'='*60}")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="auto_affi.ops.produce",
        description="Studio production workflow — Shopee URL to finished clip",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # start
    p_start = sub.add_parser("start", help="Start a new production run")
    p_start.add_argument("--shopee-url", required=True, help="Shopee product URL")
    p_start.add_argument(
        "--auto-approve", default="",
        help="Comma-separated stage names to auto-approve (e.g. script,storyboard)"
    )
    p_start.set_defaults(func=cmd_start)

    # status
    p_status = sub.add_parser("status", help="List runs awaiting review")
    p_status.add_argument("--json", action="store_true", help="JSON output")
    p_status.set_defaults(func=cmd_status)

    # approve
    p_approve = sub.add_parser("approve", help="Approve a stage")
    p_approve.add_argument("run_id", help="Production run ID")
    p_approve.add_argument("--stage", type=int, required=True, help="Stage number (1-10)")
    p_approve.set_defaults(func=cmd_approve)

    # revise
    p_revise = sub.add_parser("revise", help="Request revision")
    p_revise.add_argument("run_id", help="Production run ID")
    p_revise.add_argument("--stage", type=int, required=True, help="Stage number (1-10)")
    p_revise.add_argument("--notes", required=True, help="Revision notes (Thai)")
    p_revise.set_defaults(func=cmd_revise)

    # reject
    p_reject = sub.add_parser("reject", help="Reject and halt run")
    p_reject.add_argument("run_id", help="Production run ID")
    p_reject.add_argument("--stage", type=int, required=True, help="Stage number (1-10)")
    p_reject.add_argument("--reason", required=True, help="Rejection reason")
    p_reject.set_defaults(func=cmd_reject)

    # next
    p_next = sub.add_parser("next", help="Show next awaiting review")
    p_next.set_defaults(func=cmd_next)

    args = parser.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
