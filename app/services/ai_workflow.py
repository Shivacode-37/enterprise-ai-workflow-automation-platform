from typing import Literal

from langgraph.graph import END, START, StateGraph

from app.schemas.ai_workflow import AIWorkflowState
from app.services.ai_request_service import analyze_request


SUPPORTED_ASSET_TYPES = {
    "LAPTOP",
    "MONITOR",
    "KEYBOARD",
    "MOUSE",
    "HEADSET",
}


def analyze_request_node(
    state: AIWorkflowState,
) -> dict:
    try:
        analysis = analyze_request(state["user_text"])

        return {
            "analysis": analysis,
            "error": None,
        }

    except Exception:
        return {
            "analysis": None,
            "error": "Unable to analyze the request. Please try again.",
        }


def validate_analysis_node(
    state: AIWorkflowState,
) -> dict:
    analysis = state["analysis"]

    if analysis is None:
        return {
            "error": "AI analysis did not produce a result.",
        }

    request_type = analysis.request_type.strip().upper()

    if request_type not in SUPPORTED_ASSET_TYPES:
        return {
            "error": f"Unsupported asset type: {request_type}",
        }

    return {
        "analysis": analysis.model_copy(
            update={"request_type": request_type}
        ),
        "error": None,
    }


def route_after_validation(
    state: AIWorkflowState,
) -> Literal["success", "end"]:
    if state.get("error"):
        return "end"

    return "success"

def route_after_analysis(
    state: AIWorkflowState,
) -> Literal["validate", "end"]:
    if state.get("error"):
        return "end"

    return "validate"


def build_ai_workflow():
    graph = StateGraph(AIWorkflowState)

    graph.add_node(
        "analyze",
        analyze_request_node,
    )

    graph.add_node(
        "validate",
        validate_analysis_node,
    )

    graph.add_edge(START, "analyze")

    graph.add_conditional_edges(
        "analyze",
        route_after_analysis,
        {
            "validate": "validate",
            "end": END,
        },
    )

    graph.add_conditional_edges(
    "validate",
    route_after_validation,
    {
        "success": END,
        "end": END,
    },
)

    return graph.compile()
