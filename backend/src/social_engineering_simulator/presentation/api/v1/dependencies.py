from functools import lru_cache

from fastapi import Depends

from social_engineering_simulator.application.services.add_employee import AddCampaignEmployeeService, \
    RemoveCampaignEmployeeService
from social_engineering_simulator.application.services.create_campaign import CreateCampaignService, \
    StartCampaignService, FinishCampaignService, CancelCampaignService, ScheduleCampaignService
from social_engineering_simulator.application.services.create_organization import CreateOrganizationService, \
    GetOrganizationService, AddEmployeeInOrganization, GetEmployeeInOrganization
from social_engineering_simulator.application.services.create_template import PreviewTemplateService, \
    CreateTemplateService
from social_engineering_simulator.domain.email_template.repository import TemplateRepository
from social_engineering_simulator.domain.email_template.services.template_engine import EngineTemplate
from social_engineering_simulator.domain.organizations.campaign.repository import CampaignRepository
from social_engineering_simulator.domain.organizations.repository import OrganizationRepository
from social_engineering_simulator.infrastructure.persistence.in_memory.campaign_repository import CampaignRepoInMemory
from social_engineering_simulator.infrastructure.persistence.in_memory.organization_repository import \
    OrganizationRepoInMemory
from social_engineering_simulator.infrastructure.persistence.in_memory.template_repository import \
    TemplateRepositoryInMemory


@lru_cache()
def get_organization_repository() -> OrganizationRepository:
    return OrganizationRepoInMemory()


def get_create_organization_service(
        repo: OrganizationRepository = Depends(get_organization_repository)
) -> CreateOrganizationService:
    return CreateOrganizationService(repo=repo)


def get_organization_service(
        repo: OrganizationRepository = Depends(get_organization_repository)
) -> GetOrganizationService:
    return GetOrganizationService(repo=repo)


@lru_cache()
def get_repository_campaign() -> CampaignRepository:
    return CampaignRepoInMemory()


def start_campaign_service(repo: CampaignRepository = Depends(get_repository_campaign)) \
        -> StartCampaignService:
    return StartCampaignService(repo=repo)


def finish_campaign_service(repo: CampaignRepository = Depends(get_repository_campaign)) \
        -> FinishCampaignService:
    return FinishCampaignService(repo=repo)


def cancel_campaign_service(repo: CampaignRepository = Depends(get_repository_campaign)) \
        -> CancelCampaignService:
    return CancelCampaignService(repo=repo)


def schedule_campaign_service(repo: CampaignRepository = Depends(get_repository_campaign)) \
        -> ScheduleCampaignService:
    return ScheduleCampaignService(repo_campaign=repo)


def add_employee_campaign(repo_campaign: CampaignRepository = Depends(get_repository_campaign),
                          repo_org: OrganizationRepository = Depends(get_organization_repository)) \
        -> AddCampaignEmployeeService:
    return AddCampaignEmployeeService(repo_campaign=repo_campaign, repo_org=repo_org)


def remove_employee_campaign(repo_campaign: CampaignRepository = Depends(get_repository_campaign)) \
        -> RemoveCampaignEmployeeService:
    return RemoveCampaignEmployeeService(repo_campaign=repo_campaign)


def add_emp_in_org(
        repo: OrganizationRepository = Depends(get_organization_repository)
) -> AddEmployeeInOrganization:
    return AddEmployeeInOrganization(repo=repo)


def get_emp_in_org(repo: OrganizationRepository = Depends(get_organization_repository)
                   ) -> GetEmployeeInOrganization:
    return GetEmployeeInOrganization(repo=repo)


@lru_cache()
def get_repository_template() -> TemplateRepository:
    return TemplateRepositoryInMemory()


@lru_cache()
def get_engine_template() -> EngineTemplate:
    return EngineTemplate()


def preview_template(template_repo: TemplateRepository = Depends(get_repository_template),
                     repo_org: OrganizationRepository = Depends(get_organization_repository),
                     engine: EngineTemplate = Depends(get_engine_template)) -> PreviewTemplateService:
    return PreviewTemplateService(repo_template=template_repo, repo_org=repo_org, engine=engine)


def get_create_campaign_service(repo_campaign: CampaignRepository = Depends(get_repository_campaign),
                                repo_org: OrganizationRepository = Depends(get_organization_repository),
                                repo_template: TemplateRepository = Depends(get_repository_template)) \
        -> CreateCampaignService:
    return CreateCampaignService(repo_campaign=repo_campaign, repo_org=repo_org, repo_template=repo_template)


def add_template(repo_template: TemplateRepository = Depends(get_repository_template),
                 repo_org: OrganizationRepository = Depends(get_organization_repository)) -> CreateTemplateService:
    return CreateTemplateService(repo_template=repo_template, repo_org=repo_org)
