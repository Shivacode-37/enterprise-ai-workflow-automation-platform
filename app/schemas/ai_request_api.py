from pydantic import BaseModel

from app.schemas.ai_request import AIRequestAnalysis
from app.schemas.asset_request import AssetRequestResponse


class AIRequestInput(BaseModel):
    user_text: str


class AIRequestResult(BaseModel):
    analysis: AIRequestAnalysis | None
    error: str | None


class AIAssetRequestResult(BaseModel):
    analysis: AIRequestAnalysis
    asset_request: AssetRequestResponse
