"""Custom tag resource: ``client.custom_tags``."""

from __future__ import annotations

from typing import Any, Literal

from .._pagination import AsyncCursorPage, SyncCursorPage
from .._transport import NOT_GIVEN, NotGiven
from .._types import JSONObject
from ..models import CustomTag
from ._base import AsyncAPIResource, SyncAPIResource

__all__ = ["AsyncCustomTags", "CustomTags"]

# Both resource classes define a `list()` method, which shadows the builtin
# `list` for annotation resolution anywhere else in this module's class
# bodies -- alias it once and use `_list[...]` instead of bare `list[...]`.
_list = list

_ResourceType = Literal[1, 2]  # 1 = Account, 2 = Campaign


class CustomTags(SyncAPIResource):
    def create(self, *, label: str, description: str | NotGiven = NOT_GIVEN) -> CustomTag:
        """Create custom tag."""
        return CustomTag.model_validate(
            self._post("/api/v2/custom-tags", json={"label": label, "description": description})
        )

    def retrieve(self, id: str) -> CustomTag:
        """Get custom tag."""
        return CustomTag.model_validate(self._get(f"/api/v2/custom-tags/{id}"))

    def update(
        self,
        id: str,
        *,
        label: str | NotGiven = NOT_GIVEN,
        description: str | None | NotGiven = NOT_GIVEN,
    ) -> CustomTag:
        """Patch custom tag."""
        return CustomTag.model_validate(
            self._patch(
                f"/api/v2/custom-tags/{id}", json={"label": label, "description": description}
            )
        )

    def delete(self, id: str) -> CustomTag:
        """Delete custom tag."""
        return CustomTag.model_validate(self._delete(f"/api/v2/custom-tags/{id}"))

    def toggle_resource(
        self,
        *,
        tag_ids: _list[str],
        resource_type: _ResourceType,
        assign: bool,
        resource_ids: _list[str] | NotGiven = NOT_GIVEN,
        excluded_resource_ids: _list[str] | NotGiven = NOT_GIVEN,
        selected_all: bool | NotGiven = NOT_GIVEN,
        filter: JSONObject | NotGiven = NOT_GIVEN,
        search: str | NotGiven = NOT_GIVEN,
    ) -> JSONObject:
        """Assign or unassign tags to resources."""
        body = {
            "tag_ids": tag_ids,
            "resource_type": resource_type,
            "resource_ids": resource_ids,
            "excluded_resource_ids": excluded_resource_ids,
            "assign": assign,
            "selected_all": selected_all,
            "filter": filter,
            "search": search,
        }
        return self._post("/api/v2/custom-tags/toggle-resource", json=body)

    def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        search: str | NotGiven = NOT_GIVEN,
        resource_ids: str | NotGiven = NOT_GIVEN,
        tag_ids: str | NotGiven = NOT_GIVEN,
    ) -> SyncCursorPage[CustomTag]:
        """List custom tag. Auto-paginates: `for t in client.custom_tags.list(): ...`."""

        def fetch_page(cursor: str | None) -> Any:
            return self._get(
                "/api/v2/custom-tags",
                params={
                    "limit": limit,
                    "starting_after": cursor if cursor is not None else starting_after,
                    "search": search,
                    "resource_ids": resource_ids,
                    "tag_ids": tag_ids,
                },
            )

        return self._paginate(CustomTag, fetch_page)


class AsyncCustomTags(AsyncAPIResource):
    async def create(self, *, label: str, description: str | NotGiven = NOT_GIVEN) -> CustomTag:
        """Create custom tag."""
        return CustomTag.model_validate(
            await self._post(
                "/api/v2/custom-tags", json={"label": label, "description": description}
            )
        )

    async def retrieve(self, id: str) -> CustomTag:
        """Get custom tag."""
        return CustomTag.model_validate(await self._get(f"/api/v2/custom-tags/{id}"))

    async def update(
        self,
        id: str,
        *,
        label: str | NotGiven = NOT_GIVEN,
        description: str | None | NotGiven = NOT_GIVEN,
    ) -> CustomTag:
        """Patch custom tag."""
        return CustomTag.model_validate(
            await self._patch(
                f"/api/v2/custom-tags/{id}", json={"label": label, "description": description}
            )
        )

    async def delete(self, id: str) -> CustomTag:
        """Delete custom tag."""
        return CustomTag.model_validate(await self._delete(f"/api/v2/custom-tags/{id}"))

    async def toggle_resource(
        self,
        *,
        tag_ids: _list[str],
        resource_type: _ResourceType,
        assign: bool,
        resource_ids: _list[str] | NotGiven = NOT_GIVEN,
        excluded_resource_ids: _list[str] | NotGiven = NOT_GIVEN,
        selected_all: bool | NotGiven = NOT_GIVEN,
        filter: JSONObject | NotGiven = NOT_GIVEN,
        search: str | NotGiven = NOT_GIVEN,
    ) -> JSONObject:
        """Assign or unassign tags to resources."""
        body = {
            "tag_ids": tag_ids,
            "resource_type": resource_type,
            "resource_ids": resource_ids,
            "excluded_resource_ids": excluded_resource_ids,
            "assign": assign,
            "selected_all": selected_all,
            "filter": filter,
            "search": search,
        }
        return await self._post("/api/v2/custom-tags/toggle-resource", json=body)

    async def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        search: str | NotGiven = NOT_GIVEN,
        resource_ids: str | NotGiven = NOT_GIVEN,
        tag_ids: str | NotGiven = NOT_GIVEN,
    ) -> AsyncCursorPage[CustomTag]:
        """List custom tag. Auto-paginates: `async for t in await client.custom_tags.list(): ...`."""

        async def fetch_page(cursor: str | None) -> Any:
            return await self._get(
                "/api/v2/custom-tags",
                params={
                    "limit": limit,
                    "starting_after": cursor if cursor is not None else starting_after,
                    "search": search,
                    "resource_ids": resource_ids,
                    "tag_ids": tag_ids,
                },
            )

        return await self._paginate(CustomTag, fetch_page)
