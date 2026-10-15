
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AuditLogResponse(BaseModel):
    id: int
    request_id: int | None
    actor_type: str
    action: str
    details: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
