"""Run a campaign: create it, activate it, and check its sending status.

Executed in CI against a mocked API (see tests/test_examples.py).
"""

from __future__ import annotations

import instantlyai
from instantlyai.models import CampaignSchedule


def main(client: instantlyai.Instantly) -> None:
    campaign = client.campaigns.create(
        name="Q1 Outbound",
        campaign_schedule=CampaignSchedule.model_validate(
            {
                "schedules": [
                    {
                        "name": "Business hours",
                        "timing": {"from": "09:00", "to": "17:00"},
                        "days": {"1": True, "2": True, "3": True, "4": True, "5": True},
                        "timezone": "Etc/GMT+12",
                    }
                ]
            }
        ),
    )
    client.campaigns.activate(str(campaign.id))
    status = client.campaigns.sending_status(str(campaign.id))
    print(status)


if __name__ == "__main__":
    with instantlyai.Instantly() as client:
        main(client)
