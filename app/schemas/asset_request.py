from datetime import datetime
from enum import Enum


from amqp import PreconditionFailed
from pydantic import BaseModel, ConfigDict, Field

class PriorityEnum(str, Enum):
    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"
    URGENT = "URGENT"


class AssetRequestStatusEnum(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"

class AssetRequestBase(BaseModel):
    request_type: str = Field(..., min_length=2, max_length=50)
    priority: PriorityEnum = PriorityEnum.NORMAL
    description: str | None = None




class AssetRequestCreate(AssetRequestBase):
    user_id: int = Field(..., gt=0)


class AssetRequestUpdate(BaseModel):
    priority: PriorityEnum | None = None
    description: str | None = None


class AssetRequestResponse(AssetRequestBase):
    id: int
    user_id: int
    status: AssetRequestStatusEnum
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
