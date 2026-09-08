from fastapi import APIRouter, Depends, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.models.job import Job
from app.db.session import get_db
from app.schemas.job import JobCreate, JobListResponse, JobResponse


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)


@router.get("/", response_model=JobListResponse)
def list_jobs(
    location: str | None = None,
    company: str | None = None,
    source: str | None = None,
    page: int = 1,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    if page < 1:
        page = 1

    if limit < 1:
        limit = 20

    if limit > 100:
        limit = 100

    statement = select(Job)

    if location:
        statement = statement.where(Job.location.ilike(f"%{location}%"))

    if company:
        statement = statement.where(Job.company.ilike(f"%{company}%"))

    if source:
        statement = statement.where(Job.source.ilike(f"%{source}%"))

    total_statement = select(func.count()).select_from(statement.subquery())
    total = db.scalar(total_statement) or 0

    offset = (page - 1) * limit

    statement = (
        statement
        .order_by(Job.created_at.desc())
        .offset(offset)
        .limit(limit)
    )

    jobs = db.scalars(statement).all()

    pages = (total + limit - 1) // limit

    return JobListResponse(
        items=jobs,
        page=page,
        limit=limit,
        total=total,
        pages=pages,
    )


@router.post(
    "/",
    response_model=JobResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_job(job_data: JobCreate, db: Session = Depends(get_db)):
    job = Job(
        title=job_data.title,
        company=job_data.company,
        location=job_data.location,
        url=str(job_data.url),
        description=job_data.description,
        source=job_data.source,
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job
