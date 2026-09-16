from typing import cast
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from social_engineering_simulator.domain.organizations.department.employee.entity import Employee
from social_engineering_simulator.domain.organizations.department.entity import Department
from social_engineering_simulator.domain.organizations.entity import Organization
from social_engineering_simulator.domain.organizations.repository import AsyncOrganizationRepository
from social_engineering_simulator.infrastructure.persistence.postgres.mappers import OrganizationMapper,\
    EmployeeMapper, DepartmentMapper
from social_engineering_simulator.infrastructure.persistence.postgres.models import OrganizationModel, EmployeeModel, \
    DepartmentModel


class PostgresOrganizationRepository(AsyncOrganizationRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, organization: Organization) -> None:
        result = await self.session.execute(
            select(OrganizationModel).where(OrganizationModel.id == organization.id)
        )
        org_model = result.scalar_one_or_none()

        if org_model is None:
            org_model = OrganizationMapper.to_model(organization)
            self.session.add(org_model)
        else:
            org_model = OrganizationMapper.to_model(organization=organization, existing_org_model=org_model)

        await self._sync_departments(org_model, organization.get_departments())

        await self._sync_employees(org_model, organization.get_employees())

    async def _sync_departments(self, org_model: OrganizationModel,
                                departments: tuple[Department]):

        stmt = select(DepartmentModel).where(DepartmentModel.organization_id == org_model.id)
        result = await self.session.execute(stmt)
        existing_dep_models = {m.id: m for m in result.scalars().all()}
        new_dep_ids = {d.id for d in departments}
        for dep_id, dep_model in existing_dep_models.items():
            if dep_id not in new_dep_ids:
                await self.session.delete(dep_model)

        for dep in departments:
            if dep.id in existing_dep_models:
                existing_model = existing_dep_models[dep.id]
                existing_model.name = dep.name.value
            else:
                dep_model = DepartmentMapper.to_model(dep, org_model.id)
                self.session.add(dep_model)

    async def _sync_employees(self, org_model: OrganizationModel,
                              employees: tuple[Employee]) -> None:
        stmt = select(EmployeeModel).join(DepartmentModel).where(DepartmentModel.organization_id == org_model.id)
        result = await self.session.execute(stmt)
        existing_emp_models = {m.id: m for m in result.scalars().all()}
        new_emp_ids = {e.id for e in employees}
        for emp_m_id, emp_m in existing_emp_models.items():
            if emp_m_id not in new_emp_ids:
                await self.session.delete(emp_m)

        for emp in employees:
            if emp.id in existing_emp_models:
                existing_model = existing_emp_models[emp.id]
                existing_model.name = emp.name.value
                existing_model.email = emp.email.value
                existing_model.department_id = emp.department_id
            else:
                emp_model = EmployeeMapper.to_model(emp)

                self.session.add(emp_model)

    async def get_by_id(self, organization_id: UUID) -> Organization | None:
        stmt = select(OrganizationModel) \
            .options(selectinload(OrganizationModel.departments)
                     .selectinload(DepartmentModel.employees)) \
            .where(OrganizationModel.id == organization_id)
        result = await self.session.execute(stmt)

        org_model = cast(
            OrganizationModel | None,
            result.scalars().unique().one_or_none()
        )
        if org_model is None:
            return None

        return OrganizationMapper.to_domain(org_model)

    async def delete(self, organization_id: UUID) -> None:
        stmt = select(OrganizationModel) \
            .where(OrganizationModel.id == organization_id)
        result = await self.session.execute(stmt)

        org_model = result.scalars().one_or_none()
        if org_model is None:
            return

        await self.session.delete(org_model)

    async def exists(self, organization_id: UUID) -> bool:
        stmt = (select(OrganizationModel.id)
                .where(OrganizationModel.id == organization_id))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def get_all_organizations(self) -> tuple[Organization, ...]:
        stmt = (select(OrganizationModel).options(selectinload(OrganizationModel.departments)
                .selectinload(DepartmentModel.employees)))

        result = await self.session.execute(stmt)

        org_models = result.scalars().unique().all()
        orgs: list[Organization] = []
        for org_model in org_models:
            org = OrganizationMapper.to_domain(org_model)
            orgs.append(org)

        return tuple(orgs)
