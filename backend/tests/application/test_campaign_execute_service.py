from datetime import datetime

import pytest

from social_engineering_simulator.application.services.create_campaign import ExecuteCampaignService
from social_engineering_simulator.domain.organizations.campaign.exceptions import CampaignValidationError, \
    AlreadySentError


def test_running_campaign(employee_in_campaign, application_organization, make_draft_campaigns):
    org, repo_org = application_organization
    camp, repo_camp = employee_in_campaign

    camp.start()

    service = ExecuteCampaignService(repo_campaign=repo_camp, repo_org=repo_org)

    result = service.execute(campaign_id=camp.id, organization_id=org.id, now=datetime(2027, 1, 1, 10, 10))

    assert len(result) == 3

    assert result[0].sent_at == datetime(2027, 1, 1, 10, 10)

    with pytest.raises(AlreadySentError):
        service.execute(campaign_id=camp.id, organization_id=org.id, now=datetime(2027, 1, 1, 10, 10))

    empty_camp = make_draft_campaigns(with_employee=False)

    with pytest.raises(CampaignValidationError):
        empty_camp.start()





