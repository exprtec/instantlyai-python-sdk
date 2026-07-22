"""Inbox placement analytics resource: ``client.inbox_placement_analytics``."""

from __future__ import annotations

from typing import Any, Literal

from .._pagination import AsyncCursorPage, SyncCursorPage
from .._transport import NOT_GIVEN, NotGiven
from .._types import JSONObject
from ..models import InboxPlacementAnalytics as InboxPlacementAnalyticsModel
from ._base import AsyncAPIResource, SyncAPIResource

__all__ = ["AsyncInboxPlacementAnalytics", "InboxPlacementAnalytics"]

# Both resource classes define a `list()` method, which shadows the builtin
# `list` for annotation resolution anywhere else in this module's class
# bodies -- alias it once and use `_list[...]` instead of bare `list[...]`.
_list = list

_RecipientGeo = Literal[1, 2, 3, 4]
_RecipientType = Literal[1, 2]
_RecipientEsp = Literal[1, 2, 8, 12, 13]


class InboxPlacementAnalytics(SyncAPIResource):
    def retrieve(self, id: str) -> InboxPlacementAnalyticsModel:
        """Get inbox placement analytics."""
        return InboxPlacementAnalyticsModel.model_validate(
            self._get(f"/api/v2/inbox-placement-analytics/{id}")
        )

    def deliverability_insights(
        self,
        *,
        test_id: str,
        date_from: str | NotGiven = NOT_GIVEN,
        date_to: str | NotGiven = NOT_GIVEN,
        previous_date_from: str | NotGiven = NOT_GIVEN,
        previous_date_to: str | NotGiven = NOT_GIVEN,
        show_previous: bool | NotGiven = NOT_GIVEN,
        recipient_geo: _list[_RecipientGeo] | NotGiven = NOT_GIVEN,
        recipient_type: _list[_RecipientType] | NotGiven = NOT_GIVEN,
        recipient_esp: _list[_RecipientEsp] | NotGiven = NOT_GIVEN,
    ) -> _list[JSONObject]:
        """Retrieve inbox placement analytics deliverability insights."""
        body = {
            "test_id": test_id,
            "date_from": date_from,
            "date_to": date_to,
            "previous_date_from": previous_date_from,
            "previous_date_to": previous_date_to,
            "show_previous": show_previous,
            "recipient_geo": recipient_geo,
            "recipient_type": recipient_type,
            "recipient_esp": recipient_esp,
        }
        return self._post("/api/v2/inbox-placement-analytics/deliverability-insights", json=body)

    def stats_by_date(
        self,
        *,
        test_id: str,
        date_from: str | NotGiven = NOT_GIVEN,
        date_to: str | NotGiven = NOT_GIVEN,
        recipient_geo: _list[_RecipientGeo] | NotGiven = NOT_GIVEN,
        recipient_type: _list[_RecipientType] | NotGiven = NOT_GIVEN,
        recipient_esp: _list[_RecipientEsp] | NotGiven = NOT_GIVEN,
        sender_email: str | NotGiven = NOT_GIVEN,
    ) -> _list[JSONObject]:
        """Get inbox placement analytics stats by date."""
        body = {
            "test_id": test_id,
            "date_from": date_from,
            "date_to": date_to,
            "recipient_geo": recipient_geo,
            "recipient_type": recipient_type,
            "recipient_esp": recipient_esp,
            "sender_email": sender_email,
        }
        return self._post("/api/v2/inbox-placement-analytics/stats-by-date", json=body)

    def stats_by_test_id(
        self,
        *,
        test_ids: _list[str],
        date_from: str | NotGiven = NOT_GIVEN,
        date_to: str | NotGiven = NOT_GIVEN,
        recipient_geo: _list[_RecipientGeo] | NotGiven = NOT_GIVEN,
        recipient_type: _list[_RecipientType] | NotGiven = NOT_GIVEN,
        recipient_esp: _list[_RecipientEsp] | NotGiven = NOT_GIVEN,
        sender_email: str | NotGiven = NOT_GIVEN,
    ) -> _list[JSONObject]:
        """Retrieve inbox placement analytics stats by test id."""
        body = {
            "test_ids": test_ids,
            "date_from": date_from,
            "date_to": date_to,
            "recipient_geo": recipient_geo,
            "recipient_type": recipient_type,
            "recipient_esp": recipient_esp,
            "sender_email": sender_email,
        }
        return self._post("/api/v2/inbox-placement-analytics/stats-by-test-id", json=body)

    def list(
        self,
        *,
        test_id: str,
        limit: int | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        date_from: str | NotGiven = NOT_GIVEN,
        date_to: str | NotGiven = NOT_GIVEN,
        recipient_geo: str | NotGiven = NOT_GIVEN,
        recipient_type: str | NotGiven = NOT_GIVEN,
        recipient_esp: str | NotGiven = NOT_GIVEN,
        sender_email: str | NotGiven = NOT_GIVEN,
    ) -> SyncCursorPage[InboxPlacementAnalyticsModel]:
        """List inbox placement analytics. Auto-paginates: `for a in client.inbox_placement_analytics.list(): ...`."""

        def fetch_page(cursor: str | None) -> Any:
            return self._get(
                "/api/v2/inbox-placement-analytics",
                params={
                    "limit": limit,
                    "starting_after": cursor if cursor is not None else starting_after,
                    "test_id": test_id,
                    "date_from": date_from,
                    "date_to": date_to,
                    "recipient_geo": recipient_geo,
                    "recipient_type": recipient_type,
                    "recipient_esp": recipient_esp,
                    "sender_email": sender_email,
                },
            )

        return self._paginate(InboxPlacementAnalyticsModel, fetch_page)


