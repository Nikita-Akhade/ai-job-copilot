from abc import ABC, abstractmethod

from app.schemas.job import Job


class JobSource(ABC):
    """Base interface for all job sources."""

    @abstractmethod
    async def fetch_jobs(self) -> list[Job]:
        """Fetch and normalize jobs from the source."""
        raise NotImplementedError