from datetime import datetime, timezone, timedelta
from uuid import uuid4, UUID

import pytest

from social_engineering_simulator.domain.email_template.entity import Template
from social_engineering_simulator.domain.email_template.value_object import SubjectText, ContentText
from social_engineering_simulator.domain.organizations.campaign.entity import Campaign
from social_engineering_simulator.domain.organizations.campaign.value_object import CampaignName, CampaignStatus
from social_engineering_simulator.domain.organizations.department.employee.value_object import EmployeeName, Email
from social_engineering_simulator.domain.organizations.department.entity import Department
from social_engineering_simulator.domain.organizations.department.value_object import DepartmentName
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
    org.add_department(department=Department(name=DepartmentName("HR")))
    org.add_employee(name=EmployeeName("Eugen Smt"), email=Email("test@blabla.com"), dep_name=DepartmentName("HR"))
    org.add_employee(name=EmployeeName("Kevin Smt"), email=Email("test2@blabla.com"), dep_name=DepartmentName("HR"))
    org.add_employee(name=EmployeeName("John Smt"), email=Email("test3@blabla.com"), dep_name=DepartmentName("HR"))

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


@pytest.fixture
def make_draft_campaigns(application_organization, application_template, **kwargs):
    org, _ = application_organization
    template, _ = application_template

    def _make_draft_campaigns(
            name: CampaignName = CampaignName("Test Campaign"),
            organization_id: UUID | None = None,
            template_id: UUID | None = None,
            landing_page_id: UUID | None = None,
            status: CampaignStatus = CampaignStatus.Draft,
            template_version: int | None = None,
            _template_subject: str | None = None,
            _template_content: str | None = None,
            with_employee: bool = True,
            **kwargs
    ) -> Campaign:
        campaign = Campaign(
            name=name,
            organization_id=organization_id or org.id,
            template_id=template_id or template.id,
            landing_page_id=landing_page_id or uuid4(),
            status=status,
            template_version=template_version or template.version,
            _template_subject=_template_subject or template.subject.value,
            _template_content=_template_content or template.content.value,
            **kwargs
        )
        if with_employee:
            campaign.assign_employee(emp_id=org.employees[0])

        return campaign
    return _make_draft_campaigns


@pytest.fixture
def employee_in_campaign(application_campaign, application_organization):
    camp, repo_camp = application_campaign
    org, repo_org = application_organization

    for emp_id in org.employees:
        camp.assign_employee(emp_id)

    repo_camp.save(camp)

    return camp, repo_camp

