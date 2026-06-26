from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

from backend.app.config import settings
from backend.app.monitoring import tracer, logger

search_client = SearchClient(
    endpoint=settings.AZURE_SEARCH_ENDPOINT,
    index_name=settings.AZURE_SEARCH_INDEX,
    credential=AzureKeyCredential(settings.AZURE_SEARCH_KEY),
)

def retrieve_knowledge(query: str, top: int = 5) -> list[dict]:
    with tracer.start_as_current_span("rag.retrieve") as span:
        span.set_attribute("rag.query", query)
        span.set_attribute("rag.top", top)

        results = search_client.search(
            search_text=query,
            top=top,
        )

        docs = []

        for item in results:
            docs.append({
                "id": item.get("id", ""),
                "content": item.get("content", ""),
                "source": item.get("source", "unknown"),
            })

        logger.info("RAG returned %s documents", len(docs))
        span.set_attribute("rag.result_count", len(docs))

        return docs