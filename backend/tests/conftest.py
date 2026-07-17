import pytest
from social_engineering_simulator.domain.organizations.entity import OrganizationName, Organization, IndustryType,\
    Department, DepartmentName
from uuid import uuid4


@pytest.fixture()
def org_name():
    return OrganizationName("TestOrg")


@pytest.fixture()
def organization(org_name):
    return Organization(
        name=org_name,
        industry=IndustryType.IT_COMPANY
    )


@pytest.fixture()
def department():
    return Department(
        name=DepartmentName("HR"),
        organization_id=uuid4()
    )


@pytest.fixture()
def organization_with_department(organization):
    dept1 = Department(name=DepartmentName("IT"),
                       organization_id=organization.id)
    dept2 = Department(name=DepartmentName("HR"),
                       organization_id=organization.id)

    organization.add_department(dept1)
    organization.add_department(dept2)

    return organization