class AsyncInboxPlacementAnalytics(AsyncAPIResource):
    async def retrieve(self, id: str) -> InboxPlacementAnalyticsModel:
        """Get inbox placement analytics."""
        return InboxPlacementAnalyticsModel.model_validate(
            await self._get(f"/api/v2/inbox-placement-analytics/{id}")
        )

    async def deliverability_insights(
        self,
        *,
        test_id: str,
        date_from: str | NotGiven = NOT_GIVEN,
        date_to: str | NotGiven = NOT_GIVEN,
        previous_date_from: str | NotGiven = NOT_GIVEN,
        previous_date_to: str | NotGiven = NOT_GIVEN,
        show_previous: bool | NotGiven = NOT_GIVEN,
        recipient_geo: _list[_RecipientGeo] | NotGiven = NOT_GIVEN,
        recipient_type: _list[_RecipientType] | NotGiven = NOT_GIVEN,
        recipient_esp: _list[_RecipientEsp] | NotGiven = NOT_GIVEN,
    ) -> _list[JSONObject]:
        """Retrieve inbox placement analytics deliverability insights."""
        body = {
            "test_id": test_id,
            "date_from": date_from,
            "date_to": date_to,
            "previous_date_from": previous_date_from,
            "previous_date_to": previous_date_to,
            "show_previous": show_previous,
            "recipient_geo": recipient_geo,
            "recipient_type": recipient_type,
            "recipient_esp": recipient_esp,
        }
        return await self._post(
            "/api/v2/inbox-placement-analytics/deliverability-insights", json=body
        )

    async def stats_by_date(
        self,
        *,
        test_id: str,
        date_from: str | NotGiven = NOT_GIVEN,
        date_to: str | NotGiven = NOT_GIVEN,
        recipient_geo: _list[_RecipientGeo] | NotGiven = NOT_GIVEN,
        recipient_type: _list[_RecipientType] | NotGiven = NOT_GIVEN,
        recipient_esp: _list[_RecipientEsp] | NotGiven = NOT_GIVEN,
        sender_email: str | NotGiven = NOT_GIVEN,
    ) -> _list[JSONObject]:
        """Get inbox placement analytics stats by date."""
        body = {
            "test_id": test_id,
            "date_from": date_from,
            "date_to": date_to,
            "recipient_geo": recipient_geo,
            "recipient_type": recipient_type,
            "recipient_esp": recipient_esp,
            "sender_email": sender_email,
        }
        return await self._post("/api/v2/inbox-placement-analytics/stats-by-date", json=body)

    async def stats_by_test_id(
        self,
        *,
        test_ids: _list[str],
        date_from: str | NotGiven = NOT_GIVEN,
        date_to: str | NotGiven = NOT_GIVEN,
        recipient_geo: _list[_RecipientGeo] | NotGiven = NOT_GIVEN,
        recipient_type: _list[_RecipientType] | NotGiven = NOT_GIVEN,
        recipient_esp: _list[_RecipientEsp] | NotGiven = NOT_GIVEN,
        sender_email: str | NotGiven = NOT_GIVEN,
    ) -> _list[JSONObject]:
        """Retrieve inbox placement analytics stats by test id."""
        body = {
            "test_ids": test_ids,
            "date_from": date_from,
            "date_to": date_to,
            "recipient_geo": recipient_geo,
            "recipient_type": recipient_type,
            "recipient_esp": recipient_esp,
            "sender_email": sender_email,
        }
        return await self._post("/api/v2/inbox-placement-analytics/stats-by-test-id", json=body)

    async def list(
        self,
        *,
        test_id: str,
        limit: int | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        date_from: str | NotGiven = NOT_GIVEN,
        date_to: str | NotGiven = NOT_GIVEN,
        recipient_geo: str | NotGiven = NOT_GIVEN,
        recipient_type: str | NotGiven = NOT_GIVEN,
        recipient_esp: str | NotGiven = NOT_GIVEN,
        sender_email: str | NotGiven = NOT_GIVEN,
    ) -> AsyncCursorPage[InboxPlacementAnalyticsModel]:
        """List inbox placement analytics. Auto-paginates: `async for a in await client.inbox_placement_analytics.list(): ...`."""

        async def fetch_page(cursor: str | None) -> Any:
            return await self._get(
                "/api/v2/inbox-placement-analytics",
                params={
                    "limit": limit,
                    "starting_after": cursor if cursor is not None else starting_after,
                    "test_id": test_id,
                    "date_from": date_from,
                    "date_to": date_to,
                    "recipient_geo": recipient_geo,
                    "recipient_type": recipient_type,
                    "recipient_esp": recipient_esp,
                    "sender_email": sender_email,
                },
            )

        return await self._paginate(InboxPlacementAnalyticsModel, fetch_page)
