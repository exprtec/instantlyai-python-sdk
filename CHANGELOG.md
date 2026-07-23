# Changelog

All notable changes to this project are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versioning follows
[Semantic Versioning](https://semver.org/) (`0.x` -- minor bumps may break, see
[README](https://github.com/exprtec/instantlyai-python-sdk#readme)).

## [Unreleased]

## [0.1.3] - 2026-07-23

### Fixed

- `update()` parameters that correspond to nullable (`T | None`) model fields were typed
  as `T | NotGiven`, dropping the `None` branch the model itself allows. This didn't
  affect runtime behavior (`None` already passed through and serialized as JSON `null`,
  correctly clearing the field), but callers who legitimately wanted to clear a nullable
  field (e.g. `accounts.update(..., signature=None)`, `campaigns.update(..., daily_limit=None)`)
  got a static type error. Corrected across every resource's `update()` (sync and async):
  `accounts`, `campaigns`, `custom_tags`, `emails`, `inbox_placement_tests`, `lead_labels`,
  `lead_lists`, `leads`, `subsequences`, `webhooks`, `workspace_members`, `workspaces`.

## [0.1.2] - 2026-07-23

### Fixed

- `Account.model_validate()` no longer raises on `client.accounts.list(include_tags=True)`.
  The generated `Account` model was missing the `tags` field the API embeds per account
  when `include_tags=true` is set, so every call crashed against real data
  (`extra="forbid"` rejected the extra `tags` array).
- Corrected the reversed `resource_type` mapping in the generated `CustomTagMapping` /
  `ResourceType` docs. It previously read "1 for campaigns or 2 for accounts", the
  opposite of what the API and `custom_tags.py` actually use (`1` = Account, `2` =
  Campaign) -- purely a doc/docstring fix, the underlying values were never wrong.
- `scripts/generate_models.py` now patches both gaps in the upstream OpenAPI spec
  before codegen runs, so future regenerations don't silently reintroduce them.

## [0.1.0] - 2026-07-22

### Added

- Initial functional release: sync (`Instantly`) and async (`AsyncInstantly`) clients
  covering every Instantly.ai V2 API resource (campaigns, leads, accounts, workspaces,
  webhooks, inbox placement, DFY email accounts, SuperSearch enrichment, and more).
- Typed Pydantic v2 models generated from Instantly's OpenAPI spec.
- Typed exception hierarchy (`InstantlyError` and subclasses) mapped from HTTP status.
- Auto-retry with exponential backoff on `429`/`5xx`, honouring `Retry-After`.
- Auto-paginating `list()` methods (`SyncCursorPage` / `AsyncCursorPage`).
- `py.typed` marker for downstream type-checking.

## [0.0.1] - 2026-07-22

### Added

- Placeholder release to reserve the `instantlyai` name on PyPI.
