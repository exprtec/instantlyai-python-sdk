import httpx
import pytest
import respx

from instantlyai._exceptions import NotFoundError, RateLimitError, ServerError
from instantlyai._transport import (
    NOT_GIVEN,
    AsyncTransport,
    SyncTransport,
    build_headers,
    clean_query_params,
    compute_backoff,
    omit_not_given,
)
from instantlyai.models import Body, EventType


def test_build_headers_includes_bearer_auth_and_user_agent() -> None:
    headers = build_headers("secret")
    assert headers["Authorization"] == "Bearer secret"
    assert headers["Accept"] == "application/json"
    assert "instantlyai-python/" in headers["User-Agent"]


def test_omit_not_given_drops_only_not_given_values() -> None:
    result = omit_not_given({"a": 1, "b": None, "c": NOT_GIVEN})
    assert result == {"a": 1, "b": None}


def test_omit_not_given_serializes_models_and_enums() -> None:
    result = omit_not_given(
        {
            "body": Body(text="hello"),
            "event_type": EventType.email_sent,
            "items": [Body(html="<p>hello</p>")],
            "omitted": NOT_GIVEN,
        }
    )
    assert result == {
        "body": {"text": "hello", "html": None},
        "event_type": "email_sent",
        "items": [{"text": None, "html": "<p>hello</p>"}],
    }


def test_clean_query_params_drops_none_and_not_given() -> None:
    result = clean_query_params({"a": 1, "b": None, "c": NOT_GIVEN, "d": False})
    assert result == {"a": 1, "d": "false"}


def test_compute_backoff_honours_retry_after() -> None:
    assert compute_backoff(0, retry_after=5.0) == 5.0
    assert compute_backoff(3, retry_after=0.0) == 0.0


def test_compute_backoff_grows_exponentially_without_retry_after() -> None:
    zero = compute_backoff(0, retry_after=None)
    one = compute_backoff(1, retry_after=None)
    two = compute_backoff(2, retry_after=None)
    assert 0.5 <= zero < 0.6
    assert 1.0 <= one < 1.2
    assert 2.0 <= two < 2.4


@respx.mock
def test_sync_transport_returns_parsed_json_on_success() -> None:
    respx.get("https://api.instantly.ai/api/v2/campaigns").mock(
        return_value=httpx.Response(200, json={"items": []})
    )
    transport = SyncTransport(api_key="key")
    assert transport.request("GET", "/api/v2/campaigns") == {"items": []}


@respx.mock
def test_sync_transport_returns_none_for_204() -> None:
    respx.delete("https://api.instantly.ai/api/v2/campaigns/1").mock(
        return_value=httpx.Response(204)
    )
    transport = SyncTransport(api_key="key")
    assert transport.request("DELETE", "/api/v2/campaigns/1") is None


@respx.mock
def test_sync_transport_raises_typed_error_on_404() -> None:
    respx.get("https://api.instantly.ai/api/v2/campaigns/missing").mock(
        return_value=httpx.Response(
            404, json={"statusCode": 404, "error": "Not Found", "message": "gone"}
        )
    )
    transport = SyncTransport(api_key="key")
    with pytest.raises(NotFoundError) as exc_info:
        transport.request("GET", "/api/v2/campaigns/missing")
    assert "gone" in str(exc_info.value)


@respx.mock
def test_sync_transport_retries_on_429_then_succeeds(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("instantlyai._transport.time.sleep", lambda _seconds: None)
    route = respx.get("https://api.instantly.ai/api/v2/campaigns")
    route.side_effect = [
        httpx.Response(429, headers={"retry-after": "0"}, json={"message": "slow down"}),
        httpx.Response(200, json={"items": []}),
    ]
    transport = SyncTransport(api_key="key", max_retries=3)
    assert transport.request("GET", "/api/v2/campaigns") == {"items": []}
    assert route.call_count == 2


@respx.mock
def test_sync_transport_gives_up_after_max_retries(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("instantlyai._transport.time.sleep", lambda _seconds: None)
    route = respx.get("https://api.instantly.ai/api/v2/campaigns")
    route.mock(return_value=httpx.Response(500, json={"message": "down"}))
    transport = SyncTransport(api_key="key", max_retries=2)
    with pytest.raises(ServerError):
        transport.request("GET", "/api/v2/campaigns")
    assert route.call_count == 3  # initial attempt + 2 retries


@respx.mock
def test_sync_transport_does_not_retry_client_errors_other_than_retryable_set() -> None:
    route = respx.get("https://api.instantly.ai/api/v2/campaigns")
    route.mock(return_value=httpx.Response(401, json={"message": "nope"}))
    transport = SyncTransport(api_key="key", max_retries=3)
    with pytest.raises(Exception):  # noqa: B017
        transport.request("GET", "/api/v2/campaigns")
    assert route.call_count == 1


@respx.mock
@pytest.mark.asyncio
async def test_async_transport_returns_parsed_json_on_success() -> None:
    respx.get("https://api.instantly.ai/api/v2/campaigns").mock(
        return_value=httpx.Response(200, json={"items": []})
    )
    transport = AsyncTransport(api_key="key")
    assert await transport.request("GET", "/api/v2/campaigns") == {"items": []}
    await transport.aclose()


@respx.mock
@pytest.mark.asyncio
async def test_async_transport_retries_on_rate_limit(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_sleep(_seconds: float) -> None:
        return None

    monkeypatch.setattr("instantlyai._transport.asyncio.sleep", fake_sleep)
    route = respx.get("https://api.instantly.ai/api/v2/campaigns")
    route.side_effect = [
        httpx.Response(429, headers={"retry-after": "0"}),
        httpx.Response(200, json={"items": []}),
    ]
    transport = AsyncTransport(api_key="key", max_retries=3)
    result = await transport.request("GET", "/api/v2/campaigns")
    assert result == {"items": []}
    assert route.call_count == 2
    await transport.aclose()


@respx.mock
def test_rate_limit_error_raised_after_exhausting_retries(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("instantlyai._transport.time.sleep", lambda _seconds: None)
    route = respx.get("https://api.instantly.ai/api/v2/campaigns")
    route.mock(return_value=httpx.Response(429, headers={"retry-after": "0"}))
    transport = SyncTransport(api_key="key", max_retries=1)
    with pytest.raises(RateLimitError):
        transport.request("GET", "/api/v2/campaigns")
    assert route.call_count == 2
