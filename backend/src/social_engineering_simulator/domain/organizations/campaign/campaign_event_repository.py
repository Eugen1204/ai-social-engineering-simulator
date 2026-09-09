from asyncio import Protocol
from uuid import UUID

from social_engineering_simulator.domain.organizations.campaign.campaign_employee_event import CampaignEmployeeEvent


class CampaignEventRepository(Protocol):
    def save(self, event: CampaignEmployeeEvent) -> None:
        ...

    def get_by_campaign_id(self, campaign_id: UUID) -> list[CampaignEmployeeEvent]:
        ...

    def get_by_employee_id(self, employee_id: UUID) -> list[CampaignEmployeeEvent]:
        ...

    def get_by_event_id(self, event_id: UUID) -> CampaignEmployeeEvent | None:
        ...

    def get_by_campaign_and_employee_id(self, campaign_id: UUID, employee_id: UUID) -> list[CampaignEmployeeEvent]:
        ...
