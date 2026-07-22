from enum import Enum
from dataclasses import dataclass
from social_engineering_simulator.domain.organizations.exceptions import InvalidNameOrganizationError
import re
from social_engineering_simulator.domain.organizations.exceptions import WrongIndustryError


class IndustryType(Enum):
    IT_COMPANY = "IT Company"
    BANKING = "Bank"
    FINANCE = "Financial Services"
    RETAIL = "Retail"
    HEALTHCARE = "Healthcare"
    EDUCATION = "Education"
    TELECOM = "Telecommunications"
    ENERGY = "Energy"
    MANUFACTURING = "Manufacturing"
    TRANSPORT = "Transport & Logistics"
    CONSTRUCTION = "Construction"
    AGRICULTURE = "Agriculture"
    HOSPITALITY = "Hospitality"
    MEDIA = "Media"
    GOVERNMENT = "Government"
    NGO = "Non-Profit"
    CONSULTING = "Consulting"
    INSURANCE = "Insurance"
    REAL_ESTATE = "Real Estate"
    ENTERTAINMENT = "Entertainment"

    @classmethod
    def from_str(cls, value: str) -> "IndustryType":
        try:
            return cls(value)
        except ValueError:
            raise WrongIndustryError("Industry not found")


@dataclass(frozen=True)
class OrganizationName:
    value: str

    def __post_init__(self):
        OrganizationName._validate_name(self.value)

    @staticmethod
    def _validate_name(name: str) -> None:
        if not name or not name.strip():
            raise InvalidNameOrganizationError("The name cannot be empty.")
        if len(name) < 2:
            raise InvalidNameOrganizationError("Name must be at least 2 characters long.")
        if len(name) > 100:
            raise InvalidNameOrganizationError("Name cannot exceed 100 characters.")
        allowed_pattern = r'^[a-zA-Zа-яА-Я0-9 \-.&#]+$'
        if not re.fullmatch(allowed_pattern, name):
            raise InvalidNameOrganizationError(f"Organization name '{name}' contains invalid characters.")
