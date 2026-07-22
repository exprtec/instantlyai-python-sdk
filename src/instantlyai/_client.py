"""``Instantly`` / ``AsyncInstantly`` entrypoints.

Both classes resolve auth the same way (explicit ``api_key`` argument,
falling back to the ``INSTANTLY_API_KEY`` environment variable), build a
transport, and attach one resource namespace per API resource group. There
is no global mutable state: everything lives on the client instance, so
multiple clients (e.g. for multiple Instantly workspaces) coexist safely.
"""

from __future__ import annotations

import os
from types import TracebackType

import httpx

from . import resources
from ._transport import (
    DEFAULT_BASE_URL,
    DEFAULT_MAX_RETRIES,
    DEFAULT_TIMEOUT,
    AsyncTransport,
    SyncTransport,
)

__all__ = ["AsyncInstantly", "Instantly"]


def _resolve_api_key(api_key: str | None) -> str:
    if api_key is not None:
        return api_key
    env_key = os.environ.get("INSTANTLY_API_KEY")
    if env_key:
        return env_key
    raise ValueError(
        "No API key provided. Either pass `api_key=...` to the client, or set the "
        "`INSTANTLY_API_KEY` environment variable."
    )


class Instantly:
    """Synchronous client for the Instantly.ai V2 API.

    Example:
        >>> client = Instantly(api_key="...")
        >>> for campaign in client.campaigns.list():
        ...     print(campaign.name)
    """

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: httpx.Timeout = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        http_client: httpx.Client | None = None,
    ) -> None:
        self._transport = SyncTransport(
            api_key=_resolve_api_key(api_key),
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            http_client=http_client,
        )

        self.api_keys = resources.APIKeys(self._transport)
        self.accounts = resources.Accounts(self._transport)
        self.account_campaign_mappings = resources.AccountCampaignMappings(self._transport)
        self.audit_logs = resources.AuditLogs(self._transport)
        self.background_jobs = resources.BackgroundJobs(self._transport)
        self.block_list_entries = resources.BlockListEntries(self._transport)
        self.campaigns = resources.Campaigns(self._transport)
        self.subsequences = resources.CampaignSubsequences(self._transport)
        self.crm_actions = resources.CRMActions(self._transport)
        self.custom_tags = resources.CustomTags(self._transport)
        self.custom_tag_mappings = resources.CustomTagMappings(self._transport)
        self.dfy_email_account_orders = resources.DFYEmailAccountOrders(self._transport)
        self.emails = resources.Emails(self._transport)
        self.email_verification = resources.EmailVerification(self._transport)
        self.inbox_placement_analytics = resources.InboxPlacementAnalytics(self._transport)
        self.inbox_placement_reports = resources.InboxPlacementReports(self._transport)
        self.inbox_placement_tests = resources.InboxPlacementTests(self._transport)
        self.leads = resources.Leads(self._transport)
        self.lead_labels = resources.LeadLabels(self._transport)
        self.lead_lists = resources.LeadLists(self._transport)
        self.oauth = resources.OAuth(self._transport)
        self.supersearch_enrichment = resources.SuperSearchEnrichment(self._transport)
        self.webhooks = resources.Webhooks(self._transport)
        self.webhook_events = resources.WebhookEvents(self._transport)
        self.workspaces = resources.Workspaces(self._transport)
        self.workspace_billing = resources.WorkspaceBilling(self._transport)
        self.workspace_group_members = resources.WorkspaceGroupMembers(self._transport)
        self.workspace_members = resources.WorkspaceMembers(self._transport)

    def close(self) -> None:
        self._transport.close()

    def __enter__(self) -> Instantly:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()


class AsyncInstantly:
    """Asynchronous client for the Instantly.ai V2 API.

    Same surface as :class:`Instantly`, just with ``await``:

        >>> client = AsyncInstantly(api_key="...")
        >>> async for campaign in await client.campaigns.list():
        ...     print(campaign.name)
    """

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: httpx.Timeout = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        self._transport = AsyncTransport(
            api_key=_resolve_api_key(api_key),
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            http_client=http_client,
        )

        self.api_keys = resources.AsyncAPIKeys(self._transport)
        self.accounts = resources.AsyncAccounts(self._transport)
        self.account_campaign_mappings = resources.AsyncAccountCampaignMappings(self._transport)
        self.audit_logs = resources.AsyncAuditLogs(self._transport)
        self.background_jobs = resources.AsyncBackgroundJobs(self._transport)
        self.block_list_entries = resources.AsyncBlockListEntries(self._transport)
        self.campaigns = resources.AsyncCampaigns(self._transport)
        self.subsequences = resources.AsyncCampaignSubsequences(self._transport)
        self.crm_actions = resources.AsyncCRMActions(self._transport)
        self.custom_tags = resources.AsyncCustomTags(self._transport)
        self.custom_tag_mappings = resources.AsyncCustomTagMappings(self._transport)
        self.dfy_email_account_orders = resources.AsyncDFYEmailAccountOrders(self._transport)
        self.emails = resources.AsyncEmails(self._transport)
        self.email_verification = resources.AsyncEmailVerification(self._transport)
        self.inbox_placement_analytics = resources.AsyncInboxPlacementAnalytics(self._transport)
        self.inbox_placement_reports = resources.AsyncInboxPlacementReports(self._transport)
        self.inbox_placement_tests = resources.AsyncInboxPlacementTests(self._transport)
        self.leads = resources.AsyncLeads(self._transport)
        self.lead_labels = resources.AsyncLeadLabels(self._transport)
        self.lead_lists = resources.AsyncLeadLists(self._transport)
        self.oauth = resources.AsyncOAuth(self._transport)
        self.supersearch_enrichment = resources.AsyncSuperSearchEnrichment(self._transport)
        self.webhooks = resources.AsyncWebhooks(self._transport)
        self.webhook_events = resources.AsyncWebhookEvents(self._transport)
        self.workspaces = resources.AsyncWorkspaces(self._transport)
        self.workspace_billing = resources.AsyncWorkspaceBilling(self._transport)
        self.workspace_group_members = resources.AsyncWorkspaceGroupMembers(self._transport)
        self.workspace_members = resources.AsyncWorkspaceMembers(self._transport)

    async def close(self) -> None:
        await self._transport.aclose()

    async def __aenter__(self) -> AsyncInstantly:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.close()
