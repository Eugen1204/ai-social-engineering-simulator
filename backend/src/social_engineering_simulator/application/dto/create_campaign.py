from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class CreateCampaignRequest:
    name: str
    organization_id: UUID
    template_id: UUID
    landing_page_id: UUID


@dataclass(frozen=True)
class CampaignResponse:
    """
     Response with information about the campaign.

     The template_version field shows the template version that was
     fixed when the campaign was created. It does NOT change when the template is updated.

    """
    id: UUID
    name: str
    status: str
    template_version: int


@dataclass(frozen=True)
class ScheduleCampaignRequest:
    campaign_id: UUID
    start_time: datetime


@dataclass(frozen=True)
class OpenTemplateCampaignRequest:
    campaign_id: UUID
    organization_id: UUID
    employee_id: UUID
    open_at: datetime


@dataclass(frozen=True)
class OpenTemplateCampaignResponse:
    campaign_id: UUID
    employee_id: UUID
    opened_at: datetime


@dataclass(frozen=True)
class ClickCampaignEmployeeRequest:
    campaign_id: UUID
    organization_id: UUID
    employee_id: UUID
    click_at: datetime


@dataclass(frozen=True)
class ClickCampaignEmployeeResponse:
    campaign_id: UUID
    employee_id: UUID
    clicked_at: datetime


