"""Async usage: the same client surface, with await / async for.

Executed in CI against a mocked API (see tests/test_examples.py).
"""

from __future__ import annotations

import asyncio

import instantlyai


async def main(client: instantlyai.AsyncInstantly) -> None:
    async for campaign in await client.campaigns.list(limit=10):
        print(campaign.id, campaign.name)


async def run() -> None:
    async with instantlyai.AsyncInstantly() as client:
        await main(client)


if __name__ == "__main__":
    asyncio.run(run())
