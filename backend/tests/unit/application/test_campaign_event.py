from datetime import datetime, UTC
from uuid import uuid4

import pytest

from social_engineering_simulator.application.dto.create_campaign import OpenTemplateCampaignRequest, \
    ClickCampaignEmployeeRequest
from social_engineering_simulator.application.services.create_campaign import ExecuteCampaignService, \
    OpenCampaignEmployeeService, ClickCampaignEmployeeService, GetCampaignEmployeeTimeline
from social_engineering_simulator.domain.organizations.campaign.exceptions import EmployeeNotFoundInCampaign
from social_engineering_simulator.domain.organizations.campaign.value_object import EventType
from social_engineering_simulator.infrastructure.persistence.in_memory.campaign_event_repository import \
    CampaignEventRepositoryInMemory


def test_event_persistence(employee_in_campaign, application_organization):
    org, repo_org = application_organization
    camp, repo_camp = employee_in_campaign
    repo_event = CampaignEventRepositoryInMemory()

    camp.start()

    service_sent = ExecuteCampaignService(repo_campaign=repo_camp, repo_org=repo_org, repo_event=repo_event)

    result_sent = service_sent.execute(campaign_id=camp.id, organization_id=org.id,
                                       now=datetime(2027, 1, 1, 10, 10, tzinfo=UTC))
    emp_1 = camp.get_employee(result_sent.employees[0].employee_id)

    assert result_sent.sent_count == 3

    assert len(repo_event.get_by_campaign_id(campaign_id=camp.id)) == 3
    assert len(repo_event.get_by_employee_id(employee_id=emp_1.employee_id)) == 1
    assert repo_event.get_by_employee_id(employee_id=emp_1.employee_id)[0].event_type == EventType.EmailSent

    service_opened = OpenCampaignEmployeeService(repo_campaign=repo_camp, repo_org=repo_org, repo_event=repo_event)

    request_opened = OpenTemplateCampaignRequest(campaign_id=camp.id,
                                                 organization_id=org.id,
                                                 employee_id=emp_1.employee_id,
                                                 open_at=datetime.now(UTC))
    result_opened = service_opened.execute(request_opened)

    assert result_opened.employee_id == emp_1.employee_id

    assert len(repo_event.get_by_employee_id(employee_id=emp_1.employee_id)) == 2

    service_click = ClickCampaignEmployeeService(repo_campaign=repo_camp, repo_org=repo_org, repo_event=repo_event)

    request_click = ClickCampaignEmployeeRequest(campaign_id=camp.id,
                                                 organization_id=org.id,
                                                 employee_id=emp_1.employee_id,
                                                 click_at=datetime.now(UTC))

    service_click.execute(request_click)

    assert len(repo_event.get_by_employee_id(employee_id=emp_1.employee_id)) == 3


def test_get_employee_timeline(employee_in_campaign, application_organization):
    org, repo_org = application_organization
    camp, repo_camp = employee_in_campaign
    repo_event = CampaignEventRepositoryInMemory()

    camp.start()

    service_sent = ExecuteCampaignService(repo_campaign=repo_camp, repo_org=repo_org, repo_event=repo_event)

    # first event
    result_sent = service_sent.execute(campaign_id=camp.id, organization_id=org.id,
                                       now=datetime(2027, 1, 1, 10, 10, tzinfo=UTC))

    emp_1 = camp.get_employee(result_sent.employees[0].employee_id)

    service_opened = OpenCampaignEmployeeService(repo_campaign=repo_camp, repo_org=repo_org, repo_event=repo_event)

    # second event
    request_opened = OpenTemplateCampaignRequest(campaign_id=camp.id,
                                                 organization_id=org.id,
                                                 employee_id=emp_1.employee_id,
                                                 open_at=datetime(2027, 1, 1, 10, 12, tzinfo=UTC))

    service_opened.execute(request_opened)

    service_click = ClickCampaignEmployeeService(repo_campaign=repo_camp, repo_org=repo_org, repo_event=repo_event)

    # fourth event
    request_click = ClickCampaignEmployeeRequest(campaign_id=camp.id,
                                                 organization_id=org.id,
                                                 employee_id=emp_1.employee_id,
                                                 click_at=datetime(2027, 1, 1, 10, 15, tzinfo=UTC))

    service_click.execute(request_click)

    # third event
    request_click = ClickCampaignEmployeeRequest(campaign_id=camp.id,
                                                 organization_id=org.id,
                                                 employee_id=emp_1.employee_id,
                                                 click_at=datetime(2027, 1, 1, 10, 13, tzinfo=UTC))

    service_click.execute(request_click)

    service_get_timeline = GetCampaignEmployeeTimeline(repo_campaign=repo_camp,
                                                       repo_org=repo_org,
                                                       repo_event=repo_event)

    result_get_timeline = service_get_timeline.execute(org_id=org.id,
                                                       campaign_id=camp.id,
                                                       employee_id=emp_1.employee_id)
    print(result_get_timeline)

    assert result_get_timeline[0].event_type == EventType.EmailSent.value

    assert result_get_timeline[0].occurred_at == datetime(2027, 1, 1, 10, 10, tzinfo=UTC)

    assert result_get_timeline[1].event_type == EventType.EmailOpened.value

    assert result_get_timeline[1].occurred_at == datetime(2027, 1, 1, 10, 12, tzinfo=UTC)

    assert result_get_timeline[2].occurred_at == datetime(2027, 1, 1, 10, 13, tzinfo=UTC)

    assert result_get_timeline[2].event_type == EventType.LinkClicked.value

    assert result_get_timeline[3].occurred_at == datetime(2027, 1, 1, 10, 15, tzinfo=UTC)

    assert result_get_timeline[3].event_type == EventType.LinkClicked.value


