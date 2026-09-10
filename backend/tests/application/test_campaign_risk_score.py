from datetime import datetime, UTC
from uuid import uuid4

import pytest

from social_engineering_simulator.application.dto.create_campaign import ClickCampaignEmployeeRequest, \
    EmployeeResultRequest, OpenTemplateCampaignRequest
from social_engineering_simulator.application.services.create_campaign import ExecuteCampaignService, \
    ClickCampaignEmployeeService, GetCampaignEmployeeResultService, OpenCampaignEmployeeService, GetCampaignRiskRanking
from social_engineering_simulator.application.services.exceptions_create_campaign import EmployeeNotInCampaignError, \
    CampaignNotFoundError, CampaignIsNotRunningError, CampaignResultsNotAvailableError
from social_engineering_simulator.domain.organizations.campaign.exceptions import EmployeeNotFoundInCampaign
from social_engineering_simulator.domain.organizations.department.employee.value_object import EmployeeName, Email
from social_engineering_simulator.domain.organizations.department.value_object import DepartmentName
from social_engineering_simulator.domain.organizations.exceptions import OrganizationNotFoundError
from social_engineering_simulator.infrastructure.persistence.in_memory.campaign_event_repository import \
    CampaignEventRepositoryInMemory


def test_risk_score_campaign(employee_in_campaign, application_organization):
    org, repo_org = application_organization
    camp, repo_camp = employee_in_campaign
    repo_event = CampaignEventRepositoryInMemory()

    camp.start()

    service = ExecuteCampaignService(repo_campaign=repo_camp, repo_org=repo_org, repo_event=repo_event)

    result = service.execute(campaign_id=camp.id, organization_id=org.id, now=datetime(2027, 1, 1, 10, 10, tzinfo=UTC))

    assert result.sent_count == 3

    click_at = datetime(2027, 1, 1, 11, 10, tzinfo=UTC)

    employees_with_sent_template = result.employees

    service_click = ClickCampaignEmployeeService(repo_campaign=repo_camp, repo_org=repo_org, repo_event=repo_event)

    request_click = ClickCampaignEmployeeRequest(campaign_id=camp.id,
                                                 organization_id=org.id,
                                                 employee_id=employees_with_sent_template[0].employee_id,
                                                 click_at=click_at)

    result_click = service_click.execute(request=request_click)

    assert result_click.clicked_at == click_at

    assert camp.employees[employees_with_sent_template[0].employee_id].clicked_at[0] \
           == datetime(2027, 1, 1, 11, 10, tzinfo=UTC)

    request_2 = ClickCampaignEmployeeRequest(campaign_id=camp.id,
                                             organization_id=org.id,
                                             employee_id=employees_with_sent_template[0].employee_id,
                                             click_at=datetime(2027, 1, 1, 12, 10, tzinfo=UTC))

    service_click.execute(request=request_2)

    assert camp.employees[employees_with_sent_template[0].employee_id].clicked_at[1] \
           == datetime(2027, 1, 1, 12, 10, tzinfo=UTC)

    service = GetCampaignEmployeeResultService(repo_campaign=repo_camp, repo_org=repo_org)

    emp = camp.get_employee(employees_with_sent_template[0].employee_id)

    request = EmployeeResultRequest(organization_id=org.id,
                                    campaign_id=camp.id,
                                    employee_id=emp.employee_id)

    result = service.execute(request)

    # 0.1 + 0.3 + 0.05 (sent_score + first_click_score + additional_clicks_score)
    assert result.risk_score == 0.45

    service_2 = OpenCampaignEmployeeService(repo_campaign=repo_camp, repo_org=repo_org, repo_event=repo_event)

    request_2 = OpenTemplateCampaignRequest(campaign_id=camp.id,
                                            organization_id=org.id,
                                            employee_id=emp.employee_id,
                                            open_at=datetime(2026, 10, 10, 10, 10, tzinfo=UTC))

    result_2 = service_2.execute(request_2)

    assert result_2.opened_at == datetime(2026, 10, 10, 10, 10, tzinfo=UTC)

    result = service.execute(request)

    assert result.risk_score == pytest.approx(0.75)

    service_click.execute(request=request_click)

    result = service.execute(request)

    assert result.risk_score == pytest.approx(0.8)

    service_click.execute(request=request_click)

    result = service.execute(request)

    assert result.risk_score == pytest.approx(0.8)

    request = EmployeeResultRequest(organization_id=org.id,
                                    campaign_id=camp.id,
                                    employee_id=uuid4())

    with pytest.raises(EmployeeNotFoundInCampaign):
        service.execute(request)

    request = EmployeeResultRequest(organization_id=uuid4(),
                                    campaign_id=camp.id,
                                    employee_id=emp.employee_id)

    with pytest.raises(OrganizationNotFoundError):
        service.execute(request)

    request = EmployeeResultRequest(organization_id=org.id,
                                    campaign_id=uuid4(),
                                    employee_id=emp.employee_id)

    with pytest.raises(CampaignNotFoundError):
        service.execute(request)


