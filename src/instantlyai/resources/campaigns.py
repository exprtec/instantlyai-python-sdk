"""Campaign resource: ``client.campaigns`` / ``client.subsequences`` (see subsequences.py)."""

from __future__ import annotations

from typing import Any, Literal

from .._pagination import AsyncCursorPage, SyncCursorPage
from .._transport import NOT_GIVEN, NotGiven
from .._types import JSONObject
from ..models import (
    AutoVariantSelect,
    Campaign,
    CampaignSchedule,
    LimitEmailsPerCompanyOverride,
    ProviderRoutingRule,
    Sequence,
)
from ._base import AsyncAPIResource, SyncAPIResource

__all__ = ["AsyncCampaigns", "Campaigns"]

# Both resource classes define a `list()` method, which shadows the builtin
# `list` for annotation resolution anywhere else in this module's class
# bodies -- alias it once and use `_list[...]` instead of bare `list[...]`.
_list = list

_CampaignStatus = Literal[-99, -2, -1, 0, 1, 2, 3, 4]


class Campaigns(SyncAPIResource):
    def create(
        self,
        *,
        name: str,
        campaign_schedule: CampaignSchedule,
        pl_value: float | NotGiven = NOT_GIVEN,
        is_evergreen: bool | NotGiven = NOT_GIVEN,
        sequences: _list[Sequence] | NotGiven = NOT_GIVEN,
        email_gap: float | NotGiven = NOT_GIVEN,
        random_wait_max: float | NotGiven = NOT_GIVEN,
        text_only: bool | NotGiven = NOT_GIVEN,
        first_email_text_only: bool | NotGiven = NOT_GIVEN,
        email_list: _list[str] | NotGiven = NOT_GIVEN,
        daily_limit: float | NotGiven = NOT_GIVEN,
        stop_on_reply: bool | NotGiven = NOT_GIVEN,
        email_tag_list: _list[str] | NotGiven = NOT_GIVEN,
        link_tracking: bool | NotGiven = NOT_GIVEN,
        open_tracking: bool | NotGiven = NOT_GIVEN,
        stop_on_auto_reply: bool | NotGiven = NOT_GIVEN,
        daily_max_leads: int | NotGiven = NOT_GIVEN,
        prioritize_new_leads: bool | NotGiven = NOT_GIVEN,
        auto_variant_select: AutoVariantSelect | NotGiven = NOT_GIVEN,
        match_lead_esp: bool | NotGiven = NOT_GIVEN,
        stop_for_company: bool | NotGiven = NOT_GIVEN,
        insert_unsubscribe_header: bool | NotGiven = NOT_GIVEN,
        allow_risky_contacts: bool | NotGiven = NOT_GIVEN,
        disable_bounce_protect: bool | NotGiven = NOT_GIVEN,
        limit_emails_per_company_override: LimitEmailsPerCompanyOverride | NotGiven = NOT_GIVEN,
        cc_list: _list[str] | NotGiven = NOT_GIVEN,
        bcc_list: _list[str] | NotGiven = NOT_GIVEN,
        owned_by: str | NotGiven = NOT_GIVEN,
        ai_sdr_id: str | NotGiven = NOT_GIVEN,
        provider_routing_rules: _list[ProviderRoutingRule] | NotGiven = NOT_GIVEN,
    ) -> Campaign:
        """Create a campaign. Requires scope: `campaigns:create`, `campaigns:all`, or `all:all`."""
        body = {
            "name": name,
            "campaign_schedule": campaign_schedule,
            "pl_value": pl_value,
            "is_evergreen": is_evergreen,
            "sequences": sequences,
            "email_gap": email_gap,
            "random_wait_max": random_wait_max,
            "text_only": text_only,
            "first_email_text_only": first_email_text_only,
            "email_list": email_list,
            "daily_limit": daily_limit,
            "stop_on_reply": stop_on_reply,
            "email_tag_list": email_tag_list,
            "link_tracking": link_tracking,
            "open_tracking": open_tracking,
            "stop_on_auto_reply": stop_on_auto_reply,
            "daily_max_leads": daily_max_leads,
            "prioritize_new_leads": prioritize_new_leads,
            "auto_variant_select": auto_variant_select,
            "match_lead_esp": match_lead_esp,
            "stop_for_company": stop_for_company,
            "insert_unsubscribe_header": insert_unsubscribe_header,
            "allow_risky_contacts": allow_risky_contacts,
            "disable_bounce_protect": disable_bounce_protect,
            "limit_emails_per_company_override": limit_emails_per_company_override,
            "cc_list": cc_list,
            "bcc_list": bcc_list,
            "owned_by": owned_by,
            "ai_sdr_id": ai_sdr_id,
            "provider_routing_rules": provider_routing_rules,
        }
        return Campaign.model_validate(self._post("/api/v2/campaigns", json=body))

    def retrieve(self, id: str) -> Campaign:
        """Get a single campaign by ID."""
        return Campaign.model_validate(self._get(f"/api/v2/campaigns/{id}"))

    def update(
        self,
        id: str,
        *,
        name: str | NotGiven = NOT_GIVEN,
        pl_value: float | None | NotGiven = NOT_GIVEN,
        is_evergreen: bool | None | NotGiven = NOT_GIVEN,
        campaign_schedule: CampaignSchedule | NotGiven = NOT_GIVEN,
        sequences: _list[Sequence] | None | NotGiven = NOT_GIVEN,
        email_gap: float | None | NotGiven = NOT_GIVEN,
        random_wait_max: float | None | NotGiven = NOT_GIVEN,
        text_only: bool | None | NotGiven = NOT_GIVEN,
        first_email_text_only: bool | None | NotGiven = NOT_GIVEN,
        email_list: _list[str] | None | NotGiven = NOT_GIVEN,
        daily_limit: float | None | NotGiven = NOT_GIVEN,
        stop_on_reply: bool | None | NotGiven = NOT_GIVEN,
        email_tag_list: _list[str] | None | NotGiven = NOT_GIVEN,
        link_tracking: bool | None | NotGiven = NOT_GIVEN,
        open_tracking: bool | None | NotGiven = NOT_GIVEN,
        stop_on_auto_reply: bool | None | NotGiven = NOT_GIVEN,
        daily_max_leads: int | None | NotGiven = NOT_GIVEN,
        prioritize_new_leads: bool | None | NotGiven = NOT_GIVEN,
        auto_variant_select: AutoVariantSelect | None | NotGiven = NOT_GIVEN,
        match_lead_esp: bool | None | NotGiven = NOT_GIVEN,
        stop_for_company: bool | None | NotGiven = NOT_GIVEN,
        insert_unsubscribe_header: bool | None | NotGiven = NOT_GIVEN,
        allow_risky_contacts: bool | None | NotGiven = NOT_GIVEN,
        disable_bounce_protect: bool | None | NotGiven = NOT_GIVEN,
        limit_emails_per_company_override: LimitEmailsPerCompanyOverride
        | None
        | NotGiven = NOT_GIVEN,
        cc_list: _list[str] | None | NotGiven = NOT_GIVEN,
        bcc_list: _list[str] | None | NotGiven = NOT_GIVEN,
        owned_by: str | None | NotGiven = NOT_GIVEN,
        provider_routing_rules: _list[ProviderRoutingRule] | None | NotGiven = NOT_GIVEN,
    ) -> Campaign:
        """Partially update a campaign. Omitted fields are left unchanged."""
        body = {
            "name": name,
            "pl_value": pl_value,
            "is_evergreen": is_evergreen,
            "campaign_schedule": campaign_schedule,
            "sequences": sequences,
            "email_gap": email_gap,
            "random_wait_max": random_wait_max,
            "text_only": text_only,
            "first_email_text_only": first_email_text_only,
            "email_list": email_list,
            "daily_limit": daily_limit,
            "stop_on_reply": stop_on_reply,
            "email_tag_list": email_tag_list,
            "link_tracking": link_tracking,
            "open_tracking": open_tracking,
            "stop_on_auto_reply": stop_on_auto_reply,
            "daily_max_leads": daily_max_leads,
            "prioritize_new_leads": prioritize_new_leads,
            "auto_variant_select": auto_variant_select,
            "match_lead_esp": match_lead_esp,
            "stop_for_company": stop_for_company,
            "insert_unsubscribe_header": insert_unsubscribe_header,
            "allow_risky_contacts": allow_risky_contacts,
            "disable_bounce_protect": disable_bounce_protect,
            "limit_emails_per_company_override": limit_emails_per_company_override,
            "cc_list": cc_list,
            "bcc_list": bcc_list,
            "owned_by": owned_by,
            "provider_routing_rules": provider_routing_rules,
        }
        return Campaign.model_validate(self._patch(f"/api/v2/campaigns/{id}", json=body))

    def delete(self, id: str) -> Campaign:
        """Delete a campaign."""
        return Campaign.model_validate(self._delete(f"/api/v2/campaigns/{id}"))

    def activate(self, id: str) -> Campaign:
        """Activate (start), or resume, a campaign."""
        return Campaign.model_validate(self._post(f"/api/v2/campaigns/{id}/activate"))

    def pause(self, id: str) -> Campaign:
        """Stop (or pause) a campaign."""
        return Campaign.model_validate(self._post(f"/api/v2/campaigns/{id}/pause"))

    def duplicate(self, id: str, *, name: str | NotGiven = NOT_GIVEN) -> Campaign:
        """Duplicate a campaign."""
        return Campaign.model_validate(
            self._post(f"/api/v2/campaigns/{id}/duplicate", json={"name": name})
        )

    def export(self, id: str) -> Campaign:
        """Export a campaign to JSON format."""
        return Campaign.model_validate(self._post(f"/api/v2/campaigns/{id}/export"))

    def create_from_export(self, id: str) -> Campaign:
        """Create a campaign from a previously shared/exported one."""
        return Campaign.model_validate(self._post(f"/api/v2/campaigns/{id}/from-export"))

    def share(self, id: str) -> None:
        """Share a campaign."""
        self._post(f"/api/v2/campaigns/{id}/share")

    def add_variables(self, id: str, *, variables: _list[str] | NotGiven = NOT_GIVEN) -> Campaign:
        """Add campaign variables."""
        return Campaign.model_validate(
            self._post(f"/api/v2/campaigns/{id}/variables", json={"variables": variables})
        )

    def sending_status(
        self, id: str, *, with_ai_summary: bool | NotGiven = NOT_GIVEN
    ) -> JSONObject:
        """Get campaign sending status (diagnostics + summary)."""
        return self._get(
            f"/api/v2/campaigns/{id}/sending-status", params={"with_ai_summary": with_ai_summary}
        )

    def search_by_contact(
        self,
        *,
        search: str | NotGiven = NOT_GIVEN,
        sort_column: str | NotGiven = NOT_GIVEN,
        sort_order: str | NotGiven = NOT_GIVEN,
    ) -> JSONObject:
        """Search campaigns by lead email."""
        return self._get(
            "/api/v2/campaigns/search-by-contact",
            params={"search": search, "sort_column": sort_column, "sort_order": sort_order},
        )

    def count_launched(self) -> JSONObject:
        """Get the count of launched campaigns."""
        return self._get("/api/v2/campaigns/count-launched")

    def analytics(
        self,
        *,
        id: str | NotGiven = NOT_GIVEN,
        ids: _list[str] | NotGiven = NOT_GIVEN,
        start_date: str | NotGiven = NOT_GIVEN,
        end_date: str | NotGiven = NOT_GIVEN,
        exclude_total_leads_count: bool | NotGiven = NOT_GIVEN,
    ) -> _list[JSONObject]:
        """Get analytics for one or more campaigns."""
        return self._get(
            "/api/v2/campaigns/analytics",
            params={
                "id": id,
                "ids": ids,
                "start_date": start_date,
                "end_date": end_date,
                "exclude_total_leads_count": exclude_total_leads_count,
            },
        )

    def analytics_overview(
        self,
        *,
        id: str | NotGiven = NOT_GIVEN,
        ids: _list[str] | NotGiven = NOT_GIVEN,
        start_date: str | NotGiven = NOT_GIVEN,
        end_date: str | NotGiven = NOT_GIVEN,
        campaign_status: float | NotGiven = NOT_GIVEN,
        expand_crm_events: bool | NotGiven = NOT_GIVEN,
    ) -> JSONObject:
        """Get an aggregate analytics overview across campaigns."""
        return self._get(
            "/api/v2/campaigns/analytics/overview",
            params={
                "id": id,
                "ids": ids,
                "start_date": start_date,
                "end_date": end_date,
                "campaign_status": campaign_status,
                "expand_crm_events": expand_crm_events,
            },
        )

    def analytics_daily(
        self,
        *,
        campaign_id: str | NotGiven = NOT_GIVEN,
        start_date: str | NotGiven = NOT_GIVEN,
        end_date: str | NotGiven = NOT_GIVEN,
        campaign_status: float | NotGiven = NOT_GIVEN,
    ) -> _list[JSONObject]:
        """Get daily campaign analytics."""
        return self._get(
            "/api/v2/campaigns/analytics/daily",
            params={
                "campaign_id": campaign_id,
                "start_date": start_date,
                "end_date": end_date,
                "campaign_status": campaign_status,
            },
        )

    def analytics_steps(
        self,
        *,
        campaign_id: str | NotGiven = NOT_GIVEN,
        start_date: str | NotGiven = NOT_GIVEN,
        end_date: str | NotGiven = NOT_GIVEN,
        include_opportunities_count: bool | NotGiven = NOT_GIVEN,
    ) -> _list[JSONObject]:
        """Get per-step campaign analytics."""
        return self._get(
            "/api/v2/campaigns/analytics/steps",
            params={
                "campaign_id": campaign_id,
                "start_date": start_date,
                "end_date": end_date,
                "include_opportunities_count": include_opportunities_count,
            },
        )

    def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        search: str | NotGiven = NOT_GIVEN,
        tag_ids: str | NotGiven = NOT_GIVEN,
        ai_sales_agent_id: str | NotGiven = NOT_GIVEN,
        status: _CampaignStatus | NotGiven = NOT_GIVEN,
    ) -> SyncCursorPage[Campaign]:
        """List campaigns. Auto-paginates: `for c in client.campaigns.list(): ...`."""

        def fetch_page(cursor: str | None) -> Any:
            return self._get(
                "/api/v2/campaigns",
                params={
                    "limit": limit,
                    "starting_after": cursor if cursor is not None else starting_after,
                    "search": search,
                    "tag_ids": tag_ids,
                    "ai_sales_agent_id": ai_sales_agent_id,
                    "status": status,
                },
            )

        return self._paginate(Campaign, fetch_page)


