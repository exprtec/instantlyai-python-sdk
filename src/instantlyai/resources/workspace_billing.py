"""Workspace billing resource: ``client.workspace_billing``."""

from __future__ import annotations

from .._types import JSONObject
from ._base import AsyncAPIResource, SyncAPIResource

__all__ = ["AsyncWorkspaceBilling", "WorkspaceBilling"]


class WorkspaceBilling(SyncAPIResource):
    def plan_details(self) -> JSONObject:
        """Get workspace plan details."""
        return self._get("/api/v2/workspace-billing/plan-details")

    def subscription_details(self) -> JSONObject:
        """Get workspace subscription details."""
        return self._get("/api/v2/workspace-billing/subscription-details")


class AsyncWorkspaceBilling(AsyncAPIResource):
    async def plan_details(self) -> JSONObject:
        """Get workspace plan details."""
        return await self._get("/api/v2/workspace-billing/plan-details")

    async def subscription_details(self) -> JSONObject:
        """Get workspace subscription details."""
        return await self._get("/api/v2/workspace-billing/subscription-details")
