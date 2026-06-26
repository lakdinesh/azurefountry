import json
import re
import time

from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

from backend.app.config import settings
from backend.app.rag import retrieve_knowledge
from backend.app.guardrails import validate_input, validate_output
from backend.app.mcp_adapter import mcp_adapter
from backend.app.monitoring import tracer, logger

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "https://ai.azure.com/.default",
)

client = OpenAI(
    base_url=settings.AZURE_FOUNDRY_ENDPOINT,
    api_key=token_provider,
)


def detect_tool_call(user_message: str) -> dict | None:
    upper = user_message.upper()

    ticket_match = re.search(r"INC\d+", upper)

    if "STATUS" in upper and ticket_match:
        return {
            "tool_name": "get_ticket_status",
            "arguments": {
                "ticket_id": ticket_match.group(0)
            },
        }

    if "ESCALATE" in upper and ticket_match:
        return {
            "tool_name": "escalate_ticket",
            "arguments": {
                "ticket_id": ticket_match.group(0),
                "reason": user_message,
            },
        }

    return None


def run_enterprise_agent(user_message: str) -> dict:
    start = time.time()

    with tracer.start_as_current_span("agent.run") as span:
        valid, error = validate_input(user_message)

        if not valid:
            return {
                "answer": error,
                "sources": [],
                "tool_result": None,
                "latency_ms": 0,
                "tokens": {},
            }

        docs = retrieve_knowledge(user_message)

        context = "\n\n".join(
            f"Source: {doc['source']}\nContent: {doc['content']}"
            for doc in docs
        )

        tool_result = None
        tool_call = detect_tool_call(user_message)

        if tool_call:
            tool_result = mcp_adapter.call_tool(
                tool_call["tool_name"],
                tool_call["arguments"],
            )

        prompt = f"""
You are an Enterprise Support Agent.

Rules:
1. Answer only using the company documents and tool results.
2. Do not hallucinate.
3. If information is missing, say:
   "I don't know based on the available company documents."
4. Mention source names when possible.
5. Be concise and helpful.

Available MCP Tools:
{json.dumps(mcp_adapter.list_tools(), indent=2)}

Company Documents:
{context}

Tool Result:
{json.dumps(tool_result, indent=2) if tool_result else "No tool was used."}

User Question:
{user_message}
"""

        response = client.responses.create(
            model=settings.AZURE_MODEL_DEPLOYMENT,
            input=prompt,
            temperature=0.2,
        )

        answer = response.output_text

        output_valid, output_error = validate_output(answer)

        if not output_valid:
            answer = output_error

        usage = getattr(response, "usage", None)

        tokens = {
            "input_tokens": getattr(usage, "input_tokens", 0) if usage else 0,
            "output_tokens": getattr(usage, "output_tokens", 0) if usage else 0,
            "total_tokens": getattr(usage, "total_tokens", 0) if usage else 0,
        }

        latency_ms = round((time.time() - start) * 1000, 2)

        span.set_attribute("agent.latency_ms", latency_ms)
        span.set_attribute("agent.sources_count", len(docs))
        span.set_attribute("agent.total_tokens", tokens["total_tokens"])
        span.set_attribute("agent.tool_used", bool(tool_result))

        logger.info(
            "Agent completed latency=%s tokens=%s sources=%s",
            latency_ms,
            tokens,
            [doc["source"] for doc in docs],
        )

        return {
            "answer": answer,
            "sources": [doc["source"] for doc in docs],
            "tool_result": tool_result,
            "latency_ms": latency_ms,
            "tokens": tokens,
        }