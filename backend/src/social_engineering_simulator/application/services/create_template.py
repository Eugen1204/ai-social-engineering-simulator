from social_engineering_simulator.application.dto.create_template import CreateTemplateRequest, \
    CreateTemplateRequestResponse, GetTemplateRequest, PreviewTemplateRequest, TemplateVariablesResponse, \
    UpdateTemplateRequest, UpdateTemplateResponse
from social_engineering_simulator.domain.email_template.entity import Template
from social_engineering_simulator.domain.email_template.repository import TemplateRepository
from social_engineering_simulator.domain.email_template.services.exceptions import TemplateNotInOrganization, \
    TemplateNotFoundError
from social_engineering_simulator.domain.email_template.services.template_engine import EngineTemplate
from social_engineering_simulator.domain.email_template.value_object import SubjectText, TemplateContext, \
    RenderedTemplate, ContentText
from social_engineering_simulator.domain.organizations.exceptions import OrganizationNotFoundError
from social_engineering_simulator.domain.organizations.repository import OrganizationRepository


class CreateTemplateService:
    def __init__(self, repo_template: TemplateRepository, repo_org: OrganizationRepository):
        self.repo_template = repo_template
        self.repo_org = repo_org

    def execute(self, request: CreateTemplateRequest) -> CreateTemplateRequestResponse:
        org_id = request.organization_id
        if not self.repo_org.get_by_id(organization_id=org_id):
            raise OrganizationNotFoundError(f"Organization with id {org_id} not found")
        temp = Template(organization_id=request.organization_id, name=request.name,
                        subject=SubjectText(request.subject), content=ContentText(request.content))

        self.repo_template.save(temp)

        return CreateTemplateRequestResponse(id=temp.id,
                                             name=temp.name,
                                             subject=temp.subject.value,
                                             content=temp.content.value,
                                             version=temp.version,
                                             created_at=temp.created_at,
                                             organization_id=temp.organization_id)


class GetTemplateService:
    def __init__(self, repo_template: TemplateRepository, repo_org: OrganizationRepository):
        self.repo_template = repo_template
        self.repo_org = repo_org

    def execute(self, request: GetTemplateRequest):
        temp = self.repo_template.get_by_id(request.id_template)
        if self.repo_org.get_by_id(temp.organization_id) is None:
            raise OrganizationNotFoundError("Organization not found")
        if temp is None:
            raise TemplateNotFoundError("Template not found")
        if temp.organization_id != request.id_organization:
            raise TemplateNotInOrganization("the template does not belong to the organization")

        return CreateTemplateRequestResponse(id=temp.id,
                                             name=temp.name,
                                             subject=temp.subject.value,
                                             content=temp.content.value,
                                             version=temp.version,
                                             created_at=temp.created_at,
                                             organization_id=temp.organization_id)


class PreviewTemplateService:
    def __init__(self, repo_template: TemplateRepository, repo_org: OrganizationRepository, engine: EngineTemplate):
        self.repo_template = repo_template
        self.repo_org = repo_org
        self.engine = engine

    def execute(self, request: PreviewTemplateRequest) -> TemplateVariablesResponse:
        temp = self.repo_template.get_by_id(request.template_id)

        if self.repo_org.get_by_id(temp.organization_id) is None:
            raise OrganizationNotFoundError("Organization not found")
        if temp is None:
            raise TemplateNotFoundError("Template not found")
        if temp.organization_id != request.organization_id:
            raise TemplateNotInOrganization("the template does not belong to the organization")

        context = TemplateContext()
        for k, v in request.variables.items():
            context.set(k, v)

        res = self.engine.render(template=temp, context_template=context)
        return TemplateVariablesResponse(res.subject, res.content)


class UpdateTemplateService:
    def __init__(self, repo_template: TemplateRepository, repo_org: OrganizationRepository):
        self.repo_template = repo_template
        self.repo_org = repo_org

    def execute(self, request: UpdateTemplateRequest) -> UpdateTemplateResponse:
        template = self.repo_template.get_by_id(request.template_id)
        if self.repo_org.get_by_id(template.organization_id) is None:
            raise OrganizationNotFoundError("Organization not found")
        if template is None:
            raise TemplateNotFoundError("Template not found")
        if template.organization_id != request.organization_id:
            raise TemplateNotInOrganization("the template does not belong to the organization")
        template.update(new_content=request.content, new_subject=request.subject)

        return UpdateTemplateResponse(organization_id=template.organization_id,
                                      template_id=template.id,
                                      content=template.content.value,
                                      subject=template.subject.value,
                                      version=template.version)





