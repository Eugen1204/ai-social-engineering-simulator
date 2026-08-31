from uuid import UUID

from fastapi import APIRouter, Depends

from social_engineering_simulator.application.services.create_organization import GetOrganizationService, \
    AddEmployeeInOrganization, GetEmployeeInOrganization
from social_engineering_simulator.presentation.api.v1.schemas.organization import OrganizationHttpResponse, \
    CreateOrganizationHttpRequest, AddEmployeeRequest, AddEmployeeRequestResponse, GetEmployeeRequestResponse
from social_engineering_simulator.presentation.api.v1.dependencies import get_create_organization_service, \
    CreateOrganizationService, get_organization_service, add_emp_in_org, get_emp_in_org
from social_engineering_simulator.application.dto.create_organization import CreateOrganizationRequest, EmployeeRequest

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


@router.post("/{organization_id}/employees", response_model=AddEmployeeRequestResponse, status_code=201)
async def add_employee_in_org(organization_id: UUID, data: AddEmployeeRequest,
                              service: AddEmployeeInOrganization = Depends(add_emp_in_org)) \
        -> AddEmployeeRequestResponse:
    request = EmployeeRequest(name=data.name, email=data.email, dep_name=data.dep_name, org_id=organization_id)
    result = service.execute(request)

    return AddEmployeeRequestResponse(id=result.id, name=result.name, email=result.email, org_id=result.org_id)


@router.get("/{organization_id}/employees/{employee_id}", response_model=GetEmployeeRequestResponse, status_code=200)
async def get_employee_in_organization(organization_id: UUID, employee_id: UUID,
                                       service: GetEmployeeInOrganization = Depends(get_emp_in_org)):
    result = service.execute(employee_id=employee_id, org_id=organization_id)
    return GetEmployeeRequestResponse(id=result.id, name=result.name, email=result.email, org_id=result.org_id)


