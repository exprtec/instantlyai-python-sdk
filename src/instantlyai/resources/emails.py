"""Email resource: ``client.emails``."""

from __future__ import annotations

from typing import Any, Literal

from .._pagination import AsyncCursorPage, SyncCursorPage
from .._transport import NOT_GIVEN, NotGiven
from .._types import JSONObject
from ..models import Body, Email
from ._base import AsyncAPIResource, SyncAPIResource

__all__ = ["AsyncEmails", "Emails"]

# Both resource classes define a `list()` method, which shadows the builtin
# `list` for annotation resolution anywhere else in this module's class
# bodies -- alias it once and use `_list[...]` instead of bare `list[...]`.
_list = list

_EmailMode = Literal["emode_focused", "emode_others", "emode_all"]
_SortOrder = Literal["asc", "desc"]
_EmailType = Literal["received", "sent", "manual"]


class Emails(SyncAPIResource):
    def test(
        self, *, eaccount: str, to_address_email_list: str, subject: str, body: Body
    ) -> JSONObject:
        """Send a test email."""
        return self._post(
            "/api/v2/emails/test",
            json={
                "eaccount": eaccount,
                "to_address_email_list": to_address_email_list,
                "subject": subject,
                "body": body,
            },
        )

    def reply(
        self,
        *,
        eaccount: str,
        reply_to_uuid: str,
        subject: str,
        body: Body,
        additional_recipients: _list[str] | NotGiven = NOT_GIVEN,
        cc_address_email_list: str | NotGiven = NOT_GIVEN,
        bcc_address_email_list: str | NotGiven = NOT_GIVEN,
        reminder_ts: str | NotGiven = NOT_GIVEN,
        assigned_to: str | NotGiven = NOT_GIVEN,
    ) -> Email:
        """Reply to an email."""
        return Email.model_validate(
            self._post(
                "/api/v2/emails/reply",
                json={
                    "eaccount": eaccount,
                    "reply_to_uuid": reply_to_uuid,
                    "subject": subject,
                    "body": body,
                    "additional_recipients": additional_recipients,
                    "cc_address_email_list": cc_address_email_list,
                    "bcc_address_email_list": bcc_address_email_list,
                    "reminder_ts": reminder_ts,
                    "assigned_to": assigned_to,
                },
            )
        )

    def forward(
        self,
        *,
        eaccount: str,
        reply_to_uuid: str,
        to_address_email_list: str,
        subject: str,
        body: Body | NotGiven = NOT_GIVEN,
        cc_address_email_list: str | NotGiven = NOT_GIVEN,
        bcc_address_email_list: str | NotGiven = NOT_GIVEN,
        reply_to: str | NotGiven = NOT_GIVEN,
        forwarded_attachments: str | NotGiven = NOT_GIVEN,
        include_original_body: bool | NotGiven = NOT_GIVEN,
        assigned_to: str | NotGiven = NOT_GIVEN,
    ) -> Email:
        """Forward an email."""
        return Email.model_validate(
            self._post(
                "/api/v2/emails/forward",
                json={
                    "eaccount": eaccount,
                    "reply_to_uuid": reply_to_uuid,
                    "to_address_email_list": to_address_email_list,
                    "subject": subject,
                    "body": body,
                    "cc_address_email_list": cc_address_email_list,
                    "bcc_address_email_list": bcc_address_email_list,
                    "reply_to": reply_to,
                    "forwarded_attachments": forwarded_attachments,
                    "include_original_body": include_original_body,
                    "assigned_to": assigned_to,
                },
            )
        )

    def retrieve(self, id: str) -> Email:
        """Get email."""
        return Email.model_validate(self._get(f"/api/v2/emails/{id}"))

    def update(
        self,
        id: str,
        *,
        is_unread: float | NotGiven = NOT_GIVEN,
        reminder_ts: str | NotGiven = NOT_GIVEN,
    ) -> Email:
        """Patch email."""
        return Email.model_validate(
            self._patch(
                f"/api/v2/emails/{id}", json={"is_unread": is_unread, "reminder_ts": reminder_ts}
            )
        )

    def delete(self, id: str) -> Email:
        """Delete email."""
        return Email.model_validate(self._delete(f"/api/v2/emails/{id}"))

    def unread_count(self) -> JSONObject:
        """Count unread emails."""
        return self._get("/api/v2/emails/unread/count")

    def mark_thread_read(self, thread_id: str) -> JSONObject:
        """Mark all emails in a thread as read."""
        return self._post(f"/api/v2/emails/threads/{thread_id}/mark-as-read")

    def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        search: str | NotGiven = NOT_GIVEN,
        campaign_id: str | NotGiven = NOT_GIVEN,
        list_id: str | NotGiven = NOT_GIVEN,
        i_status: float | NotGiven = NOT_GIVEN,
        eaccount: str | NotGiven = NOT_GIVEN,
        is_unread: bool | NotGiven = NOT_GIVEN,
        has_reminder: bool | NotGiven = NOT_GIVEN,
        mode: _EmailMode | NotGiven = NOT_GIVEN,
        preview_only: bool | NotGiven = NOT_GIVEN,
        sort_order: _SortOrder | NotGiven = NOT_GIVEN,
        scheduled_only: bool | NotGiven = NOT_GIVEN,
        assigned_to: str | NotGiven = NOT_GIVEN,
        lead: str | NotGiven = NOT_GIVEN,
        company_domain: str | NotGiven = NOT_GIVEN,
        marked_as_done: bool | NotGiven = NOT_GIVEN,
        email_type: _EmailType | NotGiven = NOT_GIVEN,
        min_timestamp_created: str | NotGiven = NOT_GIVEN,
        max_timestamp_created: str | NotGiven = NOT_GIVEN,
        latest_of_thread: bool | NotGiven = NOT_GIVEN,
    ) -> SyncCursorPage[Email]:
        """List email. Auto-paginates: `for e in client.emails.list(): ...`."""

        def fetch_page(cursor: str | None) -> Any:
            return self._get(
                "/api/v2/emails",
                params={
                    "limit": limit,
                    "starting_after": cursor if cursor is not None else starting_after,
                    "search": search,
                    "campaign_id": campaign_id,
                    "list_id": list_id,
                    "i_status": i_status,
                    "eaccount": eaccount,
                    "is_unread": is_unread,
                    "has_reminder": has_reminder,
                    "mode": mode,
                    "preview_only": preview_only,
                    "sort_order": sort_order,
                    "scheduled_only": scheduled_only,
                    "assigned_to": assigned_to,
                    "lead": lead,
                    "company_domain": company_domain,
                    "marked_as_done": marked_as_done,
                    "email_type": email_type,
                    "min_timestamp_created": min_timestamp_created,
                    "max_timestamp_created": max_timestamp_created,
                    "latest_of_thread": latest_of_thread,
                },
            )

        return self._paginate(Email, fetch_page)


