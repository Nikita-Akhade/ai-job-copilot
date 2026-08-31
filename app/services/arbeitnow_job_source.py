from html import unescape
from html.parser import HTMLParser

import httpx

from app.schemas.job import Job
from app.services.job_source import JobSource


class _HTMLTextParser(HTMLParser):
    """Convert simple HTML content into readable text."""

    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        text = data.strip()
        if text:
            self.parts.append(text)

    def get_text(self) -> str:
        return " ".join(self.parts)


def clean_description(description: str) -> str:
    """Convert HTML/HTML entities into plain text."""
    parser = _HTMLTextParser()
    parser.feed(unescape(description))
    return parser.get_text()


class ArbeitnowJobSource(JobSource):
    """Fetch and normalize jobs from the public Arbeitnow API."""

    API_URL = "https://www.arbeitnow.com/api/job-board-api"

    async def fetch_jobs(self) -> list[Job]:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(self.API_URL)
            response.raise_for_status()
            payload = response.json()

        jobs: list[Job] = []

        for item in payload.get("data", []):
            title = item.get("title")
            company = item.get("company_name")
            url = item.get("url")

            if not title or not company or not url:
                continue

            description = clean_description(
                item.get("description", "")
            )

            jobs.append(
                Job(
                    title=title,
                    company=company,
                    location=item.get("location") or "",
                    url=url,
                    description=description,
                    source="arbeitnow",
                    salary=None,
                )
            )

        return jobs
