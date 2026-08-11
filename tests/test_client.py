import pytest

from instantlyai import AsyncInstantly, Instantly
from instantlyai._version import __version__

RESOURCE_NAMES = [
    "account_campaign_mappings",
    "accounts",
    "api_keys",
    "audit_logs",
    "background_jobs",
    "block_list_entries",
    "campaigns",
    "crm_actions",
    "custom_tag_mappings",
    "custom_tags",
    "dfy_email_account_orders",
    "email_verification",
    "emails",
    "inbox_placement_analytics",
    "inbox_placement_reports",
    "inbox_placement_tests",
    "lead_labels",
    "lead_lists",
    "leads",
    "oauth",
    "subsequences",
    "supersearch_enrichment",
    "webhook_events",
    "webhooks",
    "workspace_billing",
    "workspace_group_members",
    "workspace_members",
    "workspaces",
]


def test_public_version_uses_single_source_of_truth() -> None:
    import instantlyai

    assert instantlyai.__version__ == __version__


def test_explicit_api_key_is_used(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("INSTANTLY_API_KEY", raising=False)
    client = Instantly(api_key="explicit-key")
    assert client._transport.api_key == "explicit-key"
    client.close()


def test_falls_back_to_env_var(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("INSTANTLY_API_KEY", "env-key")
    client = Instantly()
    assert client._transport.api_key == "env-key"
    client.close()


def test_explicit_api_key_takes_priority_over_env_var(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("INSTANTLY_API_KEY", "env-key")
    client = Instantly(api_key="explicit-key")
    assert client._transport.api_key == "explicit-key"
    client.close()


def test_missing_api_key_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("INSTANTLY_API_KEY", raising=False)
    with pytest.raises(ValueError, match="No API key provided"):
        Instantly()


def test_sync_client_is_a_context_manager(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("INSTANTLY_API_KEY", "env-key")
    with Instantly() as client:
        assert client.campaigns is not None


def test_sync_client_exposes_all_resource_namespaces() -> None:
    client = Instantly(api_key="key")
    try:
        for name in RESOURCE_NAMES:
            assert getattr(client, name) is not None
    finally:
        client.close()


def test_multiple_clients_do_not_share_state() -> None:
    client_a = Instantly(api_key="key-a")
    client_b = Instantly(api_key="key-b")
    assert client_a._transport.api_key == "key-a"
    assert client_b._transport.api_key == "key-b"
    client_a.close()
    client_b.close()


def test_requests_per_minute_reaches_the_transport_and_defaults_to_unset() -> None:
    paced = Instantly(api_key="key", requests_per_minute=20)
    unpaced = Instantly(api_key="key")
    assert paced._transport.requests_per_minute == 20
    assert unpaced._transport.requests_per_minute is None
    paced.close()
    unpaced.close()


@pytest.mark.asyncio
async def test_async_client_is_a_context_manager(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("INSTANTLY_API_KEY", "env-key")
    async with AsyncInstantly() as client:
        assert client.campaigns is not None


@pytest.mark.asyncio
async def test_async_client_exposes_all_resource_namespaces() -> None:
    client = AsyncInstantly(api_key="key")
    try:
        for name in RESOURCE_NAMES:
            assert getattr(client, name) is not None
    finally:
        await client.close()
