from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from backend.app.config import settings

search_client = SearchClient(
    endpoint=settings.AZURE_SEARCH_ENDPOINT,
    index_name=settings.AZURE_SEARCH_INDEX,
    credential=AzureKeyCredential(settings.AZURE_SEARCH_KEY)
)

def search_company_knowledge(query: str, top: int = 3):
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

    return documents