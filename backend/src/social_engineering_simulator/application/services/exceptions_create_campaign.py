class CampaignNotFoundError(Exception):
    pass


class DifferentIdError(Exception):
    pass


class CampaignIsNotRunningError(Exception):
    pass


class CampaignNotInThisOrganizationError(Exception):
    pass


class EmployeeNotInCampaignError(Exception):
    pass


class TemplateWasNotSentError(Exception):
    pass


class TemplateAlreadyOpenedError(Exception):
    pass

