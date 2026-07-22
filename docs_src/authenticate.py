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
