from typing import Callable
from uuid import uuid4, UUID

import pytest
from starlette.testclient import TestClient

from social_engineering_simulator.domain.email_template.services.template_engine import EngineTemplate
from social_engineering_simulator.domain.organizations.department.employee.entity import Employee
from social_engineering_simulator.domain.organizations.department.employee.value_object import EmployeeName
from social_engineering_simulator.infrastructure.persistence.in_memory.campaign_event_repository import \
    CampaignEventRepositoryInMemory
from social_engineering_simulator.infrastructure.persistence.in_memory.campaign_repository import CampaignRepoInMemory
from social_engineering_simulator.infrastructure.persistence.in_memory.organization_repository import \
    OrganizationRepoInMemory
from social_engineering_simulator.infrastructure.persistence.in_memory.template_repository import \
    TemplateRepositoryInMemory
from social_engineering_simulator.presentation.api.v1.dependencies import get_repository_campaign, \
    get_organization_repository, get_repository_template, get_engine_template, get_repository_events
from social_engineering_simulator.presentation.main import app


@pytest.fixture()
def client_with_repos():
    repo_campaign = CampaignRepoInMemory()
    repo_org = OrganizationRepoInMemory()
    repo_template = TemplateRepositoryInMemory()
    repo_events = CampaignEventRepositoryInMemory()
    app.dependency_overrides[get_repository_campaign] = lambda: repo_campaign
    app.dependency_overrides[get_organization_repository] = lambda: repo_org
    app.dependency_overrides[get_repository_template] = lambda: repo_template
    app.dependency_overrides[get_engine_template] = lambda: EngineTemplate()
    app.dependency_overrides[get_repository_events] = lambda: repo_events

    client = TestClient(app)
    yield client, repo_template, repo_org, repo_events, repo_campaign
    app.dependency_overrides.clear()


@pytest.fixture
def created_organization(client_with_repos):
    client, _, _, _, _ = client_with_repos
    response = client.post("/organizations/", json={
        "name": "TestOrg",
        "industry": "IT Company",
        "departments": ["HR"]
    })
    return response.json()


@pytest.fixture
def created_template(client_with_repos, created_organization):
    client, _, _, _, _ = client_with_repos
    response = client.post(
        f"/organizations/{created_organization['id']}/templates",
        json={"name": "Test", "subject": "Hi {{name}}", "content": "Hello {{name}}"}
    )
    return response.json()


@pytest.fixture
def created_campaign(client_with_repos, created_organization, created_template):
    client, _, _, _, _ = client_with_repos
    payload = {
        "name": "Fishing",
        "organization_id": created_organization['id'],
        "template_id": created_template['id'],
        "landing_page_id": str(uuid4())
    }

    response = client.post("/campaigns/", json=payload)
    response.raise_for_status()

    return response.json()


@pytest.fixture()
def created_employee(client_with_repos, created_organization, created_campaign):
    client, _, _, _, _ = client_with_repos
    "/{organization_id}/employees"

    payload = {
        "name": "Test Test",
        "email": "dfvdsv@gmail.com",
        "dep_name": "HR",
    }

    response = client.post(f"/organizations/{created_organization['id']}/employees", json=payload)

    return response.json()


@pytest.fixture()
def created_campaign_with_emp(client_with_repos, created_employee, created_campaign):
    client, _, _, _, _ = client_with_repos
    response = client.post(f"campaigns/{created_campaign['id']}/employees/{created_employee['id']}")

    return response.json()


@pytest.fixture()
def created_employee_fabric(client_with_repos, created_organization, created_campaign):
    client, _, _, _, _ = client_with_repos

    def _make_employee_in_organization(name: str = "Test Test",
                                       email: str | None = None,
                                       dep_name: str = "HR",
                                       org_id: UUID | None = None,
                                       add_in_campaign: bool = True,
                                       campaign_id: UUID | None = None,
                                       **kwargs) -> dict:
        payload = {
                    "name": name,
                    "email": email,
                    "dep_name": dep_name,
                    **kwargs
                  }
        response = client.post(f"/organizations/{org_id or created_organization['id']}/employees", json=payload)
        response.raise_for_status()
        if add_in_campaign:
            cid = created_campaign['id'] if campaign_id is None else campaign_id
            resp = client.post(f"/campaigns/{cid}/employees/{response.json()['id']}")
            resp.raise_for_status()

        return response.json()

    return _make_employee_in_organization
