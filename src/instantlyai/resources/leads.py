"""Lead resource: ``client.leads``."""

from __future__ import annotations

from typing import Any, Literal

from .._pagination import AsyncCursorPage, SyncCursorPage
from .._transport import NOT_GIVEN, NotGiven
from .._types import JSONObject
from ..models import BackgroundJob, Lead, Payload
from ._base import AsyncAPIResource, SyncAPIResource

__all__ = ["AsyncLeads", "Leads"]

# Both resource classes define a `list()` method, which shadows the builtin
# `list` for annotation resolution anywhere else in this module's class
# bodies -- alias it once and use `_list[...]` instead of bare `list[...]`.
_list = list

_EsgCode = Literal["0", "1", "2", "3", "4", "all", "none"]
_LeadAssignFilter = Literal[
    "FILTER_VAL_CONTACTED",
    "FILTER_VAL_NOT_CONTACTED",
    "FILTER_VAL_COMPLETED",
    "FILTER_VAL_UNSUBSCRIBED",
    "FILTER_VAL_ACTIVE",
    "FILTER_LEAD_INTERESTED",
    "FILTER_LEAD_NOT_INTERESTED",
    "FILTER_LEAD_MEETING_BOOKED",
    "FILTER_LEAD_MEETING_COMPLETED",
    "FILTER_LEAD_CLOSED",
    "FILTER_LEAD_OUT_OF_OFFICE",
    "FILTER_LEAD_WRONG_PERSON",
    "FILTER_LEAD_LOST",
    "FILTER_LEAD_NO_SHOW",
    "FILTER_LEAD_CUSTOM_LABEL_POSITIVE",
    "FILTER_LEAD_CUSTOM_LABEL_NEGATIVE",
    "FILTER_VAL_BOUNCED",
    "FILTER_VAL_SKIPPED",
    "FILTER_VAL_RISKY",
    "FILTER_VAL_INVALID",
    "FILTER_VAL_VALID",
    "FILTER_VAL_IN_SUBSEQUENCE",
    "FILTER_VAL_OPENED_NO_REPLY",
    "FILTER_VAL_COMPLETED_NO_REPLY",
    "FILTER_VAL_NO_OPENS",
    "FILTER_VAL_REPLIED",
    "FILTER_VAL_LINK_CLICKED",
]


