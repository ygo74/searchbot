import os
import asyncio
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.ai.chat_completion_client_base import ChatCompletionClientBase
from semantic_kernel.contents import ChatHistory
from semantic_kernel import Kernel

from dotenv import load_dotenv

async def main():
    deployment_name = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

    chat_completion_service = AzureChatCompletion(
        deployment_name=deployment_name,
        api_key=api_key,
        endpoint=endpoint, # Used to point to your service
        service_id="my-service-id", # Optional; for targeting specific services within Semantic Kernel
    )

    # You can do the following if you have set the necessary environment variables or created a .env file
    chat_completion_service = AzureChatCompletion(service_id="my-service-id")

    # Initialize the kernel
    kernel = Kernel()

    # Add the chat completion service created above to the kernel
    kernel.add_service(chat_completion_service)


    # Retrieve the chat completion service by type
    chat_completion_service = kernel.get_service(type=ChatCompletionClientBase)

    # Retrieve the chat completion service by id
    chat_completion_service = kernel.get_service(service_id="my-service-id")

    # Retrieve the default inference settings
    execution_settings = kernel.get_prompt_execution_settings_from_service_id("my-service-id")

    chat_history = ChatHistory()
    chat_history.add_user_message("Hello, how are you?")

    response = await chat_completion_service.get_chat_message_content(
        chat_history=chat_history,
        settings=execution_settings,
    )

    print(response)


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())