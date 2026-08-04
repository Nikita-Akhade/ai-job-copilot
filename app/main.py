from fastapi import FastAPI

app = FastAPI(
    title="AI Job Copilot",
    description="AI-powered job application assistant for the German job market.",
    version="0.1.0",
)


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
