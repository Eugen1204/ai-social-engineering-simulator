class InvalidNameOrganizationError(Exception):
    """The name of the organization does not comply with the business rules"""
    pass


class InvalidDescriptionsError(Exception):
    """Something is wrong with the description of the organization."""
    pass
