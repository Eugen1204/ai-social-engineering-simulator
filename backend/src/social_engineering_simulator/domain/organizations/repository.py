from typing import Protocol
from uuid import UUID

from social_engineering_simulator.domain.organizations.entity import Organization


class OrganizationRepository(Protocol):
    def save(self, organization: Organization) -> None:
        ...

    def get_by_id(self, organization_id: UUID) -> Organization | None:
        ...

    def delete(self, organization_id: UUID) -> None:
        ...

    def exists(self, organization_id: UUID) -> bool:
        ...

    def get_all_organization(self) -> tuple[Organization, ...]:
        ...


