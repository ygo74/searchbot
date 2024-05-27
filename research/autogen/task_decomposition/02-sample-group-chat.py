# https://microsoft.github.io/autogen/docs/topics/task_decomposition
# Approach 1. Two-agent chat with function call for task decomposition

import os
from datetime import datetime
from typing import Callable, Dict, Literal, Optional, Union

from typing_extensions import Annotated

import autogen
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
import argparse


def main():

    def custom_speaker_selection_func(last_speaker: Agent, groupchat: GroupChat):
        """Define a customized speaker selection function.
        A recommended way is to define a transition for each speaker in the groupchat.

        Returns:
            Return an `Agent` class or a string from ['auto', 'manual', 'random', 'round_robin'] to select a default method to use.
        """
        messages = groupchat.messages

        if len(messages) <= 1:
            # first, let the engineer retrieve relevant data
            return planner

        if last_speaker is planner:
            # if the last message is from planner, let the engineer to write code
            return engineer
        elif last_speaker is user_proxy:
            if messages[-1]["content"].strip() != "":
                # If the last message is from user and is not empty, let the writer to continue
                return writer

        elif last_speaker is engineer:
            if "```python" in messages[-1]["content"] or "pip install" in messages[-1]["content"]:
                # If the last message is a python code block, let the executor to speak
                return code_executor
            else:
                # Otherwise, let the engineer to continue
                return engineer

        elif last_speaker is code_executor:
            if "exitcode: 1" in messages[-1]["content"]:
                # If the last message indicates an error, let the engineer to improve the code
                return engineer
            else:
                # Otherwise, let the writer to speak
                return writer

        elif last_speaker is writer:
            # Always let the user to speak after the writer
            return user_proxy

        else:
            # default to auto speaker selection method
            return "auto"

    parser = argparse.ArgumentParser()
    parser.add_argument("--model_tag", help="models tag to filter used models", default="openai")
    args = parser.parse_args()

    # Get Configuration Settings
    print("Load azure environment variables")
    load_dotenv()
    ai_endpoint = os.getenv('AZURE_OPENAI_API_ENDPOINT')
    ai_key = os.getenv('AZURE_OPENAI_API_KEY')

    print(f"AZURE_OPENAI_API_ENDPOINT : {ai_endpoint}")

    available_config_list = [
        {
            "model": "gpt-35-turbo-16k",
            "api_type": "azure",
            "api_key": ai_key,
            "base_url": ai_endpoint,
            "api_version": "2024-02-15-preview",
            "tags": ["gpt35","openai"]
        },
        {
            "model": "gpt-4-32k",
            "api_type": "azure",
            "api_key": ai_key,
            "base_url": ai_endpoint,
            "api_version": "2024-02-15-preview",
            "tags": ["gpt4","openai"]
        },
    ]

    filter_dict = {"tags": [args.model_tag]}
    config_list = autogen.filter_config(available_config_list, filter_dict)
    assert len(config_list) > 0

    # You can also use the following method to load the config list from a file or environment variable.
    # config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")

    task = (
        f"Today is {datetime.now().date()}. Write a blogpost about the stock price performance of Nvidia in the past month."
    )
    print(task)

    user_proxy = UserProxyAgent(
        name="Admin",
        system_message="A human admin. Give the task, and send instructions to writer to refine the blog post.",
        code_execution_config=False,
    )

    planner = AssistantAgent(
        name="Planner",
        system_message="""Planner. Given a task, please determine what information is needed to complete the task.
    Please note that the information will all be retrieved using Python code. Please only suggest information that can be retrieved using Python code.
    """,
        llm_config={"config_list": config_list, "cache_seed": None},
    )

    engineer = AssistantAgent(
        name="Engineer",
        llm_config={"config_list": config_list, "cache_seed": None},
        system_message="""Engineer. You write python/bash to retrieve relevant information. Wrap the code in a code block that specifies the script type. The user can't modify your code. So do not suggest incomplete code which requires others to modify. Don't use a code block if it's not intended to be executed by the executor.
    Don't include multiple code blocks in one response. Do not ask others to copy and paste the result. Check the execution result returned by the executor.
    If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try.
    """,
    )

    writer = AssistantAgent(
        name="Writer",
        llm_config={"config_list": config_list, "cache_seed": None},
        system_message="""Writer. Please write blogs in markdown format (with relevant titles) and put the content in pseudo ```md``` code block. You will write it for a task based on previous chat history. Don't write any code.""",
    )

    os.makedirs("paper", exist_ok=True)
    code_executor = UserProxyAgent(
        name="Executor",
        system_message="Executor. Execute the code written by the engineer and report the result.",
        description="Executor should always be called after the engineer has written code to be executed.",
        human_input_mode="ALWAYS",
        code_execution_config={
            "last_n_messages": 3,
            "executor": DockerCommandLineCodeExecutor(work_dir="paper"),
        },
    )

    groupchat = GroupChat(
        agents=[user_proxy, engineer, code_executor, writer, planner],
        messages=[],
        max_round=20,
        speaker_selection_method=custom_speaker_selection_func,
    )
    manager = GroupChatManager(groupchat=groupchat, llm_config={"config_list": config_list, "cache_seed": None})

    # Use Cache.disk to cache LLM responses. Change cache_seed for different responses.
    with Cache.disk(cache_seed=41) as cache:
        chat_history = user_proxy.initiate_chat(
            manager,
            message=task,
            cache=cache,
        )

if __name__ == "__main__":
    main()