class Leads(SyncAPIResource):
    def create(
        self,
        *,
        campaign: str | NotGiven = NOT_GIVEN,
        email: str | NotGiven = NOT_GIVEN,
        personalization: str | NotGiven = NOT_GIVEN,
        website: str | NotGiven = NOT_GIVEN,
        last_name: str | NotGiven = NOT_GIVEN,
        first_name: str | NotGiven = NOT_GIVEN,
        company_name: str | NotGiven = NOT_GIVEN,
        job_title: str | NotGiven = NOT_GIVEN,
        phone: str | NotGiven = NOT_GIVEN,
        lt_interest_status: float | NotGiven = NOT_GIVEN,
        pl_value_lead: str | NotGiven = NOT_GIVEN,
        list_id: str | NotGiven = NOT_GIVEN,
        assigned_to: str | NotGiven = NOT_GIVEN,
        skip_if_in_workspace: bool | NotGiven = NOT_GIVEN,
        skip_if_in_campaign: bool | NotGiven = NOT_GIVEN,
        skip_if_in_list: bool | NotGiven = NOT_GIVEN,
        blocklist_id: str | NotGiven = NOT_GIVEN,
        verify_leads_for_lead_finder: bool | NotGiven = NOT_GIVEN,
        verify_leads_on_import: bool | NotGiven = NOT_GIVEN,
        custom_variables: Payload | NotGiven = NOT_GIVEN,
    ) -> Lead:
        """Create lead."""
        body = {
            "campaign": campaign,
            "email": email,
            "personalization": personalization,
            "website": website,
            "last_name": last_name,
            "first_name": first_name,
            "company_name": company_name,
            "job_title": job_title,
            "phone": phone,
            "lt_interest_status": lt_interest_status,
            "pl_value_lead": pl_value_lead,
            "list_id": list_id,
            "assigned_to": assigned_to,
            "skip_if_in_workspace": skip_if_in_workspace,
            "skip_if_in_campaign": skip_if_in_campaign,
            "skip_if_in_list": skip_if_in_list,
            "blocklist_id": blocklist_id,
            "verify_leads_for_lead_finder": verify_leads_for_lead_finder,
            "verify_leads_on_import": verify_leads_on_import,
            "custom_variables": custom_variables,
        }
        return Lead.model_validate(self._post("/api/v2/leads", json=body))

    def retrieve(self, id: str) -> Lead:
        """Get lead."""
        return Lead.model_validate(self._get(f"/api/v2/leads/{id}"))

    def update(
        self,
        id: str,
        *,
        personalization: str | NotGiven = NOT_GIVEN,
        website: str | NotGiven = NOT_GIVEN,
        last_name: str | NotGiven = NOT_GIVEN,
        first_name: str | NotGiven = NOT_GIVEN,
        company_name: str | NotGiven = NOT_GIVEN,
        job_title: str | NotGiven = NOT_GIVEN,
        phone: str | NotGiven = NOT_GIVEN,
        lt_interest_status: float | NotGiven = NOT_GIVEN,
        pl_value_lead: str | NotGiven = NOT_GIVEN,
        assigned_to: str | NotGiven = NOT_GIVEN,
        custom_variables: Payload | NotGiven = NOT_GIVEN,
    ) -> Lead:
        """Patch lead. Omitted fields are left unchanged."""
        body = {
            "personalization": personalization,
            "website": website,
            "last_name": last_name,
            "first_name": first_name,
            "company_name": company_name,
            "job_title": job_title,
            "phone": phone,
            "lt_interest_status": lt_interest_status,
            "pl_value_lead": pl_value_lead,
            "assigned_to": assigned_to,
            "custom_variables": custom_variables,
        }
        return Lead.model_validate(self._patch(f"/api/v2/leads/{id}", json=body))

    def delete(self, id: str) -> Lead:
        """Delete lead."""
        return Lead.model_validate(self._delete(f"/api/v2/leads/{id}"))

    def bulk_delete(
        self,
        *,
        campaign_id: str | NotGiven = NOT_GIVEN,
        list_id: str | NotGiven = NOT_GIVEN,
        status: float | NotGiven = NOT_GIVEN,
        ids: _list[str] | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
    ) -> JSONObject:
        """Delete leads in bulk."""
        return self._delete(
            "/api/v2/leads",
            json={
                "campaign_id": campaign_id,
                "list_id": list_id,
                "status": status,
                "ids": ids,
                "limit": limit,
            },
        )

    def bulk_add(
        self,
        *,
        leads: _list[Payload],
        campaign_id: str | NotGiven = NOT_GIVEN,
        list_id: str | NotGiven = NOT_GIVEN,
        blocklist_id: str | NotGiven = NOT_GIVEN,
        assigned_to: str | NotGiven = NOT_GIVEN,
        verify_leads_on_import: bool | NotGiven = NOT_GIVEN,
        skip_if_in_workspace: bool | NotGiven = NOT_GIVEN,
        skip_if_in_campaign: bool | NotGiven = NOT_GIVEN,
        skip_if_in_list: bool | NotGiven = NOT_GIVEN,
    ) -> JSONObject:
        """Add leads in bulk to a campaign or list."""
        return self._post(
            "/api/v2/leads/add",
            json={
                "campaign_id": campaign_id,
                "list_id": list_id,
                "leads": leads,
                "blocklist_id": blocklist_id,
                "assigned_to": assigned_to,
                "verify_leads_on_import": verify_leads_on_import,
                "skip_if_in_workspace": skip_if_in_workspace,
                "skip_if_in_campaign": skip_if_in_campaign,
                "skip_if_in_list": skip_if_in_list,
            },
        )

    def bulk_assign(
        self,
        *,
        organization_user_ids: _list[str],
        search: str | NotGiven = NOT_GIVEN,
        filter: _LeadAssignFilter | NotGiven = NOT_GIVEN,
        campaign: str | NotGiven = NOT_GIVEN,
        list_id: str | NotGiven = NOT_GIVEN,
        in_campaign: bool | NotGiven = NOT_GIVEN,
        in_list: bool | NotGiven = NOT_GIVEN,
        smart_view_id: str | NotGiven = NOT_GIVEN,
        ids: _list[str] | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        queries: _list[JSONObject] | NotGiven = NOT_GIVEN,
        assigned_to: str | NotGiven = NOT_GIVEN,
        has_clause: bool | NotGiven = NOT_GIVEN,
    ) -> JSONObject:
        """Bulk assign leads to organization users."""
        return self._post(
            "/api/v2/leads/bulk-assign",
            json={
                "search": search,
                "filter": filter,
                "campaign": campaign,
                "list_id": list_id,
                "in_campaign": in_campaign,
                "in_list": in_list,
                "organization_user_ids": organization_user_ids,
                "smart_view_id": smart_view_id,
                "ids": ids,
                "limit": limit,
                "queries": queries,
                "assigned_to": assigned_to,
                "has_clause": has_clause,
            },
        )

    def merge(self, *, lead_id: str, destination_lead_id: str) -> Lead:
        """Merge two leads."""
        return Lead.model_validate(
            self._post(
                "/api/v2/leads/merge",
                json={"lead_id": lead_id, "destination_lead_id": destination_lead_id},
            )
        )

    def move(
        self,
        *,
        search: str | NotGiven = NOT_GIVEN,
        filter: str | NotGiven = NOT_GIVEN,
        campaign: str | NotGiven = NOT_GIVEN,
        list_id: str | NotGiven = NOT_GIVEN,
        in_campaign: bool | NotGiven = NOT_GIVEN,
        in_list: bool | NotGiven = NOT_GIVEN,
        ids: _list[str] | NotGiven = NOT_GIVEN,
        queries: _list[JSONObject] | NotGiven = NOT_GIVEN,
        excluded_ids: _list[str] | NotGiven = NOT_GIVEN,
        contacts: _list[str] | NotGiven = NOT_GIVEN,
        to_campaign_id: str | NotGiven = NOT_GIVEN,
        to_list_id: str | NotGiven = NOT_GIVEN,
        ignore_resource_filter_clauses: bool | NotGiven = NOT_GIVEN,
        check_duplicates_in_campaigns: bool | NotGiven = NOT_GIVEN,
        skip_leads_in_verification: bool | NotGiven = NOT_GIVEN,
        limit: float | NotGiven = NOT_GIVEN,
        assigned_to: str | NotGiven = NOT_GIVEN,
        esp_code: float | NotGiven = NOT_GIVEN,
        esg_code: _EsgCode | NotGiven = NOT_GIVEN,
        copy_leads: bool | NotGiven = NOT_GIVEN,
        check_duplicates: bool | NotGiven = NOT_GIVEN,
        reset_interest_status: bool | NotGiven = NOT_GIVEN,
    ) -> BackgroundJob:
        """Move leads to a campaign or list."""
        body = {
            "search": search,
            "filter": filter,
            "campaign": campaign,
            "list_id": list_id,
            "in_campaign": in_campaign,
            "in_list": in_list,
            "ids": ids,
            "queries": queries,
            "excluded_ids": excluded_ids,
            "contacts": contacts,
            "to_campaign_id": to_campaign_id,
            "to_list_id": to_list_id,
            "ignore_resource_filter_clauses": ignore_resource_filter_clauses,
            "check_duplicates_in_campaigns": check_duplicates_in_campaigns,
            "skip_leads_in_verification": skip_leads_in_verification,
            "limit": limit,
            "assigned_to": assigned_to,
            "esp_code": esp_code,
            "esg_code": esg_code,
            "copy_leads": copy_leads,
            "check_duplicates": check_duplicates,
            "reset_interest_status": reset_interest_status,
        }
        return BackgroundJob.model_validate(self._post("/api/v2/leads/move", json=body))

    def move_to_subsequence(self, *, subsequence_id: str, id: str) -> Lead:
        """Move a lead to a subsequence."""
        return Lead.model_validate(
            self._post(
                "/api/v2/leads/subsequence/move",
                json={"subsequence_id": subsequence_id, "id": id},
            )
        )

    def remove_from_subsequence(self, *, id: str) -> Lead:
        """Remove a lead from a subsequence."""
        return Lead.model_validate(self._post("/api/v2/leads/subsequence/remove", json={"id": id}))

    def update_interest_status(
        self,
        *,
        lead_email: str,
        interest_value: float,
        campaign_id: str | NotGiven = NOT_GIVEN,
        ai_interest_value: float | NotGiven = NOT_GIVEN,
        disable_auto_interest: bool | NotGiven = NOT_GIVEN,
        list_id: str | NotGiven = NOT_GIVEN,
    ) -> JSONObject:
        """Update the interest status of a lead."""
        return self._post(
            "/api/v2/leads/update-interest-status",
            json={
                "lead_email": lead_email,
                "interest_value": interest_value,
                "campaign_id": campaign_id,
                "ai_interest_value": ai_interest_value,
                "disable_auto_interest": disable_auto_interest,
                "list_id": list_id,
            },
        )

    def list(
        self,
        *,
        search: str | NotGiven = NOT_GIVEN,
        filter: str | NotGiven = NOT_GIVEN,
        campaign: str | NotGiven = NOT_GIVEN,
        list_id: str | NotGiven = NOT_GIVEN,
        in_campaign: bool | NotGiven = NOT_GIVEN,
        in_list: bool | NotGiven = NOT_GIVEN,
        ids: _list[str] | NotGiven = NOT_GIVEN,
        queries: _list[JSONObject] | NotGiven = NOT_GIVEN,
        excluded_ids: _list[str] | NotGiven = NOT_GIVEN,
        contacts: _list[str] | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        organization_user_ids: _list[str] | NotGiven = NOT_GIVEN,
        smart_view_id: str | NotGiven = NOT_GIVEN,
        is_website_visitor: bool | NotGiven = NOT_GIVEN,
        distinct_contacts: bool | NotGiven = NOT_GIVEN,
        enrichment_status: float | NotGiven = NOT_GIVEN,
        esg_code: _EsgCode | NotGiven = NOT_GIVEN,
    ) -> SyncCursorPage[Lead]:
        """List leads. Auto-paginates: `for l in client.leads.list(): ...`."""

        def fetch_page(cursor: str | None) -> Any:
            return self._post(
                "/api/v2/leads/list",
                json={
                    "search": search,
                    "filter": filter,
                    "campaign": campaign,
                    "list_id": list_id,
                    "in_campaign": in_campaign,
                    "in_list": in_list,
                    "ids": ids,
                    "queries": queries,
                    "excluded_ids": excluded_ids,
                    "contacts": contacts,
                    "limit": limit,
                    "starting_after": cursor if cursor is not None else starting_after,
                    "organization_user_ids": organization_user_ids,
                    "smart_view_id": smart_view_id,
                    "is_website_visitor": is_website_visitor,
                    "distinct_contacts": distinct_contacts,
                    "enrichment_status": enrichment_status,
                    "esg_code": esg_code,
                },
            )

        return self._paginate(Lead, fetch_page)


