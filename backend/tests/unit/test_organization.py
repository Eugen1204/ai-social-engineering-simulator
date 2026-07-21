from social_engineering_simulator.domain.organizations.department.value_object import DepartmentName
from social_engineering_simulator.domain.organizations.exceptions import DuplicateDepartmentNameError
from social_engineering_simulator.domain.organizations.department.exceptions import InvalidNameDepartmentError
import pytest


def test_add_department(organization, new_department):
    assert len(organization.get_departments()) == 0
    organization.add_department(new_department)
    assert len(organization.get_departments()) == 1
    assert organization.department_find_by_name(DepartmentName("IT")) is None


def test_duplicate(organization_with_department):
    from social_engineering_simulator.domain.organizations.department.entity import Department, DepartmentName
    duplicate = Department(name=DepartmentName("IT"))

    with pytest.raises(DuplicateDepartmentNameError):
        organization_with_department.add_department(duplicate)


def test_remove_department(organization_with_department):
    it_dept = organization_with_department.department_find_by_name(DepartmentName("IT"))
    assert it_dept is not None, "IT department should exist before deletion"

    organization_with_department.remove_department(it_dept.id)

    deleted_dept = organization_with_department.department_find_by_name(DepartmentName("IT"))
    assert deleted_dept is None, "IT department should be deleted"

    hr_dept = organization_with_department.department_find_by_name(DepartmentName("HR"))
    assert hr_dept is not None, "HR department should still exist"


def test_add_wrong_dep(organization):
    from social_engineering_simulator.domain.organizations.department.entity import DepartmentName, Department
    wrong_dept_name = "!±±!!±!±JN±@!@UO!@JDHB!UD#GD±!±!±!N±*!!U±BI±!"

    with pytest.raises(InvalidNameDepartmentError):
        department = Department(
            name=DepartmentName(wrong_dept_name))
        organization.add_department(department)