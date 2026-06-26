from fastapi import FastAPI, HTTPException

from backend.app.schemas import ChatRequest, ChatResponse
from backend.app.foundry_client import run_enterprise_agent
from backend.app.evaluation import run_basic_evaluation
from backend.app.monitoring import tracer, logger

app = FastAPI(
    title="Azure AI Foundry Enterprise Agent",
    version="1.0.0",
)

@app.get("/")
def health():
    return {
        "status": "running",
        "service": "azure-foundry-enterprise-agent",
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    with tracer.start_as_current_span("api.chat"):
        try:
            result = run_enterprise_agent(request.message)
            return ChatResponse(**result)
        except Exception as e:
            logger.exception("Chat failed")
            raise HTTPException(status_code=500, detail=str(e))


@app.post("/evaluate")
def evaluate():
    return run_basic_evaluation()