from typing import Protocol

from social_engineering_simulator.domain.email_template.repository import TemplateRepository
from social_engineering_simulator.domain.organizations.campaign.campaign_event_repository import CampaignEventRepository
from social_engineering_simulator.domain.organizations.campaign.repository import CampaignRepository
from social_engineering_simulator.domain.organizations.repository import OrganizationRepository


class UnitOfWork(Protocol):
    organizations: OrganizationRepository
    campaigns: CampaignRepository
    campaigns_events: CampaignEventRepository
    templates: TemplateRepository

    async def __aenter__(self) -> "UnitOfWork":
        ...

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        ...

    async def commit(self) -> None:
        ...

    async def rollback(self) -> None:
        ...

