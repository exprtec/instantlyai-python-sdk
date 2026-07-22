# Contributing

## Setup

```bash
git clone https://github.com/exprtec/instantlyai-python-sdk.git
cd instantlyai-python-sdk
uv sync                    # installs the package + dev/codegen/docs dependency groups
uv run pre-commit install  # runs ruff + ty on every commit
```

`uv sync` installs everything needed for development, tests, and docs (see
`[dependency-groups]` in `pyproject.toml`). No separate `pip install -e .[dev]` step.

## Running checks locally

These are exactly what CI runs:

```bash
scripts/lint.sh   # ruff format --check, ruff check, ty check
scripts/test.sh   # pytest (extra args forwarded, e.g. scripts/test.sh -k campaigns)
uv run python scripts/docs.py build   # sync docs, then `mkdocs build --strict`
```

## Project layout

- `src/instantlyai/models/` -- generated from Instantly's OpenAPI spec. **Never hand-edit
  `_generated.py`** -- re-run `uv run scripts/generate_models.py` instead (regenerates
  from the live spec by default; pass a local path to use a saved copy).
- `src/instantlyai/resources/` -- hand-written thin wrappers, one module per API
  resource group. `campaigns.py` and `accounts.py` are the reference implementations;
  match their conventions (see the module docstring in `resources/_base.py`) when
  adding or touching a resource.
- `docs_src/*.py` -- runnable example scripts. These are executed in CI
  (`tests/test_examples.py`) and embedded into `README.md` / `docs/tutorial/*.md` via
  `<!-- docs_src: name.py -->` markers, kept in sync by `scripts/docs.py sync`.
- `tests/` mirrors `src/` and uses `respx` to mock httpx -- no test ever hits the live
  API.

## Adding or changing a resource method

1. Check the endpoint's shape in the OpenAPI spec
   (`https://api.instantly.ai/openapi/api_v2.json`).
2. Add the method to both the sync and async class in the resource module, matching
   the existing style (`NOT_GIVEN` sentinel for optional params, typed nested request
   bodies using generated models where they exist, `JSONObject`/`_list[JSONObject]`
   for genuinely untyped ad-hoc responses).
3. If the method is a true cursor-paginated list (`{"items": [...], "next_starting_after": ...}`),
   name it `list`, define it **last** in the class body, and use `self._paginate(...)`.
   A class with a `list()` method needs the `_list = list` alias (see any existing
   resource file) to avoid a real static-analysis gotcha where `list` as a method name
   shadows the builtin for every other annotation in that class body.
4. Add or update tests in `tests/test_resources.py`.
5. Run `scripts/lint.sh` and `scripts/test.sh` before opening a PR.

## Docs

- Prose goes in `docs/tutorial/`; generated API reference goes in `docs/reference/`
  (mkdocstrings, pulling from docstrings -- write docstrings for extraction, Google
  style).
- Any code shown in a doc page that's meant to be runnable belongs in `docs_src/` as a
  real `.py` file, referenced from the Markdown via `<!-- docs_src: name.py -->`
  immediately above a fenced code block. Run `uv run python scripts/docs.py sync`
  after editing a `docs_src` file to update the embedded copies.

## Versioning

Single source of truth: `src/instantlyai/_version.py`. Bump it, update
`CHANGELOG.md`, and open a PR -- tagging `vX.Y.Z` on `main` triggers the release
pipeline (build, publish to PyPI via Trusted Publishing, deploy docs).

## Pull requests

- Keep PRs focused; one logical change per PR.
- Update `CHANGELOG.md` under `[Unreleased]` for any user-facing change.
- CI must be green (`test.yml`) before merge.
