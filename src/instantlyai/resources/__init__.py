"""Resource namespaces attached to ``Instantly`` and ``AsyncInstantly`` clients."""

from .account_campaign_mappings import AccountCampaignMappings, AsyncAccountCampaignMappings
from .accounts import Accounts, AsyncAccounts
from .api_keys import APIKeys, AsyncAPIKeys
from .audit_logs import AsyncAuditLogs, AuditLogs
from .background_jobs import AsyncBackgroundJobs, BackgroundJobs
from .block_list_entries import AsyncBlockListEntries, BlockListEntries
from .campaigns import AsyncCampaigns, Campaigns
from .crm_actions import AsyncCRMActions, CRMActions
from .custom_tag_mappings import AsyncCustomTagMappings, CustomTagMappings
from .custom_tags import AsyncCustomTags, CustomTags
from .dfy_email_account_orders import AsyncDFYEmailAccountOrders, DFYEmailAccountOrders
from .email_verification import AsyncEmailVerification, EmailVerification
from .emails import AsyncEmails, Emails
from .inbox_placement_analytics import AsyncInboxPlacementAnalytics, InboxPlacementAnalytics
from .inbox_placement_reports import AsyncInboxPlacementReports, InboxPlacementReports
from .inbox_placement_tests import AsyncInboxPlacementTests, InboxPlacementTests
from .lead_labels import AsyncLeadLabels, LeadLabels
from .lead_lists import AsyncLeadLists, LeadLists
from .leads import AsyncLeads, Leads
from .oauth import AsyncOAuth, OAuth
from .subsequences import AsyncCampaignSubsequences, CampaignSubsequences
from .supersearch_enrichment import AsyncSuperSearchEnrichment, SuperSearchEnrichment
from .webhook_events import AsyncWebhookEvents, WebhookEvents
from .webhooks import AsyncWebhooks, Webhooks
from .workspace_billing import AsyncWorkspaceBilling, WorkspaceBilling
from .workspace_group_members import AsyncWorkspaceGroupMembers, WorkspaceGroupMembers
from .workspace_members import AsyncWorkspaceMembers, WorkspaceMembers
from .workspaces import AsyncWorkspaces, Workspaces

__all__ = [
    "APIKeys",
    "AccountCampaignMappings",
    "Accounts",
    "AsyncAPIKeys",
    "AsyncAccountCampaignMappings",
    "AsyncAccounts",
    "AsyncAuditLogs",
    "AsyncBackgroundJobs",
    "AsyncBlockListEntries",
    "AsyncCRMActions",
    "AsyncCampaignSubsequences",
    "AsyncCampaigns",
    "AsyncCustomTagMappings",
    "AsyncCustomTags",
    "AsyncDFYEmailAccountOrders",
    "AsyncEmailVerification",
    "AsyncEmails",
    "AsyncInboxPlacementAnalytics",
    "AsyncInboxPlacementReports",
    "AsyncInboxPlacementTests",
    "AsyncLeadLabels",
    "AsyncLeadLists",
    "AsyncLeads",
    "AsyncOAuth",
    "AsyncSuperSearchEnrichment",
    "AsyncWebhookEvents",
    "AsyncWebhooks",
    "AsyncWorkspaceBilling",
    "AsyncWorkspaceGroupMembers",
    "AsyncWorkspaceMembers",
    "AsyncWorkspaces",
    "AuditLogs",
    "BackgroundJobs",
    "BlockListEntries",
    "CRMActions",
    "CampaignSubsequences",
    "Campaigns",
    "CustomTagMappings",
    "CustomTags",
    "DFYEmailAccountOrders",
    "EmailVerification",
    "Emails",
    "InboxPlacementAnalytics",
    "InboxPlacementReports",
    "InboxPlacementTests",
    "LeadLabels",
    "LeadLists",
    "Leads",
    "OAuth",
    "SuperSearchEnrichment",
    "WebhookEvents",
    "Webhooks",
    "WorkspaceBilling",
    "WorkspaceGroupMembers",
    "WorkspaceMembers",
    "Workspaces",
]