class AsyncEmails(AsyncAPIResource):
    async def test(
        self, *, eaccount: str, to_address_email_list: str, subject: str, body: Body
    ) -> JSONObject:
        """Send a test email."""
        return await self._post(
            "/api/v2/emails/test",
            json={
                "eaccount": eaccount,
                "to_address_email_list": to_address_email_list,
                "subject": subject,
                "body": body,
            },
        )

    async def reply(
        self,
        *,
        eaccount: str,
        reply_to_uuid: str,
        subject: str,
        body: Body,
        additional_recipients: _list[str] | NotGiven = NOT_GIVEN,
        cc_address_email_list: str | NotGiven = NOT_GIVEN,
        bcc_address_email_list: str | NotGiven = NOT_GIVEN,
        reminder_ts: str | NotGiven = NOT_GIVEN,
        assigned_to: str | NotGiven = NOT_GIVEN,
    ) -> Email:
        """Reply to an email."""
        return Email.model_validate(
            await self._post(
                "/api/v2/emails/reply",
                json={
                    "eaccount": eaccount,
                    "reply_to_uuid": reply_to_uuid,
                    "subject": subject,
                    "body": body,
                    "additional_recipients": additional_recipients,
                    "cc_address_email_list": cc_address_email_list,
                    "bcc_address_email_list": bcc_address_email_list,
                    "reminder_ts": reminder_ts,
                    "assigned_to": assigned_to,
                },
            )
        )

    async def forward(
        self,
        *,
        eaccount: str,
        reply_to_uuid: str,
        to_address_email_list: str,
        subject: str,
        body: Body | NotGiven = NOT_GIVEN,
        cc_address_email_list: str | NotGiven = NOT_GIVEN,
        bcc_address_email_list: str | NotGiven = NOT_GIVEN,
        reply_to: str | NotGiven = NOT_GIVEN,
        forwarded_attachments: str | NotGiven = NOT_GIVEN,
        include_original_body: bool | NotGiven = NOT_GIVEN,
        assigned_to: str | NotGiven = NOT_GIVEN,
    ) -> Email:
        """Forward an email."""
        return Email.model_validate(
            await self._post(
                "/api/v2/emails/forward",
                json={
                    "eaccount": eaccount,
                    "reply_to_uuid": reply_to_uuid,
                    "to_address_email_list": to_address_email_list,
                    "subject": subject,
                    "body": body,
                    "cc_address_email_list": cc_address_email_list,
                    "bcc_address_email_list": bcc_address_email_list,
                    "reply_to": reply_to,
                    "forwarded_attachments": forwarded_attachments,
                    "include_original_body": include_original_body,
                    "assigned_to": assigned_to,
                },
            )
        )

    async def retrieve(self, id: str) -> Email:
        """Get email."""
        return Email.model_validate(await self._get(f"/api/v2/emails/{id}"))

    async def update(
        self,
        id: str,
        *,
        is_unread: float | NotGiven = NOT_GIVEN,
        reminder_ts: str | NotGiven = NOT_GIVEN,
    ) -> Email:
        """Patch email."""
        return Email.model_validate(
            await self._patch(
                f"/api/v2/emails/{id}", json={"is_unread": is_unread, "reminder_ts": reminder_ts}
            )
        )

    async def delete(self, id: str) -> Email:
        """Delete email."""
        return Email.model_validate(await self._delete(f"/api/v2/emails/{id}"))

    async def unread_count(self) -> JSONObject:
        """Count unread emails."""
        return await self._get("/api/v2/emails/unread/count")

    async def mark_thread_read(self, thread_id: str) -> JSONObject:
        """Mark all emails in a thread as read."""
        return await self._post(f"/api/v2/emails/threads/{thread_id}/mark-as-read")

    async def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        search: str | NotGiven = NOT_GIVEN,
        campaign_id: str | NotGiven = NOT_GIVEN,
        list_id: str | NotGiven = NOT_GIVEN,
        i_status: float | NotGiven = NOT_GIVEN,
        eaccount: str | NotGiven = NOT_GIVEN,
        is_unread: bool | NotGiven = NOT_GIVEN,
        has_reminder: bool | NotGiven = NOT_GIVEN,
        mode: _EmailMode | NotGiven = NOT_GIVEN,
        preview_only: bool | NotGiven = NOT_GIVEN,
        sort_order: _SortOrder | NotGiven = NOT_GIVEN,
        scheduled_only: bool | NotGiven = NOT_GIVEN,
        assigned_to: str | NotGiven = NOT_GIVEN,
        lead: str | NotGiven = NOT_GIVEN,
        company_domain: str | NotGiven = NOT_GIVEN,
        marked_as_done: bool | NotGiven = NOT_GIVEN,
        email_type: _EmailType | NotGiven = NOT_GIVEN,
        min_timestamp_created: str | NotGiven = NOT_GIVEN,
        max_timestamp_created: str | NotGiven = NOT_GIVEN,
        latest_of_thread: bool | NotGiven = NOT_GIVEN,
    ) -> AsyncCursorPage[Email]:
        """List email. Auto-paginates: `async for e in await client.emails.list(): ...`."""

        async def fetch_page(cursor: str | None) -> Any:
            return await self._get(
                "/api/v2/emails",
                params={
                    "limit": limit,
                    "starting_after": cursor if cursor is not None else starting_after,
                    "search": search,
                    "campaign_id": campaign_id,
                    "list_id": list_id,
                    "i_status": i_status,
                    "eaccount": eaccount,
                    "is_unread": is_unread,
                    "has_reminder": has_reminder,
                    "mode": mode,
                    "preview_only": preview_only,
                    "sort_order": sort_order,
                    "scheduled_only": scheduled_only,
                    "assigned_to": assigned_to,
                    "lead": lead,
                    "company_domain": company_domain,
                    "marked_as_done": marked_as_done,
                    "email_type": email_type,
                    "min_timestamp_created": min_timestamp_created,
                    "max_timestamp_created": max_timestamp_created,
                    "latest_of_thread": latest_of_thread,
                },
            )

        return await self._paginate(Email, fetch_page)
