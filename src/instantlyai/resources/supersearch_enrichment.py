"""SuperSearch enrichment resource: ``client.supersearch_enrichment``."""

from __future__ import annotations

from typing import Literal

from .._transport import NOT_GIVEN, NotGiven
from .._types import JSONObject
from ..models import SuperSearchEnrichment as SuperSearchEnrichmentModel
from ._base import AsyncAPIResource, SyncAPIResource

__all__ = ["AsyncSuperSearchEnrichment", "SuperSearchEnrichment"]

_EnrichmentType = Literal[
    "work_email_enrichment",
    "fully_enriched_profile",
    "email_verification",
    "joblisting",
    "technologies",
    "news",
    "funding",
    "engagement_score",
    "ai_enrichment",
    "custom_flow",
]
_AIModelVersion = Literal[
    "3.5",
    "4.0",
    "gpt-4o",
    "o3",
    "gpt-4.1",
    "gpt-4.1-mini",
    "gpt-5-mini",
    "gpt-5-nano",
    "gpt-5",
    "gpt-5.4",
    "claude-4.5-sonnet",
    "claude-4.6-sonnet",
    "r1",
    "grok-4.3",
    "gemini-3.0-flash",
    "gemini-3.5-flash",
    "sonar",
    "sonar-pro",
    "instantly-ai-lightspeed-agent-for-web-research",
    "instantly-ai-lightspeed-agent-for-email-generation",
]


