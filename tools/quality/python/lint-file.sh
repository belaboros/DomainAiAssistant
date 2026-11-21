#!/usr/bin/env bash
# Claude Code PostToolUse hook (ADR-0020): lints a Python file right after Claude writes it.
# Exit 2 hands the findings back to Claude so it fixes them straight away.
set -uo pipefail

root="${CLAUDE_PROJECT_DIR:-$(pwd)}"
file=$(jq -r '.tool_input.file_path // .tool_input.notebook_path // empty' 2>/dev/null)
case "$file" in
  *.py|*.pyi) ;;
  *) exit 0 ;;
esac
[ -f "$file" ] || exit 0
cd "$root" || exit 0

failed=0
lint=$(uv run --quiet ruff check --no-fix "$file" 2>&1) || failed=1
fmt=$(uv run --quiet ruff format --check --diff "$file" 2>&1) || failed=1
if [ "$failed" -ne 0 ]; then
  printf 'Python quality gate failed for %s. Fix the findings (formatting: uv run ruff format %s).\n%s\n%s\n' \
    "$file" "$file" "$lint" "$fmt" >&2
  exit 2
fi
exit 0
