from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from social_engineering_simulator.domain.organizations.campaign.value_object import EventType


@dataclass
class CampaignEmployeeEvent:
    event_id: UUID
    campaign_id: UUID
    employee_id: UUID
    occurred_at: datetime
    event_type: EventType
