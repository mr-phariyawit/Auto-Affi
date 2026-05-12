# Instinct: Always Use .venv/bin/python

- **ID**: instinct-venv-001
- **Tier**: promoted (hard rule)
- **Created**: 2026-05-13
- **Source**: Session 1 misdiagnosis -- bare `python3` invoked system 3.9 instead of project 3.13.9

## Rule

ALWAYS use `.venv/bin/python` (or `source .venv/bin/activate && python`) when running:
- pytest / test commands
- Any Python script in src/ or tools/
- Linting (ruff, mypy)
- Package management (pip, uv)

NEVER use bare `python`, `python3`, or system Python for project commands.

## Rationale

The project uses PEP 695 generics (`class Foo[T]`) which require Python 3.12+. The system Python on macOS is 3.9. The project ships its own `.venv/` with Python 3.13.9. Using bare `python3` causes every test to fail with SyntaxError, wasting an entire session diagnosing a false "blocker".

## Applies to

All agents: Spider-Man (build), Black Panther (review), War Machine (QA), Vision (test execution), and any agent that runs Python commands.
