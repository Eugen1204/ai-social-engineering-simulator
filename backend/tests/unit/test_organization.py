from uuid import uuid4
from social_engineering_simulator.domain.organizations.exceptions import DuplicateDepartmentNameError, \
    InvalidNameOrganizationError
from social_engineering_simulator.domain.organizations.Department.exceptions import InvalidNameDepartmentError
import pytest


def test_add_department(organization, department):
    organization.add_department(department)
    assert len(organization.get_departments()) == 1
    assert department.organization_id == organization.id


def test_duplicate(organization_with_department, department):
    from social_engineering_simulator.domain.organizations.Department.entity import Department, DepartmentName
    duplicate = Department(name=DepartmentName("IT"),
                           organization_id=organization_with_department.id)

    with pytest.raises(DuplicateDepartmentNameError):
        organization_with_department.add_department(duplicate)


def test_remove_department(organization_with_department):
    departments = organization_with_department.get_departments()
    dept_id = departments[0].id
    organization_with_department.remove_department(department_id=dept_id)

    assert len(organization_with_department.get_departments()) == 1


def test_add_wrong_dep(organization):
    from social_engineering_simulator.domain.organizations.Department.entity import DepartmentName, Department
    wrong_dept_name = "!±±!!±!±JN±@!@UO!@JDHB!UD#GD±!±!±!N±*!!U±BI±!"

    with pytest.raises(InvalidNameDepartmentError):
        department = Department(
            name=DepartmentName(wrong_dept_name),
            organization_id=organization.id
        )
        organization.add_department(department)

