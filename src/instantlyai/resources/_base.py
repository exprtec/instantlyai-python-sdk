"""Shared plumbing every resource module builds on.

A resource method is thin by construction: pull the typed keyword
arguments together into a body/params dict, call one of ``_get``/``_post``/
``_patch``/``_delete``, optionally validate the JSON body into a Pydantic
model. Auto-pagination is centralised in :meth:`SyncAPIResource._paginate`
and :meth:`AsyncAPIResource._paginate` so individual `list()` methods only
need to describe *how* to fetch one page.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any, TypeVar

from pydantic import BaseModel

from .._pagination import AsyncCursorPage, SyncCursorPage
from .._transport import AsyncTransport, SyncTransport, omit_not_given

_M = TypeVar("_M", bound=BaseModel)

__all__ = ["AsyncAPIResource", "SyncAPIResource"]


class SyncAPIResource:
    def __init__(self, transport: SyncTransport) -> None:
        self._transport = transport

    def _get(self, path: str, *, params: dict[str, object] | None = None) -> Any:
        return self._transport.request("GET", path, params=omit_not_given(params or {}))

    def _post(
        self,
        path: str,
        *,
        params: dict[str, object] | None = None,
        json: dict[str, object] | None = None,
    ) -> Any:
        return self._transport.request(
            "POST", path, params=omit_not_given(params or {}), json=omit_not_given(json or {})
        )

    def _patch(self, path: str, *, json: dict[str, object] | None = None) -> Any:
        return self._transport.request("PATCH", path, json=omit_not_given(json or {}))

    def _delete(
        self,
        path: str,
        *,
        params: dict[str, object] | None = None,
        json: dict[str, object] | None = None,
    ) -> Any:
        return self._transport.request(
            "DELETE",
            path,
            params=omit_not_given(params or {}),
            json=omit_not_given(json) if json else None,
        )

    def _paginate(
        self,
        model: type[_M],
        fetch_page: Callable[[str | None], Any],
    ) -> SyncCursorPage[_M]:
        """Build an auto-paginating page from a function that fetches one raw page.

        ``fetch_page(cursor)`` is called with ``None`` for the first page and
        with the previous page's ``next_starting_after`` for every page after.
        """

        def get_next_page(cursor: str | None) -> SyncCursorPage[_M]:
            body = fetch_page(cursor)
            items = [model.model_validate(item) for item in body.get("items", [])]
            return SyncCursorPage(
                items, body.get("next_starting_after"), get_next_page=get_next_page
            )

        return get_next_page(None)


class AsyncAPIResource:
    def __init__(self, transport: AsyncTransport) -> None:
        self._transport = transport

    async def _get(self, path: str, *, params: dict[str, object] | None = None) -> Any:
        return await self._transport.request("GET", path, params=omit_not_given(params or {}))

    async def _post(
        self,
        path: str,
        *,
        params: dict[str, object] | None = None,
        json: dict[str, object] | None = None,
    ) -> Any:
        return await self._transport.request(
            "POST", path, params=omit_not_given(params or {}), json=omit_not_given(json or {})
        )

    async def _patch(self, path: str, *, json: dict[str, object] | None = None) -> Any:
        return await self._transport.request("PATCH", path, json=omit_not_given(json or {}))

    async def _delete(
        self,
        path: str,
        *,
        params: dict[str, object] | None = None,
        json: dict[str, object] | None = None,
    ) -> Any:
        return await self._transport.request(
            "DELETE",
            path,
            params=omit_not_given(params or {}),
            json=omit_not_given(json) if json else None,
        )

    async def _paginate(
        self,
        model: type[_M],
        fetch_page: Callable[[str | None], Awaitable[Any]],
    ) -> AsyncCursorPage[_M]:
        async def get_next_page(cursor: str | None) -> AsyncCursorPage[_M]:
            body = await fetch_page(cursor)
            items = [model.model_validate(item) for item in body.get("items", [])]
            return AsyncCursorPage(
                items, body.get("next_starting_after"), get_next_page=get_next_page
            )

        return await get_next_page(None)
