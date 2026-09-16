from datetime import UTC
from uuid import UUID

from social_engineering_simulator.domain.organizations.department.employee.entity import Employee
from social_engineering_simulator.domain.organizations.department.employee.value_object import EmployeeName, Email
from social_engineering_simulator.domain.organizations.department.entity import Department
from social_engineering_simulator.domain.organizations.department.value_object import DepartmentName
from social_engineering_simulator.domain.organizations.entity import Organization
from social_engineering_simulator.domain.organizations.value_object import OrganizationName, IndustryType
from social_engineering_simulator.infrastructure.persistence.postgres.models import OrganizationModel, DepartmentModel, \
    EmployeeModel


class OrganizationMapper:
    @staticmethod
    def to_domain(org_model: OrganizationModel) -> Organization:
        org = Organization(id=org_model.id,
                           name=OrganizationName(org_model.name),
                           industry=IndustryType(org_model.industry),
                           created_at=org_model.created_at.astimezone(UTC),
                           )

        for dep in org_model.departments:
            department = Department(name=DepartmentName(dep.name),
                                    created_at=dep.created_at.astimezone(UTC),
                                    id=dep.id)
            org.add_department(department)

            for emp in dep.employees:
                employee = Employee(name=EmployeeName(emp.name),
                                    email=Email(emp.email),
                                    department_id=emp.department_id,
                                    created_at=emp.created_at.astimezone(UTC),
                                    id=emp.id)
                org.add_existing_employee(employee)

        return org

    @staticmethod
    def to_model(organization: Organization, existing_org_model: OrganizationModel | None = None) -> OrganizationModel:
        if existing_org_model is None:
            model = OrganizationModel(id=organization.id,
                                      created_at=organization.created_at)
        else:
            model = existing_org_model

        model.name = organization.name.value
        model.industry = organization.industry.value

        return model


class DepartmentMapper:
    @staticmethod
    def to_domain(dep_model: DepartmentModel) -> Department:
        return Department(name=DepartmentName(dep_model.name),
                          created_at=dep_model.created_at.astimezone(UTC),
                          id=dep_model.id,
                          )

    @staticmethod
    def to_model(dep: Department, organization_id: UUID) -> DepartmentModel:
        return DepartmentModel(id=dep.id,
                               created_at=dep.created_at,
                               name=dep.name.value,
                               organization_id=organization_id)


class EmployeeMapper:
    @staticmethod
    def to_domain(emp_model: EmployeeModel) -> Employee:
        return Employee(name=EmployeeName(emp_model.name),
                        created_at=emp_model.created_at.astimezone(UTC),
                        id=emp_model.id,
                        email=Email(emp_model.email),
                        department_id=emp_model.department_id
                        )

    @staticmethod
    def to_model(emp: Employee) -> EmployeeModel:
        return EmployeeModel(id=emp.id,
                             created_at=emp.created_at,
                             name=emp.name.value,
                             department_id=emp.department_id,
                             email=emp.email.value)
