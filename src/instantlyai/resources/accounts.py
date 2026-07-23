"""Account resource: ``client.accounts``."""

from __future__ import annotations

from typing import Any, Literal

from .._pagination import AsyncCursorPage, SyncCursorPage
from .._transport import NOT_GIVEN, NotGiven
from .._types import JSONObject
from ..models import Account, BackgroundJob, Warmup
from ._base import AsyncAPIResource, SyncAPIResource

__all__ = ["Accounts", "AsyncAccounts"]

# Both resource classes define a `list()` method, which shadows the builtin
# `list` for annotation resolution anywhere else in this module's class
# bodies -- alias it once and use `_list[...]` instead of bare `list[...]`.
_list = list

_AccountFilter = Literal[
    "ACC_FILTER_PAUSED",
    "ACC_FILTER_ERROR",
    "ACC_FILTER_NO_CTD",
    "ACC_FILTER_PW_ACCOUNTS",
    "ACC_FILTER_DFY",
    "ACC_FILTER_DFY_SETUP_PENDING",
]
_AccountSortBy = Literal["timestamp_created", "email", "stat_warmup_score", "status"]
_SortOrder = Literal["asc", "desc"]


class Accounts(SyncAPIResource):
    def create(
        self,
        *,
        email: str,
        first_name: str,
        last_name: str,
        provider_code: float,
        imap_username: str,
        imap_password: str,
        imap_host: str,
        imap_port: float,
        smtp_username: str,
        smtp_password: str,
        smtp_host: str,
        smtp_port: float,
        warmup: Warmup | NotGiven = NOT_GIVEN,
        daily_limit: float | NotGiven = NOT_GIVEN,
        tracking_domain_name: str | NotGiven = NOT_GIVEN,
        tracking_domain_status: str | NotGiven = NOT_GIVEN,
        enable_slow_ramp: bool | NotGiven = NOT_GIVEN,
        inbox_placement_test_limit: float | NotGiven = NOT_GIVEN,
        sending_gap: float | NotGiven = NOT_GIVEN,
        signature: str | NotGiven = NOT_GIVEN,
        reply_to: str | NotGiven = NOT_GIVEN,
        warmup_custom_ftag: str | NotGiven = NOT_GIVEN,
        skip_cname_check: bool | NotGiven = NOT_GIVEN,
    ) -> Account:
        """Connect a new sending account."""
        body = {
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "provider_code": provider_code,
            "imap_username": imap_username,
            "imap_password": imap_password,
            "imap_host": imap_host,
            "imap_port": imap_port,
            "smtp_username": smtp_username,
            "smtp_password": smtp_password,
            "smtp_host": smtp_host,
            "smtp_port": smtp_port,
            "warmup": warmup,
            "daily_limit": daily_limit,
            "tracking_domain_name": tracking_domain_name,
            "tracking_domain_status": tracking_domain_status,
            "enable_slow_ramp": enable_slow_ramp,
            "inbox_placement_test_limit": inbox_placement_test_limit,
            "sending_gap": sending_gap,
            "signature": signature,
            "reply_to": reply_to,
            "warmup_custom_ftag": warmup_custom_ftag,
            "skip_cname_check": skip_cname_check,
        }
        return Account.model_validate(self._post("/api/v2/accounts", json=body))

    def retrieve(self, email: str) -> Account:
        """Get a single account by email."""
        return Account.model_validate(self._get(f"/api/v2/accounts/{email}"))

    def update(
        self,
        email: str,
        *,
        first_name: str | NotGiven = NOT_GIVEN,
        last_name: str | NotGiven = NOT_GIVEN,
        warmup: Warmup | None | NotGiven = NOT_GIVEN,
        daily_limit: float | None | NotGiven = NOT_GIVEN,
        tracking_domain_name: str | None | NotGiven = NOT_GIVEN,
        tracking_domain_status: str | None | NotGiven = NOT_GIVEN,
        enable_slow_ramp: bool | None | NotGiven = NOT_GIVEN,
        inbox_placement_test_limit: float | None | NotGiven = NOT_GIVEN,
        sending_gap: float | None | NotGiven = NOT_GIVEN,
        signature: str | None | NotGiven = NOT_GIVEN,
        reply_to: str | None | NotGiven = NOT_GIVEN,
        skip_cname_check: bool | NotGiven = NOT_GIVEN,
        remove_tracking_domain: bool | NotGiven = NOT_GIVEN,
    ) -> Account:
        """Partially update an account. Omitted fields are left unchanged."""
        body = {
            "first_name": first_name,
            "last_name": last_name,
            "warmup": warmup,
            "daily_limit": daily_limit,
            "tracking_domain_name": tracking_domain_name,
            "tracking_domain_status": tracking_domain_status,
            "enable_slow_ramp": enable_slow_ramp,
            "inbox_placement_test_limit": inbox_placement_test_limit,
            "sending_gap": sending_gap,
            "signature": signature,
            "reply_to": reply_to,
            "skip_cname_check": skip_cname_check,
            "remove_tracking_domain": remove_tracking_domain,
        }
        return Account.model_validate(self._patch(f"/api/v2/accounts/{email}", json=body))

    def delete(self, email: str) -> Account:
        """Delete an account."""
        return Account.model_validate(self._delete(f"/api/v2/accounts/{email}"))

    def pause(self, email: str) -> Account:
        """Pause an account."""
        return Account.model_validate(self._post(f"/api/v2/accounts/{email}/pause"))

    def resume(self, email: str) -> Account:
        """Resume a paused account."""
        return Account.model_validate(self._post(f"/api/v2/accounts/{email}/resume"))

    def mark_fixed(self, email: str) -> Account:
        """Mark an account as fixed."""
        return Account.model_validate(self._post(f"/api/v2/accounts/{email}/mark-fixed"))

    def move(
        self, *, emails: _list[str], source_workspace_id: str, destination_workspace_id: str
    ) -> JSONObject:
        """Move accounts to a different workspace."""
        return self._post(
            "/api/v2/accounts/move",
            json={
                "emails": emails,
                "source_workspace_id": source_workspace_id,
                "destination_workspace_id": destination_workspace_id,
            },
        )

    def test_vitals(self, *, accounts: _list[str] | NotGiven = NOT_GIVEN) -> JSONObject:
        """Test deliverability vitals for one or more accounts."""
        return self._post("/api/v2/accounts/test/vitals", json={"accounts": accounts})

    def enable_warmup(
        self,
        *,
        emails: _list[str] | NotGiven = NOT_GIVEN,
        include_all_emails: bool | NotGiven = NOT_GIVEN,
        excluded_emails: _list[str] | NotGiven = NOT_GIVEN,
        filter: JSONObject | NotGiven = NOT_GIVEN,
        search: str | NotGiven = NOT_GIVEN,
    ) -> BackgroundJob:
        """Enable warmup mode for a set of accounts."""
        body = {
            "emails": emails,
            "include_all_emails": include_all_emails,
            "excluded_emails": excluded_emails,
            "filter": filter,
            "search": search,
        }
        return BackgroundJob.model_validate(self._post("/api/v2/accounts/warmup/enable", json=body))

    def disable_warmup(
        self,
        *,
        emails: _list[str] | NotGiven = NOT_GIVEN,
        include_all_emails: bool | NotGiven = NOT_GIVEN,
        excluded_emails: _list[str] | NotGiven = NOT_GIVEN,
        filter: JSONObject | NotGiven = NOT_GIVEN,
        search: str | NotGiven = NOT_GIVEN,
    ) -> BackgroundJob:
        """Disable warmup mode for a set of accounts."""
        body = {
            "emails": emails,
            "include_all_emails": include_all_emails,
            "excluded_emails": excluded_emails,
            "filter": filter,
            "search": search,
        }
        return BackgroundJob.model_validate(
            self._post("/api/v2/accounts/warmup/disable", json=body)
        )

    def warmup_analytics(self, *, emails: _list[str]) -> JSONObject:
        """Get warmup analytics for a set of accounts."""
        return self._post("/api/v2/accounts/warmup-analytics", json={"emails": emails})

    def daily_analytics(
        self,
        *,
        start_date: str | NotGiven = NOT_GIVEN,
        end_date: str | NotGiven = NOT_GIVEN,
        emails: _list[str] | NotGiven = NOT_GIVEN,
    ) -> _list[JSONObject]:
        """Get daily account analytics."""
        return self._get(
            "/api/v2/accounts/analytics/daily",
            params={"start_date": start_date, "end_date": end_date, "emails": emails},
        )

    def ctd_status(self, *, host: str) -> JSONObject:
        """Get custom tracking domain status for a host."""
        return self._get("/api/v2/accounts/ctd/status", params={"host": host})

    def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        search: str | NotGiven = NOT_GIVEN,
        status: float | NotGiven = NOT_GIVEN,
        provider_code: float | NotGiven = NOT_GIVEN,
        tag_ids: str | NotGiven = NOT_GIVEN,
        tag_ids_all: str | NotGiven = NOT_GIVEN,
        include_tags: bool | NotGiven = NOT_GIVEN,
        filter: _AccountFilter | NotGiven = NOT_GIVEN,
        sort_by: _AccountSortBy | NotGiven = NOT_GIVEN,
        sort_order: _SortOrder | NotGiven = NOT_GIVEN,
        skip: int | NotGiven = NOT_GIVEN,
    ) -> SyncCursorPage[Account]:
        """List accounts. Auto-paginates: `for a in client.accounts.list(): ...`."""

        def fetch_page(cursor: str | None) -> Any:
            return self._get(
                "/api/v2/accounts",
                params={
                    "limit": limit,
                    "starting_after": cursor if cursor is not None else starting_after,
                    "search": search,
                    "status": status,
                    "provider_code": provider_code,
                    "tag_ids": tag_ids,
                    "tag_ids_all": tag_ids_all,
                    "include_tags": include_tags,
                    "filter": filter,
                    "sort_by": sort_by,
                    "sort_order": sort_order,
                    "skip": skip,
                },
            )

        return self._paginate(Account, fetch_page)


