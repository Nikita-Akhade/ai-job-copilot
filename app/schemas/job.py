from pydantic import BaseModel, HttpUrl,ConfigDict
from typing import Optional
from datetime import datetime

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