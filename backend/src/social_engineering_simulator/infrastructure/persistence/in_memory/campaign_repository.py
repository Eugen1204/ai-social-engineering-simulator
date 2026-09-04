from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from social_engineering_simulator.domain.organizations.campaign.entity import Campaign
from social_engineering_simulator.domain.organizations.campaign.repository import CampaignRepository
from social_engineering_simulator.domain.organizations.campaign.value_object import CampaignStatus


@dataclass
class CampaignRepoInMemory(CampaignRepository):
    _campaigns: dict[UUID, Campaign] = field(default_factory=dict)

    def save(self, campaign: Campaign) -> None:
        self._campaigns[campaign.id] = campaign

    def get_by_id(self, campaign_id: UUID) -> Campaign | None:
        return self._campaigns.get(campaign_id)

    def delete(self, campaign_id: UUID) -> None:
        if campaign_id in self._campaigns:
            del self._campaigns[campaign_id]

    def exists(self, campaign_id: UUID) -> bool:
        return self._campaigns.get(campaign_id) is not None

    def get_campaigns_ready_to_start(self, datetime_now: datetime) -> list[Campaign]:
        ready_campaign = []
        for campaign in self._campaigns.values():
            if (campaign.status == CampaignStatus.Scheduled
                    and campaign.schedule_time is not None
                    and campaign.schedule_time <= datetime_now):
                ready_campaign.append(campaign)

        return ready_campaign
