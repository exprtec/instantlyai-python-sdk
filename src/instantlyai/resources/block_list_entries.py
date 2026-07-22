"""Block list entry resource: ``client.block_list_entries``."""

from __future__ import annotations

from typing import Any

from .._pagination import AsyncCursorPage, SyncCursorPage
from .._transport import NOT_GIVEN, NotGiven
from .._types import JSONObject
from ..models import BlockListEntry
from ._base import AsyncAPIResource, SyncAPIResource

__all__ = ["AsyncBlockListEntries", "BlockListEntries"]

# Both resource classes define a `list()` method, which shadows the builtin
# `list` for annotation resolution anywhere else in this module's class
# bodies -- alias it once and use `_list[...]` instead of bare `list[...]`.
_list = list


class BlockListEntries(SyncAPIResource):
    def create(self, *, bl_value: str) -> BlockListEntry:
        """Create block list entry."""
        return BlockListEntry.model_validate(
            self._post("/api/v2/block-lists-entries", json={"bl_value": bl_value})
        )

    def retrieve(self, id: str) -> BlockListEntry:
        """Get block list entry."""
        return BlockListEntry.model_validate(self._get(f"/api/v2/block-lists-entries/{id}"))

    def update(self, id: str, *, bl_value: str | NotGiven = NOT_GIVEN) -> BlockListEntry:
        """Patch block list entry."""
        return BlockListEntry.model_validate(
            self._patch(f"/api/v2/block-lists-entries/{id}", json={"bl_value": bl_value})
        )

    def delete(self, id: str) -> BlockListEntry:
        """Delete block list entry."""
        return BlockListEntry.model_validate(self._delete(f"/api/v2/block-lists-entries/{id}"))

    def delete_all(
        self,
        *,
        domains_only: bool | NotGiven = NOT_GIVEN,
        search: str | NotGiven = NOT_GIVEN,
    ) -> _list[BlockListEntry]:
        """Delete all block list entries."""
        return [
            BlockListEntry.model_validate(item)
            for item in self._delete(
                "/api/v2/block-lists-entries",
                params={"domains_only": domains_only, "search": search},
            )
        ]

    def bulk_create(self, *, bl_values: _list[str]) -> JSONObject:
        """Bulk create block list entry."""
        return self._post("/api/v2/block-lists-entries/bulk-create", json={"bl_values": bl_values})

    def bulk_delete(self, *, ids: _list[str]) -> _list[BlockListEntry]:
        """Bulk delete block list entry."""
        return [
            BlockListEntry.model_validate(item)
            for item in self._post("/api/v2/block-lists-entries/bulk-delete", json={"ids": ids})
        ]

    def download(
        self,
        *,
        domains_only: bool | NotGiven = NOT_GIVEN,
        search: str | NotGiven = NOT_GIVEN,
    ) -> str:
        """Download all block list entries as CSV."""
        return self._get(
            "/api/v2/block-lists-entries/download",
            params={"domains_only": domains_only, "search": search},
        )

    def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        domains_only: bool | NotGiven = NOT_GIVEN,
        search: str | NotGiven = NOT_GIVEN,
    ) -> SyncCursorPage[BlockListEntry]:
        """List block list entry. Auto-paginates: `for e in client.block_list_entries.list(): ...`."""

        def fetch_page(cursor: str | None) -> Any:
            return self._get(
                "/api/v2/block-lists-entries",
                params={
                    "limit": limit,
                    "starting_after": cursor if cursor is not None else starting_after,
                    "domains_only": domains_only,
                    "search": search,
                },
            )

        return self._paginate(BlockListEntry, fetch_page)


class AsyncBlockListEntries(AsyncAPIResource):
    async def create(self, *, bl_value: str) -> BlockListEntry:
        """Create block list entry."""
        return BlockListEntry.model_validate(
            await self._post("/api/v2/block-lists-entries", json={"bl_value": bl_value})
        )

    async def retrieve(self, id: str) -> BlockListEntry:
        """Get block list entry."""
        return BlockListEntry.model_validate(await self._get(f"/api/v2/block-lists-entries/{id}"))

    async def update(self, id: str, *, bl_value: str | NotGiven = NOT_GIVEN) -> BlockListEntry:
        """Patch block list entry."""
        return BlockListEntry.model_validate(
            await self._patch(f"/api/v2/block-lists-entries/{id}", json={"bl_value": bl_value})
        )

    async def delete(self, id: str) -> BlockListEntry:
        """Delete block list entry."""
        return BlockListEntry.model_validate(
            await self._delete(f"/api/v2/block-lists-entries/{id}")
        )

    async def delete_all(
        self,
        *,
        domains_only: bool | NotGiven = NOT_GIVEN,
        search: str | NotGiven = NOT_GIVEN,
    ) -> _list[BlockListEntry]:
        """Delete all block list entries."""
        return [
            BlockListEntry.model_validate(item)
            for item in await self._delete(
                "/api/v2/block-lists-entries",
                params={"domains_only": domains_only, "search": search},
            )
        ]

    async def bulk_create(self, *, bl_values: _list[str]) -> JSONObject:
        """Bulk create block list entry."""
        return await self._post(
            "/api/v2/block-lists-entries/bulk-create", json={"bl_values": bl_values}
        )

    async def bulk_delete(self, *, ids: _list[str]) -> _list[BlockListEntry]:
        """Bulk delete block list entry."""
        return [
            BlockListEntry.model_validate(item)
            for item in await self._post(
                "/api/v2/block-lists-entries/bulk-delete", json={"ids": ids}
            )
        ]

    async def download(
        self,
        *,
        domains_only: bool | NotGiven = NOT_GIVEN,
        search: str | NotGiven = NOT_GIVEN,
    ) -> str:
        """Download all block list entries as CSV."""
        return await self._get(
            "/api/v2/block-lists-entries/download",
            params={"domains_only": domains_only, "search": search},
        )

    async def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        domains_only: bool | NotGiven = NOT_GIVEN,
        search: str | NotGiven = NOT_GIVEN,
    ) -> AsyncCursorPage[BlockListEntry]:
        """List block list entry. Auto-paginates: `async for e in await client.block_list_entries.list(): ...`."""

        async def fetch_page(cursor: str | None) -> Any:
            return await self._get(
                "/api/v2/block-lists-entries",
                params={
                    "limit": limit,
                    "starting_after": cursor if cursor is not None else starting_after,
                    "domains_only": domains_only,
                    "search": search,
                },
            )

        return await self._paginate(BlockListEntry, fetch_page)
