from datetime import datetime
from typing import Protocol
from uuid import UUID

from social_engineering_simulator.domain.organizations.campaign.entity import Campaign


class CampaignRepository(Protocol):
    async def save(self, campaign: Campaign) -> None:
        ...

    async def get_by_id(self, campaign_id: UUID) -> Campaign | None:
        ...

    async def delete(self, campaign_id: UUID) -> None:
        ...

    async def exists(self, campaign_id: UUID) -> bool:
        ...

    async def get_campaigns_ready_to_start(self, datetime_now: datetime) -> list[Campaign]:
        ...
