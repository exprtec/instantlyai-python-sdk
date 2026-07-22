#!/usr/bin/env bash
# Lint + format-check + type-check -- the same checks CI runs, runnable locally.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

uv run ruff format --check .
uv run ruff check .
uv run ty check
