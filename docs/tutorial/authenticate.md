# Authenticate

`instantlyai` resolves your API key in a fixed order:

1. An explicit `api_key=...` argument to `Instantly(...)` / `AsyncInstantly(...)`.
2. The `INSTANTLY_API_KEY` environment variable.

There are no config files, and no global mutable state -- every client instance carries
its own credentials, so multiple clients (e.g. one per Instantly workspace) coexist
safely in the same process.

<!-- docs_src: authenticate.py -->
```python
"""Authenticate: explicit API key vs. the INSTANTLY_API_KEY environment variable.

Executed in CI against a mocked API (see tests/test_examples.py).
"""

from __future__ import annotations

import os

import instantlyai


def main() -> None:
    # 1. Explicit api_key argument -- takes priority over the environment.
    client = instantlyai.Instantly(api_key="sk-...")
    client.close()

    # 2. Falls back to INSTANTLY_API_KEY if api_key is omitted.
    os.environ["INSTANTLY_API_KEY"] = "sk-..."
    client = instantlyai.Instantly()
    client.close()

    # 3. Multiple clients never share state -- safe for multi-workspace use.
    workspace_a = instantlyai.Instantly(api_key="key-for-workspace-a")
    workspace_b = instantlyai.Instantly(api_key="key-for-workspace-b")
    workspace_a.close()
    workspace_b.close()


if __name__ == "__main__":
    main()
```

If neither is set, the client raises `ValueError` immediately at construction time
rather than failing later on the first request.

Both `Instantly` and `AsyncInstantly` are context managers, so `with`/`async with`
closes the underlying HTTP connection pool for you:

```python
with instantlyai.Instantly() as client:
    ...
```
