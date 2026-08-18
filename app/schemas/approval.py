from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class ApprovalStatusEnum(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class ApprovalCreate(BaseModel):
    request_id: int = Field(..., gt=0)
    approver_id: int = Field(..., gt=0)


class ApprovalDecision(BaseModel):
    status: ApprovalStatusEnum
    comments: str | None = Field(
        default=None,
        max_length=1000,
    )


class ApprovalResponse(BaseModel):
    id: int
    request_id: int
    approver_id: int
    status: ApprovalStatusEnum
    comments: str | None
    created_at: datetime
    decided_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
