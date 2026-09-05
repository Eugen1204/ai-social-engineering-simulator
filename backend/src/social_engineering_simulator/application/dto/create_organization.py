from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class CreateOrganizationRequest:
    name: str
    industry: str
    departments: list[str]


@dataclass(frozen=True)
class OrganizationResponse:
    id: UUID
    name: str
    industry: str
    count_departments: int


@dataclass(frozen=True)
class EmployeeRequest:
    name: str
    email: str
    dep_name: str
    org_id: UUID


@dataclass(frozen=True)
class EmployeeResponse:
    id: UUID
    name: str
    email: str
    org_id: UUID


@dataclass(frozen=True)
class ExecuteCampaignResponse:
    campaign_id: UUID
    total_employees: int
    sent_count: int
    skipped_count: int
    execute_at: datetime








