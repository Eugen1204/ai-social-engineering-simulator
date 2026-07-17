from datetime import datetime, UTC
from social_engineering_simulator.domain.organizations.department.value_object import DepartmentName
from uuid import UUID, uuid4
from dataclasses import dataclass, field


@dataclass
class Department:
    name: DepartmentName
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    id: UUID = field(default_factory=uuid4)

    def rename(self, new_name: DepartmentName) -> None:
        self.name = new_name
