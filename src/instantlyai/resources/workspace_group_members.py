"""Workspace group member resource: ``client.workspace_group_members``."""

from __future__ import annotations

from typing import Any

from .._pagination import AsyncCursorPage, SyncCursorPage
from .._transport import NOT_GIVEN, NotGiven
from .._types import JSONObject
from ..models import WorkspaceGroupMember
from ._base import AsyncAPIResource, SyncAPIResource

__all__ = ["AsyncWorkspaceGroupMembers", "WorkspaceGroupMembers"]

# Both resource classes define a `list()` method, which shadows the builtin
# `list` for annotation resolution anywhere else in this module's class
# bodies -- alias it once and use `_list[...]` instead of bare `list[...]`.
_list = list


class WorkspaceGroupMembers(SyncAPIResource):
    def create(self, *, sub_workspace_id: str) -> WorkspaceGroupMember:
        """Create a workspace group member."""
        return WorkspaceGroupMember.model_validate(
            self._post(
                "/api/v2/workspace-group-members", json={"sub_workspace_id": sub_workspace_id}
            )
        )

    def retrieve(self, id: str) -> WorkspaceGroupMember:
        """Get a single workspace group member by ID."""
        return WorkspaceGroupMember.model_validate(
            self._get(f"/api/v2/workspace-group-members/{id}")
        )

    def delete(self, id: str) -> WorkspaceGroupMember:
        """Delete a workspace group member."""
        return WorkspaceGroupMember.model_validate(
            self._delete(f"/api/v2/workspace-group-members/{id}")
        )

    def admin(self) -> JSONObject:
        """Get the current workspace's admin workspace."""
        return self._get("/api/v2/workspace-group-members/admin")

    def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
    ) -> SyncCursorPage[WorkspaceGroupMember]:
        """List workspace group members. Auto-paginates: `for m in client.workspace_group_members.list(): ...`."""

        def fetch_page(cursor: str | None) -> Any:
            return self._get(
                "/api/v2/workspace-group-members",
                params={
                    "limit": limit,
                    "starting_after": cursor if cursor is not None else starting_after,
                },
            )

        return self._paginate(WorkspaceGroupMember, fetch_page)


class AsyncWorkspaceGroupMembers(AsyncAPIResource):
    async def create(self, *, sub_workspace_id: str) -> WorkspaceGroupMember:
        """Create a workspace group member."""
        return WorkspaceGroupMember.model_validate(
            await self._post(
                "/api/v2/workspace-group-members", json={"sub_workspace_id": sub_workspace_id}
            )
        )

    async def retrieve(self, id: str) -> WorkspaceGroupMember:
        """Get a single workspace group member by ID."""
        return WorkspaceGroupMember.model_validate(
            await self._get(f"/api/v2/workspace-group-members/{id}")
        )

    async def delete(self, id: str) -> WorkspaceGroupMember:
        """Delete a workspace group member."""
        return WorkspaceGroupMember.model_validate(
            await self._delete(f"/api/v2/workspace-group-members/{id}")
        )

    async def admin(self) -> JSONObject:
        """Get the current workspace's admin workspace."""
        return await self._get("/api/v2/workspace-group-members/admin")

    async def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
    ) -> AsyncCursorPage[WorkspaceGroupMember]:
        """List workspace group members. Auto-paginates: `async for m in await client.workspace_group_members.list(): ...`."""

        async def fetch_page(cursor: str | None) -> Any:
            return await self._get(
                "/api/v2/workspace-group-members",
                params={
                    "limit": limit,
                    "starting_after": cursor if cursor is not None else starting_after,
                },
            )

        return await self._paginate(WorkspaceGroupMember, fetch_page)
