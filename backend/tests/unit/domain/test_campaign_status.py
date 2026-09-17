from datetime import datetime, UTC, timedelta
from uuid import uuid4

import pytest

from social_engineering_simulator.domain.organizations.campaign.entity import Campaign
from social_engineering_simulator.domain.organizations.campaign.exceptions import InvalidStateTransitionError, \
    CampaignInitError, CampaignScheduleError
from social_engineering_simulator.domain.organizations.campaign.value_object import CampaignName, CampaignStatus


@pytest.fixture()
def campaign_1(organization_with_employee) -> Campaign:
    camp = Campaign(name=CampaignName("fishing"), organization_id=uuid4(), template_id=uuid4(),
                    landing_page_id=uuid4(), status=CampaignStatus.Draft, template_version=1,
                    _template_subject="Test subject", _template_content="Test content")

    camp.assign_employee(organization_with_employee.employees[0])

    return camp


def test_edit_status_campaign(campaign_1):
    campaign_1.schedule(start_time=datetime.now(UTC) + timedelta(days=1))

    assert campaign_1.status == CampaignStatus.Scheduled

    with pytest.raises(CampaignScheduleError):
        campaign_1.schedule(start_time=datetime.now(UTC) - timedelta(days=1))

    campaign_1.return_to_draft()

    assert campaign_1.status == CampaignStatus.Draft

    campaign_1.start()

    assert campaign_1.status == CampaignStatus.Running

    with pytest.raises(InvalidStateTransitionError):
        campaign_1.schedule(start_time=datetime.now(UTC) + timedelta(days=1))

    campaign_1.finish()

    assert campaign_1.status == CampaignStatus.Finished

    campaign_1.archive()

    assert campaign_1.status == CampaignStatus.Archived


def test_edit_wrong_status(campaign_1):
    with pytest.raises(InvalidStateTransitionError):
        campaign_1.finish()

    with pytest.raises(InvalidStateTransitionError):
        campaign_1.archive()

    campaign_1.start()

    with pytest.raises(InvalidStateTransitionError):
        campaign_1.archive()

    with pytest.raises(InvalidStateTransitionError):
        campaign_1.return_to_draft()

    campaign_1.finish()

    with pytest.raises(InvalidStateTransitionError):
        campaign_1.return_to_draft()

    with pytest.raises(InvalidStateTransitionError):
        campaign_1.schedule(datetime.now(UTC) + timedelta(days=1))

    with pytest.raises(InvalidStateTransitionError):
        campaign_1.start()


def test_campaign_cannot_be_created_with_invalid_initial_status():
    with pytest.raises(CampaignInitError):
        Campaign(name=CampaignName("TEST"), organization_id=uuid4(), template_id=uuid4(),
                 landing_page_id=uuid4(), status=CampaignStatus.Archived, template_version=1,
                 _template_content="efefe", _template_subject="ervrf")
