# https://microsoft.github.io/autogen/docs/topics/task_decomposition
# Approach 1. Two-agent chat with function call for task decomposition

import os
from datetime import datetime
from typing import Callable, Dict, Literal, Optional, Union

from typing_extensions import Annotated

from autogen import (
    Agent,
    AssistantAgent,
    ConversableAgent,
    GroupChat,
    GroupChatManager,
    UserProxyAgent,
    config_list_from_json,
    register_function,
)
from autogen.agentchat.contrib import agent_builder
from autogen.cache import Cache
from autogen.coding import DockerCommandLineCodeExecutor, LocalCommandLineCodeExecutor

from dotenv import load_dotenv

# Get Configuration Settings
print("Load azure environment variables")
load_dotenv()
ai_endpoint = os.getenv('AZURE_OPENAI_API_ENDPOINT')
ai_key = os.getenv('AZURE_OPENAI_API_KEY')

print(f"AZURE_OPENAI_API_ENDPOINT : {ai_endpoint}")

config_list = [
    {
        "model": "gpt-35-turbo-16k",
        "api_type": "azure",
        "api_key": ai_key,
        "base_url": ai_endpoint,
        "api_version": "2024-02-15-preview",
        "tags": "openai"
    },
]


# You can also use the following method to load the config list from a file or environment variable.
# config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")

task = (
    f"Today is {datetime.now().date()}. Write a blogpost about Yannick Gobert development activities on github. His account is ygo74."
)
print(task)

# Create planner agent.
planner = AssistantAgent(
    name="planner",
    llm_config={
        "config_list": config_list,
        "cache_seed": None,  # Disable legacy cache.
    },
    system_message="You are a helpful AI assistant. You suggest a feasible plan "
    "for finishing a complex task by decomposing it into 3-5 sub-tasks. "
    "If the plan is not good, suggest a better plan. "
    "If the execution is wrong, analyze the error and suggest a fix.",
)

# Create a planner user agent used to interact with the planner.
planner_user = UserProxyAgent(
    name="planner_user",
    human_input_mode="NEVER",
    code_execution_config=False,
)

# The function for asking the planner.


def task_planner(question: Annotated[str, "Question to ask the planner."]) -> str:
    with Cache.disk(cache_seed=4) as cache:
        planner_user.initiate_chat(planner, message=question, max_turns=1, cache=cache)
    # return the last message received from the planner
    return planner_user.last_message()["content"]

# Create assistant agent.
assistant = AssistantAgent(
    name="assistant",
    system_message="You are a helpful AI assistant. "
    "You can use the task planner to decompose a complex task into sub-tasks. "
    "Make sure your follow through the sub-tasks. "
    "When needed, write Python code in markdown blocks, and I will execute them."
    "Give the user a final solution at the end. "
    "Return TERMINATE only if the sub-tasks are completed.",
    llm_config={
        "config_list": config_list,
        "cache_seed": None,  # Disable legacy cache.
    },
)

# Setting up code executor.
os.makedirs("planning", exist_ok=True)
# Use DockerCommandLineCodeExecutor to run code in a docker container.
code_executor = DockerCommandLineCodeExecutor(work_dir="planning")
# code_executor = LocalCommandLineCodeExecutor(work_dir="planning")

# Create user proxy agent used to interact with the assistant.
user_proxy = UserProxyAgent(
    name="user_proxy",
    human_input_mode="ALWAYS",
    is_termination_msg=lambda x: "content" in x
    and x["content"] is not None
    and x["content"].rstrip().endswith("TERMINATE"),
    code_execution_config={"executor": code_executor},
)

# Register the function to the agent pair.
register_function(
    task_planner,
    caller=assistant,
    executor=user_proxy,
    name="task_planner",
    description="A task planner than can help you with decomposing a complex task into sub-tasks.",
)

# Use Cache.disk to cache LLM responses. Change cache_seed for different responses.
with Cache.disk(cache_seed=1) as cache:
    # the assistant receives a message from the user, which contains the task description
    user_proxy.initiate_chat(
        assistant,
        message=task,
        cache=cache,
    )