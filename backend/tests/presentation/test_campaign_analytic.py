from datetime import datetime, UTC
from uuid import UUID

from social_engineering_simulator.application.dto.create_campaign import ClickCampaignEmployeeRequest
from social_engineering_simulator.application.services.create_campaign import ExecuteCampaignService, \
    ClickCampaignEmployeeService


def test_get_campaign_analytic(client_with_repos, created_organization, created_campaign_with_emp, created_campaign,
                               created_employee_fabric):
    client, _, repo_org, repo_events, repo_campaign = client_with_repos

    campaign_id = created_campaign['id']
    organization_id = created_organization['id']

    client.post(f"campaigns/{campaign_id}/start")

    emp_1 = created_employee_fabric(name="Test One", email="ecev@mdwf.ci")
    emp_2 = created_employee_fabric(name="Test Twmmo", email="eceev@mdewf.ci")
    emp_3 = created_employee_fabric(name="Test Three", email="ece11cev@mdewf.ci")

    service = ExecuteCampaignService(repo_campaign=repo_campaign, repo_org=repo_org, repo_event=repo_events)

    service.execute(campaign_id=UUID(campaign_id), organization_id=UUID(organization_id),
                    now=datetime(2027, 10, 10, 10, 10, tzinfo=UTC))

    response = client.get(f"campaigns/{campaign_id}/dashboard?organization_id={organization_id}")

    assert response.status_code == 200
    assert response.json()['sent_count'] == 4
    assert response.json()['total_employees'] == 4

    service_click = ClickCampaignEmployeeService(repo_campaign=repo_campaign,
                                                 repo_org=repo_org,
                                                 repo_event=repo_events)
    request_click = ClickCampaignEmployeeRequest(campaign_id=UUID(campaign_id),
                                                 organization_id=UUID(organization_id),
                                                 employee_id=UUID(emp_1['id']),
                                                 click_at=datetime(2026, 10, 10, 10, 10, tzinfo=UTC))
    service_click.execute(request_click)

    request_click = ClickCampaignEmployeeRequest(campaign_id=UUID(campaign_id),
                                                 organization_id=UUID(organization_id),
                                                 employee_id=UUID(emp_2['id']),
                                                 click_at=datetime(2026, 10, 10, 10, 10, tzinfo=UTC))
    service_click.execute(request_click)

    request_click = ClickCampaignEmployeeRequest(campaign_id=UUID(campaign_id),
                                                 organization_id=UUID(organization_id),
                                                 employee_id=UUID(emp_3['id']),
                                                 click_at=datetime(2026, 10, 10, 10, 10, tzinfo=UTC))
    service_click.execute(request_click)

    response = client.get(f"campaigns/{campaign_id}/dashboard?organization_id={organization_id}")

    assert response.status_code == 200
    assert response.json()['clicked_employee_count'] == 3