class SuperSearchEnrichment(SyncAPIResource):
    def create(
        self,
        *,
        resource_id: str,
        type: _EnrichmentType | NotGiven = NOT_GIVEN,
        limit: float | NotGiven = NOT_GIVEN,
        filters: list[JSONObject] | NotGiven = NOT_GIVEN,
        custom_flow: list[str] | NotGiven = NOT_GIVEN,
        integration_actions: JSONObject | NotGiven = NOT_GIVEN,
    ) -> JSONObject:
        """Create an enrichment. (``createSuperSearchEnrichment``)"""
        body = {
            "resource_id": resource_id,
            "type": type,
            "limit": limit,
            "filters": filters,
            "custom_flow": custom_flow,
            "integration_actions": integration_actions,
        }
        return self._post("/api/v2/supersearch-enrichment/", json=body)

    def retrieve(self, resource_id: str) -> JSONObject:
        """Get the enrichment attached to a resource (list or campaign). (``getEnrichmentForResource``)"""
        return self._get(f"/api/v2/supersearch-enrichment/{resource_id}")

    def update_settings(
        self,
        resource_id: str,
        *,
        auto_update: bool | NotGiven = NOT_GIVEN,
        skip_rows_without_email: bool | NotGiven = NOT_GIVEN,
        is_evergreen: bool | NotGiven = NOT_GIVEN,
    ) -> SuperSearchEnrichmentModel:
        """Update enrichment settings for a resource. (``updateEnrichmentSettingsForResource``)"""
        body = {
            "auto_update": auto_update,
            "skip_rows_without_email": skip_rows_without_email,
            "is_evergreen": is_evergreen,
        }
        return SuperSearchEnrichmentModel.model_validate(
            self._patch(f"/api/v2/supersearch-enrichment/{resource_id}/settings", json=body)
        )

    def create_ai_enrichment(
        self,
        *,
        resource_id: str,
        output_column: str,
        resource_type: float,
        model_version: _AIModelVersion,
        input_columns: list[str] | NotGiven = NOT_GIVEN,
        use_instantly_account: bool | NotGiven = NOT_GIVEN,
        overwrite: bool | NotGiven = NOT_GIVEN,
        auto_update: bool | NotGiven = NOT_GIVEN,
        skip_leads_without_email: bool | NotGiven = NOT_GIVEN,
        limit: float | NotGiven = NOT_GIVEN,
        prompt: str | NotGiven = NOT_GIVEN,
        template_id: str | NotGiven = NOT_GIVEN,
        status: float | NotGiven = NOT_GIVEN,
        filters: list[JSONObject] | NotGiven = NOT_GIVEN,
    ) -> JSONObject:
        """Create an AI enrichment job for a resource. (``createAIEnrichment``)"""
        body = {
            "resource_id": resource_id,
            "output_column": output_column,
            "resource_type": resource_type,
            "input_columns": input_columns,
            "model_version": model_version,
            "use_instantly_account": use_instantly_account,
            "overwrite": overwrite,
            "auto_update": auto_update,
            "skip_leads_without_email": skip_leads_without_email,
            "limit": limit,
            "prompt": prompt,
            "template_id": template_id,
            "status": status,
            "filters": filters,
        }
        return self._post("/api/v2/supersearch-enrichment/ai", json=body)

    def ai_enrichment_in_progress(self, resource_id: str) -> list[JSONObject]:
        """Get in-progress AI enrichment jobs for a resource. (``getAiEnrichmentForResource``)"""
        return self._get(f"/api/v2/supersearch-enrichment/ai/{resource_id}/in-progress")

    def enrich_leads_from_supersearch(
        self,
        *,
        search_filters: JSONObject,
        limit: float,
        search_name: str | NotGiven = NOT_GIVEN,
        work_email_enrichment: bool | NotGiven = NOT_GIVEN,
        fully_enriched_profile: bool | NotGiven = NOT_GIVEN,
        custom_flow: list[str] | NotGiven = NOT_GIVEN,
        signal_enrichment: list[JSONObject] | NotGiven = NOT_GIVEN,
        resource_id: str | NotGiven = NOT_GIVEN,
        auto_update: bool | NotGiven = NOT_GIVEN,
        skip_rows_without_email: bool | NotGiven = NOT_GIVEN,
        list_name: str | NotGiven = NOT_GIVEN,
        ai_enrichment: JSONObject | NotGiven = NOT_GIVEN,
    ) -> JSONObject:
        """Import and enrich leads directly from a SuperSearch query. (``enrichLeadsFromSupersearch``)"""
        body = {
            "search_filters": search_filters,
            "search_name": search_name,
            "work_email_enrichment": work_email_enrichment,
            "fully_enriched_profile": fully_enriched_profile,
            "custom_flow": custom_flow,
            "signal_enrichment": signal_enrichment,
            "resource_id": resource_id,
            "auto_update": auto_update,
            "skip_rows_without_email": skip_rows_without_email,
            "list_name": list_name,
            "limit": limit,
            "ai_enrichment": ai_enrichment,
        }
        return self._post("/api/v2/supersearch-enrichment/enrich-leads-from-supersearch", json=body)

    def run(
        self,
        *,
        resource_id: str,
        lead_ids: list[str] | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        column_name: str | NotGiven = NOT_GIVEN,
        overwrite: bool | NotGiven = NOT_GIVEN,
        starting_row: int | NotGiven = NOT_GIVEN,
        count: int | NotGiven = NOT_GIVEN,
        filters: list[JSONObject] | NotGiven = NOT_GIVEN,
    ) -> JSONObject:
        """Run the enrichment configured for a resource. (``runEnrichment``)"""
        body = {
            "resource_id": resource_id,
            "lead_ids": lead_ids,
            "limit": limit,
            "column_name": column_name,
            "overwrite": overwrite,
            "starting_row": starting_row,
            "count": count,
            "filters": filters,
        }
        return self._post("/api/v2/supersearch-enrichment/run", json=body)

    def count_leads_from_supersearch(
        self,
        *,
        search_filters: JSONObject,
        skip_owned_leads: bool | NotGiven = NOT_GIVEN,
        show_one_lead_per_company: bool | NotGiven = NOT_GIVEN,
    ) -> JSONObject:
        """Count the leads a SuperSearch query would return. (``countLeadsFromSupersearch``)"""
        body = {
            "search_filters": search_filters,
            "skip_owned_leads": skip_owned_leads,
            "show_one_lead_per_company": show_one_lead_per_company,
        }
        return self._post("/api/v2/supersearch-enrichment/count-leads-from-supersearch", json=body)

    def preview_leads_from_supersearch(
        self,
        *,
        search_filters: JSONObject,
        skip_owned_leads: bool | NotGiven = NOT_GIVEN,
        show_one_lead_per_company: bool | NotGiven = NOT_GIVEN,
    ) -> JSONObject:
        """Preview the leads a SuperSearch query would return. (``previewLeadsFromSupersearch``)"""
        body = {
            "search_filters": search_filters,
            "skip_owned_leads": skip_owned_leads,
            "show_one_lead_per_company": show_one_lead_per_company,
        }
        return self._post(
            "/api/v2/supersearch-enrichment/preview-leads-from-supersearch", json=body
        )

    def signal_keywords_facet(
        self,
        *,
        category: str,
        field: str,
        prefix: str | NotGiven = NOT_GIVEN,
        limit: float | NotGiven = NOT_GIVEN,
    ) -> JSONObject:
        """Get facet keyword suggestions for a signal category. (``signalKeywordsFacet``)"""
        body = {"category": category, "field": field, "prefix": prefix, "limit": limit}
        return self._post("/api/v2/supersearch-enrichment/signal-keywords-facet", json=body)

    def history(
        self,
        resource_id: str,
        *,
        offset: float | NotGiven = NOT_GIVEN,
        limit: float | NotGiven = NOT_GIVEN,
    ) -> list[JSONObject]:
        """Get the enrichment history for a resource. (``getEnrichmentHistory``)"""
        return self._get(
            f"/api/v2/supersearch-enrichment/history/{resource_id}",
            params={"offset": offset, "limit": limit},
        )


