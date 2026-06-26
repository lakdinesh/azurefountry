import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchableField,
)

load_dotenv()

endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
key = os.getenv("AZURE_SEARCH_KEY")
index_name = os.getenv("AZURE_SEARCH_INDEX", "company-knowledge")

client = SearchIndexClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key),
)

fields = [
    SimpleField(
        name="id",
        type="Edm.String",
        key=True,
        filterable=True,
    ),
    SearchableField(
        name="content",
        type="Edm.String",
        searchable=True,
        retrievable=True,
    ),
    SearchableField(
        name="source",
        type="Edm.String",
        searchable=True,
        filterable=True,
        retrievable=True,
    ),
]

index = SearchIndex(
    name=index_name,
    fields=fields,
)

try:
    client.delete_index(index_name)
    print(f"Deleted existing index: {index_name}")
except Exception:
    print("No existing index found.")

client.create_index(index)

print(f"Created index: {index_name}")