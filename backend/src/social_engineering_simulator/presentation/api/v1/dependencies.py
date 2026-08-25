from functools import lru_cache

from fastapi import Depends

from social_engineering_simulator.application.services.create_campaign import CreateCampaignService, \
    StartCampaignService, FinishCampaignService, CancelCampaignService
from social_engineering_simulator.application.services.create_organization import CreateOrganizationService, \
    GetOrganizationService
from social_engineering_simulator.domain.organizations.campaign.repository import CampaignRepository
from social_engineering_simulator.domain.organizations.repository import OrganizationRepository
from social_engineering_simulator.infrastructure.persistence.in_memory.campaign_repository import CampaignRepoInMemory
from social_engineering_simulator.infrastructure.persistence.in_memory.organization_repository import \
    OrganizationRepoInMemory


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


def get_repository_campaign() -> CampaignRepository:
    return CampaignRepoInMemory()


def get_create_campaign_service(repo_campaign: CampaignRepository = Depends(get_repository_campaign),
                                repo_org: OrganizationRepository = Depends(get_organization_repository)) \
        -> CreateCampaignService:
    return CreateCampaignService(repo_campaign=repo_campaign, repo_org=repo_org)


def start_campaign_service(repo: CampaignRepository = Depends(get_repository_campaign)) \
        -> StartCampaignService:
    return StartCampaignService(repo=repo)


def finish_campaign_service(repo: CampaignRepository = Depends(get_repository_campaign)) \
        -> FinishCampaignService:
    return FinishCampaignService(repo=repo)


def cancel_campaign_service(repo: CampaignRepository = Depends(get_repository_campaign)) \
        -> CancelCampaignService:
    return CancelCampaignService(repo=repo)
