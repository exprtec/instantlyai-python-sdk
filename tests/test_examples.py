"""Execute every docs_src/*.py example against a mocked API.

These are the exact files embedded in README.md and docs/tutorial/*.md (see
scripts/docs.py) -- running them here means a doc snippet can never silently
stop working without a test failure.
"""

import importlib
import sys
from pathlib import Path

import httpx
import pytest
import respx
from conftest import campaign_json

DOCS_SRC = Path(__file__).resolve().parent.parent / "docs_src"
sys.path.insert(0, str(DOCS_SRC))


def _import(name: str):
    return importlib.import_module(name)


@respx.mock
def test_authenticate_example_runs() -> None:
    authenticate = _import("authenticate")
    authenticate.main()


@respx.mock
def test_quickstart_example_runs() -> None:
    respx.get("https://api.instantly.ai/api/v2/campaigns").mock(
        return_value=httpx.Response(200, json={"items": [campaign_json()]})
    )
    quickstart = _import("quickstart")
    with __import__("instantlyai").Instantly(api_key="key") as client:
        quickstart.main(client)


@respx.mock
def test_run_a_campaign_example_runs() -> None:
    respx.post("https://api.instantly.ai/api/v2/campaigns").mock(
        return_value=httpx.Response(200, json=campaign_json())
    )
    respx.post(
        "https://api.instantly.ai/api/v2/campaigns/00000000-0000-4000-8000-000000000001/activate"
    ).mock(return_value=httpx.Response(200, json=campaign_json()))
    respx.get(
        "https://api.instantly.ai/api/v2/campaigns/00000000-0000-4000-8000-000000000001/sending-status"
    ).mock(return_value=httpx.Response(200, json={"diagnostics": [], "summary": {}}))

    run_a_campaign = _import("run_a_campaign")
    with __import__("instantlyai").Instantly(api_key="key") as client:
        run_a_campaign.main(client)


@respx.mock
def test_handle_rate_limits_example_runs() -> None:
    respx.get("https://api.instantly.ai/api/v2/campaigns").mock(
        return_value=httpx.Response(200, json={"items": [campaign_json()]})
    )
    handle_rate_limits = _import("handle_rate_limits")
    with __import__("instantlyai").Instantly(api_key="key") as client:
        handle_rate_limits.main(client)


@respx.mock
@pytest.mark.asyncio
async def test_async_usage_example_runs() -> None:
    respx.get("https://api.instantly.ai/api/v2/campaigns").mock(
        return_value=httpx.Response(200, json={"items": [campaign_json()]})
    )
    async_usage = _import("async_usage")
    async with __import__("instantlyai").AsyncInstantly(api_key="key") as client:
        await async_usage.main(client)
