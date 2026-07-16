from datetime import datetime, UTC
from social_engineering_simulator.domain.organizations.value_object import IndustryType, OrganizationName
from uuid import UUID, uuid4
from dataclasses import dataclass, field

@dataclass
class Organization:
    name: OrganizationName
    industry: IndustryType
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    id: UUID = field(default_factory=uuid4)

    def rename(self, new_name: OrganizationName) -> None:
        self.name = new_name

    def change_industry(self, new_industries: IndustryType) -> None:
        self.industry = new_industries

