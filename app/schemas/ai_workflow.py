from typing import TypedDict

from app.schemas.ai_request import AIRequestAnalysis


class AIWorkflowState(TypedDict):
    user_text: str
    analysis: AIRequestAnalysis | None
    error: str | None
