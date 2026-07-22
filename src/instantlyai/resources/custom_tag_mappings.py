"""Custom tag mapping resource: ``client.custom_tag_mappings``."""

from __future__ import annotations

from typing import Any

from .._pagination import AsyncCursorPage, SyncCursorPage
from .._transport import NOT_GIVEN, NotGiven
from ..models import CustomTagMapping
from ._base import AsyncAPIResource, SyncAPIResource

__all__ = ["AsyncCustomTagMappings", "CustomTagMappings"]

# Both resource classes define a `list()` method, which shadows the builtin
# `list` for annotation resolution anywhere else in this module's class
# bodies -- alias it once and use `_list[...]` instead of bare `list[...]`.
_list = list


class CustomTagMappings(SyncAPIResource):
    def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        resource_ids: str | NotGiven = NOT_GIVEN,
    ) -> SyncCursorPage[CustomTagMapping]:
        """List custom tag mappings. Auto-paginates: `for m in client.custom_tag_mappings.list(): ...`."""

        def fetch_page(cursor: str | None) -> Any:
            return self._get(
                "/api/v2/custom-tag-mappings",
                params={
                    "limit": limit,
                    "starting_after": cursor if cursor is not None else starting_after,
                    "resource_ids": resource_ids,
                },
            )

        return self._paginate(CustomTagMapping, fetch_page)


class AsyncCustomTagMappings(AsyncAPIResource):
    async def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        resource_ids: str | NotGiven = NOT_GIVEN,
    ) -> AsyncCursorPage[CustomTagMapping]:
        """List custom tag mappings. Auto-paginates: `async for m in await client.custom_tag_mappings.list(): ...`."""

        async def fetch_page(cursor: str | None) -> Any:
            return await self._get(
                "/api/v2/custom-tag-mappings",
                params={
                    "limit": limit,
                    "starting_after": cursor if cursor is not None else starting_after,
                    "resource_ids": resource_ids,
                },
            )

        return await self._paginate(CustomTagMapping, fetch_page)
