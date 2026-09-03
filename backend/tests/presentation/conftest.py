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


@pytest.fixture()
def client_with_repos():
    repo_campaign = CampaignRepoInMemory()
    repo_org = OrganizationRepoInMemory()
    repo_template = TemplateRepositoryInMemory()
    app.dependency_overrides[get_repository_campaign] = lambda: repo_campaign
    app.dependency_overrides[get_organization_repository] = lambda: repo_org
    app.dependency_overrides[get_repository_template] = lambda: repo_template
    app.dependency_overrides[get_engine_template] = lambda: EngineTemplate()

    client = TestClient(app)
    yield client, repo_template, repo_org
    app.dependency_overrides.clear()


@pytest.fixture
def created_organization(client_with_repos):
    client, _, _ = client_with_repos
    response = client.post("/organizations/", json={
        "name": "TestOrg",
        "industry": "IT Company",
        "departments": ["HR"]
    })
    return response.json()


@pytest.fixture
def created_template(client_with_repos, created_organization):
    client, _, _ = client_with_repos
    response = client.post(
        f"/organizations/{created_organization['id']}/templates",
        json={"name": "Test", "subject": "Hi {{name}}", "content": "Hello {{name}}"}
    )
    return response.json()


@pytest.fixture
def created_campaign(client_with_repos, created_organization, created_template):
    client, _, _ = client_with_repos
    payload = {
        "name": "Fishing",
        "organization_id": created_organization['id'],
        "template_id": created_template['id'],
        "landing_page_id": str(uuid4())
    }

    response = client.post("/campaigns/", json=payload)

    return response.json()