from dataclasses import dataclass

from social_engineering_simulator.domain.organizations.campaign.exceptions import InvalidStateTransitionError
from social_engineering_simulator.domain.organizations.campaign.value_object import CampaignStatus


@dataclass(frozen=True)
class CampaignWorkflow:
    _matrix = {
        CampaignStatus.Draft: {
            "start": CampaignStatus.Running,
            "schedule": CampaignStatus.Scheduled,
        },
        CampaignStatus.Scheduled: {
            "draft": CampaignStatus.Draft,
            "cancel": CampaignStatus.Cancelled,
            "start": CampaignStatus.Running,
        },
        CampaignStatus.Running: {
            "cancel": CampaignStatus.Cancelled,
            "finish": CampaignStatus.Finished,
        },
        CampaignStatus.Finished: {
            "archive": CampaignStatus.Archived
        },
        CampaignStatus.Cancelled: {},
        CampaignStatus.Archived: {},
    }

    def get_next_status(self, current_status: CampaignStatus, action: str) -> CampaignStatus:
        next_status = self._matrix.get(current_status, {}).get(action)

        if not next_status:
            raise InvalidStateTransitionError(f"prohibited action '{action}' for status '{current_status}'")

        return next_status
