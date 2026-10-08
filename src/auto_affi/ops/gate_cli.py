"""CLI over the PGA gate for routes that run outside the coded pipeline (e.g. the Higgsfield UI operator).

The gate logic is NOT reimplemented here: every command calls `auto_affi.pipeline.prompt_audit`, so the
tamper-evident event log and the hash binding behave exactly as in `enforce_spend_gate`.
Credits are capped per run in `credits.json` (fail-closed: no budget file = no spend) and every committed
spend is appended to `ledger.jsonl`.

    python -m auto_affi.ops.gate_cli audit     --run RUN --stage video --manifest m.json
    python -m auto_affi.ops.gate_cli approve   --run RUN --stage video --by human:<name>   # only on a human's word
    python -m auto_affi.ops.gate_cli bypass    --run RUN --stage cast_sheet --reason "..." --by human:<name>
    python -m auto_affi.ops.gate_cli check     --run RUN --stage video --manifest m.json
    python -m auto_affi.ops.gate_cli budget    --run RUN --max-credits 400 --by human:<name>
    python -m auto_affi.ops.gate_cli spend     --run RUN --credits 176 [--commit | --refund] [--label ... --route ui --model ...]
    python -m auto_affi.ops.gate_cli preflight --run RUN --stage video --manifest m.json --credits 176
    python -m auto_affi.ops.gate_cli status    --run RUN

Exit codes: 0 ok · 1 audit failed · 2 usage/IO error · 3 gate blocked · 4 budget blocked.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path

from auto_affi.pipeline.prompt_audit import (
    STAGES,
    GenerationBlocked,
    ReferenceManifest,
    assert_may_generate,
    audit,
    load_approvals,
    record_approval,
    record_audit,
    record_bypass,
)

OK, AUDIT_FAILED, USAGE, GATE_BLOCKED, BUDGET_BLOCKED = 0, 1, 2, 3, 4
CREDITS_FILE = "credits.json"
LEDGER_FILE = "ledger.jsonl"


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _print(data: object) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def _load_manifest(path: Path) -> ReferenceManifest:
    return ReferenceManifest(**json.loads(path.read_text(encoding="utf-8")))


def _budget(run: Path) -> dict[str, object] | None:
    path = run / CREDITS_FILE
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def _spend_decision(run: Path, credits: float) -> tuple[int, dict[str, object]]:
    budget = _budget(run)
    if budget is None:
        return BUDGET_BLOCKED, {"allowed": False, "reason": f"no {CREDITS_FILE}: a human must set a credit cap"}
    max_c, spent = float(budget["max_credits"]), float(budget.get("spent_credits", 0))  # type: ignore[arg-type]
    allowed = credits > 0 and spent + credits <= max_c
    info: dict[str, object] = {"allowed": allowed, "credits": credits, "spent_credits": spent, "max_credits": max_c,
            "remaining_after": max_c - spent - credits}
    if not allowed:
        info["reason"] = "credits must be > 0" if credits <= 0 else "would exceed the run's credit cap"
    return (OK if allowed else BUDGET_BLOCKED), info


def cmd_audit(args: argparse.Namespace) -> int:
    result = audit(_load_manifest(args.manifest))
    record_audit(args.run, args.stage, result)
    _print({"stage": args.stage, "passed": result.passed, "prompt_hash": result.prompt_hash,
            "failures": [f.model_dump(mode="json") for f in result.failures]})
    return OK if result.passed else AUDIT_FAILED


def cmd_approve(args: argparse.Namespace) -> int:
    record_approval(args.run, args.stage, approved_by=args.by)
    _print({"stage": args.stage, "approved_by": args.by})
    return OK


def cmd_bypass(args: argparse.Namespace) -> int:
    record_bypass(args.run, args.stage, args.reason, by=args.by)
    _print({"stage": args.stage, "bypassed_by": args.by, "reason": args.reason})
    return OK


def cmd_check(args: argparse.Namespace) -> int:
    assert_may_generate(args.stage, args.run, manifest=_load_manifest(args.manifest))
    _print({"stage": args.stage, "may_generate": True})
    return OK


def cmd_budget(args: argparse.Namespace) -> int:
    budget = _budget(args.run) or {"spent_credits": 0, "unit": "higgsfield-credits"}
    budget.update(max_credits=args.max_credits, set_by=args.by, set_at=_now())
    (args.run / CREDITS_FILE).write_text(json.dumps(budget, indent=2), encoding="utf-8")
    _print(budget)
    return OK


def cmd_spend(args: argparse.Namespace) -> int:
    if args.refund:
        budget = _budget(args.run)
        if budget is None:
            return BUDGET_BLOCKED
        budget["spent_credits"] = max(0.0, float(budget.get("spent_credits", 0)) - args.credits)  # type: ignore[arg-type]
        (args.run / CREDITS_FILE).write_text(json.dumps(budget, indent=2), encoding="utf-8")
        entry = {"at": _now(), "credits": -args.credits, "label": args.label or "refund", "route": args.route,
                 "model": args.model, "request_ref": args.ref}
        with (args.run / LEDGER_FILE).open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
        _print({"refunded": args.credits, "spent_credits": budget["spent_credits"]})
        return OK
    code, info = _spend_decision(args.run, args.credits)
    if code == OK and args.commit:
        budget = _budget(args.run) or {}
        budget["spent_credits"] = float(budget.get("spent_credits", 0)) + args.credits  # type: ignore[arg-type]
        (args.run / CREDITS_FILE).write_text(json.dumps(budget, indent=2), encoding="utf-8")
        entry = {"at": _now(), "credits": args.credits, "label": args.label, "route": args.route,
                 "model": args.model, "request_ref": args.ref}
        with (args.run / LEDGER_FILE).open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
        info.update(committed=True, spent_credits=budget["spent_credits"])
    _print(info)
    return code


def cmd_preflight(args: argparse.Namespace) -> int:
    try:
        assert_may_generate(args.stage, args.run, manifest=_load_manifest(args.manifest))
    except GenerationBlocked as blocked:
        _print({"may_generate": False, "gate": "blocked", "reason": blocked.reason})
        return GATE_BLOCKED
    code, info = _spend_decision(args.run, args.credits)
    _print({"may_generate": code == OK, "gate": "pass", "budget": info})
    return code


def cmd_status(args: argparse.Namespace) -> int:
    approvals = load_approvals(args.run)
    stages = {s: approvals[s].model_dump(mode="json") if s in approvals else {"approved": False} for s in STAGES}
    ledger = args.run / LEDGER_FILE
    _print({"run": str(args.run), "stages": stages, "budget": _budget(args.run),
            "ledger_entries": len(ledger.read_text().splitlines()) if ledger.exists() else 0})
    return OK


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="gate_cli", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)

    def add(name: str, fn: Callable[[argparse.Namespace], int], *, stage: bool = False,
            manifest: bool = False) -> argparse.ArgumentParser:
        p = sub.add_parser(name)
        p.add_argument("--run", type=Path, required=True)
        if stage:
            p.add_argument("--stage", choices=STAGES, required=True)
        if manifest:
            p.add_argument("--manifest", type=Path, required=True)
        p.set_defaults(fn=fn)
        return p

    add("audit", cmd_audit, stage=True, manifest=True)
    add("approve", cmd_approve, stage=True).add_argument("--by", required=True)
    p = add("bypass", cmd_bypass, stage=True)
    p.add_argument("--reason", required=True)
    p.add_argument("--by", required=True)
    add("check", cmd_check, stage=True, manifest=True)
    p = add("budget", cmd_budget)
    p.add_argument("--max-credits", type=float, required=True)
    p.add_argument("--by", required=True)
    p = add("spend", cmd_spend)
    p.add_argument("--credits", type=float, required=True)
    p.add_argument("--commit", action="store_true")
    p.add_argument("--refund", action="store_true", help="provider refunded a failed job")
    for opt in ("--label", "--route", "--model", "--ref"):
        p.add_argument(opt, default="")
    add("preflight", cmd_preflight, stage=True, manifest=True).add_argument("--credits", type=float, required=True)
    add("status", cmd_status)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        args.run.mkdir(parents=True, exist_ok=True)
        return int(args.fn(args))
    except GenerationBlocked as blocked:
        _print({"blocked": True, "stage": blocked.stage, "reason": blocked.reason})
        return GATE_BLOCKED
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return USAGE


if __name__ == "__main__":
    raise SystemExit(main())
