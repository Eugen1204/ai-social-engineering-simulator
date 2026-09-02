from uuid import UUID

from fastapi import APIRouter, Depends

from social_engineering_simulator.application.dto.create_template import PreviewTemplateRequest, CreateTemplateRequest, \
    GetTemplateRequest, UpdateTemplateRequest
from social_engineering_simulator.application.services.create_organization import GetOrganizationService, \
    AddEmployeeInOrganization, GetEmployeeInOrganization
from social_engineering_simulator.application.services.create_template import PreviewTemplateService, \
    CreateTemplateService, GetTemplateService, UpdateTemplateService
from social_engineering_simulator.presentation.api.v1.schemas.organization import OrganizationHttpResponse, \
    CreateOrganizationHttpRequest, AddEmployeeRequest, AddEmployeeRequestResponse, GetEmployeeRequestResponse, \
    TemplateVariables, TemplateVariablesResponse, AddTemplateResponse, AddTemplateRequest, TemplateResponse, \
    UpdateTemplateHttpResponse, UpdateTemplateHttpRequest
from social_engineering_simulator.presentation.api.v1.dependencies import get_create_organization_service, \
    CreateOrganizationService, get_organization_service, add_emp_in_org, get_emp_in_org, preview_template, \
    add_template, update_template_service, get_template_service
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


@router.post("/{organization_id}/templates/{template_id}/preview", status_code=200,
             response_model=TemplateVariablesResponse)
async def template_preview(organization_id: UUID, template_id: UUID, variables: TemplateVariables,
                           service: PreviewTemplateService = Depends(preview_template)) -> TemplateVariablesResponse:
    request = PreviewTemplateRequest(organization_id=organization_id, template_id=template_id,
                                     variables=variables.variables)
    result = service.execute(request)

    return TemplateVariablesResponse(subject=result.subject, content=result.content)


@router.post("/{organization_id}/templates", status_code=201, response_model=AddTemplateResponse)
async def add_template(organization_id: UUID, request: AddTemplateRequest,
                       service: CreateTemplateService = Depends(add_template)) -> AddTemplateResponse:
    template_request = CreateTemplateRequest(organization_id=organization_id,
                                             name=request.name,
                                             subject=request.subject,
                                             content=request.content)

    result = service.execute(template_request)

    return AddTemplateResponse(id=result.id, name=result.name, subject=result.subject,
                               content=result.content, version=result.version, created_at=result.created_at,
                               organization_id=organization_id)


@router.get("/{organization_id}/templates/{template_id}", status_code=200, response_model=TemplateResponse)
async def get_template(organization_id: UUID, template_id: UUID,
                       service: GetTemplateService = Depends(get_template_service)) -> TemplateResponse:
    request = GetTemplateRequest(id_template=template_id, id_organization=organization_id)
    result = service.execute(request)

    return TemplateResponse(id=result.id,
                            organization_id=result.organization_id,
                            name=result.name,
                            subject=result.subject,
                            content=result.content,
                            version=result.version,
                            created_at=result.created_at)


@router.patch("/{organization_id}/templates/{template_id}", status_code=200, response_model=UpdateTemplateHttpResponse)
async def update_template(organization_id: UUID, template_id: UUID, update_data: UpdateTemplateHttpRequest,
                          service: UpdateTemplateService = Depends(update_template_service)) \
        -> UpdateTemplateHttpResponse:
    request = UpdateTemplateRequest(organization_id=organization_id,
                                    template_id=template_id,
                                    content=update_data.content,
                                    subject=update_data.subject)
    result = service.execute(request)

    return UpdateTemplateHttpResponse(organization_id=result.organization_id,
                                      template_id=result.template_id,
                                      content=result.content,
                                      subject=result.subject,
                                      version=result.version)

