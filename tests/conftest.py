import pytest

SCHEDULE_JSON = {
    "schedules": [
        {
            "name": "Business Hours",
            "timing": {"from": "09:00", "to": "17:00"},
            "days": {"0": True, "1": True, "2": True, "3": True, "4": True, "5": False, "6": False},
            "timezone": "Etc/GMT+12",
        }
    ]
}


def uuid_fixture(seed: str) -> str:
    return f"00000000-0000-4000-8000-{seed:0>12}"


def campaign_json(seed: str = "1", name: str = "My Campaign") -> dict:
    return {
        "id": uuid_fixture(seed),
        "name": name,
        "status": 1,
        "campaign_schedule": SCHEDULE_JSON,
        "timestamp_created": "2026-01-01T00:00:00.000Z",
        "timestamp_updated": "2026-01-01T00:00:00.000Z",
    }


def lead_json(seed: str = "1", email: str = "a@example.com") -> dict:
    return {
        "id": uuid_fixture(seed),
        "email": email,
        "organization": uuid_fixture("999"),
        "status": 1,
        "email_open_count": 0,
        "email_reply_count": 0,
        "email_click_count": 0,
        "company_domain": "example.com",
        "status_summary": {},
        "timestamp_created": "2026-01-01T00:00:00.000Z",
        "timestamp_updated": "2026-01-01T00:00:00.000Z",
    }


@pytest.fixture
def api_key() -> str:
    return "test-api-key"
