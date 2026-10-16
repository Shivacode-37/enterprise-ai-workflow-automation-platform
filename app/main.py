from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI

from app.database.base import Base
from app.database.connection import engine
import app.models

from app.api.routes.asset import router as assets_router
from app.core.config import settings

from app.api.routes.asset_request import router as asset_requests_router
from app.api.routes.approval import router as approvals_router
from app.api.routes.workflow_run import router as workflow_runs_router
from app.api.routes.ai_request import router as ai_request_router
from app.api.routes.audit_log import router as audit_logs_router
from app.api.routes.auth import router as auth_router

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Enterprise AI Workflow Automation Platform",
    lifespan=lifespan,
)

@app.on_event("startup")
def create_database_tables():
    Base.metadata.create_all(bind=engine)
app.include_router(assets_router)
app.include_router(asset_requests_router)
app.include_router(approvals_router)
app.include_router(workflow_runs_router)
app.include_router(ai_request_router)
app.include_router(audit_logs_router)
app.include_router(auth_router)

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
