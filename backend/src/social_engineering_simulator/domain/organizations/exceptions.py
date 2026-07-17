class InvalidNameOrganizationError(Exception):
    """The name of the organization does not comply with the business rules"""
    pass


class DuplicateDepartmentNameError(Exception):
    """error adding department"""
    pass


class DepartmentNotFoundError(Exception):
    """Error removing department"""
    pass
