"""API key resource: ``client.api_keys``."""

from __future__ import annotations

from typing import Any

from .._pagination import AsyncCursorPage, SyncCursorPage
from .._transport import NOT_GIVEN, NotGiven
from ..models import APIKey, Scope1
from ._base import AsyncAPIResource, SyncAPIResource

__all__ = ["APIKeys", "AsyncAPIKeys"]

# Both resource classes define a `list()` method, which shadows the builtin
# `list` for annotation resolution anywhere else in this module's class
# bodies -- alias it once and use `_list[...]` instead of bare `list[...]`.
_list = list


class APIKeys(SyncAPIResource):
    def create(self, *, name: str, scopes: _list[Scope1]) -> APIKey:
        """Create an API key."""
        return APIKey.model_validate(
            self._post("/api/v2/api-keys", json={"name": name, "scopes": scopes})
        )

    def delete(self, id: str) -> APIKey:
        """Delete an API key."""
        return APIKey.model_validate(self._delete(f"/api/v2/api-keys/{id}"))

    def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
    ) -> SyncCursorPage[APIKey]:
        """List API keys. Auto-paginates: `for k in client.api_keys.list(): ...`."""

        def fetch_page(cursor: str | None) -> Any:
            return self._get(
                "/api/v2/api-keys",
                params={
                    "limit": limit,
                    "starting_after": cursor if cursor is not None else starting_after,
                },
            )

        return self._paginate(APIKey, fetch_page)


class AsyncAPIKeys(AsyncAPIResource):
    async def create(self, *, name: str, scopes: _list[Scope1]) -> APIKey:
        """Create an API key."""
        return APIKey.model_validate(
            await self._post("/api/v2/api-keys", json={"name": name, "scopes": scopes})
        )

    async def delete(self, id: str) -> APIKey:
        """Delete an API key."""
        return APIKey.model_validate(await self._delete(f"/api/v2/api-keys/{id}"))

    async def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
    ) -> AsyncCursorPage[APIKey]:
        """List API keys. Auto-paginates: `async for k in await client.api_keys.list(): ...`."""

        async def fetch_page(cursor: str | None) -> Any:
            return await self._get(
                "/api/v2/api-keys",
                params={
                    "limit": limit,
                    "starting_after": cursor if cursor is not None else starting_after,
                },
            )

        return await self._paginate(APIKey, fetch_page)
