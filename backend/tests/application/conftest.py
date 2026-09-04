from datetime import datetime, timezone, timedelta
from uuid import uuid4

import pytest

from social_engineering_simulator.domain.email_template.entity import Template
from social_engineering_simulator.domain.email_template.value_object import SubjectText, ContentText
from social_engineering_simulator.domain.organizations.campaign.entity import Campaign
from social_engineering_simulator.domain.organizations.campaign.value_object import CampaignName, CampaignStatus
from social_engineering_simulator.domain.organizations.entity import Organization
from social_engineering_simulator.domain.organizations.value_object import OrganizationName, IndustryType
from social_engineering_simulator.infrastructure.persistence.in_memory.campaign_repository import CampaignRepoInMemory
from social_engineering_simulator.infrastructure.persistence.in_memory.organization_repository import \
    OrganizationRepoInMemory
from social_engineering_simulator.infrastructure.persistence.in_memory.template_repository import \
    TemplateRepositoryInMemory


@pytest.fixture
def application_organization():
    repo_org = OrganizationRepoInMemory()
    org = Organization(name=OrganizationName("Test org"),
                       industry=IndustryType.IT_COMPANY)

    repo_org.save(org)

    return org, repo_org


@pytest.fixture
def application_template(application_organization):
    org, _ = application_organization
    repo_template = TemplateRepositoryInMemory()
    template = Template(organization_id=org.id,
                        name="Fishing",
                        subject=SubjectText("Fishing"),
                        content=ContentText("Content_test"))
    repo_template.save(template)
    return template, repo_template


@pytest.fixture
def application_campaign(application_organization, application_template):
    repo_campaign = CampaignRepoInMemory()
    org, _ = application_organization
    template, _ = application_template

    time = datetime(2027, 9, 3, 10, 0, tzinfo=timezone.utc)

    camp = Campaign(name=CampaignName("HR fishing"),
                    organization_id=org.id,
                    template_id=template.id,
                    landing_page_id=uuid4(),
                    status=CampaignStatus.Draft,
                    template_version=template.version,
                    _template_subject=template.subject.value,
                    _template_content=template.content.value)

    camp.schedule(time)

    repo_campaign.save(camp)

    return camp, repo_campaign



