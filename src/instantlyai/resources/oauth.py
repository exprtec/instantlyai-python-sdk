"""OAuth resource: ``client.oauth``."""

from __future__ import annotations

from .._types import JSONObject
from ._base import AsyncAPIResource, SyncAPIResource

__all__ = ["AsyncOAuth", "OAuth"]


class OAuth(SyncAPIResource):
    def init_google(self) -> JSONObject:
        """Initialize a Google OAuth session."""
        return self._post("/api/v2/oauth/google/init")

    def init_microsoft(self) -> JSONObject:
        """Initialize a Microsoft OAuth session."""
        return self._post("/api/v2/oauth/microsoft/init")

    def session_status(self, session_id: str) -> JSONObject:
        """Get the status of an OAuth session."""
        return self._get(f"/api/v2/oauth/session/status/{session_id}")


class AsyncOAuth(AsyncAPIResource):
    async def init_google(self) -> JSONObject:
        """Initialize a Google OAuth session."""
        return await self._post("/api/v2/oauth/google/init")

    async def init_microsoft(self) -> JSONObject:
        """Initialize a Microsoft OAuth session."""
        return await self._post("/api/v2/oauth/microsoft/init")

    async def session_status(self, session_id: str) -> JSONObject:
        """Get the status of an OAuth session."""
        return await self._get(f"/api/v2/oauth/session/status/{session_id}")
