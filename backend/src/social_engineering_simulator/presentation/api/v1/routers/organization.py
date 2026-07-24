from fastapi import APIRouter, Depends
from social_engineering_simulator.presentation.api.v1.schemas.organization import OrganizationHttpResponse, \
    CreateOrganizationHttpRequest
from social_engineering_simulator.presentation.api.v1.dependencies import get_create_organization_service, \
    CreateOrganizationService
from social_engineering_simulator.application.dto.create_organization import CreateOrganizationRequest


router = APIRouter(prefix="/organizations")


@router.post("/", response_model=OrganizationHttpResponse, status_code=201)
async def create_organization(dto: CreateOrganizationHttpRequest,
                              service: CreateOrganizationService = Depends(get_create_organization_service)):

    application_dto = CreateOrganizationRequest(name=dto.name, industry=dto.industry, departments=dto.departments)

    result = service.execute(application_dto)

    return OrganizationHttpResponse(id=result.id,
                                    name=result.name,
                                    industry=result.industry,
                                    departments=result.departments)







