from datetime import datetime, UTC
from social_engineering_simulator.domain.organizations.value_object import IndustryType, OrganizationName
from uuid import UUID, uuid4
from dataclasses import dataclass, field
from social_engineering_simulator.domain.organizations.department.entity import Department
from social_engineering_simulator.domain.organizations.department.value_object import DepartmentName
from social_engineering_simulator.domain.organizations.exceptions import DuplicateDepartmentNameError,\
    DepartmentNotFoundError


@dataclass
class Organization:
    name: OrganizationName
    industry: IndustryType
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    id: UUID = field(default_factory=uuid4)
    _departments: list["Department"] = field(default_factory=list)

    def rename(self, new_name: OrganizationName) -> None:
        self.name = new_name

    def change_industry(self, new_industries: IndustryType) -> None:
        self.industry = new_industries

    def add_department(self, department: "Department") -> None:
        if self._find_by_name(department.name):
            raise DuplicateDepartmentNameError(f"department '{department.name}' already exists in this organization")
        self._departments.append(department)

    def remove_department(self, department_id: UUID) -> None:
        department = self._find_by_id(department_id)
        if not department:
            raise DepartmentNotFoundError(f"department '{department}' dont exists in this organization")
        self._departments.remove(department)

    def _find_by_name(self, name: DepartmentName) -> bool:
        return any(d.name == name for d in self._departments)

    def find_department(self, dep_uuid: UUID) -> "department | None":
        return self._find_by_id(dep_uuid)

    def _find_by_id(self, dep_uuid: UUID) -> "department | None":
        return next((d for d in self._departments if d.id == dep_uuid), None)
