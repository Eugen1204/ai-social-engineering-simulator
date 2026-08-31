from dataclasses import dataclass
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







