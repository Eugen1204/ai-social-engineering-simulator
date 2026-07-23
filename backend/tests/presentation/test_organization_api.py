import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from social_engineering_simulator.application.services.exception_create_organization import DuplicateDepartmentsError
from social_engineering_simulator.presentation.main import app


client = TestClient(app)


def test_create_organization():
    payload = {
        "name": "TestOrg",
        "industry": "IT Company",
        "departments": ["HR", "IT"]
    }

    response = client.post("/organization", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "TestOrg"
    assert data["industry"] == "IT Company"
    assert "departments" in data
    assert len(data["departments"]) == 2


def test_create_with_duplicate():
    payload = {
        "name": "TestOrg",
        "industry": "IT Company",
        "departments": ["HR", "HR"]
    }

    response = client.post("/organization", json=payload)

    assert response.status_code == 409

    data = response.json()
    assert "duplicate" in data["detail"].lower()


def test_create_with_wrong_industry():
    payload = {
        "name": "TestOrg",
        "industry": "WROOONG",
        "departments": ["HR", "IT"]
    }

    response = client.post("/organization", json=payload)

    assert response.status_code == 400


def test_invalid_json():
    payload = {
        "industry": "IT Company",
        "departments": ["HR", "IT"]
    }

    response = client.post("/organization", json=payload)

    assert response.status_code == 422






