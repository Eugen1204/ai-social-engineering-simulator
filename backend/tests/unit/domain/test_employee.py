from uuid import uuid4

import pytest
from social_engineering_simulator.domain.organizations.department.entity import DepartmentName
from social_engineering_simulator.domain.organizations.exceptions import EmployeeAddError, ChangeDepartmentError
from social_engineering_simulator.domain.organizations.department.employee.value_object import Email
from social_engineering_simulator.domain.organizations.department.employee.exceptions import InvalidEmailError
from social_engineering_simulator.domain.organizations.exceptions import DuplicateEmailError
from social_engineering_simulator.domain.organizations.department.employee.entity import Employee


def test_add_employee(organization_with_department, employee_name, employee_email):
    org = organization_with_department
    new_employee = org.add_employee(name=employee_name,
                                    email=employee_email,
                                    dep_name=DepartmentName("IT"))

    assert new_employee.id in org.employees

    it_dept = org.department_find_by_name(DepartmentName("IT"))
    assert new_employee.id in it_dept.get_employee_ids()

    assert new_employee.department_id == it_dept.id

    assert new_employee.name == employee_name

    assert new_employee.email == employee_email


def test_add_employee_duplicate(organization_with_department, employee_name, employee_email):
    org = organization_with_department

    org.add_employee(name=employee_name,
                     email=employee_email,
                     dep_name=DepartmentName("IT"))

    with pytest.raises(DuplicateEmailError) as exc_info:
        org.add_employee(name=employee_name,
                         email=employee_email,
                         dep_name=DepartmentName("IT"))

    assert "already exists" in str(exc_info.value)


def test_add_invalid_email(organization_with_department, employee_name):
    with pytest.raises(InvalidEmailError):
        org = organization_with_department
        org.add_employee(name=employee_name,
                         email=Email("sdkcccwe!@!"),
                         dep_name=DepartmentName("HR"))


def test_add_duplicate_email(organization_with_employee, employee_name, employee_email):
    with pytest.raises(DuplicateEmailError) as exc_info:
        org = organization_with_employee
        org.add_employee(name=employee_name,
                         email=employee_email,
                         dep_name=DepartmentName("HR")
                         )
    assert "already exist" in str(exc_info.value)


def test_move_emp_between_dep(organization_with_employee):
    org = organization_with_employee
    employee = next(iter(org._employees.values()))
    org.change_department(employee_id=employee.id, department_id=org.department_find_by_name(DepartmentName("HR")).id)
    hr_dept = org.department_find_by_name(DepartmentName("HR"))

    assert employee.department_id == hr_dept.id

    it_dept = org.department_find_by_name(DepartmentName("IT"))
    assert employee.department_id != it_dept.id


def test_wrong_move_emp_between_dep(organization_with_employee, employee):
    org = organization_with_employee
    non_existent_dep = org.department_find_by_name(DepartmentName("NonExistentDept"))
    assert non_existent_dep is None
    randon_uuid = uuid4()

    with pytest.raises(ChangeDepartmentError) as exc_info:
        org.change_department(employee_id=employee.id,
                              department_id=randon_uuid)

    assert "does not exist" in str(exc_info.value)









