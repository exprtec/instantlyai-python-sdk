"""Workspace member resource: ``client.workspace_members``."""

from __future__ import annotations

from typing import Any, Literal

from .._pagination import AsyncCursorPage, SyncCursorPage
from .._transport import NOT_GIVEN, NotGiven
from ..models import WorkspaceMember
from ._base import AsyncAPIResource, SyncAPIResource

__all__ = ["AsyncWorkspaceMembers", "WorkspaceMembers"]

# Both resource classes define a `list()` method, which shadows the builtin
# `list` for annotation resolution anywhere else in this module's class
# bodies -- alias it once and use `_list[...]` instead of bare `list[...]`.
_list = list

_WorkspaceMemberRole = Literal["owner", "admin", "editor", "view", "client"]
_WorkspaceMemberPermission = Literal[
    "dashboard.view",
    "campaigns.view",
    "campaigns.create",
    "campaigns.edit",
    "campaigns.delete",
    "organization.manage",
    "organization.integrations",
    "organization.billing",
    "organization.users.manage",
    "leadFinder.view",
    "customLeadLabels.create",
    "customLeadLabels.edit",
    "customLeadLabels.delete",
    "unibox.all",
    "analytics.view",
    "agency.manage",
    "accounts.view",
    "accounts.manage",
    "leadManagement.view",
    "leads.move",
    "crm.view",
    "websiteVisitors.view",
    "blocklist.manage",
    "preferences.manage",
    "inboxPlacement.view",
    "aiAgents.manage",
    "workspaceGroupMembers.invite",
    "workspaceGroupMembers.remove",
    "workspaceGroupMembers.leave",
]


class WorkspaceMembers(SyncAPIResource):
    def create(
        self,
        *,
        email: str,
        role: _WorkspaceMemberRole,
        user_email: str | NotGiven = NOT_GIVEN,
        nickname: str | NotGiven = NOT_GIVEN,
        permissions: _list[_WorkspaceMemberPermission] | NotGiven = NOT_GIVEN,
    ) -> WorkspaceMember:
        """Create a workspace member."""
        body = {
            "email": email,
            "user_email": user_email,
            "nickname": nickname,
            "role": role,
            "permissions": permissions,
        }
        return WorkspaceMember.model_validate(self._post("/api/v2/workspace-members", json=body))

    def retrieve(self, id: str) -> WorkspaceMember:
        """Get a single workspace member by ID."""
        return WorkspaceMember.model_validate(self._get(f"/api/v2/workspace-members/{id}"))

    def update(
        self,
        id: str,
        *,
        nickname: str | None | NotGiven = NOT_GIVEN,
        role: _WorkspaceMemberRole | NotGiven = NOT_GIVEN,
    ) -> WorkspaceMember:
        """Partially update a workspace member. Omitted fields are left unchanged."""
        body = {"nickname": nickname, "role": role}
        return WorkspaceMember.model_validate(
            self._patch(f"/api/v2/workspace-members/{id}", json=body)
        )

    def delete(self, id: str) -> WorkspaceMember:
        """Delete a workspace member."""
        return WorkspaceMember.model_validate(self._delete(f"/api/v2/workspace-members/{id}"))

    def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        accepted: bool | NotGiven = NOT_GIVEN,
        search: str | NotGiven = NOT_GIVEN,
    ) -> SyncCursorPage[WorkspaceMember]:
        """List workspace members. Auto-paginates: `for m in client.workspace_members.list(): ...`."""

        def fetch_page(cursor: str | None) -> Any:
            return self._get(
                "/api/v2/workspace-members",
                params={
                    "limit": limit,
                    "starting_after": cursor if cursor is not None else starting_after,
                    "accepted": accepted,
                    "search": search,
                },
            )

        return self._paginate(WorkspaceMember, fetch_page)


class AsyncWorkspaceMembers(AsyncAPIResource):
    async def create(
        self,
        *,
        email: str,
        role: _WorkspaceMemberRole,
        user_email: str | NotGiven = NOT_GIVEN,
        nickname: str | NotGiven = NOT_GIVEN,
        permissions: _list[_WorkspaceMemberPermission] | NotGiven = NOT_GIVEN,
    ) -> WorkspaceMember:
        """Create a workspace member."""
        body = {
            "email": email,
            "user_email": user_email,
            "nickname": nickname,
            "role": role,
            "permissions": permissions,
        }
        return WorkspaceMember.model_validate(
            await self._post("/api/v2/workspace-members", json=body)
        )

    async def retrieve(self, id: str) -> WorkspaceMember:
        """Get a single workspace member by ID."""
        return WorkspaceMember.model_validate(await self._get(f"/api/v2/workspace-members/{id}"))

    async def update(
        self,
        id: str,
        *,
        nickname: str | None | NotGiven = NOT_GIVEN,
        role: _WorkspaceMemberRole | NotGiven = NOT_GIVEN,
    ) -> WorkspaceMember:
        """Partially update a workspace member. Omitted fields are left unchanged."""
        body = {"nickname": nickname, "role": role}
        return WorkspaceMember.model_validate(
            await self._patch(f"/api/v2/workspace-members/{id}", json=body)
        )

    async def delete(self, id: str) -> WorkspaceMember:
        """Delete a workspace member."""
        return WorkspaceMember.model_validate(await self._delete(f"/api/v2/workspace-members/{id}"))

    async def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        accepted: bool | NotGiven = NOT_GIVEN,
        search: str | NotGiven = NOT_GIVEN,
    ) -> AsyncCursorPage[WorkspaceMember]:
        """List workspace members. Auto-paginates: `async for m in await client.workspace_members.list(): ...`."""

        async def fetch_page(cursor: str | None) -> Any:
            return await self._get(
                "/api/v2/workspace-members",
                params={
                    "limit": limit,
                    "starting_after": cursor if cursor is not None else starting_after,
                    "accepted": accepted,
                    "search": search,
                },
            )

        return await self._paginate(WorkspaceMember, fetch_page)
