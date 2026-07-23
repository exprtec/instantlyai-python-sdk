"""Inbox placement test resource: ``client.inbox_placement_tests``."""

from __future__ import annotations

from typing import Any, Literal

from .._pagination import AsyncCursorPage, SyncCursorPage
from .._transport import NOT_GIVEN, NotGiven
from .._types import JSONObject
from ..models import Automation, InboxPlacementTest, RecipientsLabel, Schedule1
from ._base import AsyncAPIResource, SyncAPIResource

__all__ = ["AsyncInboxPlacementTests", "InboxPlacementTests"]

# Both resource classes define a `list()` method, which shadows the builtin
# `list` for annotation resolution anywhere else in this module's class
# bodies -- alias it once and use `_list[...]` instead of bare `list[...]`.
_list = list

_DeliveryMode = Literal[1, 2]
_TestType = Literal[1, 2]
_SendingMethod = Literal[1, 2]
_TestStatus = Literal[1, 2, 3]
_NotSendingStatus = Literal["daily_limits_hit", "other"]
_SortOrder = Literal["asc", "desc"]


class InboxPlacementTests(SyncAPIResource):
    def create(
        self,
        *,
        name: str,
        type: _TestType,
        sending_method: _SendingMethod,
        email_subject: str,
        email_body: str,
        emails: _list[str],
        delivery_mode: _DeliveryMode | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        schedule: Schedule1 | NotGiven = NOT_GIVEN,
        campaign_id: str | NotGiven = NOT_GIVEN,
        test_code: str | NotGiven = NOT_GIVEN,
        tags: _list[str] | NotGiven = NOT_GIVEN,
        text_only: bool | NotGiven = NOT_GIVEN,
        recipients_labels: _list[RecipientsLabel] | NotGiven = NOT_GIVEN,
        timestamp_next_run: str | NotGiven = NOT_GIVEN,
        automations: _list[Automation] | NotGiven = NOT_GIVEN,
        status: _TestStatus | NotGiven = NOT_GIVEN,
        not_sending_status: _NotSendingStatus | NotGiven = NOT_GIVEN,
        run_immediately: bool | NotGiven = NOT_GIVEN,
    ) -> InboxPlacementTest:
        """Create an inbox placement test."""
        body = {
            "name": name,
            "type": type,
            "sending_method": sending_method,
            "email_subject": email_subject,
            "email_body": email_body,
            "emails": emails,
            "delivery_mode": delivery_mode,
            "description": description,
            "schedule": schedule,
            "campaign_id": campaign_id,
            "test_code": test_code,
            "tags": tags,
            "text_only": text_only,
            "recipients_labels": recipients_labels,
            "timestamp_next_run": timestamp_next_run,
            "automations": automations,
            "status": status,
            "not_sending_status": not_sending_status,
            "run_immediately": run_immediately,
        }
        return InboxPlacementTest.model_validate(
            self._post("/api/v2/inbox-placement-tests", json=body)
        )

    def retrieve(self, id: str, *, with_metadata: bool | NotGiven = NOT_GIVEN) -> JSONObject:
        """Get an inbox placement test."""
        return self._get(
            f"/api/v2/inbox-placement-tests/{id}", params={"with_metadata": with_metadata}
        )

    def update(
        self,
        id: str,
        *,
        name: str | NotGiven = NOT_GIVEN,
        schedule: Schedule1 | None | NotGiven = NOT_GIVEN,
        automations: _list[Automation] | None | NotGiven = NOT_GIVEN,
        status: _TestStatus | None | NotGiven = NOT_GIVEN,
    ) -> InboxPlacementTest:
        """Partially update an inbox placement test. Omitted fields are left unchanged."""
        body = {"name": name, "schedule": schedule, "automations": automations, "status": status}
        return InboxPlacementTest.model_validate(
            self._patch(f"/api/v2/inbox-placement-tests/{id}", json=body)
        )

    def delete(self, id: str) -> InboxPlacementTest:
        """Delete an inbox placement test."""
        return InboxPlacementTest.model_validate(
            self._delete(f"/api/v2/inbox-placement-tests/{id}")
        )

    def esp_options(self) -> _list[JSONObject]:
        """Get ESP options for inbox placement tests."""
        return self._get("/api/v2/inbox-placement-tests/email-service-provider-options")

    def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        search: str | NotGiven = NOT_GIVEN,
        status: float | NotGiven = NOT_GIVEN,
        sort_order: _SortOrder | NotGiven = NOT_GIVEN,
    ) -> SyncCursorPage[InboxPlacementTest]:
        """List inbox placement tests. Auto-paginates: `for t in client.inbox_placement_tests.list(): ...`."""

        def fetch_page(cursor: str | None) -> Any:
            return self._get(
                "/api/v2/inbox-placement-tests",
                params={
                    "limit": limit,
                    "starting_after": cursor if cursor is not None else starting_after,
                    "search": search,
                    "status": status,
                    "sort_order": sort_order,
                },
            )

        return self._paginate(InboxPlacementTest, fetch_page)


