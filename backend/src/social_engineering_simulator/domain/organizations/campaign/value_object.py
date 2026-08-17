import re
from dataclasses import dataclass, field
from enum import Enum

from social_engineering_simulator.domain.organizations.campaign.exceptions import InvalidNameCampaignError, \
    WrongCampaignStatus, InvalidStateTransitionError


@dataclass(frozen=True)
class CampaignName:
    value: str

    def __post_init__(self):
        CampaignName._validate_name(self.value)

    @staticmethod
    def _validate_name(name: str) -> None:
        if not name or not name.strip():
            raise InvalidNameCampaignError("The name cannot be empty.")
        if len(name) < 2:
            raise InvalidNameCampaignError("Name must be at least 2 characters long.")
        if len(name) > 100:
            raise InvalidNameCampaignError("Name cannot exceed 100 characters.")
        allowed_pattern = r'^[a-zA-Zа-яА-Я0-9 \-.&#]+$'
        if not re.fullmatch(allowed_pattern, name):
            raise InvalidNameCampaignError(f"Organization name '{name}' contains invalid characters.")


class CampaignStatus(Enum):
    Draft = "Draft"
    Scheduled = "Scheduled"
    Running = "Running"
    Finished = "Finished"
    Cancelled = "Cancelled"
    Archived = "Archived"

    @classmethod
    def from_str(cls, value: str) -> "CampaignStatus":
        try:
            return cls(value)
        except ValueError:
            raise WrongCampaignStatus("Campaign status not found")



