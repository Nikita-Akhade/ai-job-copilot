from app.db.models.job import Job as JobModel
from app.db.session import SessionLocal
from app.services.job_source import JobSource


class JobIngestionService:
    """Fetch jobs from a source and persist them in the database."""

    def __init__(self, source: JobSource):
        self.source = source

    async def ingest(self) -> int:
        jobs = await self.source.fetch_jobs()

        db = SessionLocal()

        try:
            created_count = 0

            for job in jobs:
                existing_job = (
                    db.query(JobModel)
                    .filter(JobModel.url == str(job.url))
                    .first()
                )

                if existing_job:
                    continue

                db_job = JobModel(
                    title=job.title,
                    company=job.company,
                    location=job.location,
                    url=str(job.url),
                    description=job.description,
                    source=job.source,
                    # salary is currently not part of the DB model
                )

                db.add(db_job)
                created_count += 1

            db.commit()

            return created_count

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()