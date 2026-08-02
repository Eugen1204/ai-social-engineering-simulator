from dataclasses import dataclass
from uuid import UUID

from social_engineering_simulator.domain.email_template.value_object import TemplateContext


@dataclass
class Template:
    id: UUID
    name: str
    content: str
    version: int

    def update_content(self, new_content: str):
        self.content = new_content
        self.version += 1

