from fastapi import APIRouter

from app.services.job_ingestion import JobIngestionService
from app.services.manual_job_source import ManualJobSource

router = APIRouter(
    prefix="/ingestion",
    tags=["Ingestion"],
)


@router.post("/manual")
async def ingest_manual_jobs():
    service = JobIngestionService(ManualJobSource())

    created_count = await service.ingest()

    return {
        "source": "manual",
        "created_jobs": created_count,
    }