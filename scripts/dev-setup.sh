#!/usr/bin/env bash
# dev-setup.sh — One-command developer environment bootstrap for Auto-Affi
#
# Usage: bash scripts/dev-setup.sh
#
# What it does:
#   1. Checks for Homebrew (macOS) or apt (Linux)
#   2. Installs system dependencies: ffmpeg, espeak-ng
#   3. Verifies .venv exists with Python 3.12+
#   4. Syncs Python dependencies via uv (or pip fallback)
#   5. Runs the unit test suite to verify the setup
#
# Idempotent: safe to run multiple times. Already-installed tools are skipped.

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

info()  { echo -e "${GREEN}[dev-setup]${NC} $*"; }
warn()  { echo -e "${YELLOW}[dev-setup]${NC} $*"; }
error() { echo -e "${RED}[dev-setup]${NC} $*" >&2; }

# Navigate to project root (one level up from scripts/)
cd "$(dirname "$0")/.."
PROJECT_ROOT="$(pwd)"
info "Project root: $PROJECT_ROOT"

# ------------------------------------------------------------------ #
# 1. System dependencies                                              #
# ------------------------------------------------------------------ #

install_with_brew() {
    local pkg="$1"
    if command -v "$pkg" &>/dev/null; then
        info "$pkg already installed ($(command -v "$pkg"))"
    else
        if command -v brew &>/dev/null; then
            info "Installing $pkg via Homebrew..."
            brew install "$pkg"
        else
            error "Homebrew not found. Install $pkg manually."
            return 1
        fi
    fi
}

install_with_apt() {
    local pkg="$1"
    if command -v "$pkg" &>/dev/null; then
        info "$pkg already installed"
    else
        if command -v apt-get &>/dev/null; then
            info "Installing $pkg via apt..."
            sudo apt-get update -qq && sudo apt-get install -y -qq "$pkg"
        else
            error "apt not found. Install $pkg manually."
            return 1
        fi
    fi
}

info "Checking system dependencies..."

if [[ "$(uname)" == "Darwin" ]]; then
    install_with_brew ffmpeg
    install_with_brew espeak-ng
elif [[ "$(uname)" == "Linux" ]]; then
    install_with_apt ffmpeg
    install_with_apt espeak-ng
else
    warn "Unknown OS: $(uname). Install ffmpeg and espeak-ng manually."
fi

# ------------------------------------------------------------------ #
# 2. Python environment                                               #
# ------------------------------------------------------------------ #

info "Checking Python environment..."

if [[ -f "$PROJECT_ROOT/.venv/bin/python" ]]; then
    PYTHON="$PROJECT_ROOT/.venv/bin/python"
    PY_VERSION=$("$PYTHON" --version 2>&1)
    info "Found .venv Python: $PY_VERSION"

    # Verify >= 3.12
    PY_MINOR=$("$PYTHON" -c "import sys; print(sys.version_info.minor)")
    if [[ "$PY_MINOR" -lt 12 ]]; then
        error "Python 3.12+ required, found $PY_VERSION"
        error "Recreate venv: uv venv --python 3.12"
        exit 1
    fi
else
    warn ".venv not found. Creating with uv..."
    if command -v uv &>/dev/null; then
        uv venv --python 3.12
        PYTHON="$PROJECT_ROOT/.venv/bin/python"
    else
        error "uv not found. Install: curl -LsSf https://astral.sh/uv/install.sh | sh"
        exit 1
    fi
fi

# ------------------------------------------------------------------ #
# 3. Python dependencies                                              #
# ------------------------------------------------------------------ #

info "Syncing Python dependencies..."

if command -v uv &>/dev/null; then
    uv sync --quiet 2>/dev/null || uv pip install -e ".[dev]" --quiet 2>/dev/null || true
else
    "$PYTHON" -m pip install -e ".[dev]" --quiet 2>/dev/null || true
fi

# ------------------------------------------------------------------ #
# 4. Verify setup                                                     #
# ------------------------------------------------------------------ #

info "Verifying setup..."

echo ""
echo "System tools:"
echo "  ffmpeg:    $(command -v ffmpeg 2>/dev/null || echo 'NOT FOUND')"
echo "  espeak-ng: $(command -v espeak-ng 2>/dev/null || echo 'NOT FOUND')"
echo "  Python:    $("$PYTHON" --version 2>&1)"
echo ""

# ------------------------------------------------------------------ #
# 5. Run tests                                                        #
# ------------------------------------------------------------------ #

info "Running unit tests..."
"$PYTHON" -m pytest tests/unit -m unit --tb=short -q --override-ini="addopts=" 2>&1 || {
    error "Tests failed! Check output above."
    exit 1
}

echo ""
info "Dev environment ready. Run demos with:"
info "  .venv/bin/python -m auto_affi.ops.make_demo"
