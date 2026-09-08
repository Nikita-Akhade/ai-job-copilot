from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, HttpUrl


class Job(BaseModel):
    title: str
    company: str
    location: str
    url: HttpUrl
    description: str
    source: str
    salary: Optional[str] = None


class JobCreate(BaseModel):
    title: str
    company: str
    location: str
    url: HttpUrl
    description: str
    source: str
    salary: Optional[str] = None


class JobResponse(JobCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class JobListResponse(BaseModel):
    items: list[JobResponse]
    page: int
    limit: int
    total: int
    pages: int
