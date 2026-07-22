<!-- This file is generated from README.md by scripts/docs.py -- edit that instead. -->

# instantlyai

[![PyPI version](https://img.shields.io/pypi/v/instantlyai.svg)](https://pypi.org/project/instantlyai/)
[![CI](https://github.com/exprtec/instantlyai-python-sdk/actions/workflows/test.yml/badge.svg)](https://github.com/exprtec/instantlyai-python-sdk/actions/workflows/test.yml)
[![License](https://img.shields.io/pypi/l/instantlyai.svg)](https://github.com/exprtec/instantlyai-python-sdk/blob/main/LICENSE)
[![Python versions](https://img.shields.io/pypi/pyversions/instantlyai.svg)](https://pypi.org/project/instantlyai/)

A typed, importable Python client for the [Instantly.ai](https://instantly.ai) V2 API.

- A clean, resource-based client: `client.campaigns.list(...)`, `client.leads.create(...)`.
- Full end-to-end typing, generated from Instantly's OpenAPI spec -- real editor and
  type-checker support.
- Sync **and** async clients from a single codebase (`Instantly` / `AsyncInstantly`).
- Typed exceptions, auto-retry with backoff, and auto-paginating list methods.

> **Status:** pre-1.0 (`0.x`). Minor version bumps may include breaking changes until
> `1.0.0` -- pin accordingly. See the
> [changelog](https://exprtec.github.io/instantlyai-python-sdk/changelog/).

## Install

```bash
pip install instantlyai
```

## Quickstart

Set `INSTANTLY_API_KEY` in your environment, or pass `api_key=...` explicitly.

<!-- docs_src: quickstart.py -->
```python
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
```

Async usage is the same shape, with `AsyncInstantly` and `await`/`async for`.

## Docs

Full documentation, including the tutorial and API reference, lives at
**https://exprtec.github.io/instantlyai-python-sdk**.

- [Authenticate](https://exprtec.github.io/instantlyai-python-sdk/tutorial/authenticate/)
- [Run a campaign](https://exprtec.github.io/instantlyai-python-sdk/tutorial/run-a-campaign/)
- [Handle rate limits](https://exprtec.github.io/instantlyai-python-sdk/tutorial/handle-rate-limits/)
- [Async usage](https://exprtec.github.io/instantlyai-python-sdk/tutorial/async-usage/)

## Contributing

See [CONTRIBUTING.md](https://github.com/exprtec/instantlyai-python-sdk/blob/main/CONTRIBUTING.md).
