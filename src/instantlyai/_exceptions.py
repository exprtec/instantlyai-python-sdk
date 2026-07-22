"""Typed exception hierarchy raised by the SDK.

Callers should catch these instead of inspecting HTTP status codes:

    try:
        client.campaigns.retrieve("...")
    except instantlyai.NotFoundError:
        ...
    except instantlyai.RateLimitError as exc:
        time.sleep(exc.retry_after or 1)
"""

from __future__ import annotations

from typing import Any

import httpx

__all__ = [
    "APIConnectionError",
    "APIStatusError",
    "APITimeoutError",
    "AuthenticationError",
    "ConflictError",
    "InstantlyError",
    "NotFoundError",
    "PermissionDeniedError",
    "RateLimitError",
    "ServerError",
    "ValidationError",
]


class InstantlyError(Exception):
    """Base class for every error raised by this SDK."""


class APIConnectionError(InstantlyError):
    """The request never reached the server (DNS, TLS, refused connection, ...)."""

    def __init__(self, message: str = "Connection error.", *, request: httpx.Request) -> None:
        super().__init__(message)
        self.request = request


class APITimeoutError(APIConnectionError):
    """The request timed out before a response was received."""

    def __init__(self, request: httpx.Request) -> None:
        super().__init__("Request timed out.", request=request)


class APIStatusError(InstantlyError):
    """The API responded, but with a non-2xx status code.

    Raised as one of the subclasses below when the status code is
    recognised; falls back to ``APIStatusError`` itself otherwise.
    """

    def __init__(self, message: str, *, response: httpx.Response, body: Any) -> None:
        super().__init__(message)
        self.response = response
        self.status_code = response.status_code
        self.body = body
        self.request_id = response.headers.get("x-request-id")


class AuthenticationError(APIStatusError):
    """401 - the API key is missing, invalid, or has been revoked."""


class PermissionDeniedError(APIStatusError):
    """402/403 - the API key lacks the required scope, or the workspace plan doesn't allow this."""


class NotFoundError(APIStatusError):
    """404 - the requested resource doesn't exist."""


class ConflictError(APIStatusError):
    """409 - the request conflicts with the current state of the resource."""


class ValidationError(APIStatusError):
    """400/413 - the request body or query parameters failed validation."""


class RateLimitError(APIStatusError):
    """429 - too many requests; back off and retry.

    :attr:`retry_after` reflects the server's ``Retry-After`` header, in
    seconds, when present.
    """

    @property
    def retry_after(self) -> float | None:
        value = self.response.headers.get("retry-after")
        if value is None:
            return None
        try:
            return float(value)
        except ValueError:
            return None


class ServerError(APIStatusError):
    """5xx - something went wrong on Instantly's end. Safe to retry."""


_STATUS_CODE_TO_ERROR: dict[int, type[APIStatusError]] = {
    400: ValidationError,
    401: AuthenticationError,
    402: PermissionDeniedError,
    403: PermissionDeniedError,
    404: NotFoundError,
    409: ConflictError,
    413: ValidationError,
    429: RateLimitError,
}


def build_status_error(response: httpx.Response, body: Any) -> APIStatusError:
    """Map an httpx response to the appropriate :class:`APIStatusError` subclass."""
    status_code = response.status_code
    error_cls = _STATUS_CODE_TO_ERROR.get(status_code)
    if error_cls is None:
        error_cls = ServerError if status_code >= 500 else APIStatusError
    return error_cls(_extract_message(response, body), response=response, body=body)


def _extract_message(response: httpx.Response, body: Any) -> str:
    if isinstance(body, dict):
        message = body.get("message") or body.get("error")
        if isinstance(message, str):
            return f"{response.status_code} {message}"
    text = response.text.strip()
    return f"{response.status_code} {text or response.reason_phrase}"
