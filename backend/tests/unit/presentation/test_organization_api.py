# tests/presentation/test_organization_api.py
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from social_engineering_simulator.application.services.create_organization import CreateOrganizationService
from social_engineering_simulator.presentation.main import app
from social_engineering_simulator.presentation.api.v1.dependencies import get_organization_repository
from social_engineering_simulator.infrastructure.persistence.in_memory.organization_repository import \
    OrganizationRepoInMemory


@pytest.fixture
def client():
    """Фикстура для создания тестового клиента с InMemory-репозиторием."""
    repo = OrganizationRepoInMemory()
    app.dependency_overrides[get_organization_repository] = lambda: repo
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_create_organization(client):
    payload = {
        "name": "TestOrg",
        "industry": "IT Company",
        "departments": ["HR", "IT"]
    }

    response = client.post("/organizations/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "TestOrg"
    assert data["industry"] == "IT Company"
    assert data["departments"] == 2


def test_create_with_duplicate(client):
    payload = {
        "name": "TestOrg",
        "industry": "IT Company",
        "departments": ["HR", "HR"]
    }

    response = client.post("/organizations/", json=payload)

    assert response.status_code == 409


def test_create_with_wrong_industry(client):
    payload = {
        "name": "TestOrg",
        "industry": "WROOONG",
        "departments": ["HR", "IT"]
    }

    response = client.post("/organizations/", json=payload)

    assert response.status_code == 400


def test_invalid_json(client):
    payload = {
        "industry": "IT Company",
        "departments": ["HR", "IT"]
    }

    response = client.post("/organizations/", json=payload)

    assert response.status_code == 422


def test_get_organization(client):
    payload = {
        "name": "TestOrg",
        "industry": "IT Company",
        "departments": ["HR", "IT"]
    }

    response = client.post("/organizations/", json=payload)

    data = response.json()
    org_id = data["id"]
    response_get = client.get(f"/organizations/{org_id}")

    assert response_get.status_code == 200


def test_get_wrong_organization(client):

    response_get = client.get(f"/organizations/{uuid4()}")

    assert response_get.status_code == 404

