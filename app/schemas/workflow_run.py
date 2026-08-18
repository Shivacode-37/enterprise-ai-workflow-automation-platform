from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

class WorkflowRunUpdate(BaseModel):
    status: str = Field(..., min_length=2, max_length=50)
    current_step: str | None = Field(
        default=None,
        max_length=100,
    )
    
class WorkflowRunResponse(BaseModel):
    id: int
    request_id: int
    workflow_id: str
    status: str
    current_step: str | None
    started_at: datetime
    completed_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
