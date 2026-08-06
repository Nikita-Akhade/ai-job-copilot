from fastapi import APIRouter

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.get("/")
async def list_jobs():
    return {
        "message": "No jobs available yet",
        "jobs": [],
    }