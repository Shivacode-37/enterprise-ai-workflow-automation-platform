from fastapi import FastAPI
from app.core.config import settings
# from app.database.connection import

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Enterprise AI Workflow Automation Platform",
)

@app.get("/")
async def root():
    return {
        "message":"Enterprise AI Workflow Automation Platfrom",
        "status":"Running",
        "environment":settings.environment
    }

@app.get("/health")
async def health_check():
    return {
        "status":"healthy"
    }

# @app.get("/assets")
# def get_assets(db: Session = Depends(get_db)):
#     ...
