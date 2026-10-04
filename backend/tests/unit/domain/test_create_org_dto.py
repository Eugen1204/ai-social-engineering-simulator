import pytest
from social_engineering_simulator.application.dto.create_organization import CreateOrganizationRequest
from social_engineering_simulator.application.services.create_organization import CreateOrganizationService, \
    DuplicateDepartmentsError
from social_engineering_simulator.domain.organizations.unit_of_work import UnitOfWork
from social_engineering_simulator.infrastructure.persistence.in_memory.organization_repository import \
    OrganizationRepoInMemory
from social_engineering_simulator.infrastructure.persistence.in_memory.unit_of_work import UnitOfWorkInMemory


@pytest.fixture()
def dto() -> CreateOrganizationRequest:
    return CreateOrganizationRequest(name="Test Org",
                                     industry="IT Company",
                                     departments=["HR", "IT"])


@pytest.mark.asyncio
async def test_create_org_services(dto):
    uwo = UnitOfWorkInMemory()
    service = CreateOrganizationService(uow=uwo)
    result = await service.execute(request=dto)

    assert result.name == "Test Org"
    assert result.industry == "IT Company"


@pytest.mark.asyncio
async def test_create_service_with_duplicate():
    uwo = UnitOfWorkInMemory()
    service = CreateOrganizationService(uow=uwo)
    dto = CreateOrganizationRequest(name="Test",
                                    industry="IT Company",
                                    departments=["HR", "IT", "HR"])

    with pytest.raises(DuplicateDepartmentsError):
        await service.execute(request=dto)
