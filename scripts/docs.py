#!/usr/bin/env python3
"""Keep docs-as-code in sync with the source of truth, then (optionally) build.

Two things can silently rot if edited by hand in two places:

1. ``README.md`` and ``docs/index.md`` -- the README is the PyPI landing page;
   ``docs/index.md`` is the MkDocs home page. They must say the same thing.
2. Fenced code blocks in ``docs/tutorial/*.md`` that are meant to mirror a
   runnable script in ``docs_src/`` -- marked with a preceding
   ``<!-- docs_src: name.py -->`` comment. The docs_src file is the source of
   truth (it's executed in CI); the markdown fence is kept in sync from it.

Usage:
    uv run scripts/docs.py sync            # write docs/index.md + tutorial fences
    uv run scripts/docs.py sync --check    # fail if anything is out of sync (CI/pre-commit)
    uv run scripts/docs.py build           # sync, then `mkdocs build --strict`
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
DOCS_INDEX = ROOT / "docs" / "index.md"
DOCS_SRC = ROOT / "docs_src"
TUTORIAL_DIR = ROOT / "docs" / "tutorial"

_GENERATED_HEADER = (
    "<!-- This file is generated from README.md by scripts/docs.py -- edit that instead. -->\n\n"
)

_DOCS_SRC_MARKER = re.compile(
    r"(<!--\s*docs_src:\s*(?P<name>[\w.\-/]+)\s*-->\n```(?P<lang>\w*)\n)(?P<body>.*?)(\n```)",
    re.DOTALL,
)


def _synced_markdown_content(text: str) -> str:
    """Replace every ``<!-- docs_src: name.py -->``-tagged fence with that file's current contents."""

    def replace(match: re.Match[str]) -> str:
        name = match.group("name")
        source_path = DOCS_SRC / name
        if not source_path.exists():
            raise FileNotFoundError(f"docs_src file referenced but missing: {source_path}")
        body = source_path.read_text().rstrip("\n")
        return f"{match.group(1)}{body}{match.group(5)}"

    return _DOCS_SRC_MARKER.sub(replace, text)


def sync(*, check: bool) -> bool:
    """Return True if everything is already in sync (or was written successfully)."""
    ok = True

    # README.md may itself embed docs_src fences; sync those first, since
    # docs/index.md is derived from README.md's *synced* content.
    current_readme = README.read_text()
    expected_readme = _synced_markdown_content(current_readme)
    if current_readme != expected_readme:
        if check:
            print(f"OUT OF SYNC: {README.relative_to(ROOT)} has a stale docs_src code block")
            ok = False
        else:
            README.write_text(expected_readme)
            print(f"wrote {README.relative_to(ROOT)}")

    expected_index = _GENERATED_HEADER + expected_readme
    current_index = DOCS_INDEX.read_text() if DOCS_INDEX.exists() else ""
    if current_index != expected_index:
        if check:
            print(
                f"OUT OF SYNC: {DOCS_INDEX.relative_to(ROOT)} does not match {README.relative_to(ROOT)}"
            )
            ok = False
        else:
            DOCS_INDEX.write_text(expected_index)
            print(f"wrote {DOCS_INDEX.relative_to(ROOT)}")

    for md_file in sorted(TUTORIAL_DIR.glob("*.md")):
        current = md_file.read_text()
        expected = _synced_markdown_content(current)
        if current != expected:
            if check:
                print(f"OUT OF SYNC: {md_file.relative_to(ROOT)} has a stale docs_src code block")
                ok = False
            else:
                md_file.write_text(expected)
                print(f"wrote {md_file.relative_to(ROOT)}")

    return ok


def build() -> None:
    if not sync(check=False):
        sys.exit(1)
    subprocess.run(["mkdocs", "build", "--strict"], cwd=ROOT, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    sync_parser = subparsers.add_parser("sync", help="Sync README/docs_src into docs/")
    sync_parser.add_argument("--check", action="store_true", help="Fail instead of writing changes")

    subparsers.add_parser("build", help="Sync, then `mkdocs build --strict`")

    args = parser.parse_args()

    if args.command == "sync":
        if not sync(check=args.check):
            sys.exit(1)
    elif args.command == "build":
        build()


if __name__ == "__main__":
    main()
