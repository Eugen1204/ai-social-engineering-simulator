from datetime import datetime, timezone
from uuid import UUID

from social_engineering_simulator.application.services.create_campaign import ExecuteCampaignService


def test_get_emp_timeline(client_with_repos, created_organization, created_campaign_with_emp, created_campaign,
                          created_employee):
    client, _, repo_org, repo_events, repo_campaign = client_with_repos

    campaign_id = created_campaign['id']

    client.post(f"campaigns/{campaign_id}/start")

    employee_id = created_employee['id']

    response = client.get(f"campaigns/{campaign_id}/employees/{employee_id}/timeline?org_id="
                          f"{created_organization['id']}")

    assert response.status_code == 200

    assert response.json() == []


def test_get_campaign_employees_risk(client_with_repos, created_organization, created_campaign_with_emp,
                                     created_campaign,
                                     created_employee):
    client, _, repo_org, repo_events, repo_campaign = client_with_repos

    campaign_id = created_campaign['id']

    employee_id = created_employee['id']

    organization_id = created_organization['id']

    client.post(f"campaigns/{campaign_id}/start")

    execute_service = ExecuteCampaignService(
        repo_campaign=repo_campaign,
        repo_org=repo_org,
        repo_event=repo_events
    )

    execute_service.execute(
        campaign_id=UUID(campaign_id),
        organization_id=UUID(organization_id),
        now=datetime(2027, 1, 1, 10, 0, tzinfo=timezone.utc)
    )

    response = client.get(f"/campaigns/{campaign_id}/employees/risk-ranking?organization_id="
                          f"{created_organization['id']}")

    assert response.status_code == 200




