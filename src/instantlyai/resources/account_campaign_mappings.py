"""Account campaign mapping resource: ``client.account_campaign_mappings``."""

from __future__ import annotations

from typing import Any

from .._pagination import AsyncCursorPage, SyncCursorPage
from .._transport import NOT_GIVEN, NotGiven
from ..models import AccountCampaignMapping
from ._base import AsyncAPIResource, SyncAPIResource

__all__ = ["AccountCampaignMappings", "AsyncAccountCampaignMappings"]

# Both resource classes define a `list()` method, which shadows the builtin
# `list` for annotation resolution anywhere else in this module's class
# bodies -- alias it once and use `_list[...]` instead of bare `list[...]`.
_list = list


class AccountCampaignMappings(SyncAPIResource):
    def list(
        self,
        email: str,
        *,
        limit: float | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
    ) -> SyncCursorPage[AccountCampaignMapping]:
        """List campaigns associated with an account email. Auto-paginates."""

        def fetch_page(cursor: str | None) -> Any:
            return self._get(
                f"/api/v2/account-campaign-mappings/{email}",
                params={
                    "limit": limit,
                    "starting_after": cursor if cursor is not None else starting_after,
                },
            )

        return self._paginate(AccountCampaignMapping, fetch_page)


class AsyncAccountCampaignMappings(AsyncAPIResource):
    async def list(
        self,
        email: str,
        *,
        limit: float | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
    ) -> AsyncCursorPage[AccountCampaignMapping]:
        """List campaigns associated with an account email. Auto-paginates."""

        async def fetch_page(cursor: str | None) -> Any:
            return await self._get(
                f"/api/v2/account-campaign-mappings/{email}",
                params={
                    "limit": limit,
                    "starting_after": cursor if cursor is not None else starting_after,
                },
            )

        return await self._paginate(AccountCampaignMapping, fetch_page)
