import os
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient


def get_azure_model(deployment_name: str, model_name: str) -> AzureOpenAIChatCompletionClient:
    ai_endpoint = os.getenv('AZURE_OPENAI_API_ENDPOINT')
    ai_key = os.getenv('AZURE_OPENAI_API_KEY')

    az_model_client = AzureOpenAIChatCompletionClient(
        azure_deployment=deployment_name,
        model=model_name,
        api_version="2024-06-01",
        azure_endpoint=ai_endpoint,
        api_key=ai_key
    )

    return az_model_client