def test_isolation_campaign(employee_in_campaign, application_organization, make_draft_campaigns):
    org, repo_org = application_organization
    camp_1, repo_camp = employee_in_campaign
    repo_event = CampaignEventRepositoryInMemory()

    camp_1.start()

    camp_2 = make_draft_campaigns(name="Test 2")

    repo_camp.save(camp_2)

    camp_2.start()

    service_sent = ExecuteCampaignService(repo_campaign=repo_camp, repo_org=repo_org, repo_event=repo_event)

    result_sent_1 = service_sent.execute(campaign_id=camp_1.id, organization_id=org.id,
                                         now=datetime(2027, 1, 1, 10, 10, tzinfo=UTC))

    result_sent_2 = service_sent.execute(campaign_id=camp_2.id, organization_id=org.id,
                                         now=datetime(2027, 1, 1, 10, 10, tzinfo=UTC))

    emp = camp_1.get_employee(result_sent_1.employees[0].employee_id)

    service_opened = OpenCampaignEmployeeService(repo_campaign=repo_camp, repo_org=repo_org, repo_event=repo_event)

    request_opened = OpenTemplateCampaignRequest(campaign_id=camp_1.id,
                                                 organization_id=org.id,
                                                 employee_id=emp.employee_id,
                                                 open_at=datetime(2027, 1, 1, 10, 12, tzinfo=UTC))

    service_opened.execute(request_opened)

    service_click = ClickCampaignEmployeeService(repo_campaign=repo_camp, repo_org=repo_org, repo_event=repo_event)

    request_click = ClickCampaignEmployeeRequest(campaign_id=camp_2.id,
                                                 organization_id=org.id,
                                                 employee_id=emp.employee_id,
                                                 click_at=datetime(2027, 1, 1, 10, 15, tzinfo=UTC))

    service_click.execute(request_click)

    service_get_timeline = GetCampaignEmployeeTimeline(repo_campaign=repo_camp,
                                                       repo_org=repo_org,
                                                       repo_event=repo_event)

    result_get_timeline_1_campaign = service_get_timeline.execute(org_id=org.id,
                                                                  campaign_id=camp_1.id,
                                                                  employee_id=emp.employee_id)

    print(result_get_timeline_1_campaign)

    assert len(result_get_timeline_1_campaign) == 2

    assert result_get_timeline_1_campaign[0].event_type == EventType.EmailSent.value

    assert result_get_timeline_1_campaign[1].event_type == EventType.EmailOpened.value

    result_get_timeline_2_campaign = service_get_timeline.execute(org_id=org.id,
                                                                  campaign_id=camp_2.id,
                                                                  employee_id=emp.employee_id)

    assert len(result_get_timeline_2_campaign) == 2

    assert result_get_timeline_2_campaign[0].event_type == EventType.EmailSent.value

    assert result_get_timeline_2_campaign[1].event_type == EventType.LinkClicked.value

    with pytest.raises(EmployeeNotFoundInCampaign):
        service_get_timeline.execute(org_id=org.id,
                                     campaign_id=camp_2.id,
                                     employee_id=uuid4())