class AsyncAccounts(AsyncAPIResource):
    async def create(
        self,
        *,
        email: str,
        first_name: str,
        last_name: str,
        provider_code: float,
        imap_username: str,
        imap_password: str,
        imap_host: str,
        imap_port: float,
        smtp_username: str,
        smtp_password: str,
        smtp_host: str,
        smtp_port: float,
        warmup: Warmup | NotGiven = NOT_GIVEN,
        daily_limit: float | NotGiven = NOT_GIVEN,
        tracking_domain_name: str | NotGiven = NOT_GIVEN,
        tracking_domain_status: str | NotGiven = NOT_GIVEN,
        enable_slow_ramp: bool | NotGiven = NOT_GIVEN,
        inbox_placement_test_limit: float | NotGiven = NOT_GIVEN,
        sending_gap: float | NotGiven = NOT_GIVEN,
        signature: str | NotGiven = NOT_GIVEN,
        reply_to: str | NotGiven = NOT_GIVEN,
        warmup_custom_ftag: str | NotGiven = NOT_GIVEN,
        skip_cname_check: bool | NotGiven = NOT_GIVEN,
    ) -> Account:
        """Connect a new sending account."""
        body = {
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "provider_code": provider_code,
            "imap_username": imap_username,
            "imap_password": imap_password,
            "imap_host": imap_host,
            "imap_port": imap_port,
            "smtp_username": smtp_username,
            "smtp_password": smtp_password,
            "smtp_host": smtp_host,
            "smtp_port": smtp_port,
            "warmup": warmup,
            "daily_limit": daily_limit,
            "tracking_domain_name": tracking_domain_name,
            "tracking_domain_status": tracking_domain_status,
            "enable_slow_ramp": enable_slow_ramp,
            "inbox_placement_test_limit": inbox_placement_test_limit,
            "sending_gap": sending_gap,
            "signature": signature,
            "reply_to": reply_to,
            "warmup_custom_ftag": warmup_custom_ftag,
            "skip_cname_check": skip_cname_check,
        }
        return Account.model_validate(await self._post("/api/v2/accounts", json=body))

    async def retrieve(self, email: str) -> Account:
        """Get a single account by email."""
        return Account.model_validate(await self._get(f"/api/v2/accounts/{email}"))

    async def update(
        self,
        email: str,
        *,
        first_name: str | NotGiven = NOT_GIVEN,
        last_name: str | NotGiven = NOT_GIVEN,
        warmup: Warmup | None | NotGiven = NOT_GIVEN,
        daily_limit: float | None | NotGiven = NOT_GIVEN,
        tracking_domain_name: str | None | NotGiven = NOT_GIVEN,
        tracking_domain_status: str | None | NotGiven = NOT_GIVEN,
        enable_slow_ramp: bool | None | NotGiven = NOT_GIVEN,
        inbox_placement_test_limit: float | None | NotGiven = NOT_GIVEN,
        sending_gap: float | None | NotGiven = NOT_GIVEN,
        signature: str | None | NotGiven = NOT_GIVEN,
        reply_to: str | None | NotGiven = NOT_GIVEN,
        skip_cname_check: bool | NotGiven = NOT_GIVEN,
        remove_tracking_domain: bool | NotGiven = NOT_GIVEN,
    ) -> Account:
        """Partially update an account. Omitted fields are left unchanged."""
        body = {
            "first_name": first_name,
            "last_name": last_name,
            "warmup": warmup,
            "daily_limit": daily_limit,
            "tracking_domain_name": tracking_domain_name,
            "tracking_domain_status": tracking_domain_status,
            "enable_slow_ramp": enable_slow_ramp,
            "inbox_placement_test_limit": inbox_placement_test_limit,
            "sending_gap": sending_gap,
            "signature": signature,
            "reply_to": reply_to,
            "skip_cname_check": skip_cname_check,
            "remove_tracking_domain": remove_tracking_domain,
        }
        return Account.model_validate(await self._patch(f"/api/v2/accounts/{email}", json=body))

    async def delete(self, email: str) -> Account:
        """Delete an account."""
        return Account.model_validate(await self._delete(f"/api/v2/accounts/{email}"))

    async def pause(self, email: str) -> Account:
        """Pause an account."""
        return Account.model_validate(await self._post(f"/api/v2/accounts/{email}/pause"))

    async def resume(self, email: str) -> Account:
        """Resume a paused account."""
        return Account.model_validate(await self._post(f"/api/v2/accounts/{email}/resume"))

    async def mark_fixed(self, email: str) -> Account:
        """Mark an account as fixed."""
        return Account.model_validate(await self._post(f"/api/v2/accounts/{email}/mark-fixed"))

    async def move(
        self, *, emails: _list[str], source_workspace_id: str, destination_workspace_id: str
    ) -> JSONObject:
        """Move accounts to a different workspace."""
        return await self._post(
            "/api/v2/accounts/move",
            json={
                "emails": emails,
                "source_workspace_id": source_workspace_id,
                "destination_workspace_id": destination_workspace_id,
            },
        )

    async def test_vitals(self, *, accounts: _list[str] | NotGiven = NOT_GIVEN) -> JSONObject:
        """Test deliverability vitals for one or more accounts."""
        return await self._post("/api/v2/accounts/test/vitals", json={"accounts": accounts})

    async def enable_warmup(
        self,
        *,
        emails: _list[str] | NotGiven = NOT_GIVEN,
        include_all_emails: bool | NotGiven = NOT_GIVEN,
        excluded_emails: _list[str] | NotGiven = NOT_GIVEN,
        filter: JSONObject | NotGiven = NOT_GIVEN,
        search: str | NotGiven = NOT_GIVEN,
    ) -> BackgroundJob:
        """Enable warmup mode for a set of accounts."""
        body = {
            "emails": emails,
            "include_all_emails": include_all_emails,
            "excluded_emails": excluded_emails,
            "filter": filter,
            "search": search,
        }
        return BackgroundJob.model_validate(
            await self._post("/api/v2/accounts/warmup/enable", json=body)
        )

    async def disable_warmup(
        self,
        *,
        emails: _list[str] | NotGiven = NOT_GIVEN,
        include_all_emails: bool | NotGiven = NOT_GIVEN,
        excluded_emails: _list[str] | NotGiven = NOT_GIVEN,
        filter: JSONObject | NotGiven = NOT_GIVEN,
        search: str | NotGiven = NOT_GIVEN,
    ) -> BackgroundJob:
        """Disable warmup mode for a set of accounts."""
        body = {
            "emails": emails,
            "include_all_emails": include_all_emails,
            "excluded_emails": excluded_emails,
            "filter": filter,
            "search": search,
        }
        return BackgroundJob.model_validate(
            await self._post("/api/v2/accounts/warmup/disable", json=body)
        )

    async def warmup_analytics(self, *, emails: _list[str]) -> JSONObject:
        """Get warmup analytics for a set of accounts."""
        return await self._post("/api/v2/accounts/warmup-analytics", json={"emails": emails})

    async def daily_analytics(
        self,
        *,
        start_date: str | NotGiven = NOT_GIVEN,
        end_date: str | NotGiven = NOT_GIVEN,
        emails: _list[str] | NotGiven = NOT_GIVEN,
    ) -> _list[JSONObject]:
        """Get daily account analytics."""
        return await self._get(
            "/api/v2/accounts/analytics/daily",
            params={"start_date": start_date, "end_date": end_date, "emails": emails},
        )

    async def ctd_status(self, *, host: str) -> JSONObject:
        """Get custom tracking domain status for a host."""
        return await self._get("/api/v2/accounts/ctd/status", params={"host": host})

    async def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        search: str | NotGiven = NOT_GIVEN,
        status: float | NotGiven = NOT_GIVEN,
        provider_code: float | NotGiven = NOT_GIVEN,
        tag_ids: str | NotGiven = NOT_GIVEN,
        tag_ids_all: str | NotGiven = NOT_GIVEN,
        include_tags: bool | NotGiven = NOT_GIVEN,
        filter: _AccountFilter | NotGiven = NOT_GIVEN,
        sort_by: _AccountSortBy | NotGiven = NOT_GIVEN,
        sort_order: _SortOrder | NotGiven = NOT_GIVEN,
        skip: int | NotGiven = NOT_GIVEN,
    ) -> AsyncCursorPage[Account]:
        """List accounts. Auto-paginates: `async for a in await client.accounts.list(): ...`."""

        async def fetch_page(cursor: str | None) -> Any:
            return await self._get(
                "/api/v2/accounts",
                params={
                    "limit": limit,
                    "starting_after": cursor if cursor is not None else starting_after,
                    "search": search,
                    "status": status,
                    "provider_code": provider_code,
                    "tag_ids": tag_ids,
                    "tag_ids_all": tag_ids_all,
                    "include_tags": include_tags,
                    "filter": filter,
                    "sort_by": sort_by,
                    "sort_order": sort_order,
                    "skip": skip,
                },
            )

        return await self._paginate(Account, fetch_page)
