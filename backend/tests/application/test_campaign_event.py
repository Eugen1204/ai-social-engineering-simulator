from datetime import datetime, UTC

from social_engineering_simulator.application.dto.create_campaign import OpenTemplateCampaignRequest, \
    ClickCampaignEmployeeRequest
from social_engineering_simulator.application.services.create_campaign import ExecuteCampaignService, \
    OpenCampaignEmployeeService, ClickCampaignEmployeeService
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


