from dataclasses import dataclass
from social_engineering_simulator.application.dto.create_organization import CreateOrganizationRequest, \
    OrganizationResponse
from social_engineering_simulator.domain.organizations.entity import Organization, OrganizationName
from social_engineering_simulator.domain.organizations.value_object import IndustryType
from social_engineering_simulator.domain.organizations.department.entity import Department, DepartmentName
from social_engineering_simulator.application.services.exception_create_organization import DuplicateDepartmentsError


class CreateOrganizationService:
    def execute(self, request: CreateOrganizationRequest):
        name = OrganizationName(request.name)
        industry = IndustryType.from_str(request.industry)

        org = Organization(name=name, industry=industry)

        if len(set(request.departments)) != len(request.departments):
            raise DuplicateDepartmentsError("Departments has duplicate")

        for department_name in request.departments:
            department = Department(name=DepartmentName(department_name))
            org.add_department(department=department)

        return OrganizationResponse(id=org.id,
                                    name=org.name.value,
                                    industry=org.industry.value,
                                    departments_count=len(org.get_departments()),
                                    )









