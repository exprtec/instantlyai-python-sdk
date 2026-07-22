import pytest
from pydantic import BaseModel

from instantlyai._pagination import AsyncCursorPage, SyncCursorPage


class Item(BaseModel):
    id: str


def test_sync_cursor_page_iterates_within_a_single_page() -> None:
    def get_next_page(cursor: str | None) -> SyncCursorPage[Item]:
        raise AssertionError("should not be called: there is no next page")

    page = SyncCursorPage([Item(id="1"), Item(id="2")], None, get_next_page=get_next_page)

    assert not page.has_next_page
    assert [item.id for item in page] == ["1", "2"]


def test_sync_cursor_page_walks_multiple_pages_transparently() -> None:
    pages = {
        None: (["1", "2"], "cursor-a"),
        "cursor-a": (["3"], "cursor-b"),
        "cursor-b": (["4"], None),
    }
    calls: list[str | None] = []

    def get_next_page(cursor: str | None) -> SyncCursorPage[Item]:
        calls.append(cursor)
        ids, next_cursor = pages[cursor]
        return SyncCursorPage([Item(id=i) for i in ids], next_cursor, get_next_page=get_next_page)

    first_ids, first_next = pages[None]
    page = SyncCursorPage([Item(id=i) for i in first_ids], first_next, get_next_page=get_next_page)

    assert [item.id for item in page] == ["1", "2", "3", "4"]
    assert calls == ["cursor-a", "cursor-b"]


def test_sync_cursor_page_manual_control_reads_items_without_iterating() -> None:
    def get_next_page(cursor: str | None) -> SyncCursorPage[Item]:
        raise AssertionError("manual control must not trigger auto-pagination")

    page = SyncCursorPage([Item(id="1")], "next-cursor", get_next_page=get_next_page)

    assert page.items == [Item(id="1")]
    assert page.next_starting_after == "next-cursor"
    assert page.has_next_page


@pytest.mark.asyncio
async def test_async_cursor_page_walks_multiple_pages_transparently() -> None:
    pages = {
        None: (["1", "2"], "cursor-a"),
        "cursor-a": (["3"], None),
    }

    async def get_next_page(cursor: str | None) -> AsyncCursorPage[Item]:
        ids, next_cursor = pages[cursor]
        return AsyncCursorPage([Item(id=i) for i in ids], next_cursor, get_next_page=get_next_page)

    first_ids, first_next = pages[None]
    page = AsyncCursorPage([Item(id=i) for i in first_ids], first_next, get_next_page=get_next_page)

    collected = [item.id async for item in page]
    assert collected == ["1", "2", "3"]
