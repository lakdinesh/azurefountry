from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from backend.app.config import settings
from backend.app.search_service import search_company_knowledge
from backend.app.tools import get_ticket_status, escalate_ticket

project_client = AIProjectClient(
    endpoint=settings.AZURE_AI_PROJECT_ENDPOINT,
    credential=DefaultAzureCredential()
)

def create_support_agent():
    agent = project_client.agents.create_agent(
        model=settings.AZURE_OPENAI_DEPLOYMENT_NAME,
        name="enterprise-support-agent",
        instructions="""
        You are an enterprise IT support AI agent.

        Responsibilities:
        1. Answer employee support questions using company knowledge.
        2. Check ticket status when ticket ID is provided.
        3. Escalate critical issues when needed.
        4. Never invent policy answers.
        5. If knowledge is missing, say you do not know.
        """
    )

    return agent


def run_agent(user_message: str):
    # Simple practical flow
    knowledge = search_company_knowledge(user_message)

    context = "\n".join([doc["content"] for doc in knowledge])

    final_prompt = f"""
    User question:
    {user_message}

    Company knowledge:
    {context}

    Answer using only the company knowledge.
    """

    thread = project_client.agents.threads.create()

    project_client.agents.messages.create(
        thread_id=thread.id,
        role="user",
        content=final_prompt
    )

    agent = create_support_agent()

    run = project_client.agents.runs.create_and_process(
        thread_id=thread.id,
        agent_id=agent.id
    )

    messages = project_client.agents.messages.list(thread_id=thread.id)

    response_text = ""

    for msg in messages:
        if msg.role == "assistant":
            response_text = msg.content[0].text.value

    return response_text