from fastapi import FastAPI
from app.api.router import api_router
from app.db.init_db import init_db
app = FastAPI(
    title="AI Job Copilot",
    description="AI-powered job application assistant for the German job market.",
    version="0.1.0",
)
init_db()
app.include_router(api_router)

@app.get("/")
async def root():
    return {
        "project": "AI Job Copilot",
        "version": "0.1.0",
        "status": "running",
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
    }
