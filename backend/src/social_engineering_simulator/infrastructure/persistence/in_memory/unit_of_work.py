from uuid import UUID

from social_engineering_simulator.domain.email_template.entity import Template
from social_engineering_simulator.domain.organizations.campaign.campaign_employee_event import CampaignEmployeeEvent
from social_engineering_simulator.domain.organizations.campaign.entity import Campaign
from social_engineering_simulator.domain.organizations.entity import Organization
from social_engineering_simulator.domain.organizations.unit_of_work import UnitOfWork
from social_engineering_simulator.infrastructure.persistence.in_memory.campaign_event_repository import \
    CampaignEventRepositoryInMemory
from social_engineering_simulator.infrastructure.persistence.in_memory.campaign_repository import CampaignRepoInMemory
from social_engineering_simulator.infrastructure.persistence.in_memory.organization_repository import \
    OrganizationRepoInMemory
from copy import deepcopy

from social_engineering_simulator.infrastructure.persistence.in_memory.template_repository import \
    TemplateRepositoryInMemory


class UnitOfWorkInMemory(UnitOfWork):
    def __init__(self):
        self.organizations: OrganizationRepoInMemory = OrganizationRepoInMemory()
        self.campaigns: CampaignRepoInMemory = CampaignRepoInMemory()
        self.campaigns_events: CampaignEventRepositoryInMemory = CampaignEventRepositoryInMemory()
        self.templates: TemplateRepositoryInMemory = TemplateRepositoryInMemory()

        self._snapshot_org: dict[UUID, Organization] | None = None
        self._snapshot_camp: dict[UUID, Campaign] | None = None
        self._snapshot_camp_events: dict[UUID, CampaignEmployeeEvent] | None = None
        self._snapshot_templates: dict[UUID, Template] | None = None

    async def __aenter__(self) -> "UnitOfWorkInMemory":
        self._snapshot_org = deepcopy(self.organizations._organizations)
        self._snapshot_camp = deepcopy(self.campaigns._campaigns)
        self._snapshot_camp_events = deepcopy(self.campaigns_events._events)
        self._snapshot_templates = deepcopy(self.templates._templates)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()

    async def commit(self) -> None:
        self._snapshot_org = None
        self._snapshot_camp = None

    async def rollback(self) -> None:
        if self._snapshot_org is not None:
            self.organizations._organizations.clear()
            self.organizations._organizations.update(self._snapshot_org)
        if self._snapshot_camp is not None:
            self.campaigns._campaigns.clear()
            self.campaigns._campaigns.update(self._snapshot_camp)
        if self._snapshot_templates is not None:
            self.templates._templates.clear()
            self.templates._templates.update(self._snapshot_templates)
        if self._snapshot_camp_events is not None:
            self.campaigns_events._events.clear()
            self.campaigns_events._events.update(self._snapshot_camp_events)
