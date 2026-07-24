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
    departments: List[str]
