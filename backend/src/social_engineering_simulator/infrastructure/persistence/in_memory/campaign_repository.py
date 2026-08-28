from dataclasses import dataclass, field
from uuid import UUID

from social_engineering_simulator.domain.organizations.campaign.entity import Campaign
from social_engineering_simulator.domain.organizations.campaign.repository import CampaignRepository


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
