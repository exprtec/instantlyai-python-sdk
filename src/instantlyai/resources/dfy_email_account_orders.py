"""DFY email account order resource: ``client.dfy_email_account_orders``."""

from __future__ import annotations

from typing import Any, Literal

from .._pagination import AsyncCursorPage, SyncCursorPage
from .._transport import NOT_GIVEN, NotGiven
from .._types import JSONObject
from ..models import DFYEmailAccountOrder
from ._base import AsyncAPIResource, SyncAPIResource

__all__ = ["AsyncDFYEmailAccountOrders", "DFYEmailAccountOrders"]

# Both resource classes define a `list()` method, which shadows the builtin
# `list` for annotation resolution anywhere else in this module's class
# bodies -- alias it once and use `_list[...]` instead of bare `list[...]`.
_list = list

_OrderType = Literal["dfy", "pre_warmed_up", "extra_accounts"]
_PreWarmedUpDomainExtension = Literal["com", "org", "co"]
_SimilarDomainTld = Literal["com", "org"]


class DFYEmailAccountOrders(SyncAPIResource):
    def create(
        self,
        *,
        items: _list[JSONObject],
        order_type: _OrderType,
        simulation: bool | NotGiven = NOT_GIVEN,
    ) -> JSONObject:
        """Place a DFY email account order."""
        body = {"items": items, "order_type": order_type, "simulation": simulation}
        return self._post("/api/v2/dfy-email-account-orders", json=body)

    def cancel_accounts(self, *, accounts: _list[str]) -> JSONObject:
        """Cancel DFY email accounts."""
        return self._post(
            "/api/v2/dfy-email-account-orders/accounts/cancel", json={"accounts": accounts}
        )

    def check_domains_availability(self, *, domains: _list[str]) -> JSONObject:
        """Check domains availability."""
        return self._post(
            "/api/v2/dfy-email-account-orders/domains/check", json={"domains": domains}
        )

    def pre_warmed_up_domains(
        self,
        *,
        extensions: _list[_PreWarmedUpDomainExtension] | NotGiven = NOT_GIVEN,
        search: str | NotGiven = NOT_GIVEN,
    ) -> JSONObject:
        """Get pre-warmed up domains."""
        return self._post(
            "/api/v2/dfy-email-account-orders/domains/pre-warmed-up-list",
            json={"extensions": extensions, "search": search},
        )

    def similar_domains(
        self, *, domain: str, tlds: _list[_SimilarDomainTld] | NotGiven = NOT_GIVEN
    ) -> JSONObject:
        """Generate similar available domains."""
        return self._post(
            "/api/v2/dfy-email-account-orders/domains/similar",
            json={"domain": domain, "tlds": tlds},
        )

    def list_accounts(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        with_passwords: bool | NotGiven = NOT_GIVEN,
    ) -> SyncCursorPage[JSONObject]:
        """List DFY ordered email accounts. Auto-paginates: `for a in client.dfy_email_account_orders.list_accounts(): ...`."""

        def get_next_page(cursor: str | None) -> SyncCursorPage[JSONObject]:
            body = self._get(
                "/api/v2/dfy-email-account-orders/accounts",
                params={
                    "limit": limit,
                    "starting_after": cursor if cursor is not None else starting_after,
                    "with_passwords": with_passwords,
                },
            )
            items = body.get("items", [])
            return SyncCursorPage(
                items, body.get("next_starting_after"), get_next_page=get_next_page
            )

        return get_next_page(None)

    def list(
        self, *, limit: int | NotGiven = NOT_GIVEN, starting_after: str | NotGiven = NOT_GIVEN
    ) -> SyncCursorPage[DFYEmailAccountOrder]:
        """List DFY email account orders. Auto-paginates: `for o in client.dfy_email_account_orders.list(): ...`."""

        def fetch_page(cursor: str | None) -> Any:
            return self._get(
                "/api/v2/dfy-email-account-orders",
                params={
                    "limit": limit,
                    "starting_after": cursor if cursor is not None else starting_after,
                },
            )

        return self._paginate(DFYEmailAccountOrder, fetch_page)


class AsyncDFYEmailAccountOrders(AsyncAPIResource):
    async def create(
        self,
        *,
        items: _list[JSONObject],
        order_type: _OrderType,
        simulation: bool | NotGiven = NOT_GIVEN,
    ) -> JSONObject:
        """Place a DFY email account order."""
        body = {"items": items, "order_type": order_type, "simulation": simulation}
        return await self._post("/api/v2/dfy-email-account-orders", json=body)

    async def cancel_accounts(self, *, accounts: _list[str]) -> JSONObject:
        """Cancel DFY email accounts."""
        return await self._post(
            "/api/v2/dfy-email-account-orders/accounts/cancel", json={"accounts": accounts}
        )

    async def check_domains_availability(self, *, domains: _list[str]) -> JSONObject:
        """Check domains availability."""
        return await self._post(
            "/api/v2/dfy-email-account-orders/domains/check", json={"domains": domains}
        )

    async def pre_warmed_up_domains(
        self,
        *,
        extensions: _list[_PreWarmedUpDomainExtension] | NotGiven = NOT_GIVEN,
        search: str | NotGiven = NOT_GIVEN,
    ) -> JSONObject:
        """Get pre-warmed up domains."""
        return await self._post(
            "/api/v2/dfy-email-account-orders/domains/pre-warmed-up-list",
            json={"extensions": extensions, "search": search},
        )

    async def similar_domains(
        self, *, domain: str, tlds: _list[_SimilarDomainTld] | NotGiven = NOT_GIVEN
    ) -> JSONObject:
        """Generate similar available domains."""
        return await self._post(
            "/api/v2/dfy-email-account-orders/domains/similar",
            json={"domain": domain, "tlds": tlds},
        )

    async def list_accounts(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        with_passwords: bool | NotGiven = NOT_GIVEN,
    ) -> AsyncCursorPage[JSONObject]:
        """List DFY ordered email accounts. Auto-paginates: `async for a in await client.dfy_email_account_orders.list_accounts(): ...`."""

        async def get_next_page(cursor: str | None) -> AsyncCursorPage[JSONObject]:
            body = await self._get(
                "/api/v2/dfy-email-account-orders/accounts",
                params={
                    "limit": limit,
                    "starting_after": cursor if cursor is not None else starting_after,
                    "with_passwords": with_passwords,
                },
            )
            items = body.get("items", [])
            return AsyncCursorPage(
                items, body.get("next_starting_after"), get_next_page=get_next_page
            )

        return await get_next_page(None)

    async def list(
        self, *, limit: int | NotGiven = NOT_GIVEN, starting_after: str | NotGiven = NOT_GIVEN
    ) -> AsyncCursorPage[DFYEmailAccountOrder]:
        """List DFY email account orders. Auto-paginates: `async for o in await client.dfy_email_account_orders.list(): ...`."""

        async def fetch_page(cursor: str | None) -> Any:
            return await self._get(
                "/api/v2/dfy-email-account-orders",
                params={
                    "limit": limit,
                    "starting_after": cursor if cursor is not None else starting_after,
                },
            )

        return await self._paginate(DFYEmailAccountOrder, fetch_page)