def test_all_cycle_get_employee_risk_score(employee_in_campaign, application_organization):
    org, repo_org = application_organization
    camp, repo_camp = employee_in_campaign
    repo_event = CampaignEventRepositoryInMemory()

    camp.start()

    service_sent = ExecuteCampaignService(repo_campaign=repo_camp, repo_org=repo_org, repo_event=repo_event)

    result_sent = service_sent.execute(campaign_id=camp.id, organization_id=org.id,
                                       now=datetime(2027, 1, 1, 10, 10, tzinfo=UTC))

    assert result_sent.sent_count == 3

    emp = camp.get_employee(result_sent.employees[0].employee_id)

    service_get_result = GetCampaignEmployeeResultService(repo_campaign=repo_camp, repo_org=repo_org)

    request = EmployeeResultRequest(organization_id=org.id,
                                    campaign_id=camp.id,
                                    employee_id=emp.employee_id)

    result_score = service_get_result.execute(request)

    # template just sent
    assert result_score.risk_score == 0.1

    service_open = OpenCampaignEmployeeService(repo_campaign=repo_camp, repo_org=repo_org, repo_event=repo_event)

    request_open = OpenTemplateCampaignRequest(campaign_id=camp.id,
                                               organization_id=org.id,
                                               employee_id=emp.employee_id,
                                               open_at=datetime(2026, 10, 10, 10, 10, tzinfo=UTC))

    service_open.execute(request_open)

    result_score = service_get_result.execute(request)

    # the template was opened
    assert result_score.risk_score == 0.4

    service_click = ClickCampaignEmployeeService(repo_campaign=repo_camp, repo_org=repo_org, repo_event=repo_event)

    request_click = ClickCampaignEmployeeRequest(campaign_id=camp.id,
                                                 organization_id=org.id,
                                                 employee_id=emp.employee_id,
                                                 click_at=datetime(2026, 10, 10, 10, 10, tzinfo=UTC))

    service_click.execute(request=request_click)

    service_click.execute(request=request_click)

    result_score = service_get_result.execute(request)

    # the template was opened and 2 clicks
    assert result_score.risk_score == 0.75

    emp.mark_credentials_submitted(datetime(2026, 10, 10, 10, 10, tzinfo=UTC))

    service_click.execute(request=request_click)

    result_score = service_get_result.execute(request)

    # the template was opened and 2 clicks and mark credentials submitted
    assert result_score.risk_score == 1.0


def test_get_campaign_risk_score(employee_in_campaign, application_organization):
    org, repo_org = application_organization
    camp, repo_camp = employee_in_campaign
    repo_event = CampaignEventRepositoryInMemory()
    emp_4 = org.add_employee(name=EmployeeName("Emp four"), email=Email("efefe@mwdem.co"),
                             dep_name=DepartmentName("HR"))

    camp.start()

    service_sent = ExecuteCampaignService(repo_campaign=repo_camp, repo_org=repo_org, repo_event=repo_event)

    result_sent = service_sent.execute(campaign_id=camp.id, organization_id=org.id,
                                       now=datetime(2027, 1, 1, 10, 10, tzinfo=UTC))

    emp_1 = camp.get_employee(result_sent.employees[0].employee_id)

    emp_2 = camp.get_employee(result_sent.employees[1].employee_id)

    emp_3 = camp.get_employee(result_sent.employees[2].employee_id)

    camp.assign_employee(emp_4.id)

    emp_2.mark_opened(datetime(2027, 1, 1, 10, 10, tzinfo=UTC))

    emp_3.mark_opened(datetime(2027, 1, 1, 11, 10, tzinfo=UTC))

    emp_3.mark_clicked(datetime(2027, 1, 1, 11, 10, tzinfo=UTC))

    emp_3.mark_credentials_submitted(datetime(2027, 1, 1, 12, 10, tzinfo=UTC))

    service_get_cam_risk = GetCampaignRiskRanking(repo_campaign=repo_camp,
                                                  repo_org=repo_org)

    response_get_risk = service_get_cam_risk.execute(organization_id=org.id,
                                                     campaign_id=camp.id)

    assert len(response_get_risk) == 3

    assert response_get_risk[0].risk_score == 1.0

    assert response_get_risk[1].risk_score == 0.4

    assert response_get_risk[2].risk_score == 0.1

    assert len(camp.employees) == 4


