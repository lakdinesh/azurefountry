from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

from backend.app.config import settings
from backend.app.search_service import search_company_knowledge


project_client = AIProjectClient(
    endpoint=settings.AZURE_AI_PROJECT_ENDPOINT,
    credential=DefaultAzureCredential()
)

openai_client = project_client.get_openai_client()


def run_agent(user_message: str) -> str:
    knowledge = search_company_knowledge(user_message)

    context = "\n\n".join(
        [
            f"Source: {doc.get('source', 'unknown')}\nContent: {doc.get('content', '')}"
            for doc in knowledge
        ]
    )

    final_prompt = f"""
You are an Enterprise Support Agent.

Answer the user question using only the company knowledge below.
If the answer is not available in the company knowledge, say:
"I don't know based on the available company documents."

Company Knowledge:
{context}

User Question:
{user_message}
"""

    response = openai_client.responses.create(
        extra_body={
            "agent_reference": {
                "name": settings.AGENT_NAME,
                "type": "agent_reference"
            }
        },
        input=final_prompt
    )

    return response.output_text