class CampaignNotFoundError(Exception):
    pass


class DifferentIdError(Exception):
    pass


class CampaignIsNotRunning(Exception):
    pass


class CampaignNotInThisOrganizationError(Exception):
    pass
