from uuid import uuid4, UUID

import pytest
from starlette.testclient import TestClient

from social_engineering_simulator.domain.organizations.campaign.value_object import CampaignStatus
from social_engineering_simulator.infrastructure.persistence.in_memory.organization_repository import \
    OrganizationRepoInMemory
from social_engineering_simulator.infrastructure.persistence.in_memory.template_repository import \
    TemplateRepositoryInMemory
from social_engineering_simulator.presentation.api.v1.dependencies import get_repository_campaign, \
    get_organization_repository, get_repository_template
from social_engineering_simulator.presentation.main import app
from social_engineering_simulator.infrastructure.persistence.in_memory.campaign_repository import CampaignRepoInMemory


@pytest.fixture
def client():
    """Фикстура для создания тестового клиента с InMemory-репозиторием."""
    repo_campaign = CampaignRepoInMemory()
    repo_org = OrganizationRepoInMemory()
    repo_template = TemplateRepositoryInMemory()
    app.dependency_overrides[get_repository_campaign] = lambda: repo_campaign
    app.dependency_overrides[get_organization_repository] = lambda: repo_org
    app.dependency_overrides[get_repository_template] = lambda: repo_template

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture()
def template_with_organization(client):
    payload = {
        "name": "TestOrg3",
        "industry": "IT Company",
        "departments": ["HR", "IT"]
    }

    response = client.post("/organizations/", json=payload)
    assert response.status_code == 201
    data_org = response.json()

    payload = {
        "name": "Fishing",
        "subject": "Hi {{ name }}",
        "content": "Can you click on this {{ link }}"
    }

    response = client.post(f"/organizations/{data_org['id']}/templates", json=payload)

    emp = client.post(f"/organizations/{data_org['id']}/employees", json={
        "name": "SDVSV dv",
        "email": "dcvdv@cw.com",
        "dep_name": "HR"
    })

    assert emp.status_code == 201

    return response.json(), emp.json()['id']


def test_create_campaign(client, template_with_organization):
    template_with_org, emp_id = template_with_organization

    print(template_with_org)
    payload = {
        "name": "TestCampaign",
        "organization_id": f"{template_with_org['organization_id']}",
        "template_id": f"{template_with_org['id']}",
        "landing_page_id": f"{uuid4()}"
    }

    response = client.post("/campaigns/", json=payload)
    assert response.status_code == 201
    data = response.json()
    repo = app.dependency_overrides[get_repository_campaign]()
    assert repo.exists(UUID(data["id"]))
    client.post(f"/campaigns/{data['id']}/employees/{emp_id}")

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


def test_schedule_campaign(client, template_with_organization):
    template_with_org, emp_id = template_with_organization

    payload = {
        "name": "TestCampaign",
        "organization_id": f"{template_with_org['organization_id']}",
        "template_id": f"{template_with_org['id']}",
        "landing_page_id": f"{uuid4()}"
    }

    response_camp = client.post("/campaigns/", json=payload)
    data_camp = response_camp.json()

    payload_schedule = {
        "start_time": "2027-09-01T15:00:00Z"
    }
    payload_schedule_past = {
        "start_time": "2025-09-01T15:00:00Z"
    }

    response_past = client.post(f"/campaigns/{data_camp['id']}/schedule", json=payload_schedule_past)
    assert response_past.status_code == 400

    wrong_campaign_id = uuid4()
    response_wrong_campaign = client.post(f"/campaigns/{wrong_campaign_id}/schedule",
                                          json=payload_schedule)
    assert response_wrong_campaign.status_code == 404

    response_schedule = client.post(f"/campaigns/{data_camp['id']}/schedule", json=payload_schedule)
    assert response_schedule.status_code == 200
    assert response_schedule.json()['status'] == CampaignStatus.Scheduled.value


def test_add_employee(client, template_with_organization):
    template_with_org, emp_id = template_with_organization

    payload = {
        "name": "TestCampaign",
        "organization_id": f"{template_with_org['organization_id']}",
        "template_id": f"{template_with_org['id']}",
        "landing_page_id": f"{uuid4()}"
    }

    response_camp = client.post("/campaigns/", json=payload)









