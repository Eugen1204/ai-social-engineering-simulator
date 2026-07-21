from datetime import datetime, UTC

from social_engineering_simulator.domain.organizations.value_object import IndustryType, OrganizationName
from uuid import UUID, uuid4
from dataclasses import dataclass, field
from social_engineering_simulator.domain.organizations.department.entity import Department
from social_engineering_simulator.domain.organizations.department.value_object import DepartmentName
from social_engineering_simulator.domain.organizations.exceptions import DuplicateDepartmentNameError, \
    DepartmentNotFoundError, EmployeeAddError, ChangeDepartmentError, DepartmentDelError, EmployeeDeleteError, \
    DuplicateEmailError
from social_engineering_simulator.domain.organizations.department.employee.value_object import Email, EmployeeName
from social_engineering_simulator.domain.organizations.department.employee.entity import Employee


@dataclass
class Organization:
    name: OrganizationName
    industry: IndustryType
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    id: UUID = field(default_factory=uuid4)
    _departments_names: dict[DepartmentName, UUID] = field(default_factory=dict)
    _departments: dict[UUID, "Department"] = field(default_factory=dict)
    _emails: set["Email"] = field(default_factory=set)
    _employees: dict[UUID, "Employee"] = field(default_factory=dict)

    def rename(self, new_name: OrganizationName) -> None:
        self.name = new_name

    def change_industry(self, new_industries: IndustryType) -> None:
        self.industry = new_industries

    def add_department(self, department: "Department") -> None:
        if department.name in self._departments_names:
            raise DuplicateDepartmentNameError(f"Department '{department.name}' already exists in this organization")
        self._departments[department.id] = department
        self._departments_names[department.name] = department.id

    def remove_department(self, department_id: UUID) -> None:
        department = self._departments.get(department_id)
        if not department:
            raise DepartmentNotFoundError(f"Department '{department_id}' dont exists in this organization")
        if department.has_employees():
            raise DepartmentDelError("You can't delete a department that has employees")
        del self._departments[department_id]
        del self._departments_names[department.name]

    def department_find_by_name(self, dept_name: DepartmentName) -> "Department | None":
        dept_id = self._departments_names.get(dept_name)
        if dept_id is None:
            return None
        return self._departments.get(dept_id)

    @property
    def emails(self) -> tuple[Email, ...]:
        return tuple(self._emails)

    def add_employee(self, name: EmployeeName, email: Email, dep_name: DepartmentName) -> Employee:
        department = self.department_find_by_name(dep_name)
        if not department:
            raise EmployeeAddError(f"Department '{dep_name}' not found")

        employee = Employee(name=name,
                            email=email,
                            department_id=department.id)

        if employee.id in self._employees:
            raise EmployeeAddError(f"Employee {employee.id} already exists")

        if email in self._emails:
            raise DuplicateEmailError(f"Email '{email.value}' already exists in this organization")

        self._employees[employee.id] = employee
        department.add_employee_id(employee.id)
        self._emails.add(email)

        return employee

    def remove_employee(self, employee_id: UUID):
        employee = self._employees.get(employee_id)
        if not employee:
            raise EmployeeDeleteError(f"Employee {employee_id} does not exist in the organization")
        dep_employee = self._departments.get(employee.department_id)
        if dep_employee:
            dep_employee.remove_employee_id(employee.id)

        del self._employees[employee.id]
        self._emails.remove(employee.email)

    def change_department(self, employee_id: UUID, department_id: UUID) -> None:
        employee = self._employees.get(employee_id)
        if employee is None:
            raise ChangeDepartmentError("Employee does not exist")
        department = self._departments.get(department_id)
        if department is None:
            raise ChangeDepartmentError("Department does not exist")
        if employee.department_id == department.id:
            raise ChangeDepartmentError("This employee is already in this department.")
        if department.id not in self._departments:
            raise ChangeDepartmentError("This department does not exist")
        if employee.id not in self._employees:
            raise ChangeDepartmentError("Employee does not belong to this organization")
        if employee.department_id is None:
            raise ChangeDepartmentError("Employee is not assigned to any department")
        old_department = self._departments.get(employee.department_id)
        if old_department:
            old_department.remove_employee_id(employee.id)

        employee.department_id = department.id
        department.add_employee_id(employee.id)

    @property
    def employees(self) -> tuple[UUID, ...]:
        return tuple(self._employees)

    def get_departments(self) -> tuple[Department, ...]:
        return tuple(self._departments.values())

    def get_employees(self) -> tuple[Employee, ...]:
        return tuple(self._employees.values())

