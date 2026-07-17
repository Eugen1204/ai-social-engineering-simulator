class InvalidNameDepartmentError(Exception):
    """The name of the organization does not comply with the business rules"""
    pass


class InvalidOrganizationIdError(Exception):
    """Error with the organization id"""
    pass
