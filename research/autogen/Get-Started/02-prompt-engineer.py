from dotenv import load_dotenv
import os
import asyncio

from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent

from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken

from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient


# Define prompt engineer prompt
prompt_engineer_system_message = """
I want you to act as an expert engineer in ChatGPT prompts with expertise in all fields.
Throughout our interaction, you will address me as {My dear colleague}.
Use default commands like /role_play "Expert ChatGPT Prompt Engineer" and /role_play "infinite subject matter expert" to adjust your behavior.

If a response exceeds the character limit, continue automatically and inform me with the ♻️ emoji.
Conduct periodic reviews of the entire conversation and use the 🧐 emoji to indicate it.

Also, use other indicators like 🧠 for context and 🔍 to ask direct questions to a specific expert.

To collaborate in creating the best possible response to a prompt I provide, here are the steps:
1. I will inform you how you can assist me.
2. You will suggest expert roles based on my needs.
3. You will adopt these roles if I agree or modify them if I do not.
4. You will confirm active expert roles and their associated skills, randomly assigning emojis to these roles.
5. You will ask me how you can assist me with my response to the first step.
6. I will provide my response.
7. You will ask me for reference sources if necessary and how I want them to be used.
8. I will provide these sources if necessary.
9. You will ask for more details based on my responses to steps 1, 2, and 8.
10. I will provide these details.
11. You will generate a new prompt based on confirmed roles and my responses.
12. You will present this new prompt and ask for my opinion.
13. You will revise or execute the prompt based on my feedback.
14. Once the response is complete, you will ask if any modifications are needed.

If you understand your mission, respond with "How can I assist you today, My dear colleague? (🧠)."
"""


async def main():

    # Get Configuration Settings
    load_dotenv()
    ai_endpoint = os.getenv('AZURE_OPENAI_API_ENDPOINT')
    ai_key = os.getenv('AZURE_OPENAI_API_KEY')

    ai_endpoint = os.getenv('AZURE_OPENAI_API_ENDPOINT')
    ai_key = os.getenv('AZURE_OPENAI_API_KEY')

    az_model_client = AzureOpenAIChatCompletionClient(
        azure_deployment="gpt-4o",
        model="gpt-4o-2024-08-06",
        api_version="2024-06-01",
        azure_endpoint=ai_endpoint,
        api_key=ai_key
    )


    # Create the prompt engineer agent
    prompt_engineer_agent = AssistantAgent(
        "prompt_engineer",
        model_client=az_model_client,
        system_message=prompt_engineer_system_message
    )

    user_proxy_agent   = UserProxyAgent(
        name="human_proxy"
    )

    # Create the critic agent.
    critic_agent = AssistantAgent(
        "critic",
        model_client=az_model_client,
        system_message="Provide constructive feedback. Respond with 'APPROVE' to when your feedbacks are addressed.",
    )

    # response = await user_proxy_agent.on_messages(
    #         [TextMessage(content="What is your name? ", source="user")], cancellation_token=CancellationToken()
    # )

    # print(f"Your name is {response.chat_message.content}")

    # Define a termination condition that stops the task if the critic approves.
    text_termination = TextMentionTermination("APPROVE")
    # Define a termination condition that stops the task after 15 messages.
    max_message_termination = MaxMessageTermination(15)
    # Combine the termination conditions using the `|`` operator so that the
    # task stops when either condition is met.
    termination = text_termination | max_message_termination

    # Create a team with the primary and critic agents.
    reflection_team = RoundRobinGroupChat(
        participants=[
            prompt_engineer_agent,
            critic_agent
        ],
        termination_condition=termination
    )

    # Use `asyncio.run(Console(reflection_team.run_stream(task="Write a short poem about fall season.")))` when running in a script.
    await Console(
        reflection_team.run_stream(task="Create a system prompt to act as a Solution Architect for dotnet")
    )  # Stream the messages to the console.

if __name__ == "__main__":
    asyncio.run(main())
