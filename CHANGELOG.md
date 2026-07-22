# Changelog

All notable changes to this project are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versioning follows
[Semantic Versioning](https://semver.org/) (`0.x` -- minor bumps may break, see
[README](https://github.com/exprtec/instantlyai-python-sdk#readme)).

## [Unreleased]

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
