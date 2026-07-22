"""Webhook resource: ``client.webhooks``."""

from __future__ import annotations

from typing import Any, Literal

from .._pagination import AsyncCursorPage, SyncCursorPage
from .._transport import NOT_GIVEN, NotGiven
from .._types import JSONObject
from ..models import EventType, Webhook
from ._base import AsyncAPIResource, SyncAPIResource

__all__ = ["AsyncWebhooks", "Webhooks"]

# Both resource classes define a `list()` method, which shadows the builtin
# `list` for annotation resolution anywhere else in this module's class
# bodies -- alias it once and use `_list[...]` instead of bare `list[...]`.
_list = list

_WebhookEventType = Literal[
    "all_events",
    "email_sent",
    "email_opened",
    "email_link_clicked",
    "reply_received",
    "email_bounced",
    "lead_unsubscribed",
    "campaign_completed",
    "account_error",
    "lead_neutral",
    "lead_interested",
    "lead_not_interested",
    "lead_meeting_booked",
    "lead_meeting_completed",
    "lead_closed",
    "lead_out_of_office",
    "lead_wrong_person",
    "lead_no_show",
    "supersearch_enrichment_completed",
]


class Webhooks(SyncAPIResource):
    def create(
        self,
        *,
        target_hook_url: str,
        campaign: str | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        event_type: EventType | NotGiven = NOT_GIVEN,
        custom_interest_value: float | NotGiven = NOT_GIVEN,
        headers: JSONObject | NotGiven = NOT_GIVEN,
    ) -> Webhook:
        """Create a webhook."""
        body = {
            "campaign": campaign,
            "name": name,
            "target_hook_url": target_hook_url,
            "event_type": event_type,
            "custom_interest_value": custom_interest_value,
            "headers": headers,
        }
        return Webhook.model_validate(self._post("/api/v2/webhooks", json=body))

    def retrieve(self, id: str) -> Webhook:
        """Get a single webhook by ID."""
        return Webhook.model_validate(self._get(f"/api/v2/webhooks/{id}"))

    def update(
        self,
        id: str,
        *,
        campaign: str | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        target_hook_url: str | NotGiven = NOT_GIVEN,
        event_type: EventType | NotGiven = NOT_GIVEN,
        custom_interest_value: float | NotGiven = NOT_GIVEN,
        headers: JSONObject | NotGiven = NOT_GIVEN,
    ) -> Webhook:
        """Partially update a webhook. Omitted fields are left unchanged."""
        body = {
            "campaign": campaign,
            "name": name,
            "target_hook_url": target_hook_url,
            "event_type": event_type,
            "custom_interest_value": custom_interest_value,
            "headers": headers,
        }
        return Webhook.model_validate(self._patch(f"/api/v2/webhooks/{id}", json=body))

    def delete(self, id: str) -> Webhook:
        """Delete a webhook."""
        return Webhook.model_validate(self._delete(f"/api/v2/webhooks/{id}"))

    def event_types(self) -> JSONObject:
        """List the webhook event types available to subscribe to."""
        return self._get("/api/v2/webhooks/event-types")

    def test(self, id: str) -> JSONObject:
        """Send a test payload to a webhook's target URL."""
        return self._post(f"/api/v2/webhooks/{id}/test")

    def resume(self, id: str) -> Webhook:
        """Resume a paused webhook."""
        return Webhook.model_validate(self._post(f"/api/v2/webhooks/{id}/resume"))

    def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        campaign: str | NotGiven = NOT_GIVEN,
        event_type: EventType | NotGiven = NOT_GIVEN,
    ) -> SyncCursorPage[Webhook]:
        """List webhooks. Auto-paginates: `for w in client.webhooks.list(): ...`."""

        def fetch_page(cursor: str | None) -> Any:
            return self._get(
                "/api/v2/webhooks",
                params={
                    "limit": limit,
                    "starting_after": cursor if cursor is not None else starting_after,
                    "campaign": campaign,
                    "event_type": event_type,
                },
            )

        return self._paginate(Webhook, fetch_page)


class AsyncWebhooks(AsyncAPIResource):
    async def create(
        self,
        *,
        target_hook_url: str,
        campaign: str | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        event_type: EventType | NotGiven = NOT_GIVEN,
        custom_interest_value: float | NotGiven = NOT_GIVEN,
        headers: JSONObject | NotGiven = NOT_GIVEN,
    ) -> Webhook:
        """Create a webhook."""
        body = {
            "campaign": campaign,
            "name": name,
            "target_hook_url": target_hook_url,
            "event_type": event_type,
            "custom_interest_value": custom_interest_value,
            "headers": headers,
        }
        return Webhook.model_validate(await self._post("/api/v2/webhooks", json=body))

    async def retrieve(self, id: str) -> Webhook:
        """Get a single webhook by ID."""
        return Webhook.model_validate(await self._get(f"/api/v2/webhooks/{id}"))

    async def update(
        self,
        id: str,
        *,
        campaign: str | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        target_hook_url: str | NotGiven = NOT_GIVEN,
        event_type: EventType | NotGiven = NOT_GIVEN,
        custom_interest_value: float | NotGiven = NOT_GIVEN,
        headers: JSONObject | NotGiven = NOT_GIVEN,
    ) -> Webhook:
        """Partially update a webhook. Omitted fields are left unchanged."""
        body = {
            "campaign": campaign,
            "name": name,
            "target_hook_url": target_hook_url,
            "event_type": event_type,
            "custom_interest_value": custom_interest_value,
            "headers": headers,
        }
        return Webhook.model_validate(await self._patch(f"/api/v2/webhooks/{id}", json=body))

    async def delete(self, id: str) -> Webhook:
        """Delete a webhook."""
        return Webhook.model_validate(await self._delete(f"/api/v2/webhooks/{id}"))

    async def event_types(self) -> JSONObject:
        """List the webhook event types available to subscribe to."""
        return await self._get("/api/v2/webhooks/event-types")

    async def test(self, id: str) -> JSONObject:
        """Send a test payload to a webhook's target URL."""
        return await self._post(f"/api/v2/webhooks/{id}/test")

    async def resume(self, id: str) -> Webhook:
        """Resume a paused webhook."""
        return Webhook.model_validate(await self._post(f"/api/v2/webhooks/{id}/resume"))

    async def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        campaign: str | NotGiven = NOT_GIVEN,
        event_type: EventType | NotGiven = NOT_GIVEN,
    ) -> AsyncCursorPage[Webhook]:
        """List webhooks. Auto-paginates: `async for w in await client.webhooks.list(): ...`."""

        async def fetch_page(cursor: str | None) -> Any:
            return await self._get(
                "/api/v2/webhooks",
                params={
                    "limit": limit,
                    "starting_after": cursor if cursor is not None else starting_after,
                    "campaign": campaign,
                    "event_type": event_type,
                },
            )

        return await self._paginate(Webhook, fetch_page)
