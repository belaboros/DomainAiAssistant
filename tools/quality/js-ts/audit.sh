#!/usr/bin/env bash
# Audits the locked npm dependencies of every workspace and the root dev tools (ADR-0021).
# Fails on a high or critical advisory; moderate and low ones are reported only.
set -euo pipefail
cd "$(dirname "$0")/../../.."
npm audit --audit-level=high
