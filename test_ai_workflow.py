from app.services.ai_workflow import build_ai_workflow


workflow = build_ai_workflow()

result = workflow.invoke(
    {
        "user_text": "I urgently need a laptop for a new engineer joining the team.",
        "analysis": None,
        "error": None,
    }
)

print("Analysis:", result["analysis"])
print("Error:", result["error"])
