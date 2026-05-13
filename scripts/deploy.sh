#!/usr/bin/env bash
# deploy.sh — Auto-Affi deployment script
#
# Usage: ./scripts/deploy.sh [--dry-run] [--skip-tests]
#
# Steps:
#   1. Validate environment (Python, uv, required env vars)
#   2. Sync dependencies (uv sync --frozen)
#   3. Run lint (ruff check)
#   4. Run tests (pytest -m unit)
#   5. Run smoke test (run_once --dry-run)
#   6. Report success / failure
#
# Exit codes:
#   0  — deploy successful
#   1  — validation failure
#   2  — test failure
#   3  — smoke test failure

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

DRY_RUN=false
SKIP_TESTS=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --dry-run)    DRY_RUN=true; shift ;;
        --skip-tests) SKIP_TESTS=true; shift ;;
        *)            echo "Unknown arg: $1" >&2; exit 1 ;;
    esac
done

log() { echo "[deploy] $(date -u +%H:%M:%S) $*"; }
fail() { log "FAIL: $*"; exit "${2:-1}"; }

# ---- Step 1: Validate environment -------------------------------- #
log "Step 1: Validating environment..."

if [[ ! -d ".venv" ]]; then
    fail "No .venv directory found. Run: uv venv && uv sync" 1
fi

PYTHON=".venv/bin/python"
if [[ ! -x "$PYTHON" ]]; then
    fail "Python not found at $PYTHON" 1
fi

PY_VERSION=$($PYTHON --version 2>&1 | grep -oE '[0-9]+\.[0-9]+')
PY_MAJOR=$(echo "$PY_VERSION" | cut -d. -f1)
PY_MINOR=$(echo "$PY_VERSION" | cut -d. -f2)
if [[ "$PY_MAJOR" -lt 3 ]] || [[ "$PY_MAJOR" -eq 3 && "$PY_MINOR" -lt 12 ]]; then
    fail "Python 3.12+ required, found $PY_VERSION" 1
fi

if ! command -v uv &>/dev/null; then
    fail "uv not found. Install: curl -LsSf https://astral.sh/uv/install.sh | sh" 1
fi

log "  Python: $($PYTHON --version)"
log "  uv: $(uv --version)"

# Check required env vars (warn, don't fail — dry-run paths work without them)
MISSING_VARS=""
for var in AUTO_AFFI__ANTHROPIC_API_KEY AUTO_AFFI__SHOPEE_APP_ID; do
    if [[ -z "${!var:-}" ]]; then
        MISSING_VARS="$MISSING_VARS $var"
    fi
done
if [[ -n "$MISSING_VARS" ]]; then
    log "  WARNING: Missing env vars (dry-run mode OK):$MISSING_VARS"
fi

# ---- Step 2: Sync dependencies ----------------------------------- #
log "Step 2: Syncing dependencies..."
uv sync --frozen 2>&1 | tail -3
log "  Dependencies synced."

# ---- Step 3: Lint ------------------------------------------------ #
log "Step 3: Running lint..."
if ! $PYTHON -m ruff check src/ tests/ 2>&1 | tail -3; then
    fail "Lint check failed" 2
fi
log "  Lint passed."

# ---- Step 4: Tests ----------------------------------------------- #
if [[ "$SKIP_TESTS" == "true" ]]; then
    log "Step 4: SKIPPED (--skip-tests)"
else
    log "Step 4: Running tests..."
    if ! $PYTHON -m pytest -m unit --tb=short -q 2>&1 | tail -5; then
        fail "Tests failed" 2
    fi
    log "  Tests passed."
fi

# ---- Step 5: Smoke test ------------------------------------------ #
log "Step 5: Running smoke test (run_once)..."
if ! $PYTHON -m auto_affi.ops.run_once --product-id 12345 2>&1 | tail -10; then
    fail "Smoke test failed" 3
fi
log "  Smoke test passed."

# ---- Done -------------------------------------------------------- #
if [[ "$DRY_RUN" == "true" ]]; then
    log "DRY RUN complete. No deployment actions taken."
else
    log "Deployment validation complete."
    log "To deploy: restart the service via your process manager."
fi

log "All checks passed."
exit 0
