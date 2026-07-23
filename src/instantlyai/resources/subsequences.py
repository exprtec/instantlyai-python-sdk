"""Campaign subsequence resource: ``client.subsequences`` (see campaigns.py)."""

from __future__ import annotations

from typing import Any, Literal

from .._pagination import AsyncCursorPage, SyncCursorPage
from .._transport import NOT_GIVEN, NotGiven
from .._types import JSONObject
from ..models import CampaignSubsequence, Conditions, Sequence1, SubsequenceSchedule
from ._base import AsyncAPIResource, SyncAPIResource

__all__ = ["AsyncCampaignSubsequences", "CampaignSubsequences"]

# Both resource classes define a `list()` method, which shadows the builtin
# `list` for annotation resolution anywhere else in this module's class
# bodies -- alias it once and use `_list[...]` instead of bare `list[...]`.
_list = list

_DailyLimitMode = Literal["inherit", "custom", "unlimited"]


class CampaignSubsequences(SyncAPIResource):
    def create(
        self,
        *,
        parent_campaign: str,
        name: str,
        conditions: Conditions,
        subsequence_schedule: SubsequenceSchedule,
        sequences: _list[Sequence1],
        daily_limit_mode: _DailyLimitMode | NotGiven = NOT_GIVEN,
        daily_limit: float | NotGiven = NOT_GIVEN,
        ignore_account_daily_limit: bool | NotGiven = NOT_GIVEN,
    ) -> CampaignSubsequence:
        """Create campaign subsequence."""
        body = {
            "parent_campaign": parent_campaign,
            "name": name,
            "conditions": conditions,
            "subsequence_schedule": subsequence_schedule,
            "sequences": sequences,
            "daily_limit_mode": daily_limit_mode,
            "daily_limit": daily_limit,
            "ignore_account_daily_limit": ignore_account_daily_limit,
        }
        return CampaignSubsequence.model_validate(self._post("/api/v2/subsequences", json=body))

    def retrieve(self, id: str) -> CampaignSubsequence:
        """Get campaign subsequence."""
        return CampaignSubsequence.model_validate(self._get(f"/api/v2/subsequences/{id}"))

    def update(
        self,
        id: str,
        *,
        name: str | NotGiven = NOT_GIVEN,
        daily_limit_mode: _DailyLimitMode | None | NotGiven = NOT_GIVEN,
        daily_limit: float | None | NotGiven = NOT_GIVEN,
        ignore_account_daily_limit: bool | None | NotGiven = NOT_GIVEN,
    ) -> CampaignSubsequence:
        """Patch campaign subsequence."""
        body = {
            "name": name,
            "daily_limit_mode": daily_limit_mode,
            "daily_limit": daily_limit,
            "ignore_account_daily_limit": ignore_account_daily_limit,
        }
        return CampaignSubsequence.model_validate(
            self._patch(f"/api/v2/subsequences/{id}", json=body)
        )

    def delete(self, id: str) -> CampaignSubsequence:
        """Delete campaign subsequence."""
        return CampaignSubsequence.model_validate(self._delete(f"/api/v2/subsequences/{id}"))

    def duplicate(self, id: str, *, parent_campaign: str, name: str) -> CampaignSubsequence:
        """Duplicate a subsequence."""
        return CampaignSubsequence.model_validate(
            self._post(
                f"/api/v2/subsequences/{id}/duplicate",
                json={"parent_campaign": parent_campaign, "name": name},
            )
        )

    def pause(self, id: str) -> CampaignSubsequence:
        """Pause a subsequence."""
        return CampaignSubsequence.model_validate(self._post(f"/api/v2/subsequences/{id}/pause"))

    def resume(self, id: str) -> CampaignSubsequence:
        """Resume a paused subsequence."""
        return CampaignSubsequence.model_validate(self._post(f"/api/v2/subsequences/{id}/resume"))

    def sending_status(
        self, id: str, *, with_ai_summary: bool | NotGiven = NOT_GIVEN
    ) -> JSONObject:
        """Get subsequence sending status."""
        return self._get(
            f"/api/v2/subsequences/{id}/sending-status", params={"with_ai_summary": with_ai_summary}
        )

    def list(
        self,
        *,
        parent_campaign: str,
        limit: int | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        search: str | NotGiven = NOT_GIVEN,
    ) -> SyncCursorPage[CampaignSubsequence]:
        """List campaign subsequence. Auto-paginates: `for s in client.subsequences.list(...): ...`."""

        def fetch_page(cursor: str | None) -> Any:
            return self._get(
                "/api/v2/subsequences",
                params={
                    "limit": limit,
                    "starting_after": cursor if cursor is not None else starting_after,
                    "parent_campaign": parent_campaign,
                    "search": search,
                },
            )

        return self._paginate(CampaignSubsequence, fetch_page)


