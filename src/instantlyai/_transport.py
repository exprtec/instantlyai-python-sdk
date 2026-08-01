"""The httpx wrapper: auth headers, retry/backoff, and error mapping.

:class:`SyncTransport` and :class:`AsyncTransport` share every behavioural
rule (which errors are retryable, how long to back off, how to turn a
response into either a parsed body or a typed exception) through the
free functions below -- only the actual httpx call differs between them.
"""

from __future__ import annotations

import asyncio
import logging
import random
import time
from enum import Enum
from typing import Any, TypeAlias

import httpx
from pydantic import BaseModel

from ._exceptions import APIConnectionError, APITimeoutError, build_status_error
from ._version import __version__

logger = logging.getLogger("instantlyai")

__all__ = [
    "DEFAULT_MAX_BACKOFF",
    "DEFAULT_MAX_RETRIES",
    "DEFAULT_TIMEOUT",
    "NOT_GIVEN",
    "AsyncTransport",
    "NotGiven",
    "SyncTransport",
]

DEFAULT_TIMEOUT = httpx.Timeout(30.0, connect=5.0)
DEFAULT_MAX_RETRIES = 3
DEFAULT_MAX_BACKOFF = 30.0
DEFAULT_BASE_URL = "https://api.instantly.ai"

_RETRYABLE_STATUS_CODES = frozenset({429, 500, 502, 503, 504})
_RETRYABLE_EXCEPTIONS = (
    httpx.ConnectError,
    httpx.ConnectTimeout,
    httpx.ReadTimeout,
    httpx.WriteTimeout,
    httpx.RemoteProtocolError,
)
_QueryParam: TypeAlias = str | int | float | None
_QueryParams: TypeAlias = dict[str, _QueryParam | list[_QueryParam]]


class NotGiven:
    """Sentinel for an omitted keyword argument, distinct from an explicit ``None``.

    Some endpoints (e.g. partial updates) need to tell "field not supplied"
    apart from "field explicitly cleared". Optional parameters default to
    :data:`NOT_GIVEN` rather than ``None`` so both cases stay expressible.
    """

    def __bool__(self) -> bool:
        return False

    def __repr__(self) -> str:
        return "NOT_GIVEN"


NOT_GIVEN = NotGiven()


def _jsonable(value: object) -> object:
    if isinstance(value, NotGiven):
        return value
    if isinstance(value, BaseModel):
        return value.model_dump(mode="json", by_alias=True)
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, list):
        return [_jsonable(item) for item in value]
    if isinstance(value, tuple):
        return [_jsonable(item) for item in value]
    if isinstance(value, dict):
        return {key: _jsonable(item) for key, item in value.items()}
    return value


def omit_not_given(params: dict[str, object]) -> dict[str, object]:
    """Drop omitted values and convert Pydantic models/enums to JSON-ready data."""
    return {
        key: _jsonable(value) for key, value in params.items() if not isinstance(value, NotGiven)
    }


def _query_scalar(value: object) -> _QueryParam:
    jsonable = _jsonable(value)
    if isinstance(jsonable, bool):
        return "true" if jsonable else "false"
    if isinstance(jsonable, str | int | float) or jsonable is None:
        return jsonable
    return str(jsonable)


def _queryable(value: object) -> _QueryParam | list[_QueryParam]:
    jsonable = _jsonable(value)
    if isinstance(jsonable, list):
        return [_query_scalar(item) for item in jsonable]
    return _query_scalar(jsonable)


def compute_backoff(attempt: int, *, retry_after: float | None, max_backoff: float) -> float:
    """Seconds to wait before retry number ``attempt`` (0-indexed).

    Honours the server's ``Retry-After`` header when present; otherwise
    exponential backoff with jitter: ~0.5s, ~1s, ~2s, ... Either way, the
    wait is capped at ``max_backoff`` so a caller-side deadline stays
    meaningful regardless of what the server asks for.
    """
    if retry_after is not None:
        return min(max(retry_after, 0.0), max_backoff)
    base = 0.5 * (2**attempt)
    return min(base + random.uniform(0, base * 0.1), max_backoff)


def build_headers(api_key: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
        "User-Agent": f"instantlyai-python/{__version__}",
    }


def clean_query_params(params: dict[str, object]) -> _QueryParams:
    """Drop ``None``/``NOT_GIVEN`` values so they're omitted from the query string."""
    return {
        key: _queryable(value)
        for key, value in params.items()
        if value is not None and not isinstance(value, NotGiven)
    }


def parse_response_body(response: httpx.Response) -> Any:
    if response.status_code == 204 or not response.content:
        return None
    try:
        return response.json()
    except ValueError:
        return response.text


def _retry_after_seconds(response: httpx.Response) -> float | None:
    value = response.headers.get("retry-after")
    if value is None:
        return None
    try:
        return float(value)
    except ValueError:
        return None


