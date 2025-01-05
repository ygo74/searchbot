from dotenv import load_dotenv
import os
import asyncio
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from autogen_core.models import UserMessage

async def main():

    # Get Configuration Settings
    load_dotenv()
    ai_endpoint = os.getenv('AZURE_OPENAI_API_ENDPOINT')
    ai_key = os.getenv('AZURE_OPENAI_API_KEY')

    az_model_client = AzureOpenAIChatCompletionClient(
        azure_deployment="gpt-4o",
        model="gpt-4o-2024-08-06",
        api_version="2024-06-01",
        azure_endpoint=ai_endpoint,
        api_key=ai_key
    )

    result = await az_model_client.create([UserMessage(content="What is the capital of France?", source="user")])
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
