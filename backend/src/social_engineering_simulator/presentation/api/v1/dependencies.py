from functools import lru_cache

from fastapi import Depends

from social_engineering_simulator.application.services.create_organization import CreateOrganizationService, \
    GetOrganizationService
from social_engineering_simulator.domain.organizations.repository import OrganizationRepository
from social_engineering_simulator.infrastructure.persistence.in_memory.organization_repository import \
    OrganizationRepoInMemory


@lru_cache()
def get_repository() -> OrganizationRepository:
    return OrganizationRepoInMemory()


def get_create_organization_service() -> CreateOrganizationService:
    repo = get_repository()
    return CreateOrganizationService(repo=repo)


def get_organization_service() -> GetOrganizationService:
    repo = get_repository()
    return GetOrganizationService(repo=repo)





