from uuid import uuid4, UUID

import pytest
from starlette.testclient import TestClient

from social_engineering_simulator.infrastructure.persistence.in_memory.campaign_repository import CampaignRepoInMemory
from social_engineering_simulator.infrastructure.persistence.in_memory.organization_repository import \
    OrganizationRepoInMemory
from social_engineering_simulator.presentation.api.v1.dependencies import get_repository_campaign, \
    get_organization_repository
from social_engineering_simulator.presentation.main import app


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


@pytest.fixture()
def organization(client):
    payload = {
        "name": "TestOrg2",
        "industry": "IT Company",
        "departments": ["HR", "IT"]
    }

    response = client.post("/organizations/", json=payload)
    data = response.json()

    return data


@pytest.fixture()
def employee_in_organization(organization, client):
    payload = {
        "name": "Eugen",
        "email": "blablabla@gmail.com",
        "dep_name": "IT",
        "org_id": organization["id"]
    }

    response = client.post(f"/organizations/{organization['id']}/employees", json=payload)

    return response.json()


def test_get_employee(organization, client, employee_in_organization):
    response = client.get(f"/organizations/{organization['id']}/employees/{employee_in_organization['id']}")

    assert response.status_code == 200

    response = client.get(f"/organizations/{uuid4()}/employees/{employee_in_organization['id']}")

    assert response.status_code == 404

    response = client.get(f"/organizations/{organization['id']}/employees/{uuid4()}")

    assert response.status_code == 404


def test_add_campaign_employee(client, organization, employee_in_organization):
    payload = {
        "name": "TestCampaign",
        "organization_id": f"{organization['id']}",
        "template_id": f"{uuid4()}",
        "landing_page_id": f"{uuid4()}"
    }

    payload_2 = {
        "name": "TestCampaign",
        "organization_id": f"{uuid4()}",
        "template_id": f"{uuid4()}",
        "landing_page_id": f"{uuid4()}"
    }

    response = client.post("/campaigns/", json=payload)

    campaign_data = response.json()

    assert response.status_code == 201

    assert employee_in_organization['org_id'] == organization['id']

    wrong_response = client.post("/campaigns/", json=payload_2)

    assert wrong_response.status_code == 404

    response_wrong_employee = client.post(f"/campaigns/{campaign_data['id']}/employees/{uuid4()}")

    assert response_wrong_employee.status_code == 404

    add_emp_response = client.post(f"/campaigns/{campaign_data['id']}/employees/{employee_in_organization['id']}")

    assert add_emp_response.status_code == 201

    add_emp_response = client.post(f"/campaigns/{campaign_data['id']}/employees/{employee_in_organization['id']}")

    assert add_emp_response.status_code == 409

    del_emp_response = client.delete(f"/campaigns/{campaign_data['id']}/employees/{employee_in_organization['id']}")

    assert del_emp_response.status_code == 204

    del_emp_response = client.post(
        f"/campaigns/{campaign_data['id']}/employees/{employee_in_organization['id']}/delete")

    assert del_emp_response.status_code == 404
