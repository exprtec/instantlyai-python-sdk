"""Handle rate limits: built-in retry/backoff, plus catching RateLimitError yourself.

Executed in CI against a mocked API (see tests/test_examples.py).
"""

from __future__ import annotations

import time

import instantlyai


def main(client: instantlyai.Instantly) -> None:
    # The client already retries 429s with exponential backoff (honouring
    # Retry-After, capped at `max_backoff`) up to `max_retries` times --
    # most rate limits never surface to your code at all.
    try:
        list(client.campaigns.list(limit=100))
    except instantlyai.RateLimitError as exc:
        # Raised only once retries are exhausted.
        time.sleep(exc.retry_after or 1.0)
        list(client.campaigns.list(limit=100))


if __name__ == "__main__":
    # `max_backoff` caps how long any single retry can wait, even if the
    # server's `Retry-After` header asks for longer -- useful when the whole
    # call is wrapped in a caller-side deadline (e.g. `asyncio.wait_for`).
    with instantlyai.Instantly(max_retries=5, max_backoff=10.0) as client:
        main(client)
