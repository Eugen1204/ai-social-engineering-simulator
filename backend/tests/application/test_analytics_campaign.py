from datetime import datetime, UTC
from uuid import uuid4

import pytest

from social_engineering_simulator.application.services.create_campaign import ExecuteCampaignService, \
    GetCampaignAnalyticService
from social_engineering_simulator.application.services.exceptions_create_campaign import CampaignIsDraftStatusError, \
    CampaignNotFoundError
from social_engineering_simulator.domain.organizations.exceptions import OrganizationNotFoundError


def test_risk_score_campaign(employee_in_campaign, application_organization):
    org, repo_org = application_organization
    camp, repo_camp = employee_in_campaign

    camp.start()

    service_sent = ExecuteCampaignService(repo_campaign=repo_camp, repo_org=repo_org)

    result_sent = service_sent.execute(campaign_id=camp.id, organization_id=org.id,
                                       now=datetime(2027, 1, 1, 10, 10, tzinfo=UTC))

    assert result_sent.sent_count == 3

    emp_1 = camp.get_employee(result_sent.employees[0].employee_id)
    emp_2 = camp.get_employee(result_sent.employees[1].employee_id)
    emp_3 = camp.get_employee(result_sent.employees[2].employee_id)

    service_analytic = GetCampaignAnalyticService(repo_campaign=repo_camp, repo_org=repo_org)

    result_analytic = service_analytic.execute(campaign_id=camp.id, organization_id=org.id)

    assert result_analytic.average_risk_score == pytest.approx(0.1)

    emp_1.mark_opened()

    emp_1.mark_clicked()

    emp_1.mark_credentials_submitted()

    assert emp_1.risk_score == 1.0

    result_analytic = service_analytic.execute(campaign_id=camp.id, organization_id=org.id)

    assert result_analytic.sent_count == 3
    assert result_analytic.credential_submission_employee_count == 1
    assert result_analytic.clicked_employee_count == 1
    assert result_analytic.opened_count == 1
    assert result_analytic.average_risk_score == pytest.approx(0.4)

    emp_2.mark_opened()

    emp_2.mark_clicked()

    result_analytic = service_analytic.execute(campaign_id=camp.id, organization_id=org.id)

    assert result_analytic.opened_count == 2
    assert result_analytic.clicked_employee_count == 2
    # opened 2 clicked 2 sent 3 credential 1 = 1emp = (1 + 0.7 + 0.1) / 3
    assert result_analytic.average_risk_score == 0.6

    emp_2.mark_clicked()
    emp_2.mark_clicked()
    emp_2.mark_clicked()

    result_analytic = service_analytic.execute(campaign_id=camp.id, organization_id=org.id)
    assert result_analytic.clicked_employee_count == 2


def test_analytic_raises(employee_in_campaign, application_organization):
    org, repo_org = application_organization
    camp, repo_camp = employee_in_campaign

    service_analytic = GetCampaignAnalyticService(repo_campaign=repo_camp, repo_org=repo_org)

    with pytest.raises(CampaignIsDraftStatusError):
        service_analytic.execute(camp.id, org.id)

    camp.start()

    with pytest.raises(CampaignNotFoundError):
        service_analytic.execute(uuid4(), org.id)

    with pytest.raises(OrganizationNotFoundError):
        service_analytic.execute(camp.id, uuid4())




