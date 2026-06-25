from fastapi import FastAPI, HTTPException

from backend.app.schemas import ChatRequest, ChatResponse
from backend.app.foundry_agent import run_agent
from backend.app.monitoring import logger, tracer

app = FastAPI(
    title="Enterprise Support Agent API",
    version="1.0.0"
)

@app.get("/")
def health_check():
    return {
        "status": "running",
        "service": "enterprise-support-agent"
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    with tracer.start_as_current_span("chat_api_request"):
        try:
            result = run_agent(request.message)
            return ChatResponse(**result)

        except Exception as e:
            logger.exception("Chat endpoint failed")
            raise HTTPException(
                status_code=500,
                detail=str(e)
            )