def test_get_same_risk_employee(employee_in_campaign, application_organization):
    org, repo_org = application_organization
    camp, repo_camp = employee_in_campaign
    repo_event = CampaignEventRepositoryInMemory()

    camp.start()

    service_sent = ExecuteCampaignService(repo_campaign=repo_camp, repo_org=repo_org, repo_event=repo_event)

    result_sent = service_sent.execute(campaign_id=camp.id, organization_id=org.id,
                                       now=datetime(2027, 1, 1, 10, 10, tzinfo=UTC))

    emp_1 = camp.get_employee(result_sent.employees[0].employee_id)
    emp_2 = camp.get_employee(result_sent.employees[1].employee_id)
    emp_3 = camp.get_employee(result_sent.employees[2].employee_id)

    emp_1.mark_opened(datetime(2027, 1, 1, 10, 10, tzinfo=UTC))
    emp_2.mark_opened(datetime(2027, 1, 1, 10, 10, tzinfo=UTC))

    emp_1.mark_credentials_submitted(datetime(2027, 1, 1, 10, 10, tzinfo=UTC))
    emp_2.mark_credentials_submitted(datetime(2027, 1, 1, 10, 10, tzinfo=UTC))

    service_get_cam_risk = GetCampaignRiskRanking(repo_campaign=repo_camp,
                                                  repo_org=repo_org)

    response_get_risk = service_get_cam_risk.execute(organization_id=org.id,
                                                     campaign_id=camp.id)

    assert len(response_get_risk) == 3

    response_get_risk = service_get_cam_risk.execute(organization_id=org.id,
                                                     campaign_id=camp.id)

    assert response_get_risk[0].risk_score == 1.0
    assert response_get_risk[1].risk_score == 1.0
    assert response_get_risk[2].risk_score == 0.1


def test_get_risk_score_raises(employee_in_campaign, application_organization):
    org, repo_org = application_organization
    camp, repo_camp = employee_in_campaign
    repo_event = CampaignEventRepositoryInMemory()

    service_get_cam_risk = GetCampaignRiskRanking(repo_campaign=repo_camp,
                                                  repo_org=repo_org)

    with pytest.raises(CampaignResultsNotAvailableError):
        service_get_cam_risk.execute(organization_id=org.id,
                                     campaign_id=camp.id)

    camp.start()

    service_sent = ExecuteCampaignService(repo_campaign=repo_camp, repo_org=repo_org, repo_event=repo_event)

    service_sent.execute(campaign_id=camp.id, organization_id=org.id,
                         now=datetime(2027, 1, 1, 10, 10, tzinfo=UTC))

    with pytest.raises(CampaignNotFoundError):
        service_get_cam_risk.execute(organization_id=org.id,
                                     campaign_id=uuid4())

    with pytest.raises(OrganizationNotFoundError):
        service_get_cam_risk.execute(organization_id=uuid4(),
                                     campaign_id=camp.id)


def test_with_2_campaign_get_risk_score(employee_in_campaign, application_organization, make_draft_campaigns):
    org, repo_org = application_organization
    camp_1, repo_camp = employee_in_campaign
    repo_event = CampaignEventRepositoryInMemory()
    camp_2 = make_draft_campaigns(name="Camp_2", with_employee=True, organization_id=org.id)
    repo_camp.save(camp_2)

    camp_2.start()
    camp_1.start()

    service_sent = ExecuteCampaignService(repo_campaign=repo_camp, repo_org=repo_org, repo_event=repo_event)

    result_sent_camp_1 = service_sent.execute(campaign_id=camp_1.id, organization_id=org.id,
                                              now=datetime(2027, 1, 1, 10, 10, tzinfo=UTC))

    result_sent_camp_2 = service_sent.execute(campaign_id=camp_2.id, organization_id=org.id,
                                              now=datetime(2027, 1, 1, 10, 10, tzinfo=UTC))

    emp_1 = camp_1.get_employee(result_sent_camp_1.employees[0].employee_id)
    emp_2 = camp_1.get_employee(result_sent_camp_1.employees[1].employee_id)
    emp_3 = camp_1.get_employee(result_sent_camp_1.employees[2].employee_id)

    emp_1.mark_opened()
    emp_1.mark_credentials_submitted()
    emp_2.mark_opened()
    emp_2.mark_credentials_submitted()
    emp_3.mark_opened()
    emp_3.mark_credentials_submitted()

    service_get_cam_risk = GetCampaignRiskRanking(repo_campaign=repo_camp,
                                                  repo_org=repo_org)

    camp_2_result = service_get_cam_risk.execute(organization_id=org.id,
                                                 campaign_id=camp_2.id)
    assert len(camp_2_result) == 1

    assert sum([e.risk_score for e in camp_2_result]) == 0.1

    camp_1_result = service_get_cam_risk.execute(organization_id=org.id,
                                                 campaign_id=camp_1.id)

    assert sum([e.risk_score for e in camp_1_result]) == 3.0