class AsyncInboxPlacementTests(AsyncAPIResource):
    async def create(
        self,
        *,
        name: str,
        type: _TestType,
        sending_method: _SendingMethod,
        email_subject: str,
        email_body: str,
        emails: _list[str],
        delivery_mode: _DeliveryMode | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        schedule: Schedule1 | NotGiven = NOT_GIVEN,
        campaign_id: str | NotGiven = NOT_GIVEN,
        test_code: str | NotGiven = NOT_GIVEN,
        tags: _list[str] | NotGiven = NOT_GIVEN,
        text_only: bool | NotGiven = NOT_GIVEN,
        recipients_labels: _list[RecipientsLabel] | NotGiven = NOT_GIVEN,
        timestamp_next_run: str | NotGiven = NOT_GIVEN,
        automations: _list[Automation] | NotGiven = NOT_GIVEN,
        status: _TestStatus | NotGiven = NOT_GIVEN,
        not_sending_status: _NotSendingStatus | NotGiven = NOT_GIVEN,
        run_immediately: bool | NotGiven = NOT_GIVEN,
    ) -> InboxPlacementTest:
        """Create an inbox placement test."""
        body = {
            "name": name,
            "type": type,
            "sending_method": sending_method,
            "email_subject": email_subject,
            "email_body": email_body,
            "emails": emails,
            "delivery_mode": delivery_mode,
            "description": description,
            "schedule": schedule,
            "campaign_id": campaign_id,
            "test_code": test_code,
            "tags": tags,
            "text_only": text_only,
            "recipients_labels": recipients_labels,
            "timestamp_next_run": timestamp_next_run,
            "automations": automations,
            "status": status,
            "not_sending_status": not_sending_status,
            "run_immediately": run_immediately,
        }
        return InboxPlacementTest.model_validate(
            await self._post("/api/v2/inbox-placement-tests", json=body)
        )

    async def retrieve(self, id: str, *, with_metadata: bool | NotGiven = NOT_GIVEN) -> JSONObject:
        """Get an inbox placement test."""
        return await self._get(
            f"/api/v2/inbox-placement-tests/{id}", params={"with_metadata": with_metadata}
        )

    async def update(
        self,
        id: str,
        *,
        name: str | NotGiven = NOT_GIVEN,
        schedule: Schedule1 | None | NotGiven = NOT_GIVEN,
        automations: _list[Automation] | None | NotGiven = NOT_GIVEN,
        status: _TestStatus | None | NotGiven = NOT_GIVEN,
    ) -> InboxPlacementTest:
        """Partially update an inbox placement test. Omitted fields are left unchanged."""
        body = {"name": name, "schedule": schedule, "automations": automations, "status": status}
        return InboxPlacementTest.model_validate(
            await self._patch(f"/api/v2/inbox-placement-tests/{id}", json=body)
        )

    async def delete(self, id: str) -> InboxPlacementTest:
        """Delete an inbox placement test."""
        return InboxPlacementTest.model_validate(
            await self._delete(f"/api/v2/inbox-placement-tests/{id}")
        )

    async def esp_options(self) -> _list[JSONObject]:
        """Get ESP options for inbox placement tests."""
        return await self._get("/api/v2/inbox-placement-tests/email-service-provider-options")

    async def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        search: str | NotGiven = NOT_GIVEN,
        status: float | NotGiven = NOT_GIVEN,
        sort_order: _SortOrder | NotGiven = NOT_GIVEN,
    ) -> AsyncCursorPage[InboxPlacementTest]:
        """List inbox placement tests. Auto-paginates: `async for t in await client.inbox_placement_tests.list(): ...`."""

        async def fetch_page(cursor: str | None) -> Any:
            return await self._get(
                "/api/v2/inbox-placement-tests",
                params={
                    "limit": limit,
                    "starting_after": cursor if cursor is not None else starting_after,
                    "search": search,
                    "status": status,
                    "sort_order": sort_order,
                },
            )

        return await self._paginate(InboxPlacementTest, fetch_page)
