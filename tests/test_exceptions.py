import httpx
import pytest

from instantlyai._exceptions import (
    APIStatusError,
    AuthenticationError,
    ConflictError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
    ServerError,
    ValidationError,
    build_status_error,
)


def _response(
    status_code: int, *, json_body: dict | None = None, headers: dict | None = None
) -> httpx.Response:
    request = httpx.Request("GET", "https://api.instantly.ai/api/v2/campaigns")
    return httpx.Response(status_code, request=request, json=json_body, headers=headers)


@pytest.mark.parametrize(
    ("status_code", "expected_cls"),
    [
        (400, ValidationError),
        (401, AuthenticationError),
        (402, PermissionDeniedError),
        (403, PermissionDeniedError),
        (404, NotFoundError),
        (409, ConflictError),
        (413, ValidationError),
        (429, RateLimitError),
        (500, ServerError),
        (503, ServerError),
        (418, APIStatusError),
    ],
)
def test_build_status_error_maps_status_code(
    status_code: int, expected_cls: type[APIStatusError]
) -> None:
    response = _response(
        status_code, json_body={"statusCode": status_code, "error": "x", "message": "boom"}
    )
    error = build_status_error(
        response, {"statusCode": status_code, "error": "x", "message": "boom"}
    )
    assert isinstance(error, expected_cls)
    assert error.status_code == status_code
    assert "boom" in str(error)


def test_rate_limit_error_exposes_retry_after() -> None:
    response = _response(429, headers={"retry-after": "12"})
    error = build_status_error(response, None)
    assert isinstance(error, RateLimitError)
    assert error.retry_after == 12.0


def test_rate_limit_error_retry_after_missing() -> None:
    response = _response(429)
    error = build_status_error(response, None)
    assert isinstance(error, RateLimitError)
    assert error.retry_after is None


def test_rate_limit_error_retry_after_malformed() -> None:
    response = _response(429, headers={"retry-after": "not-a-number"})
    error = build_status_error(response, None)
    assert isinstance(error, RateLimitError)
    assert error.retry_after is None


def test_status_error_falls_back_to_response_text_when_body_not_a_dict() -> None:
    response = _response(404, json_body=None)
    error = build_status_error(response, ["unexpected", "list", "body"])
    assert isinstance(error, NotFoundError)
    assert "404" in str(error)
