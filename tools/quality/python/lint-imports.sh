#!/usr/bin/env bash
# Runs import-linter with every apps/*/src and libs/*/src on the path, so packages that are
# not (yet) workspace members are checked too (ADR-0020).
set -euo pipefail
root="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "$root"
paths=""
for d in apps/*/src libs/*/src; do
  [ -d "$d" ] && paths="${paths:+$paths:}$root/$d"
done
PYTHONPATH="${paths}${PYTHONPATH:+:$PYTHONPATH}" exec uv run lint-imports .importlinter "$@"
