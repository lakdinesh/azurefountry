from fastapi import FastAPI
from backend.app.schemas import ChatRequest, ChatResponse
from backend.app.foundry_agent import run_agent

app = FastAPI(
    title="Azure AI Foundry Agent API",
    version="1.0.0"
)

@app.get("/")
def health_check():
    return {"status": "running"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    answer = run_agent(request.message)

    return ChatResponse(
        answer=answer
    )