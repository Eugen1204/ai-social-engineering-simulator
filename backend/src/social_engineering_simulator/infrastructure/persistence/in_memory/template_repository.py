from dataclasses import field, dataclass
from uuid import UUID

from social_engineering_simulator.domain.email_template.entity import Template
from social_engineering_simulator.domain.email_template.repository import TemplateRepository


@dataclass
class TemplateRepositoryInMemory(TemplateRepository):
    _templates: dict[UUID, Template] = field(default_factory=dict)

    async def save(self, template: Template) -> None:
        self._templates[template.id] = template

    async def get_by_id(self, template_id: UUID) -> Template | None:
        return self._templates.get(template_id)

