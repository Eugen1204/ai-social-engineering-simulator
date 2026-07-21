from datetime import datetime, UTC
from social_engineering_simulator.domain.organizations.department.value_object import DepartmentName
from uuid import UUID, uuid4
from dataclasses import dataclass, field
from social_engineering_simulator.domain.organizations.department.employee.entity import Employee


@dataclass
class Department:
    name: DepartmentName
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    id: UUID = field(default_factory=uuid4)
    _employee_ids: set[UUID] = field(default_factory=set)

    def rename(self, new_name: DepartmentName) -> None:
        self.name = new_name

    def add_employee_id(self, employee_id: UUID):
        self._employee_ids.add(employee_id)

    def remove_employee_id(self, employee_id: UUID):
        self._employee_ids.remove(employee_id)

    def has_employees(self) -> bool:
        return bool(self._employee_ids)

    def get_employee_ids(self) -> tuple[UUID, ...]:
        return tuple(self._employee_ids)

