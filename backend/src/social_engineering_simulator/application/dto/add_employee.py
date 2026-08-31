from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class AddCampaignEmployeeRequest:
    employee_id: UUID
    campaign_id: UUID


@dataclass(frozen=True)
class RemoveCampaignEmployeeRequest:
    employee_id: UUID
    campaign_id: UUID


@dataclass(frozen=True)
class CampaignEmployeeResponse:
    id: UUID
    name: str
    email: str
    department_id: UUID
