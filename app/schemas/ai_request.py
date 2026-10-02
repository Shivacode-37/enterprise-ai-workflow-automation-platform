from pydantic import BaseModel, Field

from app.schemas.asset_request import PriorityEnum


class AIRequestAnalysis(BaseModel):
    request_type: str = Field(
        ...,
        min_length=2,
        max_length=50,
    )

    priority: PriorityEnum = PriorityEnum.NORMAL

    description: str = Field(
        ...,
        min_length=5,
        max_length=1000,
    )

# User text
#    ↓
# LLM
#    ↓
# AIRequestAnalysis
#    ↓
# Pydantic validation
#    ↓
# Business logic
#    ↓
# Database
