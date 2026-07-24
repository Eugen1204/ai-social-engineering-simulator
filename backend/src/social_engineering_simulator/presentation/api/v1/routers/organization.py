from uuid import UUID

from fastapi import APIRouter, Depends

from social_engineering_simulator.application.services.create_organization import GetOrganizationService
from social_engineering_simulator.presentation.api.v1.schemas.organization import OrganizationHttpResponse, \
    CreateOrganizationHttpRequest
from social_engineering_simulator.presentation.api.v1.dependencies import get_create_organization_service, \
    CreateOrganizationService, get_organization_service
from social_engineering_simulator.application.dto.create_organization import CreateOrganizationRequest

router = APIRouter(prefix="/organizations")


@router.post("/", response_model=OrganizationHttpResponse, status_code=201)
async def create_organization(dto: CreateOrganizationHttpRequest,
                              service: CreateOrganizationService = Depends(get_create_organization_service)) \
        -> OrganizationHttpResponse:
    application_dto = CreateOrganizationRequest(name=dto.name, industry=dto.industry, departments=dto.departments)

    result = service.execute(application_dto)

    return OrganizationHttpResponse(id=result.id,
                                    name=result.name,
                                    industry=result.industry,
                                    departments=result.count_departments
                                    )


@router.get("/{organization_id}", response_model=OrganizationHttpResponse, status_code=200)
async def get_organization(organization_id: UUID, service: GetOrganizationService = Depends(get_organization_service)) \
        -> OrganizationHttpResponse:
    result = service.execute(organization_id)

    return OrganizationHttpResponse(id=result.id,
                                    name=result.name,
                                    industry=result.industry,
                                    departments=result.count_departments)
