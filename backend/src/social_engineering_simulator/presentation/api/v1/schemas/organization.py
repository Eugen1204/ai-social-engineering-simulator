from datetime import datetime
from typing import List
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class CreateOrganizationHttpRequest(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
    )
    name: str = Field(..., min_length=2, max_length=50, examples=["TechCorp"])
    industry: str = Field(..., min_length=2, max_length=50, examples=["IT Company"])
    departments: List[str] = Field(..., min_length=1, description="List departments names",
                                   examples=[["HR", "IT", "Finance"]])


class OrganizationHttpResponse(BaseModel):
    id: UUID
    name: str
    industry: str
    departments: int


class AddEmployeeRequest(BaseModel):
    name: str
    email: str
    dep_name: str


class AddEmployeeRequestResponse(BaseModel):
    id: UUID
    name: str
    email: str
    org_id: UUID


class GetEmployeeRequestResponse(BaseModel):
    id: UUID
    name: str
    email: str
    org_id: UUID


class TemplateVariables(BaseModel):
    variables: dict


class TemplateVariablesResponse(BaseModel):
    subject: str
    content: str


class AddTemplateResponse(BaseModel):
    id: UUID
    organization_id: UUID
    name: str
    subject: str
    content: str
    version: int
    created_at: datetime


class AddTemplateRequest(BaseModel):
    name: str
    subject: str
    content: str
