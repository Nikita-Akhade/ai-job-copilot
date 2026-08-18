from app.schemas.job import Job
from app.services.job_source import JobSource


class ManualJobSource(JobSource):
    """Provides jobs supplied manually for testing."""

    async def fetch_jobs(self) -> list[Job]:
        return [
            Job(
                title="Python Backend Developer",
                company="Example GmbH",
                location="Berlin",
                url="https://example.com/jobs/python-backend",
                description="Python backend development with FastAPI and SQLAlchemy.",
                source="manual",
                salary="€55,000 - €70,000",
            )
        ]