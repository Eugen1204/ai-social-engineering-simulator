class InvalidNameOrganizationError(Exception):
    """The name of the organization does not comply with the business rules"""
    pass


class DuplicateDepartmentNameError(Exception):
    """error adding department"""
    pass


class DuplicateEmailError(Exception):
    """email already exists"""
    pass


class DepartmentNotFoundError(Exception):
    """Error removing department"""
    pass


class DepartmentDelError(Exception):
    """Error removing department"""
    pass


class EmployeeAddError(Exception):
    """couldn't add employee"""
    pass


class EmployeeDeleteError(Exception):
    """couldn't delete employee"""
    pass


class ChangeDepartmentError(Exception):
    """It is impossible to change departments"""
    pass


class WrongIndustryError(Exception):
    """WRONG INDUSTRY"""
    pass

