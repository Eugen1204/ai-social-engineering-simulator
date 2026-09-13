from datetime import datetime, UTC
from uuid import uuid4

import pytest

from social_engineering_simulator.application.dto.create_campaign import ClickCampaignEmployeeRequest, \
    OpenTemplateCampaignRequest
from social_engineering_simulator.application.services.create_campaign import ExecuteCampaignService, \
    GetCampaignEmployeeRiskProfile, ClickCampaignEmployeeService, OpenCampaignEmployeeService, \
    CredentialSubmissionEmployeeService
from social_engineering_simulator.application.services.exceptions_create_campaign import CampaignNotFoundError, \
    EmployeeNotInCampaignError, CampaignResultsNotAvailableError
from social_engineering_simulator.domain.organizations.campaign.exceptions import EmployeeNotFoundInCampaign
from social_engineering_simulator.domain.organizations.department.employee.value_object import EmployeeName, Email
from social_engineering_simulator.domain.organizations.department.value_object import DepartmentName
from social_engineering_simulator.domain.organizations.exceptions import OrganizationNotFoundError
from social_engineering_simulator.infrastructure.persistence.in_memory.campaign_event_repository import \
    CampaignEventRepositoryInMemory


def test_get_campaign_employee_profile_ap(employee_in_campaign, application_organization):
    org, repo_org = application_organization
    camp, repo_camp = employee_in_campaign
    repo_event = CampaignEventRepositoryInMemory()

    get_risk_profile_service = GetCampaignEmployeeRiskProfile(repo_campaign=repo_camp,
                                                              repo_org=repo_org,
                                                              repo_events=repo_event)

    with pytest.raises(CampaignResultsNotAvailableError):
        get_risk_profile_service.execute(organization_id=org.id,
                                         campaign_id=camp.id,
                                         employee_id=list(camp.employees.values())[0])

    camp.start()

    result = get_risk_profile_service.execute(organization_id=org.id,
                                              campaign_id=camp.id,
                                              employee_id=list(camp.employees.values())[0].employee_id)

    assert result.event_count == 0
    assert result.is_sent is False
    assert result.last_event_at is None

    service_sent = ExecuteCampaignService(repo_campaign=repo_camp, repo_org=repo_org, repo_event=repo_event)

    result_sent = service_sent.execute(campaign_id=camp.id, organization_id=org.id,
                                       now=datetime(2027, 1, 1, 10, 10, tzinfo=UTC))

    emp_1 = camp.get_employee(result_sent.employees[0].employee_id)

    result = get_risk_profile_service.execute(organization_id=org.id,
                                              campaign_id=camp.id,
                                              employee_id=emp_1.employee_id)

    assert result.risk_score == 0.1
    assert result.is_sent is True
    assert result.is_opened is False
    assert result.is_clicked is False
    assert result.credentials_submitted is False
    assert result.event_count == 1
    assert result.last_event_at == datetime(2027, 1, 1, 10, 10, tzinfo=UTC)

    service_click = ClickCampaignEmployeeService(repo_campaign=repo_camp, repo_org=repo_org, repo_event=repo_event)

    request = ClickCampaignEmployeeRequest(campaign_id=camp.id,
                                           organization_id=org.id,
                                           employee_id=emp_1.employee_id,
                                           click_at=datetime(2027, 1, 1, 10, 10, tzinfo=UTC))

    service_click.execute(request)
    service_click.execute(request)
    service_click.execute(request)

    service_opened = OpenCampaignEmployeeService(repo_campaign=repo_camp, repo_org=repo_org, repo_event=repo_event)

    request = OpenTemplateCampaignRequest(campaign_id=camp.id, organization_id=org.id,
                                          employee_id=emp_1.employee_id,
                                          open_at=datetime(2027, 1, 1, 10, 15, tzinfo=UTC))

    service_opened.execute(request=request)

    result = get_risk_profile_service.execute(organization_id=org.id,
                                              campaign_id=camp.id,
                                              employee_id=emp_1.employee_id)
    assert result.is_opened is True
    assert result.click_count == 3
    assert result.event_count == 5
    assert result.last_event_at == datetime(2027, 1, 1, 10, 15, tzinfo=UTC)

    service = CredentialSubmissionEmployeeService(repo_campaign=repo_camp,
                                                  repo_org=repo_org,
                                                  repo_event=repo_event)
    service.execute(organization_id=org.id,
                    campaign_id=camp.id,
                    employee_id=emp_1.employee_id,
                    credential_submission_at=datetime(2027, 1, 1, 10, 15, tzinfo=UTC))

    service.execute(organization_id=org.id,
                    campaign_id=camp.id,
                    employee_id=emp_1.employee_id,
                    credential_submission_at=datetime(2027, 1, 1, 10, 15, tzinfo=UTC))

    result = get_risk_profile_service.execute(organization_id=org.id,
                                              campaign_id=camp.id,
                                              employee_id=emp_1.employee_id)

    assert result.credentials_submitted is True
    assert result.credential_submission_count == 2

    with pytest.raises(OrganizationNotFoundError):
        get_risk_profile_service.execute(organization_id=uuid4(),
                                         campaign_id=camp.id,
                                         employee_id=emp_1.employee_id)

    with pytest.raises(CampaignNotFoundError):
        get_risk_profile_service.execute(organization_id=org.id,
                                         campaign_id=uuid4(),
                                         employee_id=emp_1.employee_id)

    with pytest.raises(EmployeeNotFoundInCampaign):
        get_risk_profile_service.execute(organization_id=org.id,
                                         campaign_id=camp.id,
                                         employee_id=uuid4())
