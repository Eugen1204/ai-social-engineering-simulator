from datetime import datetime, UTC
from social_engineering_simulator.domain.organizations.Department.value_object import DepartmentName
from uuid import UUID, uuid4
from dataclasses import dataclass, field
from social_engineering_simulator.domain.organizations.Department.exceptions import InvalidOrganizationIdError


@dataclass
class Department:
    name: DepartmentName
    organization_id: UUID
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    id: UUID = field(default_factory=uuid4)

    def rename(self, new_name: DepartmentName) -> None:
        self.name = new_name

    def __post_init__(self):
        if not self.organization_id:
            raise InvalidOrganizationIdError("ID organization cannot be empty")


