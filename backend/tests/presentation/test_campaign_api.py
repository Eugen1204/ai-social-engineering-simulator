from uuid import uuid4, UUID

import pytest
from starlette.testclient import TestClient

from social_engineering_simulator.domain.organizations.campaign.value_object import CampaignStatus
from social_engineering_simulator.infrastructure.persistence.in_memory.organization_repository import \
    OrganizationRepoInMemory
from social_engineering_simulator.presentation.api.v1.dependencies import get_repository_campaign, \
    get_organization_repository
from social_engineering_simulator.presentation.main import app
from social_engineering_simulator.infrastructure.persistence.in_memory.campaign_repository import CampaignRepoInMemory


@pytest.fixture
def client():
    """Фикстура для создания тестового клиента с InMemory-репозиторием."""
    repo_campaign = CampaignRepoInMemory()
    repo_org = OrganizationRepoInMemory()
    app.dependency_overrides[get_repository_campaign] = lambda: repo_campaign
    app.dependency_overrides[get_organization_repository] = lambda: repo_org

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_create_campaign(client):
    repo_org = app.dependency_overrides[get_organization_repository]()
    payload = {
        "name": "TestOrg",
        "industry": "IT Company",
        "departments": ["HR", "IT"]
    }

    response = client.post("/organizations/", json=payload)
    assert response.status_code == 201
    data = response.json()
    print(data)
    print(repo_org._organizations)
    assert repo_org.exists(UUID(data["id"]))

    payload = {
        "name": "TestCampaign",
        "organization_id": f"{data['id']}",
        "template_id": f"{uuid4()}",
        "landing_page_id": f"{uuid4()}"
    }

    response = client.post("/campaigns/", json=payload)
    assert response.status_code == 201
    data = response.json()
    repo = app.dependency_overrides[get_repository_campaign]()
    assert repo.exists(UUID(data["id"]))
    response_start = client.post(f"/campaigns/{data['id']}/start")
    assert response_start.status_code == 200
    data_start = response_start.json()
    assert data_start["status"] == CampaignStatus.Running.value
    response_wrong_start = client.post(f"/campaigns/{uuid4()}/start")
    assert response_wrong_start.status_code == 404
    response_cancel = client.post(f"campaigns/{data['id']}/cancel")
    assert response_cancel.status_code == 200

    response_2 = client.post("/campaigns/", json=payload)
    assert response_2.status_code == 201
    data_2 = response_2.json()
    response_finished = client.post(f"campaigns/{data_2['id']}/finish")
    assert response_finished.status_code == 409




