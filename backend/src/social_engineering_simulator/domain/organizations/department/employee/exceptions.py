class InvalidNameEmployeeError(Exception):
    """The name of the organization does not comply with the business rules"""
    pass


class InvalidEmailError(Exception):
    """Something's wrong with e-maile."""
    pass
