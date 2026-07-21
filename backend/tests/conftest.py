import pytest
from social_engineering_simulator.domain.organizations.entity import OrganizationName, Organization, IndustryType,\
    Department, DepartmentName
from social_engineering_simulator.domain.organizations.department.employee.entity import Employee, EmployeeName,\
    Email


@pytest.fixture()
def org_name():
    return OrganizationName("TestOrg")

@pytest.fixture()
def employee_name() -> EmployeeName:
    return EmployeeName("Test Test")

@pytest.fixture()
def employee_email() -> Email:
    return Email("dociwcew@skdwo.com")


@pytest.fixture()
def organization(org_name):
    return Organization(
        name=org_name,
        industry=IndustryType.IT_COMPANY
    )


@pytest.fixture()
def new_department() -> Department:
    return Department(name=DepartmentName("New dep"))

@pytest.fixture()
def organization_with_department(organization) -> Organization:
    dept1 = Department(name=DepartmentName("IT"))
    dept2 = Department(name=DepartmentName("HR"))

    organization.add_department(dept1)
    organization.add_department(dept2)

    return organization


@pytest.fixture()
def hr_department(organization_with_department) -> Department:
    dept = organization_with_department.department_find_by_name(DepartmentName("HR"))
    assert dept is not None, "HR department not found"
    return dept

@pytest.fixture()
def it_department(organization_with_department) -> Department:
    dept = organization_with_department.department_find_by_name(DepartmentName("IT"))
    assert dept is not None, "IT department not found"
    return dept


@pytest.fixture()
def employee(employee_name, employee_email, it_department) -> Employee:
    return Employee(name=employee_name,
                    email=employee_email,
                    department_id=it_department.id)

@pytest.fixture()
def organization_with_employee(organization_with_department, employee, it_department) -> Organization:
    new_employee = organization_with_department.add_employee(name=employee.name,
                                              email=employee.email,
                                              dep_name=DepartmentName("IT"))

    employee.id = new_employee.id

    return organization_with_department



