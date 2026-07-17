from dataclasses import dataclass
from social_engineering_simulator.domain.organizations.department.exceptions import InvalidNameDepartmentError
import re


@dataclass(frozen=True)
class DepartmentName:
    value: str

    def __post_init__(self):
        DepartmentName._validate_name(self.value)

    @staticmethod
    def _validate_name(name: str) -> None:
        if not name or not name.strip():
            raise InvalidNameDepartmentError("The name cannot be empty.")
        if len(name) < 1:
            raise InvalidNameDepartmentError("Name must be at least 2 characters long.")
        if len(name) > 100:
            raise InvalidNameDepartmentError("Name cannot exceed 100 characters.")
        allowed_pattern = r'^[a-zA-Zа-яА-Я0-9 \-.&#]+$'
        if not re.fullmatch(allowed_pattern, name):
            raise InvalidNameDepartmentError(f"Organization name '{name}' contains invalid characters.")