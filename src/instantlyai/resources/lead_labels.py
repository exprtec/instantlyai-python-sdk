"""Lead label resource: ``client.lead_labels``."""

from __future__ import annotations

from typing import Any, Literal

from .._pagination import AsyncCursorPage, SyncCursorPage
from .._transport import NOT_GIVEN, NotGiven
from .._types import JSONObject
from ..models import LeadLabel
from ._base import AsyncAPIResource, SyncAPIResource

__all__ = ["AsyncLeadLabels", "LeadLabels"]

# Both resource classes define a `list()` method, which shadows the builtin
# `list` for annotation resolution anywhere else in this module's class
# bodies -- alias it once and use `_list[...]` instead of bare `list[...]`.
_list = list

_InterestStatusLabel = Literal["positive", "negative", "neutral"]


class LeadLabels(SyncAPIResource):
    def create(
        self,
        *,
        label: str,
        interest_status_label: _InterestStatusLabel,
        description: str | NotGiven = NOT_GIVEN,
        use_with_ai: bool | NotGiven = NOT_GIVEN,
    ) -> LeadLabel:
        """Create lead label."""
        return LeadLabel.model_validate(
            self._post(
                "/api/v2/lead-labels",
                json={
                    "label": label,
                    "interest_status_label": interest_status_label,
                    "description": description,
                    "use_with_ai": use_with_ai,
                },
            )
        )

    def retrieve(self, id: str) -> LeadLabel:
        """Get lead label."""
        return LeadLabel.model_validate(self._get(f"/api/v2/lead-labels/{id}"))

    def update(
        self,
        id: str,
        *,
        label: str | NotGiven = NOT_GIVEN,
        interest_status_label: _InterestStatusLabel | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        use_with_ai: bool | NotGiven = NOT_GIVEN,
    ) -> LeadLabel:
        """Patch lead label. Omitted fields are left unchanged."""
        return LeadLabel.model_validate(
            self._patch(
                f"/api/v2/lead-labels/{id}",
                json={
                    "label": label,
                    "interest_status_label": interest_status_label,
                    "description": description,
                    "use_with_ai": use_with_ai,
                },
            )
        )

    def delete(self, id: str, *, reassigned_status: float | NotGiven = NOT_GIVEN) -> LeadLabel:
        """Delete lead label."""
        return LeadLabel.model_validate(
            self._delete(f"/api/v2/lead-labels/{id}", json={"reassigned_status": reassigned_status})
        )

    def test_ai_reply_label(self, *, reply_text: str) -> JSONObject:
        """Test AI reply label prediction."""
        return self._post("/api/v2/lead-labels/ai-reply-label", json={"reply_text": reply_text})

    def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        search: str | NotGiven = NOT_GIVEN,
        interest_status: _InterestStatusLabel | NotGiven = NOT_GIVEN,
    ) -> SyncCursorPage[LeadLabel]:
        """List lead label. Auto-paginates: `for l in client.lead_labels.list(): ...`."""

        def fetch_page(cursor: str | None) -> Any:
            return self._get(
                "/api/v2/lead-labels",
                params={
                    "limit": limit,
                    "starting_after": cursor if cursor is not None else starting_after,
                    "search": search,
                    "interest_status": interest_status,
                },
            )

        return self._paginate(LeadLabel, fetch_page)


class AsyncLeadLabels(AsyncAPIResource):
    async def create(
        self,
        *,
        label: str,
        interest_status_label: _InterestStatusLabel,
        description: str | NotGiven = NOT_GIVEN,
        use_with_ai: bool | NotGiven = NOT_GIVEN,
    ) -> LeadLabel:
        """Create lead label."""
        return LeadLabel.model_validate(
            await self._post(
                "/api/v2/lead-labels",
                json={
                    "label": label,
                    "interest_status_label": interest_status_label,
                    "description": description,
                    "use_with_ai": use_with_ai,
                },
            )
        )

    async def retrieve(self, id: str) -> LeadLabel:
        """Get lead label."""
        return LeadLabel.model_validate(await self._get(f"/api/v2/lead-labels/{id}"))

    async def update(
        self,
        id: str,
        *,
        label: str | NotGiven = NOT_GIVEN,
        interest_status_label: _InterestStatusLabel | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        use_with_ai: bool | NotGiven = NOT_GIVEN,
    ) -> LeadLabel:
        """Patch lead label. Omitted fields are left unchanged."""
        return LeadLabel.model_validate(
            await self._patch(
                f"/api/v2/lead-labels/{id}",
                json={
                    "label": label,
                    "interest_status_label": interest_status_label,
                    "description": description,
                    "use_with_ai": use_with_ai,
                },
            )
        )

    async def delete(
        self, id: str, *, reassigned_status: float | NotGiven = NOT_GIVEN
    ) -> LeadLabel:
        """Delete lead label."""
        return LeadLabel.model_validate(
            await self._delete(
                f"/api/v2/lead-labels/{id}", json={"reassigned_status": reassigned_status}
            )
        )

    async def test_ai_reply_label(self, *, reply_text: str) -> JSONObject:
        """Test AI reply label prediction."""
        return await self._post(
            "/api/v2/lead-labels/ai-reply-label", json={"reply_text": reply_text}
        )

    async def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        search: str | NotGiven = NOT_GIVEN,
        interest_status: _InterestStatusLabel | NotGiven = NOT_GIVEN,
    ) -> AsyncCursorPage[LeadLabel]:
        """List lead label. Auto-paginates: `async for l in await client.lead_labels.list(): ...`."""

        async def fetch_page(cursor: str | None) -> Any:
            return await self._get(
                "/api/v2/lead-labels",
                params={
                    "limit": limit,
                    "starting_after": cursor if cursor is not None else starting_after,
                    "search": search,
                    "interest_status": interest_status,
                },
            )

        return await self._paginate(LeadLabel, fetch_page)
