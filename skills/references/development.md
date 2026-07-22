# Development

## Repository Shape

Keep the `src/` layout:

```text
src/instantlyai/
  __init__.py
  _client.py
  _transport.py
  _pagination.py
  _exceptions.py
  _types.py
  models/
  resources/
tests/
docs/
docs_src/
scripts/
```

The `src/` layout helps tests catch packaging and import mistakes.

## Public Exports

Expose public client classes, exceptions, pagination helpers, and `__version__` from `instantlyai.__init__`.

Expose all resource classes from `instantlyai.resources.__init__` so `_client.py` can attach resource namespaces without import drift.

Keep `src/instantlyai/py.typed` so downstream type checkers know the package is typed.

## Resource Method Pattern

Use this pattern:

```python
def retrieve(self, id: str) -> Campaign:
    return Campaign.model_validate(self._get(f"/api/v2/campaigns/{id}"))
```

For create/update methods:

1. Prefer keyword-only arguments.
2. Use generated model types for nested request bodies.
3. Default optional omitted fields to `NOT_GIVEN`.
4. Build a body mapping.
5. Let `_base.py` and `_transport.py` omit `NOT_GIVEN` and serialize models/enums.

Do not duplicate auth, retry, JSON serialization, or error mapping in resource modules.

## Typed JSON

Use generated Pydantic models whenever possible. Use `JSONObject` only when the OpenAPI spec does not provide a useful schema.

Avoid `dict[str, Any]` in public resource signatures.

Internal transport/base request maps may use `dict[str, object]` because they are serialization boundaries.

## Tests

Cover:

* Client construction, auth precedence, and context managers.
* Resource namespace wiring.
* Transport headers, retries, backoff, response parsing, and typed exceptions.
* Pydantic model and enum serialization at the request boundary.
* Representative resource methods with mocked HTTP using `respx`.
* Docs examples in `docs_src/`.

## Docs

Keep docs-as-code:

* `README.md` is the PyPI landing page.
* `docs/index.md` is generated from the README.
* `docs_src/*.py` files are runnable sources for tutorial snippets.
* Use `scripts/docs.py sync --check` and `scripts/docs.py build` for docs validation.

## Validation

Run:

```bash
uv run ruff format --check .
uv run ruff check .
uv run ty check
uv run pytest
```

Use `scripts/lint.sh` and `scripts/test.sh` as local shortcuts.

