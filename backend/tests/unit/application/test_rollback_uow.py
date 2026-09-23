import pytest

from social_engineering_simulator.application.dto.create_organization import CreateOrganizationRequest
from social_engineering_simulator.application.services.create_organization import CreateOrganizationService
from social_engineering_simulator.infrastructure.persistence.in_memory.unit_of_work import UnitOfWorkInMemory


@pytest.mark.asyncio
async def test_rollback_org(organization_with_employee):
    uow = UnitOfWorkInMemory()
    service = CreateOrganizationService(uow=uow)
    request = CreateOrganizationRequest(name='Test',
                                        industry='IT Company',
                                        departments=['HR', 'IT'])
    result = await service.execute(request)
    assert result.name == 'Test'
