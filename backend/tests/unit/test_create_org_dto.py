import pytest
from social_engineering_simulator.application.dto.create_organization import CreateOrganizationRequest
from social_engineering_simulator.application.services.create_organization import CreateOrganizationService, \
    DuplicateDepartmentsError


@pytest.fixture()
def dto() -> CreateOrganizationRequest:
    return CreateOrganizationRequest(name="Test Org",
                                     industry="IT Company",
                                     departments=["HR", "IT"])


def test_create_org_services(dto):
    service = CreateOrganizationService()
    result = service.execute(request=dto)

    assert result.name == "Test Org"
    assert result.industry == "IT Company"


def test_create_service_with_duplicate():
    service = CreateOrganizationService()
    dto = CreateOrganizationRequest(name="Test",
                                    industry="IT Company",
                                    departments=["HR", "IT", "HR"])

    with pytest.raises(DuplicateDepartmentsError):
        service.execute(request=dto)
