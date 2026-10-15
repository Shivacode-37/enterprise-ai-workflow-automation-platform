from unittest.mock import patch

from app.services.ai_workflow import build_ai_workflow


workflow = build_ai_workflow()

with patch(
    "app.services.ai_workflow.analyze_request",
    side_effect=RuntimeError("Simulated AI provider failure"),
):
    result = workflow.invoke(
        {
            "user_text": "I need a laptop.",
            "analysis": None,
            "error": None,
        }
    )

print("Analysis:", result["analysis"])
print("Error:", result["error"])

assert result["analysis"] is None
assert result["error"] == (
    "Unable to analyze the request. Please try again."
)

print("Error-path test passed.")
