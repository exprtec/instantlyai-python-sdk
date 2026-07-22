"""Cursor-based auto-paginating iterators.

Every ``list()`` method returns one of the page objects below. The object
holds the current page's items *and* transparently walks subsequent pages
when iterated:

    for campaign in client.campaigns.list():
        ...  # walks every page via the `starting_after` cursor

For manual, one-page-at-a-time control, read ``.items`` and
``.next_starting_after`` directly instead of iterating:

    page = client.campaigns.list()
    page.items              # just this page
    page.next_starting_after  # cursor for the next call, or None
"""

from __future__ import annotations

from collections.abc import AsyncIterator, Awaitable, Callable, Iterator
from typing import Generic, TypeVar

_T = TypeVar("_T")

__all__ = ["AsyncCursorPage", "SyncCursorPage"]


class SyncCursorPage(Generic[_T]):
    """A single page of results that auto-paginates when iterated."""

    def __init__(
        self,
        items: list[_T],
        next_starting_after: str | None,
        *,
        get_next_page: Callable[[str], SyncCursorPage[_T]],
    ) -> None:
        self.items = items
        self.next_starting_after = next_starting_after
        self._get_next_page = get_next_page

    @property
    def has_next_page(self) -> bool:
        return self.next_starting_after is not None

    def __iter__(self) -> Iterator[_T]:
        page: SyncCursorPage[_T] = self
        while True:
            yield from page.items
            if page.next_starting_after is None:
                return
            page = page._get_next_page(page.next_starting_after)

    def __repr__(self) -> str:
        return f"SyncCursorPage(items={self.items!r}, next_starting_after={self.next_starting_after!r})"


class AsyncCursorPage(Generic[_T]):
    """A single page of results that auto-paginates when iterated (async)."""

    def __init__(
        self,
        items: list[_T],
        next_starting_after: str | None,
        *,
        get_next_page: Callable[[str], Awaitable[AsyncCursorPage[_T]]],
    ) -> None:
        self.items = items
        self.next_starting_after = next_starting_after
        self._get_next_page = get_next_page

    @property
    def has_next_page(self) -> bool:
        return self.next_starting_after is not None

    async def __aiter__(self) -> AsyncIterator[_T]:
        page: AsyncCursorPage[_T] = self
        while True:
            for item in page.items:
                yield item
            if page.next_starting_after is None:
                return
            page = await page._get_next_page(page.next_starting_after)

    def __repr__(self) -> str:
        return f"AsyncCursorPage(items={self.items!r}, next_starting_after={self.next_starting_after!r})"
