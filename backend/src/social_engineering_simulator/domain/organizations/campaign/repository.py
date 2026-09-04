from datetime import datetime
from typing import Protocol
from uuid import UUID

from social_engineering_simulator.domain.organizations.campaign.entity import Campaign


class CampaignRepository(Protocol):
    def save(self, campaign: Campaign) -> None:
        ...

    def get_by_id(self, campaign_id: UUID) -> Campaign | None:
        ...

    def delete(self, campaign_id: UUID) -> None:
        ...

    def exists(self, campaign_id: UUID) -> bool:
        ...

    def get_campaigns_ready_to_start(self, datetime_now: datetime) -> list[Campaign]:
        ...
