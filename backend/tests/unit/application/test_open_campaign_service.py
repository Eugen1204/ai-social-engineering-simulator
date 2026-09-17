from datetime import datetime, UTC
from uuid import uuid4

import pytest

from social_engineering_simulator.application.dto.create_campaign import OpenTemplateCampaignRequest
from social_engineering_simulator.application.services.create_campaign import OpenCampaignEmployeeService, \
    ExecuteCampaignService
from social_engineering_simulator.application.services.exceptions_create_campaign import TemplateAlreadyOpenedError, \
    TemplateWasNotSentError, CampaignNotFoundError, EmployeeNotInCampaignError, CampaignIsNotRunningError
from social_engineering_simulator.domain.organizations.campaign.exceptions import NotSentYetError, AlreadyOpenedError
from social_engineering_simulator.domain.organizations.exceptions import OrganizationNotFoundError
from social_engineering_simulator.infrastructure.persistence.in_memory.campaign_event_repository import \
    CampaignEventRepositoryInMemory


def test_running_campaign(employee_in_campaign, application_organization):
    org, repo_org = application_organization
    camp, repo_camp = employee_in_campaign
    repo_event = CampaignEventRepositoryInMemory()

    camp.start()

    service = ExecuteCampaignService(repo_campaign=repo_camp, repo_org=repo_org, repo_event=repo_event)

    result = service.execute(campaign_id=camp.id, organization_id=org.id, now=datetime(2027, 1, 1, 10, 10, tzinfo=UTC))

    open_at = datetime(2027, 1, 1, 11, 10, tzinfo=UTC)

    employees_with_sent_template = result.employees

    service = OpenCampaignEmployeeService(repo_campaign=repo_camp, repo_org=repo_org, repo_event=repo_event)

    request = OpenTemplateCampaignRequest(campaign_id=camp.id, organization_id=org.id,
                                          employee_id=employees_with_sent_template[0].employee_id,
                                          open_at=open_at)

    result_open = service.execute(request=request)

    assert result_open.opened_at == open_at

    assert result_open.campaign_id == camp.id

    with pytest.raises(AlreadyOpenedError):
        service.execute(request=request)


def test_sent_at_is_none(employee_in_campaign, application_organization):
    org, repo_org = application_organization
    camp, repo_camp = employee_in_campaign
    repo_event = CampaignEventRepositoryInMemory()

    camp.start()

    service = OpenCampaignEmployeeService(repo_campaign=repo_camp, repo_org=repo_org, repo_event=repo_event)

    open_at = datetime(2027, 1, 1, 11, 10, tzinfo=UTC)

    request = OpenTemplateCampaignRequest(campaign_id=camp.id, organization_id=org.id,
                                          employee_id=list(camp.employees.values())[0].employee_id,
                                          open_at=open_at)

    with pytest.raises(NotSentYetError):
        service.execute(request=request)


def test_wrong_campaign(employee_in_campaign, application_organization):
    org, repo_org = application_organization
    camp, repo_camp = employee_in_campaign
    repo_event = CampaignEventRepositoryInMemory()

    camp.start()

    service = ExecuteCampaignService(repo_campaign=repo_camp, repo_org=repo_org, repo_event=repo_event)

    result = service.execute(campaign_id=camp.id, organization_id=org.id, now=datetime(2027, 1, 1, 10, 10, tzinfo=UTC))

    open_at = datetime(2027, 1, 1, 11, 10, tzinfo=UTC)

    employees_with_sent_template = result.employees

    service = OpenCampaignEmployeeService(repo_campaign=repo_camp, repo_org=repo_org, repo_event=repo_event)

    request = OpenTemplateCampaignRequest(campaign_id=uuid4(), organization_id=org.id,
                                          employee_id=employees_with_sent_template[0].employee_id,
                                          open_at=open_at)

    with pytest.raises(CampaignNotFoundError):
        service.execute(request=request)

    request = OpenTemplateCampaignRequest(campaign_id=camp.id, organization_id=org.id,
                                          employee_id=uuid4(),
                                          open_at=open_at)

    with pytest.raises(EmployeeNotInCampaignError):
        service.execute(request=request)

    camp.finish()

    with pytest.raises(CampaignIsNotRunningError):
        service.execute(request=request)

    request = OpenTemplateCampaignRequest(campaign_id=camp.id, organization_id=uuid4(),
                                          employee_id=uuid4(),
                                          open_at=open_at)

    with pytest.raises(OrganizationNotFoundError):
        service.execute(request=request)