class AsyncCampaigns(AsyncAPIResource):
    async def create(
        self,
        *,
        name: str,
        campaign_schedule: CampaignSchedule,
        pl_value: float | NotGiven = NOT_GIVEN,
        is_evergreen: bool | NotGiven = NOT_GIVEN,
        sequences: _list[Sequence] | NotGiven = NOT_GIVEN,
        email_gap: float | NotGiven = NOT_GIVEN,
        random_wait_max: float | NotGiven = NOT_GIVEN,
        text_only: bool | NotGiven = NOT_GIVEN,
        first_email_text_only: bool | NotGiven = NOT_GIVEN,
        email_list: _list[str] | NotGiven = NOT_GIVEN,
        daily_limit: float | NotGiven = NOT_GIVEN,
        stop_on_reply: bool | NotGiven = NOT_GIVEN,
        email_tag_list: _list[str] | NotGiven = NOT_GIVEN,
        link_tracking: bool | NotGiven = NOT_GIVEN,
        open_tracking: bool | NotGiven = NOT_GIVEN,
        stop_on_auto_reply: bool | NotGiven = NOT_GIVEN,
        daily_max_leads: int | NotGiven = NOT_GIVEN,
        prioritize_new_leads: bool | NotGiven = NOT_GIVEN,
        auto_variant_select: AutoVariantSelect | NotGiven = NOT_GIVEN,
        match_lead_esp: bool | NotGiven = NOT_GIVEN,
        stop_for_company: bool | NotGiven = NOT_GIVEN,
        insert_unsubscribe_header: bool | NotGiven = NOT_GIVEN,
        allow_risky_contacts: bool | NotGiven = NOT_GIVEN,
        disable_bounce_protect: bool | NotGiven = NOT_GIVEN,
        limit_emails_per_company_override: LimitEmailsPerCompanyOverride | NotGiven = NOT_GIVEN,
        cc_list: _list[str] | NotGiven = NOT_GIVEN,
        bcc_list: _list[str] | NotGiven = NOT_GIVEN,
        owned_by: str | NotGiven = NOT_GIVEN,
        ai_sdr_id: str | NotGiven = NOT_GIVEN,
        provider_routing_rules: _list[ProviderRoutingRule] | NotGiven = NOT_GIVEN,
    ) -> Campaign:
        """Create a campaign. Requires scope: `campaigns:create`, `campaigns:all`, or `all:all`."""
        body = {
            "name": name,
            "campaign_schedule": campaign_schedule,
            "pl_value": pl_value,
            "is_evergreen": is_evergreen,
            "sequences": sequences,
            "email_gap": email_gap,
            "random_wait_max": random_wait_max,
            "text_only": text_only,
            "first_email_text_only": first_email_text_only,
            "email_list": email_list,
            "daily_limit": daily_limit,
            "stop_on_reply": stop_on_reply,
            "email_tag_list": email_tag_list,
            "link_tracking": link_tracking,
            "open_tracking": open_tracking,
            "stop_on_auto_reply": stop_on_auto_reply,
            "daily_max_leads": daily_max_leads,
            "prioritize_new_leads": prioritize_new_leads,
            "auto_variant_select": auto_variant_select,
            "match_lead_esp": match_lead_esp,
            "stop_for_company": stop_for_company,
            "insert_unsubscribe_header": insert_unsubscribe_header,
            "allow_risky_contacts": allow_risky_contacts,
            "disable_bounce_protect": disable_bounce_protect,
            "limit_emails_per_company_override": limit_emails_per_company_override,
            "cc_list": cc_list,
            "bcc_list": bcc_list,
            "owned_by": owned_by,
            "ai_sdr_id": ai_sdr_id,
            "provider_routing_rules": provider_routing_rules,
        }
        return Campaign.model_validate(await self._post("/api/v2/campaigns", json=body))

    async def retrieve(self, id: str) -> Campaign:
        """Get a single campaign by ID."""
        return Campaign.model_validate(await self._get(f"/api/v2/campaigns/{id}"))

    async def update(
        self,
        id: str,
        *,
        name: str | NotGiven = NOT_GIVEN,
        pl_value: float | None | NotGiven = NOT_GIVEN,
        is_evergreen: bool | None | NotGiven = NOT_GIVEN,
        campaign_schedule: CampaignSchedule | NotGiven = NOT_GIVEN,
        sequences: _list[Sequence] | None | NotGiven = NOT_GIVEN,
        email_gap: float | None | NotGiven = NOT_GIVEN,
        random_wait_max: float | None | NotGiven = NOT_GIVEN,
        text_only: bool | None | NotGiven = NOT_GIVEN,
        first_email_text_only: bool | None | NotGiven = NOT_GIVEN,
        email_list: _list[str] | None | NotGiven = NOT_GIVEN,
        daily_limit: float | None | NotGiven = NOT_GIVEN,
        stop_on_reply: bool | None | NotGiven = NOT_GIVEN,
        email_tag_list: _list[str] | None | NotGiven = NOT_GIVEN,
        link_tracking: bool | None | NotGiven = NOT_GIVEN,
        open_tracking: bool | None | NotGiven = NOT_GIVEN,
        stop_on_auto_reply: bool | None | NotGiven = NOT_GIVEN,
        daily_max_leads: int | None | NotGiven = NOT_GIVEN,
        prioritize_new_leads: bool | None | NotGiven = NOT_GIVEN,
        auto_variant_select: AutoVariantSelect | None | NotGiven = NOT_GIVEN,
        match_lead_esp: bool | None | NotGiven = NOT_GIVEN,
        stop_for_company: bool | None | NotGiven = NOT_GIVEN,
        insert_unsubscribe_header: bool | None | NotGiven = NOT_GIVEN,
        allow_risky_contacts: bool | None | NotGiven = NOT_GIVEN,
        disable_bounce_protect: bool | None | NotGiven = NOT_GIVEN,
        limit_emails_per_company_override: LimitEmailsPerCompanyOverride
        | None
        | NotGiven = NOT_GIVEN,
        cc_list: _list[str] | None | NotGiven = NOT_GIVEN,
        bcc_list: _list[str] | None | NotGiven = NOT_GIVEN,
        owned_by: str | None | NotGiven = NOT_GIVEN,
        provider_routing_rules: _list[ProviderRoutingRule] | None | NotGiven = NOT_GIVEN,
    ) -> Campaign:
        """Partially update a campaign. Omitted fields are left unchanged."""
        body = {
            "name": name,
            "pl_value": pl_value,
            "is_evergreen": is_evergreen,
            "campaign_schedule": campaign_schedule,
            "sequences": sequences,
            "email_gap": email_gap,
            "random_wait_max": random_wait_max,
            "text_only": text_only,
            "first_email_text_only": first_email_text_only,
            "email_list": email_list,
            "daily_limit": daily_limit,
            "stop_on_reply": stop_on_reply,
            "email_tag_list": email_tag_list,
            "link_tracking": link_tracking,
            "open_tracking": open_tracking,
            "stop_on_auto_reply": stop_on_auto_reply,
            "daily_max_leads": daily_max_leads,
            "prioritize_new_leads": prioritize_new_leads,
            "auto_variant_select": auto_variant_select,
            "match_lead_esp": match_lead_esp,
            "stop_for_company": stop_for_company,
            "insert_unsubscribe_header": insert_unsubscribe_header,
            "allow_risky_contacts": allow_risky_contacts,
            "disable_bounce_protect": disable_bounce_protect,
            "limit_emails_per_company_override": limit_emails_per_company_override,
            "cc_list": cc_list,
            "bcc_list": bcc_list,
            "owned_by": owned_by,
            "provider_routing_rules": provider_routing_rules,
        }
        return Campaign.model_validate(await self._patch(f"/api/v2/campaigns/{id}", json=body))

    async def delete(self, id: str) -> Campaign:
        """Delete a campaign."""
        return Campaign.model_validate(await self._delete(f"/api/v2/campaigns/{id}"))

    async def activate(self, id: str) -> Campaign:
        """Activate (start), or resume, a campaign."""
        return Campaign.model_validate(await self._post(f"/api/v2/campaigns/{id}/activate"))

    async def pause(self, id: str) -> Campaign:
        """Stop (or pause) a campaign."""
        return Campaign.model_validate(await self._post(f"/api/v2/campaigns/{id}/pause"))

    async def duplicate(self, id: str, *, name: str | NotGiven = NOT_GIVEN) -> Campaign:
        """Duplicate a campaign."""
        return Campaign.model_validate(
            await self._post(f"/api/v2/campaigns/{id}/duplicate", json={"name": name})
        )

    async def export(self, id: str) -> Campaign:
        """Export a campaign to JSON format."""
        return Campaign.model_validate(await self._post(f"/api/v2/campaigns/{id}/export"))

    async def create_from_export(self, id: str) -> Campaign:
        """Create a campaign from a previously shared/exported one."""
        return Campaign.model_validate(await self._post(f"/api/v2/campaigns/{id}/from-export"))

    async def share(self, id: str) -> None:
        """Share a campaign."""
        await self._post(f"/api/v2/campaigns/{id}/share")

    async def add_variables(
        self, id: str, *, variables: _list[str] | NotGiven = NOT_GIVEN
    ) -> Campaign:
        """Add campaign variables."""
        return Campaign.model_validate(
            await self._post(f"/api/v2/campaigns/{id}/variables", json={"variables": variables})
        )

    async def sending_status(
        self, id: str, *, with_ai_summary: bool | NotGiven = NOT_GIVEN
    ) -> JSONObject:
        """Get campaign sending status (diagnostics + summary)."""
        return await self._get(
            f"/api/v2/campaigns/{id}/sending-status", params={"with_ai_summary": with_ai_summary}
        )

    async def search_by_contact(
        self,
        *,
        search: str | NotGiven = NOT_GIVEN,
        sort_column: str | NotGiven = NOT_GIVEN,
        sort_order: str | NotGiven = NOT_GIVEN,
    ) -> JSONObject:
        """Search campaigns by lead email."""
        return await self._get(
            "/api/v2/campaigns/search-by-contact",
            params={"search": search, "sort_column": sort_column, "sort_order": sort_order},
        )

    async def count_launched(self) -> JSONObject:
        """Get the count of launched campaigns."""
        return await self._get("/api/v2/campaigns/count-launched")

    async def analytics(
        self,
        *,
        id: str | NotGiven = NOT_GIVEN,
        ids: _list[str] | NotGiven = NOT_GIVEN,
        start_date: str | NotGiven = NOT_GIVEN,
        end_date: str | NotGiven = NOT_GIVEN,
        exclude_total_leads_count: bool | NotGiven = NOT_GIVEN,
    ) -> _list[JSONObject]:
        """Get analytics for one or more campaigns."""
        return await self._get(
            "/api/v2/campaigns/analytics",
            params={
                "id": id,
                "ids": ids,
                "start_date": start_date,
                "end_date": end_date,
                "exclude_total_leads_count": exclude_total_leads_count,
            },
        )

    async def analytics_overview(
        self,
        *,
        id: str | NotGiven = NOT_GIVEN,
        ids: _list[str] | NotGiven = NOT_GIVEN,
        start_date: str | NotGiven = NOT_GIVEN,
        end_date: str | NotGiven = NOT_GIVEN,
        campaign_status: float | NotGiven = NOT_GIVEN,
        expand_crm_events: bool | NotGiven = NOT_GIVEN,
    ) -> JSONObject:
        """Get an aggregate analytics overview across campaigns."""
        return await self._get(
            "/api/v2/campaigns/analytics/overview",
            params={
                "id": id,
                "ids": ids,
                "start_date": start_date,
                "end_date": end_date,
                "campaign_status": campaign_status,
                "expand_crm_events": expand_crm_events,
            },
        )

    async def analytics_daily(
        self,
        *,
        campaign_id: str | NotGiven = NOT_GIVEN,
        start_date: str | NotGiven = NOT_GIVEN,
        end_date: str | NotGiven = NOT_GIVEN,
        campaign_status: float | NotGiven = NOT_GIVEN,
    ) -> _list[JSONObject]:
        """Get daily campaign analytics."""
        return await self._get(
            "/api/v2/campaigns/analytics/daily",
            params={
                "campaign_id": campaign_id,
                "start_date": start_date,
                "end_date": end_date,
                "campaign_status": campaign_status,
            },
        )

    async def analytics_steps(
        self,
        *,
        campaign_id: str | NotGiven = NOT_GIVEN,
        start_date: str | NotGiven = NOT_GIVEN,
        end_date: str | NotGiven = NOT_GIVEN,
        include_opportunities_count: bool | NotGiven = NOT_GIVEN,
    ) -> _list[JSONObject]:
        """Get per-step campaign analytics."""
        return await self._get(
            "/api/v2/campaigns/analytics/steps",
            params={
                "campaign_id": campaign_id,
                "start_date": start_date,
                "end_date": end_date,
                "include_opportunities_count": include_opportunities_count,
            },
        )

    async def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        search: str | NotGiven = NOT_GIVEN,
        tag_ids: str | NotGiven = NOT_GIVEN,
        ai_sales_agent_id: str | NotGiven = NOT_GIVEN,
        status: _CampaignStatus | NotGiven = NOT_GIVEN,
    ) -> AsyncCursorPage[Campaign]:
        """List campaigns. Auto-paginates: `async for c in await client.campaigns.list(): ...`."""

        async def fetch_page(cursor: str | None) -> Any:
            return await self._get(
                "/api/v2/campaigns",
                params={
                    "limit": limit,
                    "starting_after": cursor if cursor is not None else starting_after,
                    "search": search,
                    "tag_ids": tag_ids,
                    "ai_sales_agent_id": ai_sales_agent_id,
                    "status": status,
                },
            )

        return await self._paginate(Campaign, fetch_page)
