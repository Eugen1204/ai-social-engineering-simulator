from uuid import UUID

from social_engineering_simulator.application.dto.create_organization import CreateOrganizationRequest, \
    OrganizationResponse, EmployeeRequest, EmployeeResponse
from social_engineering_simulator.domain.organizations.department.employee.value_object import EmployeeName, Email
from social_engineering_simulator.domain.organizations.entity import Organization, OrganizationName
from social_engineering_simulator.domain.organizations.exceptions import EmployeeNotFoundError, \
    OrganizationNotFoundError
from social_engineering_simulator.domain.organizations.repository import OrganizationRepository
from social_engineering_simulator.domain.organizations.value_object import IndustryType
from social_engineering_simulator.domain.organizations.department.entity import Department, DepartmentName
from social_engineering_simulator.application.services.exception_create_organization import DuplicateDepartmentsError


class CreateOrganizationService:
    def __init__(self, repo: OrganizationRepository):
        self.repo = repo

    def execute(self, request: CreateOrganizationRequest) -> OrganizationResponse:
        name = OrganizationName(request.name)
        industry = IndustryType.from_str(request.industry)

        org = Organization(name=name, industry=industry)

        if len(set(request.departments)) != len(request.departments):
            raise DuplicateDepartmentsError("Departments has duplicate")

        for department_name in request.departments:
            department = Department(name=DepartmentName(department_name))
            org.add_department(department=department)

        self.repo.save(org)

        return OrganizationResponse(id=org.id,
                                    name=org.name.value,
                                    industry=org.industry.value,
                                    count_departments=len(org.get_departments()))


class GetOrganizationService:
    def __init__(self, repo: OrganizationRepository):
        self.repo = repo

    def execute(self, organization_id: UUID) -> OrganizationResponse:
        org = self.repo.get_by_id(organization_id)
        if org is None:
            raise OrganizationNotFoundError(f"Organization with {organization_id} not found")

        return OrganizationResponse(id=org.id,
                                    name=org.name.value,
                                    industry=org.industry.value,
                                    count_departments=len(org.get_departments()))


class AddEmployeeInOrganization:
    def __init__(self, repo: OrganizationRepository):
        self.repo = repo

    def execute(self, request: EmployeeRequest) -> EmployeeResponse:
        org = self.repo.get_by_id(request.org_id)
        if org is None:
            raise OrganizationNotFoundError(f"Organization with {request.org_id} not found")
        emp = org.add_employee(name=EmployeeName(request.name),
                               email=Email(request.email),
                               dep_name=DepartmentName(request.dep_name))

        self.repo.save(org)

        return EmployeeResponse(id=emp.id, name=emp.name.value, email=emp.email.value, org_id=org.id)


class GetEmployeeInOrganization:
    def __init__(self, repo: OrganizationRepository):
        self.repo = repo

    def execute(self, employee_id: UUID, org_id: UUID) -> EmployeeResponse:
        org = self.repo.get_by_id(org_id)
        if org is None:
            raise OrganizationNotFoundError(f"Organization with {org_id} not found")

        emp = org.get_employee(employee_id)
        if emp is None:
            raise EmployeeNotFoundError(f"Employee with {employee_id} not found")

        return EmployeeResponse(id=emp.id, name=emp.name.value, email=emp.email.value, org_id=org_id)
