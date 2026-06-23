from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from app.config import settings

client = SearchClient(
    endpoint=settings.AZURE_SEARCH_ENDPOINT,
    index_name=settings.AZURE_SEARCH_INDEX,
    credential=AzureKeyCredential(settings.AZURE_SEARCH_KEY)
)

documents = [
    {
        "id": "1",
        "content": "Employees can reset password using the self-service password reset portal.",
        "source": "IT Policy"
    },
    {
        "id": "2",
        "content": "Critical incidents must be escalated to L2 support within 30 minutes.",
        "source": "Incident Policy"
    },
    {
        "id": "3",
        "content": "VPN access requires MFA authentication using Microsoft Entra ID.",
        "source": "Security Policy"
    }
]

client.upload_documents(documents=documents)

print("Documents uploaded successfully.")