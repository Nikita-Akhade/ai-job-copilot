from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.job import Job
from app.db.session import get_db
from app.schemas.job import JobCreate, JobResponse


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)


@router.get("/", response_model=list[JobResponse])
def list_jobs(db: Session = Depends(get_db)):
    statement = select(Job).order_by(Job.created_at.desc())

    return db.scalars(statement).all()


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
