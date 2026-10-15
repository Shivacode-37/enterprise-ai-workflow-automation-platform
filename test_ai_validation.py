from app.schemas.ai_request import AIRequestAnalysis
from app.schemas.ai_workflow import AIWorkflowState
from app.services.ai_workflow import validate_analysis_node


unsupported_analysis = AIRequestAnalysis(
    request_type="PRINTER",
    priority="NORMAL",
    description="A printer is required.",
)

state: AIWorkflowState = {
    "user_text": "I need a printer.",
    "analysis": unsupported_analysis,
    "error": None,
}

result = validate_analysis_node(state)

print(result)
