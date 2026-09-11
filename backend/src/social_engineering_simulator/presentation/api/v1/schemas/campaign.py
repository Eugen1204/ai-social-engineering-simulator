from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CampaignHttpResponse(BaseModel):
    id: UUID
    name: str
    status: str
    template_version: int


class CampaignCreateRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    name: str = Field(..., min_length=2, max_length=100, examples=["Fishing"])
    organization_id: UUID
    template_id: UUID
    landing_page_id: UUID


class ScheduleCampaignHttpRequest(BaseModel):
    start_time: datetime


class EmployeeCampaignRequest(BaseModel):
    id: UUID
    name: str
    email: str
    department_id: UUID


class GetEmployeeTimelineHttpResponse(BaseModel):
    event_id: UUID
    event_type: UUID
    occurred_at: datetime


class CampaignEmployeeRiskHttpResponse(BaseModel):
    employee_id: UUID
    risk_score: float
    sent_at: datetime | None
    opened_at: datetime | None
    click_count: int
    credential_submission_count: int


class CampaignAnalyticHttpResponse(BaseModel):
    campaign_id: UUID
    total_employees: int
    sent_count: int
    opened_count: int | None
    clicked_employee_count: int | None
    credential_submission_employee_count: int | None
    open_rate: float
    click_rate: float
    credential_submission_rate: float
    average_risk_score: float
    highest_risk_employee_count: int


