from fastapi import APIRouter, HTTPException, status, Depends
from social_engineering_simulator.presentation.api.v1.schemas.organization import OrganizationResponse, \
    CreateOrganizationHttpRequest
from social_engineering_simulator.presentation.api.v1.dependencies import get_create_organization_service, \
    CreateOrganizationService
from social_engineering_simulator.application.dto.create_organization import CreateOrganizationRequest
from social_engineering_simulator.domain.organizations.exceptions import DuplicateDepartmentNameError,\
    WrongIndustryError


router = APIRouter(prefix="/organization")


@router.post("/", response_model=OrganizationResponse, status_code=201)
async def create_organization(dto: CreateOrganizationHttpRequest,
                              service: CreateOrganizationService = Depends(get_create_organization_service)):

    application_dto = CreateOrganizationRequest(name=dto.name, industry=dto.industry, departments=dto.departments)

    return service.execute(application_dto)







