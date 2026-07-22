"""Webhook event resource: ``client.webhook_events``."""

from __future__ import annotations

from typing import Any

from .._pagination import AsyncCursorPage, SyncCursorPage
from .._transport import NOT_GIVEN, NotGiven
from .._types import JSONObject
from ..models import WebhookEvent
from ._base import AsyncAPIResource, SyncAPIResource

__all__ = ["AsyncWebhookEvents", "WebhookEvents"]

# Both resource classes define a `list()` method, which shadows the builtin
# `list` for annotation resolution anywhere else in this module's class
# bodies -- alias it once and use `_list[...]` instead of bare `list[...]`.
_list = list


class WebhookEvents(SyncAPIResource):
    def retrieve(self, id: str) -> WebhookEvent:
        """Get a single webhook event by ID."""
        return WebhookEvent.model_validate(self._get(f"/api/v2/webhook-events/{id}"))

    def summary(
        self,
        *,
        from_: str | NotGiven = NOT_GIVEN,
        to: str | NotGiven = NOT_GIVEN,
    ) -> JSONObject:
        """Get overview aggregates (success/failure counts and rates) for webhook events."""
        return self._get("/api/v2/webhook-events/summary", params={"from": from_, "to": to})

    def summary_by_date(
        self,
        *,
        from_: str | NotGiven = NOT_GIVEN,
        to: str | NotGiven = NOT_GIVEN,
    ) -> JSONObject:
        """Get overview aggregates for webhook events, bucketed by date."""
        return self._get("/api/v2/webhook-events/summary-by-date", params={"from": from_, "to": to})

    def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        success: bool | NotGiven = NOT_GIVEN,
        from_: str | NotGiven = NOT_GIVEN,
        to: str | NotGiven = NOT_GIVEN,
        search: str | NotGiven = NOT_GIVEN,
    ) -> SyncCursorPage[WebhookEvent]:
        """List webhook events. Auto-paginates: `for e in client.webhook_events.list(): ...`."""

        def fetch_page(cursor: str | None) -> Any:
            return self._get(
                "/api/v2/webhook-events",
                params={
                    "limit": limit,
                    "starting_after": cursor if cursor is not None else starting_after,
                    "success": success,
                    "from": from_,
                    "to": to,
                    "search": search,
                },
            )

        return self._paginate(WebhookEvent, fetch_page)


class AsyncWebhookEvents(AsyncAPIResource):
    async def retrieve(self, id: str) -> WebhookEvent:
        """Get a single webhook event by ID."""
        return WebhookEvent.model_validate(await self._get(f"/api/v2/webhook-events/{id}"))

    async def summary(
        self,
        *,
        from_: str | NotGiven = NOT_GIVEN,
        to: str | NotGiven = NOT_GIVEN,
    ) -> JSONObject:
        """Get overview aggregates (success/failure counts and rates) for webhook events."""
        return await self._get("/api/v2/webhook-events/summary", params={"from": from_, "to": to})

    async def summary_by_date(
        self,
        *,
        from_: str | NotGiven = NOT_GIVEN,
        to: str | NotGiven = NOT_GIVEN,
    ) -> JSONObject:
        """Get overview aggregates for webhook events, bucketed by date."""
        return await self._get(
            "/api/v2/webhook-events/summary-by-date", params={"from": from_, "to": to}
        )

    async def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        success: bool | NotGiven = NOT_GIVEN,
        from_: str | NotGiven = NOT_GIVEN,
        to: str | NotGiven = NOT_GIVEN,
        search: str | NotGiven = NOT_GIVEN,
    ) -> AsyncCursorPage[WebhookEvent]:
        """List webhook events. Auto-paginates: `async for e in await client.webhook_events.list(): ...`."""

        async def fetch_page(cursor: str | None) -> Any:
            return await self._get(
                "/api/v2/webhook-events",
                params={
                    "limit": limit,
                    "starting_after": cursor if cursor is not None else starting_after,
                    "success": success,
                    "from": from_,
                    "to": to,
                    "search": search,
                },
            )

        return await self._paginate(WebhookEvent, fetch_page)
