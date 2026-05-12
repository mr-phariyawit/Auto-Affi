# Auto-Affi

Autonomous AI marketing platform for Shopee affiliate (TH).

A crew of Claude-based agents scouts Shopee products, writes Thai-native
storyboards, produces premium 9:16 vertical videos via kie.ai (Veo / Sora /
Flux / Suno), publishes to IG / FB / YT Shorts with subId-tagged affiliate
links, collects metrics, and self-improves through an LLM Wiki feedback
loop.

## Status

Phase 0 — PM setup. Repo skeleton + CI in place. See `docs/pm/project-plan.md`.

## Documentation

Read these in order:

| Doc | What |
|---|---|
| `SPEC.md` | Full system spec — vision, architecture, agents, data model |
| `docs/execution-playbook.md` | 300% target playbook (research-synthesized) |
| `docs/llm-allocation.md` | Per-agent Claude model + prompt caching plan |
| `docs/thai-genai-stack.md` | Thai-focused gen-AI stack + kie.ai gateway |
| `docs/iso29110-gap-analysis.md` | ISO 29110 Basic Profile compliance audit |
| `docs/pm/` | Project plan, SOW, risk register, RACI |
| `docs/si/` | SRS, test plan, coding & prompt standards |

## Compliance

ISO/IEC 29110 Basic Profile — **guideline mode** (not audit-ready).
Live work tracking: Linear (aegis-team workspace).
Project Manager: Nick Fury.

## Local setup

Requirements: Python 3.12+, [uv](https://docs.astral.sh/uv/), Docker (for
Postgres + Redis + Temporal locally).

```bash
# Install dependencies and dev tools
uv sync --group dev

# Set up pre-commit hooks
uv run pre-commit install

# Copy local env (never commit .env)
cp .env.example .env
# ... then fill in vendor keys for the adapters you are exercising

# Run lint + tests
uv run ruff check src tests
uv run black --check src tests
uv run mypy src
uv run pytest -m unit
```

## Repo layout

```
src/auto_affi/
  agents/         # one module per agent (scout, strategist, ...)
  adapters/       # one per external API (shopee, kie, eleven, ...)
  workflows/      # Temporal workflows + activities
  pipeline/       # video editor + Hyperframe + ffmpeg + ASR
  wiki/           # retrieval, write, tier management
  schemas/        # pydantic models for cross-boundary data
  ops/            # CLI + ops console backend
  config/         # settings, secrets loader
  observability/  # OpenTelemetry + Langfuse integration
tests/
  unit/ integration/ e2e/ fixtures/ golden_traces/
```

See `docs/si/coding-standards.md` for conventions and `docs/si/prompt-standards.md`
for prompt-as-code workflow.

## Contributing

1. Branch off `main`: `feat/<slug>` or `claude/<slug>` for AI co-dev work
2. Conventional Commits message format
3. PR with summary + test plan + Linear issue link
4. CI must pass: ruff, black, mypy, pytest (unit + integration), gitleaks
5. ≥ 1 reviewer approval before squash-merge

## License

Proprietary — aegis-team.
