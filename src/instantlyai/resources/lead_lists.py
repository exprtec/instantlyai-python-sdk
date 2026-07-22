"""Lead list resource: ``client.lead_lists``."""

from __future__ import annotations

from typing import Any

from .._pagination import AsyncCursorPage, SyncCursorPage
from .._transport import NOT_GIVEN, NotGiven
from .._types import JSONObject
from ..models import LeadList
from ._base import AsyncAPIResource, SyncAPIResource

__all__ = ["AsyncLeadLists", "LeadLists"]

# Both resource classes define a `list()` method, which shadows the builtin
# `list` for annotation resolution anywhere else in this module's class
# bodies -- alias it once and use `_list[...]` instead of bare `list[...]`.
_list = list


class LeadLists(SyncAPIResource):
    def create(
        self,
        *,
        name: str,
        has_enrichment_task: bool | NotGiven = NOT_GIVEN,
        owned_by: str | NotGiven = NOT_GIVEN,
    ) -> LeadList:
        """Create lead list."""
        return LeadList.model_validate(
            self._post(
                "/api/v2/lead-lists",
                json={
                    "name": name,
                    "has_enrichment_task": has_enrichment_task,
                    "owned_by": owned_by,
                },
            )
        )

    def retrieve(self, id: str) -> LeadList:
        """Get lead list."""
        return LeadList.model_validate(self._get(f"/api/v2/lead-lists/{id}"))

    def update(
        self,
        id: str,
        *,
        has_enrichment_task: bool | NotGiven = NOT_GIVEN,
        owned_by: str | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
    ) -> LeadList:
        """Patch lead list. Omitted fields are left unchanged."""
        return LeadList.model_validate(
            self._patch(
                f"/api/v2/lead-lists/{id}",
                json={
                    "has_enrichment_task": has_enrichment_task,
                    "owned_by": owned_by,
                    "name": name,
                },
            )
        )

    def delete(self, id: str) -> LeadList:
        """Delete lead list."""
        return LeadList.model_validate(self._delete(f"/api/v2/lead-lists/{id}"))

    def verification_stats(self, id: str) -> JSONObject:
        """Get verification statistics for a lead list."""
        return self._get(f"/api/v2/lead-lists/{id}/verification-stats")

    def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        has_enrichment_task: bool | NotGiven = NOT_GIVEN,
        search: str | NotGiven = NOT_GIVEN,
    ) -> SyncCursorPage[LeadList]:
        """List lead list. Auto-paginates: `for l in client.lead_lists.list(): ...`."""

        def fetch_page(cursor: str | None) -> Any:
            return self._get(
                "/api/v2/lead-lists",
                params={
                    "limit": limit,
                    "starting_after": cursor if cursor is not None else starting_after,
                    "has_enrichment_task": has_enrichment_task,
                    "search": search,
                },
            )

        return self._paginate(LeadList, fetch_page)


class AsyncLeadLists(AsyncAPIResource):
    async def create(
        self,
        *,
        name: str,
        has_enrichment_task: bool | NotGiven = NOT_GIVEN,
        owned_by: str | NotGiven = NOT_GIVEN,
    ) -> LeadList:
        """Create lead list."""
        return LeadList.model_validate(
            await self._post(
                "/api/v2/lead-lists",
                json={
                    "name": name,
                    "has_enrichment_task": has_enrichment_task,
                    "owned_by": owned_by,
                },
            )
        )

    async def retrieve(self, id: str) -> LeadList:
        """Get lead list."""
        return LeadList.model_validate(await self._get(f"/api/v2/lead-lists/{id}"))

    async def update(
        self,
        id: str,
        *,
        has_enrichment_task: bool | NotGiven = NOT_GIVEN,
        owned_by: str | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
    ) -> LeadList:
        """Patch lead list. Omitted fields are left unchanged."""
        return LeadList.model_validate(
            await self._patch(
                f"/api/v2/lead-lists/{id}",
                json={
                    "has_enrichment_task": has_enrichment_task,
                    "owned_by": owned_by,
                    "name": name,
                },
            )
        )

    async def delete(self, id: str) -> LeadList:
        """Delete lead list."""
        return LeadList.model_validate(await self._delete(f"/api/v2/lead-lists/{id}"))

    async def verification_stats(self, id: str) -> JSONObject:
        """Get verification statistics for a lead list."""
        return await self._get(f"/api/v2/lead-lists/{id}/verification-stats")

    async def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        has_enrichment_task: bool | NotGiven = NOT_GIVEN,
        search: str | NotGiven = NOT_GIVEN,
    ) -> AsyncCursorPage[LeadList]:
        """List lead list. Auto-paginates: `async for l in await client.lead_lists.list(): ...`."""

        async def fetch_page(cursor: str | None) -> Any:
            return await self._get(
                "/api/v2/lead-lists",
                params={
                    "limit": limit,
                    "starting_after": cursor if cursor is not None else starting_after,
                    "has_enrichment_task": has_enrichment_task,
                    "search": search,
                },
            )

        return await self._paginate(LeadList, fetch_page)
