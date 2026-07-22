from dataclasses import dataclass


@dataclass(frozen=True)
class CreateOrganizationRequest:
    name: str
    industry: str
    departments: list[str]


