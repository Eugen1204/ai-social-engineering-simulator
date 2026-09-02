from uuid import uuid4

import pytest
from starlette.testclient import TestClient

from social_engineering_simulator.domain.email_template.services.template_engine import EngineTemplate
from social_engineering_simulator.infrastructure.persistence.in_memory.campaign_repository import CampaignRepoInMemory
from social_engineering_simulator.infrastructure.persistence.in_memory.organization_repository import \
    OrganizationRepoInMemory
from social_engineering_simulator.infrastructure.persistence.in_memory.template_repository import \
    TemplateRepositoryInMemory
from social_engineering_simulator.presentation.api.v1.dependencies import get_repository_campaign, \
    get_organization_repository, get_repository_template, get_engine_template
from social_engineering_simulator.presentation.main import app


@pytest.fixture
def client():
    """Фикстура для создания тестового клиента с InMemory-репозиторием."""
    repo_campaign = CampaignRepoInMemory()
    repo_org = OrganizationRepoInMemory()
    repo_template = TemplateRepositoryInMemory()
    app.dependency_overrides[get_repository_campaign] = lambda: repo_campaign
    app.dependency_overrides[get_organization_repository] = lambda: repo_org
    app.dependency_overrides[get_repository_template] = lambda: repo_template
    app.dependency_overrides[get_engine_template] = lambda: EngineTemplate()

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_add_template(client):
    payload = {
        "name": "TestOrg",
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

    assert response.status_code == 201

    variables = {
        "variables": {
            "name": "Eugen",
            "link": "not_fishing.com"
        }
    }

    response = client.post(f"organizations/{data_org['id']}/templates/{response.json()['id']}/preview", json=variables)

    print(response.json())
    assert response.status_code == 200






