from datetime import datetime, timezone, timedelta
from uuid import uuid4

import pytest

from social_engineering_simulator.application.services.start_scheduled_campaign import StartScheduledCampaign
from social_engineering_simulator.domain.organizations.campaign.entity import Campaign
from social_engineering_simulator.domain.organizations.campaign.value_object import CampaignStatus, CampaignName
from social_engineering_simulator.infrastructure.persistence.in_memory.campaign_repository import CampaignRepoInMemory


def test_campaign_starts_when_time_came(employee_in_campaign):
    campaign, repo_camp = employee_in_campaign

    service = StartScheduledCampaign(repo_camp)

    datetime_now = datetime(2027, 9, 3, 11, 0, tzinfo=timezone.utc)

    started = service.execute(now=datetime_now)

    assert len(started) == 1
    assert started[0].id == campaign.id

    started_2 = service.execute(datetime.now(timezone.utc))

    assert len(started_2) == 0


def test_campaign_start_with_the_same_time(application_template, application_organization):
    repo_camp = CampaignRepoInMemory()
    template, _ = application_template
    org, _ = application_organization
    camp = Campaign(name=CampaignName("HR fishing2"),
                    organization_id=org.id,
                    template_id=template.id,
                    landing_page_id=uuid4(),
                    status=CampaignStatus.Draft,
                    template_version=template.version,
                    _template_subject=template.subject.value,
                    _template_content=template.content.value)

    camp.assign_employee(org.employees[0])

    scheduled_time = datetime(2027, 9, 3, 10, 0, tzinfo=timezone.utc)
    camp.schedule(scheduled_time)
    repo_camp.save(camp)
    started = datetime(2027, 9, 3, 10, 0, tzinfo=timezone.utc)

    service = StartScheduledCampaign(repo_camp)

    started = service.execute(started)

    assert len(started) == 1


def test_campaign_not_started_before_scheduled_time(application_template, application_organization):
    repo_camp = CampaignRepoInMemory()
    template, _ = application_template
    org, _ = application_organization
    camp = Campaign(name=CampaignName("HR fishing2"),
                    organization_id=org.id,
                    template_id=template.id,
                    landing_page_id=uuid4(),
                    status=CampaignStatus.Draft,
                    template_version=template.version,
                    _template_subject=template.subject.value,
                    _template_content=template.content.value)

    camp.assign_employee(org.employees[0])

    scheduled_time = datetime(2027, 9, 3, 10, 0, tzinfo=timezone.utc)
    camp.schedule(scheduled_time)
    repo_camp.save(camp)
    started = datetime(2027, 9, 3, 9, 59, tzinfo=timezone.utc)

    service = StartScheduledCampaign(repo_camp)

    started = service.execute(started)

    assert len(started) == 0


def test_other_status_not_selected(application_template, application_organization):
    repo_camp = CampaignRepoInMemory()
    template, _ = application_template
    org, _ = application_organization
    camp = Campaign(name=CampaignName("HR fishing2"),
                    organization_id=org.id,
                    template_id=template.id,
                    landing_page_id=uuid4(),
                    status=CampaignStatus.Draft,
                    template_version=template.version,
                    _template_subject=template.subject.value,
                    _template_content=template.content.value)

    camp.assign_employee(org.employees[0])

    service = StartScheduledCampaign(repo_camp)

    started = service.execute(datetime.now(timezone.utc) + timedelta(hours=2))

    assert len(started) == 0

    camp.start()

    started = service.execute(datetime.now(timezone.utc) + timedelta(hours=2))

    assert len(started) == 0

    camp.cancel()
    started = service.execute(datetime.now(timezone.utc) + timedelta(hours=2))

    assert len(started) == 0


def test_with_3_campaigns_where_2_ready_to_started(application_template, application_organization,
                                                   make_draft_campaigns):

    repo_camp = CampaignRepoInMemory()
    template, _ = application_template
    org, _ = application_organization
    camp_1 = make_draft_campaigns(name=CampaignName("HR Fishing 1"))
    camp_2 = make_draft_campaigns(name=CampaignName("HR Fishing 2"))
    camp_3 = make_draft_campaigns(name=CampaignName("HR Fishing 3"))

    datetime_now = datetime(2027, 1, 1, 10, 0, 0, tzinfo=timezone.utc)

    camp_1.schedule(start_time=datetime(2027, 1, 1, 9, 0, 0, tzinfo=timezone.utc))

    camp_2.schedule(start_time=datetime(2027, 1, 1, 9, 59, 0, tzinfo=timezone.utc))

    camp_3.schedule(start_time=datetime(2027, 1, 1, 11, 0, 0, tzinfo=timezone.utc))

    repo_camp.save(camp_1)

    repo_camp.save(camp_2)

    repo_camp.save(camp_3)

    service = StartScheduledCampaign(repo_camp)

    result = service.execute(now=datetime_now)

    assert len(result) == 2

    assert result[0]._started_at == datetime_now

    assert result[1]._started_at == datetime_now

    assert camp_3.status == CampaignStatus.Scheduled
