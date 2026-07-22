# SDK Usage

## Auth

Resolve credentials in this order:

1. Explicit `api_key=...`
2. `INSTANTLY_API_KEY`

Client construction raises `ValueError` if neither is present.

## Sync and Async Clients

`Instantly` and `AsyncInstantly` expose the same resource namespaces and method names. Use context managers to close connection pools:

```python
with instantlyai.Instantly(api_key="...") as client:
    ...
```

```python
async with instantlyai.AsyncInstantly(api_key="...") as client:
    ...
```

Without a context manager, call `client.close()` or `await client.close()`.

## Resource Namespaces

Use the namespaces attached to the client:

```text
api_keys, accounts, account_campaign_mappings, audit_logs, background_jobs,
block_list_entries, campaigns, subsequences, crm_actions, custom_tags,
custom_tag_mappings, dfy_email_account_orders, emails, email_verification,
inbox_placement_analytics, inbox_placement_reports, inbox_placement_tests,
leads, lead_labels, lead_lists, oauth, supersearch_enrichment, webhooks,
webhook_events, workspaces, workspace_billing, workspace_group_members,
workspace_members
```

Check the resource module or generated docs before assuming a method exists.

## Return Values

Prefer attribute access on returned Pydantic models:

```python
campaign = client.campaigns.retrieve(campaign_id)
print(campaign.name)
```

Do not write `campaign["name"]`.

Some analytics/status endpoints return `JSONObject` or `list[JSONObject]` when the API does not expose a dedicated schema.

## Pagination

`list()` methods return cursor page objects. Iterating a page auto-fetches later pages:

```python
for campaign in client.campaigns.list(status=1):
    ...
```

Async iteration requires awaiting the first page:

```python
async for campaign in await client.campaigns.list():
    ...
```

For one-page control, use `.items` and `.next_starting_after` without iterating.

## IDs

Model IDs often come back as `uuid.UUID`, while resource methods accept `str`. Use `str(model.id)` when passing IDs back into resource methods.

## Errors

Catch SDK exceptions:

```python
try:
    client.campaigns.retrieve(campaign_id)
except instantlyai.NotFoundError:
    ...
except instantlyai.RateLimitError as exc:
    time.sleep(exc.retry_after or 1.0)
except instantlyai.InstantlyError:
    ...
```

The transport retries 429 and 5xx responses with exponential backoff before surfacing `RateLimitError` or `ServerError`.

