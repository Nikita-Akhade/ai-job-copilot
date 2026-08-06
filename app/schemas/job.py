from pydantic import BaseModel, HttpUrl
from typing import Optional


class Job(BaseModel):
    title: str
    company: str
    location: str

    url: HttpUrl

    description: str

    source: str

    salary: Optional[str] = None