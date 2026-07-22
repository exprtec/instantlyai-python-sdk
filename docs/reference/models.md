# Models

Every model in `instantlyai.models` is generated from Instantly's OpenAPI spec (see
`scripts/generate_models.py`) -- never hand-edited. Resource methods return these
directly; you never construct most of them yourself except for nested request-body
fields (e.g. `CampaignSchedule` when calling `client.campaigns.create(...)`).

The most commonly used top-level entities:

::: instantlyai.models
    options:
      show_root_heading: false
      members:
        - Account
        - Campaign
        - CampaignSchedule
        - Lead
        - LeadList
        - LeadLabel
        - Webhook
        - WebhookEvent
        - Workspace
        - WorkspaceMember
        - APIKey
        - BackgroundJob
        - BlockListEntry
        - Email
        - EmailVerification
        - InboxPlacementTest
        - CustomTag
        - DFYEmailAccountOrder
        - AuditLog

The rest of the ~140 generated models (nested request/response shapes, enums) are
documented inline via their docstrings -- browse `src/instantlyai/models/_generated.py`
or your editor's autocomplete for the full set.
