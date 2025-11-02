# Copyright (c) Microsoft. All rights reserved.

import asyncio

from agent_framework import ChatMessage, TextContent, UriContent, DataContent
from agent_framework.openai import OpenAIResponsesClient
from dotenv import load_dotenv

"""
OpenAI Responses Client Image Analysis Example

This sample demonstrates using OpenAI Responses Client for image analysis and vision tasks,
showing multi-modal content handling with text and images.
"""


async def main():
    print("=== OpenAI Responses Agent with Image Analysis ===")

    # Load the environment variables
    load_dotenv()

    # Load image from local file
    with open("C:\\Users\\Administrator\\Pictures\\226px-Jenkins_logo.svg.png", "rb") as f:
        image_bytes = f.read()

    # 1. Create an OpenAI Responses agent with vision capabilities
    agent = OpenAIResponsesClient().create_agent(
        name="VisionAgent",
        instructions="You are a helpful agent that can analyze images.",
    )

    # 2. Create a simple message with both text and image content
    user_message = ChatMessage(
        role="user",
        contents=[
            TextContent(text="What do you see in this image?"),
            # UriContent(
            #     uri="https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
            #     media_type="image/jpeg",
            # ),
            DataContent(
                data=image_bytes,
                media_type="image/png",
            ),
        ],
    )

    # 3. Get the agent's response
    print("User: What do you see in this image? [Image provided]")
    result = await agent.run(user_message)
    print(f"Agent: {result.text}")
    print()


if __name__ == "__main__":
    asyncio.run(main())