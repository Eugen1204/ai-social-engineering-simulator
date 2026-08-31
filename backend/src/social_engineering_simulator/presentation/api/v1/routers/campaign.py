from uuid import UUID

from fastapi import APIRouter, Depends

from social_engineering_simulator.application.dto.add_employee import AddCampaignEmployeeRequest, \
    RemoveCampaignEmployeeRequest
from social_engineering_simulator.application.dto.create_campaign import CreateCampaignRequest, ScheduleCampaignRequest
from social_engineering_simulator.application.services.add_employee import AddCampaignEmployeeService, \
    RemoveCampaignEmployeeService
from social_engineering_simulator.application.services.create_campaign import CreateCampaignService, \
    FinishCampaignService, CancelCampaignService, ScheduleCampaignService
from social_engineering_simulator.presentation.api.v1.dependencies import get_create_campaign_service, \
    start_campaign_service, finish_campaign_service, cancel_campaign_service, schedule_campaign_service, \
    add_employee_campaign, remove_employee_campaign
from social_engineering_simulator.presentation.api.v1.schemas.campaign import CampaignHttpResponse, \
    CampaignCreateRequest, ScheduleCampaignHttpRequest, EmployeeCampaignRequest

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


@router.post("/{campaign_id}/schedule", response_model=CampaignHttpResponse, status_code=200)
async def schedule_campaign(campaign_id: UUID, data: ScheduleCampaignHttpRequest,
                            service: ScheduleCampaignService = Depends(schedule_campaign_service)) \
        -> CampaignHttpResponse:
    request = ScheduleCampaignRequest(campaign_id=campaign_id, start_time=data.start_time)
    result = service.execute(request)

    return CampaignHttpResponse(id=result.id,
                                name=result.name,
                                status=result.status)


@router.post("/{campaign_id}/employees/{employee_id}", response_model=EmployeeCampaignRequest, status_code=201)
async def add_employee(campaign_id: UUID, employee_id: UUID,
                       service: AddCampaignEmployeeService = Depends(add_employee_campaign)) -> EmployeeCampaignRequest:
    request = AddCampaignEmployeeRequest(employee_id=employee_id, campaign_id=campaign_id)
    result = service.execute(request)

    return EmployeeCampaignRequest(id=result.id, name=result.name, email=result.email,
                                   department_id=result.department_id)


@router.delete("/{campaign_id}/employees/{employee_id}", status_code=204)
async def remove_employee(campaign_id: UUID, employee_id: UUID,
                          service: RemoveCampaignEmployeeService = Depends(remove_employee_campaign)) -> None:
    request = RemoveCampaignEmployeeRequest(employee_id=employee_id, campaign_id=campaign_id)
    service.execute(request)

