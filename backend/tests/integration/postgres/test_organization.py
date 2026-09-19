from datetime import datetime, UTC
from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from social_engineering_simulator.domain.organizations.department.employee.entity import Employee
from social_engineering_simulator.domain.organizations.department.employee.value_object import EmployeeName, Email
from social_engineering_simulator.domain.organizations.department.entity import Department
from social_engineering_simulator.domain.organizations.department.value_object import DepartmentName
from social_engineering_simulator.domain.organizations.entity import Organization
from social_engineering_simulator.domain.organizations.exceptions import DepartmentDelError
from social_engineering_simulator.domain.organizations.value_object import OrganizationName, IndustryType
from social_engineering_simulator.infrastructure.persistence.postgres.organization_repository import \
    PostgresOrganizationRepository


@pytest.mark.asyncio
async def test_save_and_get_organization(session: AsyncSession):
    repo = PostgresOrganizationRepository(session)

    org = Organization(name=OrganizationName('Test Organization'),
                       industry=IndustryType.IT_COMPANY,
                       created_at=datetime.now(UTC))

    await repo.save(org)
    await session.commit()

    loaded_org = await repo.get_by_id(org.id)

    assert loaded_org.id == org.id


@pytest.mark.asyncio
async def test_save_and_get_organization(session: AsyncSession):
    repo = PostgresOrganizationRepository(session)

    org = Organization(name=OrganizationName('Test Organization'),
                       industry=IndustryType.IT_COMPANY,
                       created_at=datetime.now(UTC))

    org.add_department(Department(name=DepartmentName('HR'),
                                  created_at=datetime.now(UTC)))

    org.add_employee(name=EmployeeName('John Dow'),
                     email=Email('testtest@test.com'),
                     dep_name=DepartmentName('HR'))

    emp = org.get_employees()[0]

    await repo.save(org)
    await session.commit()

    loaded_org = await repo.get_by_id(org.id)

    assert loaded_org.industry == IndustryType.IT_COMPANY
    assert emp.id in loaded_org.employees
    assert loaded_org.name == org.name

    print(loaded_org.get_departments())
    print(org.get_departments())
    assert loaded_org.get_departments() == org.get_departments()
    assert loaded_org.created_at == org.created_at


@pytest.mark.asyncio
async def test_update_organization(session: AsyncSession):
    repo = PostgresOrganizationRepository(session)

    org = Organization(
        id=uuid4(),
        name=OrganizationName("Test"),
        industry=IndustryType.IT_COMPANY,
        created_at=datetime.now(UTC)
    )

    await repo.save(org)
    await session.commit()

    org.change_industry(new_industries=IndustryType.ENERGY)
    await repo.save(org)
    await session.commit()

    loaded_org = await repo.get_by_id(org.id)

    assert loaded_org.industry == IndustryType.ENERGY


@pytest.mark.asyncio
async def test_delete_organization(session: AsyncSession):
    repo = PostgresOrganizationRepository(session)

    org = Organization(
        id=uuid4(),
        name=OrganizationName("Test"),
        industry=IndustryType.IT_COMPANY,
        created_at=datetime.now(UTC)
    )

    await repo.save(org)
    await session.commit()

    await repo.delete(org.id)
    await session.commit()

    loaded_org = await repo.get_by_id(org.id)

    assert loaded_org is None

    not_found_org = await repo.get_by_id(uuid4())

    assert not_found_org is None


@pytest.mark.asyncio
async def test_same_uuid_org(session: AsyncSession):
    repo = PostgresOrganizationRepository(session)

    original_uuid = uuid4()
    org = Organization(
        id=original_uuid,
        name=OrganizationName("Test"),
        industry=IndustryType.IT_COMPANY,
        created_at=datetime.now(UTC)
    )

    await repo.save(org)
    await session.commit()

    loaded_org = await repo.get_by_id(org.id)

    assert loaded_org.id == original_uuid


@pytest.mark.asyncio
async def test_delete_dep_with_emp(session: AsyncSession):
    repo = PostgresOrganizationRepository(session)

    org = Organization(
        id=uuid4(),
        name=OrganizationName("Test"),
        industry=IndustryType.IT_COMPANY,
        created_at=datetime.now(UTC)
    )

    dep_hr = Department(DepartmentName('HR'), created_at=datetime.now(UTC),
                        id=uuid4())

    dep_it = Department(DepartmentName('IT'), created_at=datetime.now(UTC),
                        id=uuid4())

    org.add_department(dep_hr)
    org.add_department(dep_it)

    emp_hr = org.add_employee(name=EmployeeName('Test eeffee'),
                              email=Email('evvweefc@dfef.efcd'),
                              dep_name=DepartmentName('HR'))

    emp_it = org.add_employee(name=EmployeeName('Tesft Deffee'),
                              email=Email('evvweecefc@dfef.efcd'),
                              dep_name=DepartmentName('IT'))

    await repo.save(org)
    await session.commit()

    loaded_org = await repo.get_by_id(org.id)
    assert len(loaded_org.get_departments()) == 2
    assert emp_hr.department_id == dep_hr.id
    assert emp_it.department_id == dep_it.id
    print(loaded_org.department_find_by_name(DepartmentName('HR')))
    assert loaded_org.department_find_by_name(DepartmentName('HR')).get_employee_ids() is not None

    with pytest.raises(DepartmentDelError):
        org.remove_department(dep_hr.id)
    org.remove_employee(emp_hr.id)
    org.remove_department(dep_hr.id)

    await repo.save(org)
    await session.commit()

    loaded_org_without_hr = await repo.get_by_id(org.id)
    assert len(loaded_org_without_hr.get_departments()) == 1
    assert loaded_org_without_hr.department_find_by_name(DepartmentName('HR')) is None
    assert loaded_org_without_hr.department_find_by_name(DepartmentName('IT')).id == dep_it.id
    assert loaded_org_without_hr.get_employee(emp_hr.id) is None
    assert loaded_org_without_hr.get_employee(emp_it.id).id == emp_it.id
