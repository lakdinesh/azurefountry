import time
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

from backend.app.config import settings
from backend.app.search_service import search_company_knowledge
from backend.app.guardrails import validate_user_input, validate_answer
from backend.app.monitoring import tracer, logger


token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "https://ai.azure.com/.default"
)

client = OpenAI(
    base_url=settings.AZURE_FOUNDRY_ENDPOINT,
    api_key=token_provider
)


def run_agent(user_message: str) -> dict:
    start_time = time.time()

    with tracer.start_as_current_span("enterprise_support_agent") as span:
        span.set_attribute("user.message.length", len(user_message))

        is_valid, error = validate_user_input(user_message)

        if not is_valid:
            span.set_attribute("guardrail.input_blocked", True)
            return {
                "answer": error,
                "sources": [],
                "latency_ms": 0,
                "tokens": {}
            }

        docs = search_company_knowledge(user_message)

        context = "\n\n".join(
            [
                f"Source: {doc['source']}\nContent: {doc['content']}"
                for doc in docs
            ]
        )

        prompt = f"""
You are an Enterprise Support Agent.

Rules:
1. Answer only from the company documents.
2. Do not hallucinate.
3. If answer is unavailable, say:
"I don't know based on the available company documents."
4. Mention the document source if available.

Company Documents:
{context}

User Question:
{user_message}
"""

        response = client.responses.create(
            model=settings.AZURE_MODEL_DEPLOYMENT,
            input=prompt,
            temperature=0.2
        )

        answer = response.output_text

        is_answer_valid, answer_error = validate_answer(answer)

        if not is_answer_valid:
            answer = answer_error

        latency_ms = round((time.time() - start_time) * 1000, 2)

        usage = getattr(response, "usage", None)

        token_data = {
            "input_tokens": getattr(usage, "input_tokens", 0) if usage else 0,
            "output_tokens": getattr(usage, "output_tokens", 0) if usage else 0,
            "total_tokens": getattr(usage, "total_tokens", 0) if usage else 0
        }

        span.set_attribute("llm.model", settings.AZURE_MODEL_DEPLOYMENT)
        span.set_attribute("llm.latency_ms", latency_ms)
        span.set_attribute("llm.input_tokens", token_data["input_tokens"])
        span.set_attribute("llm.output_tokens", token_data["output_tokens"])
        span.set_attribute("llm.total_tokens", token_data["total_tokens"])
        span.set_attribute("rag.source_count", len(docs))

        logger.info(
            "Agent completed | latency_ms=%s | tokens=%s | sources=%s",
            latency_ms,
            token_data,
            [doc["source"] for doc in docs]
        )

        return {
            "answer": answer,
            "sources": [doc["source"] for doc in docs],
            "latency_ms": latency_ms,
            "tokens": token_data
        }