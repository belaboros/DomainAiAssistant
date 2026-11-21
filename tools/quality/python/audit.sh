#!/usr/bin/env bash
# Audits the locked Python dependencies (all workspace members and dev tools) with pip-audit (ADR-0020).
set -euo pipefail
cd "$(dirname "$0")/../../.."
req="$(mktemp)"
trap 'rm -f "$req"' EXIT
uv export --format requirements-txt --no-hashes --all-packages --no-emit-workspace --no-emit-project --quiet -o "$req"
uv run pip-audit --strict --progress-spinner off -r "$req"
