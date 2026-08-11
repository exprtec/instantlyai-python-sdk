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
    assert compute_backoff(0, retry_after=5.0, max_backoff=30.0) == 5.0
    assert compute_backoff(3, retry_after=0.0, max_backoff=30.0) == 0.0


def test_compute_backoff_caps_retry_after_at_max_backoff() -> None:
    assert compute_backoff(0, retry_after=120.0, max_backoff=30.0) == 30.0


def test_compute_backoff_caps_exponential_growth_at_max_backoff() -> None:
    assert compute_backoff(10, retry_after=None, max_backoff=30.0) == 30.0


def test_compute_backoff_grows_exponentially_without_retry_after() -> None:
    zero = compute_backoff(0, retry_after=None, max_backoff=30.0)
    one = compute_backoff(1, retry_after=None, max_backoff=30.0)
    two = compute_backoff(2, retry_after=None, max_backoff=30.0)
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


def test_pace_wait_seconds_is_zero_when_requests_per_minute_unset() -> None:
    transport = SyncTransport(api_key="key")
    assert transport._pace_wait_seconds() == 0.0
    assert transport._pace_wait_seconds() == 0.0


def test_pace_wait_seconds_spaces_out_calls(monkeypatch: pytest.MonkeyPatch) -> None:
    clock = iter([100.0, 100.1, 103.0])
    monkeypatch.setattr("instantlyai._transport.time.monotonic", lambda: next(clock))
    transport = SyncTransport(api_key="key", requests_per_minute=60)  # 1s interval

    assert transport._pace_wait_seconds() == pytest.approx(0.0)  # first call, no reservation yet
    assert transport._pace_wait_seconds() == pytest.approx(0.9)  # 0.1s later, wait out the rest
    assert transport._pace_wait_seconds() == pytest.approx(0.0)  # already past the reserved slot


def test_async_transport_shares_the_same_pacer() -> None:
    transport = AsyncTransport(api_key="key", requests_per_minute=30)  # 2s interval
    assert transport._min_request_interval == pytest.approx(2.0)


@respx.mock
def test_sync_transport_sleeps_for_pace_wait(monkeypatch: pytest.MonkeyPatch) -> None:
    sleeps: list[float] = []
    monkeypatch.setattr("instantlyai._transport.time.sleep", lambda s: sleeps.append(s))
    respx.get("https://api.instantly.ai/api/v2/campaigns").mock(
        return_value=httpx.Response(200, json={"items": []})
    )
    transport = SyncTransport(api_key="key")
    monkeypatch.setattr(transport, "_pace_wait_seconds", lambda: 0.75)
    transport.request("GET", "/api/v2/campaigns")
    assert sleeps == [0.75]


@respx.mock
@pytest.mark.asyncio
async def test_async_transport_sleeps_for_pace_wait(monkeypatch: pytest.MonkeyPatch) -> None:
    sleeps: list[float] = []

    async def fake_sleep(seconds: float) -> None:
        sleeps.append(seconds)

    monkeypatch.setattr("instantlyai._transport.asyncio.sleep", fake_sleep)
    respx.get("https://api.instantly.ai/api/v2/campaigns").mock(
        return_value=httpx.Response(200, json={"items": []})
    )
    transport = AsyncTransport(api_key="key")
    monkeypatch.setattr(transport, "_pace_wait_seconds", lambda: 0.4)
    await transport.request("GET", "/api/v2/campaigns")
    await transport.aclose()
    assert sleeps == [0.4]


@respx.mock
def test_rate_limit_error_raised_after_exhausting_retries(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("instantlyai._transport.time.sleep", lambda _seconds: None)
    route = respx.get("https://api.instantly.ai/api/v2/campaigns")
    route.mock(return_value=httpx.Response(429, headers={"retry-after": "0"}))
    transport = SyncTransport(api_key="key", max_retries=1)
    with pytest.raises(RateLimitError):
        transport.request("GET", "/api/v2/campaigns")
    assert route.call_count == 2
