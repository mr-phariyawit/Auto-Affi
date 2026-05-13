#!/usr/bin/env bash
# deploy-cron.sh — Auto-Affi cron scheduler for MANUAL mode (QW-9)
#
# Installs (or shows) a crontab entry that runs auto_affi.ops.run_once
# at the optimal Thai posting windows for IG Reels.
#
# Usage:
#   ./scripts/deploy-cron.sh install   # Install crontab entries
#   ./scripts/deploy-cron.sh show      # Show what would be installed
#   ./scripts/deploy-cron.sh remove    # Remove crontab entries
#   ./scripts/deploy-cron.sh status    # Check if cron is active
#
# Posting windows (Thailand = UTC+7):
#   - 12:00 ICT (05:00 UTC) — lunch break scroll
#   - 20:00 ICT (13:00 UTC) — evening prime time
#
# Phase 1: laptop cron. Phase 2: Temporal Cloud or VPS systemd timer.
#
# Exit codes:
#   0 — success
#   1 — error

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VENV_PYTHON="${REPO_ROOT}/.venv/bin/python"
METRICS_CMD="${VENV_PYTHON} -m auto_affi.ops.metrics_export --output ${REPO_ROOT}/out/metrics.jsonl"
RUN_ONCE_CMD="${VENV_PYTHON} -m auto_affi.ops.run_once --dry-run"
LOG_DIR="${REPO_ROOT}/out/logs"
CRON_TAG="# AUTO_AFFI_CRON"

# Cron schedule: 05:00 UTC (12:00 ICT) and 13:00 UTC (20:00 ICT)
CRON_LUNCH="0 5 * * * cd ${REPO_ROOT} && ${RUN_ONCE_CMD} >> ${LOG_DIR}/run_once.log 2>&1 ${CRON_TAG}"
CRON_EVENING="0 13 * * * cd ${REPO_ROOT} && ${RUN_ONCE_CMD} >> ${LOG_DIR}/run_once.log 2>&1 ${CRON_TAG}"
CRON_METRICS="30 14 * * * cd ${REPO_ROOT} && ${METRICS_CMD} >> ${LOG_DIR}/metrics_export.log 2>&1 ${CRON_TAG}"

_ensure_log_dir() {
    mkdir -p "${LOG_DIR}"
}

_show_entries() {
    echo "=== Auto-Affi Cron Entries ==="
    echo ""
    echo "Lunch posting (12:00 ICT / 05:00 UTC):"
    echo "  ${CRON_LUNCH}"
    echo ""
    echo "Evening posting (20:00 ICT / 13:00 UTC):"
    echo "  ${CRON_EVENING}"
    echo ""
    echo "Daily metrics export (21:30 ICT / 14:30 UTC):"
    echo "  ${CRON_METRICS}"
    echo ""
    echo "Logs: ${LOG_DIR}/"
    echo ""
    echo "NOTE: run_once currently uses --dry-run."
    echo "Remove --dry-run from crontab when credentials are configured."
}

_install() {
    _ensure_log_dir

    # Verify Python venv exists
    if [[ ! -x "${VENV_PYTHON}" ]]; then
        echo "ERROR: ${VENV_PYTHON} not found. Run 'uv sync' first." >&2
        exit 1
    fi

    # Remove existing Auto-Affi entries, then add new ones
    local existing
    existing=$(crontab -l 2>/dev/null || true)
    local cleaned
    cleaned=$(echo "${existing}" | grep -v "${CRON_TAG}" || true)

    {
        echo "${cleaned}"
        echo "${CRON_LUNCH}"
        echo "${CRON_EVENING}"
        echo "${CRON_METRICS}"
    } | crontab -

    echo "Installed 3 cron entries. Verify with: crontab -l"
    _show_entries
}

_remove() {
    local existing
    existing=$(crontab -l 2>/dev/null || true)
    local cleaned
    cleaned=$(echo "${existing}" | grep -v "${CRON_TAG}" || true)
    echo "${cleaned}" | crontab -
    echo "Removed all Auto-Affi cron entries."
}

_status() {
    local count
    count=$(crontab -l 2>/dev/null | grep -c "${CRON_TAG}" || true)
    if [[ "${count}" -gt 0 ]]; then
        echo "Active: ${count} Auto-Affi cron entries found."
        crontab -l 2>/dev/null | grep "${CRON_TAG}"
    else
        echo "Inactive: no Auto-Affi cron entries."
    fi
}

case "${1:-show}" in
    install) _install ;;
    show)    _show_entries ;;
    remove)  _remove ;;
    status)  _status ;;
    *)
        echo "Usage: $0 {install|show|remove|status}" >&2
        exit 1
        ;;
esac
