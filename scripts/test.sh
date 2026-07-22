#!/usr/bin/env bash
# Run the test suite. Extra args are forwarded to pytest, e.g. `scripts/test.sh -k campaigns`.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

uv run pytest "$@"
