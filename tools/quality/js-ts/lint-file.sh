#!/usr/bin/env bash
# Claude Code PostToolUse hook (ADR-0021): lints a JS/TS file right after Claude writes it.
# Exit 2 hands the findings back to Claude so it fixes them straight away.
set -uo pipefail

root="${CLAUDE_PROJECT_DIR:-$(pwd)}"
file=$(jq -r '.tool_input.file_path // empty' 2>/dev/null)
case "$file" in
  *.js|*.jsx|*.mjs|*.cjs|*.ts|*.tsx|*.mts|*.cts) ;;
  *) exit 0 ;;
esac
[ -f "$file" ] || exit 0
cd "$root" || exit 0
[ -x node_modules/.bin/eslint ] || exit 0   # not installed yet: `npm ci`

failed=0
lint=$(node_modules/.bin/eslint --max-warnings 0 --no-warn-ignored "$file" 2>&1) || failed=1
fmt=$(node_modules/.bin/prettier --check "$file" 2>&1) || failed=1
if [ "$failed" -ne 0 ]; then
  printf 'JS/TS quality gate failed for %s. Fix the findings (formatting: npx prettier --write %s).\n%s\n%s\n' \
    "$file" "$file" "$lint" "$fmt" >&2
  exit 2
fi
exit 0