class AsyncCampaignSubsequences(AsyncAPIResource):
    async def create(
        self,
        *,
        parent_campaign: str,
        name: str,
        conditions: Conditions,
        subsequence_schedule: SubsequenceSchedule,
        sequences: _list[Sequence1],
        daily_limit_mode: _DailyLimitMode | NotGiven = NOT_GIVEN,
        daily_limit: float | NotGiven = NOT_GIVEN,
        ignore_account_daily_limit: bool | NotGiven = NOT_GIVEN,
    ) -> CampaignSubsequence:
        """Create campaign subsequence."""
        body = {
            "parent_campaign": parent_campaign,
            "name": name,
            "conditions": conditions,
            "subsequence_schedule": subsequence_schedule,
            "sequences": sequences,
            "daily_limit_mode": daily_limit_mode,
            "daily_limit": daily_limit,
            "ignore_account_daily_limit": ignore_account_daily_limit,
        }
        return CampaignSubsequence.model_validate(
            await self._post("/api/v2/subsequences", json=body)
        )

    async def retrieve(self, id: str) -> CampaignSubsequence:
        """Get campaign subsequence."""
        return CampaignSubsequence.model_validate(await self._get(f"/api/v2/subsequences/{id}"))

    async def update(
        self,
        id: str,
        *,
        name: str | NotGiven = NOT_GIVEN,
        daily_limit_mode: _DailyLimitMode | None | NotGiven = NOT_GIVEN,
        daily_limit: float | None | NotGiven = NOT_GIVEN,
        ignore_account_daily_limit: bool | None | NotGiven = NOT_GIVEN,
    ) -> CampaignSubsequence:
        """Patch campaign subsequence."""
        body = {
            "name": name,
            "daily_limit_mode": daily_limit_mode,
            "daily_limit": daily_limit,
            "ignore_account_daily_limit": ignore_account_daily_limit,
        }
        return CampaignSubsequence.model_validate(
            await self._patch(f"/api/v2/subsequences/{id}", json=body)
        )

    async def delete(self, id: str) -> CampaignSubsequence:
        """Delete campaign subsequence."""
        return CampaignSubsequence.model_validate(await self._delete(f"/api/v2/subsequences/{id}"))

    async def duplicate(self, id: str, *, parent_campaign: str, name: str) -> CampaignSubsequence:
        """Duplicate a subsequence."""
        return CampaignSubsequence.model_validate(
            await self._post(
                f"/api/v2/subsequences/{id}/duplicate",
                json={"parent_campaign": parent_campaign, "name": name},
            )
        )

    async def pause(self, id: str) -> CampaignSubsequence:
        """Pause a subsequence."""
        return CampaignSubsequence.model_validate(
            await self._post(f"/api/v2/subsequences/{id}/pause")
        )

    async def resume(self, id: str) -> CampaignSubsequence:
        """Resume a paused subsequence."""
        return CampaignSubsequence.model_validate(
            await self._post(f"/api/v2/subsequences/{id}/resume")
        )

    async def sending_status(
        self, id: str, *, with_ai_summary: bool | NotGiven = NOT_GIVEN
    ) -> JSONObject:
        """Get subsequence sending status."""
        return await self._get(
            f"/api/v2/subsequences/{id}/sending-status", params={"with_ai_summary": with_ai_summary}
        )

    async def list(
        self,
        *,
        parent_campaign: str,
        limit: int | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        search: str | NotGiven = NOT_GIVEN,
    ) -> AsyncCursorPage[CampaignSubsequence]:
        """List campaign subsequence. Auto-paginates: `async for s in await client.subsequences.list(...): ...`."""

        async def fetch_page(cursor: str | None) -> Any:
            return await self._get(
                "/api/v2/subsequences",
                params={
                    "limit": limit,
                    "starting_after": cursor if cursor is not None else starting_after,
                    "parent_campaign": parent_campaign,
                    "search": search,
                },
            )

        return await self._paginate(CampaignSubsequence, fetch_page)
