from uuid import UUID

from fastapi import APIRouter, Depends

from social_engineering_simulator.application.dto.create_campaign import CreateCampaignRequest
from social_engineering_simulator.application.services.create_campaign import CreateCampaignService, \
    FinishCampaignService, CancelCampaignService
from social_engineering_simulator.presentation.api.v1.dependencies import get_create_campaign_service, \
    start_campaign_service, finish_campaign_service, cancel_campaign_service
from social_engineering_simulator.presentation.api.v1.schemas.campaign import CampaignHttpResponse, \
    CampaignCreateRequest

router = APIRouter(prefix="/campaigns")


@router.post("/", response_model=CampaignHttpResponse, status_code=201)
async def create_campaign(dto: CampaignCreateRequest, service=Depends(get_create_campaign_service)) \
        -> CampaignHttpResponse:
    application_dto = CreateCampaignRequest(name=dto.name, organization_id=dto.organization_id,
                                            template_id=dto.template_id, landing_page_id=dto.landing_page_id)

    result = service.execute(application_dto)

    return CampaignHttpResponse(id=result.id,
                                name=result.name,
                                status=result.status)


@router.post("/{campaign_id}/start", response_model=CampaignHttpResponse, status_code=200)
async def start_campaign(campaign_id: UUID, service=Depends(start_campaign_service)) \
        -> CampaignHttpResponse:
    result = service.execute(campaign_id)

    return CampaignHttpResponse(id=result.id,
                                name=result.name,
                                status=result.status)


@router.post("/{campaign_id}/finish", response_model=CampaignHttpResponse, status_code=200)
async def finish_campaign(campaign_id: UUID, service: FinishCampaignService = Depends(finish_campaign_service)) \
        -> CampaignHttpResponse:
    result = service.execute(campaign_id)

    return CampaignHttpResponse(id=result.id, name=result.name, status=result.status)


@router.post("/{campaign_id}/cancel", response_model=CampaignHttpResponse, status_code=200)
async def cancel_campaign(campaign_id: UUID, service: CancelCampaignService = Depends(cancel_campaign_service)) \
        -> CampaignHttpResponse:
    result = service.execute(campaign_id)

    return CampaignHttpResponse(id=result.id,
                                name=result.name,
                                status=result.status)
