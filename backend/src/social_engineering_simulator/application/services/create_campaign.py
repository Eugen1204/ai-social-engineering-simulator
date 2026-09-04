from uuid import UUID

from social_engineering_simulator.application.dto.create_campaign import CreateCampaignRequest, CampaignResponse, \
    ScheduleCampaignRequest
from social_engineering_simulator.application.services.exceptions_create_campaign import CampaignNotFoundError, \
    CampaignIsNotRunning
from social_engineering_simulator.domain.email_template.repository import TemplateRepository
from social_engineering_simulator.domain.email_template.services.exceptions import TemplateNotFoundError, \
    TemplateNotInOrganization
from social_engineering_simulator.domain.organizations.campaign.entity import Campaign
from social_engineering_simulator.domain.organizations.campaign.repository import CampaignRepository
from social_engineering_simulator.domain.organizations.campaign.value_object import CampaignName, CampaignStatus
from social_engineering_simulator.domain.organizations.exceptions import OrganizationNotFoundError
from social_engineering_simulator.domain.organizations.repository import OrganizationRepository


class CreateCampaignService:
    def __init__(self, repo_campaign: CampaignRepository, repo_org: OrganizationRepository,
                 repo_template: TemplateRepository):
        self.repo_campaign = repo_campaign
        self.repo_org = repo_org
        self.repo_template = repo_template

    def execute(self, request: CreateCampaignRequest) -> CampaignResponse:
        name = CampaignName(request.name)
        org_id = request.organization_id
        if not self.repo_org.get_by_id(organization_id=org_id):
            raise OrganizationNotFoundError(f"Organization with id {org_id} not found")
        template = self.repo_template.get_by_id(template_id=request.template_id)
        if template is None:
            raise TemplateNotFoundError(f'Template with {request.template_id} not found')
        if template.organization_id != request.organization_id:
            raise TemplateNotInOrganization("the template does not belong to the organization")
        land_page_id = request.landing_page_id

        camp = Campaign(name=name, organization_id=org_id,
                        template_id=template.id, landing_page_id=land_page_id,
                        status=CampaignStatus.Draft,
                        template_version=template.version,
                        _template_subject=template.subject.value,
                        _template_content=template.content.value)

        self.repo_campaign.save(camp)

        return CampaignResponse(id=camp.id, name=camp.name.value, status=camp.status.value,
                                template_version=camp.template_version)


class GetCampaignService:
    def __init__(self, repo: CampaignRepository):
        self.repo = repo

    def execute(self, campaign_id: UUID) -> CampaignResponse:
        campaign = self.repo.get_by_id(campaign_id)
        if campaign is None:
            raise CampaignNotFoundError(f"Campaign with {campaign_id} not found")

        return CampaignResponse(id=campaign.id,
                                name=campaign.name.value,
                                status=campaign.status.value,
                                template_version=campaign.template_version)


class StartCampaignService:
    def __init__(self, repo: CampaignRepository):
        self.repo = repo

    def execute(self, campaign_id: UUID) -> CampaignResponse:
        campaign = self.repo.get_by_id(campaign_id)
        if campaign is None:
            raise CampaignNotFoundError(f"Campaign with {campaign_id} not found")

        campaign.start()

        self.repo.save(campaign)

        return CampaignResponse(id=campaign.id,
                                name=campaign.name.value,
                                status=campaign.status.value,
                                template_version=campaign.template_version)


class FinishCampaignService:
    def __init__(self, repo: CampaignRepository):
        self.repo = repo

    def execute(self, campaign_id: UUID) -> CampaignResponse:
        campaign = self.repo.get_by_id(campaign_id)
        if campaign is None:
            raise CampaignNotFoundError(
                f"Campaign with {campaign_id} not found"
            )
        campaign.finish()
        self.repo.save(campaign)

        return CampaignResponse(id=campaign.id, name=campaign.name.value, status=campaign.status.value,
                                template_version=campaign.template_version)


class CancelCampaignService:
    def __init__(self, repo: CampaignRepository):
        self.repo = repo

    def execute(self, campaign_id: UUID) -> CampaignResponse:
        campaign = self.repo.get_by_id(campaign_id)
        if campaign is None:
            raise CampaignNotFoundError(
                f"Campaign with {campaign_id} not found"
            )
        campaign.cancel()
        self.repo.save(campaign)

        return CampaignResponse(id=campaign.id, name=campaign.name.value, status=campaign.status.value,
                                template_version=campaign.template_version)


class ScheduleCampaignService:
    def __init__(self, repo_campaign: CampaignRepository):
        self.repo_campaign = repo_campaign

    def execute(self, request: ScheduleCampaignRequest) -> CampaignResponse:
        campaign_id = request.campaign_id
        camp = self.repo_campaign.get_by_id(campaign_id=campaign_id)
        if camp is None:
            raise CampaignNotFoundError(f"Campaign with id {campaign_id} not found")

        camp.schedule(start_time=request.start_time)
        self.repo_campaign.save(camp)

        return CampaignResponse(id=camp.id, name=camp.name.value, status=camp.status.value,
                                template_version=camp.template_version)


class ExecuteCampaignService:
    def __init__(self, repo_campaign: CampaignRepository, repo_org: OrganizationRepository):
        self.repo_campaign = repo_campaign
        self.repo_org = repo_org

    def execute(self, campaign_id: UUID):
        campaign = self.repo_campaign.get_by_id(campaign_id)
        if campaign is None:
            raise CampaignNotFoundError(f"Campaign with {campaign_id} not found")
        if campaign.status != CampaignStatus.Running:
            raise CampaignIsNotRunning(f"Campaign {campaign.name} is not running")

        organization = self.repo_org.get_by_id(campaign.organization_id)

        campaign_employees = campaign.employees

        for emp in campaign_employees.values():
            emp.mark_send()

        self.repo_campaign.save(campaign)




