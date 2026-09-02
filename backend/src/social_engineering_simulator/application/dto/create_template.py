from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class CreateTemplateRequest:
    organization_id: UUID
    name: str
    subject: str
    content: str


@dataclass
class CreateTemplateRequestResponse:
    id: UUID
    name: str
    subject: str
    content: str
    version: int
    created_at: datetime
    organization_id: UUID


@dataclass
class GetTemplateRequest:
    id_template: UUID
    id_organization: UUID


@dataclass
class PreviewTemplateRequest:
    organization_id: UUID
    template_id: UUID
    variables: dict


@dataclass
class TemplateVariablesResponse:
    subject: str
    content: str


