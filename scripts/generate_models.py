#!/usr/bin/env python3
"""Regenerate ``instantlyai.models`` from the Instantly OpenAPI spec.

Usage:
    uv run scripts/generate_models.py [path-or-url]

Fetches the spec (default: the live Instantly OpenAPI document), runs it
through datamodel-code-generator to produce ``models/_generated.py``, then
rewrites ``models/__init__.py`` with re-exports of every top-level model.

The generated file is never hand-edited -- re-run this script instead.
"""

from __future__ import annotations

import ast
import subprocess
import sys
import urllib.request
from pathlib import Path

DEFAULT_SPEC_URL = "https://api.instantly.ai/openapi/api_v2.json"
ROOT = Path(__file__).resolve().parent.parent
MODELS_DIR = ROOT / "src" / "instantlyai" / "models"
GENERATED_FILE = MODELS_DIR / "_generated.py"
INIT_FILE = MODELS_DIR / "__init__.py"

CODEGEN_ARGS = [
    "--input-file-type",
    "openapi",
    "--output-model-type",
    "pydantic_v2.BaseModel",
    "--target-python-version",
    "3.10",
    "--use-schema-description",
    "--field-constraints",
    "--use-standard-collections",
    "--use-union-operator",
    "--collapse-root-models",
    "--enum-field-as-literal",
    "one",
    "--use-double-quotes",
    "--disable-timestamp",
]


def fetch_spec(source: str) -> Path:
    if source.startswith("http://") or source.startswith("https://"):
        dest = MODELS_DIR / ".openapi-spec.json"
        with urllib.request.urlopen(source) as response:
            dest.write_bytes(response.read())
        return dest
    return Path(source)


def run_codegen(spec_path: Path) -> None:
    subprocess.run(
        [
            sys.executable,
            "-m",
            "datamodel_code_generator",
            "--input",
            str(spec_path),
            "--output",
            str(GENERATED_FILE),
            *CODEGEN_ARGS,
        ],
        check=True,
    )


def top_level_names(source: str) -> list[str]:
    tree = ast.parse(source)
    names: list[str] = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            names.append(node.name)
        elif isinstance(node, ast.Assign):
            names.extend(t.id for t in node.targets if isinstance(t, ast.Name))
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            names.append(node.target.id)
    return sorted(set(names))


def write_init(names: list[str]) -> None:
    joined = ",\n    ".join(names)
    content = (
        '"""Public Pydantic models, generated from the Instantly OpenAPI spec.\n\n'
        "Do not hand-edit this package -- re-run ``scripts/generate_models.py``.\n"
        '"""\n\n'
        "from ._generated import (\n"
        f"    {joined},\n"
        ")\n\n"
        f"__all__ = [\n    " + ",\n    ".join(f'"{n}"' for n in names) + ",\n]\n"
    )
    INIT_FILE.write_text(content)


def main() -> None:
    source = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SPEC_URL
    spec_path = fetch_spec(source)
    run_codegen(spec_path)
    names = top_level_names(GENERATED_FILE.read_text())
    write_init(names)
    print(f"Wrote {len(names)} models to {INIT_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
