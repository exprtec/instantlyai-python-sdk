"""Integration-style tests: exercise real resource methods against a mocked API."""

import httpx
import pytest
import respx
from conftest import SCHEDULE_JSON, campaign_json, lead_json, uuid_fixture

from instantlyai import AsyncInstantly, Instantly, NotFoundError
from instantlyai.models import CampaignSchedule


@respx.mock
def test_campaigns_create_serializes_nested_model_body() -> None:
    route = respx.post("https://api.instantly.ai/api/v2/campaigns").mock(
        return_value=httpx.Response(200, json=campaign_json())
    )
    client = Instantly(api_key="key")
    campaign = client.campaigns.create(
        name="My Campaign", campaign_schedule=CampaignSchedule.model_validate(SCHEDULE_JSON)
    )
    assert str(campaign.id) == uuid_fixture("1")
    assert campaign.name == "My Campaign"

    sent_body = route.calls.last.request.content
    assert b"campaign_schedule" in sent_body
    assert b"NOT_GIVEN" not in sent_body  # NotGiven fields must never reach the wire
    client.close()


@respx.mock
def test_campaigns_list_auto_paginates_across_pages() -> None:
    # A single route with an ordered side_effect -- registering two routes that
    # both match on "limit=2" is ambiguous (the second page's request also
    # satisfies the first route's looser matcher), which causes an infinite
    # pagination loop instead of a clean two-page walk.
    route = respx.get("https://api.instantly.ai/api/v2/campaigns")
    route.side_effect = [
        httpx.Response(
            200,
            json={
                "items": [campaign_json("1"), campaign_json("2")],
                "next_starting_after": uuid_fixture("2"),
            },
        ),
        httpx.Response(200, json={"items": [campaign_json("3")]}),
    ]

    client = Instantly(api_key="key")
    ids = [str(c.id) for c in client.campaigns.list(limit=2)]
    assert ids == [uuid_fixture("1"), uuid_fixture("2"), uuid_fixture("3")]
    assert route.calls[0].request.url.params["limit"] == "2"
    assert route.calls[1].request.url.params["starting_after"] == uuid_fixture("2")
    client.close()


@respx.mock
def test_campaigns_retrieve_maps_404_to_not_found_error() -> None:
    respx.get("https://api.instantly.ai/api/v2/campaigns/missing").mock(
        return_value=httpx.Response(
            404, json={"statusCode": 404, "error": "Not Found", "message": "Resource not found"}
        )
    )
    client = Instantly(api_key="key")
    with pytest.raises(NotFoundError):
        client.campaigns.retrieve("missing")
    client.close()


@respx.mock
def test_leads_list_paginates_via_post_body_cursor() -> None:
    route = respx.post("https://api.instantly.ai/api/v2/leads/list")
    route.side_effect = [
        httpx.Response(
            200, json={"items": [lead_json("1")], "next_starting_after": uuid_fixture("1")}
        ),
        httpx.Response(200, json={"items": [lead_json("2", "b@example.com")]}),
    ]
    client = Instantly(api_key="key")
    ids = [str(lead.id) for lead in client.leads.list(limit=1)]
    assert ids == [uuid_fixture("1"), uuid_fixture("2")]

    first_call_body = route.calls[0].request.content
    second_call_body = route.calls[1].request.content
    assert b'"starting_after"' not in first_call_body
    assert f'"starting_after":"{uuid_fixture("1")}"'.encode() in second_call_body
    client.close()


@respx.mock
def test_campaigns_share_returns_none_for_no_content_response() -> None:
    respx.post(f"https://api.instantly.ai/api/v2/campaigns/{uuid_fixture('1')}/share").mock(
        return_value=httpx.Response(204)
    )
    client = Instantly(api_key="key")
    assert client.campaigns.share(uuid_fixture("1")) is None
    client.close()


@respx.mock
@pytest.mark.asyncio
async def test_async_campaigns_list_auto_paginates() -> None:
    respx.get("https://api.instantly.ai/api/v2/campaigns").mock(
        return_value=httpx.Response(200, json={"items": [campaign_json("1")]})
    )
    client = AsyncInstantly(api_key="key")
    ids = [str(c.id) async for c in await client.campaigns.list()]
    assert ids == [uuid_fixture("1")]
    await client.close()
