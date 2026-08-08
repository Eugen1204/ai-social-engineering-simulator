from dataclasses import dataclass, field
from datetime import datetime, UTC
from uuid import UUID, uuid4

from social_engineering_simulator.domain.organizations.campaign.CampaignEmployee import CampaignEmployee
from social_engineering_simulator.domain.organizations.campaign.exceptions import StartCampaignError,\
    CampaignInitError, FinishCampaignError, AddCampaignEmployeeError, DeleteCampaignEmployeeError, CancelCampaignError
from social_engineering_simulator.domain.organizations.campaign.value_object import CampaignName, CampaignStatus
from social_engineering_simulator.domain.organizations.department.employee.entity import Employee


@dataclass
class Campaign:
    name: CampaignName
    organization_id: UUID
    template_id: UUID
    landing_page_id: UUID
    status: CampaignStatus
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    _start_time: datetime | None = field(default=None, init=False)
    _end_time: datetime | None = field(default=None, init=False)
    _employees: dict[UUID, CampaignEmployee] = field(default_factory=dict)

    def __post_init__(self):
        allowed_initial_status = {CampaignStatus.Draft, CampaignStatus.Scheduled}
        if self.status not in allowed_initial_status:
            raise CampaignInitError("invalid status for campaign initialization")

    def start(self) -> None:
        if self.status == CampaignStatus.Running:
            raise StartCampaignError("the campaign is already active")
        if self.status == CampaignStatus.Finished:
            raise StartCampaignError("the campaign has already ended")
        self._start_time = datetime.now(UTC)
        self.status = CampaignStatus.Running

    def finish(self) -> None:
        if self.status != CampaignStatus.Running:
            raise FinishCampaignError("campaign not active")
        self._end_time = datetime.now(UTC)
        self.status = CampaignStatus.Finished

    def cancel(self):
        if self.status != CampaignStatus.Running or self.status != CampaignStatus.Draft or \
                self.status != CampaignStatus.Scheduled:
            raise CancelCampaignError("campaign not active or draft or scheduled")
        self.status = CampaignStatus.Cancelled
        self._end_time = datetime.now(UTC)

    def assign_employee(self, emp: Employee) -> None:
        if emp.id in self._employees:
            raise AddCampaignEmployeeError("employee has already been added")
        self._employees[emp.id] = CampaignEmployee(self.id, emp.id)

    def remove_employee(self, emp: Employee) -> None:
        if emp.id not in self._employees:
            raise DeleteCampaignEmployeeError("couldn't find an employee")
        del self._employees[emp.id]
