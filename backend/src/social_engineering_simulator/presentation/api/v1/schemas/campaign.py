from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CampaignHttpResponse(BaseModel):
    id: UUID
    name: str
    status: str


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


