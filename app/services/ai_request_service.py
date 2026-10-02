from langchain_openai import ChatOpenAI

from app.core.config import settings
from app.schemas.ai_request import AIRequestAnalysis
from app.services.policy_retriever import create_policy_retriever


def analyze_request(user_text: str) -> AIRequestAnalysis:
    retriever = create_policy_retriever()

    relevant_documents = retriever.invoke(user_text)

    policy_context = "\n\n".join(
        document.page_content
        for document in relevant_documents
    )

    llm = ChatOpenAI(
        model="gpt-5.6-luna",
        api_key=settings.openai_api_key,
        temperature=0,
    )

    structured_llm = llm.with_structured_output(
        AIRequestAnalysis
    )

    result = structured_llm.invoke(
        f"""
You are an enterprise IT asset request analyzer.

Analyze the user's request using the provided enterprise IT policies.

Enterprise IT policies:
{policy_context}

Extract:

- request_type: the requested IT asset type, such as LAPTOP, MONITOR,
  KEYBOARD, MOUSE, or HEADSET.
- priority: LOW, NORMAL, HIGH, or URGENT.
- description: a concise description of the user's original request.

Only use the policies as supporting context.
Do not invent company policies.

User request:
{user_text}
"""
    )

    return result


# User
#  ↓
# RAG
#  ↓
# Company policies
#  ↓
# LLM
#  ↓
# Structured result
