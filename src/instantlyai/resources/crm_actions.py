"""CRM actions resource: ``client.crm_actions``."""

from __future__ import annotations

from .._types import JSONObject
from ._base import AsyncAPIResource, SyncAPIResource

__all__ = ["AsyncCRMActions", "CRMActions"]


class CRMActions(SyncAPIResource):
    def list_phone_numbers(self) -> list[JSONObject]:
        """List phone numbers."""
        return self._get("/api/v2/crm-actions/phone-numbers")

    def delete_phone_number(self, id: str) -> JSONObject:
        """Delete a phone number."""
        return self._delete(f"/api/v2/crm-actions/phone-numbers/{id}")


class AsyncCRMActions(AsyncAPIResource):
    async def list_phone_numbers(self) -> list[JSONObject]:
        """List phone numbers."""
        return await self._get("/api/v2/crm-actions/phone-numbers")

    async def delete_phone_number(self, id: str) -> JSONObject:
        """Delete a phone number."""
        return await self._delete(f"/api/v2/crm-actions/phone-numbers/{id}")
