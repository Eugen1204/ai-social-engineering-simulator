from dataclasses import dataclass, field
from datetime import datetime, UTC
from uuid import UUID, uuid4

from social_engineering_simulator.domain.email_template.value_object import SubjectText, ContentText


@dataclass
class Template:
    organization_id: UUID
    name: str
    subject: SubjectText
    content: ContentText
    version: int = field(default=1)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    id: UUID = field(default_factory=uuid4)

    def update_content(self, new_content: str) -> None:
        self.content = ContentText(new_content)
        self.version += 1

    def update_subject(self, new_subject: str) -> None:
        self.subject = SubjectText(new_subject)
        self.version += 1

    def update(self, new_content: str | None = None, new_subject: str | None = None) -> None:
        updated_content = ContentText(new_content) if new_content is not None else None
        updated_subject = SubjectText(new_subject) if new_subject is not None else None

        if updated_content is None and updated_subject is None:
            return

        if updated_content is not None:
            self.content = updated_content
        if updated_subject is not None:
            self.subject = updated_subject

        self.version += 1
