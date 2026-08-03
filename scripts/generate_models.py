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
import json
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
    dest = MODELS_DIR / ".openapi-spec.json"
    if source.startswith("http://") or source.startswith("https://"):
        with urllib.request.urlopen(source) as response:
            dest.write_bytes(response.read())
    else:
        dest.write_bytes(Path(source).read_bytes())
    return dest


def patch_spec(spec_path: Path) -> None:
    """Correct known gaps/bugs in the upstream spec before codegen sees it.

    Both patches below are tracked as issues against Instantly's published
    OpenAPI document; they live here (rather than as post-codegen edits to
    ``_generated.py``) so they survive the next regeneration.
    """
    spec = json.loads(spec_path.read_text())
    schemas = spec["components"]["schemas"]

    # `GET /accounts?include_tags=true` embeds a `tags` array per account, but
    # the spec only declares that on an anonymous inline extension of the
    # `Account` schema used by that one response, not on `Account` itself.
    # datamodel-code-generator drops the inline extension, so the generated
    # `Account` model (which has `extra="forbid"`) has no `tags` field and
    # raises a `ValidationError` on every `include_tags=True` call. Move the
    # property onto `Account` directly, matching what the API actually sends.
    schemas["Account"]["properties"]["tags"] = {
        "type": ["array", "null"],
        "description": "Tags associated with the account, set to `include_tags` to populate",
        "items": {
            "type": "object",
            # Explicit `additionalProperties: false` rather than relying on the
            # generator's default for a nested anonymous object without one --
            # that default isn't stable across generator versions (0.69.0 stopped
            # emitting `extra="forbid"` for this exact shape between the last
            # regen and this one, though nothing else in the spec changed), and
            # silently losing strictness here would reopen the exact class of bug
            # this patch exists to fix (an unannounced field breaking validation).
            "additionalProperties": False,
            "properties": {
                "id": {
                    "type": "string",
                    "description": "Unique identifier for the custom tag",
                },
                "label": {
                    "type": "string",
                    "description": "Display label for the custom tag",
                },
                "description": {
                    "type": ["string", "null"],
                    "description": "Detailed description of the custom tag purpose",
                },
            },
        },
    }

    # `CustomTagMapping.resource_type`'s free-text description has the
    # account/campaign mapping backwards relative to its own
    # `x-enumDescriptions` (1: Account, 2: Campaign) and relative to the
    # `toggle-resource` endpoint, which agrees with `x-enumDescriptions`.
    schemas["CustomTagMapping"]["properties"]["resource_type"]["description"] = (
        "Resource type of custom tag, can be 1 for accounts or 2 for campaigns"
    )

    # `CustomTagMapping.resource_id` is declared `format: uuid`, but it only
    # holds a UUID for campaign mappings (`resource_type=2`). Account mappings
    # (`resource_type=1`) hold the account's email address, since accounts are
    # addressed by email everywhere else in the API. The `uuid` format hint
    # doesn't match actual API behavior for `resource_type=1`, so drop it --
    # the field is a plain string whose shape depends on `resource_type`.
    schemas["CustomTagMapping"]["properties"]["resource_id"].pop("format", None)

    # Draft campaigns can be returned with `"campaign_schedule": {}` before a
    # sending window has ever been configured. The upstream schema requires
    # `campaign_schedule.schedules` with at least one item, which makes
    # `campaigns.list()` and `campaigns.retrieve()` raise `ValidationError` for
    # otherwise valid draft campaigns. Treat a missing schedules key as an empty
    # schedule so response validation matches live API behavior.
    campaign_schedule = schemas["Campaign"]["properties"]["campaign_schedule"]
    schedules = campaign_schedule["properties"]["schedules"]
    schedules.pop("minItems", None)
    schedules["default"] = []
    if "schedules" in campaign_schedule.get("required", []):
        campaign_schedule["required"].remove("schedules")

    spec_path.write_text(json.dumps(spec))


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
    patch_spec(spec_path)
    run_codegen(spec_path)
    names = top_level_names(GENERATED_FILE.read_text())
    write_init(names)
    print(f"Wrote {len(names)} models to {INIT_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
