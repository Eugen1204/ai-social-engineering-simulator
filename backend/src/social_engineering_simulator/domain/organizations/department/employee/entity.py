from datetime import datetime, UTC
from social_engineering_simulator.domain.organizations.department.employee.value_object import EmployeeName, Email
from uuid import UUID, uuid4
from dataclasses import dataclass, field


@dataclass
class Employee:
    name: EmployeeName
    email:  Email
    department_id: UUID
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    id: UUID = field(default_factory=uuid4)


