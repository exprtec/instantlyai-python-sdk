# Instantly Python SDK — Specification

> A typed, importable Python client for the Instantly.ai V2 API.
> This document specifies **how the SDK is built, structured, documented,
> versioned, and published** — not the individual API resources it wraps.
> Design conventions are modelled on the FastAPI repository, adapted for a
> client library rather than a web framework.

---

## 1. What this is

`instantlyai` is a typed, importable Python client for the Instantly.ai V2 API. It provides:

- A clean, resource-based client: `client.campaigns.list(...)`, `client.leads.bulk_add(...)`.
- Full end-to-end typing — usable by other code (including our own FastAPI
  backends) with real editor and type-checker support.
- Sync **and** async access from a single codebase.
- A **shared core** that a CLI and an MCP server consume downstream (see §10),
  so business logic lives in exactly one place.

It is the library layer: the foundation other interfaces build on.

---

## 2. Stack

| Concern            | Choice                                   | Notes |
|--------------------|------------------------------------------|-------|
| HTTP transport     | **httpx**                                | Sync + async from one library. |
| Models/validation  | **Pydantic v2**                          | Typed request/response models, (de)serialization. |
| Packaging/build    | **uv** (project + build via `pyproject.toml`) | Single source of project metadata; fast, unified toolchain. |
| Lint + format      | **ruff**                                 | Replaces black/isort/flake8; one config block. |
| Type checking      | **ty**                                   | Astral's type checker — same ecosystem as uv/ruff, fast; ship a `py.typed` marker. |
| Tests              | **pytest** + **respx**                   | respx mocks httpx without hitting the live API. |
| Docs               | **MkDocs + Material + mkdocstrings**     | Markdown-native, reference generated from docstrings. |
| Pre-commit         | **pre-commit** running ruff + ty         | Catch issues before CI. |

The lint/type/format tooling is the Astral stack throughout — **uv**, **ruff**,
**ty** — one vendor, consistent config, fast enough to run on every commit.

> **On `ty` maturity:** ty is in Beta (stable 1.0 targeted for 2026); Astral use
> it in their own projects and recommend it for motivated users. For this SDK
> that's a fine bet — but pin the ty version, use the official
> `astral-sh/ty-pre-commit` hook, and if a ty bug ever blocks CI, the fallback is
> to run mypy or pyright in that one job without changing anything else in the
> stack. Type *annotations* are tool-agnostic, so switching checkers later costs
> nothing.

**Accelerator:** Instantly publishes an OpenAPI 3.1 spec at
`https://api.instantly.ai/openapi/api_v2.json`. Use it to *generate the Pydantic
models* (e.g. datamodel-code-generator) rather than hand-writing 150+ schemas,
then hand-write the thin resource/transport layer on top. Regenerate models when
the API changes instead of chasing diffs manually. Treat generated code as
generated — never hand-edit it; re-run the generator.

---

## 3. Repository structure

Modelled on FastAPI's layout: `src/` package, docs-as-code with runnable
examples kept **outside** Markdown, a `scripts/` folder of thin task wrappers,
CI split into focused workflows.

```
python-sdk/
├── dist/                        # build artifacts (git-ignored)
├── src/
│   └── instantlyai/
│       ├── __init__.py          # public exports + __version__ (single source)
│       ├── py.typed             # PEP 561 marker — REQUIRED for typed installs
│       ├── _client.py           # Instantly / AsyncInstantly entrypoints
│       ├── _transport.py        # httpx wrapper: auth, retry, backoff, pagination
│       ├── _exceptions.py       # typed exception hierarchy
│       ├── _pagination.py       # auto-paginating iterators
│       ├── models/              # Pydantic models (generated from OpenAPI)
│       └── resources/           # one module per API resource group
│           ├── campaigns.py
│           ├── leads.py
│           └── ...
├── tests/                       # mirrors src/ layout; respx-based
├── docs/
│   ├── index.md                 # shares content w/ README (see §4)
│   ├── tutorial/                # prose, task-oriented guides
│   └── reference/               # mkdocstrings autodoc pages
├── docs_src/                    # runnable example scripts injected into docs
├── scripts/                     # docs.py, test.sh, lint.sh — thin wrappers
├── .github/workflows/
│   ├── test.yml                 # lint + type + test matrix
│   ├── docs.yml                 # build & deploy docs
│   └── publish.yml              # build + publish to PyPI (name must match §8)
├── pyproject.toml
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE                      # MIT — matches ecosystem, maximises adoption
└── mkdocs.yml
```

The `src/instantlyai/`, `dist/`, `LICENSE`, `pyproject.toml`, and `README.md`
scaffolding already exists from the name-reservation step (§8.1); the tree above
is the target this fills out to.

