"""Background job resource: ``client.background_jobs``."""

from __future__ import annotations

from typing import Any, Literal

from .._pagination import AsyncCursorPage, SyncCursorPage
from .._transport import NOT_GIVEN, NotGiven
from ..models import BackgroundJob
from ._base import AsyncAPIResource, SyncAPIResource

__all__ = ["AsyncBackgroundJobs", "BackgroundJobs"]

# Both resource classes define a `list()` method, which shadows the builtin
# `list` for annotation resolution anywhere else in this module's class
# bodies -- alias it once and use `_list[...]` instead of bare `list[...]`.
_list = list

_BackgroundJobType = Literal[
    "move-leads",
    "import-leads",
    "export-leads",
    "update-warmup-accounts",
    "rename-variable",
    "broadcast-ai-generate",
    "broadcast-website-scrape",
    "import-subscribers-from-crm",
    "resync-subscriber-crm-tags",
]
_BackgroundJobEntityType = Literal[
    "list", "campaign", "workspace", "broadcast", "subscriber-group-sync", "subscriber-group"
]
_SortColumn = Literal["created_at", "updated_at"]
_SortOrder = Literal["asc", "desc"]


class BackgroundJobs(SyncAPIResource):
    def retrieve(self, id: str, *, data_fields: str | NotGiven = NOT_GIVEN) -> BackgroundJob:
        """Get a single background job by ID."""
        return BackgroundJob.model_validate(
            self._get(f"/api/v2/background-jobs/{id}", params={"data_fields": data_fields})
        )

    def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        ids: str | NotGiven = NOT_GIVEN,
        included_ids: str | NotGiven = NOT_GIVEN,
        excluded_ids: str | NotGiven = NOT_GIVEN,
        type: _BackgroundJobType | NotGiven = NOT_GIVEN,
        entity_type: _BackgroundJobEntityType | NotGiven = NOT_GIVEN,
        entity_id: str | NotGiven = NOT_GIVEN,
        status: str | NotGiven = NOT_GIVEN,
        sort_column: _SortColumn | NotGiven = NOT_GIVEN,
        sort_order: _SortOrder | NotGiven = NOT_GIVEN,
    ) -> SyncCursorPage[BackgroundJob]:
        """List background jobs. Auto-paginates: `for j in client.background_jobs.list(): ...`."""

        def fetch_page(cursor: str | None) -> Any:
            return self._get(
                "/api/v2/background-jobs",
                params={
                    "limit": limit,
                    "starting_after": cursor if cursor is not None else starting_after,
                    "ids": ids,
                    "included_ids": included_ids,
                    "excluded_ids": excluded_ids,
                    "type": type,
                    "entity_type": entity_type,
                    "entity_id": entity_id,
                    "status": status,
                    "sort_column": sort_column,
                    "sort_order": sort_order,
                },
            )

        return self._paginate(BackgroundJob, fetch_page)


class AsyncBackgroundJobs(AsyncAPIResource):
    async def retrieve(self, id: str, *, data_fields: str | NotGiven = NOT_GIVEN) -> BackgroundJob:
        """Get a single background job by ID."""
        return BackgroundJob.model_validate(
            await self._get(f"/api/v2/background-jobs/{id}", params={"data_fields": data_fields})
        )

    async def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        ids: str | NotGiven = NOT_GIVEN,
        included_ids: str | NotGiven = NOT_GIVEN,
        excluded_ids: str | NotGiven = NOT_GIVEN,
        type: _BackgroundJobType | NotGiven = NOT_GIVEN,
        entity_type: _BackgroundJobEntityType | NotGiven = NOT_GIVEN,
        entity_id: str | NotGiven = NOT_GIVEN,
        status: str | NotGiven = NOT_GIVEN,
        sort_column: _SortColumn | NotGiven = NOT_GIVEN,
        sort_order: _SortOrder | NotGiven = NOT_GIVEN,
    ) -> AsyncCursorPage[BackgroundJob]:
        """List background jobs. Auto-paginates: `async for j in await client.background_jobs.list(): ...`."""

        async def fetch_page(cursor: str | None) -> Any:
            return await self._get(
                "/api/v2/background-jobs",
                params={
                    "limit": limit,
                    "starting_after": cursor if cursor is not None else starting_after,
                    "ids": ids,
                    "included_ids": included_ids,
                    "excluded_ids": excluded_ids,
                    "type": type,
                    "entity_type": entity_type,
                    "entity_id": entity_id,
                    "status": status,
                    "sort_column": sort_column,
                    "sort_order": sort_order,
                },
            )

        return await self._paginate(BackgroundJob, fetch_page)
