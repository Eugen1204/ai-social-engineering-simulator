from typing import Protocol
from uuid import UUID

from social_engineering_simulator.domain.email_template.entity import Template


class TemplateRepository(Protocol):
    def save(self, template: Template) -> None:
        ...

    def get_by_id(self, template_id: UUID) -> Template | None:
        ...
