from uuid import UUID

from social_engineering_simulator.application.dto.create_organization import CreateOrganizationRequest, \
    OrganizationResponse
from social_engineering_simulator.domain.organizations.entity import Organization, OrganizationName
from social_engineering_simulator.domain.organizations.repository import OrganizationRepository
from social_engineering_simulator.domain.organizations.value_object import IndustryType
from social_engineering_simulator.domain.organizations.department.entity import Department, DepartmentName
from social_engineering_simulator.application.services.exception_create_organization import DuplicateDepartmentsError, \
    OrganizationNotFoundError
from functools import lru_cache


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
