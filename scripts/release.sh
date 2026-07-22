#!/usr/bin/env bash
# Build and publish a release to PyPI from your local machine.
#
# Usage:
#   scripts/release.sh              # checks, build, TestPyPI, confirm, PyPI, tag+push
#   scripts/release.sh --test-only  # stop after the TestPyPI dry-run
#
# Prerequisites (do these first, not scripted here):
#   1. Bump the version in src/instantlyai/_version.py
#   2. Move the relevant [Unreleased] entries in CHANGELOG.md under a new
#      "## [X.Y.Z] - YYYY-MM-DD" heading
#   3. Commit that bump (this script does not commit anything for you)
#
# Requires PyPI + TestPyPI API tokens (Account settings -> API tokens on each site,
# scoped to the `instantlyai` project). Export them in your shell -- never commit
# them or put them in a file tracked by git:
#   export TESTPYPI_TOKEN=pypi-...
#   export PYPI_TOKEN=pypi-...

set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

VERSION="$(uv run python -c 'from instantlyai._version import __version__; print(__version__)')"
echo "Releasing instantlyai ${VERSION}"

if git rev-parse "v${VERSION}" >/dev/null 2>&1; then
  echo "Tag v${VERSION} already exists -- did you forget to bump _version.py?" >&2
  exit 1
fi

echo "==> Running checks"
uv run pre-commit run --all-files
uv run pytest

echo "==> Building"
rm -rf dist
uv build

echo "==> Publishing to TestPyPI"
: "${TESTPYPI_TOKEN:?Set TESTPYPI_TOKEN to your TestPyPI API token}"
uv publish --publish-url https://test.pypi.org/legacy/ --token "$TESTPYPI_TOKEN"

cat <<EOF

==> Verify the TestPyPI upload before continuing:
    pip install --index-url https://test.pypi.org/simple/ \\
        --extra-index-url https://pypi.org/simple/ instantlyai==${VERSION}
    python -c "import instantlyai; print(instantlyai.__version__)"

EOF

if [[ "${1:-}" == "--test-only" ]]; then
  echo "Stopping after TestPyPI (--test-only)."
  exit 0
fi

read -r -p "TestPyPI install confirmed working -- publish ${VERSION} to real PyPI? [y/N] " confirm
if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
  echo "Aborted before publishing to PyPI."
  exit 1
fi

echo "==> Publishing to PyPI"
: "${PYPI_TOKEN:?Set PYPI_TOKEN to your PyPI API token}"
uv publish --token "$PYPI_TOKEN"

echo "==> Tagging and pushing v${VERSION}"
git tag "v${VERSION}"
git push origin "v${VERSION}"

echo "Done: https://pypi.org/project/instantlyai/${VERSION}/"
