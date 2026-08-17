from dataclasses import dataclass, field
from datetime import datetime, UTC, timezone
from uuid import UUID, uuid4

from social_engineering_simulator.domain.organizations.campaign.CampaignEmployee import CampaignEmployee
from social_engineering_simulator.domain.organizations.campaign.exceptions import StartCampaignError, \
    CampaignInitError, FinishCampaignError, AddCampaignEmployeeError, DeleteCampaignEmployeeError, CancelCampaignError, \
    CampaignValidationError, CampaignScheduleError
from social_engineering_simulator.domain.organizations.campaign.value_object import CampaignName, CampaignStatus
from social_engineering_simulator.domain.organizations.campaign.workflow import CampaignWorkflow
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
    _scheduled_at: datetime | None = field(default=None, init=False)
    _started_at: datetime | None = field(default=None, init=False)
    _cancelled_at: datetime | None = field(default=None, init=False)
    _finished_at: datetime | None = field(default=None, init=False)
    _employees: dict[UUID, CampaignEmployee] = field(default_factory=dict)
    workflow: CampaignWorkflow = field(default_factory=CampaignWorkflow)

    def __post_init__(self):
        allowed_initial_status = {CampaignStatus.Draft, CampaignStatus.Scheduled}
        if self.status not in allowed_initial_status:
            raise CampaignInitError("invalid status for campaign initialization")

    def _apply_action(self, action_name: str) -> None:
        self.status = self.workflow.get_next_status(self.status, action_name)

    def return_to_draft(self) -> None:
        self._apply_action("draft")

    def start(self) -> None:
        # if not self._employees:
        #     raise CampaignValidationError("cannot start a campaign without employees.")
        self._apply_action("start")
        self._started_at = datetime.now(UTC)

    def finish(self) -> None:
        self._apply_action("finish")
        self._finished_at = datetime.now(UTC)

    def cancel(self) -> None:
        self._apply_action("cancel")
        self._cancelled_at = datetime.now(UTC)

    def schedule(self, start_time: datetime) -> None:
        if start_time.tzinfo is None:
            start_time = start_time.replace(tzinfo=timezone.utc)
        now = datetime.now(UTC)
        start = start_time.replace(microsecond=0)
        if start < now:
            raise CampaignScheduleError("Cannot schedule a campaign in the past")
        self._apply_action("schedule")
        self._scheduled_at = start_time

    def archive(self) -> None:
        self._apply_action("archive")

    def assign_employee(self, emp_id: UUID) -> None:
        if emp_id in self._employees:
            raise AddCampaignEmployeeError("employee has already been added")
        self._employees[emp_id] = CampaignEmployee(self.id, emp_id)

    def remove_employee(self, emp_id: UUID) -> None:
        if emp_id not in self._employees:
            raise DeleteCampaignEmployeeError("couldn't find an employee")
        del self._employees[emp_id]
