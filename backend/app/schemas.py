from typing import Any
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    answer: str
    sources: list[str]
    tool_result: dict[str, Any] | None
    latency_ms: float
    tokens: dict[str, Any]