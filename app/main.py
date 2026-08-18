from fastapi import FastAPI

from app.api.routes.asset import router as assets_router
from app.core.config import settings

from app.api.routes.asset_request import router as asset_requests_router
from app.api.routes.approval import router as approvals_router
from app.api.routes.workflow_run import router as workflow_runs_router

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Enterprise AI Workflow Automation Platform",
)

app.include_router(assets_router)
app.include_router(asset_requests_router)
app.include_router(approvals_router)
app.include_router(workflow_runs_router)


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
