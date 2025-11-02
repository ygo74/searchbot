# pip install agent-framework --pre
# Use `az login` to authenticate with Azure CLI
import os
import asyncio

from agent_framework.openai import OpenAIResponsesClient


async def main():
    # Initialize a chat agent with Azure OpenAI Responses
    # the endpoint, deployment name, and api version can be set via environment variables
    # or they can be passed in directly to the AzureOpenAIResponsesClient constructor
    agent = OpenAIResponsesClient(
        model_id="gpt-4.1", # OPENAI_RESPONSES_MODEL_ID
        base_url="http://localhost:8000/v1", # OPENAI_BASE_URL => Use our OpenAI proxy endpoint
        api_key="sk-16AwYoZqNoVKjfMz-Mr8TeuaXk3O6JeLwPdQSAQiF0s" # OPENAI_API_KEY => Use OpenAI Proxy API key
    ).create_agent(
        name="HaikuBot",
        instructions="You are good at telling jokes.",
        temperature=0.7
    )

    print(await agent.run("Tell me a joke about a pirate."))

if __name__ == "__main__":
    asyncio.run(main())