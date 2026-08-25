from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class CreateCampaignRequest:
    name: str
    organization_id: UUID
    template_id: UUID
    landing_page_id: UUID


@dataclass(frozen=True)
class CampaignResponse:
    id: UUID
    name: str
    status: str

