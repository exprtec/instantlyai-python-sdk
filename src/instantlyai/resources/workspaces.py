"""Workspace resource: ``client.workspaces`` (operates on the current workspace)."""

from __future__ import annotations

from .._transport import NOT_GIVEN, NotGiven
from .._types import JSONObject
from ..models import Workspace
from ._base import AsyncAPIResource, SyncAPIResource

__all__ = ["AsyncWorkspaces", "Workspaces"]


class Workspaces(SyncAPIResource):
    def retrieve(self) -> Workspace:
        """Get the current workspace."""
        return Workspace.model_validate(self._get("/api/v2/workspaces/current"))

    def update(
        self,
        *,
        name: str | NotGiven = NOT_GIVEN,
        org_logo_url: str | None | NotGiven = NOT_GIVEN,
    ) -> Workspace:
        """Partially update the current workspace. Omitted fields are left unchanged."""
        body = {"name": name, "org_logo_url": org_logo_url}
        return Workspace.model_validate(self._patch("/api/v2/workspaces/current", json=body))

    def schedule_removal(self) -> Workspace:
        """Schedule the current workspace for removal."""
        return Workspace.model_validate(
            self._post("/api/v2/workspaces/current/schedule-for-removal")
        )

    def cancel_removal(self) -> Workspace:
        """Cancel a scheduled removal of the current workspace."""
        return Workspace.model_validate(
            self._delete("/api/v2/workspaces/current/schedule-for-removal")
        )

    def add_whitelabel_domain(self, *, domain: str) -> Workspace:
        """Set the agency (whitelabel) domain for the workspace."""
        return Workspace.model_validate(
            self._post("/api/v2/workspaces/current/whitelabel-domain", json={"domain": domain})
        )

    def get_whitelabel_domain(self) -> JSONObject:
        """Get organization verified agency domain information."""
        return self._get("/api/v2/workspaces/current/whitelabel-domain")

    def delete_whitelabel_domain(self) -> Workspace:
        """Delete the organization agency (whitelabel) domain."""
        return Workspace.model_validate(
            self._delete("/api/v2/workspaces/current/whitelabel-domain")
        )

    def change_owner(self, *, email: str, sec: str) -> Workspace:
        """Change the current workspace's owner."""
        return Workspace.model_validate(
            self._post("/api/v2/workspaces/current/change-owner", json={"email": email, "sec": sec})
        )


class AsyncWorkspaces(AsyncAPIResource):
    async def retrieve(self) -> Workspace:
        """Get the current workspace."""
        return Workspace.model_validate(await self._get("/api/v2/workspaces/current"))

    async def update(
        self,
        *,
        name: str | NotGiven = NOT_GIVEN,
        org_logo_url: str | None | NotGiven = NOT_GIVEN,
    ) -> Workspace:
        """Partially update the current workspace. Omitted fields are left unchanged."""
        body = {"name": name, "org_logo_url": org_logo_url}
        return Workspace.model_validate(await self._patch("/api/v2/workspaces/current", json=body))

    async def schedule_removal(self) -> Workspace:
        """Schedule the current workspace for removal."""
        return Workspace.model_validate(
            await self._post("/api/v2/workspaces/current/schedule-for-removal")
        )

    async def cancel_removal(self) -> Workspace:
        """Cancel a scheduled removal of the current workspace."""
        return Workspace.model_validate(
            await self._delete("/api/v2/workspaces/current/schedule-for-removal")
        )

    async def add_whitelabel_domain(self, *, domain: str) -> Workspace:
        """Set the agency (whitelabel) domain for the workspace."""
        return Workspace.model_validate(
            await self._post(
                "/api/v2/workspaces/current/whitelabel-domain", json={"domain": domain}
            )
        )

    async def get_whitelabel_domain(self) -> JSONObject:
        """Get organization verified agency domain information."""
        return await self._get("/api/v2/workspaces/current/whitelabel-domain")

    async def delete_whitelabel_domain(self) -> Workspace:
        """Delete the organization agency (whitelabel) domain."""
        return Workspace.model_validate(
            await self._delete("/api/v2/workspaces/current/whitelabel-domain")
        )

    async def change_owner(self, *, email: str, sec: str) -> Workspace:
        """Change the current workspace's owner."""
        return Workspace.model_validate(
            await self._post(
                "/api/v2/workspaces/current/change-owner", json={"email": email, "sec": sec}
            )
        )
