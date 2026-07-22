# Generated Models

## Source of Truth

Generated Pydantic models live in:

```text
src/instantlyai/models/_generated.py
```

The public re-export file is:

```text
src/instantlyai/models/__init__.py
```

Do not hand-edit generated models. Regenerate them with:

```bash
uv run scripts/generate_models.py
```

Pass a local spec path when reproducibility matters:

```bash
uv run scripts/generate_models.py path/to/api_v2.json
```

## Resource Signatures

When the generated output contains a useful model for a structured field, resource methods should use it directly:

* `CampaignSchedule`, `Sequence`, `AutoVariantSelect`, `LimitEmailsPerCompanyOverride`, `ProviderRoutingRule`
* `Warmup`
* `Conditions`, `SubsequenceSchedule`, `Sequence1`
* `Schedule1`, `RecipientsLabel`, `Automation`
* `Body`
* `Payload`
* `EventType`

Use `model_validate(...)` in examples when constructing models from dict-like user data.

## Serialization

`_transport.omit_not_given(...)` serializes Pydantic models and enums with JSON-compatible values before sending requests.

Do not manually call `model_dump(...)` inside each resource method unless there is a resource-specific reason.

## Type Checking

Generated models are excluded from Ruff and ty because they are machine output:

```toml
[tool.ruff]
extend-exclude = ["src/instantlyai/models/_generated.py"]

[tool.ty.src]
exclude = ["src/instantlyai/models/_generated.py"]
```

Keep handwritten SDK code type-checkable even when generated code is excluded.

