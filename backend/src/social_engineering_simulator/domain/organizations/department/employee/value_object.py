from dataclasses import dataclass
from social_engineering_simulator.domain.organizations.department.employee.exceptions import InvalidNameEmployeeError, \
    InvalidEmailError
import re


@dataclass(frozen=True)
class EmployeeName:
    value: str

    def __post_init__(self):
        EmployeeName._validate_name(self.value)

    @staticmethod
    def _validate_name(name: str) -> None:
        if not name or not name.strip():
            raise InvalidNameEmployeeError("The name cannot be empty.")
        if len(name) < 1:
            raise InvalidNameEmployeeError("Name must be at least 2 characters long.")
        if len(name) > 100:
            raise InvalidNameEmployeeError("Name cannot exceed 100 characters.")
        allowed_pattern = r'^[a-zA-Zа-яА-Я -]+$'
        if not re.fullmatch(allowed_pattern, name):
            raise InvalidNameEmployeeError(f"Organization name '{name}' contains invalid characters.")


@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self):
        Email._validate_email(self.value)

        object.__setattr__(self, 'value', self.value.strip().lower())

    @staticmethod
    def _validate_email(email: str) -> None:

        if not email or not email.strip():
            raise InvalidEmailError("E-mail cannot be empty")

        if "@" not in email:
            raise InvalidEmailError("Email must contain '@'")

        local_part = email[:email.find("@")]
        allowed_pattern = r'^[a-zA-Z0-9.\-_]+$'
        if len(local_part) > 64:
            raise InvalidEmailError("The local part is too long")
        if len(local_part) < 1:
            raise InvalidEmailError("The local part is too short")
        if not re.fullmatch(allowed_pattern, local_part):
            raise InvalidEmailError("The email cannot contain special characters.")

        domain_part = email[email.find("@")+1:]
        allowed_pattern_2 = r'^[a-zA-Z0-9\-\.]+$'
        if domain_part[0] == ".":
            raise InvalidEmailError("An email cannot begin with special characters.")
        if not re.fullmatch(allowed_pattern_2, domain_part):
            raise InvalidEmailError("The email cannot contain special characters.")
        if len(domain_part) > 255:
            raise InvalidEmailError("The domain part is too long")
        if len(domain_part) < 1:
            raise InvalidEmailError("The domain part is too short")
        if domain_part.startswith("-") or domain_part.endswith("-"):
            raise InvalidEmailError("The email cannot contain special characters.")






