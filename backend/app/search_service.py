from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

from backend.app.config import settings
from backend.app.monitoring import tracer, logger

search_client = SearchClient(
    endpoint=settings.AZURE_SEARCH_ENDPOINT,
    index_name=settings.AZURE_SEARCH_INDEX,
    credential=AzureKeyCredential(settings.AZURE_SEARCH_KEY)
)

def search_company_knowledge(query: str, top: int = 3):
    with tracer.start_as_current_span("azure_ai_search_retrieval") as span:
        span.set_attribute("search.query", query)
        span.set_attribute("search.top", top)

        results = search_client.search(
            search_text=query,
            top=top
        )

        documents = []

        for result in results:
            documents.append({
                "content": result.get("content", ""),
                "source": result.get("source", "unknown")
            })

        span.set_attribute("search.result_count", len(documents))
        logger.info("Search returned %s documents", len(documents))

        return documents