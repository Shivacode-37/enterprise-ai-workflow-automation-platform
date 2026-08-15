from fastapi import FastAPI

from app.api.routes.asset import router as assets_router
from app.core.config import settings


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Enterprise AI Workflow Automation Platform",
)


app.include_router(assets_router)


@app.get("/")
async def root():
    return {
        "message": "Enterprise AI Workflow Automation Platform",
        "status": "Running",
        "environment": settings.environment,
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
    }


# @app.get("/assets")
# def get_assets(db: Session = Depends(get_db)):
#     ...
