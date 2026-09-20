from datetime import datetime, UTC
from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from social_engineering_simulator.domain.organizations.department.employee.value_object import EmployeeName, Email
from social_engineering_simulator.domain.organizations.department.entity import Department
from social_engineering_simulator.domain.organizations.department.value_object import DepartmentName
from social_engineering_simulator.domain.organizations.entity import Organization
from social_engineering_simulator.domain.organizations.value_object import OrganizationName
from social_engineering_simulator.infrastructure.persistence.postgres.organization_repository import \
    PostgresOrganizationRepository


@pytest.mark.asyncio
async def test_organization_with_2_departments(organization: Organization,
                                               session: AsyncSession):
    repo = PostgresOrganizationRepository(session)
    dep_hr = Department(DepartmentName('HR'), created_at=datetime.now(UTC),
                        id=uuid4())

    dep_it = Department(DepartmentName('IT'), created_at=datetime.now(UTC),
                        id=uuid4())

    organization.add_department(dep_hr)
    organization.add_department(dep_it)

    await repo.save(organization)
    await session.commit()

    loaded_org = await repo.get_by_id(organization.id)
    assert len(loaded_org.get_departments()) == 2


@pytest.mark.asyncio
async def test_organization_with_changed_employees(organization: Organization,
                                               session: AsyncSession):
    repo = PostgresOrganizationRepository(session)
    dep_hr = Department(DepartmentName('HR'), created_at=datetime.now(UTC),
                        id=uuid4())
    dep_it = Department(DepartmentName('IT'), created_at=datetime.now(UTC),
                        id=uuid4())

    organization.add_department(dep_hr)
    organization.add_department(dep_it)

    emp = organization.add_employee(name=EmployeeName("Test Aa"),
                                    email=Email("email1@gmail.com"),
                                    dep_name=DepartmentName('HR'))

    assert dep_hr.get_employee_ids() is not None
    await repo.save(organization)
    await session.commit()

    loaded_org = await repo.get_by_id(organization.id)

    loaded_emp = loaded_org.get_employee(emp.id)
    assert loaded_emp is not None
    assert loaded_emp.email == Email("email1@gmail.com")
    assert loaded_emp.department_id == dep_hr.id
    assert loaded_emp.name == EmployeeName("Test Aa")
    assert loaded_emp.created_at == emp.created_at

    organization.change_department(emp.id, dep_it.id)

    organization.rename(new_name=OrganizationName('New Name'))
    emp = organization.get_employee(emp.id)
    emp.email = Email('new_email@nana.com')
    emp.name = EmployeeName('New Name')

    await repo.save(organization)
    await session.commit()

    changed_loaded_org = await repo.get_by_id(organization.id)
    changed_emp = changed_loaded_org.get_employee(emp.id)

    assert changed_loaded_org.name == OrganizationName('New Name')
    assert changed_emp.name == EmployeeName('New Name')
    assert changed_emp.department_id == dep_it.id
    assert changed_emp.email == Email('new_email@nana.com')
    assert not changed_loaded_org.department_find_by_name(DepartmentName('HR')).has_employees()

