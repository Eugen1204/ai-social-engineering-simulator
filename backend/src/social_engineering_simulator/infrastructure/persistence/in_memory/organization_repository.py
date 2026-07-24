from dataclasses import field, dataclass
from uuid import UUID
from social_engineering_simulator.domain.organizations.entity import Organization
from social_engineering_simulator.domain.organizations.repository import OrganizationRepository


@dataclass
class OrganizationRepoInMemory(OrganizationRepository):
    _organizations: dict[UUID, Organization] = field(default_factory=dict)

    def save(self, organization: Organization) -> None:
        self._organizations[organization.id] = organization

    def get_by_id(self, organization_id: UUID) -> Organization | None:
        return self._organizations.get(organization_id)

    def delete(self, organization_id: UUID) -> None:
        if organization_id in self._organizations:
            del self._organizations[organization_id]

    def exists(self, organization_id: UUID) -> bool:
        return self.get_by_id(organization_id) is not None

    def get_all_organization(self) -> tuple[Organization, ...]:
        return tuple(self._organizations.values())

