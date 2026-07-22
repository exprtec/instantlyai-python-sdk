"""Inbox placement blacklist/SpamAssassin report resource: ``client.inbox_placement_reports``."""

from __future__ import annotations

from typing import Any

from .._pagination import AsyncCursorPage, SyncCursorPage
from .._transport import NOT_GIVEN, NotGiven
from ..models import InboxPlacementBlacklistAndSpamAssassinReport
from ._base import AsyncAPIResource, SyncAPIResource

__all__ = ["AsyncInboxPlacementReports", "InboxPlacementReports"]

# Both resource classes define a `list()` method, which shadows the builtin
# `list` for annotation resolution anywhere else in this module's class
# bodies -- alias it once and use `_list[...]` instead of bare `list[...]`.
_list = list


class InboxPlacementReports(SyncAPIResource):
    def retrieve(self, id: str) -> InboxPlacementBlacklistAndSpamAssassinReport:
        """Get inbox placement blacklist and SpamAssassin report."""
        return InboxPlacementBlacklistAndSpamAssassinReport.model_validate(
            self._get(f"/api/v2/inbox-placement-reports/{id}")
        )

    def list(
        self,
        *,
        test_id: str,
        limit: int | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        date_from: str | NotGiven = NOT_GIVEN,
        date_to: str | NotGiven = NOT_GIVEN,
        skip_spam_assassin_report: bool | NotGiven = NOT_GIVEN,
        skip_blacklist_report: bool | NotGiven = NOT_GIVEN,
    ) -> SyncCursorPage[InboxPlacementBlacklistAndSpamAssassinReport]:
        """List inbox placement blacklist and SpamAssassin reports. Auto-paginates: `for r in client.inbox_placement_reports.list(): ...`."""

        def fetch_page(cursor: str | None) -> Any:
            return self._get(
                "/api/v2/inbox-placement-reports",
                params={
                    "limit": limit,
                    "starting_after": cursor if cursor is not None else starting_after,
                    "test_id": test_id,
                    "date_from": date_from,
                    "date_to": date_to,
                    "skip_spam_assassin_report": skip_spam_assassin_report,
                    "skip_blacklist_report": skip_blacklist_report,
                },
            )

        return self._paginate(InboxPlacementBlacklistAndSpamAssassinReport, fetch_page)


class AsyncInboxPlacementReports(AsyncAPIResource):
    async def retrieve(self, id: str) -> InboxPlacementBlacklistAndSpamAssassinReport:
        """Get inbox placement blacklist and SpamAssassin report."""
        return InboxPlacementBlacklistAndSpamAssassinReport.model_validate(
            await self._get(f"/api/v2/inbox-placement-reports/{id}")
        )

    async def list(
        self,
        *,
        test_id: str,
        limit: int | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        date_from: str | NotGiven = NOT_GIVEN,
        date_to: str | NotGiven = NOT_GIVEN,
        skip_spam_assassin_report: bool | NotGiven = NOT_GIVEN,
        skip_blacklist_report: bool | NotGiven = NOT_GIVEN,
    ) -> AsyncCursorPage[InboxPlacementBlacklistAndSpamAssassinReport]:
        """List inbox placement blacklist and SpamAssassin reports. Auto-paginates: `async for r in await client.inbox_placement_reports.list(): ...`."""

        async def fetch_page(cursor: str | None) -> Any:
            return await self._get(
                "/api/v2/inbox-placement-reports",
                params={
                    "limit": limit,
                    "starting_after": cursor if cursor is not None else starting_after,
                    "test_id": test_id,
                    "date_from": date_from,
                    "date_to": date_to,
                    "skip_spam_assassin_report": skip_spam_assassin_report,
                    "skip_blacklist_report": skip_blacklist_report,
                },
            )

        return await self._paginate(InboxPlacementBlacklistAndSpamAssassinReport, fetch_page)
