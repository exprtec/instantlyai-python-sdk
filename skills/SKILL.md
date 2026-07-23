---
name: instantlyai
description: Instantly.ai Python SDK conventions. Use when writing or reviewing code that calls the Instantly.ai API through the `instantlyai` package, or when modifying this SDK's client, transport, resources, generated Pydantic models, tests, docs, or release tooling.
---

# instantlyai

Official project skill for working with the `instantlyai` Python SDK and code that uses it.

## Quick Reference

* Install: `uv add instantlyai` or `pip install instantlyai`; requires Python 3.10+.
* Clients: use `Instantly` for sync code and `AsyncInstantly` for async code; see [SDK Usage](references/sdk-usage.md).
* Auth: pass `api_key=...` or set `INSTANTLY_API_KEY`; construction fails fast if neither exists.
* Resources: use client namespaces like `client.campaigns`, `client.leads`, `client.accounts`, and `client.webhooks`; do not hand-build URLs in user code.
* Models: use generated models from `instantlyai.models` for structured bodies; do not pass raw dicts when a resource signature has a model type.
* Pagination: `list()` returns cursor page objects that auto-paginate when iterated; see [SDK Usage](references/sdk-usage.md).
* Errors: catch typed SDK exceptions (`NotFoundError`, `RateLimitError`, `InstantlyError`) instead of checking status codes.
* SDK development: keep `src/`, generated models, resources, tests, and docs wired as described in [Development](references/development.md).
* Model generation: update generated Pydantic models only through `scripts/generate_models.py`; see [Generated Models](references/generated-models.md).
* Validation: run `uv run ruff format --check .`, `uv run ruff check .`, `uv run ty check`, and `uv run pytest`.

## Use the Client Surface

Create a client and call resource methods rather than calling HTTPX directly:

```python
import instantlyai

with instantlyai.Instantly() as client:
    campaign = client.campaigns.retrieve(campaign_id)
```

For async code, use the async client and await resource calls:

```python
import instantlyai

async with instantlyai.AsyncInstantly() as client:
    campaign = await client.campaigns.retrieve(campaign_id)
```

## Use Generated Models for Structured Input

Resource methods expose useful Pydantic model types for nested request bodies. Build those models explicitly:

```python
from instantlyai.models import CampaignSchedule

schedule = CampaignSchedule.model_validate(
    {
        "schedules": [
            {
                "name": "Business hours",
                "timing": {"from": "09:00", "to": "17:00"},
                "days": {"1": True, "2": True, "3": True, "4": True, "5": True},
                "timezone": "Etc/GMT+12",
            }
        ]
    }
)
campaign = client.campaigns.create(name="Q1 Outbound", campaign_schedule=schedule)
```

Do not replace model-typed parameters with `dict[str, Any]`. If the OpenAPI spec lacks a useful schema, use `JSONObject` from `instantlyai._types` rather than `Any`.

## One HTTP Operation per Method

Keep each resource method mapped to one API operation. Use method names like `create`, `retrieve`, `update`, `delete`, `list`, or an explicit action name such as `activate`, `pause`, `bulk_add`, or `enable_warmup`.

Do not combine multiple API calls inside a resource method unless the SDK explicitly documents a composed helper.

## Keep Resource Methods Thin

Resource methods should:

1. Accept typed keyword arguments.
2. Build a body or params mapping.
3. Call `_get`, `_post`, `_patch`, or `_delete`.
4. Validate typed responses with `Model.model_validate(...)` when a model exists.

Keep retry, auth, serialization, pagination, and error mapping in shared infrastructure.

## Preserve Omitted vs Null

Use `NOT_GIVEN` for omitted optional arguments. Omit a kwarg to leave a field unchanged. Pass `None` only when the API intentionally distinguishes explicit null from omission.

If the corresponding model field is typed `T | None` (nullable in the read model), the parameter must be typed `T | None | NotGiven`, not just `T | NotGiven` — otherwise callers clearing the field with `None` get a static type error even though it works at runtime.

## Use the Project Tooling

Run local checks before finishing SDK changes:

```bash
uv run ruff format --check .
uv run ruff check .
uv run ty check
uv run pytest
```

For docs changes, keep `README.md`, `docs/`, and `docs_src/` synchronized with `scripts/docs.py`.

