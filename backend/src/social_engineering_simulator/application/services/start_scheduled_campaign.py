from datetime import datetime, UTC, timezone

from social_engineering_simulator.domain.organizations.campaign.entity import Campaign
from social_engineering_simulator.domain.organizations.campaign.exceptions import StartCampaignError
from social_engineering_simulator.domain.organizations.campaign.repository import CampaignRepository


class StartScheduledCampaign:
    def __init__(self, campaign_repo: CampaignRepository):
        self.campaign_repo = campaign_repo

    def execute(self, now: datetime | None = None) -> list[Campaign]:
        if now is None:
            now = datetime.now(timezone.utc)

        ready_campaigns = self.campaign_repo.get_campaigns_ready_to_start(now)
        started_campaigns = []
        for campaign in ready_campaigns:
            campaign.start(started_at=now)
            self.campaign_repo.save(campaign)
            started_campaigns.append(campaign)

        return started_campaigns



