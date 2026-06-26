import os
from pathlib import Path
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

load_dotenv()

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"

endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
key = os.getenv("AZURE_SEARCH_KEY")
index_name = os.getenv("AZURE_SEARCH_INDEX", "company-knowledge")

client = SearchClient(
    endpoint=endpoint,
    index_name=index_name,
    credential=AzureKeyCredential(key),
)

documents = []

for file in DATA_DIR.glob("*.txt"):
    documents.append({
        "id": file.stem.replace("_", "-").lower(),
        "content": file.read_text(encoding="utf-8"),
        "source": file.name,
    })

if not documents:
    raise RuntimeError("No .txt files found in data folder.")

result = client.upload_documents(documents=documents)

for item in result:
    print(item)