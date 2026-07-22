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
    departments_count: int
