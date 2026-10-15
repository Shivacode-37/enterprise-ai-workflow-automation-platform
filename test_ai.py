from app.services.ai_request_service import analyze_request

result = analyze_request(
    "I urgently need a laptop for a new engineer joining the team."
)

print(result.model_dump())
