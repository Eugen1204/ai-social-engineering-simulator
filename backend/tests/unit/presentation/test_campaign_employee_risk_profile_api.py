from datetime import datetime, UTC
from uuid import UUID, uuid4

import pytest

from social_engineering_simulator.application.services.create_campaign import ExecuteCampaignService


@pytest.mark.asyncio
async def test_get_campaign_employee_profile_pr(client_with_repos, created_organization, created_campaign_with_emp,
                                                created_campaign,
                                                created_employee_factory):
    client, _, repo_org, repo_events, repo_campaign = client_with_repos

    campaign_id = created_campaign['id']
    organization_id = created_organization['id']

    client.post(f"campaigns/{campaign_id}/start")

    emp_1 = created_employee_factory(name="Test One", email="ecev@mdwf.ci")

    service = ExecuteCampaignService(repo_campaign=repo_campaign, repo_org=repo_org, repo_event=repo_events)

    await service.execute(campaign_id=UUID(campaign_id), organization_id=UUID(organization_id),
                          now=datetime(2027, 10, 10, 10, 10, tzinfo=UTC))

    response = client.get(f"campaigns/{campaign_id}/employees/{emp_1['id']}/risk-profile?organization_id="
                          f"{organization_id}")

    assert response.status_code == 200
    assert response.json()['is_sent'] is True
    assert response.json()['employee_id'] == emp_1['id']
    assert response.json()['event_count'] == 1

    response = client.get(f"campaigns/{uuid4()}/employees/{emp_1['id']}/risk-profile?organization_id="
                          f"{organization_id}")

    assert response.status_code == 404