class AsyncLeads(AsyncAPIResource):
    async def create(
        self,
        *,
        campaign: str | NotGiven = NOT_GIVEN,
        email: str | NotGiven = NOT_GIVEN,
        personalization: str | NotGiven = NOT_GIVEN,
        website: str | NotGiven = NOT_GIVEN,
        last_name: str | NotGiven = NOT_GIVEN,
        first_name: str | NotGiven = NOT_GIVEN,
        company_name: str | NotGiven = NOT_GIVEN,
        job_title: str | NotGiven = NOT_GIVEN,
        phone: str | NotGiven = NOT_GIVEN,
        lt_interest_status: float | NotGiven = NOT_GIVEN,
        pl_value_lead: str | NotGiven = NOT_GIVEN,
        list_id: str | NotGiven = NOT_GIVEN,
        assigned_to: str | NotGiven = NOT_GIVEN,
        skip_if_in_workspace: bool | NotGiven = NOT_GIVEN,
        skip_if_in_campaign: bool | NotGiven = NOT_GIVEN,
        skip_if_in_list: bool | NotGiven = NOT_GIVEN,
        blocklist_id: str | NotGiven = NOT_GIVEN,
        verify_leads_for_lead_finder: bool | NotGiven = NOT_GIVEN,
        verify_leads_on_import: bool | NotGiven = NOT_GIVEN,
        custom_variables: Payload | NotGiven = NOT_GIVEN,
    ) -> Lead:
        """Create lead."""
        body = {
            "campaign": campaign,
            "email": email,
            "personalization": personalization,
            "website": website,
            "last_name": last_name,
            "first_name": first_name,
            "company_name": company_name,
            "job_title": job_title,
            "phone": phone,
            "lt_interest_status": lt_interest_status,
            "pl_value_lead": pl_value_lead,
            "list_id": list_id,
            "assigned_to": assigned_to,
            "skip_if_in_workspace": skip_if_in_workspace,
            "skip_if_in_campaign": skip_if_in_campaign,
            "skip_if_in_list": skip_if_in_list,
            "blocklist_id": blocklist_id,
            "verify_leads_for_lead_finder": verify_leads_for_lead_finder,
            "verify_leads_on_import": verify_leads_on_import,
            "custom_variables": custom_variables,
        }
        return Lead.model_validate(await self._post("/api/v2/leads", json=body))

    async def retrieve(self, id: str) -> Lead:
        """Get lead."""
        return Lead.model_validate(await self._get(f"/api/v2/leads/{id}"))

    async def update(
        self,
        id: str,
        *,
        personalization: str | NotGiven = NOT_GIVEN,
        website: str | NotGiven = NOT_GIVEN,
        last_name: str | NotGiven = NOT_GIVEN,
        first_name: str | NotGiven = NOT_GIVEN,
        company_name: str | NotGiven = NOT_GIVEN,
        job_title: str | NotGiven = NOT_GIVEN,
        phone: str | NotGiven = NOT_GIVEN,
        lt_interest_status: float | NotGiven = NOT_GIVEN,
        pl_value_lead: str | NotGiven = NOT_GIVEN,
        assigned_to: str | NotGiven = NOT_GIVEN,
        custom_variables: Payload | NotGiven = NOT_GIVEN,
    ) -> Lead:
        """Patch lead. Omitted fields are left unchanged."""
        body = {
            "personalization": personalization,
            "website": website,
            "last_name": last_name,
            "first_name": first_name,
            "company_name": company_name,
            "job_title": job_title,
            "phone": phone,
            "lt_interest_status": lt_interest_status,
            "pl_value_lead": pl_value_lead,
            "assigned_to": assigned_to,
            "custom_variables": custom_variables,
        }
        return Lead.model_validate(await self._patch(f"/api/v2/leads/{id}", json=body))

    async def delete(self, id: str) -> Lead:
        """Delete lead."""
        return Lead.model_validate(await self._delete(f"/api/v2/leads/{id}"))

    async def bulk_delete(
        self,
        *,
        campaign_id: str | NotGiven = NOT_GIVEN,
        list_id: str | NotGiven = NOT_GIVEN,
        status: float | NotGiven = NOT_GIVEN,
        ids: _list[str] | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
    ) -> JSONObject:
        """Delete leads in bulk."""
        return await self._delete(
            "/api/v2/leads",
            json={
                "campaign_id": campaign_id,
                "list_id": list_id,
                "status": status,
                "ids": ids,
                "limit": limit,
            },
        )

    async def bulk_add(
        self,
        *,
        leads: _list[Payload],
        campaign_id: str | NotGiven = NOT_GIVEN,
        list_id: str | NotGiven = NOT_GIVEN,
        blocklist_id: str | NotGiven = NOT_GIVEN,
        assigned_to: str | NotGiven = NOT_GIVEN,
        verify_leads_on_import: bool | NotGiven = NOT_GIVEN,
        skip_if_in_workspace: bool | NotGiven = NOT_GIVEN,
        skip_if_in_campaign: bool | NotGiven = NOT_GIVEN,
        skip_if_in_list: bool | NotGiven = NOT_GIVEN,
    ) -> JSONObject:
        """Add leads in bulk to a campaign or list."""
        return await self._post(
            "/api/v2/leads/add",
            json={
                "campaign_id": campaign_id,
                "list_id": list_id,
                "leads": leads,
                "blocklist_id": blocklist_id,
                "assigned_to": assigned_to,
                "verify_leads_on_import": verify_leads_on_import,
                "skip_if_in_workspace": skip_if_in_workspace,
                "skip_if_in_campaign": skip_if_in_campaign,
                "skip_if_in_list": skip_if_in_list,
            },
        )

    async def bulk_assign(
        self,
        *,
        organization_user_ids: _list[str],
        search: str | NotGiven = NOT_GIVEN,
        filter: _LeadAssignFilter | NotGiven = NOT_GIVEN,
        campaign: str | NotGiven = NOT_GIVEN,
        list_id: str | NotGiven = NOT_GIVEN,
        in_campaign: bool | NotGiven = NOT_GIVEN,
        in_list: bool | NotGiven = NOT_GIVEN,
        smart_view_id: str | NotGiven = NOT_GIVEN,
        ids: _list[str] | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        queries: _list[JSONObject] | NotGiven = NOT_GIVEN,
        assigned_to: str | NotGiven = NOT_GIVEN,
        has_clause: bool | NotGiven = NOT_GIVEN,
    ) -> JSONObject:
        """Bulk assign leads to organization users."""
        return await self._post(
            "/api/v2/leads/bulk-assign",
            json={
                "search": search,
                "filter": filter,
                "campaign": campaign,
                "list_id": list_id,
                "in_campaign": in_campaign,
                "in_list": in_list,
                "organization_user_ids": organization_user_ids,
                "smart_view_id": smart_view_id,
                "ids": ids,
                "limit": limit,
                "queries": queries,
                "assigned_to": assigned_to,
                "has_clause": has_clause,
            },
        )

    async def merge(self, *, lead_id: str, destination_lead_id: str) -> Lead:
        """Merge two leads."""
        return Lead.model_validate(
            await self._post(
                "/api/v2/leads/merge",
                json={"lead_id": lead_id, "destination_lead_id": destination_lead_id},
            )
        )

    async def move(
        self,
        *,
        search: str | NotGiven = NOT_GIVEN,
        filter: str | NotGiven = NOT_GIVEN,
        campaign: str | NotGiven = NOT_GIVEN,
        list_id: str | NotGiven = NOT_GIVEN,
        in_campaign: bool | NotGiven = NOT_GIVEN,
        in_list: bool | NotGiven = NOT_GIVEN,
        ids: _list[str] | NotGiven = NOT_GIVEN,
        queries: _list[JSONObject] | NotGiven = NOT_GIVEN,
        excluded_ids: _list[str] | NotGiven = NOT_GIVEN,
        contacts: _list[str] | NotGiven = NOT_GIVEN,
        to_campaign_id: str | NotGiven = NOT_GIVEN,
        to_list_id: str | NotGiven = NOT_GIVEN,
        ignore_resource_filter_clauses: bool | NotGiven = NOT_GIVEN,
        check_duplicates_in_campaigns: bool | NotGiven = NOT_GIVEN,
        skip_leads_in_verification: bool | NotGiven = NOT_GIVEN,
        limit: float | NotGiven = NOT_GIVEN,
        assigned_to: str | NotGiven = NOT_GIVEN,
        esp_code: float | NotGiven = NOT_GIVEN,
        esg_code: _EsgCode | NotGiven = NOT_GIVEN,
        copy_leads: bool | NotGiven = NOT_GIVEN,
        check_duplicates: bool | NotGiven = NOT_GIVEN,
        reset_interest_status: bool | NotGiven = NOT_GIVEN,
    ) -> BackgroundJob:
        """Move leads to a campaign or list."""
        body = {
            "search": search,
            "filter": filter,
            "campaign": campaign,
            "list_id": list_id,
            "in_campaign": in_campaign,
            "in_list": in_list,
            "ids": ids,
            "queries": queries,
            "excluded_ids": excluded_ids,
            "contacts": contacts,
            "to_campaign_id": to_campaign_id,
            "to_list_id": to_list_id,
            "ignore_resource_filter_clauses": ignore_resource_filter_clauses,
            "check_duplicates_in_campaigns": check_duplicates_in_campaigns,
            "skip_leads_in_verification": skip_leads_in_verification,
            "limit": limit,
            "assigned_to": assigned_to,
            "esp_code": esp_code,
            "esg_code": esg_code,
            "copy_leads": copy_leads,
            "check_duplicates": check_duplicates,
            "reset_interest_status": reset_interest_status,
        }
        return BackgroundJob.model_validate(await self._post("/api/v2/leads/move", json=body))

    async def move_to_subsequence(self, *, subsequence_id: str, id: str) -> Lead:
        """Move a lead to a subsequence."""
        return Lead.model_validate(
            await self._post(
                "/api/v2/leads/subsequence/move",
                json={"subsequence_id": subsequence_id, "id": id},
            )
        )

    async def remove_from_subsequence(self, *, id: str) -> Lead:
        """Remove a lead from a subsequence."""
        return Lead.model_validate(
            await self._post("/api/v2/leads/subsequence/remove", json={"id": id})
        )

    async def update_interest_status(
        self,
        *,
        lead_email: str,
        interest_value: float,
        campaign_id: str | NotGiven = NOT_GIVEN,
        ai_interest_value: float | NotGiven = NOT_GIVEN,
        disable_auto_interest: bool | NotGiven = NOT_GIVEN,
        list_id: str | NotGiven = NOT_GIVEN,
    ) -> JSONObject:
        """Update the interest status of a lead."""
        return await self._post(
            "/api/v2/leads/update-interest-status",
            json={
                "lead_email": lead_email,
                "interest_value": interest_value,
                "campaign_id": campaign_id,
                "ai_interest_value": ai_interest_value,
                "disable_auto_interest": disable_auto_interest,
                "list_id": list_id,
            },
        )

    async def list(
        self,
        *,
        search: str | NotGiven = NOT_GIVEN,
        filter: str | NotGiven = NOT_GIVEN,
        campaign: str | NotGiven = NOT_GIVEN,
        list_id: str | NotGiven = NOT_GIVEN,
        in_campaign: bool | NotGiven = NOT_GIVEN,
        in_list: bool | NotGiven = NOT_GIVEN,
        ids: _list[str] | NotGiven = NOT_GIVEN,
        queries: _list[JSONObject] | NotGiven = NOT_GIVEN,
        excluded_ids: _list[str] | NotGiven = NOT_GIVEN,
        contacts: _list[str] | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        organization_user_ids: _list[str] | NotGiven = NOT_GIVEN,
        smart_view_id: str | NotGiven = NOT_GIVEN,
        is_website_visitor: bool | NotGiven = NOT_GIVEN,
        distinct_contacts: bool | NotGiven = NOT_GIVEN,
        enrichment_status: float | NotGiven = NOT_GIVEN,
        esg_code: _EsgCode | NotGiven = NOT_GIVEN,
    ) -> AsyncCursorPage[Lead]:
        """List leads. Auto-paginates: `async for l in await client.leads.list(): ...`."""

        async def fetch_page(cursor: str | None) -> Any:
            return await self._post(
                "/api/v2/leads/list",
                json={
                    "search": search,
                    "filter": filter,
                    "campaign": campaign,
                    "list_id": list_id,
                    "in_campaign": in_campaign,
                    "in_list": in_list,
                    "ids": ids,
                    "queries": queries,
                    "excluded_ids": excluded_ids,
                    "contacts": contacts,
                    "limit": limit,
                    "starting_after": cursor if cursor is not None else starting_after,
                    "organization_user_ids": organization_user_ids,
                    "smart_view_id": smart_view_id,
                    "is_website_visitor": is_website_visitor,
                    "distinct_contacts": distinct_contacts,
                    "enrichment_status": enrichment_status,
                    "esg_code": esg_code,
                },
            )

        return await self._paginate(Lead, fetch_page)
