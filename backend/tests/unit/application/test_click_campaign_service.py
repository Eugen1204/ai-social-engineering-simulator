from datetime import datetime, UTC
from uuid import uuid4

import pytest

from social_engineering_simulator.application.dto.create_campaign import ClickCampaignEmployeeRequest
from social_engineering_simulator.application.services.create_campaign import ExecuteCampaignService, \
    ClickCampaignEmployeeService
from social_engineering_simulator.application.services.exceptions_create_campaign import CampaignIsNotRunningError
from social_engineering_simulator.domain.organizations.exceptions import OrganizationNotFoundError
from social_engineering_simulator.infrastructure.persistence.in_memory.campaign_event_repository import \
    CampaignEventRepositoryInMemory


def test_click_campaign(employee_in_campaign, application_organization):
    org, repo_org = application_organization
    camp, repo_camp = employee_in_campaign
    repo_event = CampaignEventRepositoryInMemory()

    camp.start()

    service = ExecuteCampaignService(repo_campaign=repo_camp, repo_org=repo_org, repo_event=repo_event)

    result = service.execute(campaign_id=camp.id, organization_id=org.id, now=datetime(2027, 1, 1, 10, 10, tzinfo=UTC))

    assert result.sent_count == 3

    click_at = datetime(2027, 1, 1, 11, 10, tzinfo=UTC)

    employees_with_sent_template = result.employees

    service = ClickCampaignEmployeeService(repo_campaign=repo_camp, repo_org=repo_org, repo_event=repo_event)

    request = ClickCampaignEmployeeRequest(campaign_id=camp.id,
                                           organization_id=org.id,
                                           employee_id=employees_with_sent_template[0].employee_id,
                                           click_at=click_at)

    result_click = service.execute(request=request)

    assert result_click.clicked_at == click_at

    assert camp.employees[employees_with_sent_template[0].employee_id].clicked_at[0]\
           == datetime(2027, 1, 1, 11, 10, tzinfo=UTC)

    request_2 = ClickCampaignEmployeeRequest(campaign_id=camp.id,
                                             organization_id=org.id,
                                             employee_id=employees_with_sent_template[0].employee_id,
                                             click_at=datetime(2027, 1, 1, 12, 10, tzinfo=UTC))

    service.execute(request=request_2)

    assert camp.employees[employees_with_sent_template[0].employee_id].clicked_at[1] \
           == datetime(2027, 1, 1, 12, 10, tzinfo=UTC)


def test_click_with_not_running_campaign(employee_in_campaign, application_organization):
    org, repo_org = application_organization
    camp, repo_camp = employee_in_campaign
    repo_event = CampaignEventRepositoryInMemory()

    camp.start()
    service = ExecuteCampaignService(repo_campaign=repo_camp, repo_org=repo_org, repo_event=repo_event)

    result = service.execute(campaign_id=camp.id, organization_id=org.id, now=datetime(2027, 1, 1, 10, 10, tzinfo=UTC))

    assert result.sent_count == 3

    click_at = datetime(2027, 1, 1, 11, 10, tzinfo=UTC)

    camp.finish()

    employees_with_sent_template = result.employees

    service = ClickCampaignEmployeeService(repo_campaign=repo_camp, repo_org=repo_org, repo_event=repo_event)

    request = ClickCampaignEmployeeRequest(campaign_id=camp.id,
                                           organization_id=org.id,
                                           employee_id=employees_with_sent_template[0].employee_id,
                                           click_at=click_at)

    with pytest.raises(CampaignIsNotRunningError):
        service.execute(request)


def test_click_with_wrong_org(employee_in_campaign, application_organization):
    org, repo_org = application_organization
    camp, repo_camp = employee_in_campaign
    repo_event = CampaignEventRepositoryInMemory()

    camp.start()
    service = ExecuteCampaignService(repo_campaign=repo_camp, repo_org=repo_org, repo_event=repo_event)

    result = service.execute(campaign_id=camp.id, organization_id=org.id, now=datetime(2027, 1, 1, 10, 10, tzinfo=UTC))

    assert result.sent_count == 3

    click_at = datetime(2027, 1, 1, 11, 10, tzinfo=UTC)

    employees_with_sent_template = result.employees

    service = ClickCampaignEmployeeService(repo_campaign=repo_camp, repo_org=repo_org, repo_event=repo_event)

    request = ClickCampaignEmployeeRequest(campaign_id=camp.id,
                                           organization_id=uuid4(),
                                           employee_id=employees_with_sent_template[0].employee_id,
                                           click_at=click_at)

    with pytest.raises(OrganizationNotFoundError):
        service.execute(request)
