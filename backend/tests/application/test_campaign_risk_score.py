from datetime import datetime, UTC
from uuid import uuid4

import pytest

from social_engineering_simulator.application.dto.create_campaign import ClickCampaignEmployeeRequest, \
    EmployeeResultRequest, OpenTemplateCampaignRequest
from social_engineering_simulator.application.services.create_campaign import ExecuteCampaignService, \
    ClickCampaignEmployeeService, GetCampaignEmployeeResultService, OpenCampaignEmployeeService
from social_engineering_simulator.application.services.exceptions_create_campaign import EmployeeNotInCampaignError, \
    CampaignNotFoundError, CampaignIsNotRunningError
from social_engineering_simulator.domain.organizations.campaign.exceptions import EmployeeNotFoundInCampaign
from social_engineering_simulator.domain.organizations.exceptions import OrganizationNotFoundError


def test_risk_score_campaign(employee_in_campaign, application_organization):
    org, repo_org = application_organization
    camp, repo_camp = employee_in_campaign

    camp.start()

    service = ExecuteCampaignService(repo_campaign=repo_camp, repo_org=repo_org)

    result = service.execute(campaign_id=camp.id, organization_id=org.id, now=datetime(2027, 1, 1, 10, 10, tzinfo=UTC))

    assert result.sent_count == 3

    click_at = datetime(2027, 1, 1, 11, 10, tzinfo=UTC)

    employees_with_sent_template = result.employees

    service_click = ClickCampaignEmployeeService(repo_campaign=repo_camp, repo_org=repo_org)

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

    service_2 = OpenCampaignEmployeeService(repo_campaign=repo_camp, repo_org=repo_org)

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

    camp.start()

    service_sent = ExecuteCampaignService(repo_campaign=repo_camp, repo_org=repo_org)

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

    service_open = OpenCampaignEmployeeService(repo_campaign=repo_camp, repo_org=repo_org)

    request_open = OpenTemplateCampaignRequest(campaign_id=camp.id,
                                               organization_id=org.id,
                                               employee_id=emp.employee_id,
                                               open_at=datetime(2026, 10, 10, 10, 10, tzinfo=UTC))

    service_open.execute(request_open)

    result_score = service_get_result.execute(request)

    # the template was opened
    assert result_score.risk_score == 0.4

    service_click = ClickCampaignEmployeeService(repo_campaign=repo_camp, repo_org=repo_org)

    request_click = ClickCampaignEmployeeRequest(campaign_id=camp.id,
                                                 organization_id=org.id,
                                                 employee_id=emp.employee_id,
                                                 click_at=datetime(2026, 10, 10, 10, 10, tzinfo=UTC))

    service_click.execute(request=request_click)

    service_click.execute(request=request_click)

    result_score = service_get_result.execute(request)

    # the template was opened and 2 clicks
    assert result_score.risk_score == 0.75

    #emp._submitted_credentials_at.append(datetime(2026, 10, 10, 10, 10, tzinfo=UTC))

    emp.mark_credentials_submitted(datetime(2026, 10, 10, 10, 10, tzinfo=UTC))

    service_click.execute(request=request_click)

    result_score = service_get_result.execute(request)

    # the template was opened and 2 clicks and mark credentials submitted
    assert result_score.risk_score == 1.0
