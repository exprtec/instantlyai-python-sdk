"""Audit log resource: ``client.audit_logs``."""

from __future__ import annotations

from typing import Any

from .._pagination import AsyncCursorPage, SyncCursorPage
from .._transport import NOT_GIVEN, NotGiven
from ..models import AuditLog
from ._base import AsyncAPIResource, SyncAPIResource

__all__ = ["AsyncAuditLogs", "AuditLogs"]

# Both resource classes define a `list()` method, which shadows the builtin
# `list` for annotation resolution anywhere else in this module's class
# bodies -- alias it once and use `_list[...]` instead of bare `list[...]`.
_list = list


class AuditLogs(SyncAPIResource):
    def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        activity_type: float | NotGiven = NOT_GIVEN,
        search: str | NotGiven = NOT_GIVEN,
        start_date: str | NotGiven = NOT_GIVEN,
        end_date: str | NotGiven = NOT_GIVEN,
    ) -> SyncCursorPage[AuditLog]:
        """List audit logs. Auto-paginates: `for log in client.audit_logs.list(): ...`."""

        def fetch_page(cursor: str | None) -> Any:
            return self._get(
                "/api/v2/audit-logs",
                params={
                    "limit": limit,
                    "starting_after": cursor if cursor is not None else starting_after,
                    "activity_type": activity_type,
                    "search": search,
                    "start_date": start_date,
                    "end_date": end_date,
                },
            )

        return self._paginate(AuditLog, fetch_page)


class AsyncAuditLogs(AsyncAPIResource):
    async def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        activity_type: float | NotGiven = NOT_GIVEN,
        search: str | NotGiven = NOT_GIVEN,
        start_date: str | NotGiven = NOT_GIVEN,
        end_date: str | NotGiven = NOT_GIVEN,
    ) -> AsyncCursorPage[AuditLog]:
        """List audit logs. Auto-paginates: `async for log in await client.audit_logs.list(): ...`."""

        async def fetch_page(cursor: str | None) -> Any:
            return await self._get(
                "/api/v2/audit-logs",
                params={
                    "limit": limit,
                    "starting_after": cursor if cursor is not None else starting_after,
                    "activity_type": activity_type,
                    "search": search,
                    "start_date": start_date,
                    "end_date": end_date,
                },
            )

        return await self._paginate(AuditLog, fetch_page)