class _BaseTransport:
    def __init__(
        self,
        *,
        api_key: str,
        base_url: str,
        timeout: httpx.Timeout,
        max_retries: int,
        max_backoff: float,
    ) -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.max_backoff = max_backoff

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def _should_retry_response(self, response: httpx.Response, attempt: int) -> bool:
        return attempt < self.max_retries and response.status_code in _RETRYABLE_STATUS_CODES

    def _should_retry_exception(self, exc: Exception, attempt: int) -> bool:
        return attempt < self.max_retries and isinstance(exc, _RETRYABLE_EXCEPTIONS)


class SyncTransport(_BaseTransport):
    def __init__(
        self,
        *,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: httpx.Timeout = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        max_backoff: float = DEFAULT_MAX_BACKOFF,
        http_client: httpx.Client | None = None,
    ) -> None:
        super().__init__(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            max_backoff=max_backoff,
        )
        self._client = http_client or httpx.Client(timeout=timeout)

    def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, object] | None = None,
        json: object | None = None,
    ) -> Any:
        attempt = 0
        while True:
            logger.debug("%s %s (attempt %d)", method, path, attempt + 1)
            try:
                response = self._client.request(
                    method,
                    self._url(path),
                    params=clean_query_params(params or {}),
                    json=json,
                    headers=build_headers(self.api_key),
                )
            except httpx.TimeoutException as exc:
                if self._should_retry_exception(exc, attempt):
                    wait = compute_backoff(attempt, retry_after=None, max_backoff=self.max_backoff)
                    logger.warning("%s %s timed out, retrying in %.2fs", method, path, wait)
                    time.sleep(wait)
                    attempt += 1
                    continue
                logger.error("%s %s timed out, giving up", method, path)
                raise APITimeoutError(exc.request) from exc
            except httpx.HTTPError as exc:
                if self._should_retry_exception(exc, attempt):
                    wait = compute_backoff(attempt, retry_after=None, max_backoff=self.max_backoff)
                    logger.warning("%s %s failed (%s), retrying in %.2fs", method, path, exc, wait)
                    time.sleep(wait)
                    attempt += 1
                    continue
                logger.error("%s %s failed: %s", method, path, exc)
                raise APIConnectionError(str(exc), request=exc.request) from exc

            if response.is_success:
                logger.debug("%s %s -> %d", method, path, response.status_code)
                return parse_response_body(response)
            if self._should_retry_response(response, attempt):
                wait = compute_backoff(
                    attempt,
                    retry_after=_retry_after_seconds(response),
                    max_backoff=self.max_backoff,
                )
                logger.warning(
                    "%s %s -> %d, retrying in %.2fs", method, path, response.status_code, wait
                )
                time.sleep(wait)
                attempt += 1
                continue
            logger.error("%s %s -> %d", method, path, response.status_code)
            raise build_status_error(response, parse_response_body(response))

    def close(self) -> None:
        self._client.close()


class AsyncTransport(_BaseTransport):
    def __init__(
        self,
        *,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: httpx.Timeout = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        max_backoff: float = DEFAULT_MAX_BACKOFF,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        super().__init__(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            max_backoff=max_backoff,
        )
        self._client = http_client or httpx.AsyncClient(timeout=timeout)

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, object] | None = None,
        json: object | None = None,
    ) -> Any:
        attempt = 0
        while True:
            logger.debug("%s %s (attempt %d)", method, path, attempt + 1)
            try:
                response = await self._client.request(
                    method,
                    self._url(path),
                    params=clean_query_params(params or {}),
                    json=json,
                    headers=build_headers(self.api_key),
                )
            except httpx.TimeoutException as exc:
                if self._should_retry_exception(exc, attempt):
                    wait = compute_backoff(attempt, retry_after=None, max_backoff=self.max_backoff)
                    logger.warning("%s %s timed out, retrying in %.2fs", method, path, wait)
                    await asyncio.sleep(wait)
                    attempt += 1
                    continue
                logger.error("%s %s timed out, giving up", method, path)
                raise APITimeoutError(exc.request) from exc
            except httpx.HTTPError as exc:
                if self._should_retry_exception(exc, attempt):
                    wait = compute_backoff(attempt, retry_after=None, max_backoff=self.max_backoff)
                    logger.warning("%s %s failed (%s), retrying in %.2fs", method, path, exc, wait)
                    await asyncio.sleep(wait)
                    attempt += 1
                    continue
                logger.error("%s %s failed: %s", method, path, exc)
                raise APIConnectionError(str(exc), request=exc.request) from exc

            if response.is_success:
                logger.debug("%s %s -> %d", method, path, response.status_code)
                return parse_response_body(response)
            if self._should_retry_response(response, attempt):
                wait = compute_backoff(
                    attempt,
                    retry_after=_retry_after_seconds(response),
                    max_backoff=self.max_backoff,
                )
                logger.warning(
                    "%s %s -> %d, retrying in %.2fs", method, path, response.status_code, wait
                )
                await asyncio.sleep(wait)
                attempt += 1
                continue
            logger.error("%s %s -> %d", method, path, response.status_code)
            raise build_status_error(response, parse_response_body(response))

    async def aclose(self) -> None:
        await self._client.aclose()