**Why `src/` layout:** it forces tests to run against the *installed* package,
not the working directory — catching packaging mistakes (missing files, bad
`py.typed`) before users do. FastAPI, and most serious libraries, use it.

**Public vs private:** underscore-prefixed modules (`_transport`, `_client`) are
internal; the public surface is whatever `instantlyai/__init__.py` re-exports.
This lets you refactor internals freely without breaking users — a semver-
friendly discipline (see §6).

---

## 4. Documentation

Three surfaces, each a different job. **Docstrings are the source of truth** for
the API reference — write them for extraction, not just for readers of source.

### 4.1 README (the highest-traffic surface)
The README *is* the PyPI landing page (`readme = "README.md"` in pyproject).
Order, top to bottom:
1. One-line description + badges (PyPI version, CI status, license, Python versions).
2. Install command.
3. A **working** quickstart snippet in the first screen — someone evaluating the
   SDK gives it ~30 seconds; the snippet must run as-is.
4. Links out to the docs site for depth.

Borrow FastAPI's trick: keep README and `docs/index.md` in sync via a script
(`scripts/docs.py`) rather than maintaining two copies by hand — a pre-commit
hook fails the build if they drift.

### 4.2 Docs site (MkDocs + Material + mkdocstrings)
- **Tutorial/** — prose, task-oriented ("Authenticate", "Run a campaign",
  "Handle rate limits", "Async usage"). Example code lives in `docs_src/` as
  real `.py` files and is *injected* into the Markdown, so every snippet in the
  docs is a file that CI actually runs — docs can't rot out of sync with the code.
  This is the single most valuable thing to copy from FastAPI.
- **Reference/** — generated from docstrings via mkdocstrings (`::: instantlyai.resources.campaigns`).
  Pick **one** docstring convention (Google-style recommended) and apply it everywhere.
- Enable Material's **versioned docs** (via `mike`) so `/latest` and pinned
  versions coexist — matters once you have users on older releases.
- Note: Material for MkDocs entered maintenance mode in early 2026 with a
  successor ("Zensical") reading existing `mkdocs.yml`. Current setup works today;
  expect a config migration later.

### 4.3 Supporting docs
- **CHANGELOG.md** — Keep a Changelog format, one entry per version, grouped
  Added/Changed/Fixed/Removed/Deprecated. This is where users check what a bump
  means before upgrading.
- **CONTRIBUTING.md** — env setup (`uv sync`), how to run tests/lint, how docs
  build, PR conventions.
- **examples/** — standalone runnable scripts. Both humans and agents copy from
  examples far more than they read prose.

---

## 5. SDK design conventions

Not resource-by-resource, but the rules every resource must follow:

- **Auth resolution order:** explicit `api_key` arg → `INSTANTLY_API_KEY` env var.
  Never require config files for basic use.
- **Sync + async parity:** ship `Instantly` and `AsyncInstantly` with identical
  surfaces. Generate one from the other (or template both) rather than letting
  them drift.
- **Typed exception hierarchy:** `InstantlyError` base, with
  `AuthenticationError`, `NotFoundError`, `RateLimitError`, `ValidationError`,
  `ServerError` mapped from HTTP status. Callers `except instantlyai.RateLimitError`,
  never inspect status codes themselves.
- **Auto-retry with exponential backoff** on 429/5xx, honouring `Retry-After`.
  Configurable max retries; sane default (e.g. 3).
- **Auto-paginating iterators:** `for c in client.campaigns.list():` transparently
  walks every page via the cursor. Also expose a raw single-page method for
  callers who want manual control.
- **Return typed models, not raw dicts.** `list()` yields `Campaign` objects.
- **No global mutable state.** All config lives on the client instance, so
  multiple clients (e.g. multiple workspaces) coexist — relevant for agency use
  across multiple Instantly workspaces.
- **Timeouts explicit and overridable**, with a documented default.

---

## 6. Versioning policy

**Semantic Versioning (`MAJOR.MINOR.PATCH`)**, single source of truth in
`instantlyai/__init__.py::__version__`, read by the build backend.

- **PATCH** — bug fixes, no surface change.
- **MINOR** — new resources/methods/optional args, backwards compatible.
- **MAJOR** — anything that breaks existing calling code.
- **Pre-1.0:** start at `0.x`. While `0.x`, minor bumps *may* break — state this
  explicitly in the README so users pin accordingly. Cut `1.0.0` only when the
  public surface is stable enough to promise compatibility.
- **Deprecation policy:** never remove without a deprecation cycle. Emit
  `DeprecationWarning`, document in CHANGELOG under Deprecated for at least one
  minor release before removal in the next major.
- **Dependency pinning (as a library, not an app):** pin *loosely*
  (`httpx>=0.27,<1.0`), never exact. Hard pins are for applications; a library
  that hard-pins breaks other people's dependency resolution. This is one of the
  most common ways SDKs cause install failures.
- **The "public surface" is only what `instantlyai/__init__.py` exports** —
  underscore internals can change in any release without it counting as a break.

---

## 7. CI / quality gates

Split workflows (FastAPI-style) rather than one mega-workflow:
- **test.yml** — ruff (lint+format check), ty, pytest across a Python matrix
  (3.10–3.13) and, if Windows matters, OS matrix. Coverage upload optional.
- **docs.yml** — build docs, deploy on merge to main / on release.
- **publish.yml** — build + publish (see §8). Kept separate from build for
  security (see §8.3).

Every gate runs in CI *and* locally via pre-commit so contributors get the same
answers before pushing.

---

## 8. Publishing to PyPI

### 8.1 Naming & reservation — DONE

The package name is **`instantlyai`**, and the name is already claimed via a
minimal placeholder upload (the `src/instantlyai/` + `pyproject.toml` + `LICENSE`
+ `README.md` scaffolding). No further reservation work is needed — real releases
just bump the version above the placeholder's and overwrite its content.

Context for why this was the right move (and how to redo it if ever needed):
PyPI has **no dedicated "reserve a name" feature** — the register command was
removed years ago, so the only way to hold a name is to upload a real (minimal)
package with it. The placeholder does exactly that: valid `pyproject.toml` with
`name = "instantlyai"`, a low `version`, and a `Development Status :: 1 - Planning`
classifier holds the name while real code is built.

Two follow-ups worth confirming, if not already done:
- **Claim `instantlyai` on TestPyPI too**, so the dry-run pipeline (§8.4) runs
  against the identical name.
- **Keep ecosystem names consistent** — the matching GitHub repo, and (if the
  npm CLI/MCP ship later) the npm name.

### 8.2 Metadata that matters in `pyproject.toml`
- `readme = "README.md"` → README becomes the PyPI page.
- `classifiers` → Python versions, license, dev status (drives filtering/trust).
- `keywords` → PyPI search discoverability.
- `project.urls` → Homepage, Repository, Documentation, Issues, Changelog —
  these render as links on the PyPI sidebar.
- `requires-python = ">=3.10"` → matches your test matrix.
- `license` = MIT.

### 8.3 Publish with Trusted Publishing (OIDC) — not a stored token
Current best practice, and specifically recommended after recent supply-chain
incidents: **no long-lived `PYPI_API_TOKEN` in the repo.** PyPI mints a
short-lived credential to GitHub Actions via OIDC at publish time.

Setup:
1. On PyPI: project → Settings → Publishing → add a trusted publisher; specify
   your GitHub `owner/repo` and the **exact workflow filename** (`publish.yml`).
   A filename mismatch is the #1 setup failure.
2. Separate the **build** job from the **publish** job — a deliberate security
   recommendation, not just tidiness. Build produces sdist + wheel into `dist/`;
   publish uploads via `pypa/gh-action-pypi-publish`.
3. Put the publish job in a GitHub **environment** (e.g. `pypi`), optionally with
   required reviewers — otherwise anyone who can push can cut a release.
4. Trusted Publishing auto-generates Sigstore **attestations** for uploaded files
   (provenance) — leave on.

### 8.4 Release flow
1. Dry-run to **TestPyPI** first (`repository-url: https://test.pypi.org/legacy/`),
   `pip install` from there, confirm it imports and is typed.
2. Bump `__version__`, update CHANGELOG.
3. Tag `vX.Y.Z` (semver) and push — CI builds, publishes, deploys docs.
4. Releases are triggered by tags/GitHub Releases, never manual `twine` from a laptop.

---

## 9. Definition of done (per release)
- [ ] `ruff`, `ty`, `pytest` green across the matrix.
- [ ] `py.typed` shipped; a fresh install type-checks in a downstream project.
- [ ] README quickstart runs as-is; docs build clean; examples in `docs_src/` execute in CI.
- [ ] CHANGELOG updated; version bumped in exactly one place.
- [ ] TestPyPI dry-run installs and imports.
- [ ] Published via OIDC (no token), attestations attached.

---

## 10. Downstream consumers (context)
This SDK is the shared core. Two consumers build on it as *separate* packages
that depend on `instantlyai`:
- **CLI** (Typer) — one thin command per resource method.
- **MCP server** (FastMCP) — wraps each resource method as a tool.

A fix or new endpoint in `resources/` propagates to both with zero duplicated
logic. Keeping them in their own packages keeps `instantlyai`'s dependency
footprint minimal for anyone who wants just the library.