class AsyncSuperSearchEnrichment(AsyncAPIResource):
    async def create(
        self,
        *,
        resource_id: str,
        type: _EnrichmentType | NotGiven = NOT_GIVEN,
        limit: float | NotGiven = NOT_GIVEN,
        filters: list[JSONObject] | NotGiven = NOT_GIVEN,
        custom_flow: list[str] | NotGiven = NOT_GIVEN,
        integration_actions: JSONObject | NotGiven = NOT_GIVEN,
    ) -> JSONObject:
        """Create an enrichment. (``createSuperSearchEnrichment``)"""
        body = {
            "resource_id": resource_id,
            "type": type,
            "limit": limit,
            "filters": filters,
            "custom_flow": custom_flow,
            "integration_actions": integration_actions,
        }
        return await self._post("/api/v2/supersearch-enrichment/", json=body)

    async def retrieve(self, resource_id: str) -> JSONObject:
        """Get the enrichment attached to a resource (list or campaign). (``getEnrichmentForResource``)"""
        return await self._get(f"/api/v2/supersearch-enrichment/{resource_id}")

    async def update_settings(
        self,
        resource_id: str,
        *,
        auto_update: bool | NotGiven = NOT_GIVEN,
        skip_rows_without_email: bool | NotGiven = NOT_GIVEN,
        is_evergreen: bool | NotGiven = NOT_GIVEN,
    ) -> SuperSearchEnrichmentModel:
        """Update enrichment settings for a resource. (``updateEnrichmentSettingsForResource``)"""
        body = {
            "auto_update": auto_update,
            "skip_rows_without_email": skip_rows_without_email,
            "is_evergreen": is_evergreen,
        }
        return SuperSearchEnrichmentModel.model_validate(
            await self._patch(f"/api/v2/supersearch-enrichment/{resource_id}/settings", json=body)
        )

    async def create_ai_enrichment(
        self,
        *,
        resource_id: str,
        output_column: str,
        resource_type: float,
        model_version: _AIModelVersion,
        input_columns: list[str] | NotGiven = NOT_GIVEN,
        use_instantly_account: bool | NotGiven = NOT_GIVEN,
        overwrite: bool | NotGiven = NOT_GIVEN,
        auto_update: bool | NotGiven = NOT_GIVEN,
        skip_leads_without_email: bool | NotGiven = NOT_GIVEN,
        limit: float | NotGiven = NOT_GIVEN,
        prompt: str | NotGiven = NOT_GIVEN,
        template_id: str | NotGiven = NOT_GIVEN,
        status: float | NotGiven = NOT_GIVEN,
        filters: list[JSONObject] | NotGiven = NOT_GIVEN,
    ) -> JSONObject:
        """Create an AI enrichment job for a resource. (``createAIEnrichment``)"""
        body = {
            "resource_id": resource_id,
            "output_column": output_column,
            "resource_type": resource_type,
            "input_columns": input_columns,
            "model_version": model_version,
            "use_instantly_account": use_instantly_account,
            "overwrite": overwrite,
            "auto_update": auto_update,
            "skip_leads_without_email": skip_leads_without_email,
            "limit": limit,
            "prompt": prompt,
            "template_id": template_id,
            "status": status,
            "filters": filters,
        }
        return await self._post("/api/v2/supersearch-enrichment/ai", json=body)

    async def ai_enrichment_in_progress(self, resource_id: str) -> list[JSONObject]:
        """Get in-progress AI enrichment jobs for a resource. (``getAiEnrichmentForResource``)"""
        return await self._get(f"/api/v2/supersearch-enrichment/ai/{resource_id}/in-progress")

    async def enrich_leads_from_supersearch(
        self,
        *,
        search_filters: JSONObject,
        limit: float,
        search_name: str | NotGiven = NOT_GIVEN,
        work_email_enrichment: bool | NotGiven = NOT_GIVEN,
        fully_enriched_profile: bool | NotGiven = NOT_GIVEN,
        custom_flow: list[str] | NotGiven = NOT_GIVEN,
        signal_enrichment: list[JSONObject] | NotGiven = NOT_GIVEN,
        resource_id: str | NotGiven = NOT_GIVEN,
        auto_update: bool | NotGiven = NOT_GIVEN,
        skip_rows_without_email: bool | NotGiven = NOT_GIVEN,
        list_name: str | NotGiven = NOT_GIVEN,
        ai_enrichment: JSONObject | NotGiven = NOT_GIVEN,
    ) -> JSONObject:
        """Import and enrich leads directly from a SuperSearch query. (``enrichLeadsFromSupersearch``)"""
        body = {
            "search_filters": search_filters,
            "search_name": search_name,
            "work_email_enrichment": work_email_enrichment,
            "fully_enriched_profile": fully_enriched_profile,
            "custom_flow": custom_flow,
            "signal_enrichment": signal_enrichment,
            "resource_id": resource_id,
            "auto_update": auto_update,
            "skip_rows_without_email": skip_rows_without_email,
            "list_name": list_name,
            "limit": limit,
            "ai_enrichment": ai_enrichment,
        }
        return await self._post(
            "/api/v2/supersearch-enrichment/enrich-leads-from-supersearch", json=body
        )

    async def run(
        self,
        *,
        resource_id: str,
        lead_ids: list[str] | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        column_name: str | NotGiven = NOT_GIVEN,
        overwrite: bool | NotGiven = NOT_GIVEN,
        starting_row: int | NotGiven = NOT_GIVEN,
        count: int | NotGiven = NOT_GIVEN,
        filters: list[JSONObject] | NotGiven = NOT_GIVEN,
    ) -> JSONObject:
        """Run the enrichment configured for a resource. (``runEnrichment``)"""
        body = {
            "resource_id": resource_id,
            "lead_ids": lead_ids,
            "limit": limit,
            "column_name": column_name,
            "overwrite": overwrite,
            "starting_row": starting_row,
            "count": count,
            "filters": filters,
        }
        return await self._post("/api/v2/supersearch-enrichment/run", json=body)

    async def count_leads_from_supersearch(
        self,
        *,
        search_filters: JSONObject,
        skip_owned_leads: bool | NotGiven = NOT_GIVEN,
        show_one_lead_per_company: bool | NotGiven = NOT_GIVEN,
    ) -> JSONObject:
        """Count the leads a SuperSearch query would return. (``countLeadsFromSupersearch``)"""
        body = {
            "search_filters": search_filters,
            "skip_owned_leads": skip_owned_leads,
            "show_one_lead_per_company": show_one_lead_per_company,
        }
        return await self._post(
            "/api/v2/supersearch-enrichment/count-leads-from-supersearch", json=body
        )

    async def preview_leads_from_supersearch(
        self,
        *,
        search_filters: JSONObject,
        skip_owned_leads: bool | NotGiven = NOT_GIVEN,
        show_one_lead_per_company: bool | NotGiven = NOT_GIVEN,
    ) -> JSONObject:
        """Preview the leads a SuperSearch query would return. (``previewLeadsFromSupersearch``)"""
        body = {
            "search_filters": search_filters,
            "skip_owned_leads": skip_owned_leads,
            "show_one_lead_per_company": show_one_lead_per_company,
        }
        return await self._post(
            "/api/v2/supersearch-enrichment/preview-leads-from-supersearch", json=body
        )

    async def signal_keywords_facet(
        self,
        *,
        category: str,
        field: str,
        prefix: str | NotGiven = NOT_GIVEN,
        limit: float | NotGiven = NOT_GIVEN,
    ) -> JSONObject:
        """Get facet keyword suggestions for a signal category. (``signalKeywordsFacet``)"""
        body = {"category": category, "field": field, "prefix": prefix, "limit": limit}
        return await self._post("/api/v2/supersearch-enrichment/signal-keywords-facet", json=body)

    async def history(
        self,
        resource_id: str,
        *,
        offset: float | NotGiven = NOT_GIVEN,
        limit: float | NotGiven = NOT_GIVEN,
    ) -> list[JSONObject]:
        """Get the enrichment history for a resource. (``getEnrichmentHistory``)"""
        return await self._get(
            f"/api/v2/supersearch-enrichment/history/{resource_id}",
            params={"offset": offset, "limit": limit},
        )
