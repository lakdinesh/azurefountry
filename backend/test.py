# test_foundry.py

from openai import OpenAI
from azure.identity import (
    DefaultAzureCredential,
    get_bearer_token_provider
)

endpoint = "https://lakdinesh11-0217-resource.services.ai.azure.com/openai/v1"

deployment_name = "gpt-4o"

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "https://ai.azure.com/.default"
)

client = OpenAI(
    base_url=endpoint,
    api_key=token_provider
)

response = client.responses.create(
    model=deployment_name,
    input="hello"
)

print(response.output_text)