from dataclasses import field, dataclass
from uuid import UUID

from social_engineering_simulator.domain.organizations.campaign.campaign_employee_event import CampaignEmployeeEvent
from social_engineering_simulator.domain.organizations.campaign.campaign_event_repository import CampaignEventRepository


@dataclass
class CampaignEventRepositoryInMemory(CampaignEventRepository):
    _events: dict[UUID, CampaignEmployeeEvent] = field(default_factory=dict)

    def save(self, event: CampaignEmployeeEvent) -> None:
        self._events[event.event_id] = event

    def get_by_campaign_id(self, campaign_id: UUID) -> list[CampaignEmployeeEvent]:
        return [event for event in self._events.values() if event.campaign_id == campaign_id]

    def get_by_employee_id(self, employee_id: UUID) -> list[CampaignEmployeeEvent]:
        return [event for event in self._events.values() if event.employee_id == employee_id]

    def get_by_event_id(self, event_id: UUID) -> CampaignEmployeeEvent | None:
        return self._events.get(event_id)
