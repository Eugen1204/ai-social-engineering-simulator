from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from social_engineering_simulator.domain.organizations.department.employee.entity import Employee
from social_engineering_simulator.domain.organizations.department.entity import Department
from social_engineering_simulator.domain.organizations.entity import Organization
from social_engineering_simulator.domain.organizations.exceptions import EmployeeNotFoundError
from social_engineering_simulator.domain.organizations.repository import OrganizationRepository
from social_engineering_simulator.infrastructure.persistence.postgres.models import OrganizationModel, EmployeeModel, \
    DepartmentModel


class PostgresOrganizationRepository(OrganizationRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, organization: Organization) -> None:
        org_model = await self.session.get(OrganizationModel, organization.id)

        if org_model is None:
            org_model = OrganizationModel(id=organization.id)
            self.session.add(org_model)

        org_model.name = organization.name.value
        org_model.industry = organization.industry.value
        org_model.created_at = organization.created_at

        await self._sync_departments(org_model, organization.get_departments())

        await self._sync_employees(org_model, organization.employees)

    async def _sync_departments(self, org_model: OrganizationModel,
                                departments: tuple[Department]):

        stmt = select(DepartmentModel).where(DepartmentModel.organization_id == org_model.id)
        result = await self.session.execute(stmt)
        existing_dep_models = {m.id: m for m in result.scalars().all()}
        new_dep_ids = {d.id for d in departments}

        for dep in departments:
            if dep.id in existing_dep_models:
                existing_model = existing_dep_models[dep.id]
                existing_model.name = dep.name
                existing_model.created_at = dep.created_at
            else:
                dep_model = DepartmentModel(id=dep.id,
                                            name=dep.name,
                                            created_at=dep.created_at,
                                            organization_id=org_model.id)
                self.session.add(dep_model)

        for dep_id, dep_model in existing_dep_models.items():
            if dep_id not in new_dep_ids:
                await self.session.delete(dep_model)


    async def _sync_employees(self, org_model: OrganizationModel,
                              employees: tuple[UUID], organization: Organization) -> None:
        stmt = select(EmployeeModel).join(DepartmentModel).where(DepartmentModel.organization_id == org_model.id)
        result = await self.session.execute(stmt)
        existing_models = {m.id: m for m in result.scalars().all()}

        for emp_id in employees:
            if emp_id not in existing_models:
                emp = organization.get_employee(emp_id)
                if not emp:
                    raise EmployeeNotFoundError(f"Employee with {emp_id} not found")
                emp_model = EmployeeModel(
                    id=emp_id,
                    name=emp.id,
                    email=emp.email.value,
                    created_at=emp.created_at,
                    department=emp.department_id

    def get_by_id(self, organization_id: UUID) -> Organization | None:
        ...

    def delete(self, organization_id: UUID) -> None:
        ...

    def exists(self, organization_id: UUID) -> bool:
        ...

    def get_all_organization(self) -> tuple[Organization, ...]:
        ...
