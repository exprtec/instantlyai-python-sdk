"""Quickstart: authenticate and list your campaigns.

Runnable as-is once ``INSTANTLY_API_KEY`` is set in the environment. Also
executed in CI (see ``tests/test_examples.py``) against a mocked API, so this
file can never drift from what actually works.
"""

from __future__ import annotations

import instantlyai


def main(client: instantlyai.Instantly) -> None:
    for campaign in client.campaigns.list(limit=10):
        print(campaign.id, campaign.name)


if __name__ == "__main__":
    with instantlyai.Instantly() as client:  # reads INSTANTLY_API_KEY from the environment
        main(client)
